from pathlib import Path
import hashlib,importlib.util,json,shutil,subprocess,sys
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_even_attachment_v1';W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
def need(x,m):
 if not x:raise RuntimeError(m)
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
records=S/'topic_B_L044_small_maxima_v1/author_validation/A10/records.g'
need(hashlib.sha256(records.read_bytes()).hexdigest()=='5676bc5f2f5bdaafbc8031cd0c1a35341c27773bb307d5be16395bb6c503f55f','actual acquired census')
inputs=json.loads((P/'a10_inputs.json').read_text());expected=[r['permutations'] for r in inputs['representatives']]
script='Read('+json.dumps(str(records))+');\nexpected:='+json.dumps(expected)+';;\nactual:=List(recordedMarks[5],r->List(recordedInvolutions{r},p->List([1..10],x->x^p)));;\nif actual<>expected then Error("literal census input differs");fi;\nPrint("PASS_LITERAL_COMPLETE_A10_INPUTS ",Length(actual),"\\n");QUIT;\n'
(W/'exact_inputs.g').write_text(script);r=subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(W/'exact_inputs.g')],capture_output=True,timeout=30);(W/'exact_inputs.stdout').write_bytes(r.stdout);(W/'exact_inputs.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr and b'PASS_LITERAL_COMPLETE_A10_INPUTS 10' in r.stdout,'literal original list')
spec=importlib.util.spec_from_file_location('permlib',P/'permutation_library.py');lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
primitive=S/'topic_B_L019_faithful_augmentation_v1/primitive_inputs.json';rows=json.loads(primitive.read_text())['representatives'];passed=[];tested=[]
for row in rows:
 marks=lib.parse_marks(row,row['n'],len(row['permutations']))
 for rev,t in enumerate([marks,marks[::-1]]):
  even=all((sum(x!=y for x,y in enumerate(p))//2)%2==0 for p in t)
  entry={'index':row['source_index'],'orientation':rev,'all_even':even,'anchors':[]}
  if even:
   tail=lib.closure(t[1:])
   for a in lib.anchors(t):
    other=next(x for x in range(row['n']) if x!=a)
    if {p[other] for p in tail}==set(range(row['n']))-{a}:
     entry['anchors'].append(a+1);g=lib.closure(t);need((row['n'],len(t),len(g),len(tail))==(6,3,60,10),'exact primitive exception');passed.append((row['source_index'],rev))
  tested.append(entry)
need(passed==[(0,1),(1,0),(1,1),(2,0)],'complete primitive even filter without character assumption')
put(W/'primitive_even_filter.json',{'tested':tested,'passed':passed,'character_condition_used':False})
N=W/'native';N.mkdir();shutil.copy2(P/'even_attachment.tex',N/'even_attachment.tex')
for i in range(2):
 r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','even_attachment.tex'],cwd=N,capture_output=True,timeout=30);(W/f'native{i}.stdout').write_bytes(r.stdout);(W/f'native{i}.stderr').write_bytes(r.stderr);need(r.returncode==0,'native build')
fresh=PdfReader(N/'even_attachment.pdf');old=PdfReader(P/'even_attachment.pdf');need([p.extract_text() for p in fresh.pages]==[p.extract_text() for p in old.pages],'native text unchanged')
r=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','even_attachment.pdf'],cwd=N,capture_output=True,timeout=30);(W/'render.stdout').write_bytes(r.stdout);(W/'render.stderr').write_bytes(r.stderr);need(r.returncode==0,'native render')
put(W/'extra_report.json',{'status':'PASS_LITERAL_INPUT_AND_EVEN_FILTER','actual_census_tuples':10,'primitive_orientations':len(tested),'survivors':passed,'native_pages':len(fresh.pages),'native_text_identical':True})
print((W/'extra_report.json').read_text())
