"""Replay the retained M11 certificate and source joins; no target or GAP call."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,shutil,subprocess
from pypdf import PdfReader
H=Path(__file__).resolve().parent;P=H.parent
sys.path.insert(0,str(H))
import verify_graphs,verify_alias,source_tables,join,corrections

def need(b,m):
 if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def texts(p):return [page.extract_text() for page in PdfReader(p).pages]

def imports(data):
 rows=load(H/'imports.json')['imports']
 need(sorted(r['actual_class'] for r in rows)==[1,2,4,5,7,8,10,12,17,18,21,23,27,29,30,31,34,35,37,38],'exact structural import roster')
 for r in rows:
  for k in ['record','author','accepted_review']:need(pin(Path(r[k]['path']))==r[k],'exact structural import pin')
  author=Path(r['author']['path']);record=Path(r['record']['path']);manifest=load(author)
  expected=dict(r['record'],path=str(record.relative_to(author.parent)))
  need(expected in manifest['exports'],'literal structural record bound by accepted author')
  need(load(Path(r['accepted_review']['path']))['status'].startswith('ACCEPTED'),'accepted distinct structural review')
  content=load(record)
  if r['kind']=='small_structural':
   source=content['source'];gens=content['permutation_generators'];actual=source['actual_record'];source_row=source['row']
  elif r['kind']=='mathieu_stabilizer':
   chosen=[a for a in content if a['actual_record']==r['actual_class']];need(len(chosen)==1,'unique stabilizer import')
   source=chosen[0];gens=source['actual_generators'];actual=source['actual_record'];source_row=source['row']
  else:
   chosen=[a for a in content if a['source']['actual_record']==r['actual_class']];need(len(chosen)==1,'unique atom import')
   gens=chosen[0]['actual_generators'];source=chosen[0]['source'];actual=source['actual_record'];source_row=source['row']
  need(actual==r['actual_class'] and source_row==r['source_atlas_row'] and gens==data['subgroup_generators'][actual-1],'exact imported generator array')
 return len(rows)

def controls(data,result,source,alias):
 cases=[]
 def reject(name,value,verify,expected):
  try:verify(value)
  except ValueError as exc:need(expected in str(exc),'correct rejection '+name);cases.append(name)
  else:raise ValueError('Damaged certificate accepted: '+name)
 def graph(value):return verify_graphs.verify(data,value)
 bad=copy.deepcopy(result);bad['pair_orbits'][0]['pair_positions'].pop();reject('missing_pair',bad,graph,'pair class')
 bad=copy.deepcopy(result);bad['maximal_subgroups'][0]['elements'].pop();reject('wrong_maximal_set',bad,graph,'maximal conjugator')
 bad=copy.deepcopy(result);bad['graphs'][0]['intersection_elements'].pop();reject('wrong_intersection',bad,graph,'actual intersection')
 bad=copy.deepcopy(result);bad['graphs'][0]['adjacency'][0].pop();reject('missing_incidence',bad,graph,'intersection adjacency')
 bad=copy.deepcopy(result);bad['graphs'][0]['metrics']['girth']+=2;reject('wrong_girth',bad,graph,'metric checks')
 bad=copy.deepcopy(result);bad['graphs'][0]['designs'][0]['uniform_counts'][0]['lambda_value']+=1;reject('wrong_design_multiplicity',bad,graph,'design certificate')
 bad=copy.deepcopy(alias);bad['matrix_images'][1],bad['matrix_images'][2]=bad['matrix_images'][2],bad['matrix_images'][1];reject('wrong_matrix_transport',bad,verify_alias.verify,'multiplication table')
 bad=copy.deepcopy(source);bad['table4'][0]['lambda_value']+=1
 damaged=corrections.corrected(bad,result);need(damaged['status']=='PRINTED_ROW_DISCREPANCY' and not damaged['numeric_values_automatically_repaired'],'printed damage retained')
 return dict(rejected=cases,printed_design_damage_detected=True,printed_values_automatically_repaired=False)

def main(args):
 need(args.out.is_absolute() and not args.out.exists(),'fresh absolute output')
 deps=load(H/'dependencies.json')
 for row in deps:need(pin(Path(row['path']))==row,'exact dependency '+row['path'])
 receipt=load(P/'m11_graph_execution01/receipt.json')
 need(receipt['reason']=='completed' and receipt['returncode']==0 and receipt['child_reaped'] and receipt['final_request_unchanged'] and not receipt['final_binding_failures'] and not receipt['final_boundary_failures'] and receipt['final_bindings_checked']==31,'actual bounded acquisition')
 raw=(P/'m11_graph_execution01/stdout').read_bytes();need(hashlib.sha256(raw).hexdigest()==receipt['outputs'][0]['sha256'],'raw target bytes')
 need((P/'m11_graph_execution01/stderr').read_bytes()==b'','clean target stderr')
 data=load(P/'m11_graph_request02/inputs.json');result=json.loads(raw)
 need(result['input_sha256']==hashlib.sha256((P/'m11_graph_request02/inputs.json').read_bytes()).hexdigest(),'exact acquired input')
 imported=imports(data);literal=verify_graphs.verify(data,result)
 source,_=source_tables.extract();need(source==load(H/'printed.json'),'all literal source rows')
 original=join.compare(source,result);need(original==load(H/'source_join01.json'),'original failed literal comparison retained')
 revised=corrections.corrected(source,result);need(revised==load(H/'source_join_corrected.json') and revised['status']=='ALL_PRINTED_ROWS_MATCH','exact explicit corrected comparison')
 need(original['source_rows_with_no_candidate']==[12,18,23,35],'precise four orientation discrepancies')
 alias=load(H/'gl23.stdout');alias_result=verify_alias.verify(alias)
 damage=controls(data,result,source,alias)
 guards=[]
 for flag in ['-O','-OO']:
  proc=subprocess.run([sys.executable,flag,str(H/'verify_alias.py')],capture_output=True,timeout=5)
  need(proc.returncode!=0 and b'Ordinary Python required' in proc.stderr,'ordinary mode guard');guards.append(flag)
 args.out.mkdir();save(args.out/'literal.json',literal);save(args.out/'joins.json',revised);save(args.out/'alias.json',alias_result);save(args.out/'controls.json',damage)
 native=[]
 if args.render:
  for name in ['method.tex','tables.tex']:shutil.copyfile(H/name,args.out/name)
  for i in [1,2]:
   proc=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','method.tex'],cwd=args.out,capture_output=True,timeout=30)
   (args.out/f'tex{i}.stdout').write_bytes(proc.stdout);(args.out/f'tex{i}.stderr').write_bytes(proc.stderr);need(proc.returncode==0,'native proof build')
  need('Overfull' not in (args.out/'method.log').read_text(),'proof layout')
  need(texts(args.out/'method.pdf')==texts(H/'method.pdf'),'exact fresh proof text')
  proc=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=proof-%02d.png','method.pdf'],cwd=args.out,capture_output=True,timeout=30)
  need(proc.returncode==0,'native proof pages')
  for i in range(1,len(texts(H/'method.pdf'))+1):
   name=f'proof-{i:02d}.png';need((args.out/name).read_bytes()==(H/name).read_bytes(),'exact native proof raster');native.append(name)
 report=dict(status='PASS_L036_M11_GRAPHS_AND_SOURCE_CORRECTIONS',dependencies=len(deps),structural_imports=imported,literal=literal,source_geometry_rows=37,source_design_rows=70,type_diameter_corrections=[12,18,23,35],unchanged_design_parameters=70,ambiguous_source_profiles=[[10,11],[16,17]],alias=alias_result,controls=damage,optimization_guards=guards,native_pages=native,target_reexecuted=False,whole_source_accepted=False)
 save(args.out/'report.json',report);print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--render',action='store_true');main(p.parse_args())
