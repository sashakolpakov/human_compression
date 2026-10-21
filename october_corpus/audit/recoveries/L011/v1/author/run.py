#!/usr/bin/env python3
"""Whole finite certificate runner. GAP performs the exhaustive group operations."""
import argparse,ast,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
 if not ok: raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');a=ap.parse_args()
 out=Path(a.out).resolve();need(not out.exists(),'fresh output required');out.mkdir(parents=True)
 source='OUT:='+json.dumps(str(out))+';;\nRead("programs/run_certificate.g");;\n'
 driver=out/'driver.g';driver.write_text(source)
 p=subprocess.run([a.gap,'-q','-b',str(driver)],cwd=ROOT,text=True,capture_output=True)
 (out/'stdout.txt').write_text(p.stdout);(out/'stderr.txt').write_text(p.stderr)
 need(p.returncode==0 and 'L011_CERTIFICATE_PASS' in p.stdout and not p.stderr.strip(),'GAP replay failed')
 # GAP wraps long print output with backslash-newline; remove only that formatting.
 stdout=p.stdout.replace('\\\n','').replace('\r','')
 rows=[]
 fresh_orders=[]
 for line in stdout.splitlines():
  if line.startswith('FRESH_ORDER|'):
   _,tag,value,qualification=line.split('|');fresh_orders.append(dict(tag=tag,order=int(value),qualification=qualification))
  if not line.startswith('RECORD|'):continue
  _,name,order,nodes,classes,invols,witnesses,ms=line.split('|')
  rows.append(dict(group=name,order=int(order),prefix_counts=ast.literal_eval(nodes),involution_classes=int(classes),involutions=int(invols),witnesses=int(witnesses),runtime_ms=int(ms)))
 need([r['group'] for r in rows]==['A5_control','A6','A7','M11','M22','M23','McL','U4_3','U5_2'],'complete case list')
 report={'status':'PASS','role':'REQUIRED_FINITE_PROOF_CERTIFICATE_FOR_EXACT_EIGHT_EXCEPTIONAL_GROUPS','cases':rows,'fresh_permutation_orders':fresh_orders,'stabilizer_chain_option':'random=1000, guaranteed verification; internal random construction is not excluded','search':'complete connected independent string prefixes modulo inner conjugation, with full IP tests','retained_identity':'Alternating/Mathieu/primitive named group library identities; unitary images verified by isometry/order and classical order formulas','no_full_formalization':True,'no_new_original_credit':True,'whole_program_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'programs').glob('*.g')) if p.name in ['string_search.g','unitary_models.g','run_certificate.g']}}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','groups':8,'positive_control':rows[0]['witnesses'],'finite_prefixes':sum(sum(r['prefix_counts']) for r in rows[1:])}))
if __name__=='__main__':main()
