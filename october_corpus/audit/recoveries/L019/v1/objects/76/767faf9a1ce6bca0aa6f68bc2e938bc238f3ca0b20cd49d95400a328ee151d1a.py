from pathlib import Path
import ast,copy,hashlib,importlib.util,itertools,json,os,re,subprocess,sys,time
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('normal Python required')
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_faithful_augmentation_v1';W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
def save(name,data):(W/name).write_text(json.dumps(data,indent=2)+'\n')
def verify(row,base):
 p=Path(row['path']);p=p if p.is_absolute() else base/p;need(sha(p)==row['sha256'],'hash '+str(p));need(p.stat().st_size==row['bytes'],'size '+str(p))
need(sha(P/'manifest.json')=='8840548af87fadaf13127d1ce041a85238fd4c341b0841814ac047e31de1c6a4','wrong edition')
man=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text());acq=json.loads((P/'acquired_packets.json').read_text())
for r in man['exports']:verify(r,P)
for r in deps:verify(r,S)
for r in acq:verify(r,S)
need((P/'permutation_library.py').read_bytes()==(S/'topic_B_L019_actual_wings_v1/check_wings.py').read_bytes(),'library equality')
receipts=[]
def run(name,cmd,expected=0,env=None):
 t=time.monotonic();r=subprocess.run(cmd,cwd=W,capture_output=True,timeout=90,env=env);(W/(name+'.stdout')).write_bytes(r.stdout);(W/(name+'.stderr')).write_bytes(r.stderr);receipts.append({'name':name,'cmd':cmd,'seconds':time.monotonic()-t,'returncode':r.returncode});need(r.returncode==0 if expected==0 else r.returncode!=0,name+' exit');return r
r=run('literal',[sys.executable,str(P/'check_primitive_boundary.py'),'--output',str(W/'literal_report.json')]);need(not r.stderr,'literal stderr');need((W/'literal_report.json').read_bytes()==(P/'direct_report.json').read_bytes(),'report exact')
r=run('gap',['/opt/homebrew/bin/gap','-q','-b',str(P/'gap_boundary.g')]);need(not r.stderr and b'PASS_PRIMITIVE12_ORIENTATIONS24_SURVIVORS4_TYPES2' in r.stdout,'GAP')
data=json.loads((P/'primitive_inputs.json').read_text());source=json.loads((S/'topic_B_L047_candidate_v2/finite_results.json').read_text())['primitive_markings']['literal_solutions'];expected=[{'source_index':j,**{k:row[k] for k in ('n','id','types','permutations')}} for j,row in enumerate(source)];need(data['representatives']==expected,'all literal source rows')
embedded=ast.literal_eval(re.search(r'rows:=(\[.*?\]);;', (P/'gap_boundary.g').read_text(),re.S)[1]);need(embedded==[r['permutations'] for r in expected],'GAP embedded literals')
report=json.loads((W/'literal_report.json').read_text());independent=[]
# Use the actual parity extension, independently of the author's single-value conflict search.
for row in expected:
 marks=[tuple(x-1 for x in p) for p in row['permutations']];n=row['n']
 for orient,seq in enumerate([marks,marks[::-1]]):
  identity=tuple(range(n));found={(identity,0)};queue=[(identity,0)]
  while queue:
   p,par=queue.pop()
   for j,q in enumerate(seq):
    pair=(tuple(q[x] for x in p),par^(j==0))
    if pair not in found:found.add(pair);queue.append(pair)
  projection={p for p,par in found};consistent=len(found)==len(projection)
  r=report['tested_orientations'][2*row['source_index']+orient]
  need(len(projection)==r['group_order'] and consistent==r['character_exists'],'parity extension disagreement')
  independent.append({'source_index':row['source_index'],'orientation':orient,'projection_order':len(projection),'extension_order':len(found),'character_exists':consistent})
# Independently compute the two displayed product orders from their literal tuples.
types=[]
for row in [report['surviving'][0],report['surviving'][1]]:
 marks=[tuple(x-1 for x in p) for p in row['permutations']];orders=[]
 for a,b in zip(marks,marks[1:]):
  product=tuple(b[x] for x in a);p=tuple(range(len(a)));count=0
  while True:
   p=tuple(product[x] for x in p);count+=1
   if p==tuple(range(len(a))):break
  orders.append(count)
 types.append(orders)
need(types==[[6,5],[4,5]],'displayed types')
save('independent_character_controls.json',{'status':'PASS','cases':independent,'displayed_types':types,'exact_source_rows':12,'gap_literal_equality':True})
controls=[]
for name,edit in [('missing',lambda d:d['representatives'].pop()),('duplicate_index',lambda d:d['representatives'][1].__setitem__('source_index',0)),('bad_permutation',lambda d:d['representatives'][0]['permutations'][0].__setitem__(0,2))]:
 d=copy.deepcopy(data);edit(d);save(name+'.json',d);out=W/(name+'_report.json');run('bad_'+name,[sys.executable,str(P/'check_primitive_boundary.py'),'--input',str(W/(name+'.json')),'--output',str(out)],expected=1);need(not out.exists(),'bad acceptance written');controls.append(name)
for name,cmd,env in [('optflag',[sys.executable,'-O',str(P/'check_primitive_boundary.py'),'--output',str(W/'bad_opt1.json')],None),('optenv',[sys.executable,str(P/'check_primitive_boundary.py'),'--output',str(W/'bad_opt2.json')],dict(os.environ,PYTHONOPTIMIZE='1'))]:run(name,cmd,expected=1,env=env);need(not Path(cmd[-1]).exists(),'optimized output');controls.append(name)
for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(W),str(P/'faithful_augmentation.tex')])
pdf=W/'faithful_augmentation.pdf';need(len(PdfReader(pdf).pages)==3,'page count');need([p.extract_text() for p in PdfReader(pdf).pages]==[p.extract_text() for p in PdfReader(P/'faithful_augmentation.pdf').pages],'native text')
for i in [1,2,3]:run('page'+str(i),['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110',f'-dFirstPage={i}',f'-dLastPage={i}',f'-sOutputFile={W}/page{i}.png',str(pdf)])
run('source35',['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-dFirstPage=35','-dLastPage=35',f'-sOutputFile={W}/source35.png',str(S/'sources/stability2024.pdf')])
save('receipts.json',receipts);save('report.json',{'status':'PASS_BOUNDED_FAITHFUL_AUGMENTATION','exports':len(man['exports']),'dependencies':len(deps),'acquired_roots':len(acq),'source_representatives':12,'orientations':24,'surviving_oriented_records':4,'distinct_types':2,'independent_character_checks':24,'negative_controls':len(controls),'native_pages':3,'whole_original_credit':0});print((W/'report.json').read_text())
