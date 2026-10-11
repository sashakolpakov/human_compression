#!/usr/bin/env python3
"""Fresh direct compilation of the scoped permutation obstruction."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
PIN='abdb25d913624194ec675dd789a82b5fe7e6aa6ac15e2b2f3601b5820866c060'
CPIN='553e01b6f2d9d9675b6b855339ed5d1985be3bce7451baa075fddb3ca9b06cb2'
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
 raw=(a.packet/'TransitiveExtensionObstruction.lean').read_text()
 need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'no proof holes or extra evaluator')
 source=a.out/'TransitiveExtensionObstruction.lean';source.write_text(raw)
 env=dict(os.environ,LEAN_PATH=os.pathsep.join(libs));env.pop('LEAN_SRC_PATH',None)
 run=subprocess.run([str(a.lean),'-o',str(a.out/'TransitiveExtensionObstruction.olean'),str(source)],cwd=a.out,env=env,capture_output=True,text=True,timeout=90)
 output=run.stdout+run.stderr;(a.out/'lean.log').write_text(output);need(run.returncode==0 and 'warning:'not in output,'fresh compilation')
 reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output,re.S)
 names=['delta_involutions', 'delta_distinct', 'delta_string', 'beta_ne_one', 'beta_ne_delta', 'left_cube', 'short_word_value', 'short_word_conjugate', 'beta_word', 'label_intersection', 'beta_mem_left', 'short_word_mem_right', 'beta_mem_right', 'common_subgroup_bound', 'beta_not_common', 'delta_not_C']
 need([n for n,ax in reports]==['TransitiveExtensionObstruction.'+n for n in names],'all sixteen declarations')
 need(all(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'}for n,ax in reports),'standard axioms only')
 report=dict(status='PASS_DISTINCT_FRESH_L019_TRANSITIVE_FORMAL',author_manifest_sha256=PIN,written_correction_manifest_sha256=CPIN,source_sha256=sha(source),declarations=16,axiom_reports=[dict(declaration=n,axioms=re.findall(r'[A-Za-z][\w.]*',ax))for n,ax in reports],actual_generated_subgroups=True,kernel_checked_finite_identities=True,author_checker_imported=False,old_input_C_formalized=False,source_hypotheses_formalized=False,full_source_theorem_formalized=False,trusted_cached_upstream_oleans=True,new_source_credit=0,new_question_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
