"""Exact accepted L013 whole-packet routing; private writes only."""
from pathlib import Path
import argparse,hashlib,json,re
HERE=Path(__file__).resolve().parent
NATIVE='papers/recoveries/L013/v1';SCIENCE='audit/recoveries/L013/v1'
SPECS=[('theory','corpus106_L013_theory','4ec2b452fd3696928039395aadee00a8f0aca25ff372c44dabc03f8dbb305ea3'),('theory_review','topic_L013_theory_independent_review','2b5d04d82006e8c6ea46c36406f811a82b2cb6e979e40b08b2e725bd560bb19c'),('finite','corpus106_L013_census','c806a288c122db9c28ba012bfc03b2d92a9d6cd2efc83bc0ef1775640cfab735'),('finite_review','corpus106_L013_census_root_review','6c6b17b98ac82fbb3a2476e8a0e26ba17c681af0b458e0abcaa95731e9daef1b'),('contract','corpus106_L013_complete_contract','fc83f4481365e18e477938080038d2f649f034c4c1adcd6112fe76ddf2e1c13a'),('root_adoption','corpus106_L013_complete_root_adoption','021f4a6849ec209875ee27ab9bf6f69f302454fb75a1a11a2e3f1939b0c5bcba')]
NATIVES=[('L013_common','theory','cages_and_planes',5,'Whole general middle-graph and biaffine theory'),('L013_finite','finite','finite_cages',4,'Whole finite census, exact automorphism and source-identification application')]
def bind(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 if (HERE/'manifest.json').exists():raise ValueError('Immutable proposal')
 files=[];packets=[];native_names={(key,stem+ext) for _,key,stem,_,_ in NATIVES for ext in ['.tex','.pdf']}
 for key,directory,pin in SPECS:
  d=a.study/directory;public=SCIENCE+'/'+key;manifest=bind(d/'manifest.json',public+'/manifest.json')
  if manifest['sha256']!=pin:raise ValueError('Scientific pin '+key)
  m=json.loads((d/'manifest.json').read_text());packets.append(dict(id=key,study_directory=directory,manifest=manifest,exports=len(m['exports'])))
  for e in [bind(d/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path']
   if bind(d/logical,logical)!=e:raise ValueError('Frozen payload '+logical)
   dest=NATIVE+'/'+Path(logical).name if (key,logical) in native_names else public+'/'+logical
   if dest.endswith('.md'):dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dest,bytes=e['bytes'],sha256=e['sha256']))
 if len(files)!=66 or len({r['public_path'] for r in files})!=66:raise ValueError('Whole six-packet routing')
 write('payload_routes.json',dict(status='EXACT_ACCEPTED_PAYLOAD_MAP_PUBLIC_INTEGRATION_PENDING',packets=packets,files=files,primary_source_exported=False))
 rows=[]
 for identity,key,stem,pages,role in NATIVES:
  directory=next(d for k,d,p in SPECS if k==key);text=(a.study/directory/(stem+'.tex')).read_text();title=re.search(r'\\title\{([^{}]+)\}',text).group(1)
  rows.append(dict(id=identity,title=title,tex=NATIVE+'/'+stem+'.tex',pdf=NATIVE+'/'+stem+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=pages,role=role,source_ids=['L013'],measured=False,compression_factor=None,externaldocument_dependency=None))
 write('native_catalogue_draft.json',dict(new_documents=rows,complete_scientific_pages=9,all_whole_papers_paid=True,current_public_admission=None))
 required={('finite','search.py'),('finite','direct_graphs.py'),('finite','finite_certificate.py')};whole=[]
 for r in files:
  if Path(r['logical_path']).suffix in ['.py','.g','.cpp','.lean']:
   key=(r['packet'],r['logical_path']);role='REQUIRED_FINITE_MATHEMATICS' if key in required else 'OPTIONAL_VALIDATION' if key==('theory','check_examples.py') else 'AUDIT_REVIEW_CHECKER' if r['packet']=='theory_review' else 'OPERATIONAL_BINDING_RENDER_DRIVER'
   whole.append(dict(r,role=role,complete_file=True))
 data_names=['k3_complete.json','k4_complete.json','k5_complete.json','k6_witnesses.json','inputs/n44_k6_g5_d4.g6','historical_graphs.json','figure1_edges.json']
 data=[dict(next(r for r in files if r['packet']=='finite' and r['logical_path']==f),role='REQUIRED_MATHEMATICAL_DATA',complete_file=True) for f in data_names]
 write('whole_file_roles_draft.json',dict(whole_files=whole,required_mathematical_programs=[r for r in whole if r['role']=='REQUIRED_FINITE_MATHEMATICS'],required_mathematical_data=data,formal_files=[],source_software_cost=None,unknown_not_zero=True,solver_proof_cost=None,solver_trust='Full exact CP-SAT all-solutions termination; no kernel-checked proof; saved positive rows alone do not prove absence.',software_inclusive_factor=None,measurement=None,validation_symmetry='No metric; future optional validation must be included on both sides or excluded on both.'))
 print(json.dumps(dict(files=len(files),packets=len(packets),native_pages=[5,4],whole_executable_occurrences=len(whole),required_data=len(data),public_files_written=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);main(p.parse_args())
