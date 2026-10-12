#!/usr/bin/env python3
"""Copy the exact proposed LCD payloads to a fresh private staging directory."""
import argparse,ast,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def safe(name):
 p=Path(name);need(not p.is_absolute()and '..'not in p.parts,'safe relative route');return p
def pincheck(path,row):need(path.is_file()and path.stat().st_size==row['bytes']and sha(path)==row['sha256'],'exact artifact '+str(path))
def validate(plan,catalogue,raw):
 need(plan['source_ids']==['L050','F017']and plan['source_count']==2,'two exact originals')
 need(plan['whole_common_pages']==14 and plan['complete_application_pages']==27 and plan['scientific_pages']==41,'whole science paid')
 need(plan['whole_common_paid_once']and plan['no_cross_topic_discount'],'full common acquisition')
 need(plan['scope']['required_whole_files']==83 and plan['scope']['unique_partial_Lean_declarations']==9 and plan['scope']['full_Lean']is False,'actual file/formal scope')
 need(plan['scope']['source_software']is None and plan['scope']['software_inclusive_factor']is None,'unknown software')
 need(plan['scope']['L050_rows']==54 and plan['scope']['F017_rows']==104 and plan['scope']['unresolved_questions_retained'],'corrected contract boundary')
 need(any(x['role']=='distinct_numerical_review'for x in plan['packets'])and any(x['role']=='root_numerical_adoption'for x in plan['packets']),'accepted numerical chain')
 rows=catalogue['entries'];need(len(rows)==3 and[r['physical_pages']for r in rows]==[14,15,12]and[r['compiler']for r in rows]==['pdflatex','pdflatex','xelatex'],'complete entries/compiler provenance')
 for r in rows:
  need(len(r['raw_program_inputs'])==22 and len(r['required_data_inputs'])==61 and len(r['optional_validation_inputs'])==3 and len(r['operational_driver_inputs'])==11 and len(r['partial_formal_inputs'])==5,'explicit complete topic-wide raw routes')
 need(rows[1]['source_contracts']==['L050']and rows[2]['source_contracts']==['F017'],'source routes')
 need(len(raw['files'])==102 and sum(len(x['occurrences'])for x in raw['files'])==127 and sum(x['bytes']for x in raw['files'])==548250,'whole data/software boundary')
 routes={r['public_path']:r for r in plan['new_copies']};need(len(routes)==len(plan['new_copies']),'unique public routes')
 for x in raw['files']:
  need(x['whole_file'],'no pruning')
  for occ in x['occurrences']:
   y=routes[occ['public_path']];need(y['sha256']==x['sha256']and y['bytes']==x['bytes'],'whole occurrence binding')
 return routes

def controls(plan,catalogue,raw):
 import copy
 out=[]
 edits=[('drop whole common',lambda p,c,r:p.update(whole_common_pages=0)),('missing complete application',lambda p,c,r:c['entries'].pop()),('misroute source',lambda p,c,r:c['entries'][1].update(source_contracts=['F017'])),('change authoritative compiler',lambda p,c,r:c['entries'][0].update(compiler='xelatex')),('missing full required occurrence',lambda p,c,r:r['files'][0]['occurrences'].pop()),('prune whole file',lambda p,c,r:r['files'][0].update(whole_file=False)),('software unknown zero',lambda p,c,r:p['scope'].update(source_software=0)),('full Lean overclaim',lambda p,c,r:p['scope'].update(full_Lean=True)),('duplicate new original',lambda p,c,r:p['source_ids'].append('L050')),('old source question claimed solved',lambda p,c,r:p['scope'].update(unresolved_questions_retained=False))]
 for name,fn in edits:
  p,c,r=copy.deepcopy((plan,catalogue,raw));fn(p,c,r)
  try:validate(p,c,r)
  except (ValueError,KeyError,IndexError):out.append(name)
  else:raise ValueError('mutation survived '+name)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();out=a.out.resolve();need(not out.exists(),'fresh private stage')
 pub=a.public_root.resolve();need(out!=pub and pub not in out.parents,'never stage in public tree');out.mkdir(parents=True)
 
 if (HERE/'manifest.json').is_file():
  for e in load(HERE/'manifest.json')['exports']:pincheck(HERE/safe(e['path']),e)
 plan=load(HERE/'assembly_map.json');cat=load(HERE/'catalogue_rows.json');raw=load(HERE/'raw_routes.json');routes=validate(plan,cat,raw)
 base=load(HERE/'public_baseline.json');actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((pub/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(all(actual[k]==v for k,v in base['nonmain_verifier_ASTs'].items()),'all prior verifier functions unchanged')
 for row in plan['new_copies']:
  src=a.study_root/safe(row['study_path']);pincheck(src,row);dest=out/safe(row['public_path']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest);pincheck(dest,row)
 for packet in plan['packets']:
  root=out/safe(packet['public_directory']);m=load(root/'manifest.json');pincheck(root/'manifest.json',packet['manifest'])
  need(len(m['exports'])==packet['exports'],'manifest extent')
  for x in m['exports']:pincheck(root/safe(x['path']),x)
 for x in cat['entries']:
  tex=(out/x['tex']).read_text();need(re.search(r'\\title\{([^{}]+)\}',tex).group(1)==x['title'],'literal title')
  seen=set();todo=[x['tex']]
  while todo:
   name=todo.pop()
   if name in seen:continue
   seen.add(name);tx=re.sub(r'(?<!\\)%[^\n]*','',(out/name).read_text())
   for f in re.findall(r'\\(?:input|include)\{([^{}]+)\}',tx):todo.append(str(Path(x['tex']).parent/(f if Path(f).suffix else f+'.tex')))
  need(seen=={x['tex'],*x['tex_inputs']},'complete TeX closure')
 (out/'scripts').mkdir();shutil.copy2(HERE/'build_papers.py',out/'scripts/build_papers.py');(out/'papers/catalogue.json').write_text(json.dumps({'papers':cat['entries'],'new_editions':[]},indent=2)+'\n')
 report=dict(status='PASS_PRIVATE_LCD_ASSEMBLY_WITH_ACCEPTED_NUMERICAL_CHAIN',copied_routes=len(routes),frozen_packets=len(plan['packets']),literal_titles=3,scientific_pages=41,whole_raw_files=102,whole_raw_occurrences=127,prior_nonmain_functions_preserved=len(base['nonmain_verifier_ASTs']),controls=controls(plan,cat,raw),large_enumerations_repeated=False,public_tree_mutated=False,numerical_review_bound=True)
 if a.render:
  cmd=[sys.executable,'-B','-O',str(out/'scripts/build_papers.py'),'--output-dir',str(out/'render'),'--jobs','2']
  for x in cat['entries']:cmd+=['--paper',x['id']]
  run=subprocess.run(cmd,capture_output=True,text=True);(out/'catalogue_render.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'fresh catalogue build; inspect log')
  build=load(out/'render/report.json');from pypdf import PdfReader
  checks=[]
  for x,y in zip(cat['entries'],build['papers']):
   need(y['diagnostics']==[]and y['compiler']==x['compiler'],'clean exact compiler build')
   fresh=PdfReader(out/'render'/x['id']/'paper.pdf');old=PdfReader(out/x['pdf']);ft=[p.extract_text()or''for p in fresh.pages];ot=[p.extract_text()or''for p in old.pages]
   need(len(ft)==x['physical_pages']and ft==ot,'authoritative full page texts '+x['id'])
   checks.append(dict(id=x['id'],compiler=x['compiler'],pages=len(ft),exact_page_text=True,diagnostics=[]))
  report['render']=checks
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
