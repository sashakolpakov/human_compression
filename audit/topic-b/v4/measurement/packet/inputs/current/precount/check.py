#!/usr/bin/env python3
"""Exact pre-count boundary, without PDF extraction, metrics or finite searches."""
from pathlib import Path
import argparse,json,hashlib,copy
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads((H/p).read_text())
def binding(p,r):
 b=p.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact '+str(p))
def semantic(p,d,r):
 need(p['originals']==['N001','N003','N008','L030','L040','L047'],'six exact originals')
 need(p['common_components']==['U_B','U_B6']and p['applications']==['B1','B2','B3','B4','B5','B6'],'two full commons and six apps')
 need(p['primary']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace',N001='unchanged literal authored rendering; not an original PDF coordinate'),'preserve raw primary and N001 rendering')
 need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected']and p['normalizations']==['NFC','NFKC']and p['units']==UNITS,'all thirty coordinates')
 need(p['whole_common_charged_once_each']and p['no_logical_reduction_discount']and p['all_six_complete_applications']and p['full_finite_proof_body_in_new_common']and not p['archived_two_page_finite_note_double_charged'],'complete paid premises, no omission or duplicated finite proof')
 need([x['key']for x in d['documents']]==['U_B','B1','B2','B3','B4','B5','CODE','L047','U_B6','B6','CODE6'],'full document roster')
 need([x['pages']for x in d['documents']]==[16,3,4,4,5,11,7,12,10,3,7],'all whole page boundaries')
 need(len(r['files'])==17 and len({x['file']['sha256']for x in r['files']})==17,'seventeen distinct complete raw files')
 need(sum(x['category']=='programs'for x in r['files'])==10 and sum(x['category']=='drivers'for x in r['files'])==5 and sum(x['category']=='formal'for x in r['files'])==2,'program/driver/formal categories')
 need(all('required' in x['role']for x in r['files']if x['id'].startswith('NEW_PROGRAM')),'six complete required programs')
 need(r['partial_declarations']==14 and r['new_declarations']==0 and r['whole_file_only']and r['raw_and_printed_program_representations_are_alternatives'],'formal scope and alternative representation')
 need(p['optional_validation_excluded_both_sides']and p['required_certificates_remain_required']and all(p[x]is None for x in ['software_inclusive_comparison','source_software_cost','full_graphics_cost','external_proofs_cost','factors']),'matched software/unknown boundary')
 need(p['science_adopted']and not p['input_accepted']and not p['new_counts_evaluated']and not any(p[x]for x in ['new_source_credit','new_question_credit','new_formal_credit']),'pre-count status')
 need((p['retained_source_cells'],p['retained_article_only_cells'],p['retained_own_PDF_cells'],p['retained_raw_cells'],p['new_PDF_cells'],p['new_raw_cells'])==(150,30,210,80,120,90),'exact retained/new cell dimensions')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output file')
 p,d,r=load('policy.json'),load('documents.json'),load('raw_inventory.json');semantic(p,d,r)
 roots={'study':a.study_root,'public':a.public_root};b=load('bindings.json')
 for x in b['references']:binding(roots[x['root']]/x['path'],x)
 for x in b['baseline_files']:
  binding(H/'baseline'/x['path'],x);binding(a.public_root/b['baseline_origin']/x['path'],x)
 for x in d['documents']:binding(roots[x['file']['root']]/x['file']['path'],x['file'])
 for x in r['files']+r['archival_review_tools']:
  y=x['file'];binding(roots[y['root']]/y['path'],y)
  for y in x.get('aliases',[]):binding(roots[y['root']]/y['path'],y)
 for x in load('tex_closure.json')['files']:
  y=x['file'];binding(roots[y['root']]/y['path'],y)
 if(H/'manifest.json').exists():
  for x in load('manifest.json')['exports']:binding(H/x['path'],x)
 controls=[]
 edits=[('drop source',lambda p,d,r:p['originals'].pop()),('discount old common',lambda p,d,r:p.update(no_logical_reduction_discount=False)),('trim common',lambda p,d,r:d['documents'][0].update(pages=15)),('drop old app',lambda p,d,r:d['documents'].pop(1)),('drop new references',lambda p,d,r:d['documents'][-2].update(pages=2)),('omit finite roster',lambda p,d,r:r['files'].pop(13)),('promote validation',lambda p,d,r:p.update(optional_validation_excluded_both_sides=False)),('source software zero',lambda p,d,r:p.update(source_software_cost=0)),('both program alternatives charged',lambda p,d,r:r.update(raw_and_printed_program_representations_are_alternatives=False)),('invent original PDF',lambda p,d,r:p['primary'].update(N001='original PDF')),('duplicate finite proof',lambda p,d,r:p.update(archived_two_page_finite_note_double_charged=True)),('new Lean credit',lambda p,d,r:r.update(new_declarations=14)),('premature factor',lambda p,d,r:p.update(factors=1)),('change old source cells',lambda p,d,r:p.update(retained_source_cells=140)),('omit unit',lambda p,d,r:p['units'].pop())]
 for name,f in edits:
  z=copy.deepcopy((p,d,r));f(*z)
  try:semantic(*z)
  except(ValueError,KeyError):controls.append(name)
  else:raise ValueError('control survived '+name)
 report=dict(status='PASS_PRECOUNT_BOUNDARY',controls=controls,originals=6,new_metric_evaluation=False,factors=None,programs_executed=False,formal_executed=False)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
