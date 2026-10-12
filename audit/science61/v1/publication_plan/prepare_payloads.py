"""Baseline-independent accepted L011 mapping; no public or programme writes."""
from pathlib import Path
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
NATIVE='papers/recoveries/L011/v1';SCIENCE='audit/recoveries/L011/v1'
SPECS=[('author','corpus106_L011_recovery_v2','4286c4a9a3a5ec1c3dfbab7e68e9a576648081288ebc9af8be938b8cd01d2ccb'),('root_review','corpus106_L011_root_review','f7226b58ddf934a114e79513c9ef99add8c75535cd6d1cdb67f0383ccdc4b1d2')]
NATIVES=[('L011_common','low_dimension_obstructions',4,'Whole common low-dimension obstruction proofs'),('L011_application','simple_group_application',4,'Whole simple-group application and complete finite-search proof')]
def bind(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 if (HERE/'manifest.json').exists():raise ValueError('Immutable proposal')
 files=[];packets=[];native_names={stem+ext for _,stem,_,_ in NATIVES for ext in ['.tex','.pdf']}
 for key,directory,pin in SPECS:
  d=a.study/directory;public=SCIENCE+'/'+key;manifest=bind(d/'manifest.json',public+'/manifest.json')
  if manifest['sha256']!=pin:raise ValueError('Scientific pin '+key)
  m=json.loads((d/'manifest.json').read_text());packets.append(dict(id=key,study_directory=directory,manifest=manifest,exports=len(m['exports'])))
  for e in [bind(d/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path']
   if bind(d/logical,logical)!=e:raise ValueError('Frozen payload '+logical)
   dest=NATIVE+'/'+Path(logical).name if key=='author' and logical in native_names else public+'/'+logical
   if dest.endswith('.md'):dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dest,bytes=e['bytes'],sha256=e['sha256']))
 if len(files)!=52 or len({r['public_path'] for r in files})!=52:raise ValueError('Whole two-packet routing')
 write('payload_routes.json',dict(status='EXACT_ACCEPTED_PAYLOAD_MAP_AWAITING_ACTUAL_SCIENCE60_BASELINE',packets=packets,files=files,primary_source_exported=False))
 rows=[]
 for identity,stem,pages,role in NATIVES:
  text=(a.study/SPECS[0][1]/(stem+'.tex')).read_text();title=re.search(r'\\title\{([^{}]+)\}',text).group(1)
  rows.append(dict(id=identity,title=title,tex=NATIVE+'/'+stem+'.tex',pdf=NATIVE+'/'+stem+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=pages,role=role,source_ids=['L011'],measured=False,compression_factor=None,externaldocument_dependency=None))
 write('native_catalogue_draft.json',dict(new_documents=rows,complete_scientific_pages=8,all_whole_papers_paid=True,current_public_admission=None))
 inventory=json.loads((a.study/SPECS[0][1]/'program_inventory.json').read_text());whole=[]
 for x in inventory['files']:
  r=next(r for r in files if r['packet']=='author' and r['logical_path']==x['path']);whole.append(dict(r,role=x['role'],complete_file=True))
 need_paths={r['logical_path'] for r in files if r['packet']=='author' and Path(r['logical_path']).suffix in ['.py','.g']}
 if not need_paths<={r['logical_path'] for r in whole}:raise ValueError('whole executable boundary')
 write('whole_file_roles_draft.json',dict(whole_files=whole,required_mathematical_programs=[r for r in whole if r['role']=='REQUIRED_MATHEMATICAL_PROGRAM'],required_mathematical_data=[],generated_receipts_are_not_independent_algorithm_inputs=True,formal_files=[],source_software_cost=None,external_runtime_cost=None,unknown_not_zero=True,software_inclusive_factor=None,measurement=None,validation_symmetry='No metric; future executable comparisons must be symmetric. The full three required programs remain prerequisites.',order_verification='All11 orders are freshly verified from generator-only groups; additive v2 eliminates supplied/cached sizes or chains. Exact accepted correction retained.'))
 print(json.dumps(dict(files=len(files),packets=len(packets),native_pages=[4,4],whole_inventory=len(whole),required_programs=3,baseline_bound=False,public_files_written=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);main(p.parse_args())
