import ast,copy,hashlib,importlib.util,itertools,json,os,re,subprocess,sys,time
from pathlib import Path
from pypdf import PdfReader
if sys.flags.optimize: raise RuntimeError('normal Python required')
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_actual_wings_v1';W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def verify(row,base):
 p=Path(row['path']);p=p if p.is_absolute() else base/p
 need(p.is_file(),f'missing {p}');need(sha(p)==row['sha256'],f'hash {p}')
 if 'bytes' in row:need(p.stat().st_size==row['bytes'],f'size {p}')
 return str(p)
need(sha(P/'manifest.json')=='9069a4a3c03a1ae05a27e9aa4bfe71ce32a9c917737a771eb93bafb883e0a268','author edition')
M=json.loads((P/'manifest.json').read_text());D=json.loads((P/'dependencies.json').read_text());A=json.loads((P/'acquired_packets.json').read_text());verified=[]
for r in M['exports']:verified.append(verify(r,P))
for r in D:verified.append(verify(r,S))
for r in A:verified.append(verify(r,S))
write(W/'integrity.json',{'status':'PASS','exports':len(M['exports']),'dependencies':len(D),'acquired_roots':len(A),'unique_paths':len(set(verified))})
receipts=[]
def run(name,cmd,cap=90,expected=0,env=None):
 t=time.monotonic();r=subprocess.run(cmd,cwd=W,capture_output=True,timeout=cap,env=env)
 (W/(name+'.stdout')).write_bytes(r.stdout);(W/(name+'.stderr')).write_bytes(r.stderr)
 rec={'name':name,'command':cmd,'exit_code':r.returncode,'seconds':time.monotonic()-t,'stdout_sha256':sha(W/(name+'.stdout')),'stderr_sha256':sha(W/(name+'.stderr'))};receipts.append(rec)
 need(r.returncode==expected if expected==0 else r.returncode!=0,f'{name}: exit {r.returncode}')
 return r
run('literal',[sys.executable,str(P/'check_wings.py'),'--output',str(W/'literal_report.json')])
need((W/'literal_report.json').read_bytes()==(P/'direct_report.json').read_bytes(),'literal report differs')
r=run('gap',['/opt/homebrew/bin/gap','-q','-b',str(P/'gap_wings.g')]);need(not r.stderr and b'PASS_WINGS_SMALL15_LARGE4_ANCHORS4' in r.stdout,'gap failure')
r=run('extract_a11',['/opt/homebrew/bin/gap','-q','-b',str(P/'extract_a11.g')]);need(not r.stderr and b'DONE_ACTUAL_A11_WINGS' in r.stdout,'extraction failure')
small=json.loads((S/'topic_B_L047_candidate_v2/finite_results.json').read_text());rows=[]
for kind in ('small_transitive','primitive_markings'):
 for j,row in enumerate(small[kind]['literal_solutions']):
  if 2*len(row['permutations'])>row['n']:rows.append({'kind':kind,'source_index':j,'n':row['n'],'id':row['id'],'permutations':row['permutations']})
