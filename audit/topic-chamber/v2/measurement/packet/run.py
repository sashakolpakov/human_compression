#!/usr/bin/env python3
"""Replay the complete numerical packet using three explicitly supplied archives."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path

def need(x,m):
    if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
    for key in ['inputs','input_review','input_adoption']:p.add_argument('--'+key.replace('_','-'),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();need(not a.out.exists(),'Fresh replay directory');a.out.mkdir(parents=True);packet=a.packet.resolve();out=a.out.resolve()
    roots=[]
    for k in ['inputs','input_review','input_adoption']:roots+=['--'+k.replace('_','-'),str(getattr(a,k).resolve())]
    def run(name,args):
        r=subprocess.run(args,capture_output=True,text=True,timeout=240);(out/(name+'.stdout')).write_text(r.stdout);(out/(name+'.stderr')).write_text(r.stderr);need(r.returncode==0,'Replay stage '+name)
    run('compute',[sys.executable,'-B','-O',str(packet/'compute.py'),'--protocol',str(packet/'protocol.json'),*roots,'--out',str(out/'arithmetic')])
    run('reader',[sys.executable,'-B','-O',str(packet/'build_reader.py'),'--results',str(out/'arithmetic/results.json'),'--out',str(out/'reader'),'--xelatex',a.xelatex])
    assembled=out/'assembled';assembled.mkdir();shutil.copy(packet/'protocol.json',assembled/'protocol.json')
    for f in ['results.json','comparisons.csv']:shutil.copy(out/'arithmetic'/f,assembled/f)
    for f in ['measurement.tex','measurement.pdf','complete_costs.svg','complete_costs.pdf']:shutil.copy(out/'reader'/f,assembled/f)
    run('controls',[sys.executable,'-B','-O',str(packet/'check.py'),'--packet',str(assembled),*roots,'--out',str(out/'controls')])
    for f in ['results.json','comparisons.csv','measurement.tex','complete_costs.svg','complete_costs.pdf']:
        need((packet/f).read_bytes()==(assembled/f).read_bytes(),'Exact regenerated '+f)
    from pypdf import PdfReader
    old=[p.extract_text() or '' for p in PdfReader(packet/'measurement.pdf').pages];new=[p.extract_text() or '' for p in PdfReader(assembled/'measurement.pdf').pages];need(old==new and len(new)==2,'Exact two-page reader text')
    report={'status':'PASS_PORTABLE_AUTHOR_REPLAY','exact_regenerated_files':['results.json','comparisons.csv','measurement.tex','complete_costs.svg','complete_costs.pdf'],'reader_pages':2,'reader_page_text_sha256':[hashlib.sha256(s.encode()).hexdigest() for s in new],'controls':json.loads((out/'controls/report.json').read_text()),'input_archive_paths_explicit':True,'original_primary_PDFs_not_required_for_arithmetic':True,'no_primary_text_exported':True,'independent_review':False}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='controls'}))
if __name__=='__main__':main()
