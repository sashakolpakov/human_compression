#!/usr/bin/env python3
"""Freshly render and cross-check the reader without reopening the proof census."""
from pathlib import Path
import argparse,csv,hashlib,json,shutil,subprocess,sys,xml.etree.ElementTree as ET
import pypdf
HERE=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def number(s):return float(s.strip().split('\\')[0].replace(',',''))
def check_values(base):
    m=json.loads((base/'numerical_manifest.json').read_text());b=(base/'measurement.json').read_bytes()
    need(sha(b)==next(r['sha256'] for r in m['exports'] if r['path']=='results.json'),'Frozen numerical source')
    d=json.loads(b);tex=(base/'measurement.tex').read_text()
    primary=d['factors']['NFC']['calibrated_selected']['characters_without_whitespace']
    count=0
    for row in primary['conditional_applications']:
        lines=[line for line in tex.splitlines() if line.startswith(row['source_id']+' &')]
        need(len(lines)==1,'Unique application table row')
        fields=lines[0].split('&');f=row['factor']
        need(number(fields[2])==f['numerator'] and number(fields[3])==f['denominator'],'Complete document table costs')
        need(number(fields[4])==round(f['decimal'],6),'Conditional table factor');count+=3
    for form in ['NFC','NFKC']:
        rows=[line for line in tex.splitlines() if line.startswith(form+' &')]
        metrics=list(d['factors'][form]['calibrated_selected'])
        need(len(rows)==len(metrics)==5,'All five calibrated units')
        for line,key in zip(rows,metrics):
            fields=line.split('&');r=d['factors'][form]['calibrated_selected'][key]
            need(number(fields[2])==round(r['written_topic']['decimal'],6),'Written sensitivity factor')
            need(number(fields[3])==round(r['program_inclusive_topic']['decimal'],6),'Program sensitivity factor');count+=2
    need('49{,}059+78{,}251' in tex and '127{,}310+53{,}035' in tex,'Acquisition charged in both formulas')
    for value in [primary['written_topic']['decimal'],primary['program_inclusive_topic']['decimal'],primary['raw_program_representation_sensitivity']['decimal']]:
        need(f'{value:.6f}' in tex,'Primary factor present')
    return d,count
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');ap.add_argument('--author-pdf',type=Path);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'Fresh output directory required')
    a.out.mkdir(parents=True)
    for name in ['measurement.tex','measurement.json','numerical_manifest.json','plot_costs.py']:
        shutil.copyfile(HERE/name,a.out/name)
    data,checks=check_values(a.out)
    proc=subprocess.run([sys.executable,'-B','plot_costs.py'],cwd=a.out,text=True,capture_output=True)
    (a.out/'plot.log').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'Plot execution')
    ET.parse(a.out/'costs.svg')
    with (a.out/'costs.csv').open() as f:rows=list(csv.DictReader(f))
    need(len(rows)==7,'Complete acquisition and six stages')
    p=data['factors']['NFC']['calibrated_selected']['characters_without_whitespace']['costs']
    need([int(rows[-1][k]) for k in ['source_cumulative','written_cumulative','including_complete_program_cumulative']]==[p['full_sources'],p['full_written_papers'],p['full_program_inclusive']],'Graph final costs')
    diagnostics=[]
    for i in [1,2]:
        p1=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,text=True,capture_output=True)
        log=p1.stdout+p1.stderr;(a.out/f'pass{i}.log').write_text(log)
        need(p1.returncode==0,'TeX compile')
        if i==2:
            diagnostics=[line for line in log.splitlines() if any(t in line for t in ['Overfull','Underfull','Missing character','LaTeX Warning'])]
    need(not diagnostics,'Render diagnostics')
    reader=pypdf.PdfReader(a.out/'measurement.pdf');need(len(reader.pages)==3,'Three reader pages')
    texts=[p.extract_text() or '' for p in reader.pages]
    bad=[(i+1,ord(c)) for i,t in enumerate(texts) for c in t if (ord(c)<32 and c not in '\n\t\r') or 0xE000<=ord(c)<=0xF8FF or c=='\ufffd']
    need(not bad,'Extracted glyph scan')
    comparison=None
    if a.author_pdf:
        old=[p.extract_text() or '' for p in pypdf.PdfReader(a.author_pdf).pages]
        need(old==texts,'Exact per-page author PDF text');comparison=True
    report={'status':'PASS_READER_RENDER_AND_NUMERICAL_CROSSCHECK','reader_pages':3,'numerical_table_checks':checks,'metric_rows':10,'application_rows':6,'graph_stages':7,'glyph_issues':bad,'render_diagnostics':diagnostics,'exact_author_page_text_match':comparison,'page_text_sha256':[sha(t.encode()) for t in texts],'numerical_results_sha256':sha((a.out/'measurement.json').read_bytes()),'numerical_manifest_sha256':sha((a.out/'numerical_manifest.json').read_bytes()),'reader_tex_sha256':sha((a.out/'measurement.tex').read_bytes()),'pypdf_version':pypdf.__version__,'proof_census_repeated':False,'numerical_admission_claimed':False}
    (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
