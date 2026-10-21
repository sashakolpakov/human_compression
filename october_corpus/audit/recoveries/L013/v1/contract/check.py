"""Assembly binding/scope replay only; no solver or uniform proof rerun."""
from pathlib import Path
import argparse,copy,hashlib,json
PIN_THEORY='4ec2b452fd3696928039395aadee00a8f0aca25ff372c44dabc03f8dbb305ea3'
HERE=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def binding(root,r):
 p=root/r['path'];need(p.is_file(),'file '+r['path']);b=p.read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'binding '+r['path'])
def semantics(c,s,w):
 need(c['status']=='COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_PROPOSED_FOR_ROOT_REVIEW' and not c['complete_original_admission_here'],'root adoption gate')
 need(c['source_id']=='L013' and c['source_rows']==45 and c['new_Lean']==0 and c['new_question_credit']==0 and c['measurement'] is None,'single original/no unearned credit')
 need(len(s['rows'])==45 and [r['id'] for r in s['rows']]==['L013.%02d'%i for i in range(1,46)],'complete fixed source disposition IDs')
 need(not s['all_literal_assertions_reproved'] and s['root_complete_adoption']=='PENDING','literal theorem-set and adoption limits')
 r={r['id']:r for r in s['rows']}
 need(r['L013.28']['disposition']=='REPROVED_WITH_EXPLICIT_RANGE' and 'not a proof of global nonexistence atq8' in r['L013.28']['qualification'],'type2 precise range')
 need('No exhaustive degree6' in r['L013.17']['qualification'],'degree6 witness boundary')
 need(r['L013.44']['disposition']=='UNANSWERED','future direction')
 need('not an unrooted invariant' in r['L013.39']['qualification'],'middle pair convention')
 need(sum(x['pages'] for x in w['scientific_documents'])==9 and [x['pages'] for x in w['scientific_documents']]==[5,4],'whole two papers')
 need(len(w['programs'])==6 and len(w['required_data'])==7 and w['formal_files']==[],'whole code/data inventory')
 need(sum(x['role'].startswith('REQUIRED') for x in w['programs'])==3,'three required finite programs')
 need(w['source_program_cost'] is None and w['solver_and_other_external_cost'] is None and w['compression_factor'] is None,'unknown not zero')
 need('saved positive rows do not prove absence' in w['finite_absence_dependency'],'exhaustion trust')
 return True

def main(a):
 if (HERE/'manifest.json').exists():
  for r in load(HERE/'manifest.json')['exports']:binding(HERE,r)
 b=load(HERE/'accepted_components.json');n=0
 for packet in b['components']:
  binding(a.study_root,packet['manifest'])
  for r in packet['exports']:binding(a.study_root,r);n+=1
 c=load(HERE/'principal_contract.json');s=load(HERE/'source_dispositions.json');w=load(HERE/'whole_boundary.json');semantics(c,s,w)
 binding(a.study_root,s['source'])
 for r in w['scientific_documents']+w['programs']+w['required_data']:binding(a.study_root,r)
 controls=[]
 def reject(name,which,mutation):
  data=copy.deepcopy([c,s,w]);mutation(data[which])
  try:semantics(*data)
  except ValueError as e:controls.append({'name':name,'rejection':str(e)});return
  raise ValueError('accepted control '+name)
 reject('claim complete source adoption',0,lambda z:z.update(complete_original_admission_here=True))
 reject('delete a source row',1,lambda z:z['rows'].pop())
 reject('literal theorem-set equivalence',1,lambda z:z.update(all_literal_assertions_reproved=True))
 reject('degree6 completeness',1,lambda z:z['rows'][16].update(qualification='All degree6 graphs'))
 reject('q8 global nonexistence',1,lambda z:z['rows'][27].update(qualification='No graph exists'))
 reject('chosen profile made invariant',1,lambda z:z['rows'][38].update(qualification='Intrinsic invariant'))
 reject('future question solved',1,lambda z:z['rows'][43].update(disposition='SOLVED'))
 reject('omit whole common',2,lambda z:z['scientific_documents'].pop(0))
 reject('required solver made optional',2,lambda z:z['programs'][0].update(role='OPTIONAL'))
 reject('unknown source software zero',2,lambda z:z.update(source_program_cost=0))
 result={'status':'PASS_COMBINED_CONTRACT_BINDING','source_rows':45,'components':4,'component_exports':n,'native_science_pages':9,'whole_programs':6,'required_data':7,'controls':controls,'expensive_scientific_rerun':False,'adoption':'PENDING_ROOT','new_credit':0}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='controls'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
