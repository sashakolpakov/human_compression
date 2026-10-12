"""Private exact L122 accepted science/review mapping; no public writes."""
from pathlib import Path
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
NATIVE='papers/recoveries/L122/v1';SCIENCE='audit/recoveries/L122/v1'
SPECS=[('author','corpus106_L122_complete_recovery','38fa5807b76a5c92085874a6c92853becb73a68e29a2d4236448a818511fe9c0'),('root_review','corpus106_L122_complete_root_review','ed107ddf260dc8b9e2edf24bdbc41bcac0f200ec3d9e1988a901615be099ad57')]
NATIVES=[('L122_common','components/positive/triality_coordinates','triality_coordinates',4,'Complete positive common theory'),('L122_examples','components/positive/finite_triality_examples','finite_triality_examples',4,'Complete positive application'),('L122_counterexample','components/counterexample/no_triality','no_triality',3,'Complete actual coset counterexample'),('L122_current_contract','current_contract','current_contract',2,'Current whole-source contract addendum')]
def bind(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(n,x):(HERE/n).write_text(json.dumps(x,indent=2)+'\n')
def main(a):
 if (HERE/'manifest.json').exists():raise ValueError('Frozen proposal')
 files=[];packets=[];native={s+e:NATIVE+'/'+d+e for _,s,d,_,_ in NATIVES for e in ['.tex','.pdf']}
 for key,directory,pin in SPECS:
  p=a.study/directory;man=bind(p/'manifest.json',SCIENCE+'/'+key+'/manifest.json')
  if man['sha256']!=pin:raise ValueError('scientific pin')
  m=json.loads((p/'manifest.json').read_text());packets.append(dict(id=key,study_directory=directory,manifest=man,exports=len(m['exports'])))
  for x in [bind(p/'manifest.json','manifest.json')]+m['exports']:
   n=x['path']
   if bind(p/n,n)!=x:raise ValueError('Frozen bytes '+n)
   dest=native[n] if key=='author' and n in native else SCIENCE+'/'+key+'/'+n
   if dest.endswith('.md'):dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=n,study_path=directory+'/'+n,public_path=dest,bytes=x['bytes'],sha256=x['sha256']))
 if len(files)!=73 or len({x['public_path'] for x in files})!=73:raise ValueError('exact whole routing')
 put('payload_routes.json',dict(packets=packets,files=files,primary_source_exported=False))
 docs=[]
 for i,s,d,n,r in NATIVES:
  t=(a.study/SPECS[0][1]/(s+'.tex')).read_text();title=re.search(r'\\title\{([^{}]+)\}',t).group(1)
  docs.append(dict(id=i,title=title,tex=NATIVE+'/'+d+'.tex',pdf=NATIVE+'/'+d+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=n,role=r,source_ids=['L122'],measured=False,compression_factor=None,externaldocument_dependency=None))
 put('native_catalogue_draft.json',dict(new_documents=docs,complete_scientific_pages=11,complete_native_pages=13,all_whole_papers_paid=True))
 inv=json.loads((a.study/SPECS[0][1]/'program_inventory.json').read_text());whole=[]
 for f in inv['files']:
  row=next(x for x in files if x['packet']=='author' and x['logical_path']==f['path']);whole.append(dict(row,role=f['role'],complete_file=True))
 if {x['logical_path'] for x in files if x['packet']=='author' and Path(x['logical_path']).suffix in ['.py','.g','.lean']}!={x['logical_path'] for x in whole if Path(x['logical_path']).suffix in ['.py','.g','.lean']}:raise ValueError('whole executable inventory')
 put('whole_file_roles_draft.json',dict(whole_files=whole,required_mathematical_programs=[x for x in whole if x['role']=='REQUIRED_MATHEMATICAL_PROGRAM'],required_mathematical_data=[x for x in whole if x['role']=='REQUIRED_MATHEMATICAL_DATA'],optional_validation=[x for x in whole if x['role']=='OPTIONAL_VALIDATION'],operational_drivers=[x for x in whole if x['role']=='OPERATIONAL_DRIVER'],archived_discovery=[x for x in whole if x['role']=='ARCHIVED_DISCOVERY_NOT_PREMISE'],formal_files=[],source_executable_listing_pages=[],source_software_cost=None,external_proof_cost=None,external_runtime_cost=None,software_inclusive_factor=None,measurement=None,unknown_not_zero=True,validation_symmetry='Future optional executable verification is included on both sides or omitted on both. Required proof programs/data and unknown source software remain explicit.',receipts='All generated receipts bound as whole author exports. No receipt replaces the required algorithm or data.'))
 print(json.dumps(dict(files=len(files),packets=2,native_pages=[4,4,3,2],whole_inventory=len(whole))))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);main(p.parse_args())
