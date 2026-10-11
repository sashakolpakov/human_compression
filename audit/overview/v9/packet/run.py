#!/usr/bin/env python3
"""Rebuild from exported input copies, check actual graphs, compare all reader text."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
from pypdf import PdfReader
H=Path(__file__).resolve().parent
EXACT=['results.json','topics.csv','applications.csv','plot_data.json','whole_topics.svg','whole_topics.pdf','conditional_1.svg','conditional_1.pdf','conditional_2.svg','conditional_2.pdf','summary.tex','build_report.json']
def need(x,m):
 if not x:raise ValueError('OVERVIEW42_REPLAY: '+m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--public-root',type=Path);p.add_argument('--xelatex',default='xelatex');a=p.parse_args();need(not a.out.exists()and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 command=[sys.executable,'-B','-O',str(H/'build.py'),'--out',str(a.out/'build'),'--render','--xelatex',a.xelatex]
 if a.public_root:command+=['--public-root',str(a.public_root)]
 q=subprocess.run(command,capture_output=True);(a.out/'build.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'fresh build')
 command=[sys.executable,'-B','-O',str(H/'check.py'),'--packet',str(a.out/'build'),'--out',str(a.out/'check.json')]
 if a.public_root:command+=['--public-root',str(a.public_root)]
 q=subprocess.run(command,capture_output=True);(a.out/'check.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'fresh semantic/geometry controls')
 exact=[]
 for name in EXACT:
  b=(a.out/'build'/name).read_bytes();need(b==(H/name).read_bytes(),'exact regenerated '+name);exact.append(dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 old=[x.extract_text()or''for x in PdfReader(H/'summary.pdf').pages];new=[x.extract_text()or''for x in PdfReader(a.out/'build/summary.pdf').pages];need(old==new and len(new)==6,'all six per-page texts')
 r=dict(status='PASS',exact_rebuilt_outputs=exact,reader_pages=6,reader_page_text_hashes=[hashlib.sha256(x.encode()).hexdigest()for x in new],check=json.loads((a.out/'check.json').read_text()),source_extraction_repeated=False,mathematics_replayed=False)
 (a.out/'replay.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS12 exact outputs,6 page texts,98 comparisons,40 controls')
if __name__=='__main__':main()
