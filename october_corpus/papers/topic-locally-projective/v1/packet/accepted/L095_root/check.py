#!/usr/bin/env python3
"""Distinct root presentation and prime-subgroup checks; GAP still trusted."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,os,signal,time
PIN='b26d7d1c7808bf87564b636ae7a0255f07f5542f9561a68c5b9e4fc7a9514627'
def need(b,s):
 if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 need(sha(a.packet/'manifest.json')==PIN,'frozen author')
 m=json.loads((a.packet/'manifest.json').read_text())
 for r in m['exports']:
  rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path');f=a.packet/rel;need(sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],'exact export')
 (a.out/'programs').mkdir();shutil.copyfile(a.packet/'programs/ambient_marking.g',a.out/'programs/ambient_marking.g');shutil.copyfile(Path(__file__).with_name('distinct.g'),a.out/'distinct.g')
 t=time.monotonic();c=subprocess.Popen([a.gap,'-q','-b','-A','-r','-K','512m','distinct.g'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:stdout,stderr=c.communicate(timeout=45)
 except subprocess.TimeoutExpired:
  os.killpg(c.pid,signal.SIGKILL);stdout,stderr=c.communicate();raise ValueError('bounded root timeout')
 (a.out/'stdout').write_text(stdout);(a.out/'stderr').write_text(stderr)
 need(c.returncode==0 and 'L095_DISTINCT_PASS' in stdout and not any(x in stdout+stderr for x in ['Error,','Syntax error','Syntax warning']),'root GAP checks')
 data=json.loads((a.out/'distinct.json').read_text());need(data[:4]==[20,175560,171,600415200],'upper bound')
 report=dict(status='PASS_DISTINCT_ROOT_CHECKS',author_exports=len(m['exports']),data=data,seconds=time.monotonic()-t,ACE_loaded_in_distinct_run=False,cyclic_rewrite='Integer table rather than author abelian vectors; complete relator loops checked by separate root code.',prime_subgroups='Enumerated inside every Sylow subgroup, identified up to ambient conjugacy; different from author element-conjugacy-class enumeration.',trust='Both routes retain GAP algorithms and the accepted ambient marking. This is not a proof of GAP correctness or full Lean formalization.',source_credit=0,question_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
