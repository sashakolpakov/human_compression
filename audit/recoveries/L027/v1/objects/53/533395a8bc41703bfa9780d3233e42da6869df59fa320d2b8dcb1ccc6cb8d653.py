"""Verify the exact reviewed edition and optionally the independent control."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,os,subprocess
P=Path(__file__).resolve().parent
def need(ok,why):
 if not ok:raise ValueError(why)
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--replay-independent',action='store_true');a=ap.parse_args()
 roots={'study':a.study.resolve(),'repo':a.repo.resolve()};out=a.out.resolve();need(not out.exists(),'Fresh output')
 manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for x in manifest['exports']:need(pin(P/x['path'])=={k:x[k]for k in ['bytes','sha256']},'Export '+x['path'])
 for x in deps:need(pin(roots[x['namespace']]/x['path'])=={k:x[k]for k in ['bytes','sha256']},'Dependency '+x['path'])
 review=json.loads((P/'review.json').read_text());need(review['status']=='ACCEPTED_L027_ODD_THREE_V2','Decision')
 need(review['author_manifest']['sha256']=='cf9d3b4e82f414e9b2eed5ed670799ad6a70c4402db2a7f24e66d62d90437357','Author edition')
 old=roots['study']/'corpus106_L027_odd_three_v1';new=roots['study']/'corpus106_L027_odd_three_v2'
 text=(old/'odd_three.tex').read_text()
 for row in json.loads((new/'edition_delta.json').read_text())['changes']:
  need(text.count(row['before'])==1,'Unique literal delta');text=text.replace(row['before'],row['after'])
 need(text==(new/'odd_three.tex').read_text(),'Exactly two editorial changes')
 for name in ['finite.g','literal.py','check.py','finite_expected.json','literal_expected.json','scope.json','source_map.json']:
  need((old/name).read_bytes()==(new/name).read_bytes(),'Unchanged interface '+name)
 fresh=json.loads((P/'fresh_report.json').read_text());native=json.loads((P/'native_report.json').read_text())
 need(fresh['status']=='PASS_L027_ODD_THREE_CONTROLS' and fresh['actual_subset_pairs']==11584,'Complete science replay')
 need(native['status']=='PASS_EXACT_L027_ODD_THREE_V2_DELTA_AND_NATIVE' and native['native_pages']==5 and native['native_text_identical'],'Final native')
 independent=json.loads((P/'independent_report.json').read_text());need(independent['status']=='PASS_INDEPENDENT_L027_LITERAL_MATRIX_GROUPS' and independent['subset_pairs']==1152,'Independent matrices')
 out.mkdir(parents=True);replay=None
 if a.replay_independent:
  env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
  cmd=[sys.executable,'-B',str(P/'independent.py'),'--out',str(out/'independent.json')]
  try:r=subprocess.run(cmd,env=env,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:
   (out/'independent.stdout').write_bytes(e.stdout or b'');(out/'independent.stderr').write_bytes(e.stderr or b'');raise
  (out/'independent.stdout').write_bytes(r.stdout);(out/'independent.stderr').write_bytes(r.stderr)
  need(r.returncode==0 and not r.stderr,'Clean independent execution');need(json.loads((out/'independent.json').read_text())==independent,'Exact independent output')
  replay=dict(command=cmd,returncode=r.returncode,report=pin(out/'independent.json'))
 report=dict(status='PASS_L027_ODD_THREE_DISTINCT_REVIEW_CLOSURE',exports=len(manifest['exports']),dependencies=len(deps),independent_replay=replay,mathematical_proof_verified_by_program=False,whole_original_credit=0)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
