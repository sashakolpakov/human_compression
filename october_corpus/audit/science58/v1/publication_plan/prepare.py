"""Private F008 science-only proposal builder; never writes the public checkout."""
from pathlib import Path
import argparse, ast, copy, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
BASE='5c8f37aca03c59903f521840008235b5e4b95a4b'
AUDIT='audit/science58/v1'
NATIVE='papers/recoveries/F008/v1'
SCIENCE='audit/recoveries/F008/v1'
AUTHOR='corpus106_F008_three_dimensional'
AUTHOR_PIN='e23fc1b32cd5e291808a1b27b3e6db85ee2d947428c08725ebc0b1d43689de35'

def need(v,m):
 if not v: raise ValueError(m)
def load(p): return json.loads(p.read_text())
def binding(p,name):
 b=p.read_bytes(); return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(obj if isinstance(obj,str) else json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main(a):
 study,repo=a.study,a.repo
 need(not(HERE/'manifest.json').exists(),'frozen proposal')
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 review=study/a.review_dir; pin=binding(review/'manifest.json','manifest.json')['sha256']
 need(pin==a.review_pin,'actual root review pin')
 W=HERE/'wrappers'; files=[]; packets=[]
 specifications=[('author',AUTHOR,SCIENCE+'/author',AUTHOR_PIN),
                 ('planar_review','corpus106_F008_planar_independent_review',SCIENCE+'/planar_review','bc1ca86a5a76b9644c26ccb995b0bbf7fb3cc7b1466be3bf32f03eb11df32d53'),
                 ('planar_adoption','corpus106_F008_planar_root_adoption',SCIENCE+'/planar_root_adoption',None),
                 ('root_review',a.review_dir,SCIENCE+'/root_review',pin)]
 native={'inherited/planar/weighted_divisors.tex','inherited/planar/weighted_divisors.pdf',
         'inherited/planar/mondrian_density.tex','inherited/planar/mondrian_density.pdf',
         'three_dimensional.tex','three_dimensional.pdf'}
 for key,directory,public,expected in specifications:
  d=study/directory; m=load(d/'manifest.json'); manifest=binding(d/'manifest.json',public+'/manifest.json')
  need(expected is None or manifest['sha256']==expected,'scientific manifest pin')
  packets.append(dict(id=key,study_directory=directory,manifest=manifest,exports=len(m['exports'])))
  for e in [binding(d/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path']; need(binding(d/logical,logical)==e,'frozen payload')
   dest=NATIVE+'/'+Path(logical).name if key=='author' and logical in native else public+'/'+logical
   if dest.endswith('.md'): dest=dest[:-3]+'.txt'
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dest,bytes=e['bytes'],sha256=e['sha256']))
 need(len({r['public_path'] for r in files})==len(files),'unique copy routes')
 write(HERE/'copy_plan.json',dict(base_commit=BASE,packets=packets,files=files))
 history={}
 names=['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']
 for name in names:
  dest=AUDIT+'/previous/'+name; p=W/dest; p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/name).read_bytes());history[name]=binding(p,dest)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science57 pointers and unchanged nested science56/55/programme53 guards.'))
 old=load(repo/'audit/corpus/latest.json'); oldcat=load(repo/old['active_catalogue']['path'])
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(asts)==141,'141 old functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json']
 for prefix in ['audit/overview/v19/packet','audit/science55/v1','audit/science56/v1','audit/science57/v1']:
  protected += [str(p.relative_to(repo)) for p in (repo/prefix).rglob('*') if p.is_file()]
 tracked=set(subprocess.check_output(['git','-C',str(repo),'ls-files'],text=True).splitlines())
 protected=sorted(set(protected)&tracked)
 write(HERE/'baseline.json',dict(commit=BASE,old_nonmain_ASTs=asts,protected_files=[binding(repo/p,p) for p in protected],old_catalogue=old['active_catalogue'],history=history,counts=dict(active=106,reviewed=57,measured=53,unmeasured=4,pending=48,editorial=1,archived=55,topics=19)))
 def pub(path):
  if (W/path).is_file(): return binding(W/path,path)
  row=next((r for r in files if r['public_path']==path),None)
  return dict(path=path,bytes=row['bytes'],sha256=row['sha256']) if row else binding(repo/path,path)
 def route(packet,name): return next(r['public_path'] for r in files if r['packet']==packet and r['logical_path']==name)
 roles=[]
 for row in files:
  if Path(row['logical_path']).suffix not in ['.py','.g','.cpp','.lean']: continue
  role='AUDIT_REVIEW_OR_OPERATIONAL'
  if row['packet']=='author': role='OPTIONAL_VALIDATION' if row['logical_path']=='check_algebra.py' else 'OPERATIONAL_BINDING_RENDER_DRIVER'
  roles.append(dict(row,role=role,complete_file=True))
 write(W/(AUDIT+'/whole_file_roles.json'),dict(whole_files=roles,required_mathematical_programs=[],required_mathematical_data=[],formal_files=[],source_software_cost=None,unknown_not_zero=True,software_inclusive_factor=None,measurement=None,scope='Optional algebra and review diagnostics are not analytic premises. Every executable occurrence is retained whole; no software-inclusive scalar.'))
 ad=dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE58_GATE',source_id='F008',source_ids=['F008'],auxiliary_original=True,source_author_role='Auxiliary original by Noah Lebowitz-Lockard and Gérald Tenenbaum; not focal-group authored.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=packets[0]['manifest'],distinct_root_review_manifest=packets[-1]['manifest'],root_scientific_acceptance=packets[-1]['manifest'],prior_planar_review=packets[1]['manifest'],prior_planar_root_adoption=packets[2]['manifest'],source_map=pub(route('author','source_map.json')),scope=pub(route('author','scope.json')),retained_inputs=pub(route('author','dependencies.json')),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_common=[pub(NATIVE+'/weighted_divisors.pdf')],whole_applications=[pub(NATIVE+'/mondrian_density.pdf')],whole_common_application_supplements=[pub(NATIVE+'/three_dimensional.pdf')],physical_pages=[5,4,6],source_pages=13,source_routes=36,comparison_topic_created=False,current_measurements_changed=False,required_mathematical_programs=[],source_software_cost=None,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note='Complete corrected principal recovery of planar and strong three-dimensional density, almost-all rectangle count and the stated weighted moment theorem. Conjecture1.1 remains unanswered. General multiplicative weights and improved-error ancillary remarks are not recovered; retained historical/general background is explicit. No literal theorem-set equivalence.',roles='Root authored the earlier planar papers; rewrite_termination distinctly reviewed them and authored the new3D proof and this publication proposal. Root distinctly reviews the new3D proof and combined source contract. Publication wiring review is separate.',frozen_status_overlay='Author-stage pending3D/review labels in preserved files are historical. The distinct scientific review supplies current acceptance without changing those bytes.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad); admission=pub(ap)
 rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['F008'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['F008'])
 summary='Auxiliary original: complete corrected planar/strong3D density proofs, almost-all rectangle bound and weighted moments. Whole common5+planar4+3D6 pages. Conjecture1.1 and general-weight/improved-error ancillary remarks remain unproved; no numerical factor.'
 cat=copy.deepcopy(oldcat)
 cat.update(status='CURRENT_ACCESSIBLE106_58_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=58,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=47,review_revision='Only F008 moves from mathematical pending to corrected principal recovery. It is an auxiliary original, not focal-group authored. Other105 records remain exact.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=58,measured=53,measurement_pending=5,pending=47,editorial=1))
 row=next(r for r in cat['entries'] if r['original_id']=='F008'); previous=copy.deepcopy(row['current_principal_recovery'])
 row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,auxiliary_original=True,scope=summary,historical_admission_evidence=previous)
 row['next_obligation']='Any later comparison must acquire all three full manuscripts and preserve ancillary nonrecoveries/open Conjecture1.1. Symmetric input review is required before counts or factors; no source software cost is silently zero.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured58-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old); c.update(status='CURRENT_PROGRAMME_58_CORRECTED_RECOVERIES_53_MEASURED_47_PENDING_1_EDITORIAL',admitted_principal_originals=58,accessible_pending_complete_recovery=47,admitted_original_ids=sorted(old['admitted_original_ids']+['F008']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids'] if i!='F008'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured58.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 docs=[]
 for identity,stem,role,pages in [('F008_U','weighted_divisors','common',5),('F008_A','mondrian_density','planar application',4),('F008_3D','three_dimensional','complete common/application supplement',6)]:
  tex=NATIVE+'/'+stem+'.tex'; src=study/next(r['study_path'] for r in files if r['public_path']==tex)
  docs.append(dict(id=identity,topic='Auxiliary arithmetic recovery',comparison_topic_created=False,auxiliary_original=True,title=re.search(r'\\title\{([^{}]+)\}',src.read_text()).group(1),role=role,source_ids=['F008'],tex=tex,pdf=NATIVE+'/'+stem+'.pdf',tex_inputs=[],compiler='pdflatex',physical_pages=pages,admission=admission,measured=False,compression_factor=None,externaldocument_dependency=None))
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(docs);sc['original_ids'].append('F008');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_FIVE_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_documents=docs,complete_scientific_pages=15,compiler='pdflatex',all_whole_papers_paid=True))
 text=(repo/'README.rst').read_text().replace('**57 accessible originals','**58 accessible originals').replace('53 are measured and four (N014, L024, L102 and F011) await measurement.','53 are measured and five (N014, L024, L102, F011 and F008) await measurement.').replace('48 await mathematical recovery;','47 await mathematical recovery;')
 insertion='The `F008 guide <'+NATIVE+'/PUBLICATION.rst>`_ presents an **auxiliary original,\nnot focal-group authored**, by Noah Lebowitz-Lockard and Gérald Tenenbaum.\nIts complete five-page common theory, four-page planar application and six-page\nthree-dimensional supplement recover the principal density, rectangle-count and\nweighted-moment bounds. General-weight and improved-error ancillary remarks\nremain unproved, and **Conjecture 1.1 remains unanswered**.\n\nAll five source editions, complete proof packets and distinct reviews are recorded'
 need('All four source editions, complete proof packets and distinct reviews are recorded' in text,'README insertion')
 text=text.replace('All four source editions, complete proof packets and distinct reviews are recorded',insertion).replace('audit/science57/v1/new_original_registration.json',rp).replace('None of these four recoveries','None of these five recoveries');write(W/'README.rst',text)
 text=(repo/'audit/completion.rst').read_text().replace('**57 reviewed corrected principal recoveries**','**58 reviewed corrected principal recoveries**').replace('53 are measured and four (N014, L024, L102 and F011) are unmeasured. There are 48 originals','53 are measured and five (N014, L024, L102, F011 and F008) are unmeasured. There are 47 originals').replace('N014, L024, L102 and F011 have separate scientific admissions','N014, L024, L102, F011 and F008 have separate scientific admissions').replace('science57/v1/new_original_registration.json','science58/v1/new_original_registration.json')
 text=text.replace('The `current overview','F008 is an auxiliary original, not focal-group authored. Its principal recovery\nkeeps the general-weight/improved-error ancillary limits and unanswered\nConjecture 1.1 explicit.\n\nThe `current overview',1);write(W/'audit/completion.rst',text)
 text=(repo/'audit/protocol.tex').read_text().replace('106=57\\ \\text{reviewed corrected recoveries}+48','106=58\\ \\text{reviewed corrected recoveries}+47').replace('Of the 57 corrected recoveries','Of the 58 corrected recoveries').replace('N014, L024, L102 and F011 are scientifically accepted but unmeasured','N014, L024, L102, F011 and F008 are scientifically accepted but unmeasured')
 text=text.replace('The accepted overview v19','F008 is an auxiliary original, not focal-group authored. Its general-weight and\nimproved-error ancillary remarks remain unreproved, and Conjecture 1.1 remains\nunanswered.\n\nThe accepted overview v19',1);write(W/'audit/protocol.tex',text)
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['F008'],auxiliary_original=True,counts=dict(active=106,corrected_recoveries=58,measured=53,unmeasured=5,mathematical_pending=47,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 print(json.dumps(dict(files=len(files),packets=len(packets),native_pages=[5,4,6],prior_functions=len(asts))))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--review-dir',required=True);p.add_argument('--review-pin',required=True);main(p.parse_args())
