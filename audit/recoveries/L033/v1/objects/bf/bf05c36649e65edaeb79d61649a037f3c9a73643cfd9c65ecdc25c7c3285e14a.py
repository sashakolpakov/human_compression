"""Literal source-disposition audit; does not claim principal acceptance."""
from pathlib import Path
import json,hashlib,copy
W=Path(__file__).resolve().parent;S=W.parents[3];O=W/'audit01'
def read(p):return json.loads(p.read_text())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not O.exists(),'fresh audit');old=W.parent/'claim_register_draft01.json';prior=read(old);rows=copy.deepcopy(prior['rows'])
components={
'residues':('corpus106_L052_residue_theory_v1/residue_theory.tex','corpus106_L052_residue_theory_root_adoption'),
'kernels':('corpus106_L033_quotient_kernels_v1/quotient_kernels.tex','corpus106_L033_quotient_kernels_root_adoption'),
'spherical':('corpus106_L033_spherical_v2/spherical_quotients.tex','corpus106_L033_spherical_root_adoption'),
'translations':('corpus106_L033_translation_kernel_v2/translation_kernel.tex','corpus106_L033_translation_kernel_root_review'),
'periods':('corpus106_L033_period_adapter_v1/period_adapter.tex','corpus106_L033_period_adapter_root_review'),
'existence':('corpus106_L033_finite_quotients_v2/finite_quotients.tex','corpus106_L033_finite_quotients_root_adoption'),
'core':('corpus106_L033_hyperbolic_core_v1/finite_core.tex','corpus106_L033_hyperbolic_core_root_adoption'),
'names':('corpus106_L033_hyperbolic_names_v1/names.tex','corpus106_L033_hyperbolic_names_root_adoption'),
'divisor':('algebra/coxeter_quotients/divisor_v1/quotients.tex','algebra/coxeter_quotients/divisor_root_adoption'),
'small_square':('algebra/coxeter_quotients/small_square_v1/square.tex','algebra/coxeter_quotients/small_square_review_v1')}
component_records={}
deps={}
def bind(p):
    r=pin(p);deps[r['path']]=r;return r
for k,(proof,gate)in components.items():
    gate=S/gate;m=read(gate/'manifest.json')
    component_records[k]=dict(proof=bind(S/proof),gate_manifest=bind(gate/'manifest.json'),gate_status=m['status'])
    for name in ['review.json','dependencies.json']:
        if(gate/name).exists():component_records[k][name.replace('.json','')]=bind(gate/name)
