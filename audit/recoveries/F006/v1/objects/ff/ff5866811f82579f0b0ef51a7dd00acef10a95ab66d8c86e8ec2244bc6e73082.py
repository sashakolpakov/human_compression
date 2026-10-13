#!/usr/bin/env python3
"""Distinct bounded binding/oracle replay, with optional complete author replay."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess
H=Path(__file__).resolve().parent
PIN='e04647d6c40e18d93b2d944d57348acfa6437029560365278b58a36a08e0cdb9'
EXPECTED=[['S2xS3',5,3,4,16,20,84,84,0,0,0],['S2xS4',6,4,12,48,68,148,148,0,0,0],['S3xS3',6,4,1,4,5,8,8,0,0,0],['S2xS5',7,5,4,16,20,28,28,0,0,0],['S3xS4',7,5,6,24,34,34,34,0,0,0],['S2xS6',8,6,8,32,40,56,56,0,0,0],['S3xS5',8,6,2,8,10,8,8,0,0,0],['S4xS4',8,6,9,36,57,30,30,0,0,0],['T6_9',6,4,1,4,5,8,8,2,0,0],['T6_11',6,4,12,48,68,148,148,152,0,0]]
def need(b,s):
 if not b:raise ValueError('L047_DISTINCT_REVIEW: '+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def verify_counts(r,s):
 need(r['rows']==EXPECTED,'ten exact rows and all columns')
 need(r['normalized_markings']==59 and r['transitive_completions']==154 and r['independent_completions']==0 and r['positive_control_completions']==6,'exact totals, including independent column')
 need(s['computational_cases']==10 and s['normalized_markings']==59 and s['transitive_completions']==154 and s['independent_completions']==0,'bounded scope table')
 need(not s['whole_L047_proved_here']and not s['reduction_to_ten_actions_proved_here']and not s['lean_formalized'],'bounded scope only')
 need(s['new_original_credit']==s['new_question_credit']==s['new_formal_credit']==0,'no new credit')
 need(s['required_programs']==['search.g','run.g']and s['operational_runner']=='check.py'and len(s['retained_external_trust'])==2,'complete required program/trust boundary')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gap',default='gap');ap.add_argument('--full-author-replay',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for e in load(H/'manifest.json')['exports']:need((H/e['path']).stat().st_size==e['bytes']and sha(H/e['path'])==e['sha256'],'review export '+e['path'])
 need(sha(a.author/'manifest.json')==PIN,'exact author freeze');man=load(a.author/'manifest.json');need(len(man['exports'])==12,'twelve author exports')
 for e in man['exports']:need((a.author/e['path']).stat().st_size==e['bytes']and sha(a.author/e['path'])==e['sha256'],'author export '+e['path'])
 r=load(H/'copied_replay/report.json');s=load(a.author/'scope.json');verify_counts(r,s)
 need(r==load(a.author/'author_report.json'),'fresh copy equals author report')
 for name,h in r['files'].items():need(sha(a.author/name)==h,'actual replay code pin')
 done=[]
 changes=[('omitted normalized action',lambda r,s:r['rows'].pop()),('independent completion hidden behind zero solutions',lambda r,s:r['rows'][-1].__setitem__(9,1)),('false positive control',lambda r,s:r.update(positive_control_completions=0)),('raw count called normalized',lambda r,s:r.update(normalized_markings=456)),('whole source overclaim',lambda r,s:s.update(whole_L047_proved_here=True)),('reduction overclaim',lambda r,s:s.update(reduction_to_ten_actions_proved_here=True)),('formal overclaim',lambda r,s:s.update(lean_formalized=True)),('new original credit',lambda r,s:s.update(new_original_credit=1)),('required program omitted',lambda r,s:s['required_programs'].pop()),('catalogue trust hidden',lambda r,s:s['retained_external_trust'].pop())]
 for name,f in changes:
  rr,ss=copy.deepcopy(r),copy.deepcopy(s);f(rr,ss)
  try:verify_counts(rr,ss)
  except ValueError:done.append(name)
  else:raise ValueError('negative control survived '+name)
 proc=subprocess.run([a.gap,'-q','-b',str(H/'independent_oracle.g')],text=True,capture_output=True)
 (a.out/'oracle.stdout.log').write_text(proc.stdout);(a.out/'oracle.stderr.log').write_text(proc.stderr)
 need(proc.returncode==0 and not proc.stderr.strip()and 'Error'not in proc.stdout and proc.stdout.count('PASS_L047_INDEPENDENT_ORACLES')==1,'independent GAP oracle pass')
 rows=[line.strip()for line in proc.stdout.splitlines()if line.startswith('ORACLE_')]
 need(rows==['ORACLE_MARKINGS|S2xS3|24|4|12|[ 4 ]','ORACLE_MARKINGS|S3xS3|72|1|72|[ 4 ]','ORACLE_MARKINGS|T6_9|72|1|72|[ 4 ]','ORACLE_MARKINGS|T6_11|288|12|48|[ 4 ]','ORACLE_NEIGHBORS|12|36|6|196|52'],'independent literal oracle summaries')
 full=None
 if a.full_author_replay:
  cp=a.out/'author_copy';cp.mkdir()
  for e in man['exports']:shutil.copyfile(a.author/e['path'],cp/e['path'])
  shutil.copyfile(a.author/'manifest.json',cp/'manifest.json')
  import sys
  p=subprocess.run([sys.executable,'-B','-O',str(cp/'check.py'),'--out',str(a.out/'full_replay'),'--gap',a.gap],text=True,capture_output=True)
  need(p.returncode==0,'fresh author replay '+p.stdout+p.stderr);full=load(a.out/'full_replay/report.json');verify_counts(full,s)
 report=dict(status='PASS_BOUNDED_INDEPENDENT_REVIEW',author_exports=12,case_count=10,normalized_markings=59,transitive_completions=154,independent_completions=0,positive_control_completions=6,independent_raw_markings=[24,72,72,288],independent_normalizer_orbits=[4,1,1,12],independent_literal_neighbor_pairs=36,pruned_positive_pairs=6,distance_positions_checked=196,equality_positions_retained=52,semantic_negative_controls=done,fresh_full_author_replay=full is not None,bound_prior_fresh_replay_executor='enumeration_review',whole_L047_accepted=False,reduction_accepted=False,formal_accepted=False,new_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
