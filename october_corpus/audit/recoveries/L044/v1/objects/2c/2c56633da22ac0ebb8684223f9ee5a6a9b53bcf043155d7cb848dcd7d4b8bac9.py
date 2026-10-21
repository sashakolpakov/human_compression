from pathlib import Path
import json,hashlib,subprocess
from pypdf import PdfReader
S=Path(__file__).resolve().parent.parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,expected_prefix,pages in [('odd_degree_nonfirst_internal','44aafd3',3)]:
 A=S/('topic_B_L044_'+stem+'_v1');W=S/'reboot_20261013'/('L044_'+stem+'_distinct');W.mkdir(exist_ok=True)
 assert h(A/'manifest.json').startswith(expected_prefix)
 m=json.loads((A/'manifest.json').read_text());d=json.loads((A/'dependencies.json').read_text());count=0
 for base,records in [(A,m['exports']),(S,d['bindings'])]:
  for x in records:
   p=base/x['path'];assert p.stat().st_size==x['bytes'] and h(p)==x['sha256'],str(p)
 for x in d['bindings']:
  p=S/x['path']
  if p.name=='manifest.json':
   for e in json.loads(p.read_text()).get('exports',[]):
    q=p.parent/e['path'];assert q.stat().st_size==e['bytes'] and h(q)==e['sha256'],str(q);count+=1
 for k in range(2):
  with (W/f'build{k+1}.log').open('wb') as f:subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={W}',str(A/(stem+'.tex'))],cwd=A,stdout=f,stderr=subprocess.STDOUT,check=True)
 a=PdfReader(A/(stem+'.pdf'));b=PdfReader(W/(stem+'.pdf'));assert len(a.pages)==len(b.pages)==pages
 log=(W/(stem+'.log')).read_text();assert not any(x in log for x in ['Overfull','LaTeX Warning:','undefined references'])
 texts=[]
 for x,y in zip(a.pages,b.pages):assert x.extract_text()==y.extract_text();texts.append(hashlib.sha256(y.extract_text().encode()).hexdigest())
 subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100',f'-sOutputFile={W}/page%02d.png',str(W/(stem+'.pdf'))],check=True)
 r={'status':'PASS_BINDINGS_AND_NATIVE_REPLAY','author_manifest_sha256':h(A/'manifest.json'),'exports':len(m['exports']),'dependency_bindings':len(d['bindings']),'acquired_direct_exports':count,'pages':pages,'page_text_sha256':texts,'whole_original_credit':0};(W/'replay_report.json').write_text(json.dumps(r,indent=2)+'\n');print(stem,json.dumps(r))
