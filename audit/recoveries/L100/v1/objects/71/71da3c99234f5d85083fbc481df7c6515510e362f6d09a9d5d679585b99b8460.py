import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path

S=Path('/Users/sasha/medusa/research/leemans');W=Path(__file__).resolve().parent;P=W.parent/'constructions_component_v1'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,base=None):return {'path':str(p.relative_to(base)) if base else str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable packet exists');P.mkdir()
    for name in ['constructions.py','controls.py','check.py','export_input.g','constructions.tex','README.rst','approach.rst','freeze.py']:
        shutil.copyfile(W/name,P/name)
    shutil.copyfile(W/'native02/constructions.pdf',P/'constructions.pdf')
    for src,dst in [('literal02','expected'),('input01','expected_input'),('controls01','author_controls'),('development','development'),('native01','development/native01'),('native02','native'),('literal01','development/literal01'),('literal01_receipt','development/literal01_receipt'),('literal02_receipt','author_literal_receipt'),('source','source_rasters')]:
        shutil.copytree(W/src,P/dst)
    source=S/'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf'
    routes={'source':row(source,S),'edition':'complete22-page Halle preprint; laterjournaluncollected','native_pages_read':[8,9,10,12,13,14,15,16],
      'complete_construction_claims':['Construction-5.1','Construction-5.2','Lemma4.1','Lemma4.2','Lemma4.3','Table1'],
      'finite_boundary':{'six_subsets':54264,'hyperovals':168,'hyperoval_orbits':[56,56,56],'objects':[21,21,56,56,210],'models':2,'flag_types_per_model':32,'positive_rank_base_residues_per_model':31,'chambers_per_model':20160,'normalizer_full_incidence_maps':24,'source_table1_entries':20},
      'truncation_routes':[{'parent':v,'source_label':l,'retained_source_types':[x+1 for x in ts]} for v,l,ts in [('5.1','4.1',(1,2,3,4)),('5.2','4.1',(1,2,3,4)),('5.1','4.10',(0,2,3,4)),('5.1','3.1',(1,2,4)),('5.2','3.1',(1,2,4)),('5.1','3.6',(2,3,4)),('5.1','2.2',(2,4)),('5.2','2.2',(2,4))]],
      'literal_truncation_qualifications':['All maps are identity on retained objects/incidence and surjective on chamber projections.','No classification by numeric diagram is inferred.','Previously cited independent constructions are not identified without a supplied map.'],
      'local_two_transitivity':{'5.1':[False,True,True,True,True],'5.2':[False,True,True,True,True],'2.2_local_degrees':[15,4],'2.2_flags':[False,True]},
      'remaining':['Higher-rank exhaustion and rank bounds','Other constructions and doubling','Full automorphism and correlation groups','G-conjugacy fusion multiplicities','Group names/kernels beyond reported orders','Any unlisted source clause'],'whole_source_credit':0,'measurement_credit':0,'question_credit':0,'Lean_credit':0}
    save(P/'source_routes.json',routes)
    save(P/'roles.json',{'author':'publication_recovery','root_input':'Previously accepted rank-two input, scope/literal-mapping requests and standard flag-transitivity transport clarification; no final distinct review yet.','underlying_mathematics':'Gottschalk--Leemans constructions and attributed earlier work','distinct_review_pending':True,'new_priority_claim':False})
    old=W/'development/constructions_before_truncations.py'
    save(P/'historical_aliases.json',[{'logical_path':str(W/'constructions.py'),'sha256':sha(old),'exact_packet_path':'development/constructions_before_truncations.py','reason':'Retained first complete two-model execution before the truncation extension.'}])
    deps={}
    def add(p,expected=None):
        p=p.resolve();r=row(p)
        if expected:need(r['sha256']==expected['sha256'] and r['bytes']==expected['bytes'],'acquired binding '+str(p))
        if p in deps:need(deps[p]==r,'conflicting dep')
        deps[p]=r
    roots={
      'corpus106_L100_rank_two_v1':'2a53441260ce172d195ae028e433d21d9b4af75fcd74209ae1fd7a40c12ea114',
      'corpus106_L100_rank_two_v2':'ff40f6de14f2676f867c8fccf4f8a2065a3741bd900cb4960bb9bfa33bb19971',
      'corpus106_L100_rank_two_independent_review':'9e4443356c32816da7238af18566f34064b2bbf327b52f1c7b2cc0ce30b10b18',
      'corpus106_L100_rank_two_root_adoption':'c7f806d92f93372122f0ee02fe517955dbaa882bf5a9457418027b32d777c240'}
    for folder,h in roots.items():
        root=S/folder;m=root/'manifest.json';need(sha(m)==h,'exact acquired manifest');add(m)
        manifest=json.loads(m.read_text())
        for r in manifest['exports']:add(root/r['path'],r)
        for r in json.loads((root/'dependencies.json').read_text()):
            p=Path(r['path']);add(p if p.is_absolute() else S/p,r)
    for p in [source,S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',S/'geometry/psl3_4/result.g',Path(sys.executable).resolve(),Path('/opt/homebrew/bin/gap').resolve(),Path('/opt/homebrew/bin/pdflatex').resolve(),Path('/opt/homebrew/bin/gs').resolve()]:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    final=[]
    for p,r in sorted(deps.items(),key=lambda x:str(x[0])):
        if p.is_relative_to(S):r={**r,'path':str(p.relative_to(S)),'namespace':'study'}
        else:r={**r,'namespace':'runtime'}
        final.append(r)
    save(P/'dependencies.json',final)
    save(P/'acquired_roots.json',roots)
    exports=[row(p,P) for p in sorted(P.rglob('*')) if p.is_file()]
    manifest={'status':'AUTHOR_COMPLETE_L100_TWO_PROJECTIVE_CONSTRUCTIONS_AWAITING_DISTINCT_REVIEW','exports':exports}
    save(P/'manifest.json',manifest)
    print(json.dumps({'packet':str(P),'manifest_sha256':sha(P/'manifest.json'),'exports':len(exports),'dependencies':len(final)},indent=2))
if __name__=='__main__':main()
