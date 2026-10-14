from pathlib import Path
import json,hashlib,subprocess,os,shutil
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L045_symplectic_upper_distinct';A=S/'corpus106_L045_symplectic_upper_v2';P=S/'corpus106_L045_symplectic_upper_v1'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
d=json.loads((A/'edition_delta.json').read_text());old=(P/'symplectic_upper.tex').read_text();new=(A/'symplectic_upper.tex').read_text()
need(old.count(d['before'])==1,'single old paragraph');need(old.replace(d['before'],d['after'])==new,'sole exact editorial paragraph')
changed=[]
for x in json.loads((P/'manifest.json').read_text())['exports']:
 if sha(P/x['path'])!=sha(A/x['path']):changed.append(x['path'])
need(set(changed)==set(json.loads((A/'edition_files.json').read_text())['changed_old_exports']),'exact unchanged scientific bytes')
roots={'study':S,'public':S.parents[1]/'math_compression','gap':Path('/opt/homebrew/bin/gap').resolve().parent.parent}
for x in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'export '+x['path'])
deps=json.loads((A/'dependencies.json').read_text())['files']
for x in deps:
 p=roots[x['namespace']]/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'dependency '+x['path'])
N=W/'final_native';N.mkdir();shutil.copy2(A/'symplectic_upper.tex',N/'symplectic_upper.tex');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
commands=[]
for i in range(2):
 cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(N),str(N/'symplectic_upper.tex')]
 z=subprocess.run(cmd,cwd=N,capture_output=True,env=env,timeout=60);(N/f'build{i}.stdout').write_bytes(z.stdout);(N/f'build{i}.stderr').write_bytes(z.stderr);need(z.returncode==0 and not z.stderr,'native clean build');commands.append(cmd)
log=(N/'symplectic_upper.log').read_text();need(all(s not in log for s in ('Overfull','Underfull','LaTeX Warning')),'clean native log')
pages=PdfReader(N/'symplectic_upper.pdf').pages;text='\n'.join(p.extract_text() or '' for p in pages);need(text==(A/'native_text.txt').read_text(),'final native exacttext')
cmd=['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%02d.png'),str(N/'symplectic_upper.pdf')];z=subprocess.run(cmd,capture_output=True,timeout=60);need(z.returncode==0,'render');commands.append(cmd)
save(W/'final_edition_report.json',{'status':'PASS_EXACT_EDITORIAL_V2','author_manifest_sha256':sha(A/'manifest.json'),'unchanged_mathematics_programs_and_reports':True,'changed_old_exports':changed,'bindings':len(deps),'pages':len(pages),'exact_native_text':True,'commands':commands,'mathematical_replay':'replay01/report.json; all scientific bytes identical'})
print('PASS exact editorial v2; four fresh native pages; all final bindings')
