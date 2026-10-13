import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def need(ok,m):
 if not ok: raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p=Path(__file__).resolve().parent
 need(__debug__,'optimized Python')
 for x in json.loads((p/'manifest.json').read_text())['exports']:
  b=(p/x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'export '+x['path'])
 for x in json.loads((p/'bindings.json').read_text()):
  b=Path(x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'binding '+x['path'])
 r=json.loads((p/'assessment.json').read_text());need(r['accepted'] and len(r['cases'])==3 and r['tuple_total']==9091 and r['subset_pair_total']==4706944,'exact assessment')
 subprocess.run([sys.executable,str(p/'assess.py'),'--study',str(a.study),'--out',str(a.out)],check=True)
 fresh=json.loads((a.out/'assessment.json').read_text())
 for k in ['status','accepted','cases','negative_controls','tuple_total','subset_pair_total','whole_original_credit','new_question_credit','new_formal_credit','finite_executions_repeated']:
  need(fresh[k]==r[k],'fresh semantic result '+k)
 print('PASS_DISTINCT_F006_WARNING_ASSESSMENT')
if __name__=='__main__':main()
