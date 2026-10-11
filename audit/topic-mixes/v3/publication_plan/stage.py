#!/usr/bin/env python3
"""Stage only exact new exports and existing public references, never public edits."""
from pathlib import Path
import argparse,hashlib,json
R=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def exact(root,row,key):
 p=Path(row[key]);need(not p.is_absolute()and'..'not in p.parts,'safe path');b=(root/p).read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'exact '+str(p));return b
def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',required=True,type=Path);a.add_argument('--public-root',required=True,type=Path);a.add_argument('--out',required=True,type=Path);x=a.parse_args();need(not x.out.exists(),'fresh private stage required');x.out.mkdir(parents=True);m=load(R/'assembly_map.json')
 for row in m['new_copies']:
  b=exact(x.study_root,row,'study_path');p=x.out/row['public_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for row in m['existing_payload_references']:
  b=exact(x.public_root,row,'path');p=x.out/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for src,dst in [('PUBLICATION.rst','papers/topic-mixes/v3/PUBLICATION.rst'),('audit_README.rst','audit/topic-mixes/v3/README.rst'),('catalogue_rows.json','audit/topic-mixes/v3/proposed_catalogue_rows.json')]:
  p=x.out/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/src).read_bytes())
 report={'status':'PASS_PRIVATE_STAGE_ONLY','new_exact_exports':len(m['new_copies']),'existing_files_reused_at_original_paths':len(m['existing_payload_references']),'existing_public_files_would_be_recopied':False,'primary_assets_copied':False,'current_pointers_written':False,'admission_written':False};(x.out/'stage_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
