import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'flag_structure_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable fresh packet');P.mkdir()
    for n in ['certify.py','check.py','flags.tex','README.rst','freeze.py']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native01/flags.pdf',P/'flags.pdf');shutil.copytree(W/'native01',P/'native_author');shutil.copytree(W/'native_source',P/'native_source')
    shutil.copytree(W/'run01',P/'history/run01');shutil.copyfile(W/'run01/fresh/report.json',P/'expected.json')
    roots={'parabolic_component_v2':'fc2a6933ce83667a652b6af5a8cbacbe730ba3926a0ef189e65893b4de52599a',
           'parabolic_review_v1':'7e9f1e33262d9f309ec0959f78975e5fe49efb77ab55491d922eb00f6167f449',
           'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
           'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
           'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86'}
    deps={};rr=[]
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'exact acquired binding '+str(p))
        if str(p) in deps:need(deps[str(p)]==r,'binding conflict')
        deps[str(p)]=r
    for name,h in roots.items():
        R=G/name;M=R/'manifest.json';need(row(M)['sha256']==h,'exact acquired root');add(M);rr.append(row(M,S))
        for r in read(M)['exports']:add(R/r['path'],r)
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute()else S/p,r)
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:add(p)
    save(P/'acquired_roots.json',rr)
    save(P/'scope.json',dict(source='corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf',physical_page=15,clause='Lemma4.3 intermediate flag names',types=['line','point','H3','H4','point pair'],flag_types=31,source_corrections=[],target_censuses=0,whole_source_credit=0))
    save(P/'roles.json',dict(author='publication_recovery',root='Requested closure of remaining source clauses; no new argument/code supplied here.',acquired_reviews='Parabolic v2 and projective construction, exact full closure.',distinct_review='pending'))
    out=[]
    for p,r in sorted(deps.items()):
        p=Path(p);out.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',out);exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()]
    save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_INTERMEDIATE_FLAG_STRUCTURE_COMPONENT_V1',exports=exports,dependencies=len(out)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(out)),indent=2))
if __name__=='__main__':main()
