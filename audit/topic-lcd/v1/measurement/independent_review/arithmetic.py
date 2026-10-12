#!/usr/bin/env python3
"""Independent arithmetic from frozen accepted cells, with no author imports."""
import csv,json,hashlib,itertools
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction
from pathlib import Path
VAR=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
DOCS=['L050','F017','U_LCD','A_L050','A_F017'];ROLES=['required_program','required_derived_certificate','required_data','required_finite_record','optional_validation','operational_driver','partial_formal_file','partial_formal_scope'];PAGES=[11,17,14,15,12]
def need(v,msg):
 if not v:raise ValueError(msg)
def read(p):return json.loads(p.read_text())
def dec(n,d,places=12):
 with localcontext() as ctx:ctx.prec=70;return format(Decimal(n)/Decimal(d),f'.{places}f')
def exact(n,d):
 f=Fraction(n,d);return {'numerator':n,'denominator':d,'reduced_numerator':f.numerator,'reduced_denominator':f.denominator,'decimal':dec(n,d)}
def classify(n,d):return 'expansion' if n<d else 'equal length' if n==d else 'local saving'
def csvrows(path):
 with path.open(newline='') as f:return list(csv.DictReader(f))
def validate(p,result=None,check_csv=True):
 a=read(p/'inputs/author_counts.json');raw=read(p/'inputs/raw_counts.json');r=read(p/'results.json') if result is None else result
 need(list(a['documents'])==['L050','F017','U_LCD','A_F017','A_L050'] or set(a['documents'])==set(DOCS),'five source/ours documents')
 need({k:a['documents'][k]['pages'] for k in DOCS}==dict(zip(DOCS,PAGES)) and a['physical_pages']==69,'complete page boundary')
 need(r['raw_file_inventory']==raw,'exact retained raw vectors/occurrences')
 need(len(raw['files'])==102 and len({x['sha256'] for x in raw['files']})==102 and len(raw['occurrence_bindings'])==127,'full unique/occurrence boundary')
 counts=Counter(x['role'] for x in raw['files']);need(counts==dict(zip(ROLES,[20,2,19,42,3,11,2,3])),'role counts')
 rb={k:sum(x['bytes'] for x in raw['files'] if x['role']==k) for k in ROLES};need(sum(rb.values())==548250,'all original bytes')
 roles=[]
 for k in ROLES:roles.append({'role':k,'whole_files':counts[k],'whole_bytes':rb[k],'mathematical_premise':k in ROLES[:4]})
 need(r['raw_role_inventory']==roles,'full raw role aggregation')
 req=[x for x in raw['files'] if x['role'] in ROLES[:4]]
 need(all(x['mathematical_premise']==(x['role'] in ROLES[:4]) and x['whole_file'] for x in raw['files']),'required versus optional roles')
 need(len(req)==83 and sum(x['bytes'] for x in req)==422956,'complete conservative conditional preacquisition')
 acq=r['acquisition'];need(acq['initial_common']==['U_LCD'] and acq['local_applications']=={'L050':['A_L050'],'F017':['A_F017']},'full U and both local applications')
 need(acq['required_whole_content_sha256']==[x['sha256'] for x in req] and acq['required_whole_files']==83 and acq['required_whole_bytes']==422956 and acq['optional_validation_is_not_prepaid'] and acq['retained_classical_cost'] is None,'whole required boundary and unknown costs')
 need(all(v is None for v in r['unknown_costs'].values()) and r['pooled_factor'] is None,'unknowns not zero; no pooled scalar')
 scope=r['scope'];need(scope['software_inclusive_factor'] is None and scope['source_software_cost'] is None and scope['graph_layout_cost'] is None,'no asymmetric software/graphics scalar')
 for k in ['whole_common_once','both_complete_applications','no_sibling_application_dependency','programs_excluded_symmetrically','complete_required_program_data_records_acquired','retained_classical_premises_acquired','whole_required_files_never_discounted']:need(scope[k] is True,'paid scope '+k)
 need(not scope['optional_validation_required_for_conditional'] and not scope['full_source_formalized'] and scope['unique_partial_Lean_declarations']==9 and not scope['printed_CODE_document_present'],'optional/formal boundary')
 need(scope['L050_dispositions']==54 and scope['F017_dispositions']==104 and all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'science/credit unchanged')
 expected_rows={};fractions=[];costrows=[];acquisition=[]
 for v,f,u in itertools.product(VAR,FORMS,UNITS):
  costs={k:a['documents'][k]['variants'][v][f][u] for k in DOCS};rolesums={k:sum(x['metrics'][f][u] for x in raw['files'] if x['role']==k) for k in ROLES}
  src=costs['L050']+costs['F017'];app=costs['A_L050']+costs['A_F017'];common=costs['U_LCD'];total=common+app
  pairs={'written':(src,total),'conditional_L050':(costs['L050'],costs['A_L050']),'conditional_F017':(costs['F017'],costs['A_F017'])}
  row={'variant':v,'normalization':f,'unit':u,'costs':costs,'raw_costs':rolesums,'totals':{'source':src,'common':common,'applications':app,'written':total},'comparisons':{k:exact(*x) for k,x in pairs.items()},'interpretation':{k:classify(*x) for k,x in pairs.items()},'acquisition':{'common_then_L050_then_F017':[common,common+costs['A_L050'],total],'required_raw_premises':sum(rolesums[k] for k in ROLES[:4]),'optional_raw_validation':rolesums['optional_validation'],'software_added_to_manuscript_denominator':False},'software_inclusive_factor':None}
  expected_rows[v,f,u]=row
  for k,(n,d) in pairs.items():fractions.append(dict(variant=v,normalization=f,unit=u,comparison=k,**{a:str(b) for a,b in exact(n,d).items()},interpretation=classify(n,d)))
  for kind,data in [('PDF',costs),('raw-role',rolesums)]:
   costrows += [dict(variant=v,normalization=f,unit=u,representation=kind,key=k,cost=str(value)) for k,value in data.items()]
  acquisition += [dict(variant=v,normalization=f,unit=u,stage=s,complete_manuscript_cost=str(x)) for s,x in zip(['whole_common','common_and_L050','common_and_both_apps'],row['acquisition']['common_then_L050_then_F017'])]
 need(len(r['coordinates'])==30 and len({(x['variant'],x['normalization'],x['unit']) for x in r['coordinates']})==30,'complete sensitivity coordinates')
 for x in r['coordinates']:need(x==expected_rows[x['variant'],x['normalization'],x['unit']],'exact whole/local fraction and component arithmetic')
 primary=expected_rows['calibrated_selected','NFC','characters_without_whitespace'];need(r['primary']==primary and r['primary_coordinate']==['calibrated_selected','NFC','characters_without_whitespace'],'fixed primary')
 need(acq['complete_written_stages']==primary['acquisition']['common_then_L050_then_F017'],'whole common cumulative charge')
 need(r['coordinate_count']==30 and r['exact_fraction_count']==90 and r['whole_written_fractions']==30 and r['conditional_fractions']==60,'one whole plus two conditional at every coordinate')
 if check_csv:
  need(csvrows(p/'fractions.csv')==fractions,'all 90 fraction CSV rows')
  need(csvrows(p/'costs.csv')==costrows,'all 390 manuscript/role CSV rows')
  need(csvrows(p/'acquisition.csv')==acquisition,'all 90 cumulative cost rows')
  need(read(p/'acquisition.json')==acq,'standalone acquisition JSON')
  expected_raw=[]
  for x in raw['files']:
   for f,u in itertools.product(FORMS,UNITS):expected_raw.append(dict(file=x['path'],role=x['role'],mathematical_premise=str(x['mathematical_premise']),whole_bytes=str(x['bytes']),sha256=x['sha256'],occurrences=str(len(x['occurrences'])),normalization=f,unit=u,cost=str(x['metrics'][f][u])))
  need(csvrows(p/'raw_files.csv')==expected_raw,'all 1020 whole raw cells')
  expected_occ=[]
  for x in raw['occurrence_bindings']:
   expected_occ.append(dict(path=x['path'],sha256=x['sha256'],whole_bytes=str(x['bytes']),role=x['role'],mathematical_premise=str(x['mathematical_premise']),original_role=x['original_role'],application_occurrence=x['application_occurrence']))
  need(csvrows(p/'raw_occurrences.csv')==expected_occ,'all 127 raw occurrence rows')
 return {'status':'PASS_INDEPENDENT_ARITHMETIC','fractions':90,'PDF_components':150,'raw_role_components':240,'raw_unique_cells':1020,'raw_occurrences':127,'cumulative_stages':90,'required_whole_files':83,'required_original_bytes':422956,'primary':primary,'role_bytes':rb,'own_science_or_extraction_rerun':False}
