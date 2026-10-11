"""Whole-paper arithmetic over the distinctly accepted Operations inputs.
Pattern reused from the frozen Diagonal numerical packet; actual dimensions,
identities and whole-programme boundary are separately instantiated here.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
from collections import Counter
import json,hashlib,copy
H=Path(__file__).resolve().parent
INPUT_PIN='3b0d503dcdd3fe778a05213523fa248109b06f6639df31a6ddbc9196cd1b8b03'
REVIEW_PIN='edb9e44fe49f5cd32ce66a909cef4e0324861d3026d9863417d23417768960d7'
PROTOCOL_PIN='502943aa208a986afb827dc90b547f61c0266e69430a31bb9c18501189e6e204'
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,m):
 if not x:raise ValueError('OPERATIONS_NUMERICAL_REJECT: '+m)
def binding(root,row):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe exact input');b=(root/p).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound file '+str(p))
def manifests():
 for folder,pin in [('inputs',INPUT_PIN),('input_review',REVIEW_PIN)]:
  need(sha((H/folder/'manifest.json').read_bytes())==pin,'distinctly accepted input manifest')
  for row in load(H/folder/'manifest.json')['exports']:binding(H/folder,row)
 need(sha((H/'protocol_freeze.json').read_bytes())==PROTOCOL_PIN,'fixed prior numerical boundary');binding(H,load(H/'protocol_freeze.json')['protocol'])
 if (H/'manifest.json').exists():
  for row in load(H/'manifest.json')['exports']:binding(H,row)

def validate_inputs(c,p,review,recount,protocol,external):
 need(review['status']=='ROOT_ACCEPTED_COMPLETE_MEASUREMENT_INPUTS' and review['author_manifest_sha256']==INPUT_PIN and review['numeric_counts_accepted'] and review['numerical_factor_calculation_may_proceed'],'distinct input acceptance')
 need(review['source_rows']==protocol['source_rows']=={'N005':81,'N006':27,'N007':32},'complete source contracts')
 need(review['glyph_decision']['status']=='ACCEPTED_AS_DECLARED_ENCODED_EVENT_PROXIES' and not review['glyph_decision']['literal_unicode_claim'],'explicit proxy convention')
 need(list(c['documents'])==['N005','N006','N007','U','A0','A1','A2','A2nine','A2HN','CODEold','CODEnew'],'all eleven whole PDFs')
 need([r['pages'] for r in c['documents'].values()]==[60,22,12,21,18,5,8,5,4,2,4],'all 161 physical pages')
 need({k:r['metrics'] for k,r in c['documents'].items()}==recount['documents'],'all independent PDF cells/hashes')
 need({k:r['metrics'] for k,r in c['text_only_sensitivity'].items()}==recount['text_only_sensitivity'],'all independent text-only sensitivity')
 need({k:r['metrics'] for rows in c['raw_files'].values() for k,r in rows.items()}==recount['raw_files'],'all independent raw cells/hashes')
 need([len(c['raw_files'][k]) for k in ['programs','required_drivers','drivers','formal']]==[23,2,5,3],'all software categories')
 need(Counter(r['role'] for r in c['raw_files']['programs'].values())==Counter(required_finite_proof_or_witness=16,validation=5,required_finite_proof_s2_s3_s4=1,auxiliary_validation_controls=1),'17 required and 6 validation whole files')
 for cat in ['programs','required_drivers','drivers','formal']:
  need(set(c['raw_files'][cat])=={r['id'] for r in p[cat]},'exact complete file ID set')
  for r in p[cat]:need(all(c['raw_files'][cat][r['id']][k]==r[k] for k in ['bytes','sha256','role']),'whole file identity/role '+r['id'])
 need(protocol['common']==['U'] and protocol['applications']=={'N005':['A0'],'N006':['A2','A2nine','A2HN'],'N007':['A1']} and protocol['written_denominator']==['U','A0','A2','A2nine','A2HN','A1'],'whole theory once, all applications/companions')
 need(protocol['whole_program_files']==23 and protocol['required_decoding_drivers']==2 and protocol['complete_printed_program_alternative'] is None,'complete raw programme, no invented complete printed appendix')
 need(protocol['partial_printed_alternatives']=={'CODEold':['P.N007.diagonal_models'],'CODEnew':['P.N005.affine_example','P.N005.literal_twist','P.N005.presentation_identities']},'partial printed alternatives exact')
 need(protocol['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and protocol['additional_variant']=='text_only_sensitivity' and protocol['normalizations']==['NFC','NFKC'] and protocol['units']==UNITS,'all 30 ordinary +10 text-only coordinates')
 need(protocol['acquisition_order']==['U','N005','N006','N007'],'declared whole-document sequence')
 need(protocol['program_roles']=={'required_proof_or_witness':17,'validation':6},'correct programme role totals')
 need(all(s in protocol['conditional_acquisition'] for s in ['whole 21-page common theory','all 23 whole mathematical/validation files','both complete required decoding drivers','required external data']),'complete conditional preacquisition')
 need(protocol['no_large_witness_discount'] and protocol['no_cross_topic_discount'] and protocol['binary_decoded_compressed_decompressed_alternatives'],'no omitted witness or duplicated representation')
 need(protocol['operational_drivers_separate']==5 and protocol['formal_files_separate']==3 and protocol['partial_declarations']==17 and protocol['new_N005_formal_declarations']==0,'formal and operational scope')
 need(external['required_representation_bytes']==protocol['external_representation_bytes_separate']==21960689 and external['installed_file_bytes_once']==protocol['listed_installed_bytes_separate']==2516249,'full external storage disclosed')
 need(external['required_representation_files']==4 and len(external['installed_files_once_by_identical_hash'])==16 and external['unknown_proof_cost'] is None,'whole retained data and unpriced proofs')
 need(all(v is None for v in protocol['unknown_costs'].values()) and protocol['unknown_costs']==c['unknown_costs'],'unknown costs remain unknown')
 need(protocol['excluded_later_certificates']==['Fi22','Fi24prime'] and all(protocol[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no extra claim')
 need(protocol['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace'),'fixed primary unit')

def fraction(n,d):
 need(type(n)==type(d)==int and n>0 and d>0,'exact positive integer costs');f=Fraction(n,d)
 with localcontext() as ctx:ctx.prec=42;decimal=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)

def calculate(c,p):
 rows=[]
 for variant in p['variants']+[p['additional_variant']]:
  for norm in p['normalizations']:
   for unit in p['units']:
    docs={k:(c['text_only_sensitivity'][k]['metrics'][norm][unit] if variant=='text_only_sensitivity' else r['metrics'][variant][norm][unit]) for k,r in c['documents'].items()}
    originals={k:docs[k] for k in p['originals']};apps={k:sum(docs[j] for j in ids) for k,ids in p['applications'].items()};common=docs['U'];written=common+sum(apps.values());source=sum(originals.values())
    files={cat:{k:r['metrics'][norm][unit] for k,r in rs.items()} for cat,rs in c['raw_files'].items()};program=sum(files['programs'].values());decoder=sum(files['required_drivers'].values())
    cumulative=[dict(stage='U',current_increment=common,current_cumulative=common,matched_source_increment=0,matched_source_cumulative=0,scope='Theory acquisition before any matched application; not a claim of zero historical theory cost.')]
    a=common;b=0
    for k in p['originals']:
     a+=apps[k];b+=originals[k];cumulative.append(dict(stage=k,current_increment=apps[k],current_cumulative=a,matched_source_increment=originals[k],matched_source_cumulative=b))
    rows.append(dict(variant=variant,normalization=norm,unit=unit,document_costs=docs,original_costs=originals,source_sum=source,common_theory=common,application_costs=apps,all_applications=sum(apps.values()),written_denominator=written,raw_file_costs=files,whole_program_cost=program,required_decoder_cost=decoder,whole_software_cost=program+decoder,program_inclusive_denominator=written+program+decoder,complete_printed_program_denominator=None,partial_printed_costs={k:dict(printed_cost=docs[k],replaced_raw_cost=sum(files['programs'][i] for i in ids),whole_file_ids=ids,not_a_complete_program_denominator=True) for k,ids in p['partial_printed_alternatives'].items()},operational_driver_cost=sum(files['drivers'].values()),partial_formal_cost=sum(files['formal'].values()),acquisition=cumulative,whole=dict(written=fraction(source,written),including_whole_raw_software=fraction(source,written+program+decoder)),conditional={k:fraction(originals[k],apps[k]) for k in p['originals']}))
 primary=next(r for r in rows if all(r[k]==v for k,v in p['primary'].items()))
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic='Operations',title=p['title'],originals=p['originals'],source_rows=p['source_rows'],ordinary_coordinates=30,text_only_coordinates=10,exact_whole_fractions=80,exact_conditional_fractions=120,total_exact_fractions=200,rows=rows,primary=primary,conditional_acquisition=p['conditional_acquisition'],complete_printed_program_alternative=None,external_bytes=dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249,not_character_counts=True,full_runtime_cost=None,proof_cost=None),unknown_costs=p['unknown_costs'],source_exceptions_outside_this_edition=['Fi22','Fi24prime'],new_source_credit=0,new_question_credit=0,new_formal_credit=0)

def validate_results(r,c,p):
 need(r==calculate(c,p),'every whole-document cost, fraction and acquisition stage')
 need(len(r['rows'])==40 and r['total_exact_fractions']==200,'all forty coordinates')
 for x in r['rows']:
  need(x['written_denominator']==x['common_theory']+sum(x['application_costs'].values()),'whole theory once')
  need(x['program_inclusive_denominator']==x['written_denominator']+sum(x['raw_file_costs']['programs'].values())+sum(x['raw_file_costs']['required_drivers'].values()),'full programmes+both decoders')
  for f in list(x['whole'].values())+list(x['conditional'].values()):need(f['numerator']*f['reduced_denominator']==f['denominator']*f['reduced_numerator'],'exact rational reduction')

def controls(c,ip,review,recount,p,e,r):
 checks=[]
 def reject(n,call):
  try:call()
  except (ValueError,KeyError,TypeError):checks.append(n);return
  raise ValueError('accepted invalid numerical mutation '+n)
 for name,edit in [('omit HN',lambda x:x['applications']['N006'].pop()),('omit N005',lambda x:x['applications'].pop('N005')),('omit full conditional acquisition',lambda x:x.update(conditional_acquisition='Selected theory only')),('omit decoder',lambda x:x.update(required_decoding_drivers=1)),('omit witness',lambda x:x.update(whole_program_files=22)),('invent whole printed route',lambda x:x.update(complete_printed_program_alternative='CODEnew')),('drop raw sensitivity',lambda x:x['variants'].pop(0)),('drop text-only sensitivity',lambda x:x.update(additional_variant='calibrated_selected')),('discount witnesses',lambda x:x.update(no_large_witness_discount=False)),('external proofs zero',lambda x:x['unknown_costs'].update(retained_classification_proofs=0)),('cross-topic discount',lambda x:x.update(no_cross_topic_discount=False)),('old common also charged',lambda x:x['common'].append('Uold')),('N005 formal claim',lambda x:x.update(new_N005_formal_declarations=1)),('omit included validation file from printed alternative',lambda x:x['partial_printed_alternatives']['CODEnew'].pop()),('Fischer cost silently imported',lambda x:x['excluded_later_certificates'].pop())]:
  z=copy.deepcopy(p);edit(z);reject(name,lambda z=z:validate_inputs(c,ip,review,recount,z,e))
 for name,edit in [('omit large J3 witness',lambda x:x['raw_files']['programs'].pop('P.N006.J3_rank4_witness')),('demote affine finite premise',lambda x:x['raw_files']['programs']['P.N005.affine_example'].update(role='validation')),('alter source count',lambda x:x['documents']['N005']['metrics']['calibrated_selected']['NFC'].update(characters_without_whitespace=1)),('omit application page',lambda x:x['documents']['A0'].update(pages=17))]:
  z=copy.deepcopy(c);edit(z);reject(name,lambda z=z:validate_inputs(z,ip,review,recount,p,e))
 for name,edit in [('incorrect reduced fraction',lambda x:x['rows'][0]['whole']['written'].update(reduced_numerator=1)),('partial conditional denominator',lambda x:x['rows'][0]['conditional']['N006'].update(denominator=1)),('omit decoder from result',lambda x:x['primary'].update(required_decoder_cost=0)),('free initial theory',lambda x:x['primary']['acquisition'][0].update(current_increment=0)),('external proof priced zero',lambda x:x['external_bytes'].update(proof_cost=0)),('invent full printed factor',lambda x:x['primary'].update(complete_printed_program_denominator=1))]:
  z=copy.deepcopy(r);edit(z);reject(name,lambda z=z:validate_results(z,c,p))
 return checks

def compute():
 manifests();p=load(H/'protocol.json');c=load(H/'inputs/author_counts.json');ip=load(H/'inputs/policy.json');review=load(H/'input_review/review.json');recount=load(H/'input_review/recount.json');e=load(H/'inputs/external_data.json')
 validate_inputs(c,ip,review,recount,p,e);r=calculate(c,p);validate_results(r,c,p);tests=controls(c,ip,review,recount,p,e,r)
 return r,tests
