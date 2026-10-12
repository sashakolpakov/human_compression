#!/usr/bin/env python3
"""Root's independent overview arithmetic and vector audit.

The independent v16 fraction/CSV/geometry audit is adapted, with its unchanged
older vector parser. No current author arithmetic or plotting code is imported.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse, csv, hashlib, importlib.util, json
from pypdf import PdfReader

def need(x, m):
 if not x: raise ValueError(m)
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(a, b):
 f = Fraction(a,b)
 with localcontext() as c:
  c.prec=50; s=format(Decimal(a)/Decimal(b),'.12f')
 return dict(numerator=a,denominator=b,exact_fraction=f'{f.numerator}/{f.denominator}',decimal=s)
def bind(root, row):
 p=Path(row['path']); need(not p.is_absolute() and '..' not in p.parts,'safe export')
 q=root/p; need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'exact '+str(p))
def check(packet, public):
 need(sha(packet/'manifest.json')=='f70c8ac7eb978bea55db674216998641d13dcc58368dd3aaa716899d620732e1','frozen overview author')
 for row in read(packet/'manifest.json')['exports']: bind(packet,row)
 for name in ['manifest.json','results.json']:
  need((packet/'inputs'/('previous_'+name)).read_bytes()==(public/'audit/overview/v16/packet'/name).read_bytes(),'actual previous accepted overview')
 for name,pin in [
  ('inputs/numbers_manifest.json','0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'),
  ('inputs/numerical_review_manifest.json','2d071fbfffb2288d5b0d6f434b2c0d4b63fb95f187216b8d0bf5fc093397d04d'),
  ('inputs/numerical_root/manifest.json','000bced9618afa28c1e4e65424f464d29ea50682eb6f0e2e95509eab065d5599'),
  ('inputs/editorial_root/manifest.json','63fd7715402444d0ec49b102ac574dd789f6d6cebe852659a9cced0d3a738de7')]:
  need(sha(packet/name)==pin,'actual adopted boundary '+name)
 for row in read(packet/'inputs/numerical_root/manifest.json')['exports']: bind(packet/'inputs/numerical_root',row)
 for row in read(packet/'inputs/editorial_root/manifest.json')['exports']: bind(packet/'inputs/editorial_root',row)
 row=next(x for x in read(packet/'inputs/numbers_manifest.json')['exports'] if x['path']=='results.json')
 bind(packet/'inputs',dict(row,path='numbers_results.json'))
 old=read(packet/'inputs/previous_results.json'); r=read(packet/'results.json'); n=read(packet/'inputs/numbers_results.json')
 before={t['topic']:t for t in old['topics']}; after={t['topic']:t for t in r['topics']}
 need(set(before)==set(after) and len(after)==len(r['topics'])==19,'same nineteen topics')
 need(all(before[k]==after[k] for k in before if k!='A'),'all eighteen other topics unchanged')
 oldpairs={p['source']:p for t in old['topics'] for p in t['pairs']}
 newpairs={p['source']:p for t in r['topics'] for p in t['pairs']}
 need(len(oldpairs)==50 and len(newpairs)==51 and set(newpairs)==set(oldpairs)|{'L121'},'exact additional mathematical original')
 need(all(oldpairs[k]==newpairs[k] for k in oldpairs),'all fifty previous individual records unchanged')
 need(set(r['original_ids'])==set(newpairs) and len(r['original_ids'])==51,'unique original IDs')
 need((r['active_originals'],r['accessible_pending_originals'],r['mathematical_pending_originals'],r['accessible_unmeasured_originals'],r['editorial_original_count'],r['archived_unavailable_originals'])==(106,54,54,55,1,55),'complete counts')
 need(r['editorial_original_ids']==['L022'] and r['pooled_factor'] is None and not r['software_inclusive_comparisons_available'] and not r['cross_topic_deduplication'],'editorial and symmetric boundary')
 need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no duplicate credits')
 need(not r['manuscripts_remeasured'],'no re-extraction claim')
 scope=read(packet/'programme_scope.json'); prior=read(packet/'inputs/previous_programme_snapshot.json')
 need(sha(packet/'inputs/previous_programme_snapshot.json')=='f708a64e034faab55a471cba204673b81b33cef7862481babaac0460d69567ae','immutable programme50 partition')
 measured=set(scope['measured_original_ids']); pending=set(scope['mathematical_pending_original_ids']); editorial=set(scope['editorial_original_ids'])
 need(measured==set(prior['measured_original_ids'])|{'L121'} and pending==set(prior['accessible_pending_original_ids'])-{'L121','L022'} and editorial=={'L022'},'exact category transitions')
 need(measured==set(newpairs) and not(measured&pending or measured&editorial or pending&editorial) and measured|pending|editorial==set(prior['active_original_ids']),'disjoint exhaustive active partition')
 need(scope['active_original_ids']==prior['active_original_ids'] and scope['archived_original_ids']==prior['archived_original_ids'],'source corpus unchanged')
 need(scope['editorial_factor'] is None and scope['editorial_measured_credit']==0 and scope['actual_root_registration_binding'] is None,'proposed publication and no editorial factor')
 with (packet/'editorial.csv').open() as f: editorial_rows=list(csv.DictReader(f))
 need(len(editorial_rows)==1 and editorial_rows[0]['original']=='L022' and editorial_rows[0]['factor']=='','null editorial CSV')
 t=after['A']; cost=n['primary']['document_costs']
 need(t['source_ids']==n['source_ids'] and t['source_count']==9,'actual nine sources')
 need((t['representation'],t['normalization'],t['unit'])==('calibrated_selected_pdf','NFC','characters_without_whitespace'),'unchanged primary coordinate')
 need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'])==(273937,66140,136125,202265),'whole accepted source/common/application costs')
 need(t['common_components']=={'U':cost['U']} and t['application_components']=={a:{a:cost[a]} for a in n['applications'].values()},'complete manuscript components')
 need(t['entire_source_pages']==131 and t['entire_common_pages']==[23] and sum(t['entire_application_pages'].values())==56 and t['entire_application_pages']['L121']==11,'whole physical extents')
 need(t['whole_file_inventory']==n['whole_file_inventory'] and t['whole_file_group_costs']==n['whole_file_group_costs'] and t['unknown_costs']==n['unknown_costs'],'complete required inventory and unknowns')
 need(t['required_whole_file_count']==20 and t['complete_whole_file_count']==45 and t['required_original_bytes']==105850 and t['raw_required_program_data_cost']==92586,'complete software inventory')
 need(t['separate_software_inventory']==n['primary']['separate_software'] and t['complete_enlarged_printed_program_representation'] is None,'old printed appendices remain partial')
 need(t['added_Lean_declarations']==6 and not t['full_source_formalized'] and t['no_sibling_application_dependency'] and t['no_cross_topic_discount'],'formal and acquisition limits')
 need(t['scope_dispositions']==129 and t['originals_not_dispositions']==9 and t['conditional_records_preserved']==8,'source identities versus clauses')
 need(t['previous_overview_whole']==before['A']['written'],'historical whole rate preserved')
 for pair in t['pairs']:
  app=n['applications'][pair['source']]
  need(pair['application']==app and pair['source_cost']==cost[pair['source']] and pair['application_cost']==cost[app],'adopted source/application pairing')
 pairs=[]
 for t in r['topics']:
  need(t['source_count']==len(t['pairs']) and t['source_ids']==[p['source'] for p in t['pairs']],'one original per pair')
  need(sum(p['source_cost'] for p in t['pairs'])==t['source_sum'] and sum(p['application_cost'] for p in t['pairs'])==t['applications_sum'],'complete sums')
  need(t['written_denominator']==t['common_theory']+t['applications_sum'] and t['written']==fraction(t['source_sum'],t['written_denominator']),'whole rational arithmetic')
  need(t['embedded_validation_listings_screened'] and not t['held_sources'],'matched listing boundary')
  need(all(t.get(k) is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost']),'no asymmetric software factor')
  for p in t['pairs']:
   need(p['conditional']==fraction(p['source_cost'],p['application_cost']),'conditional rational arithmetic');pairs.append((t,p))
 need(len(pairs)==51,'all local factors')
 with (packet/'topics.csv').open() as f:rows=list(csv.DictReader(f))
 need(len(rows)==19,'all CSV topics')
 for row,t in zip(rows,r['topics']):
  need(row['topic']==t['topic'] and int(row['originals'])==t['source_count'],'topic CSV identity')
  for x,y in [('source_cost','source_sum'),('whole_common','common_theory'),('all_applications','applications_sum'),('written_denominator','written_denominator')]:need(int(row[x])==t[y],'topic CSV cost')
  need(row['written_exact']==t['written']['exact_fraction'] and row['written_factor']==t['written']['decimal'],'topic CSV quotient')
 with (packet/'applications.csv').open() as f:rows=list(csv.DictReader(f))
 need(len(rows)==51,'all CSV originals')
 for row,(t,p) in zip(rows,pairs):
  need((row['topic'],row['source'],row['application'])==(t['topic'],p['source'],p['application']),'local CSV identity')
  need(int(row['source_cost'])==p['source_cost'] and int(row['application_cost'])==p['application_cost'] and int(row['whole_common_prepaid'])==t['common_theory'],'local CSV costs')
  need(row['conditional_exact']==p['conditional']['exact_fraction'] and row['conditional_factor']==p['conditional']['decimal'],'local CSV quotient')
 spec=importlib.util.spec_from_file_location('accepted_rectangle_parser',public/'audit/overview/v10/packet/geometry_checks.py');parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
 whole=[(t['topic'],[('source',t['source_sum']),('common',t['common_theory']),('applications',t['applications_sum'])]) for t in r['topics']]
 local=[(p['source'],[('source',p['source_cost']),('application',p['application_cost'])]) for _,p in pairs]
 bars=0
 for name,rows,height,legend in [('whole_topics',whole,604.8,3),('conditional_1',local[:26],655.2,2),('conditional_2',local[26:],655.2,2)]:
  maximum=max(max(v[0][1],sum(n for _,n in v[1:])) for _,v in rows);sx=777.6*.77/(maximum*1.08);sy=height*.84/len(rows);expected={}
  for i,(identity,values) in enumerate(rows):
   start=0
   for k,(kind,value) in enumerate(values):
    expected[f'bar-{identity}-{kind}']=[777.6*.19+(start*sx if k else 0),height*.08+(i+(.535 if k else .235))*sy,value*sx,.23*sy]
    if k:start+=value
  parser.compare_geometry(parser.svg_rectangles((packet/(name+'.svg')).read_text()),expected);actual,h=parser.pdf_rectangles(packet/(name+'.pdf'));need(abs(h-height)<1e-6,'PDF canvas');parser.compare_pdf(actual,height,expected,legend);bars+=len(expected)
 need(bars==159,'all actual vector bars')
 pages=[' '.join((p.extract_text() or '').split()) for p in PdfReader(packet/'reader.pdf').pages];need(len(pages)==6,'complete reader')
 for t in r['topics']:
  cells=[t['topic'],str(t['source_count']),format(t['source_sum'],','),format(t['common_theory'],','),format(t['applications_sum'],','),f"{float(t['written']['decimal']):.3f}"];need(' '.join(cells) in pages[0],'rendered whole row')
 for i,(t,p) in enumerate(pairs):
  cells=[p['source'],t['topic'],format(p['source_cost'],','),format(p['application_cost'],','),f"{float(p['conditional']['decimal']):.3f}"];need(' '.join(cells) in pages[1 if i<26 else 2],'rendered conditional row')
 need('written expansion' in pages[0] and '1.354347' in pages[0] and '1.071157' in pages[0], 'rendered current factors and expansion')
 need('one edi-' in pages[0] or 'one editorial' in pages[0], 'editorial separation visible')
 need('23-page' in pages[1] and '56 pages' in pages[1] and '131 pages' in pages[1] and 'no sibling application' in pages[1], 'complete acquisition displayed')
 need('105,850' in pages[2] and '92,586' in pages[2] and 'Historical software' in pages[2] and 'six added Lean declarations' in pages[2], 'required programs and formal limits visible')
 return dict(status='PASS_ROOT_INDEPENDENT_OVERVIEW51', exact_fractions=70, unchanged_topics=18, unchanged_individual_records=50, unchanged_prior_fractions=68, SVG_bars=159, PDF_bars=159, reader_pages=6, recovered=51, mathematical_pending=54, editorial=1, active=106, archived=55, software_inclusive_factor=None, new_question_credit=0, source_measurement_or_science_rerun=False, current_author_code_imported=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--public',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh report');r=check(a.packet,a.public);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
