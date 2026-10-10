#!/usr/bin/env python3
"""Render the unchanged phase229 paper for page and presentation audit only."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
import pypdf
ROOT=Path(__file__).resolve().parent
EXPECTED={'application':('phase229_equal_label_application.md','5aa69f79f3e50fe1c8cfe1ddcd0286b54080cfd54048df03fa5386ef399633a1')}
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def presentation(text):
 # Same limited escaping as the retained phase98 presentation helper.
 protected=re.compile(r'```[^\n]*\n.*?\n```|(?m:^(?: {4}[^\n]*(?:\n|$))+)|`[^`\n]+`|\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<!\\)\$[^$\n]+\$',re.S)
 def escape(s):return re.sub(r'(?<=[A-Z])\*(?!\*)',r'\\*',s.replace('_',r'\_'))
 chunks=[];at=0
 for m in protected.finditer(text):chunks.extend([escape(text[at:m.start()]),m.group()]);at=m.end()
 return ''.join(chunks+[escape(text[at:])])
def nodes(tree,typ):
 result=[]
 def walk(x):
  if isinstance(x,dict):
   if x.get('t')==typ:result.append(x['c'])
   for y in x.values():walk(y)
  elif isinstance(x,list):
   for y in x:walk(y)
 walk(tree);return result
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh directory required')
 out=a.out.resolve();out.mkdir(parents=True)
 config=json.loads((ROOT/'phase232_render_config.json').read_text())
 reports={}
 for name,(file,digest) in EXPECTED.items():
  source=ROOT/file;need(sha(source)==digest,'changed manuscript')
  d=out/name;d.mkdir();body=source.read_text();(d/'source.md').write_text(body);(d/'render.md').write_text(presentation(body));(d/'header.tex').write_text(config['header'])
  commands=[]
  def run(label,cmd):
   p=subprocess.run(cmd,cwd=d,text=True,capture_output=True,timeout=120)
   (d/(label+'.stdout')).write_text(p.stdout);(d/(label+'.stderr')).write_text(p.stderr)
   need(p.returncode==0,label+' failed');commands.append(cmd)
  reader='--from='+config['reader'];pd=shutil.which('pandoc');xe=shutil.which('xelatex')
  need(pd and xe,'render programs unavailable')
  for n in ['source','render']:run(n+'-ast',[pd,n+'.md',reader,'--to=json','--output='+n+'.json'])
  s=json.loads((d/'source.json').read_text());t=json.loads((d/'render.json').read_text())
  for typ in ['Math','Table','CodeBlock']:need(nodes(s,typ)==nodes(t,typ),'changed '+typ)
  cmd=[pd,'render.md',reader,'--standalone','--to=latex','--include-in-header=header.tex']
  for v in config['variables']:cmd.extend(['--variable',v])
  run('latex',cmd+['--output=paper.tex'])
  # A layout-only line break in the long dependency path (18), after its
  # second arrow. Every word and arrow is retained; source ASTs stay unchanged.
  tex=(d/'paper.tex').read_text()
  pattern=r'\\\[\s*(\\text\{generalized cubes and halving\}.*?)(\\tag\{18\})\s*\\\]'
  found=re.search(pattern,tex,re.S);need(found is not None,'dependency display18 absent')
  old_body=found.group(1)
  split=' \\text{marked identification (6)}'
  need(old_body.count(split)==1,'ambiguous display18 split')
  new_body='\\begin{gathered}\n'+old_body.replace(split,' \\\\\n'+split)+'\\end{gathered}\n'
  tex=tex[:found.start(1)]+new_body+tex[found.end(1):]
  (d/'paper.tex').write_text(tex)
  layout={'scope':'Display18 only: gathered line break before marked identification; no words, arrows or tags removed.',
          'old_math_body':old_body,'new_math_body':new_body}
  (d/'layout_transform.json').write_text(json.dumps(layout,indent=2)+'\n')
  for i in [1,2]:run('xelatex'+str(i),[xe,'-interaction=nonstopmode','-halt-on-error','paper.tex'])
  pdf=pypdf.PdfReader(d/'paper.pdf');(d/'extraction.txt').write_text('\n'.join(p.extract_text() or '' for p in pdf.pages))
  diagnostics=[line for line in (d/'paper.log').read_text().splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',line,re.I)]
  run('rasterize',[shutil.which('gs'),'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r85','-sOutputFile=page-%02d.png','paper.pdf'])
  need(sha(source)==digest,'source changed during render')
  reports[name]={'source':file,'source_sha256':digest,'pages':len(pdf.pages),'pdf_sha256':sha(d/'paper.pdf'),'diagnostics':diagnostics,'AST_math_table_code_preserved':True,'explicit_typesetting_layout_transform':layout,'commands':commands}
 result={'status':'RENDER_COMPLETE_VISUAL_REVIEW_SEPARATE','config':config,'config_sha256':sha(ROOT/'phase232_render_config.json'),'renderer_sha256':sha(ROOT/'phase232_render.py'),'papers':reports,'matched_ratio':None,'scope':'Layout audit of unchanged full manuscripts. No new source credit or matched source/replacement measurement.'}
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{'pages':v['pages'],'diagnostics':v['diagnostics']}for k,v in reports.items()}))
if __name__=='__main__':main()
