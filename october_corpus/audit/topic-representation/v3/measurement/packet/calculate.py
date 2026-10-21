"""Exact arithmetic from independently accepted complete Representation inputs."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import hashlib,json
ROOT=Path(__file__).resolve().parent
PINS={'input':'4c61d955ddc8178c759e7943cde62deefb3c6696878a54d095146e207e5c8b29','review':'3c103ab2a8991bbbd532e572b5fead2940783de74bcb71d480263d102be6f8f1','root':'6455c8cb576814818bd563dcb12d776aeff829fbebfad19d90686f7736334a1e'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
DOCS=['F010','L126','U_R','R1','R2','CODE'];COMPARE=['written','conditional_F010','conditional_L126']
ROLES=['required_finite_certificate','required_graph_data','optional_validation','current_orchestration_driver','partial_formal_evidence']
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(n,d):
 need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer costs');f=Fraction(n,d)
 with localcontext()as c:c.prec=50;decimal=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def load(root=ROOT):
 p=read(root/'protocol.json');data={}
 for x in p['inputs']:
  f=Path(x['path']);need(not f.is_absolute()and '..'not in f.parts,'safe copied path')
  need((root/f).stat().st_size==x['bytes']and sha(root/f)==x['sha256'],'exact input '+str(f))
  data[f.name]=read(root/f)
  if x['source_export']!='manifest.json':
   m=read(root/x['manifest']);e=next(e for e in m['exports']if e['path']==x['source_export']);need((e['bytes'],e['sha256'])==(x['bytes'],x['sha256']),'manifest owns input')
 for k,v in PINS.items():need(sha(root/'inputs'/(k+'_manifest.json'))==v,'adopted manifest '+k)
 policy=data['input_policy.json'];ad=data['root_adoption.json'];a=data['input_author_counts.json'];i=data['review_independent_counts.json'];raw=data['input_raw_file_map.json']
 need(ad['status']=='ROOT_ACCEPTED_REPRESENTATION_SUCCESSOR_MEASUREMENT_INPUTS'and ad['numerical_authoring_permitted']is True,'root numerical permission')
 need(ad['input_manifests']['author']['sha256']==PINS['input']and ad['input_manifests']['independent']['sha256']==PINS['review'],'root evidence chain')
 need(p['primary']==[policy['primary'][k]for k in ['variant','normalization','unit']]==['calibrated_selected','NFC',UNITS[2]],'fixed inherited primary')
 need(p['written_documents']==['U_R','R1','R2']and p['source_ids']==DOCS[:2]and p['conditional_applications']=={'F010':'R1','L126':'R2'},'whole documents')
 need(p['allowed_comparisons']==COMPARE and p['software_inclusive_factor']is None and not p['optional_validation_required']and p['required_graph_certificate_and_data_acquired_for_L126']and p['no_sibling_application_dependency'],'symmetric acquisition boundary')
 need(policy['variants']==VARIANTS and policy['normalizations']==FORMS and policy['units']==UNITS,'all30 coordinates')
 need(list(a['documents'])==DOCS and[a['documents'][k]['pages']for k in DOCS]==[13,13,13,4,12,16],'full71 pages')
 need(a['documents']==i['documents']and a['raw_files']==i['raw_files'],'independent 180/170 input cells')
 need(a['documents']['F010']==data['input_accepted_F010_counts.json'],'every prior F010 source cell unchanged')
 need(len(raw['files'])==17 and all(x['whole_file']for x in raw['files']),'all17 complete files')
 need([sum(x['role']==r for x in raw['files'])for r in ROLES]==[1,1,9,2,4],'required versus optional file roles')
 need(raw['partial_declarations']==22 and raw['mandatory_data_files']==1,'partial formal and data')
 return data

def row(v,f,u,c,raw):
 return dict(variant=v,normalization=f,unit=u,costs=c,raw_costs=raw,totals={'source':c['F010']+c['L126'],'common':c['U_R'],'applications':c['R1']+c['R2'],'written':c['U_R']+c['R1']+c['R2']},comparisons={'written':frac(c['F010']+c['L126'],c['U_R']+c['R1']+c['R2']),'conditional_F010':frac(c['F010'],c['R1']),'conditional_L126':frac(c['L126'],c['R2'])},software_inclusive_factor=None,inventory={'printed_all10_programs':c['CODE'],'raw_all10_programs':raw['required_finite_certificate']+raw['optional_validation'],'mandatory_graph_data':raw['required_graph_data'],'printed_and_raw_code_are_alternatives':True,'data_is_not_in_printed_code':True,'source_software_cost':None})

def calculate(root=ROOT):
 d=load(root);a=d['input_author_counts.json'];p=d['input_policy.json'];rm=d['input_raw_file_map.json'];coords=[]
 for v in VARIANTS:
  for f in FORMS:
   for u in UNITS:
    c={k:a['documents'][k]['variants'][v][f][u]for k in DOCS}
    raw={r:sum(a['raw_files'][x['key']]['metrics'][f][u]for x in rm['files']if x['role']==r)for r in ROLES}
    coords.append(row(v,f,u,c,raw))
 primary=next(x for x in coords if[x['variant'],x['normalization'],x['unit']]==['calibrated_selected','NFC',UNITS[2]])
 r=dict(status='AUTHOR_NUMERICAL_SUCCESSOR_PENDING_DISTINCT_REVIEW',topic='Representation',title='Groups represented by incidence geometries',source_ids=DOCS[:2],source_titles=d['input_source_boundary.json']['source_titles'],input_manifests=PINS,primary_coordinate=['calibrated_selected','NFC',UNITS[2]],coordinate_count=30,exact_fraction_count=90,whole_written_fractions=30,conditional_fractions=60,coordinates=coords,primary=primary,physical_pages=dict(zip(DOCS,[13,13,13,4,12,16])),whole_document_map=d['input_document_map.json'],raw_file_inventory=rm,source_boundary=d['input_source_boundary.json'],unknown_costs=p['unknowns'],scope={'F010_blocks':6,'L126_dispositions':31,'whole_common_once':True,'both_complete_applications':True,'no_sibling_application_dependency':True,'programs_excluded_symmetrically':True,'optional_validation_required_for_conditional':False,'required_certificate_and_graph_data_for_L126':True,'retained_classical_premises_acquired':True,'whole_required_files_never_discounted':True,'full_source_formalized':False,'partial_Lean_declarations':22,'software_inclusive_factor':None,'source_software_cost':None},acquisition={'initial_common':['U_R'],'F010_local':['R1'],'L126_local':['R2'],'retained_classical_cost':None,'F010_required_software':[],'L126_required_software':['certificate/check.py','certificate/graph.json'],'optional_validation_is_not_prepaid':True,'complete_written_stages':[primary['costs']['U_R'],primary['costs']['U_R']+primary['costs']['R1'],primary['totals']['written']]},preservation={'F010_source_all30_cells_unchanged':True,'prior_R1_cells_reused':False,'every_current_own_PDF_reextracted_in_accepted_inputs':True,'old_science_and_measurement_packets_immutable':True,'no_extraction_font_or_science_rerun':True},interpretation={'whole_topic':'The complete replacement is longer in the fixed primary manuscript coordinate: expansion, not achieved whole-topic compression.','conditional':'Ratios measure each complete local application after whole U and actual retained premises have been acquired. The L126 application also needs the entire graph certificate and JSON. Conditional reuse does not remove the initial common-theory cost.','boundary':'Written mathematical exposition including algorithms remains counted. Executable listings are excluded on both sides. Whole required and optional software/data is inventoried separately, not assigned a one-sided ratio.','graphs':'Whole-document acquisition and evidence association, not a theorem dependency DAG or a node-count comparison.'},author_roles='enumeration_review authored current science, inputs and this numerical packet. enumeration_volume independently reviewed science/migration/inputs; root independently adopted inputs. This packet is not independent numerical acceptance.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False)
 validate(r);return r

def validate(r):
 need(len(r['coordinates'])==30 and{(x['variant'],x['normalization'],x['unit'])for x in r['coordinates']}=={(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS},'all30 unique coordinates')
 for x in r['coordinates']:
  need(list(x['costs'])==DOCS and list(x['raw_costs'])==ROLES,'all cost components')
  need(x==row(x['variant'],x['normalization'],x['unit'],x['costs'],x['raw_costs']),'whole exact arithmetic and inventory')
 primary=next(x for x in r['coordinates']if[x['variant'],x['normalization'],x['unit']]==r['primary_coordinate'])
 need(r['primary_coordinate']==['calibrated_selected','NFC',UNITS[2]]and r['primary']==primary,'fixed primary')
 need((r['coordinate_count'],r['exact_fraction_count'],r['whole_written_fractions'],r['conditional_fractions'])==(30,90,30,60),'fraction scope')
 need(r['source_ids']==DOCS[:2]and r['physical_pages']==dict(zip(DOCS,[13,13,13,4,12,16])),'full boundary')
 for k in ['whole_common_once','both_complete_applications','no_sibling_application_dependency','programs_excluded_symmetrically','required_certificate_and_graph_data_for_L126','retained_classical_premises_acquired','whole_required_files_never_discounted']:need(r['scope'][k]is True,'scope '+k)
 need(r['scope']['optional_validation_required_for_conditional']is False and r['scope']['software_inclusive_factor']is None and r['scope']['source_software_cost']is None,'symmetric software policy')
 need(r['scope']['partial_Lean_declarations']==22 and r['scope']['full_source_formalized']is False,'actual partial formal boundary')
 need(all(v is None for v in r['unknown_costs'].values()),'unknown is not zero')
 need(r['acquisition']['L126_required_software']==['certificate/check.py','certificate/graph.json']and r['acquisition']['optional_validation_is_not_prepaid'],'required acquisition')
 need(r['acquisition']['complete_written_stages']==[primary['costs']['U_R'],primary['costs']['U_R']+primary['costs']['R1'],primary['totals']['written']],'whole sequential acquisition')
 need(primary['totals']['source']<primary['totals']['written']and 'expansion' in r['interpretation']['whole_topic'],'candid primary expansion')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit'])and not r['primary_material_exported'],'no new credit/primary export')
