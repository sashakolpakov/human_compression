#!/usr/bin/env python3
"""Build documentary/logical graphs from fixed existing Topic D proofs; no text weights."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
LOGICAL=['proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use']
OTHER=['attribution','validation','formal_scope','comparison','operational']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists() or a.out.is_symlink():raise ValueError('fresh output required')
 a.out.mkdir(parents=True);roots={'research':a.study_root,'public':a.public_root};base='papers/topic-d/v2/'
 scope=json.loads((a.public_root/base/'scope.json').read_text());nodes={};edges=[];inputs={}
 def bind(ns,path):
  b=(roots[ns]/path).read_bytes();r=dict(namespace=ns,path=path,bytes=len(b),sha256=SHA(b));inputs[ns,path]=r;return r
 def loc(ns,path,start=0,end=None,**extra):
  bind(ns,path);t=(roots[ns]/path).read_text();end=len(t) if end is None else end
  if not 0<=start<end<=len(t):raise ValueError((path,start,end))
  return dict(namespace=ns,path=path,start_codepoint=start,end_codepoint_exclusive=end,first_line=t.count('\n',0,start)+1,last_line=t.count('\n',0,end-1)+1,sha256_utf8=SHA(t[start:end].encode()),scope='Statement/proof context; overlapping locator, not exclusive cost ownership',**extra)
 span={k:loc('public',base+v['path'],v['start_codepoint'],v['end_codepoint_exclusive'],accepted_span=k) for k,v in scope['proof_spans'].items()}
 sourcebindings={};sourcepages={}
 for key,s in scope['sources'].items():
  pr=bind('research',s['primary']['path']);tp='sources/catalogue_'+key+'.txt';tb=bind('research',tp);t=(a.study_root/tp).read_text();marks=list(re.finditer(r'--- PDF PAGE (\d+) ---\n',t));sourcepages[key]={}
  for i,m in enumerate(marks):sourcepages[key][int(m.group(1))]=loc('research',tp,m.end(),marks[i+1].start() if i+1<len(marks) else len(t),physical_page=int(m.group(1)),primary_pdf_sha256=pr['sha256'])
  sourcebindings[key]=dict(**s,original_pdf_available=True,pdf_cost=None,text_cost=None,primary_binding=pr,documentary_extraction_binding=tb,source_text_distributed=False)
 def sl(key,pages):return [sourcepages[key][p] for p in pages]
 def add(id,label,doc,side,category,locators,flags=None,scope_note=None):
  if id in nodes:raise ValueError(id)
  nodes[id]=dict(id=id,label=label,document=doc,side=side,category=category,locators=locators,cost=None,cost_status='unmeasured; retained external proof and graphic costs unknown',documentary_flags=flags or [],scope_note=scope_note)
 def n(id,label,spans,category='proved_statement',flags=None):add(id,label,'U_D' if id.startswith('UD.') else id.split('.')[0], 'new',category,[span[x] for x in spans],flags)
 def ext(id,label,locators,note):add(id,label,'EXTERNAL','external','retained_input',locators,scope_note=note)
 def edge(s,t,k='proof_use',why=None):
  if s not in nodes or t not in nodes:raise ValueError((s,t))
  if any((e['source'],e['target'],e['kind'])==(s,t,k) for e in edges):return
  edges.append(dict(source=s,target=t,kind=k,evidence=why or 'Used in the displayed target proof/context; this is a direct use, not a minimal-axiom assertion.',target_evidence=nodes[t]['locators'],necessity_claim=False))
 def uses(t,ss,k='proof_use',why=None):
  for s in ss:edge(s,t,k,why)
 # Common written proof interfaces, split by actual mathematical argument.
 for id,label,sp in [
 ('UD.OrbitData','Transitive A/H orbit data, multiplicities and action kernel',['Actions.1']),
 ('UD.Centralizer','Equivariant permutations: normalizer quotients and wreath factors',['Actions.1']),
 ('UD.Normalizer','Faithful action normalizer exact sequence; no splitting asserted',['Actions.1']),
 ('UD.ExtensionOrbits','Equivariant fibers classified by stabilizer orbits',['Actions.1']),
 ('UD.AdmissibleExtensions','Invariant admissibility and exact support: fiber decomposition and fixed-point sum',['Support.1']),
 ('UD.ExactSupport','One-base exact-support orbit count',['Support.1']),
 ('UD.Reversal','Involution orbits include the fixed-point correction',['Support.1']),
 ('UD.OddOrbits','Free commuting involution stays free on odd group orbits',['Support.1']),
 ('UD.FieldSupport','Divisor support inversion conditional on the actual least-field adapter',['Support.1']),
 ('UD.Helly','Anchored typed coset-Helly criterion',['Panels.Helly']),
 ('UD.CosetRealization','Flag-transitive geometry reconstructed from stabilizer cosets',['Panels.1']),
 ('UD.PanelRecognition','Arbitrary Borel panel recognition: E4, firmness, flags and residues',['Panels.1']),
 ('UD.LocalTests','RWPRI, two-transitivity and IP2 reduced to subgroup/residue tests',['Panels.1']),
 ('UD.Transport','Every inclusion reconstructed by normalizer transporters',['Panels.2']),
 ('UD.MaximalAugmentation','Complete augmentation through maximal residues and stabilizer fibers',['Panels.2']),
 ('UD.Termination','Strict generated joins and empty terminal level give the rank exclusion',['Panels.2'])]:n(id,label,sp)
 n('UD.Conventions','Finite type conventions, coset incidence, string C-group definition',['U.Conventions'],'definition')
 n('UD.PolytopeInterface','Regular-polytope/string-C-group correspondence is retained',['U.Conventions'],'retained_input_context')
 ext('ext.Mobius','Incidence-algebra Möbius inverse identity; divisor specialization',[span['Support.1'],*sl('L074',[7,8])],'Classical identity; the finite fixed-point/Burnside double count is written in U_D. The divisor-poset/number-theoretic bridge is a separate classical specialization, not automatically formalized by the support supplement.')
 ext('ext.FiniteGroups','Elementary finite group/action facts: orbit-stabilizer, cosets, odd periods',[span['Actions.1'],span['Support.1']],'Ordinary background, not a hidden source classification.')
 ext('ext.Polytope','Regular abstract polytopes and string C-groups',[span['U.Conventions'],*sl('L066',[7]),*sl('L074',[5])],'McMullen–Schulte correspondence retained; not rederived by finite IP tests.')
 ext('ext.PermutationAut','Ordinary automorphisms of symmetric and alternating groups; degree-six exception',[span['A1.2'],*sl('L066',[3,8])],'Aut(S_N) and Aut(A_N) induced by ambient permutations in the stated ordinary degrees; exceptional degree six is not inferred from this input.')
 ext('ext.WilsonCentralizer','Classical involution centralizers in S_N/A_N',[*sl('L066',[3,7])],'Historical source cites Wilson; current wreath and sign derivations are written from UD.OrbitData/UD.Centralizer, so this is not an unpriced current premise.')
 ext('ext.SuzukiRoots','Finite Suzuki root groups, ovoid action, involution centralizers and two-point torus',[span['A2.1'],*sl('L074',[3,4,5])],'Suzuki/Lüneburg finite structure retained, including regular U action away from the fixed point, central involutions and root-coordinate torus action.')
 ext('ext.SuzukiMaximals','Suzuki 1962 maximal subgroups and odd-torus centralizer/normalizer structure',[span['A2.1'],*sl('L074',[4])],'Classification retained, not derived from orbit counting or sampling.')
 ext('ext.SuzukiAut','Aut(Sz(2^N)), canonical subfields, simplicity and field action',[span['A2.1'],span['A2.3'],*sl('L074',[5,6,9])],'Classical automorphism/subfield/simple-group structure retained. Local normalization, generation and rank deductions are written.')
 ext('ext.FiniteFields','Finite field subfield lattice and cyclic Frobenius fixed fields',[span['A2.4'],span['A2.5'],span['A2.6']],'Standard finite-field structure retained; all least-field, orbit-length and divisor adapters are proved at use.')
 ext('ext.LuneburgGeneral','Lüneburg general-field Suzuki/Bruhat and ovoid results',[*sl('L074',[3,4])],'Historical Lemmas 1–3 quote broader background. Current proof retains only specified finite structure; arbitrary-field Bruhat and general plane-section claims are not rederived.')
 ext('ext.Leemans1998','Earlier Suzuki geometry result behind source torus-order coprimality',[*sl('L074',[4])],'Historical attribution for Lemma 4. Current IP proof does not use this coprimality lemma.')
 ext('ext.Leemans2006','Earlier almost-simple Suzuki C-group/rank theorem',[*sl('L074',[5])],'Historical Theorem 3 is explicitly quoted from 2006. Current D2 rederives the admitted restatement; no extra L085 manuscript credit.')
 ext('ext.Fermat','Fermat congruence',[*sl('L074',[6]),span['A2.6']],'Classical source background; no new result and no premise of the new uniform formulas.')
 ext('ext.LeemansVauthier','Leemans–Vauthier 2006 prior S6 polyhedron classification',[*sl('L066',[7]),span['A1.4']],'Attribution only in the current recovery; current finite enumeration is independently specified.')
 ext('ext.TomLib','Complete J2 subgroup-class/maximal-inclusion catalogue (TomLib)',[span['A3.1']],'Required current computational input: catalogue completeness is retained, not proved by the search. Do not retroactively attribute TomLib to the 2002 source.')
 ext('ext.GAP','Exact GAP subgroup, automorphism, transporter, orbit and membership operations',[span['A1.3'],span['A3.1']],'Required exact algorithm implementations retained. Their implementation/construction cost is unknown.')
 ext('ext.J2Structure','J2 and full automorphism group data, simplicity',[span['A3.1'],span['Census.1']],'Actual group representation and full automorphism group retained. Simplicity gives final action faithfulness; auxiliary normalizer permutation images need not be faithful.')
 ext('ext.MagmaPrior','Historical Magma implementation and Dehon–Leemans geometry algorithms',[*sl('L104',[1,2])],'Source uses Magma and earlier algorithms for nontrivial Borel. No assertion that historical code is the current GAP code; original implementation cost unknown.')
 ext('ext.J2HistoricalSubgroups','Historical maximal-subgroup data and Pahlings subgroup-pattern reference',[*sl('L104',[2,4,5])],'Maximal residue enumeration uses group data; Pahlings is explicitly cited for the supplement subgroup pattern. Exact historical catalogue construction/call chain is not reconstructed.')
 ext('ext.J2Secondary','Prior J2 geometry construction, Pasini/Leemans doubling and supplement annotations',[*sl('L104',[3,4,5])],'Printed secondary claims only; not a premise asserting their recovery.')
 uses('UD.Centralizer',['UD.OrbitData']);uses('UD.Normalizer',['UD.OrbitData','UD.Centralizer']);uses('UD.OrbitData',['ext.FiniteGroups'],'retained_input_use')
 uses('UD.AdmissibleExtensions',['UD.ExtensionOrbits']);uses('UD.AdmissibleExtensions',['ext.Mobius','ext.FiniteGroups'],'retained_input_use')
 uses('UD.ExactSupport',['UD.AdmissibleExtensions']);uses('UD.Reversal',['UD.ExactSupport']);uses('UD.OddOrbits',['ext.FiniteGroups'],'retained_input_use');uses('UD.FieldSupport',['UD.ExactSupport','UD.OddOrbits']);uses('UD.FieldSupport',['ext.Mobius'],'retained_input_use')
 uses('UD.PolytopeInterface',['ext.Polytope'],'retained_input_use');uses('UD.CosetRealization',['UD.Conventions'],'definition_use');uses('UD.PanelRecognition',['UD.Helly','UD.CosetRealization']);uses('UD.LocalTests',['UD.PanelRecognition']);uses('UD.MaximalAugmentation',['UD.Transport','UD.ExtensionOrbits','UD.PanelRecognition','UD.LocalTests']);uses('UD.Termination',['UD.PanelRecognition','UD.MaximalAugmentation'])
 # Local complete written arguments. No preceding combined manuscript is a logical premise.
 definitions=[
 ('D1.Multiplicities','Marked V4 multiplicities, faithfulness and endpoint parity',['A1.1']),
 ('D1.Centralizers','C2 orbit centralizers and alternating sign kernel',['A1.1']),
 ('D1.Ordered','Reversible coordinates and ordered symmetric pair formula',['A1.2']),
 ('D1.Reversal','Endpoint exchange fixed orbits from x=y, with repaired proof',['A1.2']),
 ('D1.Symmetric','Symmetric unordered-pair floor formula in ordinary degrees',['A1.2']),
 ('D1.EvenOrdered','Even endpoint restrictions and ordered alternating formula',['A1.2']),
 ('D1.Alternating','Alternating unordered-pair formula in ordinary degrees',['A1.2']),
 ('D1.DegreeParity','Adding/removing a fixed point in the permutation-conjugacy orbit count',['A1.2']),
 ('D1.Exceptional','Full Aut(S6)/Aut(A6) endpoint, middle, generation and all-IP classification',['A1.3']),
 ('D1.Polyhedra','Exactly two regular S6 polyhedra; no regular A6 polyhedron',['A1.3']),
 ('D1.Table','All fourteen printed table rows, including small and exceptional degrees',['A1.4']),
 ('D1.Series','Additional rational generating series from direct multiplicity counting',['A1.2']),
 ('D2.Normalization','Canonical (b,c) coordinates and actual Frobenius/duality actions',['A2.1']),
 ('D2.SubfieldPosition','Two-point torus argument makes containing subfield canonical',['A2.2']),
 ('D2.Generation','Generated group is exactly Sz of the joint coordinate field',['A2.2']),
 ('D2.IP','Odd rotations and torus normalizers prove every required intersection',['A2.3']),
 ('D2.Rank','Rank exactly three; almost-simple extension excluded and existence proved',['A2.3']),
 ('D2.Support','Actual least-field support and free exact-degree Frobenius action',['A2.4']),
 ('D2.Pairs','All odd N endpoint-pair formula via degree and inversion',['A2.4']),
 ('D2.Duality','Duality is fixed-point-free on odd Frobenius orbits',['A2.1','A2.4']),
 ('D2.Polyhedra','All odd N regular-polyhedron count E(N)/(2N) and non-self-duality',['A2.4']),
 ('D2.Fibers','First-coordinate degree and stabilizer-fiber count psi',['A2.5']),
 ('D2.Nested','Exact equivalence with the printed nested Möbius formula and subfield count',['A2.5']),
 ('D2.PrimeExamples','Prime specialization and exact N=15 source examples',['A2.4','A2.6']),
 ('D2.FrobeniusRoot','Square root of Frobenius from the cyclic field automorphism group',['A2.6']),
 ('D2.InvolutionCount','Involution count from unique fixed points and root centers',['A2.6']),
 ('D3.Interfaces','Exact catalogue, subgroup transport, normalizer images and equivalence',['A3.1']),
 ('D3.Candidates','Exhaustive all-Borel augmentation: 644/1226/1931/271/0 candidates',['Census.1','A3.1']),
 ('D3.Fusion','Full automorphism/type fusion yields 8/19/3 classes',['Census.1','A3.1']),
 ('D3.Verified','All thirty representatives satisfy all stated geometric axioms',['Census.1','A3.1']),
 ('D3.NoHigher','Empty terminal level excludes every rank at least five',['Census.1']),
 ('D3.Faithfulness','Final J2 action faithful; no faithfulness assumed for auxiliary images',['A3.1'])]
 for id,title,sp in definitions:n(id,title,sp)
 for id,title,sp in [('D1.Qualifications','Endpoint reversal is not unconditional completed-triple self-duality; regular context and original attribution',['A1.4']),('D2.RetainedBoundary','Exact finite retained structure, unused/general background and original attribution',['A2.6']),('D3.Exclusions','Printed diagrams, complete Aut/Cor, doubling and supplement annotations excluded',['A3.2'])]:n(id,title,sp,'scope_context')
 uses('D1.Multiplicities',['UD.OrbitData']);uses('D1.Centralizers',['UD.Centralizer']);uses('D1.Ordered',['D1.Multiplicities']);uses('D1.Reversal',['D1.Multiplicities','D1.Ordered']);uses('D1.Symmetric',['D1.Ordered','D1.Reversal','UD.Reversal']);uses('D1.Symmetric',['ext.PermutationAut'],'retained_input_use');uses('D1.EvenOrdered',['D1.Multiplicities','D1.Ordered']);uses('D1.Alternating',['D1.EvenOrdered','D1.Reversal','UD.Reversal']);uses('D1.Alternating',['ext.PermutationAut'],'retained_input_use');uses('D1.DegreeParity',['D1.Multiplicities']);uses('D1.Series',['D1.Multiplicities'],why='CPI10 counts weights, endpoint parity and the unfaithful multiplicity tuples directly; it does not sum CPI5 or the reversal fixed-count formula.');uses('D1.Exceptional',['UD.ExtensionOrbits']);uses('D1.Polyhedra',['D1.Exceptional','UD.PolytopeInterface']);uses('D1.Table',['D1.Symmetric','D1.Alternating','D1.Exceptional','D1.DegreeParity'])
 uses('D2.Normalization',['ext.SuzukiRoots','ext.SuzukiAut','ext.FiniteFields'],'retained_input_use');uses('D2.SubfieldPosition',['D2.Normalization']);uses('D2.Generation',['D2.SubfieldPosition']);uses('D2.Generation',['ext.SuzukiMaximals'],'retained_input_use');uses('D2.IP',['D2.Generation']);uses('D2.IP',['ext.SuzukiRoots','ext.SuzukiMaximals'],'retained_input_use');uses('D2.Rank',['D2.Generation','D2.IP']);uses('D2.Rank',['ext.SuzukiRoots','ext.SuzukiAut','UD.PolytopeInterface'],'retained_input_use');uses('D2.Support',['D2.Normalization','D2.Generation','UD.ExactSupport']);uses('D2.Support',['ext.FiniteFields'],'retained_input_use');uses('D2.Pairs',['D2.Normalization','UD.FieldSupport','UD.OddOrbits']);uses('D2.Pairs',['ext.FiniteFields'],'retained_input_use');uses('D2.Duality',['D2.Normalization','UD.OddOrbits']);uses('D2.Polyhedra',['D2.Support','D2.Duality','D2.IP','D2.Rank','UD.FieldSupport','UD.PolytopeInterface']);uses('D2.Fibers',['D2.Normalization','UD.ExtensionOrbits','UD.ExactSupport']);uses('D2.Fibers',['ext.FiniteFields'],'retained_input_use');uses('D2.Nested',['D2.Fibers','D2.Support','D2.Polyhedra']);uses('D2.Nested',['ext.Mobius'],'retained_input_use');uses('D2.PrimeExamples',['D2.Pairs','D2.Polyhedra','D2.Nested']);uses('D2.FrobeniusRoot',['ext.FiniteFields'],'retained_input_use');uses('D2.InvolutionCount',['ext.SuzukiRoots'],'retained_input_use')
 uses('D3.Interfaces',['UD.Transport','UD.CosetRealization','UD.ExtensionOrbits']);uses('D3.Interfaces',['ext.TomLib','ext.GAP','ext.J2Structure'],'retained_input_use');uses('D3.Candidates',['UD.MaximalAugmentation','D3.Interfaces']);uses('D3.Fusion',['D3.Candidates','D3.Interfaces']);uses('D3.Verified',['D3.Fusion','UD.PanelRecognition','UD.LocalTests']);uses('D3.NoHigher',['D3.Candidates','UD.Termination']);uses('D3.Faithfulness',['UD.CosetRealization']);uses('D3.Faithfulness',['ext.J2Structure'],'retained_input_use')
 # Full code files: required mathematical work, diagnostics and operational drivers.
 programids={'phase110_commuting_pairs_integration_finite.g':'program.exceptional','phase5_j2_search.g':'program.search','phase5_j2_fuse.g':'program.fusion','phase5_j2_verify.g':'program.verify','phase4_geometry_checks.g':'program.predicates','phase110_commuting_pairs_integration_formula.py':'diagnostic.pairs','phase10_suzuki_marked_fields_check.py':'diagnostic.fields','phase10_suzuki_marked_groups_check.g':'diagnostic.q8','phase110_commuting_pairs_integration_run.py':'driver.pairs','phase164_enumeration_run.py':'driver.enumeration'}
 for p in scope['program_inventory']:
  id=programids[p['path']];required=id.startswith('program.');add(id,p['role'],'PROGRAMS','new' if required else 'verification','required_program' if required else 'diagnostic' if id.startswith('diagnostic.') else 'operational_driver',[loc('public',base+p['copy'])],scope_note='Whole unchanged file; not a selected favorable branch.')
 uses('program.exceptional',['ext.GAP'],'retained_input_use');uses('D1.Exceptional',['program.exceptional'])
 uses('program.predicates',['UD.PanelRecognition','UD.LocalTests']);uses('program.search',['UD.PanelRecognition','UD.LocalTests','UD.MaximalAugmentation','D3.Interfaces'],why='The standalone search implements its own FlagTransitive, RankTwoAdmissible and ValidPanels predicates; it does not read phase4_geometry_checks.g.');uses('program.fusion',['D3.Interfaces']);uses('program.verify',['program.predicates']);uses('D3.Candidates',['program.search']);uses('D3.Fusion',['program.fusion']);uses('D3.Verified',['program.verify'])
 for d,ts in [('diagnostic.pairs',['D1.Symmetric','D1.Alternating','D1.Series']),('diagnostic.fields',['D2.Pairs','D2.Polyhedra','D2.Nested']),('diagnostic.q8',['D2.Normalization','D2.Generation','D2.IP'])]:uses(d,ts,'validation','Finite diagnostic of the target formulas/construction; no implication from these samples to the all-parameter theorem.')
 uses('driver.pairs',['program.exceptional','diagnostic.pairs'],'operational','Runs the unchanged files and validates outputs; no extra mathematical premise.')
 uses('driver.enumeration',['program.search','program.fusion','program.verify','program.predicates','diagnostic.fields','diagnostic.q8'],'operational','Only admitted small/J2 branches selected; whole driver retains historical unused M22 code. This is operational provenance.')
 # Every named accepted historical row, including explicit ancillary exclusions.
 for r in scope['contracts']:
  flags=[]
  if r['id']=='L066.5':flags=['The statement is retained; the printed proof inference about conjugating one endpoint does not establish simultaneous conjugation. Current multiplicity proof repairs it.']
  if r['id']=='L066.6':flags=['Read only as endpoint reversal. It does not establish self-duality of every completed generating triple.']
  if r['id']=='L066.13':flags=['Regular-polyhedron context retained; no exclusion of every nonregular polyhedron.']
  if r['id'] in ['L074.6','L074.7']:flags=['Full general-field/ovoid statement exceeds current retained finite scope.']
  if r['id']=='L104.4':flags=['Printed-main-body and supplement assertions are explicitly outside the current principal recovery.']
  add('h.'+r['id'],r['reference']+': '+r['conclusion'],r['source_id'],'historical','source_statement',sl(r['source_id'],r['source_pages']),flags)
  nodes['h.'+r['id']]['accepted_recovery_status']=r['current_status']
 for id,label,src,ps in [
 ('h.L066.diagonal','Printed diagonal fixed-orbit count and reversal averaging','L066',[5,6]),
 ('h.L074.coordinates','Printed finite root/torus matrices and ovoid coordinates','L074',[3,4]),
 ('h.L074.normalization','Step 2: normalize endpoints and classify Frobenius orbits','L074',[5,6]),
 ('h.L074.middle','Step 3: centralizer action on middle involutions','L074',[6,7]),
 ('h.L074.duality','Printed no-self-duality argument','L074',[7]),
 ('h.L074.IP','Printed IP/nondegeneracy argument using coprimality and proper subgroups','L074',[7,11]),
 ('h.L074.subfields','Printed generated Suzuki subfields and subtraction of proper fields','L074',[10,11]),
 ('h.L074.Q','Printed unfiltered first-coordinate/stabilizer-fiber orbit sum','L074',[9,10]),
 ('h.L104.axioms','All six source geometry axioms and equivalence convention','L104',[1,2]),
 ('h.L104.oldsearch','Prior search with nontrivial Borel','L104',[1,2]),
 ('h.L104.extension','New maximal-residue extension for the trivial-Borel case','L104',[2,3]),
 ('h.L104.ranktest','No extension above the computed terminal maximal residues','L104',[3]),
 ('h.L104.supplement','Printed link to complete classification supplement','L104',[4,5])]:add(id,label,src,'historical','documentary_proof_step',sl(src,ps))
 uses('h.L066.3',['ext.WilsonCentralizer'],'retained_input_use');uses('h.L066.4',['h.L066.3']);uses('h.L066.4',['h.L066.16'],why='The printed even/odd-degree observation on physical page 3 supplies the odd-degree part of Lemma 3.2.');uses('h.L066.diagonal',['h.L066.4','h.L066.5']);uses('h.L066.1',['h.L066.4','h.L066.diagonal','h.L066.15']);uses('h.L066.1',['ext.PermutationAut'],'retained_input_use');uses('h.L066.10',['h.L066.3']);uses('h.L066.11',['h.L066.4','h.L066.10']);uses('h.L066.2',['h.L066.11','h.L066.diagonal','h.L066.12']);uses('h.L066.2',['h.L066.16'],why='The printed even/odd-degree reduction on physical page 3 enters the alternating-group principal formula for both degrees.');uses('h.L066.2',['ext.PermutationAut'],'retained_input_use');uses('h.L066.6',['h.L066.5']);uses('h.L066.7',['ext.Polytope'],'definition_use');uses('h.L066.8',['h.L066.15','h.L066.7']);uses('h.L066.12',['h.L066.15']);uses('h.L066.13',['h.L066.12','h.L066.7']);uses('h.L066.14',['h.L066.1','h.L066.2']);uses('h.L066.9',['ext.LeemansVauthier'],'attribution');uses('h.L066.16',['ext.FiniteGroups'],'retained_input_use')
 for row in ['5','6','7']:uses('h.L074.'+row,['ext.LuneburgGeneral'],'retained_input_use')
 uses('h.L074.8',['ext.Leemans1998'],'retained_input_use');uses('h.L074.16',['ext.SuzukiMaximals'],'retained_input_use');uses('h.L074.3',['ext.Leemans2006'],'retained_input_use');uses('h.L074.9',['ext.SuzukiRoots'],'retained_input_use');uses('h.L074.10',['ext.Fermat'],'retained_input_use');uses('h.L074.11',['ext.Mobius'],'retained_input_use');uses('h.L074.coordinates',['h.L074.5','h.L074.17'],'definition_use');uses('h.L074.normalization',['h.L074.coordinates','h.L074.6','h.L074.9']);uses('h.L074.normalization',['ext.SuzukiAut'],'retained_input_use');uses('h.L074.middle',['h.L074.normalization','h.L074.6','h.L074.9']);uses('h.L074.duality',['h.L074.middle']);uses('h.L074.IP',['h.L074.8','h.L074.16','h.L074.9']);uses('h.L074.IP',['ext.Polytope'],'retained_input_use');uses('h.L074.4',['h.L074.normalization','h.L074.middle','h.L074.duality','h.L074.IP','h.L074.3']);uses('h.L074.4',['h.L074.10'],'validation','Fermat is the printed integrality check, not the construction or classification argument.')
 uses('h.L074.12',['h.L074.normalization','h.L074.11']);uses('h.L074.12',['ext.FiniteFields'],'retained_input_use');uses('h.L074.1',['h.L074.12','h.L074.duality']);uses('h.L074.13',['h.L074.middle','h.L074.11']);uses('h.L074.13',['ext.FiniteFields'],'retained_input_use');uses('h.L074.Q',['h.L074.12','h.L074.13','h.L074.duality','h.L074.IP']);uses('h.L074.14',['h.L074.Q']);uses('h.L074.14',['h.L074.subfields'],why='Lemma 10 on physical page 11 asserts generated Suzuki subfield groups, not only the raw Q count; its preceding pages 10–11 supply this documentary identification.');uses('h.L074.subfields',['h.L074.16','h.L074.normalization']);uses('h.L074.2',['h.L074.14','h.L074.subfields','h.L074.11','h.L074.IP','h.L074.3']);uses('h.L074.15',['h.L074.13','h.L074.Q','h.L074.4']);uses('h.L074.17',['ext.LuneburgGeneral'],'attribution')
 uses('h.L104.oldsearch',['ext.MagmaPrior'],'retained_input_use');uses('h.L104.oldsearch',['h.L104.axioms'],'definition_use');uses('h.L104.extension',['h.L104.axioms'],'definition_use');uses('h.L104.extension',['ext.MagmaPrior','ext.J2HistoricalSubgroups'],'retained_input_use');uses('h.L104.ranktest',['h.L104.extension']);uses('h.L104.1',['h.L104.oldsearch','h.L104.extension']);uses('h.L104.2',['h.L104.ranktest']);uses('h.L104.2',['h.L104.oldsearch'],why='The all-Borel higher-rank exclusion combines the earlier nontrivial-Borel search with the B=1 extension test; the latter alone is insufficient.');uses('h.L104.3',['h.L104.1','h.L104.supplement']);uses('h.L104.supplement',['h.L104.1']);uses('h.L104.4',['h.L104.1','h.L104.supplement']);uses('h.L104.4',['ext.J2Secondary'],'retained_input_use')
 # Historical-to-current arrows record attribution or comparison, never premises.
 for h,cur in [('h.L066.3','D1.Centralizers'),('h.L066.5','D1.Reversal'),('h.L074.normalization','D2.Normalization'),('h.L074.13','D2.Fibers'),('h.L074.11','UD.FieldSupport'),('h.L104.extension','UD.MaximalAugmentation')]:edge(h,cur,'attribution','Historical idea/source origin retained. The current complete proof is written; this arrow is not a logical dependency on the old proof.')
 # Formal layers are evidence, not logical antecedents of the written assertions.
 fs=json.loads((a.public_root/base/'formal/scope.json').read_text());bind('public',base+'formal/scope.json')
 for m in fs['modules']:
  id='formal.'+Path(m['file']).stem;add(id,m['file']+': '+str(len(m['declarations']))+' scoped reports','FORMAL','verification','formal_evidence',[loc('public',base+'formal/'+m['file'])],scope_note=fs['formal_scope'][Path(m['file']).stem]);nodes[id]['reports']=m['declarations']
 uses('UD.ExtensionOrbits',['formal.ExtensionOrbits'],'formal_scope','Actual single-base-orbit quotient/fiber equivalence; original disjoint union remains written in this initial layer.')
 uses('UD.OddOrbits',['formal.ExtensionOrbits'],'formal_scope','Odd-period action implication; the finite-odd-order adapter remains written.')
 uses('D2.Rank',['formal.InvolutionCentralizers'],'formal_scope','Generic generated centre-free rank obstruction only; source structural hypotheses not formally instantiated.')
 support=base+'support-formal/'
 for file,label,count,targets in [('SupportCounting.lean','Finite support incidence inversion and orbit count',12,['UD.AdmissibleExtensions','UD.ExactSupport']),('OrbitFiberDecomposition.lean','Actual orbit quotient and global stabilizer-fiber decomposition',16,['UD.ExtensionOrbits','UD.AdmissibleExtensions'])]:
  id='formal.'+Path(file).stem;add(id,label,'FORMAL','verification','formal_evidence',[loc('public',support+file)],scope_note='Later separately reviewed generic support supplement. Source admissibility, generation, least-field/divisor bridge, normalizers and catalogue completeness are not formalized.');nodes[id]['report_count']=count;uses(targets[0],[id],'formal_scope');
  for t in targets[1:]:edge(id,t,'formal_scope')
 # Exact contract routes. Ancillary retained/excluded rows stay visible without invented recovery.
 route={
 'L066.1':['D1.Symmetric','D1.Exceptional','D1.DegreeParity'],'L066.2':['D1.Alternating','D1.Exceptional','D1.DegreeParity'],'L066.3':['D1.Centralizers'],'L066.4':['D1.Ordered'],'L066.5':['D1.Reversal'],'L066.6':['D1.Reversal'],'L066.7':[],'L066.8':['D1.Polyhedra'],'L066.9':[],'L066.10':['D1.Centralizers'],'L066.11':['D1.EvenOrdered'],'L066.12':['D1.Exceptional'],'L066.13':['D1.Polyhedra'],'L066.14':['D1.Table'],'L066.15':['D1.Exceptional'],'L066.16':['D1.DegreeParity'],
 'L074.1':['D2.Pairs'],'L074.2':['D2.Polyhedra','D2.Nested'],'L074.3':['D2.Rank'],'L074.4':['D2.PrimeExamples'],'L074.5':['D2.FrobeniusRoot'],'L074.6':[],'L074.7':[],'L074.8':[],'L074.9':['D2.InvolutionCount'],'L074.10':[],'L074.11':['UD.FieldSupport'],'L074.12':['D2.Pairs'],'L074.13':['D2.Fibers'],'L074.14':['D2.Nested'],'L074.15':['D2.PrimeExamples'],'L074.16':[],'L074.17':[],
 'L104.1':['D3.Fusion','D3.Verified'],'L104.2':['D3.NoHigher'],'L104.3':['D3.Fusion','D3.Verified'],'L104.4':[]}
 retained={'L066.7':['ext.Polytope'],'L066.9':['ext.LeemansVauthier'],'L074.6':['ext.SuzukiRoots'],'L074.7':['ext.SuzukiRoots'],'L074.10':['ext.Fermat'],'L074.16':['ext.SuzukiMaximals'],'L074.17':['ext.SuzukiRoots']}
 rows=[]
 for r in scope['contracts']:
  id=r['id'];context=['D1.Qualifications'] if id in ['L066.6','L066.9','L066.13'] else ['UD.Conventions'] if id=='L066.7' else ['D2.RetainedBoundary'] if id in ['L074.3','L074.5','L074.6','L074.7','L074.8','L074.9','L074.10','L074.11','L074.16','L074.17'] else ['D3.Exclusions'] if id=='L104.4' else []
  rows.append(dict(id=id,source=r['source_id'],accepted_record=r,historical_outputs=['h.'+id],new_outputs=route[id],retained_input_nodes=retained.get(id,[]),qualification_context_nodes=context,coverage_kind='proved_or_qualified_output' if route[id] else 'excluded' if id=='L104.4' else 'unused_background' if id=='L074.8' else 'attribution' if id=='L066.9' else 'definition' if id in ['L066.7','L074.17'] else 'retained_not_reproved',cost=None))
  for t in route[id]:edge('h.'+id,t,'comparison','Same declared result or explicitly corrected/qualified replacement; not a proof dependency.')
 pred={n:[] for n in nodes}
 for e in edges:
  if e['kind'] in LOGICAL:pred[e['target']].append(e['source'])
 def closure(outs):
  seen=set(outs);todo=list(outs)
  for x in todo:
   for y in pred[x]:
    if y not in seen:seen.add(y);todo.append(y)
  return sorted(seen)
 for r in rows:r['historical_closure']=closure(r['historical_outputs']);r['new_closure']=closure(r['new_outputs']);r['retained_context_closure']=closure(r['retained_input_nodes'])
 appout={s:sorted({n for r in rows if r['source']==s for n in r['new_outputs']}) for s in scope['source_ids']}
 bind('research','topic_D_logical_dag/manifest.json');bind('research','topic_D_logical_dag_v2/manifest.json')
 # Bind scientific/public admissions and original/follow-up formal review without source redistribution.
 for ns,p in [('research','topic_D_volume/manifest.json'),('research','topic_D_volume_independent_review/manifest.json'),('research','topic_D_root_adoption/manifest.json'),('public','audit/topic-d/v2/admission.json'),('public',base+'scope.json'),('public',base+'manifest.json'),('public','audit/topic-d/v2/support-formal/admission.json')]:bind(ns,p)
 for doc in ['umbrella','commuting-involutions','suzuki-polyhedra','hall-janko-geometries','program-appendix']:
  for suffix in ['.tex','.pdf']:bind('public',base+doc+suffix)
 bind('public',base+'preamble.tex')
 counts=dict(nodes=len(nodes),edges=len(edges),nodes_by_side=dict(Counter(n['side'] for n in nodes.values())),nodes_by_category=dict(Counter(n['category'] for n in nodes.values())),edges_by_kind=dict(Counter(e['kind'] for e in edges)),source_clauses=37)
 g=dict(schema='human-compression.logical-dag.v1',status='AUTHOR_PROPOSED_LOGICAL_DAG_AWAITING_INDEPENDENT_SEMANTIC_REVIEW',scope='Exact existing Topic D principal contracts plus explicitly scoped ancillary rows; no new result or intake.',public_proof_edition_commit='2d631760842796450899761f8763b0e9a9ff4b77',source_order=['L066','L074','L104'],applications={'L066':'D1','L074':'D2','L104':'D3'},document_titles={'U_D':'Marked actions, support and geometry enumeration','D1':'Commuting involutions','D2':'Suzuki polyhedra','D3':'Hall–Janko geometries'},edge_orientation='prerequisite -> use',logical_edge_kinds=LOGICAL,nonlogical_edge_kinds=OTHER,source_bindings=sourcebindings,immutable_inputs=list(inputs.values()),accepted_scope_spans=span,nodes=list(nodes.values()),edges=edges,checks=counts,new_application_outputs=appout,new_output_closures={s:closure(o) for s,o in appout.items()},additional_current_outputs={'D1.Series':closure(['D1.Series']),'D3.Faithfulness':closure(['D3.Faithfulness'])},unused_common_statement_nodes=['UD.Normalizer'],required_mathematical_programs=['program.exceptional','program.search','program.fusion','program.verify','program.predicates'],diagnostic_programs=['diagnostic.pairs','diagnostic.fields','diagnostic.q8'],operational_drivers=['driver.pairs','driver.enumeration'],formal_evidence={'initial_report_count':10,'later_support_report_count':28,'later_components':[12,16],'first_support_12_counted_again':False,'source_specific_instantiations_claimed':False,'divisor_number_theoretic_bridge_verified':False},graph_granularity='Named statements and substantive argument blocks; context locators may overlap. Historical routes document claims used in the source, including flagged qualifications, and are not retrospective validity endorsements.',node_count_policy='Inventory only, never mathematical complexity or a compression factor.',measurement={'weights_assigned':False,'exclusive_partition_assigned':False,'all_costs_unknown_here':True,'formal_validation_separate':True},new_source_credit=0,new_question_credit=0,compression_ratio=None,limits=['Historical full source software/algorithm bodies and external classifications have unknown proof cost.','All five current required programs have logical routes; all three complete diagnostics and both full drivers remain visible with nonlogical roles.','Historical-to-current arrows are comparison or attribution only; no unpriced private proof-bank premise.','L104 diagrams/full Aut/Cor/doubling/supplement recovery is not asserted.','Full general-field Suzuki/Lüneburg statements and unused coprimality/Fermat background are distinguished from the finite inputs actually retained.','The full normalizer exact sequence is present and proved in the common paper but is not needed by the selected application routes; it is not silently removed from the complete paper.','No exclusive costs, ratios, measurement adoption or formal end-to-end source recovery is inferred.'])
 coverage=dict(schema='topic_d_logical_coverage_v1',rows=rows,source_clause_count=37,accepted_scope_binding=bind('public',base+'scope.json'),principal_contracts_unchanged=True,excluded_assertion_ids=['L104.4'],unused_background_ids=['L074.8'],historical_graph_semantics='dependencies asserted/used in the original source; corrections remain flags',comparison_arrows_not_logical=True,weights_assigned=False,new_source_credit=0,new_question_credit=0)
 protocol=dict(schema='topic_d_logical_protocol_v1',status='FIXED_LOGICAL_BOUNDARY_NO_MEASUREMENT',authoritative_scope=base+'scope.json',accepted_contract_rows=37,accepted_proof_context_spans=19,source_order=['L066','L074','L104'],edge_orientation='prerequisite -> use',logical_edge_kinds=LOGICAL,nonlogical_edge_kinds=OTHER,whole_program_boundary=dict(required=5,diagnostic=3,operational_drivers=2),formal_evidence_only=dict(original_reports=10,later_support_reports=28,components=[12,16],no_double_count=True),measurement_dependency='None: logical routes do not use the pending measurement calibration or counts.',source_locator_policy='Locally supplied exact primary PDF and cached page-text hashes; no primary files or source text in exports.',cost_policy='No weights or exclusive partitions. External proof/catalogue/graphic costs stay null. No ratio from node counts.',review_boundary='Semantic edge selection requires independent reading; the portable checker verifies exact bytes, source scope, types, acyclicity, closures and required routes, not mathematical truth.',primary_redistribution=False)
 for name,obj in [('logical_graph.json',g),('coverage.json',coverage),('protocol.json',protocol)]: (a.out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(counts))
if __name__=='__main__':main()
