#!/usr/bin/env python3
"""Portable independent C ownership/reader audit. No scientific computation."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
PINS={'topic_C_dag_costs':'d78d618ed35ffb31d260ded85d27627f8db43a435a5fe4cd02822dd510beb718','topic_C_dag_costs_v2':'74cebf42fad7330804bfb95a85bf44eae729e62fb4c311b4ad7c32364e6202d8'}
def need(b,s):
 if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--public-root',type=Path,required=True);a.add_argument('--node',default='node');a.add_argument('--out',type=Path,required=True);o=a.parse_args();need(not o.out.exists() and not o.out.is_symlink(),'fresh output');o.out.mkdir(parents=True)
 here=Path(__file__).resolve().parent;inventories={}
 for folder,h in PINS.items():
  p=o.study_root/folder;need(sha(p/'manifest.json')==h,'frozen '+folder);m=json.loads((p/'manifest.json').read_text());inventories[folder]=m
  for r in m['exports']:
   rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe export path');f=p/rel;need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'export '+folder+'/'+str(rel))
 old=o.study_root/'topic_C_dag_costs';new=o.study_root/'topic_C_dag_costs_v2';delta=json.loads((new/'correction.json').read_text())
 for name in delta['exact_unchanged_exports']:need((old/name).read_bytes()==(new/name).read_bytes(),'unchanged '+name)
 for row in delta['exact_changed_exports']:need(sha(old/row['path'])==row['old_sha256'] and sha(new/row['path'])==row['new_sha256'],'changed pair '+row['path'])
 need(len(delta['exact_changed_exports'])==7 and len(delta['exact_unchanged_exports'])==33,'bounded reader delta')
 need('sixteen Lean declarations' in (new/'README.rst').read_text(),'correct formal count')
 commands=[[sys.executable,'-B','-O',str(here/'independent_check.py'),'--study-root',str(o.study_root),'--out',str(o.out/'arithmetic.json')],[o.node,str(here/'independent_viewer.js'),str(new/'explorer.html'),str(o.out/'viewer.json')]]
 for i,cmd in enumerate(commands):
  r=subprocess.run(cmd,capture_output=True,text=True);(o.out/f'command{i+1}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'fresh independent command '+str(i+1)+' failed: '+(r.stdout+r.stderr)[-3000:])
 d=json.loads((new/'view_data.json').read_text());base=o.public_root/'audit/topic-c/v2/dag/costs';paths={r['path'] for r in d['documents'].values() if r['path']}|{l['path'] for n in d['nodes'] for l in n.get('current_public_locators',[])}
 for p in paths:
  resolved=(base/'../../../../../'/p).resolve();need(resolved==(o.public_root/p).resolve() and resolved.is_file(),'prospective proof route '+p)
 report={'status':'PASS_INDEPENDENT_COSTS_READER_AND_CORRECTION','author_pins':PINS,'independent_arithmetic':json.loads((o.out/'arithmetic.json').read_text()),'independent_viewer':json.loads((o.out/'viewer.json').read_text()),'unchanged_v2_exports':33,'changed_v2_exports':7,'resolved_proof_document_paths':len(paths),'no_primary_redistribution':True,'no_real_browser_layout_claim':True,'new_source_credit':0,'new_question_credit':0}
 (o.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['independent_arithmetic','independent_viewer']}))
if __name__=='__main__':main()
