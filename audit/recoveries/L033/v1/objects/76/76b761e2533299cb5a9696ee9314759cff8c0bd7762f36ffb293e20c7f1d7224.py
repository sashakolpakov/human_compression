from pathlib import Path
import json,hashlib,shutil
Q=Path(__file__).resolve().parent.parent;T=Q/'principal_stage01';P=Q/'principal_v1';F=Q/'principal_author01'
def pin(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def read(p):return json.loads(p.read_text())
def need(v,m):
    if not v:raise ValueError(m)
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def main():
    need(not P.exists(),'fresh frozen packet');m=read(T/'manifest.json')
    for r in m['exports']:
        z=pin(T/r['path']);need(all(z[k]==r[k]for k in ['bytes','sha256']),'stage unchanged')
    report=read(F/'report.json');need(report['status']=='PASS_L033_COMPLETE_SOURCE_SYNTHESIS'and report['native']['rasters_identical'],'complete author replay')
    shutil.copytree(T,P);(P/'manifest.json').unlink();shutil.copytree(F,P/'author_validation');shutil.copyfile(Path(__file__),P/'freeze.py')
    save(P/'author_execution.json',dict(status='CLEAN_AUTHOR_TERMINAL_PASS',owner='publication_recovery',session_id=39320,command=['/Users/sasha/.venvs/global/bin/python',str(T/'check.py'),'--out',str(F),'--render'],exit_code=0,stdout_report=pin(F/'report.json'),target_censuses=0,stage_manifest=pin(T/'manifest.json'),native_pages_directly_viewed=list(range(1,10)),fresh_native_identity='All9 rebuilt rasters equal directly viewed native03; all50 reading-volume page texts/content streams exact.'))
    deps={r['path']:r for r in read(P/'dependencies.json')}
    for p in [T/'manifest.json',Path(__file__),*sorted(F.rglob('*'))]:
        if p.is_file():deps[str(p)]=pin(p)
    save(P/'dependencies.json',[deps[k]for k in sorted(deps)])
    exports=[pin(p,P)for p in sorted(P.rglob('*'))if p.is_file()]
    save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L033_PRINCIPAL_SYNTHESIS_V1',exports=exports,dependencies=len(deps)))
    hand=dict(status='FROZEN_AUTHOR_HANDOFF_DISTINCT_REVIEW_REQUIRED',author_manifest=pin(P/'manifest.json'),check_command=['/Users/sasha/.venvs/global/bin/python',str(P/'check.py'),'--out',str(Q/'principal_review_fresh_NEW'),'--render'],scope=read(P/'scope.json'),author_report=pin(F/'report.json'),new_censuses=0,public_edits=False)
    save(Q/'principal_handoff01.json',hand);print(json.dumps(hand,indent=2))
if __name__=='__main__':main()
