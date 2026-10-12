"""Operational replay: literal certificates by default; --enumerate reruns exact CP-SAT."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys,tempfile,time
from finite_certificate import verify,load
from direct_graphs import need
HERE=Path(__file__).resolve().parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def bindings(root):
 m=load(root/'manifest.json')
 for r in m['exports']:
  p=root/r['path'];need(p.is_file() and p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'binding '+r['path'])
 return len(m['exports'])
def scope_check(root):
 s=load(root/'scope.json');need(s['complete_original_admission'] is False and s['new_question_credit']==0 and s['new_Lean_declarations']==0,'no whole-source credit')
 need(s['complete_census_degrees']==[3,4,5] and s['witness_only_degrees']==[6],'exact finite range')
 need(s['exhaustion_premise']=='Completed OR-Tools CP-SAT all-solutions run on the entire specified Boolean model; no kernel-checked solver proof.','explicit solver trust')
 inv=load(root/'program_data_inventory.json');expected={'search.py':'REQUIRED_FINITE_ENUMERATION','direct_graphs.py':'REQUIRED_MATHEMATICAL_CHECKER','finite_certificate.py':'REQUIRED_MATHEMATICAL_CHECKER','check.py':'OPERATIONAL_REPLAY_DRIVER'}
 need({r['path']:r['role'] for r in inv['programs']}==expected,'whole program roles')
 expected_data={'k3_complete.json','k4_complete.json','k5_complete.json','k6_witnesses.json','inputs/n44_k6_g5_d4.g6','historical_graphs.json','figure1_edges.json'}
 need({r['path'] for r in inv['required_data']}==expected_data,'complete data boundary')
 for r in inv['programs']+inv['required_data']:
  need((root/r['path']).is_file(),'whole file presence')
 for k,stats in [(3,[6,9,6,17]),(4,[12,42,12,359]),(5,[20,130,20,3815])]:
  d=load(root/f'k{k}_complete.json');need(d['k']==k and list(d['model'].values())==stats,'exact model dimensions');need(d['seed']==0 and d['time_limit_seconds']==(90 if k==5 else 30),'declared run settings')
 return True

def controls(root,out):
 passed=[]
 def reject(name,file,mutation,kind='math'):
  with tempfile.TemporaryDirectory(prefix='L013-control-') as t:
   p=Path(t)
   for r in load(root/'manifest.json')['exports']:
    q=p/r['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/r['path'],q)
   shutil.copyfile(root/'manifest.json',p/'manifest.json')
   q=p/file
   if file.endswith('.json'):
    z=load(q);mutation(z);dump(q,z)
   else:q.write_bytes(mutation(q.read_bytes()))
   try:
    if kind=='bindings':bindings(p)
    elif kind=='scope':scope_check(p)
    elif kind=='report':need(verify(p)==load(p/'finite_report.json'),'exact derived report')
    else:verify(p)
   except (ValueError,KeyError,IndexError,FileNotFoundError) as e:passed.append(dict(name=name,rejection=str(e)));return
   raise ValueError('control accepted: '+name)
 reject('incomplete enumeration','k3_complete.json',lambda z:z.update(status='FEASIBLE'))
 reject('missing assignment','k3_complete.json',lambda z:z['labelled_graphs'].pop())
 reject('duplicate assignment','k3_complete.json',lambda z:z['labelled_graphs'].__setitem__(1,copy.deepcopy(z['labelled_graphs'][0])))
 reject('wrong automorphism order','k3_complete.json',lambda z:z['graphs'][0].update(automorphism_order=1))
 reject('nonbijective claimed generator','k3_complete.json',lambda z:z['graphs'][0]['automorphism_generators'][0].__setitem__(0,z['graphs'][0]['automorphism_generators'][0][1]))
 reject('wrong middle degree','k3_complete.json',lambda z:z['graphs'][0]['middle_edges'].pop())
 reject('assignment merged into wrong full class','k3_complete.json',lambda z:z['labelled_graphs'][0].update(full_graph_certificate=next(r['certificate'] for r in z['graphs'] if r['certificate']!=z['labelled_graphs'][0]['full_graph_certificate'])))
 reject('degree-six census overclaim','k6_witnesses.json',lambda z:z.update(status='COMPLETE_CENSUS'))
 reject('wrong historical order','historical_graphs.json',lambda z:z['graphs'][0].update(source_automorphism_order=1))
 reject('figure color exchanged','figure1_edges.json',lambda z:z.update(red_edges=z['green_edges']))
 reject('whole-source overclaim','scope.json',lambda z:z.update(complete_original_admission=True),'scope')
 reject('omitted whole data','program_data_inventory.json',lambda z:z['required_data'].pop(),'scope')
 reject('solver trust omitted','scope.json',lambda z:z.update(exhaustion_premise='Saved positive witnesses alone'),'scope')
 reject('model edge count changed','k3_complete.json',lambda z:z['model'].update(edge_variables=8),'scope')
 reject('same-size proof corruption','finite_cages.tex',lambda b:b.replace(b'Boolean',b'Booleam',1),'bindings')
 reject('changed chosen middle profile','finite_report.json',lambda z:z['censuses'][2]['graphs'][4]['chosen_middle_profile'].update(diameter=99),'report')
 dump(out/'controls.json',passed);return len(passed)

def main(a):
 a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic();n=bindings(HERE);scope_check(HERE)
 if a.study_root:
  r=load(HERE/'scope.json')['source'];p=a.study_root/r['path'];need(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'private primary binding')
 report=verify(HERE);need(report==load(HERE/'finite_report.json'),'exact saved mathematical report');dump(a.out/'finite_report.json',report)
 control_count=controls(HERE,a.out);fresh=[]
 if a.enumerate:
  for k in [3,4,5]:
   p=a.out/f'k{k}_fresh.json';cmd=[sys.executable,'-B','-O',str(HERE/'search.py'),'--k',str(k),'--seconds','90','--seed','0','--out',str(p)]
   run=subprocess.run(cmd,capture_output=True,text=True,timeout=120);(a.out/f'k{k}_fresh.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'solver process')
   old=load(HERE/f'k{k}_complete.json');new=load(p)
   need(new['status']=='OPTIMAL' and new['complete'],'fresh exhaustive completion')
   need(new['model']==old['model'],'fresh entire model')
   need(sorted(tuple(x['edge_indices']) for x in new['labelled_graphs'])==sorted(tuple(x['edge_indices']) for x in old['labelled_graphs']),'fresh complete assignment equality')
   need(new['automorphism_orders']==old['automorphism_orders'],'fresh class inventory')
   fresh.append(dict(k=k,status=new['status'],assignments=new['labelled_solutions'],classes=new['full_graph_classes']))
 rendered=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'render';d.mkdir(exist_ok=True);shutil.copyfile(HERE/'finite_cages.tex',d/'finite_cages.tex')
  for i in [0,1]:
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','finite_cages.tex'],cwd=d,capture_output=True,text=True);(d/f'pass{i}.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'native render')
  log=(d/'finite_cages.log').read_text();need(not any(x in log for x in ['Overfull','LaTeX Warning','! LaTeX Error']),'clean render')
  old=[p.extract_text() for p in PdfReader(HERE/'finite_cages.pdf').pages];new=[p.extract_text() for p in PdfReader(d/'finite_cages.pdf').pages];need(old==new and len(new)==4,'all four exact page texts');rendered=dict(pages=4,page_texts_exact=True,diagnostics=[])
 result=dict(status='PASS',bindings=n,complete_assignments=346,full_classes=13,witnesses=2,exact_historical_identifiers=6,figure_colors=2,controls=control_count,fresh_enumeration=fresh,render=rendered,scope='Bounded finite component only; absence requires completed full-model CP-SAT execution.',seconds=time.monotonic()-start)
 dump(a.out/'report.json',result);print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--enumerate',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
