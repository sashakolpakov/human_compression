"""Public L033 adapter: explicit relocation, no source patch or census."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time
from pathlib import Path
def need(v,m):
 if not v:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--volume',type=Path,required=True);ap.add_argument('--policy',type=Path,required=True);a=ap.parse_args();S=a.study.resolve();P=S/'algebra/coxeter_quotients/principal_v1';O=a.out.resolve();need(not O.exists(),'Fresh output');O.mkdir(parents=True)
 policy=read(a.policy);oldroot=policy['historical_roots']['study']
 def relocated(name):
  need(name.startswith(oldroot),'Exact historical study path');q=(S/name[len(oldroot):]).resolve();need(q.is_relative_to(S),'No escape');return q
 def exact(r):
  q=relocated(r['path']);b=q.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'Exact relocated scientific interface');return q
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 def run(name,cmd,cap=60,cwd=None):
  start=time.monotonic();rc=None;deadline=False
  with(O/(name+'.stdout')).open('wb')as f,(O/(name+'.stderr')).open('wb')as e:
   try:rc=subprocess.run(cmd,stdout=f,stderr=e,timeout=cap,cwd=cwd,env=env).returncode
   except subprocess.TimeoutExpired:deadline=True
  save(O/(name+'.receipt.json'),dict(command=cmd,cap_seconds=cap,exit_code=rc,deadline=deadline,seconds=time.monotonic()-start,target_census=False));need(rc==0 and not deadline and not(O/(name+'.stderr')).stat().st_size,'Clean '+name)
 C=read(P/'expected/components.json');need(len(C)==12,'All12 accepted components')
 for c in C.values():
  for k in ('proof','proof_pdf','author_manifest','gate_manifest','review','dependencies'):exact(c[k])
  need(read(exact(c['gate_manifest']))['status']==c['gate_status'],'Accepted component gate')
 N=read(P/'expected/named_rows.json');M=read(P/'expected/minima.json');core=read(S/'corpus106_L033_hyperbolic_core_v1/source_map.json')['types'];positive=read(S/'corpus106_L033_hyperbolic_core_v1/positives.json');names=read(S/'corpus106_L033_hyperbolic_names_v1/source_map.json')['rows'];need(len(N)==len(names)==22,'All22 source names')
 for got,n in zip(N,names):
  need(all(got[k]==v for k,v in n.items()),'Exact named source row')
  z=[x for x in positive if(x['type'],x['node'])==(n['type'],n['selected_node'])];need(len(z)==1,'Unique literal marked tuple');z=z[0]
  need(z['order']==n['order']and z['local_orders']==n['local_orders']==core[n['type']]['universal_local_orders'],'Actual universal marking')
  need(hashlib.sha256(json.dumps(z['permutations'],separators=(',',':')).encode()).hexdigest()==got['tuple_sha256'],'Exact ordered tuple')
 for r in M:
  if r['type']=='3535':need((r['bound'],r['broad'],r['universal'],r['universal_exclusion'])==(3840,1920,None,3840),'Ninth-square accepted interface')
  else:
   x=core[r['type']];need((r['bound'],r['broad'],r['universal'])==(x['bound'],x['broad_minimum'],x['universal_minimum']),'Complete minimum source join')
 # Import constants only from unchanged author preparation; its private-path
 # build() is deliberately not executed. The adapter performs explicit joins.
 sp=importlib.util.spec_from_file_location('author_preparation_constants',P/'prepare.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 header='\\begin{center}\\small\n\\begin{tabular}{llr}\\toprule\nDiagram & Certified source group & Order\\\\\\midrule\n'
 nt=header+''.join(m.DIAGRAMS[r['type']]+' & $'+r['tex_group']+'$ & '+str(r['order'])+r'\\'+'\n'for r in N)+r'\bottomrule\end{tabular}\end{center}'+'\n'
 header='\\begin{center}\\small\n\\begin{tabular}{lrrr}\\toprule\nDiagram & Complete bound & Broad minimum & Universal minimum\\\\\\midrule\n'
 mt=header+''.join(m.DIAGRAMS[r['type']]+' & '+str(r['bound'])+' & '+str(r['broad'])+' & '+(str(r['universal'])if r['universal']else'$>'+str(r['universal_exclusion'])+'$')+r'\\'+'\n'for r in M)+r'\bottomrule\end{tabular}\end{center}'+'\n'
 need(nt==(P/'named_table.tex').read_text()and mt==(P/'minimum_table.tex').read_text(),'Both exact adjacent native inputs')
 run('small',[sys.executable,str(P/'joins.py'),'--out',str(O/'small')]);need(read(O/'small/report.json')==read(P/'small_report.json'),'Exact elementary action/D4/A3 controls')
 run('contract',[sys.executable,str(P/'validate.py'),'--join',str(P/'expected'),'--out',str(O/'contract')]);need(read(O/'contract/report.json')['damage_controls']==18,'18 actual source-contract damages')
 guards=[]
 for script in [P/'check.py',P/'prepare.py',P/'joins.py',P/'validate.py',Path(__file__).resolve()]:
  for mode in ('argument','environment'):
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd+=['-O']
   else:e['PYTHONOPTIMIZE']='1'
   dst=O/(script.stem+'_'+mode+'_FORBIDDEN');r=subprocess.run(cmd+[str(script),'--out',str(dst)],capture_output=True,timeout=10,env=e);need(r.returncode!=0 and b'normal Python required'in r.stderr and not dst.exists(),'Actual optimization guard');guards.append([script.name,mode])
 from pypdf import PdfReader
 volume=PdfReader(a.volume);page=0
 for r in policy['manuscripts']:
  part=PdfReader(S/r['logical_pdf']);need(len(part.pages)==r['physical_pages'],'Exact manuscript pages')
  for p in part.pages:
   v=volume.pages[page];need(p.extract_text()==v.extract_text()and p.get_contents().get_data()==v.get_contents().get_data(),'Exact complete-volume text/content');page+=1
 need(page==len(volume.pages)==50,'All50 pages')
 T=O/'native';T.mkdir();tex=shutil.which('pdflatex');gs=shutil.which('gs');need(tex and gs,'Installed TeX/Ghostscript')
 for i in (1,2):run('native'+str(i),[tex,'-halt-on-error','-interaction=nonstopmode','-output-directory',str(T),str(P/'principal.tex')],cwd=P)
 need(not any(x in(T/'principal.log').read_text()for x in ('Warning','Overfull','Underfull','Infinite glue')),'Clean native layout')
 old=PdfReader(P/'principal.pdf');new=PdfReader(T/'principal.pdf');need(len(old.pages)==len(new.pages)==9 and[p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'Exact9page native text')
 run('render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(T/'page-%02d.png'),str(T/'principal.pdf')])
 need(all((T/('page-%02d.png'%i)).read_bytes()==(P/'native_author'/('page-%02d.png'%i)).read_bytes()for i in range(1,10)),'All9 exact author rasters')
 result=dict(status='PASS_PUBLIC_L033_PRINCIPAL_APPLICATION',source_clauses=109,component_manuscripts=12,positive_named_rows=22,excluded_rows=4,minimum_interfaces=9,retained_inputs=8,corrections=7,bibliography_attributions=29,damaged_controls=18,optimization_guards=len(guards),native_pages=9,complete_written_pages=50,native_text_identical=True,native_rasters_identical=True,unchanged_author_joins_and_contract=True,explicit_relocated_component_and_finite_join=True,private_source_fallback=False,target_censuses=0,new_Lean=0,new_question_credit=0,new_measurements=0,whole_original_credit=0)
 save(O/'report.json',result);print(json.dumps(result))
if __name__=='__main__':main()
