import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json
P=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def exact(p,r):
 b=p.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact file '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists()and a.out.parent.exists(),'fresh output')
 m=json.loads((P/'manifest.json').read_text());need(m['status']=='ACCEPTED_L100_RANK_TWO_COMPONENT_V2','review status')
 for r in m['exports']:
  q=Path(r['path']);need(not q.is_absolute()and '..'not in q.parts,'safe export');exact(P/q,r)
 deps=json.loads((P/'dependencies.json').read_text())
 for r in deps:exact(Path(r['path']),r)
 r=json.loads((P/'final02/report.json').read_text());need(r['status']=='PASS_FINAL_L100_RANK_TWO_V2_REVIEW_CHECK'and r['literal_candidates']==60 and r['literal_neighbour_pairs']==3098 and r['literal_witnesses']==24 and r['local2T_correction_explicit'],'final scope')
 r=json.loads((P/'literal02.json').read_text());need(r['status']=='PASS_INDEPENDENT_LITERAL_L100_CANDIDATE_CHECKS'and r['classes']==7,'literal independent result')
 for d in ['export01','literal02_receipt','final02_receipt']:
  r=json.loads((P/d/'receipt.json').read_text());need(r['status']=='TERMINAL_PASS'and r['returncode']==0,'terminal receipt '+d)
 a.out.mkdir();report={'status':'PASS_L100_DISTINCT_REVIEW_BINDINGS','exports':len(m['exports']),'dependencies':len(deps),'new_group_or_geometry_enumerations':0};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
