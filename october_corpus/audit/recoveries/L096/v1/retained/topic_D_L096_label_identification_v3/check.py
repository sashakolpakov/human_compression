#!/usr/bin/env python3
"""Finite source-invariant comparison; no group/census/extraction replay."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,tarfile
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,s):
 if not v:raise ValueError(s)
def invariant(r):
 need(r['order']>0 and all(r['order']%h==0 for h in r['parabolic_orders']),'integral positive group indices')
 return (r['rank'],tuple(sorted(r['order']//h for h in r['parabolic_orders'])),r['borel_order'])
def target(s):return (s['rank'],tuple(sorted(s['type_sizes'])),s['borel_order'])
def unique_classes(rows,part,s):
 need(len(rows)==124 and len(part)==124,'complete supplied HS roster')
 hits=[]
 for i,(r,c) in enumerate(zip(rows,part),1):
  need((r['member'],r['active_row'],r['construction_row'])==(c['member'],c['active_row'],c['construction_row']),'exact family row alignment')
  if invariant(r)==target(s):hits.append({'literal_input':i,'member':r['member'],'active_row':r['active_row'],'class_id':c['class_id'],'representative':c['representative_input_row']})
 need(hits,'no matching family')
 need(len({x['class_id'] for x in hits})==1,'not a unique compatible class')
 need(hits[0]['class_id']==s['expected_class'],'expected actual class')
 return hits

def evaluate(S):
 ids=read(HERE/'source_identifiers.json')['identifiers']
 hs=read(S/'topic_D_L096_HS_extension/eligibility_results.json')['rows']
 hp=read(S/'topic_D_L096_HS_extension/family_partition.json')['rows']
 shadows=read(S/'topic_D_L096_HS_extension/shadow_results.json')['rows']
 j2=read(S/'topic_D_L096_J2_extension/results.json')['rows']
 result=[]
 for s in ids:
  if s['source']=='L091':
   hits=unique_classes(hs,hp,s);rep=hits[0]['representative'];r=next(x for x in shadows if x['literal_input_row']==rep)
   result.append({'source_identifier':s['key'],'matching_inputs':hits,'current_class':hits[0]['class_id'],'IP':r['IP'],'WIP':r['WIP'],'L096_historical_label':s['L096_label']})
  else:
   hits=[x for x in j2 if invariant(x)==target(s)]
   need(len(hits)==1,'unique complete J2 family');r=hits[0]
   need(r['construction_row']==s['expected_prior_representative'],'exact J2 prior row')
   need(s['L096_label'] is None,'unproved supplemental rank prefix')
   result.append({'source_identifier':s['key'],'prior_representative':r['construction_row'],'IP':r['IP'],'WIP':r['WIP'],'L096_historical_label':None})
 claims=read(S/'topic_D_L096_volume/historical_label_claims.json')['claims']
 result.append(singleton_bridge(S))
 resolved=[x for x in claims if (x['group']=='HS' and x['label']=='3.2') or (x['group']=='M12' and x['label']=='5.1')]
 need(len(claims)==232 and len(resolved)==4 and all(x['claim']=='IP' for x in resolved),'exact positive source occurrences')
 return {'status':'AUTHOR_BOUNDED_IDENTIFICATION_PENDING_DISTINCT_REVIEW','identifications':result,'resolved_label_claim_occurrences':resolved,'remaining_positive_label_occurrences':228,'historical_completeness_premise':'Exact HS source roster completeness remains retained, as in its accepted packet; J2 and M12 use the accepted complete censuses.','new_group_run':False,'new_source_intake':False,'full_L096_recovery':False},(ids,hs,hp,j2)

def validate_singleton_census(c):
 need(c['status']=='passed' and len(c['borel_anchors'])==147 and all(x['exhaustion_complete'] for x in c['borel_anchors']),'complete 147-anchor prior census')
 need(c['counts']['automorphism_and_type']['5']==1,'unique prior rank-five class')
 w=[x for x in c['verified_witnesses'] if x['rank']==5]
 need(len(w)==1 and w[0]['id']==55 and w[0]['all_requested_axioms'] and w[0]['twot'],'exact eligible census witness55')
 return w[0]

def singleton_bridge(S):
 c=read(S/'phase6_sporadic_M12_certificate.json');w=[validate_singleton_census(c)]
 comp=read(S/'phase6_sporadic_M12_archive_compare.json')
 cv=[x for x in comp['coverage'] if x['member']=='m12.rk5']
 need(len(cv)==1 and cv[0]['matches_complete_census'] and cv[0]['expected_classes']==cv[0]['matched_classes']==[55],'rank5 complete coverage')
 matches=[x for x in comp['matches'] if x['member']=='m12.rk5']
 need(len(matches)==1 and matches[0]['raw_id']==1 and matches[0]['census_id']==55 and matches[0]['twot'],'literal source family map')
 rr=[x for x in read(S/'topic_D_L096_extended_candidate/mathieu_results.json')['rows'] if x['member']=='m12.rk5']
 need(len(rr)==1,'one exact shadow input');r=rr[0]
 need(r['active_row']==r['construction_row']==1 and r['borel_order']==3 and sorted(r['parabolic_orders'])==sorted(w[0]['parabolic_orders']) and all(r['filters'].values()),'same actual rank5 family')
 need([(x['rank'],x['IPk'],x['WIPk']) for x in r['by_rank']]==[(2,True,True),(3,True,True),(4,True,True),(5,False,False)],'complete rank-wise predicates')
 return {'source_identifier':'M12.5.1','prior_representative':55,'method':'singleton complete broader census plus exact archive map','IP':False,'WIP':False,'IP3':True,'IP4':True,'WIP5':False,'L096_historical_label':'5.1'}

def archive_conflict(S):
 with tarfile.open(S/'sources/L096_supplementary_archive.tar') as tf:
  doc=tf.extractfile('README').read().decode()
 need("sequence number 2 in 'geo' corresponds to geometry 4.1 in reference [20]" in doc,'exact historical example')
 part=read(S/'topic_D_L096_HS_extension/family_partition.json')['rows']
 p=[x for x in part if x['member']=='hs.rk4' and x['active_row']==2]
 need(len(p)==1 and p[0]['construction_row']==2,'literal final position2')
 r=next(x for x in read(S/'topic_D_L096_HS_extension/shadow_results.json')['rows'] if x['literal_input_row']==p[0]['representative_input_row'])
 need([(x['IPk'],x['WIPk']) for x in r['by_rank'] if x['rank'] in [3,4]]==[(False,False),(False,False)],'actual negative example')
 claims=[x for x in read(S/'topic_D_L096_volume/historical_label_claims.json')['claims'] if x['group']=='HS' and x['label']=='4.1']
 need(len(claims)==3 and all(x['claim']=='IP' and x['source_reference']==21 for x in claims),'printed positive claims and distinct reference number')
 return {'status':'INCOMPATIBLE_EDITION_ROUTES_NOT_AN_EXTERNAL_LABEL_IDENTIFICATION','archive_member':'hs.rk4','final_slot':2,'literal_reference_number':20,'table_reference_number':21,'actual_class':p[0]['class_id'],'actual_IP3':False,'actual_IP4':False,'actual_full_IP':r['IP'],'positive_table_occurrences':len(claims),'erroneous_link_not_determined':True}

def hs_rank_six(S):
 p=read(S/'topic_D_L096_HS_extension/family_partition.json')
 need(p['census_completeness_retained_source_only'] is True,'global HS completeness remains retained, not recomputed')
 c=[x for x in p['classes'] if x['member']=='hs.rk6']
 need(len(c)==1 and c[0]['class_id']==80 and c[0]['representative_input_row']==124,'unique retained rank-six family')
 r=[x for x in read(S/'topic_D_L096_HS_extension/shadow_results.json')['rows'] if x['rank']==6]
 need(len(r)==1 and r[0]['literal_input_row']==124 and r[0]['active_row']==1 and r[0]['member']=='hs.rk6','same actual rank-six family')
 need([(x['rank'],x['IPk'],x['WIPk']) for x in r[0]['by_rank']]==[(2,True,True),(3,False,False),(4,False,False),(5,False,False),(6,False,False)],'rank-six accepted quantifiers')
 return {'source_identifier':'HS.6.1','source_physical_page':6,'claim':'not WIP6','claim_category':'separate unnumbered negative claim, outside232positive occurrences','actual_class':80,'literal_input_row':124,'member':'hs.rk6','active_row':1,'retained_global_classification':True,'WIP6':False,'new_group_run':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=True);need(not any(a.out.iterdir()),'fresh output required')
 if (HERE/'manifest.json').exists():
  for b in read(HERE/'manifest.json')['exports']:
   f=HERE/b['path'];need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'frozen own export '+b['path'])
 for b in read(HERE/'bindings.json')['inputs']:
  f=a.study_root/b['path'];need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'fixed dependency '+b['path'])
 result,data=evaluate(a.study_root);result['archive_conflict']=archive_conflict(a.study_root);result['additional_negative_identification']=hs_rank_six(a.study_root);ids,hs,hp,j2=data;controls=[]
 def rejected(name,fn):
  try:fn()
  except (ValueError,StopIteration,KeyError):controls.append(name);return
  raise ValueError('control accepted '+name)
 rejected('drop literal HS input',lambda:unique_classes(hs[:-1],hp[:-1],ids[0]))
 z=copy.deepcopy(ids[0]);z['type_sizes'][0]=177;rejected('wrong source type size',lambda:unique_classes(hs,hp,z))
 z=copy.deepcopy(ids[0]);z['borel_order']=360;rejected('wrong source Borel',lambda:unique_classes(hs,hp,z))
 z=copy.deepcopy(hp);z[2]['class_id']=999;rejected('equal invariants do not merge inequivalent classes',lambda:unique_classes(hs,z,ids[0]))
 z=copy.deepcopy(hp);z[1]['active_row']=99;rejected('row position cannot replace exact alignment',lambda:unique_classes(hs,z,ids[0]))
 z=copy.deepcopy(ids[0]);z['expected_class']=1;rejected('positive result cannot identify a different name',lambda:unique_classes(hs,hp,z))
 rejected('J2 supplemental name remains unsupported',lambda:need(all(x['L096_label'] is None for x in [{**ids[2],'L096_label':'4.1'}]),'unproved supplemental prefix'))
 for identifier in ['J1.4.1','HS.3.1']:
  rejected('unverified '+identifier,lambda identifier=identifier:need(identifier in [x['source_identifier'] for x in result['identifications'] if x['L096_historical_label'] is not None],'no primary numeric-name bridge'))
 z=copy.deepcopy(read(a.study_root/'phase6_sporadic_M12_certificate.json'));z['borel_anchors'][0]['exhaustion_complete']=False
 rejected('observed singleton with incomplete census',lambda:validate_singleton_census(z))
 z=copy.deepcopy(read(a.study_root/'phase6_sporadic_M12_certificate.json'));z['counts']['automorphism_and_type']['5']=2
 rejected('multiple complete rank5 classes cannot identify a name',lambda:validate_singleton_census(z))
 (a.out/'identifications.json').write_text(json.dumps(result,indent=2)+'\n')
 if (HERE/'identifications.json').exists():need(read(HERE/'identifications.json')==result,'exact regenerated identification')
 pages=None
 if a.render:
  from pypdf import PdfReader
  rdir=a.out/'render';rdir.mkdir();shutil.copy2(HERE/'identifying_geometries.tex',rdir)
  for k in range(2):
   r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','identifying_geometries.tex'],cwd=rdir,capture_output=True,text=True)
   (rdir/f'pass{k}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'render')
  log=(rdir/'identifying_geometries.log').read_text();need(not any(x in log for x in ['LaTeX Warning:','Overfull','Underfull']),'clean render')
  after=[p.extract_text() for p in PdfReader(rdir/'identifying_geometries.pdf').pages];pages=len(after)
  if (HERE/'identifying_geometries.pdf').exists():need(after==[p.extract_text() for p in PdfReader(HERE/'identifying_geometries.pdf').pages],'exact page texts')
 report={'status':'PASS_BOUNDED_SOURCE_IDENTIFICATION','all_HS_inputs':124,'HS_actual_classes':80,'complete_J2_rank4_classes':3,'explicit_numeric_names_resolved':2,'positive_claim_occurrences_resolved':4,'remaining':228,'separate_negative_names_proved':1,'controls':controls,'render_pages':pages,'group_or_census_replay':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
