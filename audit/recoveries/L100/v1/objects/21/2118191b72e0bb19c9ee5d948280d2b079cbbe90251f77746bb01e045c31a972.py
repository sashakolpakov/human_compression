import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'aut_cor_structure_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable fresh packet');P.mkdir()
    for n in ['automorphism_names.py','validate.py','source_names.py','check.py','structures.tex','README.rst','plan.rst','primary_notation.json','atlas_l34.html','freeze.py']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native02/structures.pdf',P/'structures.pdf');shutil.copytree(W/'native02',P/'native_author')
    H=P/'history';H.mkdir()
    for n in ['probe01','batch01','full01','validate01','native01']:shutil.copytree(W/n,H/n)
    for n in ['run_bounded.py','run_bounded_v2.py','outer_involutions01.json','source_names01.json']:shutil.copyfile(W/n,H/n)
    E=P/'expected';E.mkdir()
    for i in range(1,30):shutil.copyfile(W/f'full01/result/model{i}.json',E/f'model{i}.json')
    shutil.copyfile(W/'full01/result/coordinate_group.json',E/'coordinate_group.json');shutil.copyfile(W/'validate01/report.json',E/'validation.json')
    shutil.copyfile(W/'source_names01.json',P/'source_names.json')
    N=P/'native_source';N.mkdir()
    for i in range(1,8):shutil.copyfile(G/f'source_join_component_v2/native/high-0{i}.png',N/f'preprint-page-{i+6:02d}.png')
    shutil.copyfile(G/'source_join_component_v2/definitions/source-02.png',N/'definition-source-02.png')
    roots={
      'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
      'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
      'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86',
      'palette_serialization_v1':'5399e45468b83a49e0d2750a2087cb8e6006919b08548d0434b5195ed550eff3',
      'palette_serialization_review_v1':'6a09697960e322a8d10bcabc9354504f8e0b1e6c17a9ed485ab36c25aa6ab96a',
      'source_join_component_v2':'2e69c5d047fa7d15fb8d101090a78c18a69f3100db2aeb111abc107878639ffb',
      'source_join_review_v2':'1cbc91ca8ba73e421cf2e6412b20654a5057f7545ffc232d29566d169f41fd00',
      'doubling_component_v1':'1930bd893bc514511b02ea1736e7c292e26b127d3a64475cbe0ac91dd366ffa1',
      'doubling_review_v1':'2c74cab966cfed8a74366f57e8ca7004ddadf5f6f347b97ec1efd4e20d318774',
      'postprocess_review_v1':'2aec2b0183913fc9da8f24b46003311d1f06b60cb0278b517a0bf2538185bb96'}
    deps={};rootrows=[]
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'acquired binding '+str(p))
        if str(p)in deps:need(deps[str(p)]==r,'binding conflict')
        deps[str(p)]=r
    for name,h in roots.items():
        R=G/name;M=R/'manifest.json';need(row(M)['sha256']==h,'exact acquired root');add(M);rootrows.append(row(M,S))
        for r in read(M)['exports']:add(R/r['path'],r)
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute()else S/p,r)
    for p in (G/'postprocess_target01').rglob('*'):
        if p.is_file():add(p)
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:add(p)
    for p in [G/'constructions_component_v1/constructions.py',G/'remaining_audit_work/remaining_obligations02.rst',S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',Path(sys.executable).resolve(),Path('/opt/homebrew/bin/pdflatex'),Path('/opt/homebrew/bin/gs')]:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    save(P/'acquired_roots.json',rootrows)
    save(P/'development.json',dict(probe01='Model1 complete2.63s.',batch01='Remaining28 models complete6.60s. Every result preserved.',closure='Initial lightweight runner omitted one transitive imported Python file from its direct receipt list. The file is an immutable acquired export. Successor run_bounded_v2 explicitly adds it, and full01 freshly completes all29 in7.09s; original receipts remain unchanged.',validation='Separate witness validator passes all29/58,471052 all-vertex generator checks,16 damages and2 inconsistent-section controls.',native='Initial native01 had one overfull line; native02 changes only wording to remove an unbreakable slash compound and has three clean pages, all directly viewed.',notation='Root supplied primary notation pointers; browser exact PSigmaL paragraph read, direct HTTP401 retained as a limitation, ATLAS HTML acquired documentary only.',all_owned_handles_terminal=True))
    save(P/'roles.json',dict(author='publication_recovery',root_input='Suggested explicit coordinate/type actions and separately paid kernels/splittings; supplied primary notation pointers. No code, finite certificate, or new splitting proof contribution.',earlier_accepted_components='Acquired unchanged with complete proofs/reviews and exact literal interfaces.',distinct_review='pending',whole_source_credit=0,new_measurements=0))
    final=[]
    for p,r in sorted(deps.items()):
        p=Path(p);final.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',final)
    exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()];save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_AUT_COR_STRUCTURE_COMPONENT_V1',exports=exports,dependencies=len(final)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(final)),indent=2))
if __name__=='__main__':main()
