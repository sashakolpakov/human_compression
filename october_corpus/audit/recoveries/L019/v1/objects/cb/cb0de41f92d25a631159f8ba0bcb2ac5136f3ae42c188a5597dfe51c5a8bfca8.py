from pathlib import Path
import ast, copy, hashlib, importlib.util, itertools, json, os, re, subprocess, sys, time
from pypdf import PdfReader
if sys.flags.optimize: raise RuntimeError('normal Python required')
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_initial_fracture_v1';W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x: raise RuntimeError(m)
def save(name,data):(W/name).write_text(json.dumps(data,indent=2)+'\n')
def verify(row,base):
    p=Path(row['path']);p=p if p.is_absolute() else base/p
    need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'binding '+str(p))
need(sha(P/'manifest.json')=='e24b1df4bb853a9f1ba02073507da23acd2046d37a42988fa25095a9283dc3c4','edition')
man=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text());acq=json.loads((P/'acquired_packets.json').read_text())
for row in man['exports']:verify(row,P)
for row in deps+acq:verify(row,S)
need((P/'permutation_library.py').read_bytes()==(S/'topic_B_L019_actual_wings_v1/check_wings.py').read_bytes(),'acquired library')
data=json.loads((P/'inputs.json').read_text())
expected={'a11_rank_six':json.loads((S/'topic_B_L019_actual_wings_v1/wing_inputs.json').read_text())['a11_rank_six'],
 's8_rank_six':[{'source_index':i,'permutations':p} for i,p in enumerate(json.loads((S/'topic_B_L044_symmetric_faithful_pairs_v1/finite/author_certificate01/records.json').read_text()))],
 'small_extremal':json.loads((S/'topic_B_L047_candidate_v2/finite_results.json').read_text())['small_extremal']['extremal_markings']}
need(data==expected,'complete source roster')
# These are literal original array extractions, not an execution of a relocated historical extractor.
embedded=[ast.literal_eval(x) for x in re.findall(r'(?:tt|t):=List\((\[.*?\]),PermList\);;', (P/'gap_boundaries.g').read_text())]
need(embedded==[row['permutations'] for key in ('a11_rank_six','s8_rank_six','small_extremal') for row in data[key]],'GAP literal arrays')
receipts=[]
def run(name,cmd,success=True,env=None):
    start=time.monotonic();r=subprocess.run(cmd,cwd=W,capture_output=True,timeout=90,env=env)
    (W/(name+'.stdout')).write_bytes(r.stdout);(W/(name+'.stderr')).write_bytes(r.stderr)
    receipts.append({'name':name,'args':cmd,'seconds':time.monotonic()-start,'returncode':r.returncode})
    need((r.returncode==0)==success,name+' exit');return r
r=run('literal',[sys.executable,str(P/'check_boundaries.py'),'--output',str(W/'literal_report.json')]);need(not r.stderr,'literal stderr')
need((W/'literal_report.json').read_bytes()==(P/'direct_report.json').read_bytes(),'literal result')
r=run('gap',['/opt/homebrew/bin/gap','-q','-b',str(P/'gap_boundaries.g')]);need(not r.stderr and r.stdout== (P/'gap.stdout').read_bytes(),'GAP exact replay')
report=json.loads((W/'literal_report.json').read_text());lines=r.stdout.decode().replace('\r','').splitlines();computed=[]
for row in report['a11']:computed.append('A11|%d|%s|1'%(row['source_index'],str(row['reverse']).lower()))
for row in report['s8']:computed.append('S8|%d|%d|%s'%(row['source_index'],row['omitted'],str(sorted(map(len,row['orbits'])))))
for row in report['small']:computed.append('SMALL|%d|%s'%(row['source_index'],str([sorted(map(len,o)) for o in row['omission_orbits']])))
need([x.replace(' ','') for x in lines[:-1]]==[x.replace(' ','') for x in computed],'GAP versus literal')
sys.path.insert(0,str(P));from permutation_library import centralizer_fixing
# Independent brute force centralizer control, including disconnected and fixed-point actions.
small=[]
for n,cycles in [(3,[(0,1)]),(4,[(0,1),(2,3)]),(5,[(0,1),(1,2)]),(6,[(0,1),(1,2),(3,4)]),(7,[(0,1),(2,3),(4,5)])]:
    marks=[]
    for a,b in cycles:
        p=list(range(n));p[a],p[b]=b,a;marks.append(tuple(p))
    brute={t for t in itertools.permutations(range(n)) if all(all(t[p[x]]==p[t[x]] for x in range(n)) for p in marks)}
    got={t[:-1] for t in centralizer_fixing([p+(n,) for p in marks],n)}
    need(brute==got,'unrestricted centralizer control')
    small.append({'n':n,'centralizer_order':len(got)})
controls=[]
for name,edit in [('missing',lambda d:d['a11_rank_six'].pop()),('duplicate_index',lambda d:d['a11_rank_six'][1].__setitem__('source_index',0)),('bad_permutation',lambda d:d['s8_rank_six'][0]['permutations'][0].__setitem__(0,99)),('outer_replaced_by_standard',lambda d:d['small_extremal'].__setitem__(2,copy.deepcopy(d['small_extremal'][1])))]:
    bad=copy.deepcopy(data);edit(bad);save(name+'.json',bad);out=W/(name+'_report.json')
    run('bad_'+name,[sys.executable,str(P/'check_boundaries.py'),'--input',str(W/(name+'.json')),'--output',str(out)],False);need(not out.exists(),'invalid output accepted');controls.append(name)
for name,cmd,env in [('optflag',[sys.executable,'-O',str(P/'check_boundaries.py'),'--output',str(W/'bad_opt1.json')],None),('optenv',[sys.executable,str(P/'check_boundaries.py'),'--output',str(W/'bad_opt2.json')],dict(os.environ,PYTHONOPTIMIZE='1'))]:
    run(name,cmd,False,env);need(not Path(cmd[-1]).exists(),'optimized output');controls.append(name)
for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(W),str(P/'initial_fracture.tex')])
pdf=W/'initial_fracture.pdf';need(len(PdfReader(pdf).pages)==3,'pages');need([p.extract_text() for p in PdfReader(pdf).pages]==[p.extract_text() for p in PdfReader(P/'initial_fracture.pdf').pages],'native text')
for i in range(1,4):run('page'+str(i),['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110',f'-dFirstPage={i}',f'-dLastPage={i}',f'-sOutputFile={W}/page{i}.png',str(pdf)])
for i in [9,10]:run('source'+str(i),['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110',f'-dFirstPage={i}',f'-dLastPage={i}',f'-sOutputFile={W}/source{i}.png',str(S/'sources/stability2024.pdf')])
save('independent_controls.json',{'centralizer_controls':small,'damaged_controls':controls,'source_arrays_identical':True,'GAP_literals_identical':True})
save('receipts.json',receipts);save('report.json',{'status':'PASS_BOUNDED_INITIAL_FRACTURE','exports':len(man['exports']),'dependencies':len(deps),'acquired_manifest_bindings':len(acq),'a11_tails':len(report['a11']),'s8_omissions':len(report['s8']),'small_extremal_tuples':len(report['small']),'independent_centralizer_controls':len(small),'negative_controls':len(controls),'native_pages':3,'whole_original_credit':0});print((W/'report.json').read_text())
