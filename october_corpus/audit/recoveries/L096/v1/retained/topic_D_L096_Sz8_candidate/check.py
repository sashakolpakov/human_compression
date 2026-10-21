#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,time
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
GAP='/opt/homebrew/bin/gap'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--full',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if (ROOT/'manifest.json').exists():
  for e in json.loads((ROOT/'manifest.json').read_text())['exports']:
   p=ROOT/e['path'];need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'exact export '+e['path'])
 for name in ['ambient.g','enumerate.g','shadows.g','export_results.g','thin_geometries.tex']:
  shutil.copy2(ROOT/name,a.out/name)
 results=json.loads((ROOT/'results.json').read_text());rows=results['rows']
 need(len(rows)==results['RWPRI']==147 and results['thin']==183,'complete rows')
 need([r['shadow']['row'] for r in rows]==list(range(1,148)),'row identities')
 need(len({tuple(r['triple']) for r in rows})==147,'distinct marked tuples')
 for r in rows:
  s=r['shadow'];need(s['order']==29120 and s['full_flag_extensions']==12,'group/geometry')
  need(len(s['type_results'])==3 and all(type(x) is bool for x in s['type_results']),'three exact type decisions')
  need(s['IP3']==all(s['type_results']) and s['WIP3']==any(s['type_results']),'type quantifiers')
  need(all(x in [4,10,14,26] for x in s['parabolics']),'prime polygons')
  need(isinstance(s['negative_witnesses'],list),'negative witness list')
 counts=[sum(r['shadow']['IP3'] for r in rows),sum(r['shadow']['WIP3'] and not r['shadow']['IP3'] for r in rows),sum(not r['shadow']['WIP3'] for r in rows)]
 need(counts==results['rank3_counts']==[27,48,72],'aggregate')
 executions={}
 def run(name,limit,marker=None):
  t=time.monotonic();r=subprocess.run([GAP,'-q','-b',name+'.g'],cwd=a.out,capture_output=True,text=True,timeout=limit)
  (a.out/(name+'.stdout.log')).write_text(r.stdout);(a.out/(name+'.stderr.log')).write_text(r.stderr)
  need(r.returncode==0 and not r.stderr,'clean '+name)
  if marker:need(marker in r.stdout,'completion '+name)
  executions[name]=dict(seconds=time.monotonic()-t,returncode=0,stderr_empty=True)
 run('enumerate',30,'COMPLETE_SZ8_INVOLUTION_CENSUS')
 need(sha(a.out/'sz8_rows.g')==sha(ROOT/'sz8_rows.g'),'entire enumerated roster')
 if a.full:run('shadows',180,'PASS_SZ8_RANK3_SHADOWS')
 else:shutil.copy2(ROOT/'sz8_shadow_results.g',a.out/'sz8_shadow_results.g')
 run('export_results',30)
 need(json.loads((a.out/'results.json').read_text())==results,'all retained type decisions')
 render=None
 if a.render:
  for j in [1,2]:
   r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','thin_geometries.tex'],cwd=a.out,capture_output=True,text=True,timeout=30)
   (a.out/('render%d.log'%j)).write_text(r.stdout+r.stderr);need(r.returncode==0,'render')
  log=(a.out/'thin_geometries.log').read_text();bad=[l for l in log.splitlines() if any(w in l for w in ['Overfull','Underfull','LaTeX Warning','Missing character'])];need(not bad,'clean render')
  texts=[p.extract_text() or '' for p in PdfReader(a.out/'thin_geometries.pdf').pages]
  need(len(texts)==3 and texts==[p.extract_text() or '' for p in PdfReader(ROOT/'thin_geometries.pdf').pages],'exact3pages')
  render=dict(pages=3,diagnostics=[])
 report=dict(status='PASS',author='root',census=[1083,195,186,186,183,147],rank3_and_full_IP_counts=counts,exact_flag_extensions=1764,type_tests=441,fresh_shadow_replay=a.full,retained_shadow_receipt=None if a.full else json.loads((ROOT/'shadows_execution.json').read_text()),executions=executions,render=render,new_source_credit=0,new_question_credit=0,complete_Lean=False,all_RWPRI_are_thin_proved=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
