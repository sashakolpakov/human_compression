#!/usr/bin/env python3
"""Independent A10 numerical review; reads accepted cells, never imports author arithmetic."""
import argparse,copy,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
from derive import *
from geometry_review import inspect,expected
from geometry_parser import compare_geometry,compare_pdf,svg_rectangles,pdf_rectangles
HERE=Path(__file__).resolve().parent
AUTHOR='524b5f73c007e5ba783920859874fe3cb8b5ce7a73d28929b82bf94678e9e31f'
INPUT='2c879d415d4408f42f61e79663cf7e414111d50ccf666c2f6fa903cc6118d3ae'
INPUT_REVIEW='6993040ac0d1e787f18ae7be3c6bbe3ea2bde93a508baad6bd0d8ba7589604a8'
PRIOR='0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'
PRIOR_ADOPTION='000bced9618afa28c1e4e65424f464d29ea50682eb6f0e2e95509eab065d5599'
PROTOCOL='d3d26cbbd599e7d66134cb62bc9ad50ce17f6e4bd4400298d001f965fac76632'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p,r):need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'exact artifact '+str(p))
def manifest(p,pin=None):
 if pin:need(sha(p)==pin,'immutable manifest '+str(p))
 m=read(p);paths=[]
 for r in m['exports']:bind(p.parent/r['path'],r);paths.append(r['path'])
 need(len(paths)==len(set(paths)),'unique export paths');return len(paths)
def protocol(p,o):
 need(p['source_order']==SOURCES and p['applications']==PAIRS and p['application_documents']==BUNDLES and p['common_documents']==COMMON,'fixed full native manuscript closure')
 need(p['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace'),'fixed primary')
 need(p['variants']==VARIANTS and p['normalizations']==NORMS and p['units']==UNITS,'fixed30 sensitivity coordinates')
 need(p['source_pages']==152 and p['whole_common_pages']==41 and p['application_pages']==63 and p['old_partial_program_pages']==30,'complete pages')
 need(p['raw_classes']==CLASS_COUNTS and p['required_contents']==o['required'],'explicit99 whole program/data premises')
 need(p['unchanged_conditionals']==SOURCES[:8],'only8 inherited application fractions')
 need('all99 required' in p['conditional_formula']and 'all three common' in p['conditional_formula'],'full acquisition prerequisite')
 need(p['roles']['numerical_author']=='root'and 'enumeration_volume authored the inputs' in p['roles']['disclosure'],'authorship distinction')
 for k in ['complete_enlarged_printed_program_representation','software_inclusive_factors','historical_source_software_cost']:need(p[k]is None,'unknown software boundary '+k)
 need(p['unknown_costs']==o['unknown_costs']and p['cross_topic_discount']is False,'external costs and no discounts')
def reader(tex,o):
 p=o['primary'];count=0
 need('=\\frac{319016}{108271+155199}'in tex and '=1.210825.'in tex,'whole reader equation')
 for s in SOURCES:
  a=PAIRS[s];r=p['conditional'][s];line=f"{s} & {a} & {r['source_cost']:,} & {r['replacement_cost']:,} & {r['display_six']}"
  need(line in tex,'reader individual row '+s);count+=1
 names=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed UTF-8 bytes']
 for n in NORMS:
  for u,label in zip(UNITS,names):
   row=n+': '+label+' & '+' & '.join(o['coordinates']['/'.join([v,n,u])]['written']['display_six']for v in VARIANTS)
   need(row in tex,'reader sensitivity row '+n+'/'+u);count+=3
 labels={'required_program':'Required programs','required_data':'Required data','operational':'Operational files','optional_validation':'Optional validation','partial_formal':'Partial formal files','output_receipt':'Output receipts'}
 for k,g in o['groups'].items():need(f"{labels[k]} & {g['files']} & {g['metrics']['NFC']['characters_without_whitespace']:,} & {g['literal_bytes']:,}"in tex,'reader complete inventory '+k)
 for phrase in ['all 99 required program and data contents','Each is paid in full','no sibling application is a free premise','decreases from 1.354347','The net replacement increase is 61,205','no software-inclusive ratio is reported','only the old eleven-file subset','423 occurrences of drawing-font aliases','unknown cost','No mathematical enumeration or Lean compilation is repeated']:
  need(phrase in tex,'reader scope '+phrase)
 return count+1

