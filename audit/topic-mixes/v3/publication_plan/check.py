#!/usr/bin/env python3
"""Bounded publication assembly replay, with no mathematical code execution."""
from pathlib import Path
import argparse,ast,copy,hashlib,json,re,shutil,subprocess,sys
from pypdf import PdfReader
R=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bound(r,root,key='path'):
 p=Path(r[key]);need(not p.is_absolute()and'..'not in p.parts,'safe path');b=(root/p).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'exact binding '+str(p));return b
def validate(m,stage,public):
 need(m['source_ids']==['F005','L016','F007']and m['new_original_proposed']=='F007'and m['original_count']==3,'only F007 is new original')
 need(m['source_scope']=={'F005':35,'L016':19,'F007_numbered':48,'F007_additional':6},'exact source dispositions')
 need((m['common_pages'],m['application_pages'],m['printed_inventory_pages'])==(13,27,12),'complete common/app/code pages')
 need(m['common_documents']==['U','U1','U2']and m['application_documents']=={'F005':['A1','A2'],'L016':['A3'],'F007':['A4','A5']},'no free common or companions')
 need((m['required_programs'],m['optional_programs'],m['operational_drivers'],m['scoped_formal_files'],m['partial_declarations'])==(2,6,6,3,12),'exact software/formal roles')
 need(m['software_inclusive_factor']is None and m['historical_software_cost']is None and not m['full_Lean'],'no invented software or full formalization')
 need(m['whole_common_paid_once']and m['all_companions_charged']and m['no_cross_topic_discount']and not m['current_pointers_modified'],'full closure and no current mutation')
 need(m['new_question_credit']==0 and m['new_formal_credit']==0,'no extra credits')
 need(len(m['new_copies'])==m['new_copy_count']==130 and len({r['public_path']for r in m['new_copies']})==130,'exact new130 exports')
 for q in m['new_copies']:bound(q,stage,'public_path')
 need(len(m['existing_payload_references'])==m['existing_payload_reference_count']==114,'all114 old payload references')
 for q in m['existing_payload_references']:bound(q,public);bound(q,stage)
 bound(m['existing_public_admission'],public);old=load(public/m['existing_public_admission']['path'])
 for q in old['artifacts']:bound(q,public)
 for q in old['accepted_packets']+old['retained_accepted_packets']:bound(q,public)
 for p in m['packets']:
  base=stage/p['public_directory'];bound({'path':'manifest.json',**p['manifest']},base);j=load(base/'manifest.json');need(len(j['exports'])==p['exports'],'whole frozen packet')
  for q in j['exports']:bound(q,base)
 bound(m['numerical_distinct_review'],stage)
 num=load(stage/'audit/topic-mixes/v3/measurement/packet/results.json');need(num['source_ids']==m['source_ids']and num['software_inclusive_factors']is None,'current three-source numbers')
 need(num['required_printed_coverage']['REQ']==num['required_files']and num['full_required_only_printed_representation']=='REQ','REQ includes both complete programs')
 need(len(m['raw_inventory'])==17 and len({q['public_path']for q in m['raw_inventory']})==17,'whole unique17 files')
 for q in m['raw_inventory']:bound(q,stage,'public_path')
 for q in m['PDF_routes']:
  if not q['external_primary']:bound(q,stage,'public_path')
 need(len(m['PDF_routes'])==15 and sum(q['pages']for q in m['PDF_routes'])==114,'whole input inventory without source copying')
 science=stage/'papers/topic-mixes/v3/faithfulness';scope=load(science/'formal_scope.json');need(scope['count']==6 and not scope['full_source_formalization'],'new six partial declarations')
 return {'new_copies':130,'existing_payload_references':114,'old_admission_artifacts':len(old['artifacts']),'whole_file_inventory':17}

def title(t):
 p=t.index('\\title{')+7;depth=1;i=p
 while depth:
  if t[i]=='{'and t[i-1]!='\\':depth+=1
  elif t[i]=='}'and t[i-1]!='\\':depth-=1
  i+=1
 return t[p:i-1]
def closures(stage):
 rows=load(R/'catalogue_rows.json')['entries'];results=[]
 need(len(rows)==12 and sum(q['physical_pages']for q in rows)==52,'twelve full documents52pages')
 for q in rows:
  main=stage/q['tex'];t=main.read_text();need(title(t)==q['title'],'literal title '+q['id']);base=main.parent;visited=set();programs=set()
  def visit(p):
   if p in visited:return
   visited.add(p);s=p.read_text()
   for x in re.findall(r'\\input\{([^}]+)\}',s):visit(base/(x if x.endswith('.tex')else x+'.tex'))
   for x in re.findall(r'\\VerbatimInput(?:\[[^]]*\])?\{([^}]+)\}',s):programs.add(base/x);need((base/x).is_file(),'whole raw listing exists')
  visit(main);paths={x.relative_to(stage).as_posix()for x in visited|programs};need(paths==set(q['tex_inputs'])|{q['tex']},'full tex and raw input closure '+q['id'])
  need(len(PdfReader(stage/q['pdf']).pages)==q['physical_pages'],'authoritative physical extent')
  results.append({'id':q['id'],'title':q['title'],'pages':q['physical_pages'],'role':q['catalogue_role'],'inputs':sorted(paths),'tex':q['tex'],'pdf':q['pdf']})
 need(sum(q['role']=='current'for q in results)==10,'ten current catalogue rows')
 return results

