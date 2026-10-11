#!/usr/bin/env python3
"""Bounded current-v12 check; complete source/Lean/GAP runs are separate."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile

def need(ok,msg):
 if not ok:raise ValueError('V12_PUBLIC_REJECT: '+msg)
def load(root,p):return json.loads((root/p).read_text())
def binding(root,r):
 p=Path(r['path']);need(not p.is_absolute()and'..'not in p.parts,'safe binding');b=(root/p).read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact '+str(p))
def verify(root):
 base='audit/overview/v12/';a=load(root,base+'admission.json');p=load(root,'audit/overview/latest.json')
 need(a['status']=='ROOT_ADMITTED_MATCHED_LISTING_OVERVIEW','distinct root admission required')
 for r in a['artifacts']:binding(root,r)
 need(p['admission']['path']==base+'admission.json'and p['reader']['path']==base+'packet/reader.pdf','current v12 routes')
 for k in ['admission','reader','counts_source','measurement_policy','measurement_policy_reader','measurement_policy_review']:binding(root,p[k])
 need([p[k]for k in ['topics','recovered_originals','active_catalogue_originals','pending_accessible_originals','archived_unavailable_originals','current_whole_factors','current_conditional_factors']]==[19,43,106,63,55,19,43],'unchanged programme/full factors')
 need(p['held_topics']==p['held_sources']==[]and p['software_inclusive_factors_status']=='UNAVAILABLE_UNTIL_BOTH_SIDES_INVENTORIED','restored manuscript factors only')
 need(a['software_inclusive_factors']is None and a['pooled_factor']is None and a['new_source_credit']==a['new_question_credit']==a['new_formal_credit']==0,'unknown scope/new-credit guard')
 readme=(root/'README.rst').read_text();need(base+'packet/reader.pdf'in readme and'Pending code exclusion'not in readme and'Nineteen whole-topic factors and forty-three individual'in readme,'current README routes and scope')
 with tempfile.TemporaryDirectory(prefix='v12-public-')as temp:
  out=Path(temp)/'run';run=subprocess.run([sys.executable,'-B','-O',str(root/base/'packet/check.py'),'--public-root',str(root),'--out',str(out)],capture_output=True,text=True)
  need(run.returncode==0,'portable numerical check failed '+run.stdout+run.stderr);r=load(out,'report.json')
  need(r['exact_fractions']==62 and r['graphs']['actual_svg_bars']==r['graphs']['actual_pdf_bars']==143,'all current values/actual bars')
 return 62,143
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);x=ap.parse_args();print(json.dumps(dict(status='PASS',counts=verify(x.public_root))))
