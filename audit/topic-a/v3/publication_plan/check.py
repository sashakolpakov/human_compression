#!/usr/bin/env python3
"""Verify mapped copies and replay bounded accepted science/numerics, not GAP/Lean."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,subprocess,sys,importlib.util,re,ast
from pypdf import PdfReader
H=Path(__file__).resolve().parent
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012']
def need(x,m):
 if not x:raise ValueError(m)
def load(f):return json.loads(f.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bound(row,root,key='path'):
 p=Path(row[key]);need(not p.is_absolute()and'..'not in p.parts,'safe route');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p));return b
def validate(m,root,public):
 need(m['source_ids']==SOURCES and (m['common_pages'],m['application_pages'],m['program_pages'],m['source_rows'],m['proof_interfaces'])==(23,45,30,102,60),'complete scope')
 need(m['required_complete_program_data']==11 and m['unchanged_scoped_Lean_modules']==14,'program/formal scope')
 need(m['proposed_topic_change']==dict(before=19,after=18,new_originals=0,new_questions=0,new_formal_declarations=0,current_pointer_changed=False),'no registration credit/current change')
 need(len(m['files'])==m['file_count']==196 and len({x['public_path']for x in m['files']})==196,'exact unique export closure')
 for r in m['files']:bound(r,root,'public_path')
 for p in m['packets']:
  folder=root/p['public_directory'];j=load(folder/'manifest.json');need(len(j['exports'])==p['exports'],'packet exports');bound(dict(p['manifest'],path=p['public_directory']+'/manifest.json'),root)
  for r in j['exports']:bound(r,folder)
 for p in m['embedded_packet_aliases']:
  folder=root/p['public_directory'];bound(dict(p['manifest'],path=p['public_directory']+'/manifest.json'),root)
  for r in load(folder/'manifest.json')['exports']:bound(r,folder)
 for r in m['external_public_bindings']:bound(r,public)
 science=root/'papers/topic-a/v3';s=load(science/'scope.json');need(s['source_ids']==SOURCES and s['source_rows']==102 and s['inclusive_proof_interfaces']==60,'actual scientific contract')
 f=load(science/'formal_scope.json');need(f['module_count']==14 and f['new_declarations']==0 and not f['whole_volume_formalized']and not f['arbitrary_parabolic_theorem_formalized'],'actual partial formal scope')
 n=load(root/'audit/topic-a/v3/measurement/packet/results.json');need(n['source_ids']==SOURCES and n['software_inclusive_factors']is None and n['historical_source_software_cost']is None,'exact numeric/software scope')
 return s

def titles_and_inputs(root):
 rows=load(H/'catalogue_rows.json')['entries'];science=root/'papers/topic-a/v3';checks=[]
 def brace(t,start):
  pos=t.index('{',start);i=pos+1;depth=1
  while depth:
   if t[i]=='{'and t[i-1]!='\\':depth+=1
   if t[i]=='}'and t[i-1]!='\\':depth-=1
   i+=1
  return t[pos+1:i-1]
 for r in rows:
  t=(root/r['tex']).read_text();tag='\\title{'if'\\title{'in t else'\\section*{';need(brace(t,t.index(tag))==r['title'],'literal title');seen=set();code=set()
  def visit(p):
   if p in seen:return
   seen.add(p);text=(root/p).read_text()
   for q in re.findall(r'\\input\{([^}]+)\}',text):visit('papers/topic-a/v3/'+(q if q.endswith('.tex')else q+'.tex'))
   for q in re.findall(r'\\VerbatimInput(?:\[[^]]*\])?\{([^}]+)\}',text):code.add('papers/topic-a/v3/'+q);need((root/('papers/topic-a/v3/'+q)).is_file(),'whole programme input')
  visit(r['tex']);need(seen==set(r['tex_inputs'])|{r['tex']}and code==set(r['program_inputs']),'complete TeX/program input closure')
  count=len(PdfReader(root/r['pdf']).pages);need(count==r['physical_pages'],'PDF extent');checks.append(dict(id=r['id'],title=r['title'],pages=count,tex_files=len(seen),whole_program_inputs=len(code)))
 need(len(rows)==12 and sum(x['pages']for x in checks)==98,'all12/98pages');return checks

def execute(cmd,out):
 p=subprocess.run(cmd,capture_output=True,text=True);out.write_text(p.stdout+p.stderr);need(p.returncode==0,'child replay '+str(out)+': '+p.stdout[-1000:]+p.stderr[-1000:])
def recount(stage,public,sources,out):
 # Redirect only explicitly named frozen roots. Primary PDFs are user supplied.
 aliases={x['study_directory']:x['public_directory']for x in load(H/'assembly_map.json')['packets']+load(H/'assembly_map.json')['embedded_packet_aliases']}
 class Study:
  def __truediv__(self,path):
   p=Path(path);head=p.parts[0];tail=Path(*p.parts[1:])
   if head in aliases:return stage/aliases[head]/tail
   if head=='sources':return sources/p
   known={'embedded_validation_listing_audit':'audit/overview/v11/listing_audit','embedded_listing_root_review':'audit/overview/v11/listing_review'}
   need(head in known,'unmapped study dependency '+str(p));return public/known[head]/tail
 ip=stage/'audit/topic-a/v3/measurement/packet/inputs/input';spec=importlib.util.spec_from_file_location('unified_a_public_input',ip/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 from types import SimpleNamespace
 report=mod.replay(SimpleNamespace(study_root=Study(),public_root=public));out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');return dict(PDF_cells=600,raw_cells=300,controls=len(report['controls_rejected']),primary_root='User supplied, no source assets copied',adapter='Exact frozen replay function; only study-root path dispatch changes')

def controls(m,stage,public):
 rejected=[]
 edits=[('drop L012',lambda q:q['source_ids'].pop()),('free old common',lambda q:q.update(common_pages=0)),('drop entire export',lambda q:q['files'].pop()),('invent new source credit',lambda q:q['proposed_topic_change'].update(new_originals=1)),('inflate formal scope',lambda q:q.update(unchanged_scoped_Lean_modules=15)),('change preserved program hash',lambda q:next(r for r in q['files']if r['public_path'].endswith('phase250_fixed_groups.g')).update(sha256='0'*64))]
 for name,fn in edits:
  q=deepcopy(m);fn(q)
  try:validate(q,stage,public)
  except(ValueError,KeyError):rejected.append(name);continue
  raise ValueError('missed control '+name)
 return rejected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--recount',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for r in load(H/'manifest.json')['exports']:bound(r,H)
 m=load(H/'assembly_map.json');validate(m,a.stage_root,a.public_root);catalogue=titles_and_inputs(a.stage_root)
 for guide in load(H/'guide_bindings.json')['files']:bound(guide,a.stage_root)
 baseline=load(H/'public_baseline.json');current={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((a.public_root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(baseline['non_main_count']==110 and all(current.get(k)==v for k,v in baseline['non_main_functions'].items()),'all110 prior non-main verifier ASTs preserved')
 science=a.stage_root/'papers/topic-a/v3';cmd=[sys.executable,'-B','-O',str(science/'check.py'),'--out',str(a.out/'science'),'--public-root',str(a.public_root)]
 if a.render:cmd+=['--render','--xelatex',a.xelatex]
 execute(cmd,a.out/'science.log')
 nums=a.stage_root/'audit/topic-a/v3/measurement/packet';cmd=[sys.executable,'-B','-O',str(nums/'check.py'),'--out',str(a.out/'numbers')]
 if a.render:cmd+=['--render','--xelatex',a.xelatex]
 execute(cmd,a.out/'numbers.log');n=load(a.out/'numbers/report.json');need(n['exact_fractions']==270 and n['graphs']['SVG_bars']==27,'accepted arithmetic')
 rc=None
 if a.recount:need(a.sources_root is not None,'--sources-root required for actual primary recount');rc=recount(a.stage_root,a.public_root,a.sources_root,a.out/'recount.json')
 result=dict(status='PASS_PRIVATE_ASSEMBLY_REPLAY_NOT_PUBLIC_ADMISSION',exact_export_copies=196,packets=5,embedded_packets_reused=3,catalogue_rows=catalogue,source_ids=SOURCES,source_rows=102,proof_interfaces=60,science_pages=68,program_pages=30,required_complete_files=11,scoped_formal_files=14,new_formal_declarations=0,new_original_credit=0,software_inclusive_factor=None,arithmetic_fractions=270,graph_bars=27,controls=controls(m,a.stage_root,a.public_root),rendered=a.render,recount=rc,scientific_GAP_Lean_reexecuted=False,current_public_pointers_changed=False,baseline_nonmain_functions_unchanged=110)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
