"""Prepare a private, science-only publication proposal from exact accepted bytes."""
from pathlib import Path
import argparse, ast, copy, hashlib, json, re

HERE = Path(__file__).resolve().parent
BASE = '40eabd39932684ac6fd6fccb804e06486363d31b'
AUDIT = 'audit/science55/v1'
N = 'papers/topic-c/extensions/generalized-halving/v1'
NA = 'audit/topic-c/extensions/generalized-halving/v1'
L = 'papers/recoveries/L024/v1'
LA = 'audit/recoveries/L024/v1'
PACKETS = [
 ('N014_author','topic_C_N014_complete',NA+'/author','1e4f67f5a84b39177c666b55d7884ca8ab6281f6f4b2de803a1c36f9d56cb973'),
 ('N014_review','topic_C_N014_complete_independent_review',NA+'/independent_review','c9cdab9e438af28a573acd0cdd925f012f1c71c402cc75c4525186697f2ae159'),
 ('N014_adoption','topic_C_N014_complete_root_adoption',NA+'/root_adoption','50a01e40384e0c33be130b564d39c84f5b69cd1fc98a3e7c5441fbe3f9ae64a4'),
 ('L024_author','corpus106_L024_recovery_v3',LA+'/author','dd11979eadc2efa7babbfa814be27778f97fdce5267aa3d8553125326a1c63d2'),
 ('L024_review','corpus106_L024_independent_review',LA+'/independent_review','d34aa3204689b9d45c73ebdd3c4e4a51a3fe80d0c8c3264f745d12244bcb2874'),
 ('L024_adoption','corpus106_L024_root_adoption',LA+'/root_adoption','16e6421b17996bc4150c89caf76e1cbbe5d12bced2e827a2f884ee1944941cb9'),
]

def need(ok, msg):
 if not ok: raise ValueError(msg)
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p, name):
 b=p.read_bytes(); return dict(path=name,bytes=len(b),sha256=sha(b))
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n' if not isinstance(d,str) else d)
def text_title(p): return re.search(r'\\title\{([^{}]+)\}',p.read_text()).group(1)

