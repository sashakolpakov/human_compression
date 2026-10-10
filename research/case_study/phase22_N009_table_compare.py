#!/usr/bin/env python3
"""Exact Table 6 comparison, with optional re-extraction of the private primary text."""
import argparse,hashlib,json,re
from collections import Counter
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--source-text',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args();ROOT=args.directory
SOURCE_HASH='091caf4266f2ac595aec76def47d451700fff7c80f6d0f3eabeee2e6f31f38e7'
rows=json.loads((ROOT/'phase22_N009_table6_rows.json').read_text())
if args.source_text:
 raw=args.source_text.read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_HASH
 lines=raw.decode().splitlines();parsed=[]
 for i,line in enumerate(lines):
  if not 800<=i<=1120:continue
  m=re.search(r'\{([\d,]+)\}',line)
  if not m:continue
  labels=[]
  for lo,hi in [(46,63),(63,79)]:
   text=line[lo:hi].replace('∗','').replace(' ','')
   if re.fullmatch(r'[ a-z]*',lines[i+1]) and lines[i+1].strip():text+=lines[i+1][lo:hi].strip()
   z=re.fullmatch(r'\[([\d,]+)\](\d+[a-z]?)',text);assert z,(i,text)
   labels.append('{'+z[1]+'}*'+z[2])
  tail=line[79:].split();assert len(tail)==2
  r=dict(source_line=i+1,type=list(map(int,m[1].split(','))),printed_labels=labels,universal_order=tail[0],count=int(tail[1]),labels=labels.copy(),orientation_note=None)
  if r['type']==[4,16,4]:
   assert r['labels'][1].startswith('{4,16}')
   r['labels'][1]=r['labels'][1].replace('{4,16}','{16,4}')
   r['orientation_note']='Printed vertex-figure type {4,16}; compare its dual {16,4} to match the ordered last two edge types. No count or letter changed.'
  parsed.append(r)
 assert parsed==rows,'Primary extraction differs from transcribed mathematical table'
assert len(rows)==107
dual=dict(json.loads((ROOT/'phase22_N009_atlas_duals.json').read_text()));dual.update(json.loads((ROOT/'phase22_N009_rank4_atlas_duals.json').read_text()))
def canonical(a,b):return min((a,b),(dual[b],dual[a]))
def compare(rank,filename):
 facets=json.loads((ROOT/filename).read_text());ordered=Counter();fixed=Counter()
 for key,typ,a,b,sd in facets:
  assert len(typ)==rank-1;c=canonical(a,b);ordered[c]+=1;fixed[c]+=int(sd)
 assert all((n+fixed[c])%2==0 for c,n in ordered.items())
 actual={c:(n+fixed[c])//2 for c,n in ordered.items()};expected={}
 for r in rows:
  if len(r['type'])!=rank-1:continue
  c=canonical(*r['labels']);assert c not in expected
  expected[c]=r['count']
 assert actual==expected,(actual,expected)
 return dict(ordered_markings=len(facets),self_dual_markings=sum(fixed.values()),classes=sum(actual.values()),source_rows=len(expected),all_labels_match=True,rows=[dict(labels=list(c),ordered=n,self_dual=fixed[c],up_to_reversal=actual[c],source_count=expected[c]) for c,n in sorted(ordered.items())])
finite=json.loads((ROOT/'phase22_N009_universal_orders.json').read_text())+json.loads((ROOT/'phase22_N009_universal5_orders.json').read_text())
actual_orders={tuple(labels):n for labels,n in finite};expected_orders={tuple(r['labels']):int(r['universal_order']) for r in rows if r['universal_order']!='∞'}
assert actual_orders==expected_orders and len(finite)==106
infinite=[r for r in rows if r['universal_order']=='∞'];assert len(infinite)==1 and infinite[0]['labels']==['{4,4}*128','{4,4}*64']
report=dict(schema_version=1,source_pdf='https://cdm.ucalgary.ca/article/download/62475/46803',source_extraction_expected_sha256=SOURCE_HASH,source_extraction_verified=args.source_text is not None,rank4=compare(4,'phase22_N009_facet_matches.json'),rank5=compare(5,'phase22_N009_rank5_facet_matches.json'),finite_universal_amalgams_verified=106,finite_universal_order_histogram=dict(Counter(str(n) for n in actual_orders.values())),infinite_universal_row_retained='McMullen–Schulte semidirect decomposition quoted as source Theorem 5.3; not a Todd–Coxeter result.',source_orientation_notes=[r for r in rows if r['orientation_note']],scope='All 107 Table 6 labels/counts and all 106 finite universal orders; four source vertex-type labels are explicitly dualized. No new whole-paper or priority claim.')
output=args.output or ROOT/'phase22_N009_table_compare.json';output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status='PASS',rank4={k:v for k,v in report['rank4'].items() if k!='rows'},rank5={k:v for k,v in report['rank5'].items() if k!='rows'},finite_universal_orders=106,primary_text_verified=report['source_extraction_verified'])))
