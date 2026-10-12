"""Exact L025 publication payloads; no public writes or new measurements.
Mapping mechanics adapted from science61 with attribution in README.rst.
"""
from pathlib import Path
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
NATIVE='papers/recoveries/L025/v1'; SCIENCE='audit/recoveries/L025/v1'
SPECS=[('author','corpus106_L025_recovery','6d1c8b7cf3465831a8ec9d5c14cb858123f97e6f4d86a14bb5fe0883c616627c'),('odd_cycle_review','corpus106_L025_even_extremality_independent_review','27a89199a058adc6fb59f0b769ce545e8301ef3e78eed77e2ee9607df0a234ea'),('independent_review','corpus106_L025_independent_review','498b27d81a3191e38c6044aea2beaee53398c809ee1e68f1a6d990a0b807f533'),('root_adoption','corpus106_L025_complete_root_adoption','a0ff396e9b64f229c758d8341e4085efd252bd3718ad5e98eff4590eab7970a8')]
NATIVES=[('L025_application','cycles_in_incidence_graphs','cycles_in_incidence_graphs',7,'Complete corrected principal application'),('L025_common','retained/common/cages_and_planes','common/cages_and_planes',5,'Whole acquired L013 common theory'),('L025_odd_cycle','retained/odd_cycle/odd_cycle_bound','odd_cycle/odd_cycle_bound',3,'Whole odd-cycle extremality companion')]
def bind(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 if (HERE/'manifest.json').exists():raise ValueError('Immutable proposal')
 files=[];packets=[];native={src+ext:NATIVE+'/'+dest+ext for _,src,dest,_,_ in NATIVES for ext in ['.tex','.pdf']}
 for key,directory,pin in SPECS:
  d=a.study/directory; public=SCIENCE+'/'+key; manifest=bind(d/'manifest.json',public+'/manifest.json')
  if manifest['sha256']!=pin:raise ValueError('Scientific pin '+key)
  m=json.loads((d/'manifest.json').read_text());packets.append(dict(id=key,study_directory=directory,manifest=manifest,exports=len(m['exports'])))
  for e in [bind(d/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path']
   if bind(d/logical,logical)!=e:raise ValueError('Frozen payload '+logical)
   dest=native[logical] if key=='author' and logical in native else public+'/'+logical
   if dest.endswith('.md'):dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dest,bytes=e['bytes'],sha256=e['sha256']))
 if len(files)!=78 or len({r['public_path'] for r in files})!=78:raise ValueError('Whole four-packet routing')
 write('payload_routes.json',dict(status='EXACT_ACCEPTED_SCIENCE_MAPPING',packets=packets,files=files,primary_source_exported=False))
 docs=[]
 for identity,src,dest,pages,role in NATIVES:
  text=(a.study/SPECS[0][1]/(src+'.tex')).read_text();title=re.search(r'\\title\{([^{}]+)\}',text).group(1)
  docs.append(dict(id=identity,title=title,tex=NATIVE+'/'+dest+'.tex',pdf=NATIVE+'/'+dest+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=pages,role=role,source_ids=['L025'],measured=False,compression_factor=None,externaldocument_dependency=None))
 write('native_catalogue_draft.json',dict(new_documents=docs,complete_scientific_pages=15,all_whole_papers_paid=True))
 inventory=json.loads((a.study/SPECS[0][1]/'program_roles.json').read_text())
 roles={}
 for field,role in [('required_mathematical_programs','REQUIRED_MATHEMATICAL_PROGRAM'),('required_mathematical_inputs','REQUIRED_MATHEMATICAL_DATA'),('optional_existing_programs','OPTIONAL_VALIDATION'),('optional_retained_common_checks','OPTIONAL_VALIDATION'),('operational_only','OPERATIONAL_DRIVER')]:
  for n in inventory[field]:roles[n]=role
 roles[inventory['existing_partial_formal_file']]='RETAINED_PARTIAL_FORMAL'
 whole=[]
 for r in files:
  if r['packet']!='author':continue
  n=r['logical_path'];role=roles.get(n)
  if not role and (n.startswith('reports/') or n in ['retained/common/author_replay.json','retained/common/optional_examples.json','retained/odd_cycle/author_replay.json','retained/odd_cycle/optional_report.json'] or n.startswith('retained/suzuki/') and Path(n).suffix in ['.json','.log']):role='RETAINED_OR_GENERATED_EVIDENCE'
  if role:whole.append(dict(r,role=role,complete_file=True))
 if not {r['logical_path'] for r in files if r['packet']=='author' and Path(r['logical_path']).suffix in ['.py','.g','.lean']}<={r['logical_path'] for r in whole}:raise ValueError('executable/formal omission')
 write('whole_file_roles_draft.json',dict(whole_files=whole,required_mathematical_programs=[r for r in whole if r['role']=='REQUIRED_MATHEMATICAL_PROGRAM'],required_mathematical_data=[r for r in whole if r['role']=='REQUIRED_MATHEMATICAL_DATA'],optional_validation=[r for r in whole if r['role']=='OPTIONAL_VALIDATION'],operational_drivers=[r for r in whole if r['role']=='OPERATIONAL_DRIVER'],formal_files=[r for r in whole if r['role']=='RETAINED_PARTIAL_FORMAL'],source_executable_listing_pages=[7,15],source_software_cost=None,external_proof_cost=None,external_runtime_cost=None,software_inclusive_factor=None,measurement=None,unknown_not_zero=True,validation_symmetry='No measurement. Future source listings and replacement programs require matched treatment; required programs and data stay explicit proof premises.',archival_proof_prose='Previous Suzuki own proof/audit prose already travels as exact .rst archival copies; no third-party primary text is exported. Complete native current proof remains in the parent.',retained_censuses=['four (5,5)-cages of order30','F012 n(4,6,18)>=32'],all_author_exports_mapped=True))
 print(json.dumps(dict(files=len(files),packets=len(packets),native_pages=[7,5,3],whole_inventory=len(whole),required_programs=2,required_data=6,public_files_written=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);main(p.parse_args())
