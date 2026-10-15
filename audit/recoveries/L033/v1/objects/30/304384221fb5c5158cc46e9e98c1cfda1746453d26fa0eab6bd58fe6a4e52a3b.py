"""Author source join. Reads accepted finite records; runs no group search."""
import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,hashlib,json,re
W=Path(__file__).resolve().parent;S=W.parents[2]
AUD=S/'reboot_20261013/L033_work/principal_work/source_contract_work/audit01'
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
EXTRA={
'methods':('corpus106_L033_coxeter_lins_methods_v1/method.tex','corpus106_L033_coxeter_lins_methods_root_adoption'),
'cubic':('algebra/coxeter_quotients/cubic_example_v1/cubes.tex','algebra/coxeter_quotients/cubic_example_root_adoption')}
EXPECTED_GATES={
'residues':'e767e6fa22949710896f31a99574f6535faa141177e988681d4755db90fd2d0c',
'kernels':'46266dff9b182453ff4a91802769621eebb59b90af48377e5ea2ea3795b7fe9c',
'spherical':'140789d1e99d7c0f4bd2a076e63cde51254c190cf3b05fba0249ef44f905d7aa',
'translations':'f8c9aa195d760b21d8ce610c76d9904d7d00a4769dfa1d0108bb1a2432024c1b',
'periods':'08cdd4a61975615e0582cdd490b7a01404994c86b79913b29f4160627d0797e7',
'existence':'6a429450cc55eb12c02ded237acca6584df9eb1ae21482cec83cda54915f03ee',
'core':'1bf7aed4508bf9f5bdfdb3edb29e4cae830e5a4ef434c9015ecff0776d3761ce',
'names':'03aa7e96483e6c6dc2fa1df036acadd2522f8981e2c088b81e63199121635819',
'divisor':'0c4beaea0402380e83840a87a252c5f3a17168800d56a373ee9a2464e20c100b',
'small_square':'632c3eaf1f2217c8599ff8afb796de841883cc7602aa5d96742023f86e6c4ba4',
'methods':'ec933fee1a78221675be6060695e86e273aefefb13b94af63d60c0742686a4f5',
'cubic':'0df00ed910684714a6e66637d6aeb39b2c9223ba9edb0838d4769115b59571d3'}
DIAGRAMS={'3334':r'$(3,3,3,4)$','3335':r'$(3,3,3,5)$','3434':r'$(3,4,3,4)$','3534':r'$(3,5,3,4)$','3535':r'$(3,5,3,5)$','353':r'$[3,5,3]$','435':r'$[4,3,5]$','535':r'$[5,3,5]$','5333':r'$[5,3_3]$'}
NAME_TEX=[r'2^4:A_5:2',r'(2^3:L_2(7))\times C_2',r'2^5:A_5:2',r'(4\mathbin{\cdot}(2^4:A_5)):2',r'2^6:A_5:2',r'(A_5\times A_5):2',r'2^{1+4}:S_3:S_3',r'S_6\times C_2',r'S_6\times S_3',r'(2^3:L_2(7))\times C_2^2',r'L_2(7)\times S_3^2',r'2^8:S_3:S_3',r'L_2(16):2',r'2^5:A_5:2',r'(2^4:A_5:2)\times C_2',r'(2^5:A_5:2)\times C_2',r'2^5:A_5:2:2',r'(A_5\times A_5):2',r'L_2(16):2',r'(2^5:A_5)\times C_2',r'2^6:A_5',r'(2^6:A_5)\times C_2']

