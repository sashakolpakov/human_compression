"""Check the complete synthesis closure and new finite joins, without a census."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,subprocess,time
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def need(x,s):
 if not x:raise ValueError(s)
def load(p):return json.loads(Path(p).read_text())
def pin(p):
 p=Path(p);h=hashlib.sha256()
 with p.open('rb')as f:
  for block in iter(lambda:f.read(2**20),b''):h.update(block)
 return dict(path=str(p),bytes=p.stat().st_size,sha256=h.hexdigest())
def same(p,r):
 q=pin(p);need((q['bytes'],q['sha256'])==(r['bytes'],r['sha256']),'exact binding '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
 need(a.out.is_absolute() and not a.out.exists(),'fresh absolute output');start=time.monotonic()
 m=load(P/'manifest.json');deps=load(P/'dependencies.json')
 for r in m['exports']:same(P/r['path'],r)
 for r in deps:same(r['path'],r)
 a.out.mkdir();runs=[]
 def run(name,cmd):
  q=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True)
  (a.out/(name+'.stdout')).write_bytes(q.stdout);(a.out/(name+'.stderr')).write_bytes(q.stderr)
  runs.append(dict(name=name,command=cmd,returncode=q.returncode));need(q.returncode==0 and not q.stderr,'clean '+name)
 for script,name in [('verify.py','synthesis'),('vertex_figures.py','vertex_figures')]:
  run(name,[sys.executable,str(P/script),'--out',str(a.out/(name+'.json'))])
  need(load(a.out/(name+'.json'))==load(P/(name+'.json')),'exact '+name+' output')
 for script in ['check.py','verify.py','vertex_figures.py']:
  q=subprocess.run([sys.executable,'-O',str(P/script)],stdin=subprocess.DEVNULL,capture_output=True)
  need(q.returncode!=0 and b'ordinary Python required'in q.stderr,'optimization guard '+script)
 comps=load(P/'components.json')
 for c in comps:
  same(c['manifest']['path'],c['manifest']);need(load(c['manifest']['path'])['status']==c['status'],'exact acquired acceptance status')
 ledger=load(P/'source_ledger.json');need(len(ledger['rows'])==46 and len({x['id']for x in ledger['rows']})==46,'complete46 source clauses')
 need(ledger['source_tables']==list(range(1,8)) and ledger['source_sections']==list(range(1,8)),'whole fixed-source ledger')
 volume=load(P/'complete_manuscripts.json');same(P/'complete_proofs.pdf',volume['volume'])
 actual=PdfReader(P/'complete_proofs.pdf');need(len(actual.pages)==volume['pages']==41,'complete41page proof volume');i=0
 for r in volume['manuscripts']:
  same(r['tex']['path'],r['tex']);same(r['pdf']['path'],r['pdf']);pdf=PdfReader(r['pdf']['path'])
  need(len(pdf.pages)==r['pages'] and r['first_volume_page']==i+1,'complete manuscript interval')
  for page in pdf.pages:
   need(page.get_contents().get_data()==actual.pages[i].get_contents().get_data(),'whole literal native PDF page');i+=1
  need(r['last_volume_page']==i,'exact end page')
 native_pages=0
 if a.render:
  native=a.out/'native';native.mkdir()
  for j in range(2):run('tex'+str(j),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(P/'principal.tex')])
  need('Overfull'not in(native/'principal.log').read_text(),'clean native layout')
  pdf=PdfReader(native/'principal.pdf');old=PdfReader(P/'native/principal.pdf');need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in old.pages],'exact fresh native manuscript text')
  run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'principal.pdf')])
  native_pages=len(list(native.glob('page-*.png')));need(native_pages==4,'four fresh synthesis pages')
  for p in native.glob('page-*.png'):need(pin(p)['sha256']==pin(P/'native'/p.name)['sha256'],'exact directly viewed native raster')
 z=load(a.out/'synthesis.json');v=load(a.out/'vertex_figures.json')
 result=dict(status='PASS_L070_COMPLETE_SYNTHESIS',manifest=pin(P/'manifest.json'),exports=len(m['exports']),dependencies=len(deps),source_clauses=46,acquired_component_gates=len(comps),complete_manuscripts=16,complete_proof_pages=41,new_manuscript_pages=native_pages,groups=79,occurrences=88,regular=z['regular'],oriented_chiral=z['oriented_chiral'],first_atlas=56,new_vertex_figure_maps=len(v['results']),new_vertex_figure_edges=sum(x['edges_checked']for x in v['results']),synthesis_damages=z['synthesis_damage_controls'],map_damages=v['map_damage_controls'],optimization_guards=3,new_group_calls=0,new_censuses=0,whole_original_credit=0,seconds=time.monotonic()-start,runs=runs)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='runs'}))
if __name__=='__main__':main()
