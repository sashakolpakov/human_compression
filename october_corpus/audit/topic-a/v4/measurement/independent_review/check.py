#!/usr/bin/env python3
"""Bound distinct A9 arithmetic review; no numerical-author helper imports."""
from pathlib import Path
import argparse, copy, hashlib, json
from pypdf import PdfReader
from derive import need, PRIMARY, SOURCES, PAIRS, VARIANTS, NORMS, UNITS
from review_numeric import run
from geometry_review import expected
from geometry_parser import compare_geometry

HERE=Path(__file__).resolve().parent
PIN='0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'
POLICY='38917fe6993adcb7cbf6f67311030d7c00ee8008ff774a0947638944d142d7ec'
INPUTS={
 'inputs/input/manifest.json':'9b754940f2edee8ba7e3bf4010f236613040f850bca3ad440d3e5a6876fedd7f',
 'inputs/input_review/manifest.json':'44ce9b72aef085d1bcbc243564e1b402980ae065ca0140971b0957cb583908dd',
 'inputs/input_adoption/manifest.json':'a544128754789f9d2a5b65c73d7b85fb0140e156e27330ed4a51083f1696a4da',
 'prior/root_adoption/manifest.json':'aa51838885a49341e60e3b34978116a3b5ac798f418f4697960856d93dc93dd9'}
PRIOR='cc2211a4fb04f7119abadce8969926043e046056b18961311ef198238ed12f70'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(root,row):
 p=Path(row['path']);need(not p.is_absolute() and '..'not in p.parts,'relative safe export')
 b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact export '+str(p))
def verify_manifest(root,pin):
 p=root/'manifest.json';need(sha(p.read_bytes())==pin,'trusted frozen manifest '+str(root))
 m=read(p);need(len({r['path']for r in m['exports']})==len(m['exports']),'unique export paths')
 for row in m['exports']:bind(root,row)
 return len(m['exports'])
def roles(r):
 need(r['protocol']['sha256']==POLICY and r['field']=='roles.disclosure','explicit frozen protocol correction')
 want={'current_numerical_author':'rewrite_termination','L121_application_assembly_author':'root','new_input_author':'enumeration_volume','prior_eight_original_numerical_author':'enumeration_volume','scheduled_distinct_numerical_reviewer':'enumeration_volume'}
 need(all(r['corrected_roles'][k]==v for k,v in want.items()),'actual distinct and prior roles')
 need(r['changes_to_protocol_bytes']is False and r['changes_to_metric_or_graphs']is False,'role-only clarification')
def reader(packet,o):
 pages=PdfReader(packet/'reader.pdf').pages;need(len(pages)==4,'complete four reader pages')
 texts=[p.extract_text()or''for p in pages];plain=' '.join(' '.join(texts).split())
 p=o['primary'];need(p['written']['display_six']in texts[0],'rendered whole exact rounded fraction')
 for src in SOURCES:need(p['conditional'][src]['display_six']in texts[0],'rendered individual exact rounded fraction '+src)
 for v in VARIANTS:
  for n in NORMS:
   for u in UNITS:need(o['coordinates']['/'.join([v,n,u])]['written']['display_six']in texts[3],'rendered whole sensitivity exact rounding')
 for phrase in ['L121 uses no sibling application','Required programs and data remain premises','no software-inclusive or optional-validation-inclusive factor','No complete printed repre','unknown, not zero','not a new mathematical claim']:
  need(phrase in plain,'actual reader boundary '+phrase)
 return {'pages':4,'primary_fraction_displays':10,'whole_sensitivity_displays':30,'page_text_sha256':[sha(t.encode())for t in texts]}
def main():
 a=argparse.ArgumentParser();a.add_argument('--author-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);q=a.parse_args()
 need(not q.out.exists(),'fresh output');q.out.mkdir(parents=True);packet=q.author_root
 count=verify_manifest(packet,PIN);accepted={}
 for name,pin in INPUTS.items():accepted[name]=verify_manifest((packet/name).parent,pin)
 need(sha((packet/'protocol.json').read_bytes())==POLICY,'fixed protocol')
 need(sha((packet/'prior/numerical_manifest.json').read_bytes())==PRIOR,'accepted prior numerical manifest')
 old={r['path']:r for r in read(packet/'prior/numerical_manifest.json')['exports']}
 for name in ['results.json','protocol.json']:bind(packet/'prior',old[name])
 adoption=read(packet/'inputs/input_adoption/adoption.json');need(adoption['numerical_comparison_authorized']and adoption['status']=='ROOT_ACCEPTED_COMPLETE_ADDITIVE_INPUT_BOUNDARY','authorized adopted input boundary')
 r,o=run(packet);role=read(packet/'role_clarification.json');roles(role)
 for field,value in [('L121_application_assembly_author','rewrite_termination'),('current_numerical_author','enumeration_volume')]:
  changed=copy.deepcopy(role);changed['corrected_roles'][field]=value
  try:roles(changed)
  except ValueError:r['controls'].append('false role '+field)
  else:raise ValueError('role corruption survived')
 plot=read(packet/'plot_data.json');need(plot['primary_coordinate']==PRIMARY,'graph primary coordinate')
 for stem in ['costs','cumulative']:compare_geometry(plot[stem]['expected_rectangles'],expected(o,stem))
 r.update(status='PASS_DISTINCT_ADDITIVE_A9_NUMERICAL_REVIEW',author_manifest_sha256=PIN,author_exports=count,accepted_packet_exports=accepted,reader=reader(packet,o),role_clarification_checked=True,reviewer_prior_roles=['Authored accepted L121 inputs; not independently re-adjudicated here','Authored prior A8 numerical mechanics; current integer/gcd derivation and geometry expectations independently written'],fresh_source_extraction=False,scientific_or_Lean_replay=False)
 if(HERE/'manifest.json').exists():
  for row in read(HERE/'manifest.json')['exports']:bind(HERE,row)
 (q.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');(q.out/'independent_derivation.json').write_text(json.dumps(o,indent=2)+'\n')
 print(json.dumps({k:r[k]for k in ['status','exact_fractions','unchanged_conditional_fractions','CSV_rows','whole_files']}))
if __name__=='__main__':main()