def build(out):
    need(not out.exists(),'fresh preparation');out.mkdir()
    prior=read(AUD/'claim_register.json');components=read(AUD/'components.json')
    for k,(p,g)in EXTRA.items():components[k]={'proof':pin(S/p),'gate_manifest':pin(S/g/'manifest.json')}
    components['small_square']['gate_manifest']=pin(S/'algebra/coxeter_quotients/small_square_root_adoption/manifest.json')
    for k,c in components.items():
        g=Path(c['gate_manifest']['path']);need(pin(g)['sha256']==EXPECTED_GATES[k],'exact gate '+k)
        c['gate_status']=read(g)['status'];c['author_manifest']=pin(Path(c['proof']['path']).parent/'manifest.json')
        c['proof_pdf']=pin(Path(c['proof']['path']).with_suffix('.pdf'))
        c['review']=pin(g.parent/'review.json');c['dependencies']=pin(g.parent/'dependencies.json')
    rows=copy.deepcopy(prior['rows'])
    for r in rows:
        rid=r['id'];r.pop('component_records',None)
        r['audit_status']=r['status']
        if rid=='E2.5':r.update(status='ACQUIRED_COMPLETE_PROOF',component_keys=['cubic'],route='Exact infinite dual-grid proof and source type permutation; no finite zero-period substitution.')
        if rid in ['P2.2','C.reducible']:r.update(status='PROVED_ELEMENTARY_SYNTHESIS_JOIN',route='Complete proof in principal.tex Proposition '+('1'if rid=='P2.2'else'2'))
        if rid in ['T2.3','C.regular_marking','C.coxeter_cover']:r['status']='ACQUIRED_COMPLETE_PROOF_INTERFACE'
        if rid=='E3.3':r['route']='Acquired antipodal D4 flag; new explicit fourth-type nonextension proof in principal.tex Section2.'
        if rid.startswith(('P2.','T2.','E2.','T3.','E3.'))or rid in ['C.regular_marking','C.coxeter_cover','C.reducible']:section=2
        elif rid.startswith(('T4.','Table1.'))or rid=='C.coxeter_element':section=3
        elif rid.startswith(('T5.','Euclidean.'))or rid in ['C.projective_euclidean','C.affine_future','C.affine_kernel_enumeration','C.abstract_classification']:section=4
        elif rid.startswith(('Hyperbolic.','Table2.'))or rid in ['C.type_trichotomy','C.hypermap_rotation_cover','C.affine_rank2_boundary']:section=5
        elif rid.startswith(('Table3.','Minimum.')):section=6
        else:section=7
        r['manuscript_section']=section
        if not r.get('component_keys')and r['status'] not in ['PROVED_ELEMENTARY_SYNTHESIS_JOIN']:
            r['retained_or_scope']=True
    need(len(rows)==109 and len({r['id']for r in rows})==109,'exact source inventory')
    need(not any('PENDING'in r['status']for r in rows),'all source dispositions explicit')
    names=read(S/'corpus106_L033_hyperbolic_names_v1/source_map.json')['rows']
    positive=read(S/'corpus106_L033_hyperbolic_core_v1/positives.json')
    core=read(S/'corpus106_L033_hyperbolic_core_v1/source_map.json')['types']
    table=[]
    for r,t in zip(names,NAME_TEX):
        hits=[z for z in positive if(z['type'],z['node'])==(r['type'],r['selected_node'])];need(len(hits)==1,'literal selected node')
        z=hits[0];need(z['order']==r['order']and z['local_orders']==r['local_orders']==core[r['type']]['universal_local_orders'],'exact universal witness join')
        table.append({**r,'tex_group':t,'tuple_sha256':hashlib.sha256(json.dumps(z['permutations'],separators=(',',':')).encode()).hexdigest()})
    minima=[]
    for rid in ['3334','3335','3434','3534','3535','353','435','535','5333']:
        r=next(x for x in rows if x['id']=='Minimum.'+rid)
        if rid!='3535':
            z=core[rid];need((r['complete_bound'],r['broad_minimum'],r['universal_minimum'])==(z['bound'],z['broad_minimum'],z['universal_minimum']),'minimum interface '+rid)
        else:need((r['complete_bound'],r['broad_minimum'],r['universal_minimum'],r['universal_lower_bound_exclusive'])==(3840,1920,None,3840),'separate ninth-square theorem')
        minima.append(dict(type=rid,bound=r['complete_bound'],broad=r['broad_minimum'],universal=r['universal_minimum'],universal_exclusion=r['universal_lower_bound_exclusive']))
    premises=[
    ('Coxeter complex','Classical parabolic intersection, fundamental chambers, flag complex and chamber regularity.','Humphreys; McMullen--Schulte; Tits',[20,25,29]),
    ('Geometric representations','Faithful finite/affine/Coxeter representation; affine alcove stabilizers and discreteness.','Humphreys; fixed source',[20]),
    ('Diagram classifications','Finite, irreducible affine and compact hyperbolic simplex lists; exact21 Table2 rows.','Humphreys6.9; McMullen--Schulte3C',[20,25]),
    ('Finite normal subgroups','Maxwell Theorem0.1 as quoted by source4.1; primary full proof not acquired.','Maxwell1998 through fixed source',[22]),
    ('String correspondence','String C-group to regular abstract polytope, with exact marking.','Aschbacher; Schulte',[1,27]),
    ('Toroidal exhaustion','Exact rank3/cubic/F4 families and rank4 nonstring exhaustion; no all-rank new lattice classification.','Coxeter; Cacciari; McMullen--Schulte; Ens',[7,11,14,24,25]),
    ('Earlier constructions','Named historical hypermap, modular, Janko and star-polytope constructions retained separately.','Corn--Singerman; Monson--Schulte; Breda--Jones--Schulte; Hartley--Leemans; McMullen',[3,10,12,19,23,26]),
    ('Finite computation','Complete fixed GAP/LINS algorithms and characteristically-simple, multiplier and socle-overgroup tables.','Installed LINS documentation, Firth algorithm; explicit accepted interface proofs',[])]
    corrections=[
    dict(id='quotient',source=['T3.2'],result='Local injection+flag transitivity is insufficient; affineA2 counterexample, exact pair-product repair.'),
    dict(id='local_scope',source=['T3.4'],result='Marked quotient remains; local injection needs universal residues. Broad1920 has localH3order60 not120.'),
    dict(id='E6',source=['Table1.E6'],result='51840=72*6!, not12*6!.'),
    dict(id='half_power',source=['C.coxeter_element'],result='Blanket half-power longest-element statement qualified by actualA3 counterexample.'),
    dict(id='affine_sufficiency',source=['C.affine_kernel_enumeration'],result='Parabolic avoidance alone does not classify valid affine quotient geometries.'),
    dict(id='table_rows',source=['Table3.3434.1','Table3.3534.1','Table3.3535.1','Table3.3535.2'],result='All exact-order kernels failIP; source orders336/2160/3840/9720 excluded.'),
    dict(id='minima',source=['Minimum.'+x['type']for x in minima],result='Two explicitly distinguished local conventions, with two universal exclusion-only bounds.')]
    source_text=(S/'sources/catalogue_L033.txt').read_text();biblio=source_text.split('References\n',1)[1].split('16 FERNANDES',1)[0]
    biblio=biblio.replace('AN EXPLORATION OF LOCALLY SPHERICAL REGULAR HYPERTOPES 15\n','')
    entries=re.split(r'(?m)^(\d+)\. ',biblio)[1:];bibliography=[]
    for n,t in zip(entries[::2],entries[1::2]):
        n=int(n);roles=[p[0]for p in premises if n in p[3]]
        if n in [9,21]:roles=['Historical forthcoming work; not an acquired theorem']
        if n==16:roles=['Source background theory replaced/acquired by full L052 residue proof']
        if n in [18,28]:roles=['Retained Euclidean projective-residue context']
        bibliography.append(dict(source_reference=n,literal_extracted_text=t.strip(),roles=roles or['Source bibliography/background; not an extra premise of the new synthesis']))
    need([r['source_reference']for r in bibliography]==list(range(1,30)),'all29source citations')
    save(out/'components.json',components)
    save(out/'claim_register.json',dict(status='AUTHOR_COMPLETE_CORRECTED_SOURCE_DISPOSITIONS_AWAITING_DISTINCT_REVIEW',source='L033',source_sha256=prior['source_sha256'],rows=rows,legacy_rows=83,additional_table2_rows=21,additional_scope_rows=5,retained_inputs=[dict(id=i+1,name=p[0],scope=p[1],attribution=p[2],source_references=p[3])for i,p in enumerate(premises)],corrections=corrections,principal_refutation=False,new_measurements=0,new_Lean=0,new_question_credit=0,public_admission=False))
    save(out/'bibliography_routes.json',bibliography);save(out/'named_rows.json',table);save(out/'minima.json',minima)
    head='\\begin{center}\\small\n\\begin{longtable}{llr}\\toprule\nDiagram & Certified source group & Order\\\\\\midrule\n\\endhead\n'
    (out/'named_table.tex').write_text(head+''.join(DIAGRAMS[r['type']]+' & $'+r['tex_group']+'$ & '+str(r['order'])+r'\\'+'\n'for r in table)+r'\bottomrule\end{longtable}\end{center}'+'\n')
    head='\\begin{center}\\small\n\\begin{tabular}{lrrr}\\toprule\nDiagram & Complete bound & Broad minimum & Universal minimum\\\\\\midrule\n'
    (out/'minimum_table.tex').write_text(head+''.join(DIAGRAMS[r['type']]+' & '+str(r['bound'])+' & '+str(r['broad'])+' & '+(str(r['universal'])if r['universal']else'$>'+str(r['universal_exclusion'])+'$')+r'\\'+'\n'for r in minima)+r'\bottomrule\end{tabular}\end{center}'+'\n')
    save(out/'report.json',dict(status='PASS_L033_SOURCE_JOIN',source_clauses=109,components=len(components),positive_named_rows=len(table),excluded_rows=4,minima=len(minima),table2_rows=21,bibliography=29,retained_inputs=len(premises),correction_groups=len(corrections),new_target_censuses=0))
    print(json.dumps(read(out/'report.json')))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);v=a.parse_args();need(v.out.is_absolute(),'absolute output');build(v.out)