names=read(S/'corpus106_L033_hyperbolic_names_v1/source_map.json');named={r['source_id']:r for r in names['rows']}
minima={'3334':(7680,168,1920),'3335':(7200,2520,7200),'3434':(9216,168,1152),'3534':(2160,1080,None),'3535':(3840,1920,None),'353':(8160,660,8160),'435':(7680,1920,3840),'535':(8160,3420,7200),'5333':(7680,960,3840)}
for r in rows:
    rid=r['id'];r['prior_status']=r['status'];r['component_keys']=[]
    if rid in ['P2.1','T3.1']:
        r.update(status='ACQUIRED_COMPLETE_PROOF',component_keys=['kernels'],route='Exact maximal-parabolic proof and upward marked-lifting proof already written in the accepted kernel component; reproduce or cite in synthesis.')
    elif rid in ['P2.2','T2.3','C.regular_marking','C.coxeter_cover']:
        r.update(status='ACQUIRED_INTERFACE_SYNTHESIS_JOIN',component_keys=['residues'],route='Accepted regular marking/residue stabilizer/coset reconstruction, with a short literal right-coset explanation in synthesis.')
        if rid=='P2.2':r['qualification']='Arbitrary subgroup families give an action with kernel intersection_i Core_G(G_i), not automatically an embedding as the full automorphism group. The introductory sentence preceding the proposition is broader than the proposition itself.'
    elif rid=='E2.5':r.update(status='ROOT_AUTHOR_INTERFACE_PENDING',route='Root is authoring the literal cubic-dual zero-period construction. Do not set a finite theorem parameter t>=2 to zero.',qualification='Source types(0,2,1,3) correspond to H10 types(0,1,2,3); cubes become dual vertices, edges dual squares, vertices dual cubes. Direct infinite-grid geometry proof required.')
    elif rid=='T3.2':r.update(status='ACQUIRED_AUXILIARY_CORRECTION',component_keys=['kernels'])
    elif rid=='T3.4':r.update(status='ACQUIRED_BROAD_COUNTEREXAMPLE_AND_QUALIFIED_REPAIR',component_keys=['translations','residues','small_square'],qualification='A marked Coxeter quotient and incidence reconstruction always hold. Local injection requires actual universal spherical residues. The accepted broad1920 square has local H3 groups60 versus universal120, explicitly contradicting local injection under the p5 finite-diagram definition.')
    elif rid in ['E3.3','T4.2','T4.3'] or rid.startswith('Table1.'):
        r.update(status='ACQUIRED_COMPLETE_PROOF' if rid!='Table1.E6'else'ACQUIRED_NUMERICAL_CORRECTION',component_keys=['spherical'])
        if rid.startswith('Table1.'):r['qualification']=(r.get('qualification')or'')+' Universal/projective identity and count are proved subject to the named finite Coxeter and Maxwell inputs. Conventional extended Schlafli notation is inherited, not a separate new presentation theorem.'
    elif rid=='T5.1':r.update(source_label='Corollary 5.1',status='ACQUIRED_QUALIFIED_PROOF',component_keys=['translations'],route='Direct reflection-commutator proof; the legacy ID is retained only for stable mapping, because the source says Corollary5.1.')
    elif rid=='C.reducible':r.update(status='ELEMENTARY_SYNTHESIS_JOIN_PENDING',route='Disconnected marked generators commute; full IP makes their generated factors intersect trivially. Cosets and incidence then split as a direct sum. Include this short proof explicitly.')
    elif rid=='C.coxeter_element':r.update(status='QUALIFIED_RETAINED_CONTEXT',component_keys=['spherical'],qualification='Coxeter-element conjugacy is retained in the finite setting. The blanket half-power-is-longest assertion is false: in standard A3, c=(1234), c^2=(13)(24), whereas w0=(14)(23). Only verified central-antipode powers are used.')
    elif rid.startswith('Euclidean.B3.')or rid.startswith('Euclidean.A3.'):
        r.update(status='ACQUIRED_FAMILY_EXISTENCE_RETAINED_EXHAUSTION',component_keys=['periods'])
    elif rid.startswith('Euclidean.'):
        r['status']='EXPLICIT_RETAINED_FAMILY_CLASSIFICATION';r['route']='Retain the exact attributed family and domain below; no fresh independent family exhaustion is claimed.'
        r['source_domains']={'Euclidean.square':['{4,4}(s,0):s>=2','{4,4}(s,s):s>=1'],'Euclidean.triangular':['{3,6}(s,0):s>=2','{3,6}(s,s):s>=1'],'Euclidean.hypermap':['(3,3,3)(s,0):s>=2','(3,3,3)(s,s):s>=2'],'Euclidean.cubic':['{4,3^(n-2),4}_(s^k,0^(n-k)):s>=2;k=1,2,n'],'Euclidean.F4':['{3,3,4,3}_(s^k,0^(4-k)):s>=2;k=1,2']}[rid]
    elif rid=='Hyperbolic.finite_existence':r.update(status='ACQUIRED_UNIFORM_PROOF',component_keys=['existence'],route='Finite triple-parabolic avoidance plus integral matrix reduction proves arbitrary chamber size for rank>=3, including all retained compact nonstring types.')
    elif rid in named:
        r.update(status='ACQUIRED_POSITIVE_NAMED_MARKING',component_keys=['core','names'],actual_certificate=named[rid],qualification='Actual universal spherical local orders, fullIP/flag tests and exact structural certificates are joined. Semidirect symbols use the actual certified actions; no uniqueness is inferred from notation.')
    elif rid in ['Table3.3434.1','Table3.3534.1','Table3.3535.1','Table3.3535.2']:
        key={'Table3.3434.1':'core','Table3.3534.1':'core','Table3.3535.1':'small_square','Table3.3535.2':'divisor'}[rid]
        r.update(status='ACQUIRED_EXCLUDED_PRINTED_ROW',component_keys=[key],qualification='All exact-order normal kernels of the fixed marked Coxeter presentation fail necessary IP, under either local convention. No abstract named-group existence is inferred or required.')
    elif rid.startswith('Minimum.'):
        t=rid.split('.')[1];bound,broad,universal=minima[t]
        r.update(status='ACQUIRED_MINIMUM_WITH_EXPLICIT_LOCAL_CONVENTION',component_keys=['small_square'if t=='3535'else'core'],complete_bound=bound,broad_minimum=broad,universal_minimum=universal,universal_lower_bound_exclusive=bound if universal is None else None,qualification='Every displayed broad minimum is attained. A null universal minimum means exclusion through the bound only. Counts are ordered kernels, not unlabelled geometries.')
    if r['component_keys']:r['component_records']=[component_records[k]for k in r['component_keys']]
