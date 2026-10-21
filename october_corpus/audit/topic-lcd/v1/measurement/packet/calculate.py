"""Exact LCD manuscript arithmetic from adopted whole-document inputs.

This module consumes accepted integer vectors; it performs no text extraction,
scientific computation, font inference, or software-inclusive comparison.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import hashlib,json
ROOT=Path(__file__).resolve().parent
PINS={'input':'3d4f1a989020ed6cf9e632263b785b79ecdf5d30765170760b8240f9c13d27cc','review':'2f9fa038f66491e5b8607970f7fa499a88f398a2868a72a80d3588948e954071','root':'214712d6b2976d813205ea083e59c14d88243c94b568233c7d9eef115ec5d6ac'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
DOCS=['L050','F017','U_LCD','A_L050','A_F017'];COMPARE=['written','conditional_L050','conditional_F017'];PRIMARY=['calibrated_selected','NFC',UNITS[2]]
ROLES=['required_program','required_derived_certificate','required_data','required_finite_record','optional_validation','operational_driver','partial_formal_file','partial_formal_scope'];REQUIRED=ROLES[:4]
ROLE_COUNTS=dict(zip(ROLES,[20,2,19,42,3,11,2,3]));PAGES=dict(zip(DOCS,[11,17,14,15,12]))
TITLES={
 'L050':'Linear codes with complementary duals from some strongly regular subgraphs of the McLaughlin graph',
 'F017':'LCD codes from adjacency matrices of graphs',
 'U_LCD':'Incidence operators, orthogonal codes and permutation modules',
 'A_L050':'Ternary codes from the Witt design and the plane of order four',
 'A_F017':'Reflexive and complementary dual codes from graph families'}
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(n,d):
 need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer manuscript costs');f=Fraction(n,d)
 with localcontext()as c:c.prec=50;decimal=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def effect(q):return 'expansion'if q['numerator']<q['denominator']else('equal length'if q['numerator']==q['denominator']else'local saving')
def load(root=ROOT):
 p=read(root/'protocol.json');d={}
 for x in p['inputs']:
  f=Path(x['path']);need(not f.is_absolute()and '..'not in f.parts,'safe copied input')
  need((root/f).stat().st_size==x['bytes']and sha(root/f)==x['sha256'],'exact input '+str(f));d[f.name]=read(root/f)
  if x['source_export']!='manifest.json':
   m=read(root/x['manifest']);e=next(e for e in m['exports']if e['path']==x['source_export']);need((e['bytes'],e['sha256'])==(x['bytes'],x['sha256']),'manifest owns '+str(f))
 for k,v in PINS.items():need(sha(root/'inputs'/(k+'_manifest.json'))==v,'accepted manifest '+k)
 need(sha(root/'protocol.json')==sha(root/'protocol_freeze/protocol.json'),'fixed pre-evaluation protocol')
 ad=d['root_adoption.json'];review=d['independent_result.json'];a=d['author_counts.json'];raw=d['raw_counts.json'];policy=d['input_policy.json'];boundary=d['raw_boundary.json']
 need(ad['status']=='ROOT_ACCEPTED_COMPLETE_LCD_MEASUREMENT_INPUTS'and ad['numerical_stage_authorized']is True,'root numerical authorization')
 need(ad['manifests']=={'topic_LCD_measurement_inputs_v2':PINS['input'],'topic_LCD_measurement_independent_review':PINS['review']},'exact adopted author and review')
 need(review['author_manifest_sha256']==PINS['input']and review['recount']['pdf_cells']==150 and review['recount']['raw_unique_cells']==1020,'distinct complete input recount')
 need(p['primary']==[policy['primary'][k]for k in ['variant','normalization','unit']]==PRIMARY,'fixed primary')
 need(p['variants']==policy['variants']==VARIANTS and p['normalizations']==policy['normalizations']==FORMS and p['units']==policy['units']==UNITS,'all30 policy coordinates')
 need(p['source_ids']==DOCS[:2]and p['written_documents']==DOCS[2:]and p['conditional_applications']=={'L050':'A_L050','F017':'A_F017'}and p['allowed_comparisons']==COMPARE,'complete manuscript routes')
 need(p['whole_required_boundary_acquired_for_each_conditional']and not p['optional_validation_required']and not p['sibling_premise'],'conditional acquisition')
 need(set(a['documents'])==set(DOCS)and{k:a['documents'][k]['pages']for k in DOCS}==PAGES and a['PDF_metric_cells']==150 and a['physical_pages']==69,'all5 complete PDFs/69 pages')
 dm={x['key']:x for x in d['document_map.json']['documents']}
 need(set(dm)==set(DOCS)and all(dm[k]['whole_document']and dm[k]['sha256']==a['documents'][k]['pdf_sha256']and dm[k]['pages']==PAGES[k]for k in DOCS),'exact whole PDF bindings')
 screen=d['listing_screen.json'];need(not screen['final_L050_application_screen_pending']and all(not x['executable_listings']and not x['masks']for x in screen['documents']),'no unmatched executable listing')
 need(screen['required_certificates_remain_premises']and screen['optional_validation_excluded_both_sides'],'symmetric software policy')
 need(len(raw['files'])==102 and len(raw['occurrence_bindings'])==127 and raw['metric_cells']==1020 and raw['whole_bytes']==548250,'complete raw closure')
 need(raw['roles']==ROLE_COUNTS and all(x['whole_file']for x in raw['files'])and len({x['sha256']for x in raw['files']})==102,'whole-content deduplication and roles')
 need(sum(x['bytes']for x in raw['files'])==548250,'whole raw bytes')
 for x in raw['files']:
  need(x['mathematical_premise']==(x['role']in REQUIRED),'preserve actual premise roles')
  actual=[y for y in raw['occurrence_bindings']if y['sha256']==x['sha256']]
  need(sorted(x['occurrences'])==sorted(y['path']for y in actual)and all(y['bytes']==x['bytes']for y in actual),'all duplicate occurrences disclosed')
 need(boundary['unique_partial_declarations']==9 and boundary['full_Lean']is False and boundary['source_software']is None and boundary['software_inclusive_factor']is None,'partial formal and unknown software')
 need(d['science_bindings.json']['F017_dispositions']==104 and d['science_bindings.json']['L050_dispositions']==54 and d['science_bindings.json']['whole_topic_science_accepted'],'accepted corrected contracts')
 return d

def row(v,f,u,c,raw):
 totals={'source':c['L050']+c['F017'],'common':c['U_LCD'],'applications':c['A_L050']+c['A_F017'],'written':c['U_LCD']+c['A_L050']+c['A_F017']}
 comparisons={'written':frac(totals['source'],totals['written']),'conditional_L050':frac(c['L050'],c['A_L050']),'conditional_F017':frac(c['F017'],c['A_F017'])}
 return dict(variant=v,normalization=f,unit=u,costs=c,raw_costs=raw,totals=totals,comparisons=comparisons,interpretation={k:effect(q)for k,q in comparisons.items()},acquisition={'common_then_L050_then_F017':[c['U_LCD'],c['U_LCD']+c['A_L050'],totals['written']],'required_raw_premises':sum(raw[k]for k in REQUIRED),'optional_raw_validation':raw['optional_validation'],'software_added_to_manuscript_denominator':False},software_inclusive_factor=None)

def calculate(root=ROOT):
 d=load(root);a=d['author_counts.json'];raw=d['raw_counts.json'];coords=[]
 for v in VARIANTS:
  for f in FORMS:
   for u in UNITS:
    c={k:a['documents'][k]['variants'][v][f][u]for k in DOCS}
    rc={k:sum(x['metrics'][f][u]for x in raw['files']if x['role']==k)for k in ROLES}
    coords.append(row(v,f,u,c,rc))
 primary=next(x for x in coords if[x['variant'],x['normalization'],x['unit']]==PRIMARY)
 role_inventory=[dict(role=k,whole_files=ROLE_COUNTS[k],whole_bytes=sum(x['bytes']for x in raw['files']if x['role']==k),mathematical_premise=k in REQUIRED)for k in ROLES]
 r=dict(status='AUTHOR_NUMERICAL_PACKET_PENDING_DISTINCT_REVIEW',topic='LCD',title='Incidence operators and codes',source_ids=DOCS[:2],titles=TITLES,source_attribution={'L050':{'authors':'Dimitri Leemans and Bernardo G. Rodrigues','edition':'Mathematical Communications 21 (2016), 239–249; complete eleven-page source'},'F017':{'authors':'Jennifer D. Key and Bernardo G. Rodrigues','edition':'Complete seventeen-page author manuscript, 4 August 2017'}},input_manifests=PINS,primary_coordinate=PRIMARY,coordinate_count=30,exact_fraction_count=90,whole_written_fractions=30,conditional_fractions=60,coordinates=coords,primary=primary,physical_pages=PAGES,whole_document_map=d['document_map.json'],raw_file_inventory=raw,raw_role_inventory=role_inventory,unknown_costs=d['input_policy.json']['unknowns'],scope={'L050_dispositions':54,'F017_dispositions':104,'whole_common_once':True,'both_complete_applications':True,'no_sibling_application_dependency':True,'programs_excluded_symmetrically':True,'optional_validation_required_for_conditional':False,'complete_required_program_data_records_acquired':True,'retained_classical_premises_acquired':True,'whole_required_files_never_discounted':True,'full_source_formalized':False,'unique_partial_Lean_declarations':9,'software_inclusive_factor':None,'source_software_cost':None,'printed_CODE_document_present':False,'graph_layout_cost':None},acquisition={'initial_common':['U_LCD'],'local_applications':{'L050':['A_L050'],'F017':['A_F017']},'required_whole_content_sha256':[x['sha256']for x in raw['files']if x['mathematical_premise']],'required_whole_files':sum(ROLE_COUNTS[k]for k in REQUIRED),'required_whole_bytes':sum(x['bytes']for x in raw['files']if x['mathematical_premise']),'required_boundary_policy':'Conservative complete-topic acquisition before either conditional comparison: all required whole programs, derived certificates, mandatory data and retained finite records. No claim that this union is a minimal premise set for each application.','retained_classical_cost':None,'optional_validation_is_not_prepaid':True,'complete_written_stages':primary['acquisition']['common_then_L050_then_F017']},retained_scope={'L050':'All four corrected principal Theorem 1 clauses and 54 source dispositions. Named graph/classification/Brauer and historical code-table inputs remain retained. Uniqueness of all SRG(253,140,87,65) and the other two fifteen-dimensional L3(4) module constructions remain unresolved.','F017':'All 104 recorded source dispositions, with seven explicitly retained input classes: association spectra, classical SRG parameters, earlier incidence-code descriptions, earlier distances, odd-characteristic incidence minima, ternary Proposition 18 memberships, and the prior generalized-Paley observation. Four large Paley pairs retain source upper bounds; general further-family and efficient-decoding questions are not solved.','corrections':'The compared applications recover corrected contracts, not every erroneous literal assertion. The scientific source maps retain each correction and exclusion. This numerical comparison does not establish new results or accept unresolved source questions.'},preservation={'accepted_PDF_cells':150,'accepted_raw_cells':1020,'raw_occurrences':127,'raw_unique_contents':102,'every_accepted_vector_preserved':True,'old_packets_immutable':True,'no_extraction_font_or_science_rerun':True},interpretation={'whole_topic':'The complete replacement is longer in the fixed primary manuscript coordinate: expansion, not achieved whole-topic compression.','conditional':'Each factor compares a complete source with its complete local application after the whole common paper, the complete declared required programs/data/finite records and actual retained premises have been acquired. Optional validation is not a proof premise. There is no sibling-application premise.','boundary':'Complete extracted manuscript text is counted, including title, abstract, tables, references and mathematical algorithm/proof prose. Executable listings are excluded symmetrically; none occurs in these five PDFs. Required and optional software/data are separately inventoried; unknown historical software prevents a software-inclusive scalar.','graphs':'Whole-document acquisition and declared premise associations, not a minimal theorem DAG or a node-count comparison. Complete-file graphs show the conservative acquired union, not every individual scientific dependency.'},author_roles='enumeration_volume authored the input and this numerical packet and the F017 application; rewrite_termination independently reviewed the inputs and authored L050; root authored substantial common/instance arguments and distinctly reviewed/adopted the current science and inputs. Numerical distinct acceptance is separate from this author packet.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False,pooled_factor=None)
 validate(r);return r

def validate(r):
 need(len(r['coordinates'])==30 and{(x['variant'],x['normalization'],x['unit'])for x in r['coordinates']}=={(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS},'all30 unique coordinates')
 for x in r['coordinates']:
  need(list(x['costs'])==DOCS and list(x['raw_costs'])==ROLES,'complete cost components')
  need(x==row(x['variant'],x['normalization'],x['unit'],x['costs'],x['raw_costs']),'exact arithmetic and acquisition')
 primary=next(x for x in r['coordinates']if[x['variant'],x['normalization'],x['unit']]==r['primary_coordinate'])
 need(r['primary_coordinate']==PRIMARY and r['primary']==primary,'fixed primary')
 need((r['coordinate_count'],r['exact_fraction_count'],r['whole_written_fractions'],r['conditional_fractions'])==(30,90,30,60),'fraction scope')
 need(r['source_ids']==DOCS[:2]and r['physical_pages']==PAGES,'full manuscript boundary')
 for k in ['whole_common_once','both_complete_applications','no_sibling_application_dependency','programs_excluded_symmetrically','complete_required_program_data_records_acquired','retained_classical_premises_acquired','whole_required_files_never_discounted']:need(r['scope'][k]is True,'scope '+k)
 need(not r['scope']['optional_validation_required_for_conditional']and r['scope']['software_inclusive_factor']is None and r['scope']['source_software_cost']is None and not r['scope']['printed_CODE_document_present'],'symmetric software boundary')
 need(r['scope']['unique_partial_Lean_declarations']==9 and not r['scope']['full_source_formalized'],'scoped formal evidence')
 need(all(v is None for v in r['unknown_costs'].values())and r['pooled_factor']is None,'unknown is not zero')
 raw=r['raw_file_inventory'];need(len(raw['files'])==102 and len(raw['occurrence_bindings'])==127 and len({x['sha256']for x in raw['files']})==102,'all whole contents and occurrences')
 need(r['acquisition']['required_whole_content_sha256']==[x['sha256']for x in raw['files']if x['mathematical_premise']]and r['acquisition']['required_whole_files']==83 and r['acquisition']['optional_validation_is_not_prepaid'],'complete conservative required acquisition')
 need(r['acquisition']['complete_written_stages']==primary['acquisition']['common_then_L050_then_F017'],'complete sequential manuscript acquisition')
 need(primary['totals']['source']<primary['totals']['written']and 'expansion' in r['interpretation']['whole_topic'],'candid expansion')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit'])and not r['primary_material_exported'],'no new credit/primary export')
