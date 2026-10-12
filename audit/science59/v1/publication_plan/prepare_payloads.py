"""Map accepted L039 payloads privately; no public baseline or admission implied."""
from pathlib import Path
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
NATIVE='papers/recoveries/L039/v1';SCIENCE='audit/recoveries/L039/v1'
SPECS=[('author','corpus106_L039_full_recovery',SCIENCE+'/author','1da5d6e7297f1c6b41fc8d9f1b42d97b5e1b33679602a946f7cf697da8affa3c'),('root_review','corpus106_L039_full_root_review',SCIENCE+'/root_review','28e18a922e6b5bf05b79cfb356d1d7da534a89150557a79df3d47c84a9b5feee')]
NATIVES=[('L039_base','inputs/bounded_author/ree_involutions',3,'Complete prior companion: rank-three existence, rank bound and odd-quotient exclusions'),('L039_rank4','rank_four_replacement',7,'Complete rank-four replacement, auxiliary-claim correction and retained-input diagram')]
def bind(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 if (HERE/'manifest.json').exists():raise ValueError('Immutable proposal')
 files=[];packets=[];native_names={stem+ext for _,stem,_,_ in NATIVES for ext in ['.tex','.pdf']}
 for key,directory,public,pin in SPECS:
  d=a.study/directory;manifest=bind(d/'manifest.json',public+'/manifest.json')
  if manifest['sha256']!=pin:raise ValueError('Scientific pin '+key)
  m=json.loads((d/'manifest.json').read_text());packets.append(dict(id=key,study_directory=directory,manifest=manifest,exports=len(m['exports'])))
  for e in [bind(d/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path']
   if bind(d/logical,logical)!=e:raise ValueError('Frozen payload '+logical)
   dest=NATIVE+'/'+Path(logical).name if key=='author' and logical in native_names else public+'/'+logical
   if dest.endswith('.md'):dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dest,bytes=e['bytes'],sha256=e['sha256']))
 if len(files)!=40 or len({r['public_path'] for r in files})!=40:raise ValueError('Whole two-packet routing')
 write('payload_routes.json',dict(status='EXACT_ACCEPTED_PAYLOAD_MAP_PUBLIC_INTEGRATION_PENDING',packets=packets,files=files,primary_source_exported=False))
 rows=[]
 for identity,stem,pages,role in NATIVES:
  text=(a.study/SPECS[0][1]/(stem+'.tex')).read_text();title=re.search(r'\\title\{([^{}]+)\}',text).group(1)
  rows.append(dict(id=identity,title=title,tex=NATIVE+'/'+Path(stem).name+'.tex',pdf=NATIVE+'/'+Path(stem).name+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=pages,role=role,source_ids=['L039'],measured=False,compression_factor=None,externaldocument_dependency=None))
 write('native_catalogue_draft.json',dict(new_documents=rows,complete_scientific_pages=10,all_whole_papers_paid=True,current_public_admission=None))
 whole=[]
 for r in files:
  if Path(r['logical_path']).suffix in ['.py','.g','.cpp','.lean']:
   role='AUDIT_HISTORICAL_REVIEW' if r['logical_path'].startswith('inputs/') else 'OPTIONAL_VALIDATION' if r['logical_path']=='diagnostics.py' else 'OPERATIONAL_BINDING_RENDER_DRIVER'
   whole.append(dict(r,role=role,complete_file=True))
 write('whole_file_roles_draft.json',dict(whole_files=whole,required_mathematical_programs=[],required_mathematical_data=[],formal_files=[],source_software_cost=None,unknown_not_zero=True,software_inclusive_factor=None,measurement=None))
 print(json.dumps(dict(files=len(files),packets=len(packets),native_pages=[3,7],whole_executable_occurrences=len(whole),public_files_written=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);main(p.parse_args())
