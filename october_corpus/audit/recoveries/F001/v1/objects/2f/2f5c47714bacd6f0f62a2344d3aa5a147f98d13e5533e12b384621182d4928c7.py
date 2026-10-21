from pathlib import Path
import argparse,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent

def need(v,m):
 if not v:raise ValueError(m)
def bind(root,r):
 b=(root/r['path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'binding '+r['path'])
def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();x.out.mkdir(exist_ok=False,parents=True)
 m=json.loads((P/'manifest.json').read_text())
 for r in m['exports']:bind(P,r)
 b=json.loads((P/'bindings.json').read_text())
 for r in b['bindings']:bind(x.study_root,r)
 author=x.study_root/'corpus106_F001_rank_bound_v1'
 for r in b['author_exports']:bind(author,r)
 job=x.out/'independent.json';subprocess.run([sys.executable,'-B','-O',str(P/'independent_check.py'),'--author',str(author),'--out',str(job)],check=True)
 need(json.loads(job.read_text())==json.loads((P/'independent_report.json').read_text()),'independent result changed')
 report={'status':'PASS','review_exports':len(m['exports']),'author_exports':len(b['author_exports']),'source_and_author_pins':len(b['bindings']),'independent_IP_pairs':4096,'independent_negative_controls':3,'whole_original_credit':0};(x.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
