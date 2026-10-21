import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'parabolic_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable fresh packet');P.mkdir()
    for n in ['inventory.py','atoms_v3.py','kernels.py','validate.py','source_names.py','check.py','parabolics.tex','README.rst','freeze.py']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native02/parabolics.pdf',P/'parabolics.pdf');shutil.copytree(W/'native02',P/'native_author');shutil.copytree(W/'input01',P/'input01')
    H=P/'history';H.mkdir()
    for n in ['atoms01','atoms02','atoms03','kernels01','validate01','native01']:shutil.copytree(W/n,H/n)
    for n in ['atoms.py','atoms_v2.py']:shutil.copyfile(W/n,H/n)
    E=P/'expected';E.mkdir()
    for src,dst in [('atoms03/result/report.json','atoms.json'),('kernels01/result/report.json','kernels.json'),('validate01/result/report.json','validation.json')]:shutil.copyfile(W/src,E/dst)
    shutil.copyfile(W/'source_names01.json',P/'source_names.json')
    N=P/'native_source';N.mkdir()
    for i in range(1,8):shutil.copyfile(G/f'source_join_component_v2/native/high-0{i}.png',N/f'preprint-page-{i+6:02d}.png')
    shutil.copyfile(G/'source_join_component_v2/definitions/source-02.png',N/'preprint-page-04.png')
    roots={
      'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
      'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
      'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86',
      'palette_serialization_v1':'5399e45468b83a49e0d2750a2087cb8e6006919b08548d0434b5195ed550eff3',
      'palette_serialization_review_v1':'6a09697960e322a8d10bcabc9354504f8e0b1e6c17a9ed485ab36c25aa6ab96a',
      'source_join_component_v2':'2e69c5d047fa7d15fb8d101090a78c18a69f3100db2aeb111abc107878639ffb',
      'source_join_review_v2':'1cbc91ca8ba73e421cf2e6412b20654a5057f7545ffc232d29566d169f41fd00',
      'baer_component_v1':'a8569d8dfad9403a8a7fc41271aee37c8aa8491de878e8bae852d3e9f50bd07d',
      'baer_review_v1':'2d9ee5f051d2ab8a07573c2ebd5d4d56d7816bfbe6fdcfa5de70de0de9acfd5e'}
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
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:add(p)
    for p in [S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',Path(sys.executable).resolve(),Path('/opt/homebrew/bin/pdflatex'),Path('/opt/homebrew/bin/gs')]:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    save(P/'acquired_roots.json',rootrows)
    save(P/'development.json',dict(atoms01='Syntax failure before scientific execution: three conditional expressions omitted spaces after else. Original file/stdout/stderr/receipt retained.',atoms02='Syntax-only successor passed62 atoms, then rejected the next order60 atom because the initial selector tried a point oval only. Entire successful prefix and failure retained.',atoms03='Adds a literal five-line orbit action for the dual-oval case. All77 complete in0.53s; no subgroup census or source count inferred from this run.',kernels01='All61 distinct actual(H,K) certificates/99 source positions complete, with actual quotient tables and explicit complements/nonsplittings.',validate01='Separate witness validation passes all77/61;21 damaged records reject. Source join adds3 damaged-source rejections.',native01='Initial build failed on an undefined GL macro; full initial TeX and logs retained. The final native02 adds the macro and corrects the bibliography title to the fixed source title; no mathematical change.',native02='Three clean pages, all directly viewed. Source pp4,7--13 directly viewed for notation and every structural label.',all_owned_handles_terminal=True))
    save(P/'roles.json',dict(author='publication_recovery',root_input='Earlier suggested literal projective stabilizer routes, and requested exact kernels and splitting beyond cardinality agreement. Advisory strategy only; no new code or proof step supplied for this component.',earlier_accepted_components='Acquired unchanged with complete proofs/reviews and exact literal model/kernel/node interfaces.',distinct_review='pending',whole_source_credit=0,new_measurements=0))
    final=[]
    for p,r in sorted(deps.items()):
        p=Path(p);final.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',final)
    exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()];save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_PARABOLIC_KERNEL_COMPONENT_V1',exports=exports,dependencies=len(final)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(final)),indent=2))
if __name__=='__main__':main()
