"""Independent additive numeric checks; no numerical-author helpers imported."""
from pathlib import Path
import csv,json,copy
from derive import derive,need,SOURCES,PAIRS,VARIANTS,NORMS,UNITS,PRIMARY
from geometry_review import inspect,expected
from geometry_parser import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def load(p):return json.loads(p.read_text())
def minus_display(f):return{k:v for k,v in f.items()if k!='display_six'}
def validate(r,o,prior):
 need(r['source_ids']==SOURCES and r['applications']==PAIRS,'exact nine pairings')
 need((r['source_count'],r['source_pages'],r['whole_common_pages'],sum(r['application_pages'].values()))==(9,131,23,56),'whole pages and one common paper')
 need(r['primary_coordinate']==PRIMARY and r['coordinate_count']==30 and r['exact_fraction_count']==300 and r['inherited_conditional_fractions_preserved']==240,'fixed coordinates/fractions')
 need(set(r['coordinates'])==set(o['coordinates']),'all30 coordinate identities')
 for key,want in o['coordinates'].items():
  got=r['coordinates'][key]
  for part in ['document_costs','source_sum','whole_common','application_sum','whole_written']:need(got[part]==want[part],'exact '+key+' '+part)
  need(got['written']==minus_display(want['written']),'whole exact fraction '+key)
  need(got['conditional']=={k:minus_display(v)for k,v in want['conditional'].items()},'all exact individual fractions '+key)
  old=prior['coordinates'][key];need(all(got['conditional'][k]==old['conditional'][k]for k in SOURCES[:-1]),'all240 earlier fraction objects preserved')
  need(got['prior_whole_written']==old['written'],'historical whole fraction unchanged')
  add=got['addition'];need(add['source']=='L121'and add['application']=='A9'and add['source_cost']==want['document_costs']['L121']and add['application_cost']==want['document_costs']['A9']and add['extra_common_cost']==0 and bool(add['reason']),'unchanged entire common charged once')
  sw=got['separate_software'];need(sw['complete_enlarged_printed_cost']is None and sw['software_inclusive_factor']is None and sw['historical_source_software_cost']is None,'unknown software boundary')
  need(sw['old_partial_printed_appendices']=={k:want['document_costs'][k]for k in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']}and sw['old_partial_printed_sum']==sum(sw['old_partial_printed_appendices'].values()),'only old subset printed')
  n=key.split('/')[1];m=key.split('/')[2];need(sw['raw_group_costs']=={g:v['metrics'][n][m]for g,v in o['groups'].items()},'separate complete whole-file totals')
 need(r['primary']==r['coordinates'][PRIMARY],'primary object identity')
 need(r['whole_file_group_costs']==o['groups'],'entire raw role totals')
 need(len(r['whole_file_inventory'])==45 and len({x['file']['sha256']for x in r['whole_file_inventory']})==45,'actual whole contents no duplicate discount')
 for actual,want in zip(r['whole_file_inventory'],o['raw_files']):
  need(all(actual[k]==want[k]for k in ['id','file','role','metrics'])and actual['cost_group']==want['group']and actual['whole_file'],'actual inventory row')
  need(actual['mathematical_premise']==(want['group']=='required_program_or_data'),'exact required role')
 need(len(r['primary_acquisition'])==10,'ten cumulative stages')
 for got,want in zip(r['primary_acquisition'],o['stages']):need(all(got[k]==v for k,v in want.items())and got['required_program_data_and_external_premises_separate'],'cumulative full acquisition')
 need(r['complete_enlarged_printed_program_representation']is None and r['software_inclusive_factors']is None and r['optional_validation_inclusive_factors']is None and r['historical_source_software_cost']is None and r['full_formalization_cost']is None and all(x is None for x in r['unknown_costs'].values()),'all unknown costs null')
 need(not r['cross_topic_discount']and r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0 and r['no_extraction']and r['no_scientific_or_formal_replay'],'no scope/credit inflation')
 return True

def csvcheck(packet,o):
 expected={}
 rows=[]
 for k,c in o['coordinates'].items():
  for name,f in [('written',c['written'])]+list(c['conditional'].items()):rows.append({'coordinate':k,'comparison':name,**{x:str(v)for x,v in minus_display(f).items()}})
 expected['fractions.csv']=rows
 expected['document_costs.csv']=[dict(coordinate=k,document=d,cost=str(v))for k,c in o['coordinates'].items()for d,v in c['document_costs'].items()]
 expected['whole_files.csv']=[dict(id=r['id'],path=r['file']['path'],role=r['role'],bytes=str(r['file']['bytes']),sha256=r['file']['sha256'],normalization=n,unit=u,cost=str(r['metrics'][n][u]))for r in o['raw_files']for n in NORMS for u in UNITS]
 expected['acquisition.csv']=[dict(stage=str(x['stage']),acquired='whole U'if not x['stage']else PAIRS[SOURCES[x['stage']-1]]+' for '+SOURCES[x['stage']-1],source_written=str(x['source_written']),replacement_written=str(x['replacement_written']),required_program_data_and_external_premises_separate='True')for x in o['stages']]
 for name,rows in expected.items():need(list(csv.DictReader((packet/name).open()))==rows,'all complete CSV rows '+name)
 return {k:len(v)for k,v in expected.items()}

def readercheck(packet,o):
 t=(packet/'reader.tex').read_text();p=o['primary'];d=p['document_costs']
 need(r'\frac{'+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+'}'in t,'actual headline exact costs')
 need(p['written']['display_six']in t,'headline exact six-place rounding')
 for src,app in PAIRS.items():
  want=f"{src} & {app} & {d[src]:,} & {d[app]:,} & {p['conditional'][src]['display_six']}";need(want in t,'complete conditional display '+src)
 labels=dict(zip(UNITS,['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed UTF-8 bytes']))
 for n in NORMS:
  for u in UNITS:
   want=f'{n}: {labels[u]} & '+' & '.join(o['coordinates']['/'.join([v,n,u])]['written']['display_six']for v in VARIANTS);need(want in t,'exact sensitivity display')
 need('after acquiring the \\emph{entire} common theory'in t and 'L121 uses no sibling application'in t,'conditional acquisition wording')
 need('Required programs and data remain premises'in t and 'no software-inclusive or optional-validation-inclusive factor'in t,'source/software symmetry')
 need('No complete printed representation exists'in t and 'not added to raw files'in t,'partial printed appendix restriction')
 need('unknown, not zero'in t and 'do not formalize group orders, infinite families or geometry'in t,'unknowns and partial formal scope')
 return {'headline_and_conditional_rows':10,'whole_sensitivity_rows':10}

def controls(r,o,prior,packet):
 done=[]
 def bad(name,fn):
  q=copy.deepcopy(r);fn(q)
  try:validate(q,o,prior)
  except(ValueError,KeyError):done.append(name)
  else:raise ValueError('control survives '+name)
 tests=[('remove common',lambda q:q['coordinates'][PRIMARY].update(whole_common=0)),('omit A9',lambda q:q['coordinates'][PRIMARY].update(application_sum=110576)),('alter source',lambda q:q['coordinates'][PRIMARY]['document_costs'].update(L121=1)),('misroute new application',lambda q:q['applications'].update(L121='A8')),('alter reduced fraction',lambda q:q['coordinates'][PRIMARY]['written'].update(numerator=1)),('alter old conditional',lambda q:q['coordinates'][PRIMARY]['conditional']['N009'].update(decimal='0')),('drop sensitivity',lambda q:q['coordinates'].pop(next(iter(q['coordinates'])))),('software becomes zero',lambda q:q.update(software_inclusive_factors=0)),('required program relabeled optional',lambda q:q['whole_file_inventory'][0].update(mathematical_premise=False)),('mandatory data omitted',lambda q:q['whole_file_inventory'].pop(37)),('partial appendix declared complete',lambda q:q.update(complete_enlarged_printed_program_representation=30)),('lost cumulative common',lambda q:q['primary_acquisition'][0].update(replacement_written=0)),('new credit',lambda q:q.update(new_source_credit=1)),('unpriced graphic cost zero',lambda q:q['unknown_costs'].update(full_graphical_structure=0)),('duplicate-content discount',lambda q:q['whole_file_group_costs']['required_program_or_data'].update(literal_bytes=0)),('change primary metric',lambda q:q.update(primary_coordinate='raw_untrimmed/NFC/characters_without_whitespace'))]
 for name,f in tests:bad(name,f)
 for stem in ['costs','cumulative']:
  want=expected(o,stem);actual=svg_rectangles((packet/(stem+'.svg')).read_text())
  for name,f in [('width distortion',lambda x:x[next(iter(x))].__setitem__(2,1)),('zero-baseline shift',lambda x:x[next(iter(x))].__setitem__(0,0)),('missing bar',lambda x:x.pop(next(iter(x))))]:
   q=copy.deepcopy(actual);f(q)
   try:compare_geometry(q,want)
   except RuntimeError:done.append(stem+' '+name)
   else:raise ValueError('graph control survived')
  q,h=pdf_rectangles(packet/(stem+'.pdf'));q[0][3]+=1
  try:compare_pdf(q,h,want,0)
  except RuntimeError:done.append(stem+' PDF height distortion')
  else:raise ValueError('PDF control survived')
 return done

def run(packet):
 o=derive(packet/'inputs/input/author_counts.json',packet/'inputs/input/precount/raw_inventory.json');r=load(packet/'results.json');prior=load(packet/'prior/results.json');validate(r,o,prior);cs=csvcheck(packet,o);rd=readercheck(packet,o);g=inspect(packet,o);tests=controls(r,o,prior,packet)
 return {'status':'PASS_DISTINCT_ARITHMETIC_AND_VECTOR_CHECKS','coordinates':30,'exact_fractions':300,'unchanged_conditional_fractions':240,'adopted_PDF_cells':660,'adopted_raw_cells':450,'CSV_rows':cs,'whole_files':45,'primary_whole':o['primary']['written'],'primary_L121':o['primary']['conditional']['L121'],'reader_checks':rd,'graphs':g,'controls':tests,'new_source_credit':0,'software_inclusive_factors':None},o
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--out',type=Path,required=True);q=a.parse_args();need(not q.out.exists(),'fresh output');r,o=run(q.packet);q.out.write_text(json.dumps(r,indent=2)+'\n');print({k:r[k]for k in ['status','exact_fractions','CSV_rows']})