table2=[
('affine.A','Atilde_(n-1)','n>=3','cycle on n vertices, all bonds3'),('affine.D','Dtilde_(n-1)','n>=5','affine D tree, all bonds3'),('affine.C','Ctilde_(n-1)','n>=3','n-node chain, both end bonds4, other bonds3'),('affine.B','Btilde_(n-1)','n>=4','affine B tree, single end bond4, other bonds3'),('affine.E6','Etilde6','rank7','three arms of length2 from central node, all bonds3'),('affine.E7','Etilde7','rank8','three arms of lengths1,3,3, all bonds3'),('affine.E8','Etilde8','rank9','three arms of lengths1,2,5, all bonds3'),('affine.F4','Ftilde4','rank5','chain3,3,4,3'),('affine.G2','Gtilde2','rank3','chain3,6'),('affine.A1','Atilde1','rank2','two nodes, infinity bond'),
('hyperbolic.string2','[p,q]','p,q>=3;1/p+1/q<1/2','rank3 string'),('hyperbolic.triangle','[(k,l,m)]','k,l,m>=3;1/k+1/l+1/m<1','rank3 triangle'),('hyperbolic.333p','[(3,3,3,p)]','p=4,5','rank4 square'),('hyperbolic.3434','[(3,4,3,4)]','fixed','rank4 square'),('hyperbolic.353p','[(3,5,3,p)]','p=4,5','rank4 square'),('hyperbolic.pentagon','[(3,3,3,3,4)]','fixed','rank5 pentagon'),('hyperbolic.p35','[p,3,5]','p=4,5','rank4 string'),('hyperbolic.353','[3,5,3]','fixed','rank4 string'),('hyperbolic.p335','[p,3,3,5]','p=3,4,5','rank5 string'),('hyperbolic.fork4','[5,3_3]','fixed','rank4 fork with three bonds5,3,3'),('hyperbolic.fork5','[5,3,3_3]','fixed','rank5 fork: 5-3 stem and two3 leaves')]
for key,label,domain,diagram in table2:
    rows.append(dict(id='Table2.'+key,pages=[12],source_label=label,source_domain=domain,diagram=diagram,status='RETAINED_DIAGRAM_CLASSIFICATION',route='Humphreys[20]Section6.9 / McMullen-Schulte[25]Section3C; exact displayed list is an input, not a new enumeration.',component_keys=['existence']if key.startswith('hyperbolic.')else[],qualification='Rank2 affine A1 is universal dihedron context only; finite quotients change the infinity bond.'if key=='affine.A1'else None))
