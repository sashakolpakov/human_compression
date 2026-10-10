#!/usr/bin/env python3
"""Render the unchanged phase207 papers for page and presentation audit only."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
import pypdf
ROOT=Path(__file__).resolve().parent
EXPECTED={'umbrella':('phase207_topic_A_umbrella.md','6780b3447a956c697ec09ee8f6de5371462ff23551663259fc5eb9731097d59d'),
          'application':('phase207_L032_application.md','e45df2d55f8a86001359806f9047932195787f6b7aa2903a968a77f8163de435')}
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
 config=json.loads((ROOT/'phase228_render_config.json').read_text())
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
  for i in [1,2]:run('xelatex'+str(i),[xe,'-interaction=nonstopmode','-halt-on-error','paper.tex'])
  pdf=pypdf.PdfReader(d/'paper.pdf');(d/'extraction.txt').write_text('\n'.join(p.extract_text() or '' for p in pdf.pages))
  diagnostics=[line for line in (d/'paper.log').read_text().splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',line,re.I)]
  run('rasterize',[shutil.which('gs'),'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r85','-sOutputFile=page-%02d.png','paper.pdf'])
  need(sha(source)==digest,'source changed during render')
  reports[name]={'source':file,'source_sha256':digest,'pages':len(pdf.pages),'pdf_sha256':sha(d/'paper.pdf'),'diagnostics':diagnostics,'AST_math_table_code_preserved':True,'commands':commands}
 result={'status':'RENDER_COMPLETE_VISUAL_REVIEW_SEPARATE','config':config,'config_sha256':sha(ROOT/'phase228_render_config.json'),'renderer_sha256':sha(ROOT/'phase228_render.py'),'papers':reports,'matched_ratio':None,'scope':'Layout audit of unchanged full manuscripts. No new source credit or matched source/replacement measurement.'}
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{'pages':v['pages'],'diagnostics':v['diagnostics']}for k,v in reports.items()}))
if __name__=='__main__':main()
