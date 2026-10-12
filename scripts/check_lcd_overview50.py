#!/usr/bin/env python3
"""Verify the separately adopted LCD overview and its actual programme routes."""
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path

def need(x,m):
 if not x:raise ValueError('OVERVIEW50: '+m)
def verify(root):
 def read(p):return json.loads((root/p).read_text())
 def bind(e):
  p=Path(e['path']);need(not p.is_absolute() and '..' not in p.parts,'relative binding');b=(root/p).read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'exact '+str(p))
 base='audit/overview/v16/';a=read(base+'admission.json')
 need(hashlib.sha256((root/base/'admission.json').read_bytes()).hexdigest()=='f7bd328069d7813cb7156b6673253ecfe7df072be7a5197a82753f2e104ea193','root admission pin')
 need(a['status']=='ROOT_ADMITTED_LCD_OVERVIEW50','accepted root status')
 for k in ['author_manifest','independent_manifest','previous_overview','previous_overview_pointer','current_corpus','current_catalogue','active_original_catalogue','original_registration','registration_report','programme_review']:bind(a[k])
 for e in a['scientific_and_numerical_admissions']:bind(e)
 for key,pin in [('author_manifest','b0b4aa864b41166ff578ba00715f8ea431c1555e2c1ee04431b04584af8de9fa'),('independent_manifest','fcb5352421e72ccfba49827aaefd6dc615800eed1a2dd8dd17f4a011789dbfa6')]:
  row=a[key];need(row['sha256']==pin,'accepted author/review identity')
  for e in read(row['path'])['exports']:bind(dict(e,path=str(Path(row['path']).parent/e['path'])))
 for k,v in dict(topic_count=19,distinct_originals=50,active_originals=106,pending_originals=56,archived_originals=55,exact_fractions=69,actual_SVG_bars=157,actual_PDF_bars=157,reader_pages=6,unchanged_topic_records=18,unchanged_other_individual_records=48,unchanged_prior_fractions=66).items():need(a[k]==v,'scope '+k)
 need(a['newly_registered_originals']==['L050','F017'] and a['new_source_credit']==a['new_question_credit']==a['new_formal_credit']==0 and a['software_inclusive_factors'] is a['source_software_cost'] is a['pooled_factor'] is None and a['required_program_roles_preserved'] and a['no_cross_topic_discount'],'credit and costs')
 r=read(base+'packet/results.json');old=read(a['previous_overview']['path']);need(r['topics'][:18]==old['topics'] and len(r['topics'])==19,'preserved18topicobjects')
 need(read(base+'packet/inputs/previous_results.json')==old and read(base+'packet/inputs/numbers_results.json')==read('audit/topic-lcd/v1/measurement/packet/results.json'),'actual accepted numerical routes')
 cur=read('audit/corpus/latest.json');need(set(r['original_ids'])==set(cur['measured_original_ids']) and cur['currently_measured_originals']==50,'corpus agrees')
 ptr=read('audit/overview/latest.json');need(ptr['admission']['path']==base+'admission.json' and ptr['reader']['path']==base+'packet/reader.pdf' and ptr['recovered_originals']==ptr['historically_measured_originals']==ptr['current_conditional_factors']==50 and ptr['topics']==ptr['current_whole_factors']==19 and ptr['pending_accessible_originals']==56,'current pointer')
 for k in ['admission','reader','counts_source','measurement_policy','measurement_policy_reader','measurement_policy_review']:bind(ptr[k])
 review=read(base+'independent_review/review.json');need(review['status']=='ROOT_ACCEPTED_CONSOLIDATED_OVERVIEW50' and not review['corrections_requested'] and review['role_disclosure'] and review['author_manifest_sha256']==a['author_manifest']['sha256'],'separate root review')
 spec=importlib.util.spec_from_file_location('overview50_distinct_root',root/base/'independent_review/check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 need(m.check(root/base/'packet',root)==read(base+'independent_review/report.json'),'independent arithmetic/actualvector replay')
 visual=read(base+'independent_review/visual_review.json');need(visual['pages']==6 and visual['reader_sha256']==hashlib.sha256((root/base/'packet/reader.pdf').read_bytes()).hexdigest(),'all six pages viewed')
 text=(root/'README.rst').read_text();need(base+'packet/reader.pdf' in text and '50 accessible originals' in text and 'fifty individual' in text,'current readable summary')
 return 69,157
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);print(verify(p.parse_args().repo))
