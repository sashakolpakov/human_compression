"""Exact whole-paper arithmetic over already accepted Diagonal inputs."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import copy,hashlib,json
H=Path(__file__).resolve().parent
INPUT_PIN='4e7991712d5e186c5d0eca9a8173f245a2d1a584eadb1187ef952cef48caec04'
REVIEW_PIN='aaba6c23e49f13b3a761fde6c0fac4c5ff1d91c2ba8659488a8881eda3446381'
PROTOCOL_PIN='89e96d87b38c342c578559e03d3e5557e0d0f169585af24c3b61705dfc89fd03'
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(ok,text):
 if not ok:raise ValueError('DIAGONAL_NUMERICAL_REJECT: '+text)
def load(path):return json.loads(Path(path).read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def save(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def bind(root,row):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative input');data=(root/p).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact binding '+str(p));return data

def manifests():
 for folder,pin in [('inputs',INPUT_PIN),('input_review',REVIEW_PIN)]:
  need(sha((H/folder/'manifest.json').read_bytes())==pin,'exact independently accepted input manifest')
  for row in load(H/folder/'manifest.json')['exports']:bind(H/folder,row)
 need(sha((H/'protocol_freeze.json').read_bytes())==PROTOCOL_PIN,'fixed arithmetic boundary before evaluation');bind(H,load(H/'protocol_freeze.json')['protocol'])
 if (H/'manifest.json').exists():
  for row in load(H/'manifest.json')['exports']:bind(H,row)

def validate_inputs(counts,policy,review,recount,protocol,external):
 need(review['status']=='ROOT_ACCEPTED_COMPLETE_MEASUREMENT_INPUTS' and review['author_manifest_sha256']==INPUT_PIN and review['numeric_counts_accepted'] and review['numerical_factor_calculation_may_proceed'],'distinct accepted full inputs')
 need(review['source_ids']==['N007','N006'] and review['source_rows']=={'N007':32,'N006':27},'two complete corrected contracts')
 need(review['glyph_decision']['status']=='ACCEPTED_AS_DECLARED_ENCODED_EVENT_PROXIES' and not review['glyph_decision']['literal_unicode_claim'],'honest graphical proxy convention')
 need(list(counts['documents'])==['N007','N006','U','A1','A2','A2nine','A2HN','CODEold'],'all eight full PDFs')
 need([r['pages'] for r in counts['documents'].values()]==[12,22,8,5,8,5,4,2],'all sixty-six pages including three companions')
 need(counts['pdf_metric_cells']==240 and counts['raw_metric_cells']==280 and counts['text_only_sensitivity_cells']==80,'full adopted input dimensions')
 need({k:r['metrics'] for k,r in counts['documents'].items()}==recount['documents'],'all independent PDF coordinates and hashes')
 need({k:r['metrics'] for k,r in counts['text_only_sensitivity'].items()}==recount['text_only_sensitivity'],'independent text-only sensitivity')
 need({k:r['metrics'] for rows in counts['raw_files'].values() for k,r in rows.items()}==recount['raw_files'],'all independent whole raw files')
 need([len(counts['raw_files'][k]) for k in ['programs','required_drivers','drivers','formal']]==[19,2,4,3],'all files and distinct roles')
 need(sum(r['role']=='required_finite_proof_or_complete_witness' for r in counts['raw_files']['programs'].values())==16 and sum(r['role']=='validation' for r in counts['raw_files']['programs'].values())==3,'sixteen required and three validation files')
 for category in ['programs','required_drivers','drivers','formal']:
  need(set(counts['raw_files'][category])=={r['path'] for r in policy[category]},'full exact file inventory '+category)
  for r in policy[category]:
   now=counts['raw_files'][category][r['path']];need(all(now[k]==r[k] for k in ['bytes','sha256','role']),'full file binding and role')
 need(protocol['common']==['U'] and protocol['applications']=={'N007':['A1'],'N006':['A2','A2nine','A2HN']} and protocol['written_denominator']==['U','A1','A2','A2nine','A2HN'],'whole current common and every local companion, old common not added')
 need(protocol['required_whole_raw_files']==19 and protocol['required_decoding_drivers']==2 and protocol['complete_printed_program_alternative'] is None,'all raw software, no false complete printed route')
 need(protocol['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and protocol['additional_variant']=='text_only_sensitivity' and protocol['normalizations']==['NFC','NFKC'] and protocol['units']==UNITS,'all forty coordinate settings')
 need(protocol['no_large_witness_discount'] and protocol['no_cross_topic_discount'] and protocol['binary_decoded_compressed_decompressed_alternatives'],'no hidden discount or double representation')
 need(protocol['operational_drivers_separate']==4 and protocol['formal_files_separate']==3 and protocol['partial_declarations']==17,'operational and partial formal scope')
 need(external['required_representation_bytes']==protocol['external_representation_bytes_separate']==21960689 and external['installed_file_bytes_once']==protocol['listed_installed_bytes_separate']==2516249,'complete external bytes shown separately')
 need(external['required_representation_files']==4 and len(external['installed_files_once_by_identical_hash'])==16,'all external representations and listed installed files')
 need(external['unknown_proof_cost'] is None and not external['compact_word_discount'] and not external['cross_topic_overlap_discount'],'external bytes do not price proofs')
 need(all(v is None for v in protocol['unknown_costs'].values()) and protocol['unknown_costs']==counts['unknown_costs'],'unknowns null')
 need(protocol['excluded_later_certificates']==['Fi22','Fi24prime'] and all(protocol[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new scientific credit or excluded exception import')

def fraction(n,d):
 need(isinstance(n,int) and isinstance(d,int) and n>0 and d>0,'positive exact costs');f=Fraction(n,d)
 with localcontext() as c:c.prec=42;decimal=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)

def calculate(counts,protocol):
 rows=[]
 for variant in protocol['variants']+[protocol['additional_variant']]:
  for norm in protocol['normalizations']:
   for unit in protocol['units']:
    docs={k:(counts['text_only_sensitivity'][k]['metrics'][norm][unit] if variant=='text_only_sensitivity' else r['metrics'][variant][norm][unit]) for k,r in counts['documents'].items()}
    originals={k:docs[k] for k in ['N007','N006']};apps={k:sum(docs[d] for d in ids) for k,ids in protocol['applications'].items()};common=docs['U'];written=common+sum(apps.values());numerator=sum(originals.values())
    files={category:{name:r['metrics'][norm][unit] for name,r in rs.items()} for category,rs in counts['raw_files'].items()};programs=sum(files['programs'].values());decoders=sum(files['required_drivers'].values())
    rows.append(dict(variant=variant,normalization=norm,unit=unit,original_costs=originals,source_sum=numerator,document_costs=docs,common_theory=common,application_costs=apps,all_applications=sum(apps.values()),written_denominator=written,whole_program_cost=programs,required_decoder_cost=decoders,whole_software_cost=programs+decoders,program_inclusive_denominator=written+programs+decoders,complete_printed_program_denominator=None,old_single_printed_validation_cost=docs['CODEold'],raw_file_costs=files,operational_driver_cost=sum(files['drivers'].values()),partial_formal_cost=sum(files['formal'].values()),whole={'written':fraction(numerator,written),'including_whole_raw_software':fraction(numerator,written+programs+decoders)},conditional={k:fraction(originals[k],apps[k]) for k in ['N007','N006']}))
 primary=next(r for r in rows if all(r[k]==v for k,v in protocol['primary'].items()))
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic='Diagonal',title=protocol['title'],originals=['N007','N006'],source_rows=protocol['source_rows'],ordinary_coordinates=30,text_only_coordinates=10,exact_whole_fractions=80,exact_conditional_fractions=80,total_exact_fractions=160,rows=rows,primary=primary,conditional_acquisition=protocol['conditional_acquisition'],complete_printed_program_alternative=None,external_bytes={'required_representation_files':4,'required_representation_bytes':21960689,'listed_installed_files':16,'listed_installed_bytes':2516249,'not_character_counts':True,'full_runtime_cost':None,'proof_cost':None},unknown_costs=protocol['unknown_costs'],source_exceptions_outside_this_edition=['Fi22','Fi24prime'],new_source_credit=0,new_question_credit=0,new_formal_credit=0)

def validate_results(results,counts,protocol):
 need(results==calculate(counts,protocol),'every exact numerator, denominator, companion, software file and displayed boundary')
 need(len(results['rows'])==40 and results['total_exact_fractions']==160,'complete forty-coordinate arithmetic')
 for r in results['rows']:
  need(r['written_denominator']==r['common_theory']+sum(r['application_costs'].values()),'whole common once and all applications')
  need(r['program_inclusive_denominator']==r['written_denominator']+sum(r['raw_file_costs']['programs'].values())+sum(r['raw_file_costs']['required_drivers'].values()),'whole raw software including decoding drivers')
  for f in list(r['whole'].values())+list(r['conditional'].values()):need(f['numerator']*f['reduced_denominator']==f['denominator']*f['reduced_numerator'],'exact rational reduction')

def controls(counts,policy,review,recount,protocol,external,results):
 checks=[]
 def reject(name,call):
  try:call()
  except (ValueError,KeyError,TypeError):checks.append(name);return
  raise ValueError('accepted mutation '+name)
 for name,edit in [('drop HN companion',lambda p:p['applications']['N006'].remove('A2HN')),('omit required decoder',lambda p:p.update(required_decoding_drivers=1)),('drop large witness',lambda p:p.update(required_whole_raw_files=18)),('invent full printed appendix',lambda p:p.update(complete_printed_program_alternative='CODEold')),('remove raw sensitivity',lambda p:p['variants'].remove('raw_untrimmed')),('remove text-only sensitivity',lambda p:p.update(additional_variant='calibrated_selected')),('discount large witnesses',lambda p:p.update(no_large_witness_discount=False)),('unknown graphic cost zero',lambda p:p['unknown_costs'].update(full_graphics=0)),('add unmeasured Fischer exception',lambda p:p['excluded_later_certificates'].pop()),('full formalization claim',lambda p:p.update(partial_declarations=0)),('charge previous common too',lambda p:p['common'].append('Uold'))]:
  p=copy.deepcopy(protocol);edit(p);reject(name,lambda p=p:validate_inputs(counts,policy,review,recount,p,external))
 for name,edit in [('omit full witness from counts',lambda c:c['raw_files']['programs'].pop(next(k for k in c['raw_files']['programs'] if 'J3_' in k))),('reinterpret validation as proof',lambda c:next(r for r in c['raw_files']['programs'].values() if r['role']=='validation').update(role='required_finite_proof_or_complete_witness')),('source count changed',lambda c:c['documents']['N006']['metrics']['calibrated_selected']['NFC'].update(characters_without_whitespace=1)),('omit N006 reference page',lambda c:c['documents']['A2'].update(pages=7))]:
  c=copy.deepcopy(counts);edit(c);reject(name,lambda c=c:validate_inputs(c,policy,review,recount,protocol,external))
 for name,edit in [('wrong reduced fraction',lambda r:r['rows'][0]['whole']['written'].update(reduced_numerator=1)),('conditional omits companion',lambda r:r['rows'][0]['conditional']['N006'].update(denominator=1)),('program total omits decoder',lambda r:r['primary'].update(required_decoder_cost=0)),('discounted complete software',lambda r:r['rows'][1].update(whole_program_cost=0)),('external proof assigned zero',lambda r:r['external_bytes'].update(proof_cost=0))]:
  r=copy.deepcopy(results);edit(r);reject(name,lambda r=r:validate_results(r,counts,protocol))
 return checks

def compute():
 manifests();p=load(H/'protocol.json');c=load(H/'inputs/author_counts.json');ip=load(H/'inputs/policy.json');review=load(H/'input_review/review.json');recount=load(H/'input_review/recount.json');external=load(H/'inputs/external_data.json')
 validate_inputs(c,ip,review,recount,p,external);r=calculate(c,p);validate_results(r,c,p);tests=controls(c,ip,review,recount,p,external,r)
 return r,tests
