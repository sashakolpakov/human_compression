#!/usr/bin/env python3
"""Check the additive precount boundary without extracting or scoring new text."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError('L121_INPUT_POLICY: '+m)
def read(n):return json.loads((HERE/n).read_text())
def bound(p,e):
 b=p.read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'exact binding '+str(p))
def semantic(p,d,r,b,a):
 old=read('baseline/policy.json');need(p['source_ids']==old['source_ids']+['L121']and p['source_to_application']==dict(old['source_to_application'],L121='A9'),'one exact additional source')
 need(p['primary']==old['primary']and p['variants']==old['variants']and p['normalizations']==old['normalizations']and p['metrics']==old['metrics'],'identical inherited primary and30-coordinate policy')
 need(p['common_documents']==['U']and p['common_pages']==23 and p['application_pages']==56 and p['source_pages']==131 and p['pdf_documents']==22 and p['physical_pages']==240,'complete22-document boundary')
 need(p['complete_program_appendices']==old['complete_program_appendices']and p['program_appendix_pages']==30 and d['new_program_appendix']is None,'no invented complete enlarged appendix')
 need(p['required_complete_files']==20 and p['raw_files']==45 and p['partial_formal_modules']==15 and p['all_raw_formal_files']==16 and p['current_operational_drivers']==6,'complete roles')
 need(p['inherited_PDF_metric_cells']==600 and p['inherited_raw_metric_cells']==300 and p['expected_new_PDF_metric_cells']==60 and p['expected_new_raw_metric_cells']==150 and not p['new_metrics_evaluated'],'old cells preserved and new scoring pending')
 need(not p['science_acceptance_pending']and p['input_acceptance_pending']and p['ratios']is None and p['symmetric_software_factors']is None and all(v==0 for v in p['new_credit'].values()),'no premature numeric acceptance/credit')
 need('nine source and ten replacement'in p['symmetric_listing_policy']and 'twenty files'in p['symmetric_listing_policy'],'updated symmetry prose')
 need(len(d['documents'])==22 and sum(x['pages']for x in d['documents'])==240 and[d['documents'][-2]['id'],d['documents'][-1]['id']]==['L121','A9'],'complete new PDFs')
 need(all(x['whole_document']for x in d['documents'])and[d['documents'][-2]['pages'],d['documents'][-1]['pages']]==[12,11],'whole source and application')
 need(len(r['files'])==45 and len({x['file']['sha256']for x in r['files']})==45 and r['duplicate_content_groups']==[]and all(x['whole_file']for x in r['files']),'actual whole-content uniqueness')
 need([x['inherited_record']for x in r['files'][:30]]==read('baseline/raw_inventory.json'),'all30 prior raw records unchanged')
 new=r['files'][30:];need(sum(x['mathematical_premise']for x in new)==9,'all9 new required files')
 relation=next(x for x in new if x['file']['path'].endswith('cubic_relation/check.py'));need(relation['role']=='required_program'and relation['mathematical_premise'],'coordinate calculation remains required')
 wrapper=next(x for x in new if x['file']['path']=='topic_A_L121_application/check.py');need(wrapper['role']=='operational_validation_runner'and not wrapper['mathematical_premise'],'top wrapper inventory')
 need(a['common_acquired_in_full']and not a['sibling_application_premise']and len(a['required_new_file_ids'])==9 and len(a['required_old_file_ids'])==11 and not a['full_Lean'],'actual complete acquisition')
 need(b['L121_scientific_acceptance']['root_adoption']['sha256']=='38901fc13359b1124ee2bbb005b7ac445aca47163ef16dcf62db5bc26f5c04f6'and b['L121_input_acceptance']is None,'actual science/pending input chain')
 return True

def controls(args):
 changes=[('drop common',lambda x:x[0].update(common_pages=0)),('primary switching',lambda x:x[0]['primary'].update(variant='raw_untrimmed')),('partial source',lambda x:x[1]['documents'][-2].update(pages=11)),('partial application',lambda x:x[1]['documents'][-1].update(whole_document=False)),('invent full printed code',lambda x:x[1].update(new_program_appendix='old CODE_A')),('drop required role',lambda x:x[2]['files'][30].update(mathematical_premise=False)),('omit wrapper',lambda x:x[2]['files'].pop()),('dedup distinct contents',lambda x:x[2]['files'][-1]['file'].update(sha256=x[2]['files'][0]['file']['sha256'])),('free sibling',lambda x:x[4].update(sibling_application_premise=True)),('unknown software zero',lambda x:x[0].update(symmetric_software_factors=0)),('premature input acceptance',lambda x:x[0].update(input_acceptance_pending=False)),('alter old raw role',lambda x:x[2]['files'][0]['inherited_record'].update(role='optional_validation')),('stale source count',lambda x:x[0].update(symmetric_listing_policy='eight sources')),('new source credit',lambda x:x[0]['new_credit'].update(source=1))];done=[]
 for name,f in changes:
  a=copy.deepcopy(args);f(a)
  try:semantic(*a)
  except(ValueError,KeyError,StopIteration):done.append(name)
  else:raise ValueError('mutation survived '+name)
 return done

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh report');roots=dict(study=a.study_root,public=a.public_root)
 if(HERE/'manifest.json').exists():
  for e in read('manifest.json')['exports']:bound(HERE/e['path'],e)
 p,d,r,b,ac=[read(n)for n in['policy.json','documents.json','raw_inventory.json','bindings.json','acquisition_routes.json']]
 for e in b['references']:bound(roots[e['root']]/e['path'],e)
 for e in b['baseline_copy_files']:bound(HERE/e['path'],e)
 for row in d['documents']+r['files']:
  e=row['file'];bound(roots[e['root']]/e['path'],e)
 spec=json.loads((a.public_root/'audit/topic-a/v3/measurement/packet/inputs/input/input_spec.json').read_text())
 for row in d['documents'][:20]:need(row['pages']==spec[row['id']]['pages']and row['file']['sha256']==spec[row['id']]['file']['sha256'],'old PDF untouched')
 old=read('baseline/author_counts.json');need(old==json.loads((a.public_root/'audit/topic-a/v3/measurement/packet/inputs/input/author_counts.json').read_text()),'all old count vectors byte-equivalent data')
 semantic(p,d,r,b,ac);report=dict(status='PASS_PRECOUNT_BOUNDARY_NO_NEW_COUNTS',inherited_PDF_cells=600,inherited_raw_cells=300,complete_documents=22,physical_pages=240,new_source_application_pages=[12,11],whole_raw_contents=45,unchanged_raw_contents=30,new_required_files=9,new_optional_validation_files=0,new_operational_runners=4,new_formal_files=2,controls=controls((p,d,r,b,ac)),new_text_extraction=False,new_metric_evaluation=False,science_execution=False,formal_execution=False,factors=None)
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