records=(S/'reboot_20261013/L071_A11_full_IP01/records.g').read_text();ids=ast.literal_eval(re.search(r'recordedMarks\[6\]:=(\[.*?\]);;',records,re.S)[1])
parts=re.findall(r'MARKS (\d+) (\[.*?\])\s*ANCHORS',r.stdout.decode(),re.S)
large=[{'source_index':int(j)-1,'ids':ids[int(j)-1],'permutations':ast.literal_eval(text)} for j,text in parts]
data=json.loads((P/'wing_inputs.json').read_text());need(data=={'small_exceptions':rows,'a11_rank_six':large},'actual acquired representative mismatch')
gap=(P/'gap_wings.g').read_text()
for key,expected in [('small',[x['permutations'] for x in rows]),('large',[x['permutations'] for x in large])]:need(ast.literal_eval(re.search(key+r':= (\[.*?\]);;',gap,re.S)[1])==expected,'GAP literal mismatch')
write(W/'input_provenance.json',{'status':'PASS','small_indices':[[x['kind'],x['source_index']] for x in rows],'large_indices':[x['source_index'] for x in large],'all_actual_census_ids':ids,'fresh_gap_extraction_matches':True,'gap_embedded_data_exact':True})
controls=[]
for name,edit in [('missing',lambda d:d['a11_rank_six'].pop()),('duplicate',lambda d:d['a11_rank_six'].__setitem__(3,copy.deepcopy(d['a11_rank_six'][0]))),('nonpermutation',lambda d:d['a11_rank_six'][0]['permutations'][0].__setitem__(0,2)),('wrong_index',lambda d:d['small_exceptions'][0].__setitem__('source_index',99))]:
 d=copy.deepcopy(data);edit(d);inp=W/(name+'.json');write(inp,d);out=W/(name+'_result.json');run('bad_'+name,[sys.executable,str(P/'check_wings.py'),'--input',str(inp),'--output',str(out)],expected=1);need(not out.exists(),'bad input wrote acceptance');controls.append(name)
for name,cmd,env in [('opt_argument',[sys.executable,'-O',str(P/'check_wings.py'),'--output',str(W/'opt_result.json')],None),('opt_env',[sys.executable,str(P/'check_wings.py'),'--output',str(W/'opt_env_result.json')],dict(os.environ,PYTHONOPTIMIZE='1'))]:run(name,cmd,expected=1,env=env);controls.append(name)
spec=importlib.util.spec_from_file_location('wing',P/'check_wings.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
# Exhaust every centralizing permutation for distinct orbit patterns up to six points.
central_cases=[(3,[(1,0,2)],2),(4,[(1,0,3,2)],0),(4,[(1,0,3,2),(2,3,0,1)],0),(5,[(1,0,3,2,4)],4),(6,[(1,0,3,2,5,4)],0),(6,[(1,0,2,4,3,5),(0,2,1,3,5,4)],0)]
central_reports=[]
for n,marks,a in central_cases:
 brute={q for q in itertools.permutations(range(n)) if q[a]==a and all(all(q[p[x]]==p[q[x]] for x in range(n)) for p in marks)}
 computed=set(mod.centralizer_fixing(marks,a));need(brute==computed,'equivariant map completeness control');central_reports.append({'n':n,'marks':marks,'fixed':a,'centralizer_order':len(brute),'permutations_examined':__import__('math').factorial(n)})
write(W/'controls.json',{'status':'PASS','damaged_or_optimized':controls,'independent_centralizer_controls':central_reports})
for i in range(2):
 r=run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(W),str(P/'actual_wings.tex')]);need(not r.stderr,'native stderr')
pdf=W/'actual_wings.pdf';reader=PdfReader(pdf);need(len(reader.pages)==3,'native page count');need([p.extract_text() for p in reader.pages]==[p.extract_text() for p in PdfReader(P/'actual_wings.pdf').pages],'native text differs')
for number in range(1,4):run('page'+str(number),['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110',f'-dFirstPage={number}',f'-dLastPage={number}',f'-sOutputFile={W}/page{number}.png',str(pdf)])
source=S/'sources/stability2024.pdf';run('source17',['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-dFirstPage=17','-dLastPage=17',f'-sOutputFile={W}/source17.png',str(source)])
write(W/'receipts.json',receipts);write(W/'report.json',{'status':'PASS_BOUNDED_ACTUAL_WINGS','exports':len(M['exports']),'dependencies':len(D),'fresh_small_representatives':len(rows),'fresh_A11_representatives':len(large),'input_origin_verified':True,'native_pages':3,'independent_centralizer_controls':len(central_cases),'negative_controls':len(controls),'whole_original_credit':0})
print(json.dumps(json.loads((W/'report.json').read_text())))