extras=[
('C.source_equivalence',[4],'Source equivalence includes reordering types and duality.','EXPLICIT_SCOPE_CONVENTION','Finite kernel counts refer to ordered marks; existence, exclusion and minimum joins are invariant under diagram relabelling. No kernel total is promoted to an unlabelled count.'),
('C.abstract_classification',[1,2,11],'Abstract says spherical and Euclidean classification; section5 reviews only specified affine families and announces remaining geometric classification.','QUALIFIED_PRINCIPAL_SCOPE','Give complete spherical result, qualified necessary affine translation theorem, exact listed families with named retained exhaustion, and recorded future-work scope. Do not claim a new all-rank invariant-lattice classification.'),
('C.affine_kernel_enumeration',[11],'Avoiding individual parabolics alone is described as enough to complete affine quotient classification.','ACQUIRED_QUALIFICATION','The accepted affine A2 translation example satisfies local injection but is a one-chamber quotient. Pair-product avoidance and full flag validity are additional requirements; arbitrary normal translation subgroups do not automatically give hypertopes.'),
('C.hypermap_rotation_cover',[13],'Corn-Singerman regular hypermap/universal triangle rotation presentation.','RETAINED_CONTEXTUAL_RESULT','Retain attribution[10] and the orientation-preserving triangle presentation; the new full reflection-group finite-existence proof does not reproduce every historical hypermap construction.'),
('C.affine_rank2_boundary',[12],'Affine A1 infinity diagram.','EXPLICIT_BOUNDARY','The accepted arbitrary-large finite same-diagram theorem requires rank>=3. A finite quotient of infinite dihedral group has finite pair order and a different diagram.')]
for rid,pages,claim,status,route in extras:rows.append(dict(id=rid,pages=pages,claim=claim,status=status,route=route,component_keys=[]))
need(len(rows)==109 and len({r['id']for r in rows})==109,'83 legacy+21 diagrams+5 scope clauses')
for p in [old,S/'sources/catalogue_L033.pdf',S/'sources/catalogue_L033.txt',S/'corpus106_L033_hyperbolic_names_v1/source_map.json',W/'synthesis_outline.rst',Path(__file__),W.parent.parent/'hyperbolic_recovery_work/source12.png',W.parent.parent/'hyperbolic_recovery_work/source14.png']:bind(p)
O.mkdir();save(O/'claim_register.json',dict(status='SOURCE_DISPOSITION_AUDIT_NOT_PRINCIPAL_ACCEPTANCE',source='L033',source_sha256=prior['source_sha256'],legacy_rows=83,additional_table2_rows=21,additional_scope_rows=5,rows=rows,whole_original_credit=0,new_Lean=0,new_question_credit=0,measurement=None))
save(O/'components.json',component_records)
save(O/'remaining.json',dict(status='UNPAID_SYNTHESIS_JOINS_ONLY_NOT_WHOLE_ACCEPTANCE',items=[dict(id='E2.5',owner='/root',need='Separate infinite-grid proof and exact dual/source map; final frozen acceptance not yet acquired.'),dict(id='P2.2',need='Write exact coset action/kernel and right-coset reconstruction join; acquired residue theorem supplies the substantive result.'),dict(id='C.reducible',need='Write commuting direct factors and direct-sum incidence argument.'),dict(id='principal',need='Complete coherent manuscript, all source routes, exact retained-input and correction lists, final independent review and publication closure.')],large_target_censuses_needed=0,not_to_claim=['Maxwell primary theorem reproved','Complete all-rank affine lattice classification','Historical five hyperbolic constructions independently recovered','Universal minima beyond2160/3840 for the two excluded types','Unlabelled classification counts from ordered kernel totals']))
save(O/'bindings.json',[deps[k]for k in sorted(deps)])
exports=[]
for p in sorted(O.iterdir()):
    r=pin(p);r['path']=p.name;exports.append(r)
save(O/'manifest.json',dict(status='SOURCE_DISPOSITION_AUDIT_NOT_PRINCIPAL_ACCEPTANCE',exports=exports));print(json.dumps(dict(manifest=pin(O/'manifest.json'),rows=len(rows),bindings=len(deps),whole_original_credit=0)))
