from pathlib import Path
import argparse,json,hashlib,subprocess,shutil
from independent import model
HERE=Path(__file__).resolve().parent
PIN='e9d55ceb3ac44abe327c8481cc0fc256c544fbf713e89dcecafe9cf91296531e'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(t,m):
 if not t:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 author=a.study_root/'topic_C_N014_transitivity_converse';need(digest(author/'manifest.json')==PIN,'author pin')
 m=json.loads((author/'manifest.json').read_text());n=0
 for e in m['exports']:
  p=author/e['path'];need(p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],'author export '+e['path']);n+=1
 report=model();report['author_exports']=n;report['author_manifest_sha256']=PIN
 own=HERE/'manifest.json'
 if own.exists():
  for e in json.loads(own.read_text())['exports']:
   p=HERE/e['path'];need(p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],'review export')
 if a.render:
  from pypdf import PdfReader
  tex=author/'transitivity_converse.tex';shutil.copy2(tex,a.out/tex.name)
  for i in range(2):
   r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',tex.name],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{i+1}.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'render')
  log=(a.out/'transitivity_converse.log').read_text();need(all(z not in log for z in ['Overfull','undefined','Missing character']),'render diagnostics')
  page=lambda p:[x.extract_text() for x in PdfReader(p).pages]
  need(page(a.out/'transitivity_converse.pdf')==page(author/'transitivity_converse.pdf'),'exact two page text');report['rendered_pages']=2
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
