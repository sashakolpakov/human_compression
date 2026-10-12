#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def need(x,s):
 if not x:raise RuntimeError(s)
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();base=Path(__file__).resolve().parent
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 m=json.loads((base/'manifest.json').read_text())
 for x in m['exports']:
  f=base/x['path'];need(f.stat().st_size==x['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256'],'review binding '+x['path'])
 subprocess.run([sys.executable,'-B','-O',str(base/'independent_delta.py'),'--author',str(a.author),'--out',str(a.out/'independent.json')],check=True)
 subprocess.run([sys.executable,'-B','-O',str(a.author/'migration_check.py'),'--out',str(a.out/'author_migration.json')],check=True,cwd=a.author)
 if a.render:subprocess.run([sys.executable,'-B','-O',str(a.author/'check.py'),'--out',str(a.out/'render'),'--render'],check=True,cwd=a.author)
 (a.out/'report.json').write_text(json.dumps({'status':'PASS','review_exports':len(m['exports']),'bounded_migration_only':True,'unchanged_program_formal_repeated':False,'fresh_render':a.render},indent=2)+'\n');print('Bounded migration review PASS')
if __name__=='__main__':main()
