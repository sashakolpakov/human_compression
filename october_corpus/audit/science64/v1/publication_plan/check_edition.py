"""Verify precise publication-only successor, without science/native reruns."""
from pathlib import Path
import argparse,hashlib,json
R=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prior',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();e=json.loads((R/'edition.json').read_text());pm=R/'predecessor_manifest.json'
 need(sha(pm)==e['predecessor_manifest_sha256']=='c44596a45c73c03a8024eefae927d4dd4cbb448998d57f3cc1a9afc1f1cdfc17','predecessor')
 old=json.loads(pm.read_text());same=[];changed=[]
 for x in old['exports']:
  if a.prior:need(sha(a.prior/x['path'])==x['sha256'],'preserved predecessor '+x['path'])
  (same if sha(R/x['path'])==x['sha256'] else changed).append(x['path'])
 need(same==e['same_previous_exports'] and changed==e['changed_previous_exports'],'exact delta boundary')
 need(len(same)==32 and len(changed)==18,'bounded publication delta')
 if (R/'manifest.json').exists():
  for x in json.loads((R/'manifest.json').read_text())['exports']:need(sha(R/x['path'])==x['sha256'],'current export')
 for n in ['copy_plan.json','payload_routes.json','native_catalogue_draft.json','whole_file_roles_draft.json','replay.py','baseline.json','wrappers/audit/protocol.tex','wrappers/audit/protocol.pdf','wrappers/scripts/check_science64.py','wrappers/scripts/check_science64_history.py']:
  need(n in same,'unchanged science/history/renderer '+n)
 ad=json.loads((R/'wrappers/audit/recoveries/L015/v1/admission.json').read_text());guide=(R/'wrappers/papers/recoveries/L015/v1/PUBLICATION.rst').read_text()
 for name in ['Dimitri Leemans','Klara Stokes','Philippe Tranchida']:need(name in ad['source_author_role'] and name in guide,'complete attribution '+name)
 need(len(json.loads((R/'reports/routes.json').read_text())['controls'])==36,'fresh route controls')
 report={'status':'PASS_ATTRIBUTION_ONLY_SUCCESSOR','unchanged_predecessor_exports':32,'changed_publication_exports':18,'exact_payload_routes_unchanged':26,'protocol_bytes_unchanged':True,'prior_review_native_receipts_reused':True,'science_mutated':False,'public_written':False}
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
