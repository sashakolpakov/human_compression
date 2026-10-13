"""Independent operational replay in a repository containing public routes only."""
from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression';A=S/'reboot_20261013/N012_publication_work';T=A/'stage01'
def need(v,s):
 if not v:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 mini=W/'mini_repo';mini.mkdir(exist_ok=False)
 tp=T/'audit/recoveries/N012/v1/transport.json';need(sha(tp)=='0bddf32d1440ea9e74ae0b9fcecd3fc8ca60ba47300d999236b6f41c1490be94','transport pin')
 raw=tp.read_bytes();tr=json.loads(raw);unique={}
 for row in tr['files']:
  if 'public_path' not in row:continue
  rel=Path(row['public_path']);need(not rel.is_absolute() and '..'not in rel.parts,'path');key=str(rel)
  if key in unique:need(unique[key]==(row['stored_bytes'],row['stored_sha256']),'conflicting public route');continue
  unique[key]=(row['stored_bytes'],row['stored_sha256']);src=(R if row['transport']=='EXISTING_PUBLIC' else T)/rel
  need(src.stat().st_size==row['stored_bytes']and sha(src)==row['stored_sha256'],'stored input');dst=mini/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 dest=mini/tp.relative_to(T);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 checker=W/'check_restored.py';shutil.copyfile(S/'reboot_20261013/N012_portable_check.py',checker)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
 def run(name,opt=False,expected=None):
  command=[sys.executable]+(['-O']if opt else [])+[str(checker),'--repo',str(mini),'--expected-transport',expected or sha(dest),'--out',str(W/name)]
  p=subprocess.run(command,cwd=mini,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=360)
  (W/(name+'.stdout')).write_text(p.stdout);(W/(name+'.stderr')).write_text(p.stderr);return p
 p=run('replay01');need(p.returncode==0 and not p.stderr.strip(),'fresh public-only replay')
 fresh=json.loads((W/'replay01/report.json').read_text());prior=json.loads((A/'portable01/report.json').read_text());need(fresh==prior,'all author/public replay fields exactly agree')
 controls=[]
 for name,change in [
  ('missing_review_packet',lambda t:t.update(packets=[x for x in t['packets']if x['path']!='corpus106_N012_principal_root_review/manifest.json'])),
  ('mathematical_file_omitted',lambda t:next(x for x in t['files']if x['path']=='corpus106_N012_integral_v1/integral_groups.tex').update(transport='PRIVATE_PRIMARY_SOURCE_HASH_ONLY')),
  ('damaged_stored_digest',lambda t:next(x for x in t['files']if x.get('public_path','').endswith('/classification/source_recovery.tex')).update(stored_sha256='0'*64))]:
  trial=copy.deepcopy(tr)
  change(trial)
  dest.write_text(json.dumps(trial,indent=2)+'\n');p=run('negative_'+name);need(p.returncode!=0 and 'ValueError:'in p.stderr,'negative control accepted '+name);controls.append(name)
 dest.write_bytes(raw);p=run('negative_optimized',opt=True);need(p.returncode!=0 and 'Validation does not support optimized Python'in p.stderr,'optimized Python accepted');controls.append('optimized_python')
 need(sha(tp)==sha(dest),'frozen transport preserved')
 report=dict(status='PASS_DISTINCT_PUBLIC_ONLY_N012_OPERATIONAL_REVIEW',transport_sha256=sha(tp),checker_sha256=sha(checker),mini_repository_payloads=len(unique),full_replay_matches_author_report=True,negative_controls=controls,prior_role='Authored only the integral component; this review concerns transport and execution, not mathematical self-acceptance. Independently reviewed the separate quotient completion earlier.',mathematical_reapproval=False,private_runtime_fallback=False,public_writes=False,whole_original_credit=0)
 (W/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
