#!/usr/bin/env python3
"""Fresh complete numerical/plot/TeX replay; no source or scientific rerun."""
from pathlib import Path
import argparse,subprocess,json,hashlib,sys
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent

def need(b,m):
 if not b:raise ValueError('ADDITIONAL_REPLAY_REJECT: '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh replay');a.out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for r in json.loads((HERE/'manifest.json').read_text())['exports']:need((HERE/r['path']).stat().st_size==r['bytes'] and sha(HERE/r['path'])==r['sha256'],'frozen export '+r['path'])
 commands=[[sys.executable,'-B','-O',str(HERE/'compute.py'),'--study-root',str(a.study_root),'--out',str(a.out/'numeric')],[sys.executable,'-B',str(HERE/'build_reader.py'),'--results',str(a.out/'numeric/results.json'),'--out',str(a.out/'reader'),'--xelatex',a.xelatex],[sys.executable,'-B','-O',str(HERE/'check.py'),'--study-root',str(a.study_root),'--out',str(a.out/'checks.json')]]
 for i,cmd in enumerate(commands):
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=240);(a.out/f'command{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'fresh command '+str(i))
 equal=[]
 for folder,names in [('numeric',['results.json','comparisons.csv']),('reader',['measurement.tex','whole_costs.svg','whole_costs.pdf','plot_data.json'])]:
  for name in names:need((a.out/folder/name).read_bytes()==(HERE/name).read_bytes(),'exact regenerated '+name);equal.append(name)
 original=[p.extract_text() or '' for p in PdfReader(HERE/'measurement.pdf').pages];fresh=[p.extract_text() or '' for p in PdfReader(a.out/'reader/measurement.pdf').pages];need(fresh==original,'all reader page text exact')
 report=dict(status='PASS',exact_regenerated_files=equal,reader_pages_equal=len(fresh),checks=json.loads((a.out/'checks.json').read_text()),scientific_programs_executed=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
