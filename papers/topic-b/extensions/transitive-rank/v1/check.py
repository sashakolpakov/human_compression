#!/usr/bin/env python3
"""Portable L047 author replay. Completeness rests on the written reductions.
No source target theorem is imported, and no full Lean proof is asserted.
"""
import argparse, copy, hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
PROGRAMS={'small_extremal':'PASS_EXTREMAL_S5_S6','small_transitive':'PASS_SMALL_TRANSITIVE_IMPRIMITIVE','primitive_bounds':'PASS_PRIMITIVE_BOUNDS','primitive_markings':'PASS_PRIMITIVE_MARKINGS'}
EXPECTED_POSITIVE={'small_transitive':{(6,9):1,(6,11):12,(8,45):1},'primitive_markings':{(6,1):3,(6,2):8,(10,5):1}}
TYPES={'small_transitive':{(6,9):{(3,2,3)},(6,11):{(2,3,3),(3,3,2),(2,3,4),(4,3,2),(2,4,3),(3,4,2)},(8,45):{(3,4,4,3)}},'primitive_markings':{(6,1):{(3,5),(5,3),(5,5)},(6,2):{(3,3,3),(4,5),(5,4),(4,6),(6,4),(5,6),(6,5),(6,6)},(10,5):{(3,3,3,3)}}}
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def record(p):b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def load(n):return json.loads((ROOT/n).read_text())
def check_file(p,row):need(record(p)=={k:row[k] for k in ['bytes','sha256']},f'changed binding: {p}')
def scope_guard(s,m):
 need(s['source_ids']==['L047'] and s['principal_source_contracts']==1,'source boundary')
 need(s['full_IP_required'] and s['new_sharp_rank_induction_decreases_degree'] and s['quotient_images_not_assumed_IP'] is True,'hypothesis boundary')
 need(s['ordered_vs_unordered_distinction'],'ordered distinction')
 need(s['source_rows']==len(m['rows'])==58 and s['proof_context_count']==len(m['proof_contexts'])==12,'source map counts')
 need(s['new_required_program_count']==6 and s['all_declared_program_count']==10 and len(s['new_mathematical_programs'])==10,'whole program boundary')
 need(s['new_Lean_declarations']==0 and s['reused_partial_Lean_declarations']==14 and not s['full_source_formalization'],'formal boundary')
 need(all(s[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']) and not s['ratios_computed'],'credit boundary')
 need(s['full_external_costs'] is None and s['complete_software_inclusive_factor'] is None,'unknown retained costs')
 rows={x['id']:x for x in m['rows']}
 need(rows['Tab1.1']['status']=='corrected' and '[3,2,3]' in rows['Tab1.1']['claim'],'literal table correction')
 need('not a new' in rows['I3']['qualification'] or 'No new' in rows['I3']['qualification'],'question status')
 need(sum(x['status']=='attributed_ancillary_report_not_a_premise' for x in m['rows'])==23,'ancillary source claims')
 for x in m['rows']:need(all(n in {q['id'] for q in m['proof_contexts']} for n in x['proof_contexts']),'unbound proof context')
def compose(a,b):return tuple(b[i] for i in a)
def order(a):
 seen=set();o=1
 import math
 for i in range(len(a)):
  if i in seen:continue
  j=i;l=0
  while j not in seen:seen.add(j);l+=1;j=a[j]
  o=math.lcm(o,l)
 return o
def closure(gs,n):
 e=tuple(range(n));out={e};todo=[e]
 for a in todo:
  for b in gs:
   c=compose(a,b)
   if c not in out:out.add(c);todo.append(c)
 return out
def marking_check(n,types,perms,expected_order=None):
 gs=[tuple(x-1 for x in p) for p in perms];e=tuple(range(n))
 need(all(sorted(g)==list(range(n)) and order(g)==2 for g in gs),'involution permutations')
 need([order(compose(a,b)) for a,b in zip(gs,gs[1:])]==types,'literal ordered types')
 need(all(compose(gs[i],gs[j])==compose(gs[j],gs[i]) for i in range(len(gs)) for j in range(i+2,len(gs))),'string commutation')
 sub={m:closure([g for i,g in enumerate(gs) if m>>i&1],n) for m in range(1<<len(gs))}
 need(all(sub[a]&sub[b]==sub[a&b] for a in sub for b in sub),'full subset IP')
 H=sub[(1<<len(gs))-1]
 if expected_order is not None:need(len(H)==expected_order,'generated order')
 need(len({g[0] for g in H})==n,'transitivity')
 return {'order':len(H),'rank':len(gs),'subset_pairs':len(sub)**2,'some_odd':any(sum(g[i]>g[j] for i in range(n) for j in range(i+1,n))%2 for g in gs)}
def parse(name,text,err):
 need(not err.strip() and 'Error,' not in text and text.count(PROGRAMS[name])==1,'incomplete GAP execution '+name)
 cases=[];sol=[];ext=[]
 for line in text.splitlines():
  if line.startswith('CASE '):
   m=re.search(r'n=(\d+) id=(\d+) order=(\d+).*complete_high_markings=(\d+)',line);need(m is not None,'case encoding');cases.append(tuple(map(int,m.groups())))
  if line.startswith('SOLUTION|'):
   _,n,i,t,p=line.split('|');sol.append({'n':int(n),'id':int(i),'types':json.loads(t),'permutations':json.loads(p)})
  if line.startswith('EXTREMAL|'):
   _,n,p=line.split('|');ext.append({'n':int(n),'permutations':json.loads(p)})
 if name in EXPECTED_POSITIVE:
  need({(n,i):c for n,i,o,c in cases if c}==EXPECTED_POSITIVE[name],'complete positive-case roster')
  need(len(cases)==len({(n,i) for n,i,o,c in cases}),'duplicate cases')
  for n,i,o,c in cases:
   ss=[x for x in sol if (x['n'],x['id'])==(n,i)];need(len(ss)==c,'literal tuple count')
   if c:need({tuple(x['types']) for x in ss}==TYPES[name][n,i],'complete type list')
  for x in sol:
   o=next(o for n,i,o,c in cases if (n,i)==(x['n'],x['id']));x['integer_permutation_check']=marking_check(x['n'],x['types'],x['permutations'],o)
  if name=='primitive_markings':need([(n,i) for n,i,o,c in cases]==[(6,1),(6,2),(7,5),(8,3),(8,5),(10,4),(10,5),(10,7),(12,2),(8,0),(6,0)],'primitive finite roster')
  if name=='primitive_markings':need(all(x['integer_permutation_check']['some_odd'] for x in sol if (x['n'],x['id']) in [(6,2),(10,5)]),'primitive parity exclusions')
  else:
   need({n for n,i,o,c in cases}=={6,8,9} and len(cases)==78,'small degree roster')
   need(all(x['integer_permutation_check']['some_odd'] for x in sol if x['n']==6),'alternating parity exclusions')
 elif name=='small_extremal':need([x['n'] for x in ext]==[5,6,6],'extremal complete list')
 else:
  screens=[l.split('|') for l in text.splitlines() if l.startswith('SCREEN|')]
  need(all(len(x)==6 for x in screens) and {int(x[1]) for x in screens}.issubset(set(range(2,26))),'primitive screen')
  need(sum(x[-1]=='complete_marking_census' for x in screens)==9,'residual screen count')
 return {'case_rows':cases,'literal_solutions':sol,'extremal_markings':ext}
def controls(s,m,results):
 rejected=[]
 changes=[('lost_IP','full_IP_required',False),('unordered_equals_ordered','ordered_vs_unordered_distinction',False),('same_degree_induction','new_sharp_rank_induction_decreases_degree',False),('quotient_assumed_IP','quotient_images_not_assumed_IP',False),('omit_required_file','new_required_program_count',5),('new_formal_credit','new_Lean_declarations',1),('invent_external_zero','full_external_costs',0),('new_question_credit','new_question_credit',1)]
 for label,key,value in changes:
  t=copy.deepcopy(s);t[key]=value
  try:scope_guard(t,m)
  except ValueError:rejected.append(label)
  else:raise ValueError('control accepted '+label)
 sol=results['small_transitive']['literal_solutions'][0]
 for label,types,perms in [('source_false_type',[2,3,3],sol['permutations']),('redundant_marking',sol['types'],[sol['permutations'][0]]*len(sol['permutations']))]:
  try:marking_check(sol['n'],types,perms)
  except ValueError:rejected.append(label)
  else:raise ValueError('finite control accepted '+label)
 return rejected

def audit(args):
 start=time.monotonic();out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
 if (ROOT/'manifest.json').exists():
  for row in load('manifest.json')['exports']:check_file(ROOT/row['path'],row)
 deps=load('dependencies.json')
 for row in deps['packets']:
  mf=ROOT/row['manifest'];check_file(mf,row);e={x['path']:x for x in json.loads(mf.read_text())['exports']}
  for name in row['copied_exports']:check_file(mf.parent/name,e[name])
 s=load('scope.json');m=load('source_map.json');scope_guard(s,m)
 for row in s['new_mathematical_programs']:check_file(ROOT/row['path'],row)
 for q in m['proof_contexts']:
  b=(ROOT/q['file']).read_text()[q['start_codepoint']:q['end_codepoint_exclusive']].encode();need(sha(b)==q['sha256_utf8'],'changed proof span')
 migration=load('finite_migration.json');body=(ROOT/migration['source']).read_text()[migration['start_codepoint']:migration['end_codepoint_exclusive']]
 need(body==(ROOT/migration['target']).read_text() and sha(body.encode())==migration['sha256_utf8'],'complete finite proof migration')
 if args.programs:
  for row in load('external_software.json')['files']:check_file(Path(row['path']),row)
 if args.study_root:
  for key in ['pdf','text']:check_file(args.study_root/m['source'][key]['path'],m['source'][key])
  text=(args.study_root/m['source']['text']['path']).read_text()
  for row in m['rows']:
   q=row['source_span'];need(sha(text[q['start_codepoint']:q['end_codepoint_exclusive']].encode())==q['sha256_utf8'],'source locator')
 results={};fresh=[]
 for name in PROGRAMS:
  if args.programs:
   proc=subprocess.run([args.gap,'-q','-b',name+'.g'],cwd=ROOT,text=True,capture_output=True,timeout=1800)
   (out/(name+'.stdout.log')).write_text(proc.stdout);(out/(name+'.stderr.log')).write_text(proc.stderr)
   need(proc.returncode==0,'GAP exit '+name);txt,err=proc.stdout,proc.stderr;fresh.append(name)
  else:txt=(ROOT/'author_programs'/f'{name}.stdout.log').read_text();err=(ROOT/'author_programs'/f'{name}.stderr.log').read_text()
  results[name]=parse(name,txt,err)
 finite=None
 if args.programs:
  proc=subprocess.run([sys.executable,'-B','-O',str(ROOT/'retained/finite_boundary/check.py'),'--out',str(out/'finite_boundary'),'--gap',args.gap],capture_output=True,text=True,timeout=1800)
  need(proc.returncode==0,'finite-boundary replay '+proc.stdout+proc.stderr);finite=json.loads((out/'finite_boundary/report.json').read_text());need(finite['normalized_markings']==59 and finite['transitive_completions']==154 and finite['independent_completions']==0,'finite lemma summary')
 render=[]
 if args.render:
  for name in ['string_rank_theory','transitive_string_groups','program-appendix']:
   dest=out/name;dest.mkdir();
   for passno in [1,2]:
    proc=subprocess.run([args.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(dest),name+'.tex'],cwd=ROOT,capture_output=True,text=True,timeout=120)
    (dest/f'pass{passno}.log').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'TeX failed '+name)
   log=(dest/(name+'.log')).read_text();need(not re.search(r'Overfull|Undefined control|undefined references|LaTeX Warning',log),'TeX diagnostics '+name)
   pdf=PdfReader(dest/(name+'.pdf'));old=PdfReader(ROOT/(name+'.pdf'))
   need([p.extract_text() for p in pdf.pages]==[p.extract_text() for p in old.pages],'rendered page text changed '+name)
   render.append({'document':name,'pages':len(pdf.pages),'exact_page_text':True})
 rejected=controls(s,m,results)
 (out/'finite_results.json').write_text(json.dumps(results,indent=2)+'\n')
 report={'status':'PASS_AUTHOR_PACKET_NOT_INDEPENDENT_ACCEPTANCE','source_rows':len(m['rows']),'proof_contexts':len(m['proof_contexts']),'new_programs_fresh':fresh,'bounded_root_lemma_fresh':finite is not None,'new_Lean_declarations':0,'inherited_Lean_reexecuted':False,'new_source_credit':0,'controls_rejected':rejected,'renders':render,'results_sha256':record(out/'finite_results.json')['sha256'],'elapsed_seconds':round(time.monotonic()-start,3)}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--study-root',type=Path);p.add_argument('--programs',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');print(json.dumps(audit(p.parse_args())))
