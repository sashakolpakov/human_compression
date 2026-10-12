#!/usr/bin/env python3
"""Independent root arithmetic and rendering audit of the additive LCD overview.

Only the older accepted rectangle parser is reused; no current author code is
imported. Primary counts come from the separately adopted numerical packet.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,csv,hashlib,importlib.util,json
from pypdf import PdfReader

def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext() as c:c.prec=50;s=format(Decimal(a)/Decimal(b),'.12f')
 return dict(numerator=a,denominator=b,exact_fraction=f'{f.numerator}/{f.denominator}',decimal=s)
def check(packet,public):
 m=read(packet/'manifest.json')
 for row in m['exports']:
  p=packet/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen '+row['path'])
 for name in ['manifest.json','results.json']:
  need((packet/'inputs'/('previous_'+name)).read_bytes()==(public/'audit/overview/v15/packet'/name).read_bytes(),'exact accepted previous overview')
 for prefix,pin,export in [('numbers','0e1366b9e5d21d7e8158f3330d00db892840e1f9b2bf6d94c5bc05069b8d4cf9','results.json'),('root','9afdffa0e9ed57ece5a32b3a27eee2302ebd3e23056a338001046d5a0204b027','adoption.json')]:
  mp=packet/'inputs'/(prefix+'_manifest.json');need(sha(mp)==pin,'exact adopted manifest')
  row=next(e for e in read(mp)['exports'] if e['path']==export);f=packet/'inputs'/(prefix+'_'+export);need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'actual accepted contents')
 need(sha(packet/'inputs/numerical_review_manifest.json')=='92d6586139518e13401c1dd60deb44341546b7289a7aae1a95e385dad938b0d2','distinct numerical review')
 old=read(packet/'inputs/previous_results.json');r=read(packet/'results.json');n=read(packet/'inputs/numbers_results.json');cost=n['primary']['costs']
 need(r['topics'][:18]==old['topics'] and len(r['topics'])==19,'all 18 prior topic objects unchanged')
 need(len(r['original_ids'])==len(set(r['original_ids']))==50 and set(r['original_ids'])==set(old['original_ids'])|{'L050','F017'},'two distinct additional originals')
 need(r['active_originals']==106 and r['accessible_pending_originals']==56 and r['archived_unavailable_originals']==55,'programme partition')
 need(r['pooled_factor'] is None and not r['software_inclusive_comparisons_available'] and not r['cross_topic_deduplication'],'cost boundary')
 need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no extra proof credit')
 t=r['topics'][-1];need(t['topic']=='LCD' and t['source_ids']==['L050','F017'],'new LCD pair')
 need((t['representation'],t['normalization'],t['unit'])==('calibrated_selected_pdf','NFC','characters_without_whitespace'),'fixed coordinate')
 need(tuple(t[k] for k in ['source_sum','common_theory','applications_sum','written_denominator'])==(58756,32300,66886,99186),'complete adopted costs')
 need(t['common_components']=={'U_LCD':cost['U_LCD']} and t['application_components']=={'L050':{'A_L050':cost['A_L050']},'F017':{'A_F017':cost['A_F017']}},'no partial or free manuscript')
 need(t['entire_source_pages']=={'L050':11,'F017':17} and t['entire_common_pages']==[14] and t['entire_application_pages']=={'L050':15,'F017':12},'complete paper extents')
 need(t['whole_file_inventory']==n['raw_file_inventory']['files'] and t['whole_file_group_costs']==n['primary']['raw_costs'] and t['unknown_costs']==n['unknown_costs'],'required whole inventories and unknowns')
 need(t['required_whole_file_count']==83 and t['required_original_bytes']==422956 and t['whole_file_original_bytes']==548250 and len(t['whole_file_inventory'])==102,'complete acquisition')
 need(t['scientific_boundary']==n['retained_scope'] and t['source_dispositions']=={'L050':54,'F017':104},'corrected scope')
 need(t['scoped_Lean_declarations']==9 and not t['full_source_formalized'] and t['no_sibling_application_dependency'] and t['no_cross_topic_discount'],'formal and acquisition scope')
 need('Expansion' in t['whole_topic_interpretation'],'expansion disclosed')
 for p in t['pairs']:
  doc='A_'+p['source'];need(p['application']==p['original_application_id']==doc and p['source_cost']==cost[p['source']] and p['application_cost']==cost[doc],'actual local costs')
 pairs=[]
 for t in r['topics']:
  need(t['source_count']==len(t['pairs']) and t['source_ids']==[p['source'] for p in t['pairs']],'one original per pair')
  need(sum(p['source_cost'] for p in t['pairs'])==t['source_sum'] and sum(p['application_cost'] for p in t['pairs'])==t['applications_sum'],'complete sums')
  need(t['written_denominator']==t['common_theory']+t['applications_sum'] and t['written']==fraction(t['source_sum'],t['written_denominator']),'whole rational arithmetic')
  need(t['embedded_validation_listings_screened'] and not t['held_sources'],'matched listing boundary')
  need(all(t.get(k) is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost']),'no asymmetric software factor')
  for p in t['pairs']:
   need(p['conditional']==fraction(p['source_cost'],p['application_cost']),'conditional rational arithmetic');pairs.append((t,p))
 need(len(pairs)==50,'all local factors')
 with (packet/'topics.csv').open() as f:rows=list(csv.DictReader(f))
 need(len(rows)==19,'all CSV topics')
 for row,t in zip(rows,r['topics']):
  need(row['topic']==t['topic'] and int(row['originals'])==t['source_count'],'topic CSV identity')
  for x,y in [('source_cost','source_sum'),('whole_common','common_theory'),('all_applications','applications_sum'),('written_denominator','written_denominator')]:need(int(row[x])==t[y],'topic CSV cost')
  need(row['written_exact']==t['written']['exact_fraction'] and row['written_factor']==t['written']['decimal'],'topic CSV quotient')
 with (packet/'applications.csv').open() as f:rows=list(csv.DictReader(f))
 need(len(rows)==50,'all CSV originals')
 for row,(t,p) in zip(rows,pairs):
  need((row['topic'],row['source'],row['application'])==(t['topic'],p['source'],p['application']),'local CSV identity')
  need(int(row['source_cost'])==p['source_cost'] and int(row['application_cost'])==p['application_cost'] and int(row['whole_common_prepaid'])==t['common_theory'],'local CSV costs')
  need(row['conditional_exact']==p['conditional']['exact_fraction'] and row['conditional_factor']==p['conditional']['decimal'],'local CSV quotient')
 spec=importlib.util.spec_from_file_location('accepted_rectangle_parser',public/'audit/overview/v10/packet/geometry_checks.py');parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
 whole=[(t['topic'],[('source',t['source_sum']),('common',t['common_theory']),('applications',t['applications_sum'])]) for t in r['topics']]
 local=[(p['source'],[('source',p['source_cost']),('application',p['application_cost'])]) for _,p in pairs]
 bars=0
 for name,rows,height,legend in [('whole_topics',whole,604.8,3),('conditional_1',local[:25],655.2,2),('conditional_2',local[25:],655.2,2)]:
  maximum=max(max(v[0][1],sum(n for _,n in v[1:])) for _,v in rows);sx=777.6*.77/(maximum*1.08);sy=height*.84/len(rows);expected={}
  for i,(identity,values) in enumerate(rows):
   start=0
   for k,(kind,value) in enumerate(values):
    expected[f'bar-{identity}-{kind}']=[777.6*.19+(start*sx if k else 0),height*.08+(i+(.535 if k else .235))*sy,value*sx,.23*sy]
    if k:start+=value
  parser.compare_geometry(parser.svg_rectangles((packet/(name+'.svg')).read_text()),expected);actual,h=parser.pdf_rectangles(packet/(name+'.pdf'));need(abs(h-height)<1e-6,'PDF canvas');parser.compare_pdf(actual,height,expected,legend);bars+=len(expected)
 need(bars==157,'all actual vector bars')
 pages=[' '.join((p.extract_text() or '').split()) for p in PdfReader(packet/'reader.pdf').pages];need(len(pages)==6,'complete reader')
 for t in r['topics']:
  cells=[t['topic'],str(t['source_count']),format(t['source_sum'],','),format(t['common_theory'],','),format(t['applications_sum'],','),f"{float(t['written']['decimal']):.3f}"];need(' '.join(cells) in pages[0],'rendered whole row')
 for i,(t,p) in enumerate(pairs):
  cells=[p['source'],t['topic'],format(p['source_cost'],','),format(p['application_cost'],','),f"{float(p['conditional']['decimal']):.3f}"];need(' '.join(cells) in pages[1 if i<25 else 2],'rendered conditional row')
 need('written expansion' in pages[0] and '14-page' in pages[1] and '0.659169' in pages[1] and '1.157126' in pages[1] and 'not newly solved' in pages[2] and '422,956' in pages[2] and 'nine inherited generic declarations' in pages[2] and 'Historical software' in pages[2],'rendered scope')
 return dict(status='PASS_ROOT_INDEPENDENT_OVERVIEW50',exact_fractions=69,unchanged_topics=18,unchanged_individual_records=48,unchanged_prior_fractions=66,SVG_bars=157,PDF_bars=157,reader_pages=6,recovered=50,pending=56,software_inclusive_factor=None,new_question_credit=0,source_measurement_or_science_rerun=False,current_author_code_imported=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--public',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh report');r=check(a.packet,a.public);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
