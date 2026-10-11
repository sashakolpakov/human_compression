#!/usr/bin/env python3
"""Author the closed affine topic's documentary and current logical graphs.

No primary text is exported. Locators bind existing texts and may overlap;
they are proof contexts, never exclusive measurement owners.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, re

SHA = lambda b: hashlib.sha256(b).hexdigest()
LOGICAL = ['proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use']
OTHER = ['attribution','comparison','validation','formal_scope','operational']
BASE = 'papers/topic-affine/v2/'

def build(study, public, out):
    roots={'research':study,'public':public}; inputs={}; nodes=[]; edges=[]
    def bind(ns,path):
        if (ns,path) not in inputs:
            b=(roots[ns]/path).read_bytes()
            inputs[ns,path]=dict(namespace=ns,path=path,bytes=len(b),sha256=SHA(b))
        return inputs[ns,path]
    def loc(ns,path,start=0,end=None,pages=None):
        bind(ns,path);t=(roots[ns]/path).read_text()
        if end is None:end=len(t)
        s=dict(namespace=ns,path=path,start_codepoint=start,end_codepoint_exclusive=end,
          first_line=t.count('\n',0,start)+1,last_line=t.count('\n',0,end-1)+1,
          sha256_utf8=SHA(t[start:end].encode()),
          scope='Exact statement/proof context; may overlap; no exclusive cost ownership')
        if pages:s['physical_pdf_pages']=pages
        return s
    def sec(key,anchor=None,end=None):
        path=BASE+'sections/'+key+'.tex';t=(public/path).read_text()
        a=0 if anchor is None else t.index(anchor)
        b=len(t) if end is None else t.index(end,a+len(anchor or ''))
        z=loc('public',path,a,b);z['accepted_region']=key;return z
    primary='sources/regular_2np2025.txt';text=(study/primary).read_text()
    page_starts={int(m.group(1)):m.start() for m in re.finditer(r'--- PDF PAGE (\d+) ---',text)}
    def page(a,b=None):
        b=a if b is None else b
        return loc('research',primary,page_starts[a],page_starts.get(b+1,len(text)),list(range(a,b+1)))
    def node(id,label,side,category,document,locations,flags=None,note=None):
        nodes.append(dict(id=id,label=label,side=side,category=category,document=document,
          locators=locations if isinstance(locations,list) else [locations],documentary_flags=flags or [],
          scope_note=note,cost=None,cost_status='Unmeasured; external and graphic costs unknown'))
    def new(id,label,key,anchor=None,end=None,note=None,category='proved_statement'):
        node(id,label,'new',category,'U_Affine' if not key.startswith('application') else 'A_Affine',sec(key,anchor,end),note=note)
    def hist(id,label,a,b=None,flags=None,category='source_statement_and_proof'):
        node('h.'+id,label,'historical',category,'L012',page(a,b),flags)
    def ext(id,label,locations,note):
        node('ext.'+id,label,'external','retained_external_input','retained',locations,note=note)
    def edge(s,t,kind='proof_use',why=None):
        if any((e['source'],e['target'],e['kind'])==(s,t,kind) for e in edges):
            return
        target=next(n for n in nodes if n['id']==t)
        edges.append(dict(source=s,target=t,kind=kind,
          evidence=why or 'Direct use in the bound target statement/proof context; not a minimal-axiom claim.',
          target_evidence=target['locators'],necessity_claim=False))
    def uses(target,*sources,kind='proof_use',why=None):
        for source in sources:edge(source,target,kind,why)

    scope=json.loads((public/(BASE+'scope.json')).read_text());bind('public',BASE+'scope.json')
    for p in ['audit/topic-affine/v2/admission.json','audit/topic-affine/v2/independent_review/review.json',
              BASE+'umbrella.tex',BASE+'umbrella.pdf',BASE+'mixed-prime-polyhedra.tex',
              BASE+'mixed-prime-polyhedra.pdf',BASE+'required-programs.tex',BASE+'required-programs.pdf',
              'audit/topic-affine/v2/measurement/admission.json']:
        bind('public',p)
    for p in ['topic_Affine_logical_dag/manifest.json','topic_Affine_volume/manifest.json','topic_Affine_volume_independent_review/manifest.json',
              'topic_Affine_measurement_results/manifest.json','topic_Affine_measurement_results_independent_review/manifest.json']:
        bind('research',p)
    for r in scope['source_bindings']:bind('research',r['path'])
    # Retained theorem/algorithm interfaces. A source citation is not a reproof.
    ext('FiniteGroups','Elementary group structure, solvable extensions and cyclic/dihedral groups',
        [page(4,7),sec('application-02'),sec('application-references')],
        'Includes Sylow, elementary abelian minimal normal subgroups, centralizer action and elementary solvability facts. No new classical theorem claim.')
    ext('IntegerLattices','Free abelian groups, determinant/minor index and lattice arithmetic',
        [sec('03-affine'),sec('04-periods')],
        'Elementary algebra used in the written proofs and exact integer algorithms; no floating point.')
    ext('Burnside','Burnside solvability theorem for groups of order p^a q^b',
        [page(7),sec('application-02')],'Classical theorem retained; historical primary proof not newly acquired or formalized.')
    ext('Lucchini','Lucchini 1998 cyclic-core inequality',
        [loc('research','sources/phase254_Lucchini1998.txt'),page(4),sec('application-07')],
        'Original Proposition, printed p.241/physical p.3; complete primary paper previously reviewed. HFL attributes this to a Suzuki locator; current source is Lucchini.')
    ext('Polytope','Regular-polytope/string-C-group correspondence and duality',
        [page(4,5),sec('00-markings'),sec('application-references')],
        'McMullen–Schulte correspondence retained. Rank-three IP test itself is proved locally.')
    ext('ConderBound','Conder order lower bound',page(5),'Source Proposition 2.6; current rank-three bound is proved by a subgroup-product count.')
    ext('ConderTight','Conder even-parameter tight construction',page(6),'Source Proposition 2.7; current tight case has a local supported-kernel proof.')
    ext('CoxeterMoser','Classical square-map presentations',page(6),'Source Proposition 2.10 cites Coxeter–Moser §8.3; current complete square presentation is proved locally.')
    ext('QuotientCriteria','Classical string-C-group quotient criteria',page(6),'Source Propositions 2.8–2.9, citing McMullen–Schulte and Cunningham–Pellicer. Current required rank-three lifting arguments are written locally.')
    ext('Atlas','Conder small regular-polytope atlas', [page(3),page(10),page(13,16)],
        'Historical base geometry, order-96 case, table and two-seed uniqueness. Not a required catalogue for the current explicit constructions.')
    ext('RS','Exact Reidemeister–Schreier and Tietze presentation algorithms',
        [page(4),sec('03-affine')],'An actual subgroup presentation is required, not its abelianization alone. Algorithm correctness is retained.')
    ext('Magma','Historical Magma computations', [page(4),page(10),page(13,14)],
        'Source-reported computations; original runnable scripts/results are not reconstructed by this documentary graph.')
    ext('GAP','Exact GAP group/presentation algorithms',sec('application-references'),
        'Computational trust interface for the four complete GAP programs. No Lean replacement of the algorithms is claimed.')
    ext('SmallGroups','Complete order-384 SmallGroups catalogue',sec('application-07'),
        'Version 1.5.4, all 20,169 entries; construction/completeness proof remains retained, not zero-cost.')
    ext('MW20','Montero–Ivić Weiss polygon construction, earlier equal-label existence',sec('application-equal'),
        'Historical attribution only in the current locally complete existence proof; no imported universal-presentation or halving theorem.')
    ext('LZ25','Li–Zhang equal-parameter construction, existing answer',sec('application-equal'),
        'Historical attribution only; no new question or priority claim.')

    # Common theory: actual proof interfaces, including unused but fully charged statements.
    new('U.Marking','Marked subgroups, string convention and IP','00-markings',category='definition')
    new('U.RankThree','Rank-three intersection test','00-markings','It is enough to test' if 'It is enough to test' in (public/(BASE+'sections/00-markings.tex')).read_text() else None)
    new('UA.K0','Lift one intersection from a quotient','01-kernels','\\textbf{Lemma UA.K0','\\textbf{Theorem UA.K')
    new('UA.K','Intersection property is exactly the kernel-profile condition','01-kernels','\\textbf{Theorem UA.K','\\textbf{Proposition UA.D')
    new('UA.D','Boolean deletion maps: IP, normal kernels and semidirect factors','01-kernels','\\textbf{Proposition UA.D','\\textbf{Theorem UA.SK')
    new('UA.SK','Compatible supported kernels: generation, kernel profiles, IP and order','01-kernels','\\textbf{Theorem UA.SK', '\\textbf{Corollary UA.SK.Local')
    new('UA.SK.Local','Antichain supports preserve the prescribed local groups','01-kernels','\\textbf{Corollary UA.SK.Local','\\textbf{Corollary UA.SK.Delete')
    new('UA.SK.Delete','Supported products inherit all compatible deletions','01-kernels','\\textbf{Corollary UA.SK.Delete')
    new('UA.Affine','The complete square Coxeter presentation as an affine group','02-squares')
    new('UA.Square','Square period quotients: order, IP, deletions and lower central term','02-squares')
    new('AL.AffineSetup','Integral affine multiplication and the translation kernel','03-affine',end='\\textbf{Lemma AL.1',category='definition')
    new('AL.1','Normalized Schreier transitions generate the exact translation lattice','03-affine','\\textbf{Lemma AL.1','The normalization in (2) matters.')
    new('AL.RawInvariant','Raw differences suffice only with invariant-lattice closure','03-affine','The normalization in (2) matters.','\\textbf{Lemma AL.2')
    new('AL.2','An exact abstract kernel presentation identifies the affine group','03-affine','\\textbf{Lemma AL.2')
    new('AL.Period','Exact period presentations, order and solvability for every positive multiplier','04-periods',end='Suppose now that the marking')
    new('AL.3','All parabolic intersections from finite affine overlap differences','04-periods','Suppose now that the marking','\\subsection*{One coarse quotient')
    new('AL.SmallerPeriods','A coarse quotient controls every smaller normal period','04-periods','\\subsection*{One coarse quotient')
    new('AL.4','A compatible dihedral extension changes one adjacent order','05-extensions',end='There is a useful exact presentation variant.')
    new('AL.PresentationExtension','A normal cyclic kernel identifies the complete extended presentation','05-extensions','There is a useful exact presentation variant.')
    uses('U.RankThree','U.Marking',kind='definition_use')
    uses('UA.K','UA.K0');uses('UA.SK','UA.K');uses('UA.SK.Local','UA.SK');uses('UA.SK.Delete','UA.SK','UA.D')
    uses('UA.Square','UA.Affine','UA.D');uses('AL.1','AL.AffineSetup',kind='definition_use')
    uses('AL.RawInvariant','AL.1');uses('AL.2','ext.IntegerLattices',kind='retained_input_use')
    uses('AL.2','AL.AffineSetup',kind='definition_use');uses('AL.Period','AL.AffineSetup',kind='definition_use')
    uses('AL.Period','ext.IntegerLattices','ext.FiniteGroups',kind='retained_input_use')
    uses('AL.3','AL.Period','U.RankThree');uses('AL.4','U.RankThree')
    uses('AL.4','ext.FiniteGroups',kind='retained_input_use');uses('AL.PresentationExtension','AL.4')
    edge('UA.SK','AL.4','comparison','The text calls AL.4 a specialization, but supplies an independent proof requiring only one deletion. It is not an imported proof premise.')
    edge('AL.3','AL.SmallerPeriods','comparison','Coordinate-free companion proved independently; application proofs invoke AL.3, not this alternative lemma.')

    # Required complete code. Embedded controls remain in each full file.
    pmap=[('kernel64','phase250_affine64_kernel.g'),('affine64','phase250_affine_check.py'),
          ('census384','phase250_base384_census.g'),('fixed','phase250_fixed_groups.g'),
          ('kernel66','phase2_cubic_kernel_check.g'),('affine66','phase2_cubic_lattice_check.py')]
    for id,name in pmap:
        node('program.'+id,name,'new','required_program','CODE',loc('public',BASE+'programs/'+name),
             note='Complete unchanged program, including its embedded diagnostics; no pruning and no separate double charge.')
    for id in ['kernel64','kernel66']:uses('program.'+id,'ext.GAP','ext.RS',kind='retained_input_use')
    for id in ['fixed','census384']:uses('program.'+id,'ext.GAP',kind='retained_input_use')
    uses('program.census384','ext.SmallGroups',kind='retained_input_use')
    for id in ['affine64','affine66']:uses('program.'+id,'ext.IntegerLattices',kind='retained_input_use')
    uses('program.affine64','AL.1');uses('program.affine66','AL.RawInvariant')
    # The second Python file records the kernel script's bytes but does not run it.
    edge('program.kernel66','program.affine66','operational','The affine checker hashes the separate kernel script as provenance; it does not read a mathematical result from it or execute it.')

    # Application proof steps; the fine interface may share one accepted TeX context.
    appnodes=[
      ('AF.Statements','Principal theorem statements and precise ranges','01'),
      ('AF.DihedralQuotient','The quotient by O_2 is dihedral of order 2p','02'),
      ('AF.TypeRestriction','An odd prime divides an adjacent label; complete type dichotomy','02'),
      ('AF.OddSquareBase','The final commutator period gives the exact square quotient','03'),
      ('AF.OddExtension','Two edge periods give the literal order, type, IP and solvability','03'),
      ('AF.OddCorollary','The prime odd-factor specialization','03'),
      ('AF.Affine64','The exact universal affine group of type {6,4}','04'),
      ('AF.Words64','All nine source words, invariant lattices and determinants for {6,4}','04'),
      ('AF.Period64','All three full {6,4} presentations for every positive m','04'),
      ('AF.Cor64','The three residue classes give every n at least five','04'),
      ('AF.Delete64','Exact deletion criterion for each {6,4} period lattice','05'),
      ('AF.Extensions64','One-edge extensions give every nonexceptional excess','05'),
      ('AF.Seed384','The literal exceptional 384 seed, retraction and all intersections','05'),
      ('AF.ExceptionalExtensions','The exceptional seed extends uniformly at excess five','05'),
      ('AF.SourcePeriods','Exact three-branch presentation bridge, with the corrected first sign','06'),
      ('AF.SignIdentity','The literal first-sign relation forces a shorter rotation','06'),
      ('AF.SignExample','The concrete n=10,s=4 literal and corrected presentations','06'),
      ('AF.Bounds','Rank-three product counting gives the parameter bounds','07'),
      ('AF.TightEven','The endpoint tight case follows from a Boolean supported base','07'),
      ('AF.CyclicDescent','A cyclic-core involution descends every hypothetical excluded case','07'),
      ('AF.Census384','Complete order-384 catalogue search excludes the descent base','07'),
      ('AF.ExistenceRange','The complete if-and-only-if range for type {6,2^s}','07'),
      ('AF.Affine66','The exact universal affine group of type {6,6}','08'),
      ('AF.Words66','All nine source words, invariant lattices and determinants for {6,6}','08'),
      ('AF.Period66','All three full {6,6} presentations for every positive m','08'),
      ('AF.Tetra96','An explicit tetrahedral central cover supplies the order-96 case','08'),
      ('AF.Cor66','All powers-of-two orders in the {6,6} corollary','08'),
    ]
    for id,label,key in appnodes:new(id,label,'application-'+key,category='statement_context' if id=='AF.Statements' else 'proved_statement')
    new('AF.EqualModel','The augmentation-module model and the duality cocycle','application-equal')
    new('AF.EqualIP','The two dihedral graph subgroups have the required intersection','application-equal')
    new('AF.EqualGeneration','Adjacent binary differences generate the entire module','application-equal')
    new('AF.KnownAnswer','The already answered prime-label existence question','application-equal')
    new('AF.Exclusions','Problem 1.1, the separate table and two-seed uniqueness are excluded','application-09',category='scope_context')
    new('AF.FormalScope','Nine scoped declarations, retained algorithms and written obligations','application-09',category='scope_context')
    uses('AF.DihedralQuotient','ext.Burnside','ext.FiniteGroups',kind='retained_input_use')
    uses('AF.TypeRestriction','AF.DihedralQuotient')
    uses('AF.TypeRestriction','ext.Polytope',kind='retained_input_use')
    uses('AF.OddSquareBase','UA.Affine','UA.Square');uses('AF.OddExtension','AF.OddSquareBase','UA.SK','UA.SK.Local')
    uses('AF.OddExtension','ext.FiniteGroups',kind='retained_input_use');uses('AF.OddCorollary','AF.OddExtension')
    uses('AF.Affine64','AL.2','program.kernel64','program.affine64')
    uses('AF.Words64','AF.Affine64','program.affine64')
    uses('AF.Period64','AF.Words64','AL.Period','AL.3','program.affine64')
    uses('AF.Cor64','AF.Period64');uses('AF.Delete64','AF.Words64')
    uses('AF.Extensions64','AF.Period64','AF.Delete64','AL.4')
    uses('AF.Seed384','program.fixed');uses('AF.ExceptionalExtensions','AF.Seed384','AL.PresentationExtension')
    uses('AF.SourcePeriods','AF.Words64','AF.Delete64','AL.PresentationExtension','AF.Period64')
    uses('AF.SignExample','AF.SignIdentity','program.fixed')
    uses('AF.Bounds','U.Marking',kind='definition_use');uses('AF.TightEven','UA.SK','UA.SK.Local','UA.D')
    uses('AF.CyclicDescent','ext.Lucchini',kind='retained_input_use');uses('AF.CyclicDescent','U.RankThree')
    uses('AF.Census384','program.census384')
    uses('AF.ExistenceRange','AF.Bounds','AF.TightEven','AF.Extensions64','AF.ExceptionalExtensions','AF.CyclicDescent','AF.Census384')
    uses('AF.Affine66','AL.2','program.kernel66','program.affine66')
    uses('AF.Words66','AF.Affine66','program.affine66')
    uses('AF.Period66','AF.Words66','AL.Period','AL.3','program.affine66')
    uses('AF.Tetra96','U.RankThree','UA.K');uses('AF.Cor66','AF.Period66','AF.Tetra96')
    uses('AF.EqualIP','AF.EqualModel','U.RankThree');uses('AF.EqualGeneration','AF.EqualModel')
    uses('AF.KnownAnswer','AF.EqualIP','AF.EqualGeneration')
    uses('AF.KnownAnswer','ext.Polytope',kind='retained_input_use')
    uses('AF.Statements','AF.TypeRestriction','AF.OddExtension','AF.ExistenceRange','AF.Cor66',kind='proof_assembly',why='The initial theorem statements are proved by these later complete derivations; this arrow adds no repeated proof or cost.')
    uses('AF.KnownAnswer','ext.MW20','ext.LZ25',kind='attribution',why='The complete local proof is written here; these earlier results are credited without importing unpaid proof premises.')
    for id in ['AF.OddCorollary','AF.Period64','AF.ExceptionalExtensions','AF.ExistenceRange','AF.Cor66']:
        uses(id,'ext.Polytope',kind='retained_input_use')

    # Historical graph: what the source asserts/uses, not retroactive certification.
    hist('Definitions','Definitions of string C-groups, types and regular polytopes',4,6,category='source_definition')
    for i,title,pg in [
        (1,'Commutator identities',4),(2,'Solvable extensions',4),(3,'Characteristic m-power sublattices of Z^3',4),
        (4,'Cyclic-core inequality called Lucchini’s theorem',4),(5,'Degenerate rank-three dihedral products',5),
        (6,'Order lower bound',5),(7,'Tight construction for all even parameters',6),
        (8,'Quotient criterion for an injective adjacent parabolic',6),(9,'Normal rotation-power quotients preserve IP',6),
        (10,'Classical square-map presentations and orders',6)]:
        hist('P2.'+str(i),'Proposition 2.'+str(i)+': '+title,pg,
             flags=['The literal reference [31, Theorem 2.20] is not the current Lucchini primary binding.'] if i==4 else None,
             category='retained_source_statement' if i in [4,6,7,8,9,10] else ('source_statement_without_proof' if i in [2,3] else 'source_statement_and_proof'))
    hist('T3.1','The induction proving the odd-prime adjacent-label restriction',6,7)
    hist('T1.2','Theorem 1.2: geometric type dichotomy',3,7)
    hist('T4.1','Theorem 4.1: two cyclic layers over a square-map quotient',8,9)
    hist('C4.2','Corollary 4.2: prime odd-factor specialization',9)
    hist('64.Kernels','Three exact free-abelian kernel presentations of indices 96,192,384',10)
    hist('64.Bases','The three finite base quotients and their marked IP',10)
    hist('64.Scale','Characteristic m-power subgroups and exact cubic indices',10,11)
    hist('T4.3','Theorem 4.3: three {6,4} families, IP and solvability',10,11)
    hist('C4.4','Corollary 4.4: all three powers-of-two parameter branches',11)
    hist('L4.5.0','Lemma 4.5: literal R0 branch with the first positive exponent',11,12,
         flags=['The bound preprint has a false first sign. The replacement uses a negative first exponent; this historical route is not certified as written.'])
    hist('L4.5.1','Lemma 4.5: R1 period branch',11,12)
    hist('L4.5.2','Lemma 4.5: R2 period branch with excess five excluded',11,12)
    hist('L4.6.seed','Magma identification of the exceptional 384 quotient',12,13)
    hist('L4.6','Lemma 4.6: the cyclic exceptional extensions',12,13)
    hist('L4.7.base','Magma exclusion of the order-384 base',13)
    hist('L4.7.descent','The cyclic-core/rotation-quotient descent',13)
    hist('T1.3','Theorem 1.3: the complete {6,2^s} existence range',3,13,
         flags=['The source proof invokes the literal Lemma 4.5 R0 branch. Corrected current coverage is recorded separately; historical use is documentary.'])
    hist('66.Kernels','Three exact free-abelian kernel presentations of indices 192,384,768',14)
    hist('66.Bases','The three finite {6,6} base quotients and their marked IP',14)
    hist('66.Scale','Characteristic m-power subgroups and exact cubic indices',14)
    hist('T5.1','Theorem 5.1: three {6,6} families, IP and solvability',14,15)
    hist('C5.2.base','The atlas order-96 {6,6} example',15)
    hist('C5.2','Corollary 5.2: every n at least five',15,
         flags=['The preceding sentence says Theorem 1.2; its power-of-two family argument is Theorem 5.1. Documentary edge follows the displayed mathematics and records the cross-reference.'])
    hist('Question','The final prime-at-least-five Type (2) question',15,category='source_question')
    hist('Problem1.1','Broad regular/chiral group characterization problem',2,category='excluded_question')
    hist('Table1','Separate small-order yes/no table',3,category='excluded_assertion')
    hist('SeedUniqueness','Exactly two order-384 regular polyhedra of type {6,4}',13,category='excluded_assertion')
    hist('NormalSubgroups64','The auxiliary four-normal-subgroup observation',10,category='ancillary_not_recovered')
    for t in ['h.P2.1','h.P2.2','h.P2.3','h.P2.5']:uses(t,'ext.FiniteGroups',kind='retained_input_use')
    uses('h.P2.3','ext.IntegerLattices',kind='retained_input_use')
    for t,e in [('Definitions','Polytope'),('P2.4','Lucchini'),('P2.6','ConderBound'),('P2.7','ConderTight'),
                ('P2.8','QuotientCriteria'),('P2.9','QuotientCriteria'),('P2.10','CoxeterMoser')]:
        uses('h.'+t,'ext.'+e,kind='retained_input_use')
    uses('h.T3.1','ext.Burnside','ext.FiniteGroups',kind='retained_input_use')
    uses('h.T1.2','h.T3.1','h.Definitions')
    uses('h.T4.1','h.P2.1','h.P2.2','h.P2.5','h.P2.8','h.P2.10')
    uses('h.C4.2','h.T4.1','h.P2.6')
    for prefix,theorem in [('64','h.T4.3'),('66','h.T5.1')]:
        uses('h.'+prefix+'.Kernels','ext.Magma','ext.RS',kind='retained_input_use')
        uses('h.'+prefix+'.Bases','h.'+prefix+'.Kernels')
        uses('h.'+prefix+'.Bases','ext.Magma','ext.Atlas',kind='retained_input_use')
        uses('h.'+prefix+'.Scale','h.'+prefix+'.Kernels','h.P2.3')
        uses(theorem,'h.'+prefix+'.Bases','h.'+prefix+'.Scale','h.P2.2','h.P2.8')
        uses(theorem,'ext.Burnside',kind='retained_input_use',why='The base quotient has order involving only 2 and 3 and is therefore solvable; the source then invokes Proposition 2.2.')
    uses('h.C4.4','h.T4.3')
    for branch in ['0','1','2']:uses('h.L4.5.'+branch,'h.C4.4','h.P2.5','h.P2.8')
    uses('h.L4.6.seed','ext.Magma',kind='retained_input_use');uses('h.L4.6','h.L4.6.seed','h.P2.5','h.P2.8')
    uses('h.L4.7.base','ext.Magma',kind='retained_input_use');uses('h.L4.7.descent','h.P2.4','h.P2.9','h.L4.7.base')
    uses('h.T1.3','h.P2.7','h.C4.4','h.L4.5.0','h.L4.5.1','h.L4.5.2','h.L4.6','h.L4.7.descent')
    uses('h.T1.3','ext.Magma',kind='retained_input_use',why='The final source paragraph says remaining small cases are handled with Magma; no original script is retained.')
    uses('h.C5.2.base','ext.Atlas',kind='retained_input_use');uses('h.C5.2','h.T5.1','h.C5.2.base')
    for t in ['h.Table1','h.SeedUniqueness']:uses(t,'ext.Atlas',kind='retained_input_use')
    uses('h.NormalSubgroups64','ext.Magma',kind='retained_input_use')

    # The nine reports are evidence of precisely scoped generic statements.
    for name,count,target in [('AffinePeriodIntersections',2,'AL.SmallerPeriods'),
                              ('PeriodSignObstruction',3,'AF.SignIdentity'),
                              ('QuotientIntersectionCriterion',4,'AL.SmallerPeriods')]:
        found=list((public/(BASE+'formal')).glob(name+'.lean'))
        if not found:found=list((public/BASE).glob(name+'.lean'))
        if len(found)!=1:raise ValueError('formal path '+name)
        node('lean.'+name,name+': '+str(count)+' scoped declarations','verification','formal_evidence','FORMAL',
             loc('public',str(found[0].relative_to(public))),note='Evidence only; not a written-proof premise or end-to-end application formalization.')
        edge('lean.'+name,target,'formal_scope',
             'The four exact image-intersection/kernel-product and defect criteria are the actual formal dependencies of AffinePeriodIntersections; they are not a literal formalization of UA.K0 or of affine coordinates.' if name=='QuotientIntersectionCriterion' else
             'The actual statement interface supports the indicated generic written assertion; source-specific hypotheses remain written/computational.')
    edge('lean.QuotientIntersectionCriterion','lean.AffinePeriodIntersections','operational','Actual Lean import dependency; not an additional mathematical source or a second count of four declarations.')
    for name,id,category in [('check.py','driver.check','operational_driver'),('integrity_controls.py','driver.integrity','operational_driver'),('controls.py','diagnostic.controls','finite_diagnostic')]:
        node(id,name,'verification',category,'AUX',loc('public',BASE+name),note='Auxiliary file outside the six-program mathematical boundary; not a logical premise.')
    for id,_ in pmap:edge('program.'+id,'driver.check','operational','The portable runner executes and binds the complete program in fresh output.')
    edge('driver.check','driver.integrity','operational','Integrity controls exercise the portable binding interface.')
    edge('AL.SmallerPeriods','diagnostic.controls','validation','The complete controls.py enumerates the C2^3 smaller-period interfaces and rejects omitted faithfulness or M <= N; it does not prove the general lemma.')

    # Every accepted scope record is retained byte-for-byte in JSON content.
    mapping={
      'L012.T1.2':(['h.T1.2','h.T3.1'],['AF.TypeRestriction']),
      'L012.T4.1.presentation':(['h.T4.1'],['AF.OddExtension']),
      'L012.T4.1.IP':(['h.T4.1'],['AF.OddExtension']),
      'L012.T4.1.solvable':(['h.T4.1'],['AF.OddExtension']),
      'L012.C4.2':(['h.C4.2'],['AF.OddCorollary']),
      'L012.C4.4':(['h.C4.4'],['AF.Cor64']),
      'L012.L4.5.branch0':(['h.L4.5.0'],['AF.SourcePeriods','AF.SignIdentity','AF.SignExample']),
      'L012.L4.5.branch1':(['h.L4.5.1'],['AF.SourcePeriods']),
      'L012.L4.5.branch2':(['h.L4.5.2'],['AF.SourcePeriods']),
      'L012.L4.6':(['h.L4.6'],['AF.ExceptionalExtensions']),
      'L012.L4.7.base':(['h.L4.7.base'],['AF.Census384']),
      'L012.L4.7.descent':(['h.L4.7.descent'],['AF.CyclicDescent','AF.Census384']),
      'L012.T1.3':(['h.T1.3'],['AF.ExistenceRange']),
      'L012.C5.2.base':(['h.C5.2.base'],['AF.Tetra96']),
      'L012.C5.2.all':(['h.C5.2'],['AF.Cor66']),
      'L012.question.type2':(['h.Question'],['AF.KnownAnswer']),
      'L012.problem1.1':(['h.Problem1.1'],[]),'L012.table1':(['h.Table1'],[]),
      'L012.seed_uniqueness':(['h.SeedUniqueness'],[]),
      'retained.Burnside':([],[]),'retained.Lucchini':(['h.P2.4'],[]),
      'retained.SmallGroups':([],[]),'retained.RS':([],[]),
      'reused.UA':([],['UA.K','UA.D','UA.SK','UA.Affine','UA.Square']),
      'reused.rank3':(['h.P2.8'],['U.RankThree']),
      'new.affine_organization':(['h.T4.3'],['AL.1','AL.2','AL.3','AL.Period','AF.Affine64','AF.Period64']),
      'new.sign_obstruction':(['h.L4.5.0'],['AF.SignIdentity','AF.SignExample','AF.SourcePeriods'])}
    for i in range(1,4):
        mapping['L012.T4.3.family'+str(i)]=(['h.T4.3'],['AF.Period64'])
        mapping['L012.T5.1.family'+str(i)]=(['h.T5.1'],['AF.Period66'])
    retained={'retained.Burnside':['ext.Burnside'],'retained.Lucchini':['ext.Lucchini'],
      'retained.SmallGroups':['ext.SmallGroups'],'retained.RS':['ext.RS'],'reused.rank3':['ext.Polytope']}
    excluded={'L012.problem1.1','L012.table1','L012.seed_uniqueness'}
    pred={n['id']:[] for n in nodes}
    for e in edges:
        if e['kind'] in LOGICAL:pred[e['target']].append(e['source'])
    def closure(ids):
        seen=set(ids);todo=list(ids)
        while todo:
            for x in pred[todo.pop()]:
                if x not in seen:seen.add(x);todo.append(x)
        return sorted(seen)
    rows=[]
    for record in scope['source_rows']:
        id=record['id'];h,n=mapping[id];ret=retained.get(id,[])
        kind=('excluded' if id in excluded else 'retained_input' if id.startswith('retained.') else
          'historically_answered_question' if id=='L012.question.type2' else
          'corrected_source_statement' if id in ['L012.L4.5.branch0','new.sign_obstruction'] else
          'reused_complete_proof' if id.startswith('reused.') else
          'proof_organization' if id=='new.affine_organization' else 'proved_principal_component')
        rows.append(dict(id=id,source='L012',accepted_record=record,historical_outputs=h,new_outputs=n,
          retained_input_nodes=ret,qualification_context_nodes=['AF.Exclusions'] if id in excluded else [],
          coverage_kind=kind,cost=None,historical_closure=closure(h),new_closure=closure(n),retained_context_closure=closure(ret)))
        for hh in h:
            for nn in n:edge(hh,nn,'attribution','Source-to-current correspondence only. It does not import the historical proof or certify an incorrect literal statement.')
    principal_out=sorted({x for r in rows if r['coverage_kind'] in ['proved_principal_component','corrected_source_statement'] and not r['id'].startswith('new.') for x in r['new_outputs']})
    full_out=sorted({x for r in rows for x in r['new_outputs']})
    mainclosure=closure(principal_out)
    common=[n['id'] for n in nodes if n['side']=='new' and n['document']=='U_Affine' and n['category']=='proved_statement']
    source_bind=dict(source_id='L012',title='Regular 3-polytopes of order 2^n p',
      edition='arXiv:2001.02945v2, 14 July 2024; no journal collation claimed',physical_pages=17,
      primary=bind('research','sources/regular_2np2025.pdf'),extracted_context=bind('research',primary),
      original_pdf_available=True,pdf_cost=None,text_cost=None)
    accepted_spans={k:sec(k) for k in scope['proof_regions']}
    graph=dict(schema='human_compression.paired_logical_dag.v1',status='AUTHOR_FROZEN_CANDIDATE_REQUIRES_INDEPENDENT_SEMANTIC_REVIEW',
      scope='One admitted affine principal source contract, all 33 inherited rows; historical documentary versus current complete common/application routes.',
      public_proof_edition_commit='1eb5745',public_measurement_edition_commit='fe91a420a9120a0566b474209c71e1732cc5bebe',source_order=['L012'],applications={'L012':'A_Affine'},
      edge_orientation='prerequisite -> use',logical_edge_kinds=LOGICAL,nonlogical_edge_kinds=OTHER,
      source_bindings={'L012':source_bind},immutable_inputs=list(inputs.values()),accepted_scope_spans=accepted_spans,
      nodes=nodes,edges=edges,new_application_outputs={'L012':principal_out},new_output_closures={'L012':mainclosure},
      full_record_outputs=full_out,full_record_closure=closure(full_out),
      additional_current_outputs={'AF.KnownAnswer':closure(['AF.KnownAnswer']),'AL.SmallerPeriods':closure(['AL.SmallerPeriods'])},
      unused_common_statement_nodes=sorted(set(common)-set(mainclosure)),
      required_mathematical_programs=['program.'+x[0] for x in pmap],
      diagnostic_programs=['diagnostic.controls'],operational_drivers=['driver.check','driver.integrity'],
      formal_evidence=dict(report_count=9,module_counts=[2,3,4],evidence_only=True,application_instantiations_formalized=False),
      graph_granularity='Named statements plus distinct proof interfaces and actual computational dependencies; section contexts can overlap.',
      node_count_policy='Inventory only; neither graph size nor edge count measures mathematical complexity or compression.',
      measurement=dict(weights_assigned=False,exclusive_partition_assigned=False,whole_common_paper_paid=True,
        complete_six_programs_paid=True,unused_common_statements_not_removed=True,
        accepted_numerical_packet='topic_Affine_measurement_results/manifest.json',
        numerical_values_not_recomputed=True,external_and_graphic_cost=None),
      new_source_credit=0,new_question_credit=0,compression_ratio=None,
      limits=['Historical arrows record dependencies asserted or used in the source, including its literal sign defect; they are not a retrospective proof certification.',
        'The complete current proof is locally present. Earlier own umbrellas are provenance, not unpriced mathematical premises.',
        'The six required programs are complete files. Two drivers and one finite diagnostic are separate operational/validation evidence.',
        'No cost partition, arithmetic, font calibration, source acquisition or mathematical recomputation is performed here.'])
    graph['checks']=dict(nodes=len(nodes),edges=len(edges),nodes_by_side=dict(Counter(n['side'] for n in nodes)),
      nodes_by_category=dict(Counter(n['category'] for n in nodes)),edges_by_kind=dict(Counter(e['kind'] for e in edges)),source_clauses=33)
    coverage=dict(schema='human_compression.paired_contract_routes.v1',rows=rows,source_clause_count=33,
      accepted_scope_binding=bind('public',BASE+'scope.json'),principal_contracts_unchanged=1,
      excluded_assertion_ids=sorted(excluded),historical_graph_semantics='Dependencies asserted/used in the bound preprint, not retrospective certification.',
      comparison_arrows_not_logical=True,weights_assigned=False,new_source_credit=0,new_question_credit=0)
    protocol=dict(schema='human_compression.logical_graph_protocol.v1',status='LOGICAL_ONLY',authoritative_scope=bind('public',BASE+'scope.json'),
      accepted_contract_rows=33,accepted_proof_context_spans=len(accepted_spans),source_order=['L012'],
      edge_orientation='prerequisite -> use',logical_edge_kinds=LOGICAL,nonlogical_edge_kinds=OTHER,
      required_programs=graph['required_mathematical_programs'],auxiliary_roles={'diagnostics':graph['diagnostic_programs'],'drivers':graph['operational_drivers']},
      source_locator_policy='Exact UTF-8 text hashes, codepoint and line intervals; historical primary PDF pages. Overlaps allowed and not cost owners.',
      formal_evidence_only=True,cost_policy='No weights or ratios. Full common paper and complete required code remain charged in the independently accepted numerical audit.',
      review_boundary='Independent semantic review must check edges, exclusions and actual proof use. Automated closure checks do not establish those meanings.',primary_redistribution=False)
    out.mkdir(parents=True,exist_ok=True)
    for name,obj in [('logical_graph.json',graph),('coverage.json',coverage),('protocol.json',protocol)]:
        (out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    return graph

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--public-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);o=a.parse_args()
    g=build(o.study_root,o.public_root,o.out);print(json.dumps(g['checks']))
