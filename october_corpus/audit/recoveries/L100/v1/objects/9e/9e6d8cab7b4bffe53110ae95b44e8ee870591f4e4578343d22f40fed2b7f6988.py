import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
from pypdf import PdfReader
E=Path(__file__).resolve().parent;G=E.parent;S=G.parents[1];A=G/'butterfly_component_v1';P=G/'butterfly_component_v2';F=G/'butterfly_frozen01'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def verify(p,r):need(row(p)['sha256']==r['sha256']and row(p)['bytes']==r['bytes'],'exact binding '+str(p))
def main():
    need(not P.exists(),'new immutable successor');M=read(A/'manifest.json');need(row(A/'manifest.json')['sha256']=='5bd339ada959a6377e1600d5bbd0ed8267b62baf437665b5c7ba3facc0b8afab','exact predecessor')
    for r in M['exports']:verify(A/r['path'],r)
    deps={}
    def add(p,r=None):
        p=p.absolute()
        if r:verify(p,r)
        q=row(p);q['path']=str(p.relative_to(S))if p.is_relative_to(S)else str(p);q['namespace']='study'if p.is_relative_to(S)else'runtime'
        need(str(p)not in deps or deps[str(p)]==q,'unique binding');deps[str(p)]=q
    for r in read(A/'dependencies.json'):
        p=Path(r['path']);add(p if p.is_absolute()else S/p,r)
    add(A/'manifest.json')
    for r in M['exports']:add(A/r['path'],r)
    prior=read(F/'report.json');need(prior['status']=='PASS_L100_BUTTERFLY_OVAL_COMPONENT'and prior['replay']['butterfly_maps']==18 and prior['replay']['oval_maps']==6 and prior['controls']['damages']==63 and prior['optimization_guards']==14,'complete acquired predecessor science')
    old=(A/'constructions.tex').read_text();new=(E/'constructions.tex').read_text();before='This exhausts every possible opposite pole, and gives\nexactly one.';after='This exhausts every possible opposite pole. The combined search over these\nthree choices gives exactly one opposite pole for each retained pair.'
    need(old.count(before)==1 and new==old.replace(before,after),'one literal explanatory sentence delta')
    need(len(PdfReader(E/'constructions.pdf').pages)==4,'four final native pages');need(not any(t in (E/'constructions.log').read_text()for t in ['Overfull','Underfull','Warning']),'clean final native')
    shutil.copytree(A,P);(P/'manifest.json').unlink();shutil.move(P/'native_author',P/'native_v1');N=P/'native_author';N.mkdir()
    for p in E.iterdir():
        if p.is_file()and p.name!='freeze_successor.py':shutil.copyfile(p,N/p.name)
    shutil.copyfile(E/'constructions.tex',P/'constructions.tex');shutil.copyfile(E/'constructions.pdf',P/'constructions.pdf');shutil.copyfile(E/'prose_delta.diff',P/'prose_delta.diff');shutil.copyfile(E/'freeze_successor.py',P/'freeze_successor.py')
    science=[]
    for r in M['exports']:
        if r['path']in ['constructions.tex','constructions.pdf','dependencies.json']or r['path'].startswith('native_author/'):continue
        verify(P/r['path'],r);science.append(r['path'])
    for directory in [E,F]:
        for p in directory.rglob('*'):
            if p.is_file()and '__pycache__'not in p.parts:add(p)
    save(P/'edition_delta.json',dict(predecessor=row(A/'manifest.json',S),before=before,after=after,reason='Root requested precise prose saying uniqueness follows from the combined three-point search, not one completion for each separate point.',unchanged_exports=science,mathematical_code_or_map_delta=False,root_contribution='Editorial precision request; no new proof step or computation.',predecessor_author_replay=row(F/'report.json',S),new_mathematical_replays=0,final_native_pages=4,all_native_pages_directly_viewed=True))
    save(P/'dependencies.json',[deps[k]for k in sorted(deps)])
    exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()];save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_BUTTERFLY_OVAL_COMPONENT_V2',exports=exports,dependencies=len(deps)))
    for r in exports:verify(P/r['path'],r)
    for r in read(P/'dependencies.json'):
        p=Path(r['path']);verify(p if p.is_absolute()else S/p,r)
    report=dict(status='PASS_L100_BUTTERFLY_OVAL_EDITORIAL_SUCCESSOR',manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(deps),unchanged_scientific_exports=len(science),acquired_replay=row(F/'report.json'),mathematical_replays=0,native_pages=4)
    save(E/'successor_check.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