def controls(r,p,o,packet):
 names=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,RuntimeError,KeyError,IndexError):names.append(name);return
  raise ValueError('mutation accepted: '+name)
 def result(name,edit):
  z=copy.deepcopy(r);edit(z);reject(name,lambda:verify_result(z,o))
 K=PRIMARY
 result('omit14page common supplement',lambda z:z['coordinates'][K]['common_costs'].pop('U_HEX'))
 result('omit4page common proof',lambda z:z['coordinates'][K].__setitem__('whole_common',100126))
 result('omit L003 companion',lambda z:z['application_documents']['A10'].pop())
 result('restore historical L121 cost',lambda z:z['coordinates'][K]['application_costs'].__setitem__('A9',25549))
 result('alter complete source sum',lambda z:z['coordinates'][K].__setitem__('source_sum',273937))
 result('omit a sensitivity coordinate',lambda z:z['coordinates'].pop(next(iter(z['coordinates']))))
 result('incorrect reduced numerator',lambda z:z['coordinates'][K]['written'].__setitem__('numerator',159509))
 result('truncate decimal display',lambda z:z['coordinates'][K]['written'].__setitem__('decimal','1.210824761831'))
 result('change old conditional',lambda z:z['coordinates'][K]['conditional']['L032'].__setitem__('replacement_cost',8229))
 result('swap source pairing',lambda z:z['applications'].__setitem__('L003','A9'))
 result('classify required data as output',lambda z:next(x for x in z['whole_file_inventory']if x['accounting_class']=='required_data').__setitem__('accounting_class','output_receipt'))
 result('drop a complete raw content',lambda z:z['whole_file_inventory'].pop())
 result('sum overlapping raw roles',lambda z:z['whole_file_group_costs']['required_data'].__setitem__('files',72))
 result('erase mandatory whole-file premise',lambda z:next(x for x in z['whole_file_inventory']if x['mathematical_premise']).__setitem__('mathematical_premise',False))
 result('free common acquisition',lambda z:z['primary_acquisition'][0].__setitem__('replacement_written',0))
 result('drop final acquisition',lambda z:z['primary_acquisition'].pop())
 result('invent software-inclusive scalar',lambda z:z.__setitem__('software_inclusive_factors',1.2))
 result('unknown graphics changed to zero',lambda z:z['unknown_costs'].__setitem__('full_L003_graphics',0))
 result('treat partial appendix as enlarged total',lambda z:z.__setitem__('complete_enlarged_printed_program_representation',30))
 result('apply cross-topic overlap discount',lambda z:z.__setitem__('cross_topic_discount',True))
 result('claim new source credit from arithmetic',lambda z:z.__setitem__('new_source_credit',1))
 result('claim full formal credit',lambda z:z.__setitem__('new_formal_credit',1))
 q=copy.deepcopy(p);q['required_contents'].pop();reject('protocol omits required content',lambda:protocol(q,o))
 q=copy.deepcopy(p);q['primary']['variant']='raw_untrimmed';reject('posthoc primary change',lambda:protocol(q,o))
 q=copy.deepcopy(p);q['unchanged_conditionals'].append('L121');reject('false nine-app invariance',lambda:protocol(q,o))
 tex=(packet/'reader.tex').read_text();reject('misrounded reader factor',lambda:reader(tex.replace('12.288729','12.288728'),o))
 reject('reader suggests source-only software',lambda:reader(tex.replace('no software-inclusive ratio is reported','software-inclusive ratio is 1.2'),o))
 for stem in ['costs','cumulative']:
  e=expected(o,stem);actual=svg_rectangles((packet/(stem+'.svg')).read_text());key=next(iter(actual))
  z=copy.deepcopy(actual);z[key][2]+=1;reject(stem+' actual SVG width',lambda:compare_geometry(z,e))
  z=copy.deepcopy(actual);z[key][0]+=1;reject(stem+' actual SVG baseline',lambda:compare_geometry(z,e))
  z=copy.deepcopy(actual);z.pop(key);reject(stem+' missing SVG bar',lambda:compare_geometry(z,e))
  rect,H=pdf_rectangles(packet/(stem+'.pdf'));rect[0][2]+=1;reject(stem+' actual PDF rectangle',lambda:compare_pdf(rect,H,e,0))
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();packet=a.packet.resolve();a.out.mkdir(parents=True,exist_ok=True)
 counts={'author':manifest(packet/'manifest.json',AUTHOR),'accepted_input':manifest(packet/'inputs/input/manifest.json',INPUT),'input_root_review':manifest(packet/'inputs/root_review/manifest.json',INPUT_REVIEW),'prior_numerical_adoption':manifest(packet/'prior/numerical_root_adoption/manifest.json',PRIOR_ADOPTION)}
 need(sha(packet/'prior/manifest.json')==PRIOR,'prior numerical author pin');oldmanifest=read(packet/'prior/manifest.json')
 for name in ['results.json','protocol.json']:bind(packet/'prior'/name,next(x for x in oldmanifest['exports']if x['path']==name))
 extra=read(packet/'prior_acceptance_binding.json');bind(packet/extra['path'],extra);need(extra['sha256']==PRIOR_ADOPTION,'exact additive prior numerical adoption')
 need(read(packet/'prior/numerical_root_adoption/adoption.json')['bindings']['author']['sha256']==PRIOR,'adopted previous numerical author')
 need(sha(packet/'protocol.json')==PROTOCOL,'pre-arithmetic protocol pin');p=read(packet/'protocol.json');o=derive(packet);protocol(p,o);r=read(packet/'results.json');fractions,old=verify_result(r,o);csvs=verify_csvs(packet,o);geometry=inspect(packet,o)
 plot=read(packet/'plot_data.json');need(plot['primary_coordinate']==PRIMARY,'plot primary')
 for stem in geometry:compare_geometry(plot[stem]['expected_rectangles'],expected(o,stem))
 displays=reader((packet/'reader.tex').read_text(),o);pages=PdfReader(packet/'reader.pdf').pages;need(len(pages)==4,'four complete reader pages');texts=[x.extract_text()or''for x in pages]
 for e in [o['primary']['written'],*o['primary']['conditional'].values()]:need(e['display_six']in ''.join(texts),'actual reader primary value')
 for e in o['coordinates'].values():need(e['written']['display_six']in texts[3],'actual reader sensitivity value')
 owncontrols=controls(r,p,o,packet)
 report=dict(status='PASS_DISTINCT_A10_NUMERICAL_REVIEW',author_manifest=AUTHOR,accepted_input_manifest=INPUT,input_root_acceptance=INPUT_REVIEW,prior_numeric_adoption=PRIOR_ADOPTION,verified_exports=counts,coordinates=30,fractions=fractions,old_conditional_records=old,input_PDF_cells=870,raw_content_cells=2030,whole_raw_contents=203,required_whole_contents=len(o['required']),CSV_rows=csvs,primary={k:o['primary'][k]for k in ['source_sum','whole_common','application_sum','whole_written','written']},conditional_primary=o['primary']['conditional'],graph_bars={k:{x:v[x]for x in ['SVG_bars','PDF_bars']}for k,v in geometry.items()},reader_pages=4,reader_fraction_displays_checked=displays,reader_page_text_sha256=[hashlib.sha256(x.encode()).hexdigest()for x in texts],controls=owncontrols,software_inclusive_factor=None,input_or_science_re_adjudicated=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'expected_geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
 (a.out/'independent_fractions.json').write_text(json.dumps({k:dict(written=v['written'],conditional=v['conditional'])for k,v in o['coordinates'].items()},indent=2)+'\n')
 if(HERE/'manifest.json').exists():manifest(HERE/'manifest.json')
 print(json.dumps({k:report[k]for k in ['status','fractions','old_conditional_records','CSV_rows','graph_bars','reader_pages']}));print('independent controls:',len(owncontrols))
if __name__=='__main__':main()