def render_documents(rows,stage,out,xe):
 out.mkdir();reports=[]
 for i,row in enumerate(rows):
  d=out/f'{i:02d}';d.mkdir();base=Path(row['tex']).parent
  for x in row['inputs']:
   dest=d/Path(x).relative_to(base);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(stage/x,dest)
  name=Path(row['tex']).name
  for j in range(2):
   p=subprocess.run([xe,'-interaction=nonstopmode','-halt-on-error',name],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(d/f'render{j}.txt').write_text(p.stdout);need(p.returncode==0,'fresh TeX render '+row['id'])
  log=(d/Path(name).with_suffix('.log')).read_text();bad=[x for x in log.splitlines()if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning|Font Warning',x)];need(not bad,'render diagnostics '+row['id']+str(bad))
  old=[p.extract_text()or''for p in PdfReader(stage/row['pdf']).pages];new=[p.extract_text()or''for p in PdfReader(d/Path(name).with_suffix('.pdf')).pages];need(old==new,'all exact page text '+row['id']);reports.append({'id':row['id'],'pages':len(new),'all_page_text_equal':True,'diagnostics':[]})
 return reports

def controls(m,stage,public):
 tests=[('omit whole old common',lambda q:q.update(common_pages=8)),('omit F005 companion',lambda q:q['application_documents']['F005'].pop()),('omit F007 companion',lambda q:q['application_documents']['F007'].pop()),('required becomes optional',lambda q:q.update(required_programs=1,optional_programs=7)),('drop old exact payload',lambda q:q['existing_payload_references'].pop()),('drop new export',lambda q:q['new_copies'].pop()),('invent source software zero',lambda q:q.update(historical_software_cost=0)),('invent full formalization',lambda q:q.update(full_Lean=True)),('double original credit',lambda q:q.update(new_original_proposed='F005')),('alter whole program binding',lambda q:q['raw_inventory'][0].update(sha256='0'*64))];passed=[]
 for name,fn in tests:
  c=copy.deepcopy(m);fn(c)
  try:validate(c,stage,public)
  except (ValueError,KeyError):passed.append(name);continue
  raise ValueError('unrejected '+name)
 return passed

def main():
 a=argparse.ArgumentParser();a.add_argument('--stage-root',type=Path,required=True);a.add_argument('--public-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');x=a.parse_args();need(not x.out.exists(),'fresh output');x.out.mkdir(parents=True)
 if(R/'manifest.json').exists():
  for q in load(R/'manifest.json')['exports']:bound(q,R)
 m=load(R/'assembly_map.json');report=validate(m,x.stage_root,x.public_root);rows=closures(x.stage_root)
 for q in load(R/'guide_bindings.json')['files']:bound(q,x.stage_root)
 baseline=load(R/'public_baseline.json');current={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((x.public_root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(baseline['nonmain_count']==110 and all(current.get(k)==v for k,v in baseline['nonmain_functions'].items()),'all110 prior functions unchanged')
 nums=x.stage_root/'audit/topic-mixes/v3/measurement/packet';cmd=[sys.executable,'-B','-O',str(nums/'check.py'),'--out',str(x.out/'numbers')]
 if x.render:cmd+=['--render','--xelatex',x.xelatex]
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(x.out/'numbers.log').write_text(p.stdout);need(p.returncode==0,'portable numerical child replay '+p.stdout[-1000:]);n=load(x.out/'numbers/report.json');need(n['exact_fractions']==120 and n['actual_SVG_bars']==16,'current numeric assertions')
 rendered=render_documents(rows,x.stage_root,x.out/'renders',x.xelatex)if x.render else None
 report.update(status='PASS_PRIVATE_MIX3_ASSEMBLY_NOT_PUBLIC_ADMISSION',source_ids=m['source_ids'],proposed_new_original='F007',catalogue=rows,current_catalogue_rows=10,historical_inventory_rows=2,science_pages=40,printed_inventory_pages=12,required_programs=2,optional_programs=6,operational_drivers=6,partial_formal_files=3,partial_declarations=12,numerical_fractions=120,unchanged_input_cells=620,actual_SVG_PDF_bars=16,prior_nonmain_functions_unchanged=110,controls=controls(m,x.stage_root,x.public_root),renders=rendered,scientific_GAP_Lean_not_rerun=True,primary_sources_not_copied=True,public_current_pointers_not_modified=True,software_inclusive_factor=None)
 (x.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
