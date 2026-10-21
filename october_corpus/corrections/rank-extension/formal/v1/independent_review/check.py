#!/usr/bin/env python3
"""Fresh direct compilation of the scoped permutation obstruction."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
PIN='6f18adac317a26aeeec070473c61d4b6f54ee95c55a4976d3a6ddbf823474cae'
CPIN='2e182cee7ea5e9148694c8a43244caeebfa1f4bca6993c4dde5cee19bf83ff70'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--correction',type=Path,required=True);p.add_argument('--lean',type=Path,required=True);p.add_argument('--packages',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 for key in ['packet','correction','lean','packages','out']:setattr(a,key,getattr(a,key).resolve())
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 need(sha(a.packet/'manifest.json')==PIN and sha(a.correction/'manifest.json')==CPIN,'exact formal and written editions')
 for r in json.loads((a.packet/'manifest.json').read_text())['exports']:
  f=a.packet/r['path'];need(f.stat().st_size==r['bytes']and sha(f)==r['sha256'],'exact formal export')
 pins=json.loads((a.packet/'dependency_manifest.json').read_text());libs=[]
 for row in pins['packages']:
  pkg=a.packages/row['name'];rev=subprocess.check_output(['git','-C',str(pkg),'rev-parse','HEAD'],text=True).strip()
  need(rev==row['rev'],'package revision')
  need(subprocess.run(['git','-C',str(pkg),'diff','--quiet','HEAD','--'],capture_output=True).returncode==0,'package source clean')
  lib=pkg/'.lake/build/lib/lean'
  if lib.is_dir():libs.append(str(lib.resolve()))
 version=subprocess.check_output([str(a.lean),'--version'],text=True).strip();need('version 4.32.2,'in version,'exact compiler')
 raw=(a.packet/'RankExtensionObstruction.lean').read_text()
 need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'no proof holes or extra evaluator')
 source=a.out/'RankExtensionObstruction.lean';source.write_text(raw)
 env=dict(os.environ,LEAN_PATH=os.pathsep.join(libs));env.pop('LEAN_SRC_PATH',None)
 run=subprocess.run([str(a.lean),'-o',str(a.out/'RankExtensionObstruction.olean'),str(source)],cwd=a.out,env=env,capture_output=True,text=True,timeout=90)
 output=run.stdout+run.stderr;(a.out/'lean.log').write_text(output);need(run.returncode==0 and 'warning:'not in output,'fresh compilation')
 reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output,re.S)
 names=['delta_involutions','delta_distinct','delta_string','sigma_ne_one','left_cube','right_cube','label_intersection','sigma_mem_left','sigma_mem_right','delta_not_C']
 need([n for n,ax in reports]==['RankExtensionObstruction.'+n for n in names],'all ten declarations')
 need(all(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'}for n,ax in reports),'standard axioms only')
 report=dict(status='PASS_DISTINCT_FRESH_L019_FORMAL',author_manifest_sha256=PIN,written_correction_manifest_sha256=CPIN,source_sha256=sha(source),declarations=10,axiom_reports=[dict(declaration=n,axioms=re.findall(r'[A-Za-z][\w.]*',ax))for n,ax in reports],actual_generated_subgroups=True,kernel_checked_finite_identities=True,author_checker_imported=False,old_input_C_formalized=False,source_hypotheses_formalized=False,full_source_theorem_formalized=False,trusted_cached_upstream_oleans=True,new_source_credit=0,new_question_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
