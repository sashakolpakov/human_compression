#!/usr/bin/env python3
"""Fresh full-topic XeLaTeX build; complete code/data inclusion, no source PDFs."""
import argparse,hashlib,json,re,shutil,subprocess,unicodedata
from pathlib import Path
import pypdf
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','psl-polytopes','pgl-polytopes','projective-maniplexes','chiral-projective-lines','chiral-projective-groups','required-programs','validation-programs']
def need(b,m):
 if not b:raise ValueError('E_CHIRAL_RENDER_REJECT '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');ap.add_argument('--compare',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');need(pypdf.__version__=='6.13.0','pypdf version');a.out.mkdir(parents=True);out=a.out.resolve();report=[]
 inputs=[*ROOT.glob('*.tex'),*ROOT.glob('sections/*.tex')]
 src=out/'src';src.mkdir()
 for p in inputs:t=src/p.relative_to(ROOT);t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,t)
 scope=json.loads((ROOT/'program_scope.json').read_text())
 for name in DOCS:
  d=out/name;d.mkdir()
  for i in [1,2]:
   p=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(d),name+'.tex'],cwd=src,capture_output=True,text=True,timeout=180)
   (d/f'run{i}.stdout').write_text(p.stdout);(d/f'run{i}.stderr').write_text(p.stderr);need(p.returncode==0,'TeX '+name)
  log=(d/(name+'.log')).read_text();diag=[s for s in log.splitlines() if re.search('Overfull|Missing character|Missing glyph|Warning:',s)];need(not diag,'diagnostics '+name+str(diag))
  pdf=d/(name+'.pdf');pages=[p.extract_text() or '' for p in pypdf.PdfReader(pdf).pages]
  raw='\n'.join(pages);need(not any(ord(c)<32 and c not in '\t\n\r' or c=='\ufffd' or unicodedata.category(c)=='Co' for c in raw),'glyph extraction '+name)
  row={'name':name,'pages':len(pages),'tex_sha256':sha(ROOT/(name+'.tex')),'pdf_sha256':sha(pdf),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in pages],'diagnostics':[]}
  if name.endswith('programs'):
   selected=[]
   for i,t in enumerate(pages,1):
    marker='\n'+str(i);need(t.endswith(marker),'footer '+name);selected.append(t[:-len(marker)])
   text=(ROOT/(name+'.tex')).read_text();blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',text,re.S)
   role='validation only' if name=='validation-programs' else None
   files=[r for r in scope['files'] if (r['role']==role if role else r['role']!='validation only')]
   need(len(blocks)==len(files),'whole file count '+name)
   for block,f in zip(blocks,files):
    rawcode=(ROOT/f['path']).read_text();need(block==rawcode,'exact code in TeX '+f['path']);need(re.sub(r'\s+','',rawcode) in re.sub(r'\s+','','\n'.join(selected)),'full code characters in PDF '+f['path'])
   row['whole_program_data_files']=len(files)
  if a.compare:
   old=[p.extract_text() or '' for p in pypdf.PdfReader(ROOT/(name+'.pdf')).pages];need(pages==old,'authoritative page texts '+name);row['identical_page_text']=True
  report.append(row)
 result={'status':'PASS','documents':report,'total_pages':sum(r['pages'] for r in report),'renderer_sha256':sha(Path(__file__)),'pypdf_version':pypdf.__version__}
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','pages':result['total_pages'],'report':str(out/'report.json')}))
if __name__=='__main__':main()