def prepare(study, repo):
 need(not (HERE/'manifest.json').exists(),'Frozen proposal must not be regenerated.')
 W=HERE/'wrappers';W.mkdir(exist_ok=True)
 rows=[];packets=[];renames=[];reused=[]
 native_names={'common_supplement.tex','common_supplement.pdf','halving_applications.tex','halving_applications.pdf','preamble.tex','references.tex'}
 for key,directory,public,pin in PACKETS:
  P=study/directory;m=load(P/'manifest.json');need(sha((P/'manifest.json').read_bytes())==pin,'exact author/review pin '+key)
  manifest_row=binding(P/'manifest.json',public+'/manifest.json')
  packets.append(dict(id=key,study_directory=directory,manifest=manifest_row,exports=len(m['exports'])))
  exports=[dict(path='manifest.json',**{k:v for k,v in manifest_row.items()if k!='path'})]+m['exports']
  for e in exports:
   logical=e['path'];q=P/logical;need(binding(q,logical)=={k:e[k] for k in ['path','bytes','sha256']},'frozen file '+logical)
   dst=public+'/'+logical;reuse=False
   if key=='N014_author':
    if logical.startswith('old_common/'):
     dst='papers/topic-c/v2/'+logical[len('old_common/'):];reuse=True
     need((repo/dst).read_bytes()==q.read_bytes(),'unchanged old C common')
    elif logical in native_names or logical.startswith('sections/'):dst=N+'/'+logical
   if key=='L024_author' and logical in ['schur_characters.tex','schur_characters.pdf']:dst=L+'/'+logical
   if logical.endswith('.md'):
    dst=dst[:-3]+'.txt'
    renames.append(dict(packet=key,logical_path=logical,public_path=dst,bytes=e['bytes'],sha256=e['sha256'],kind='exact project-authored historical proof or scope prose; no primary-source transcription'))
   r=dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dst,bytes=e['bytes'],sha256=e['sha256'],reuse_existing_public=reuse)
   rows.append(r)
   if reuse:reused.append(dict(path=dst,bytes=e['bytes'],sha256=e['sha256']))
 need(len({r['public_path'] for r in rows})==len(rows),'public path collision')
 write(HERE/'copy_plan.json',dict(base_commit=BASE,packets=packets,files=rows))
 write(HERE/'provenance_path_map.json',dict(policy='Change extensions only, never bytes. Restore logical paths in a fresh private replay directory; never rename in the public repository.',renames=renames))
 write(HERE/'reused_science.json',dict(files=reused,whole_old_common_required=True,whole_old_common_pages=10,no_cross_topic_discount=True))

 historical=['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','scripts/verify_snapshot.py']
 history={}
 for name in historical:
  dst=AUDIT+'/previous/'+name;target=W/dst;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((repo/name).read_bytes());history[name]=binding(target,dst)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact programme53 reader/current routes and verifier for unchanged historical checks.'))
 old=load(repo/'audit/corpus/latest.json');oldcat=load(repo/old['active_catalogue']['path'])
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/packet/results.json','audit/overview/v19/admission.json','papers/topic-a/latest.json','papers/topic-affine/latest.json','papers/topic-b/latest.json']
 for p in (repo/'audit/overview/v19/packet').iterdir():
  if p.is_file() and str(p.relative_to(repo)) not in protected:protected.append(str(p.relative_to(repo)))
 asts={n.name:sha(ast.dump(n,include_attributes=False).encode()) for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(asts)==135,'current135 function boundary')
 write(HERE/'baseline.json',dict(commit=BASE,old_nonmain_ASTs=asts,protected_files=[binding(repo/p,p)for p in protected],old_catalogue=old['active_catalogue'],old_counts=dict(active=106,reviewed=53,measured=53,mathematical_pending=52,editorial=1,archived=55,comparison_topics=19),history=history))

 def author_path(key,logical):return next(r['public_path']for r in rows if r['packet']==key and r['logical_path']==logical)
 def bpublic(path):
  if (W/path).exists():return binding(W/path,path)
  match=next((r for r in rows if r['public_path']==path),None)
  if match:return {k:match['public_path']if k=='path'else match[k]for k in ['path','bytes','sha256']}
  return binding(repo/path,path)
 def pb(key):return next(p['manifest']for p in packets if p['id']==key)
 admissions={}
 for oid,base in [('N014',NA),('L024',LA)]:
  ad=dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE55_GATE',source_ids=[oid],source_id=oid,principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,source_edition_only=True,author_manifest=pb(oid+'_author'),distinct_review_manifest=pb(oid+'_review'),root_adoption_manifest=pb(oid+'_adoption'),public_mapping=AUDIT+'/publication_plan/copy_plan.json',source_map=bpublic(author_path(oid+'_author','source_map.json')),scope=bpublic(author_path(oid+'_author','scope.json')),required_program_inventory=AUDIT+'/whole_file_roles.json',publication_gate=AUDIT+'/root_integration.json')
  if oid=='N014':
   ad.update(whole_common=[bpublic('papers/topic-c/v2/umbrella.pdf'),bpublic(N+'/common_supplement.pdf')],whole_applications=[bpublic(N+'/halving_applications.pdf')],physical_pages=[10,8,17],source_routes=52,named_source_items=43,scope_note='Complete corrected/refuted clausewise adjudication; literal coset identification is true, unrestricted RC and the introductory transitivity converse are false. Borrowed nonthin splitting and the informal hemicube observation retain their stated limits.',roles='enumeration_volume assembled; rewrite_termination distinctly reviewed complete assembly; root adopted, reusing distinct reviews of root-authored components.')
  else:
   ad.update(whole_common=[],whole_applications=[bpublic(L+'/schur_characters.pdf')],physical_pages=[5],source_routes=13,scope_note='Corrected principal existence results and infinite family. The unspecified historical36-marking run, introductory global minimality and all-family polytopality suggestion are not recovered.',roles='root authored; enumeration_volume distinctly reviewed; root adopted that review. No self-review claim.',comparison_topic_created=False)
  write(W/(base+'/admission.json'),ad);admissions[oid]=bpublic(base+'/admission.json')

 # Whole roles are an overlay, not a replacement or sum over mixed categories.
 raw=[]
 inventory=load(study/'topic_C_N014_complete/program_inventory.json')
 for e in inventory['current_files']:
  raw.append(dict(original_id='N014',**e,public_path=author_path('N014_author',e['path'])))
 r=next(x for x in rows if x['packet']=='N014_author'and x['logical_path']=='check.py')
 raw.append(dict(original_id='N014',path='check.py',public_path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'],role='operational_assembly_driver',required_for_N014=False,scope='Exact top-level driver overlay already accepted by distinct review.'))
 for logical,role,scope in [('verify_schur_example.g','required_mathematical_program','Whole fixed generation and character-table calculation; contained64 IP tests only corroborate the written proof.'),('schur_example_report.txt','retained_complete_computation_receipt','Exact full run result, not a separate algorithm or a source-software estimate.')]:
  r=next(x for x in rows if x['packet']=='L024_author'and x['logical_path']==logical);raw.append(dict(original_id='L024',path=logical,public_path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'],role=role,scope=scope))
 write(W/(AUDIT+'/whole_file_roles.json'),dict(status='COMPLETE_CURRENT_ROLE_OVERLAY_NO_LENGTH_EVALUATION',current_files=raw,N014_inherited_raw_ledger=bpublic(author_path('N014_author','raw_occurrences.json')),N014_formal_scope=bpublic(author_path('N014_author','formal_scope.json')),L024_retained_inputs=bpublic(author_path('L024_author','dependencies.json')),no_disjoint_role_sum=True,software_inclusive_factor=None,source_listing_policy={'N014':'No executable listing in inspected supplied primary. Historical software cost unknown.','L024':'Literal GAP commands in source pp3–5 require matched exclusion before a future manuscript measure. No input audit or factor here.'},new_formal_declarations=0))

 # Only two original records change. Historical evidence remains present.
 cat=copy.deepcopy(oldcat)
 cat.update(status='CURRENT_ACCESSIBLE106_55_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=55,currently_measured_originals=53,measurement_pending_original_ids=['L024','N014'],accessible_pending_complete_recovery=50,review_revision='Only N014 and L024 receive accepted corrected principal recovery records; all104 other original records are exact.',new_proof_credit=2,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=55,measured=53,measurement_pending=2,pending=50,editorial=1))
 summaries={'N014':'Complete corrected source adjudication: exact residue transport and coset identification, regular residual-connectivity counterexample, corrected second-leaf criterion and affine period presentations, all toroid iterations/diagrams, and the false introductory transitivity converse. Exact v1 and retained borrowed limits remain explicit.','L024':'Complete corrected principal existence results: explicit PSU5(3) real-Schur-index2 polytopal example and corrected infinite family, with retained character/classification inputs. Historical36-marking run, global minimality wording and suggested all-family polytopality remain unproved.'}
 for e in cat['entries']:
  oid=e['original_id']
  if oid not in admissions:continue
  prior=copy.deepcopy(e['current_principal_recovery'])
  e['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admissions[oid]],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=summaries[oid],historical_admission_evidence=prior)
  e['principal_results_to_recover']['summary']=summaries[oid]
  e['principal_results_to_recover']['scope_status']='COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_ACCEPTED'
  e['next_obligation']='Prepare and independently review a complete symmetric measurement-input boundary before evaluating any factor. Preserve the accepted source corrections, retained inputs and ancillary limits.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured55-catalogue.json';write(W/cp,cat)
 reg=dict(status='ROOT_ACCEPTED_CORRECTED_SCIENTIFIC_RECOVERIES_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['N014','L024'],admissions=list(admissions.values()),principal_originals_added=2,measurement_originals_added=0,compression_factor=None,new_question_credit=0,whole_source_formalized=False,comparison_topics_added=0)
 rp=AUDIT+'/new_original_registration.json';write(W/rp,reg)
 corpus=copy.deepcopy(old)
 corpus.update(status='CURRENT_PROGRAMME_55_CORRECTED_RECOVERIES_53_MEASURED_50_PENDING_1_EDITORIAL',admitted_principal_originals=55,accessible_pending_complete_recovery=50,admitted_original_ids=sorted(old['admitted_original_ids']+['N014','L024']),accessible_pending_original_ids=[x for x in old['accessible_pending_original_ids']if x not in admissions],measurement_pending_original_ids=['L024','N014'],previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=bpublic(cp),scientific_unmeasured_original_ids=['L024','N014'],current_science_registration=bpublic(rp),current_scope='Complete reviewed corrected principal recoveries, not theorem-set equivalence; finish105 mathematical originals then stop.')
 corpus['added_admissions'].append(bpublic(rp));corpus.pop('snapshot',None)
 snap='audit/corpus/updates/accessible106-corrected-unmeasured55.json';write(W/snap,corpus)
 corpus['snapshot']=bpublic(snap);write(W/'audit/corpus/latest.json',corpus)

 documents=[]
 specs=[('N014_U',N,'common_supplement','C','common_supplement',8,'xelatex',['sections/01-residues.tex','sections/02-cosets.tex','sections/03-further-leaves.tex']),('N014_A',N,'halving_applications','C','application',17,'xelatex',['sections/10-regular-counterexample.tex','sections/20-affine-groups.tex','sections/30-iterated-geometry.tex','sections/40-transitivity-converse.tex']),('L024_A',L,'schur_characters',None,'standalone_corrected_recovery',5,'pdflatex',[])]
 for key,base,stem,topic,role,pages,compiler,sections in specs:
  oid=key.split('_')[0];directory=study/('topic_C_N014_complete'if oid=='N014'else'corpus106_L024_recovery_v3')
  documents.append(dict(id=key,topic=topic,comparison_topic_created=False,title=text_title(directory/(stem+'.tex')),role=role,source_ids=[oid],tex=base+'/'+stem+'.tex',pdf=base+'/'+stem+'.pdf',tex_inputs=[base+'/'+x for x in (['preamble.tex','references.tex']+sections if oid=='N014'else[])],compiler=compiler,physical_pages=pages,admission=admissions[oid],measured=False,compression_factor=None))
 olddoc=dict(id='N014_old_U',topic='C',role='entire_acquired_common',source_ids=['N014'],tex='papers/topic-c/v2/umbrella.tex',pdf='papers/topic-c/v2/umbrella.pdf',tex_inputs=[x['path'] for x in reused if x['path'].endswith('.tex')and not x['path'].endswith('/umbrella.tex')],compiler='xelatex',physical_pages=10,title=text_title(repo/'papers/topic-c/v2/umbrella.tex'))
 sc='papers/catalogue_corrected_unmeasured.json';write(W/sc,dict(status='ACCEPTED_SCIENCE_MEASUREMENT_PENDING',entries=documents,acquired_dependencies=[olddoc],original_ids=['N014','L024'],new_measurements=0,existing_comparison_topic_count=19,root_publication_gate=AUDIT+'/root_integration.json'))
 pc=load(repo/'papers/latest_catalogue.json');pc['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_TWO_CORRECTED_UNMEASURED';pc['active_source_catalogue']=bpublic(cp);pc['corrected_unmeasured_scientific_catalogue']=bpublic(sc);write(W/'papers/latest_catalogue.json',pc)
 write(HERE/'native_catalogue.json',dict(new_documents=documents,acquired_documents=[olddoc]))

 # Exact, small documentation successor; the complete old reader is snapshotted.
 readme=(repo/'README.rst').read_text()
 before='**53 accessible originals have admitted and measured principal-result recoveries.\n52 await mathematical recovery; L022 is an editorial with no mathematical result\nto recover.**'
 after='**55 accessible originals have reviewed corrected principal-result recoveries:\n53 are measured and two (N014 and L024) await measurement.\n50 await mathematical recovery; L022 is an editorial with no mathematical result\nto recover.**'
 need(before in readme,'exact README partition');readme=readme.replace(before,after)
 needle='Current papers and comparisons\n------------------------------\n'
 new='Reviewed recoveries awaiting measurement\n----------------------------------------\n\nThe `N014 guide <'+N+'/PUBLICATION.rst>`_ routes the complete generalized-halving\nrecovery: the unchanged ten-page Topic C common paper, its eight-page supplement\nand the seventeen-page application. It distinguishes true coset identification\nfrom false preservation clauses and supplies their corrections and counterexamples.\n\nThe `L024 guide <'+L+'/PUBLICATION.rst>`_ gives the five-page Schur-index recovery\nwith its exact finite certificate and retained character-theoretic inputs. The\nunspecified historical marking run, global minimality wording and suggested\nall-family polytopality remain outside its accepted principal conclusions.\n\nBoth source editions, complete proof packets and distinct reviews are recorded\nin the `science register <'+AUDIT+'/new_original_registration.json>`_.\nNeither recovery has a compression factor. N014 is not added to C\'s measured\nfive-original boundary, and L024 creates no comparison topic. The table and\noverview below remain the accepted 53-original measurement edition. Corrected\nrecovery does not assert equivalence with every literal source assertion.\n\n'+needle
 readme=readme.replace(needle,new)
 readme=readme.replace('A uses its full 23-page common paper and all nine\napplications, including L121.','A uses three complete common papers (41 pages) and all ten\napplication bundles (63 pages).')
 readme=readme.replace('Each admission links the immutable author packet,\ndistinct review, input audit and numerical review.','Each scientific admission links the immutable author packet and distinct\nreview. Measured editions additionally link the input audit and numerical review.')
 readme=readme.replace('audit/programme53/v1/previous/README.rst',AUDIT+'/previous/README.rst').replace('audit/programme53/v1/previous/audit/protocol.pdf',AUDIT+'/previous/audit/protocol.pdf')
 write(W/'README.rst',readme)
 tex=(repo/'audit/protocol.tex').read_text()
 tex=tex.replace('106=53\\ \\text{measured recoveries}+52\\ \\text{mathematical targets}\n       +1\\ \\text{editorial}.','106=55\\ \\text{reviewed corrected recoveries}+50\\ \\text{mathematical targets}\n       +1\\ \\text{editorial}.')
 needle='The register counts originals, not theorem nodes, contracts, editions or files.'
 tex=tex.replace(needle,needle+'\nOf the 55 corrected recoveries, 53 have accepted manuscript measurements.\nN014 and L024 are scientifically accepted but unmeasured; neither is included\nin a new factor. Their corrections adjudicate the declared principal contracts,\nwithout asserting equivalence with every literal source statement. The goal\nis complete reviewed recovery of all 105 mathematical originals, then stop.')
 write(W/'audit/protocol.tex',tex)
 completion=(repo/'audit/completion.rst').read_text();start=completion.index('The current register');end=completion.index('The `current overview')
 completion=completion[:start]+'The current register contains **55 reviewed corrected principal recoveries**:\n53 are measured and two (N014 and L024) are unmeasured. There are 50 originals\nawaiting mathematical recovery and one editorial (L022), giving 106 accessible\noriginals. The other 55 historical originals remain archived. The stop boundary\nis complete reviewed recovery of the 105 mathematical originals.\n\nN014 and L024 have separate scientific admissions; their corrections and retained\nlimits do not assert literal theorem-set equivalence. No factor, comparison topic,\nnew question answer or complete Lean claim is added. See the\n`science register <science55/v1/new_original_registration.json>`_.\n\n'+completion[end:]
 write(W/'audit/completion.rst',completion)
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['N014','L024'],counts=dict(active=106,corrected_recoveries=55,measured=53,unmeasured=2,mathematical_pending=50,editorial=1,archived=55,comparison_topics=19),corpus_pointer=bpublic('audit/corpus/latest.json'),active_catalogue=bpublic(cp),snapshot=bpublic(snap),papers_pointer=bpublic('papers/latest_catalogue.json'),new_registration=bpublic(rp),admissions=admissions,unchanged_measurement_overview='audit/overview/v19/admission.json',new_comparison_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 print(json.dumps(dict(mapped_files=len(rows),packets=len(packets),reused_files=len(reused),markdown_extension_maps=len(renames),native_pages=[10,8,17,5],old_nonmain_ASTs=len(asts))))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();prepare(a.study,a.repo)
