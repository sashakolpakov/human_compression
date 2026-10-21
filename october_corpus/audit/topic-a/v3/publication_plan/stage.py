#!/usr/bin/env python3
"""Copy only mapped accepted exports into a fresh private/public-shaped stage."""
from pathlib import Path
import argparse,json,hashlib,shutil
H=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(study,out):
 need(not out.exists(),'fresh stage required');out.mkdir(parents=True);m=json.loads((H/'assembly_map.json').read_text())
 for r in m['files']:
  b=(study/r['study_path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'exact accepted file '+r['study_path']);target=out/r['public_path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 for src,dst in [('PUBLICATION.rst','papers/topic-a/v3/PUBLICATION.rst'),('audit_README.rst','audit/topic-a/v3/README.rst'),('catalogue_rows.json','audit/topic-a/v3/proposed_catalogue_rows.json')]:
  target=out/dst;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((H/src).read_bytes())
 report=dict(status='PASS_EXACT_PRIVATE_STAGE',accepted_files=len(m['files']),packets=len(m['packets']),embedded_packets_reused=len(m['embedded_packet_aliases']),primary_assets_copied=False,current_pointers_changed=False,admission_created=False)
 (out/'stage_report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();print(json.dumps(run(a.study_root,a.out)))
