#!/usr/bin/env python3
"""Portable distinct review: no author parser or mathematical imports."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys,copy
P=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def compare(a,b):
 need(len(a['rows'])==len(b['rows'])==6,'rank boundary')
 for x,y in zip(a['rows'],b['rows']):
  need((x['rank'],x['count'],x['connected'],x['self_dual'])==(y['rank'],y['classes'],y['connected'],y['self_dual']),'census row')
  need([{k:z[k] for k in ['marking','schlafli','self_dual']} for z in x['representatives']]==y['representatives'],'full representative list')
 need(a['group_order']==b['group_order']==120 and a['involutions']==b['involutions']==31,'group size')
def main():
 q=argparse.ArgumentParser();q.add_argument('--author',type=Path,required=True);q.add_argument('--out',type=Path,required=True);q=q.parse_args();q.out.mkdir(parents=True,exist_ok=False)
 need(H(q.author/'manifest.json')=='ac22b0f717ad32ac49aa990d514c224e4ac84994338b42a4bb5bcf2c0db9cbd3','author pin')
 m=json.loads((q.author/'manifest.json').read_text())
 for r in m['exports']:
  p=q.author/r['path'];need(p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'author export '+r['path'])
 if (P/'manifest.json').exists():
  for r in json.loads((P/'manifest.json').read_text())['exports']:
   p=P/r['path'];need(p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'review export '+r['path'])
 run=subprocess.run([sys.executable,str(P/'oracle.py'),'--out',str(q.out/'oracle.json')],capture_output=True,text=True,check=True)
 (q.out/'oracle.stdout').write_text(run.stdout);(q.out/'oracle.stderr').write_text(run.stderr)
 a=json.loads((q.author/'census/report.json').read_text());b=json.loads((q.out/'oracle.json').read_text());compare(a,b)
 need(b==json.loads((P/'oracle_report.json').read_text()),'exact independent output')
 controls=[]
 for name,mutate in [('omit_rank4',lambda x:x['rows'][3].update(count=0)),('omit_representative',lambda x:x['rows'][2]['representatives'].pop()),('false_self_duality',lambda x:x['rows'][3].update(self_dual=1)),('wrong_group_order',lambda x:x.update(group_order=60)),('truncated_rank_range',lambda x:x['rows'].pop())]:
  bad=copy.deepcopy(a);mutate(bad)
  try:compare(bad,b)
  except ValueError:controls.append(name)
  else:raise ValueError('mutation survived '+name)
 out={'status':'PASS_BOUNDED_DISTINCT_REVIEW','author_exports':len(m['exports']),'rank_rows':6,'exact_class_representatives':11,'independent_group_model':True,'independent_prefixes':b['independent_prefixes'],'semantic_controls':b['controls'],'comparison_controls':controls,'bounded_dihedral_cases':16,'whole_original_credit':0,'new_question_credit':0,'new_formal_credit':0}
 (q.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
