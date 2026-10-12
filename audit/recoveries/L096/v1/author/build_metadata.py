"""Author assembly metadata; no source extraction or finite group computation."""
from pathlib import Path
import collections,difflib,hashlib,json,re,shutil
B=Path(__file__).resolve().parent;S=B.parent;V=S/'topic_D_L096_volume_v2'
read=lambda p:json.loads(p.read_text())
def pin(p,base=S):return {'path':str(p.relative_to(base)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(name,obj):(B/name).write_text(json.dumps(obj,indent=2)+'\n')
# Preserve the accepted native common PDF; its fresh rebuild is text-compared.
shutil.copyfile(V/'umbrella.pdf',B/'umbrella.pdf')
profiles=read(B/'transcribed_profiles.json');rec=read(B/'label_reconciliation.json')
profiles['status']='AUTHOR_PRIMARY_PROFILE_TRANSCRIPTION_FOR_DISTINCT_REVIEW';put('transcribed_profiles.json',profiles)
source=read(V/'source_map.json');source['status']='AUTHOR_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_PENDING_DISTINCT_REVIEW'
source['historical_label_claims']=rec['claims'];source['unresolved_label_occurrences']=3
source['full_source_recovered']=False
source['complete_corrected_principal_recovery_proposed']=True
source['literal_original_replacement_equivalence']=False
source['mathematical_principal_obligations_unresolved']=[]
source['historical_metadata_unverified']=[{'group':'J1','label':'4.1','source_tables':[2,4,8],'occurrences':3,'mathematical_replacement':'Complete three-class J1 population by exact type-size profiles; full rank-four IP uniquely belongs to {266,1463,1463,2926}. No claim of ordinal identity.'}]
source['J1_complete_profile_classification']=rec['J1_complete_profile_classification']
source['additional_limits']=['Retained previous classification completeness is separate from actual supplied-roster exhaustiveness.','J3 global classification is not newly certified. Its literal archive quotient has 19 classes; the numerical 17-to-19 discrepancy is preserved.','HS README 4.1 erroneous active-entry pointer is corrected by its unique primary type-index profile.','Three J1 ordinal correspondences remain historical metadata; the mathematical classification and all aggregate counts are complete.','No source software/runtime/full graphical cost is assigned zero.','No new question answer, complete Lean claim, or measured factor.']
for r in source['main_and_count_clauses']:
 if 'historical_label_status' in r:r['historical_label_status']='CURRENT_CORRECTED_NAMING_CONTRACT_SEE_COMPANION'
 if r['id']=='D96.rank6':r['current_route']='Accepted HS full shadow decisions and accepted label-identification v3 unique-rank-six argument; no remaining mathematical obligation.'
source['current_scientific_papers']=[{'tex':n+'.tex','pdf':n+'.pdf','pages':k} for n,k in [('umbrella',11),('shadow_applications',9),('named_geometries',7)]]
put('source_map.json',source)
# Each root/independent packet is retained exactly, with original roles.
packets=['topic_D_L096_volume_v2','topic_D_L096_volume_independent_review','topic_D_L096_label_identification_v3','topic_D_L096_label_identification_root_review']
deps=[]
for name in packets:
 p=S/name/'manifest.json';m=read(p)
 deps.append({'packet':name,'manifest':pin(p),'exports':[{'path':name+'/'+x['path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in m['exports']]})
old=read(V/'accepted_dependencies.json')
put('dependencies.json',{'status':'EXACT_RETAINED_ACCEPTED_PROOFS_AND_NEW_AUTHOR_PROGRAM','direct_packets':deps,'prior_complete_dependency_ledger':pin(V/'accepted_dependencies.json'),'all_prior_mathematical_components':old,'old_topic_D_common':read(V/'topic_D_dependency_overlap.json'),'role_disclosure':'New profile work authored here; prior independent volume/J2/M22 review roles are reused solely as inherited evidence. Root and previous author supplied the accepted generic/component science. New work requires distinct review.','new_Lean':False,'whole_original_credit':False})
# Auxiliary primary records are private, complete and externally identifiable.
idx=read(B/'private_auxiliary/wayback_ps_index.json');conv=read(B/'private_auxiliary/conversion_records.json')
extra={'algoSupp_archived.ps':('20030716224622','http://cso.ulb.ac.be:80/~dleemans/abstracts/algoSupp.ps'),'m22supp_archived.ps':('20031106191636','http://cso.ulb.ac.be:80/~dleemans/abstracts/m22supp.ps'),'m23supp_archived.ps':('20030720084201','http://cso.ulb.ac.be:80/~dleemans/abstracts/m23supp.ps')}
aux=[]
for x in conv:
 if x['source']=='list_archived.ps':continue
 stem=x['source'].replace('_archived.ps','');lookup=[z for z in idx if len(z)>1 and str(z[0]).endswith('/'+stem+'.ps')]
 if x['source'] in extra:stamp,url=extra[x['source']]
 else:
  if not lookup:raise ValueError(stem)
  url,stamp=lookup[0][:2]
 path=B/'private_auxiliary'/x['source'];render=B/'private_auxiliary'/x['private_render']
 aux.append({'id':stem,'edition':x['source'],'original_url':url,'archived_url':f'https://web.archive.org/web/{stamp}id_/{url}','capture_timestamp':stamp,'whole_original_file':pin(path),'private_conversion':pin(render),'pages':x['pages'],'directly_viewed_pages':profiles['directly_viewed_primary_pages'][stem],'text_exported':False,'primary_asset_exported':False,'scope':'Only named profile/type/panel/correlation facts used. Whole auxiliary original not claimed recovered.'})
put('source_ledger.json',{'primary':source['primary'],'primary_text_private':source['primary_text'],'auxiliary_primary_records':aux,'conversion_command':'gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=RENDER SOURCE.ps','reading_convention':'Private byte-reading aid only; actual diagram rasters determine transcription. No extraction/calibration metric is inferred.','J1_later_documentary_context':{'url':'https://msp.org/iig/2017/15-1/iig-v15-n1-p04-s.pdf','locator':'Section4.3, printed87, Figure8','claim':'Names the correct profile as4.1 in the2008 atlas and attributes earlier uniqueness to Gottschalk–Leemans; no1998 ordinal inference made.'},'no_new_original_intake':True})
# Explicit text migration, with every old proof environment unchanged.
proof=lambda s:re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}',s,re.S)
mp=[]
for p in sorted(V.rglob('*.tex')):
 q=B/p.relative_to(V)
 mp.append({'source':pin(p),'target':pin(q,B),'literal_identical':p.read_bytes()==q.read_bytes(),'proof_environments':len(proof(p.read_text())),'all_proof_bodies_identical':proof(p.read_text())==proof(q.read_text())})
if not all(x['all_proof_bodies_identical'] for x in mp):raise ValueError('old proof changed')
put('migration.json',{'status':'EXACT_ACCEPTED_PROOF_TRANSFER_PLUS_NEW_COMPANION','files':mp,'new_scientific_files':['named_geometries.tex','label_table.tex'],'new_proofs':['complete compatible family lemma','normalizing correlation criterion','centralizing correlation criterion','M22 correlation/residue discriminators','J3 inner interchange discriminator'],'new_main_math_not_independently_admitted':True,'old_common_pdf_exact':pin(V/'umbrella.pdf'),'changed_application_prose':'Abstract/title and historical-obligation section only; complete new companion supplies current correction.','full_current_written_pages':27,'old_Topic_D_common_additionally_required':True})
# Current file roles are full-file, potentially overlapping, never disjoint sums.
inv=read(V/'whole_program_inventory.json');occ=inv['all_occurrences'][:]
newroles={'label_invariants.g':'required_bounded_group_certificate','parse_invariants.py':'required_full_output_and_graph_checker','reconcile_labels.py':'required_profile_and_all_claim_reconstruction','transcribed_profiles.json':'required_primary_invariant_data','label_invariants.json':'required_bounded_invariant_results','records/label_invariants.log':'required_complete_bounded_execution_output','label_reconciliation.json':'required_full_named_claim_results','check.py':'operational_integrity_render_replay_driver','build_metadata.py':'operational_metadata_assembly_driver'}
for n,role in newroles.items():
 p=B/n
 if not p.exists():continue
 occ.append({**pin(p),'role':role,'whole_file':True,'component':'corpus106_L096_recovery','role_basis':'explicit current use'})
# Preserve all old data-occurrence records, even when also newly consumed.
for n in ['topic_D_L096_M22_extension/prior_inputs.g','topic_D_L096_J3_extension/archive_data/inputs.g']:
 occ.append({**pin(S/n),'role':'required_complete_data_for_new_label_invariant','whole_file':True,'component':'corpus106_L096_recovery','role_basis':'direct whole-file Read in label_invariants.g'})
unique={}
for r in occ:
 u=unique.setdefault(r['sha256'],{'sha256':r['sha256'],'bytes':r['bytes'],'paths':[],'roles':[]})
 if u['bytes']!=r['bytes']:raise ValueError('size conflict')
 if r['path'] not in u['paths']:u['paths'].append(r['path'])
 if r['role'] not in u['roles']:u['roles'].append(r['role'])
inv['status']='AUTHOR_COMPLETE_WHOLE_CONTENT_INVENTORY_NO_FACTOR';inv['all_occurrences']=occ;inv['unique_contents']=sorted(unique.values(),key=lambda x:x['sha256']);inv['inherited_occurrences']=870;inv['new_occurrences']=len(occ)-870;inv['occurrence_count']=len(occ);inv['unique_content_count']=len(unique);inv['role_categories_disjoint']=False
put('whole_program_inventory.json',inv)
print('metadata',len(source['main_and_count_clauses']),len(source['historical_label_claims']),len(aux),len(mp),len(occ),len(unique))
