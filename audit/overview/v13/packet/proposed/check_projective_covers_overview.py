#!/usr/bin/env python3
"""Public v13 whole-manuscript guard, separate from scientific replay."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile

def need(ok,msg):
 if not ok:raise ValueError('V13_PUBLIC_REJECT: '+msg)
def load(root,path):return json.loads((root/path).read_text())
def binding(root,row):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'safe binding');b=(root/p).read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'exact '+str(p))
def verify(root):
 base='audit/overview/v13/';a=load(root,base+'admission.json');p=load(root,'audit/overview/latest.json')
 need(a['status']=='ROOT_ADMITTED_EXPANDED_PROJECTIVE_MIXES_OVERVIEW','distinct root overview admission')
 for row in a['artifacts']:binding(root,row)
 for k in ['admission','reader','counts_source','measurement_policy','measurement_policy_reader','measurement_policy_review']:binding(root,p[k])
 need(p['admission']['path']==base+'admission.json'and p['reader']['path']==base+'packet/reader.pdf','current v13 routes')
 need([p[k]for k in ['topics','recovered_originals','active_catalogue_originals','pending_accessible_originals','archived_unavailable_originals','current_whole_factors','current_conditional_factors']]==[19,46,106,60,55,19,46],'whole19/46 programme')
 need(p['held_topics']==p['held_sources']==[]and p['software_inclusive_factors_status']=='UNAVAILABLE_UNTIL_BOTH_SIDES_INVENTORIED','manuscript-only comparisons')
 need(a['software_inclusive_factors']is None and a['pooled_factor']is None,'no invented software/pooled factor')
 text=(root/'README.rst').read_text();need(base+'packet/reader.pdf'in text and'forty-six individual'in text and'46 accessible originals'in text,'root current README scope')
 with tempfile.TemporaryDirectory(prefix='overview-v13-')as temp:
  out=Path(temp)/'run';run=subprocess.run([sys.executable,'-B','-O',str(root/base/'packet/check.py'),'--public-root',str(root),'--out',str(out)],capture_output=True,text=True);need(run.returncode==0,'portable overview replay '+run.stdout+run.stderr);r=load(out,'report.json');need(r['factors']==65 and r['graphs']['SVG_bars']==r['graphs']['PDF_bars']==149 and r['root_programme_bound'],'all exact comparisons/bars/programme')
 return 65,149
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);a=ap.parse_args();print(json.dumps(dict(status='PASS',counts=verify(a.public_root))))
