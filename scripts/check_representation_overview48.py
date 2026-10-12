#!/usr/bin/env python3
"""Current v15 overview, requiring a real separately frozen root acceptance."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

def need(x,m):
 if not x:raise ValueError('OVERVIEW48: '+m)
def verify(root,allow_pending=False):
 def read(p):return json.loads((root/p).read_text())
 def bind(e):
  p=Path(e['path']);need(not p.is_absolute()and '..'not in p.parts,'unsafe binding');b=(root/p).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'binding '+str(p))
 base='audit/overview/v15/';a=read(base+'admission.json');pending=a['independent_manifest']is None
 need((allow_pending and pending and a['status']=='PROPOSED_OVERVIEW48_AWAITING_DISTINCT_ROOT_REVIEW')or(not pending and a['status']=='ROOT_ADMITTED_REPRESENTATION_OVERVIEW48'),'distinct root overview acceptance missing')
 for key in ['author_manifest','previous_overview','previous_overview_pointer','current_corpus','current_catalogue','active_original_catalogue','original_registration','registration_report']:bind(a[key])
 for row in a['scientific_and_numerical_admissions']:bind(row)
 need(a['author_manifest']['sha256']=='c44d8d9aa6cddc9127d1d11493dad747b623efe207a42f6e24a94e2394e69b8a','author overview pin')
 for row in [a['author_manifest']]+([]if pending else[a['independent_manifest']]):
  bind(row)
  for e in read(row['path'])['exports']:bind(dict(e,path=str(Path(row['path']).parent/e['path'])))
 for k,v in dict(topic_count=18,distinct_originals=48,active_originals=106,pending_originals=58,archived_originals=55,exact_fractions=66,actual_SVG_bars=150,actual_PDF_bars=150,reader_pages=6,unchanged_topic_records=17,unchanged_other_individual_records=46).items():need(a[k]==v,'summary '+k)
 need(a['newly_registered_originals']==['L126']and a['new_source_credit']==a['new_question_credit']==a['new_formal_credit']==0 and a['software_inclusive_factors']is a['source_software_cost']is a['pooled_factor']is None and a['required_program_roles_preserved']and a['no_cross_topic_discount'],'scope/unknown credit')
 result=read(base+'packet/results.json');old=read(a['previous_overview']['path']);need(result['original_manuscript_count']==48 and result['topic_count']==18,'overview count')
 before={t['topic']:t for t in old['topics']};after={t['topic']:t for t in result['topics']};need(set(before)==set(after)and {k for k in before if before[k]!=after[k]}=={'Representation'},'17 exact unchanged topics')
 need(read(base+'packet/inputs/previous_results.json')==old and read(base+'packet/inputs/numbers_results.json')==read('audit/topic-representation/v3/measurement/packet/results.json'),'actual accepted result routes')
 cur=read('audit/corpus/latest.json');need(set(result['original_ids'])==set(cur['measured_original_ids'])and cur['currently_measured_originals']==48,'corpus/overview agree')
 ptr=read('audit/overview/latest.json');need(ptr['admission']['path']==base+'admission.json'and ptr['reader']['path']==base+'packet/reader.pdf'and ptr['recovered_originals']==ptr['historically_measured_originals']==ptr['current_conditional_factors']==48 and ptr['topics']==ptr['current_whole_factors']==18 and ptr['pending_accessible_originals']==58,'current overview pointer')
 for k in ['admission','reader','counts_source','measurement_policy','measurement_policy_reader','measurement_policy_review']:bind(ptr[k])
 # Isolate familiar module names: earlier checkers also have build.py/plotting.py.
 names=['build','reader','plotting','geometry_checks'];saved={k:sys.modules.get(k)for k in names};path=root/base/'packet';sys.path.insert(0,str(path))
 for k in names:sys.modules.pop(k,None)
 try:
  spec=importlib.util.spec_from_file_location('representation_overview48_author',path/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);report=m.verify()
 finally:
  sys.path.pop(0)
  for k in names:
   sys.modules.pop(k,None)
   if saved[k]is not None:sys.modules[k]=saved[k]
 need(report['exact_fractions']==66 and report['actual_SVG_bars']==report['actual_PDF_bars']==150,'fresh arithmetic/vector replay')
 if not pending:
  review=read(base+'independent_review/review.json');need(a['independent_manifest']['sha256']=='d4f15eb92dae7d9231ac6eb9982af93f0ad7ba93fb99a4e65883517394827e3d'and review['status']=='ROOT_INDEPENDENT_OVERVIEW48_ACCEPTED'and not review['findings']and review['prior_role_disclosure']and review['author_manifest_sha256']==a['author_manifest']['sha256'],'real independent review status')
  spec=importlib.util.spec_from_file_location('root_overview48_review',root/base/'independent_review/check.py');reviewer=importlib.util.module_from_spec(spec);spec.loader.exec_module(reviewer)
  need(reviewer.check(root/base/'packet',root)==read(base+'independent_review/report.json'),'fresh distinct root arithmetic/vector replay')
 return (66,150)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--allow-pending-private',action='store_true');a=p.parse_args();print(verify(a.repo,a.allow_pending_private))
