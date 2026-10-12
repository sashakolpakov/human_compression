"""Restore every logical dependency using public files only; no old census run."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(x,m):
    if not x:raise ValueError(m)
def bound(p,r):need(p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'exact public/logical bytes '+str(p))
def safe(s):
    p=PurePosixPath(s);need(not p.is_absolute() and '..' not in p.parts,'safe path');return p
def main(a):
    need(not a.out.exists(),'fresh replay directory');a.out.mkdir(parents=True);plan=load(HERE/'copy_plan.json');study=a.out/'logical_study';study.mkdir()
    for r in plan['files']:
        src=a.repo/safe(r['public_path']);bound(src,r);dst=study/safe(r['study_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    for packet in plan['packets']:
        p=study/safe(packet['study_manifest']);m=load(p);need(len(m['exports'])==packet['exports'],'full packet')
        for r in m['exports']:bound(p.parent/safe(r['path']),r)
    for r in plan['public_dependencies']:bound(a.repo/r['path'],r)
    cmd=[sys.executable,'-B','-O',str(study/'corpus106_L096_recovery/check.py'),'--study-root',str(study),'--public-root',str(a.repo),'--out',str(a.out/'author_replay')]
    if a.render:cmd.append('--render')
    if a.new_programs:cmd.append('--programs')
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=240);(a.out/'author_stdout.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'current bounded author replay')
    rep=load(a.out/'author_replay/report.json');need(rep['exports_verified']==42 and rep['source_dispositions']==73 and rep['positive_named_occurrences']==232 and rep['direct_profile_confirmations']==229 and rep['unverified_historical_ordinals']==3,'complete corrected contract')
    need(rep['whole_file_occurrences']==881 and rep['unique_whole_contents']==824 and len(rep['controls'])==20,'whole roles/controls')
    need(rep['private_primary_bindings_if_supplied']==0 and not rep['old_census_or_shadow_rerun'] and not rep['new_formal_run'],'public-only scope')
    if a.render:need([r['pages'] for r in rep['render']]==[11,9,7],'all27 native pages')
    review=load(study/'corpus106_L096_complete_root_review/review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['source_ids']==['L096'],'actual root adoption')
    report=dict(status='PASS_PUBLIC_ONLY_WHOLE_DEPENDENCY_RECONSTRUCTION',logical_files=len(plan['files']),complete_packets=len(plan['packets']),author=rep,whole_native_pages=[11,9,7],additional_old_common_pages=6,new_bounded_discriminators_repeated=a.new_programs,old_census_shadow_or_Lean_repeated=False,primary_assets_restored=False,root_science_status=review['status'])
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--new-programs',action='store_true');main(p.parse_args())
