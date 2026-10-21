"""Complete unified-B arithmetic; all input boundaries are already accepted."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import copy,hashlib,json
H=Path(__file__).resolve().parent
INPUT_PIN='e6f86129f414b960078738c0ae43cc799a78a3053c88af99965d605c9371c0b0'
REVIEW_PIN='67eded6cc8c36562cca175820827038f04dce4b7b7e1b69cb3893375c9532194'
PROTOCOL_PIN='d0ac3b3c30a9ac480a926b96824dc6d1334bd06b7c1a324f3230351d9dc5812c'
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
ORIGINALS=['N001','N003','N008','L030','L040']
def need(ok,text):
 if not ok:raise ValueError('UNIFIED_B_NUMERICAL_REJECT: '+text)
def load(path):return json.loads(Path(path).read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def save(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def bind(root,row):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative input');b=(root/p).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact bound input '+str(p));return b

def manifests():
 for folder,pin in [('inputs',INPUT_PIN),('input_review',REVIEW_PIN)]:
  need(sha((H/folder/'manifest.json').read_bytes())==pin,'exact independently accepted input packet')
  for row in load(H/folder/'manifest.json')['exports']:bind(H/folder,row)
 need(sha((H/'protocol_freeze.json').read_bytes())==PROTOCOL_PIN,'precalculation numerical boundary');bind(H,load(H/'protocol_freeze.json')['protocol'])
 if (H/'manifest.json').exists():
  for row in load(H/'manifest.json')['exports']:bind(H,row)

def validate_inputs(c,source,ip,review,recount,p):
 need(review['status']=='ROOT_ACCEPTED_COMPLETE_B_INPUTS' and review['author_input_manifest_sha256']==INPUT_PIN and review['counts_accepted'] and review['numerical_factor_calculation_may_proceed'],'distinct root input acceptance')
 need(review['originals']==p['originals']==source['source_order']==ORIGINALS and review['source_rows']==p['source_rows']==65 and review['proof_contexts']==p['proof_contexts']==56,'all five contracts and contexts')
 need(list(c['documents'])==['U_B','B1','B2','B3','B4','B5','CODE'] and [r['pages'] for r in c['documents'].values()]==[16,3,4,4,5,11,7],'whole fifty-page current edition')
 need({k:r['metrics'] for k,r in c['documents'].items()}==recount['documents'],'all independently accepted PDF metrics/text hashes')
 need({k:r['metrics'] for rows in c['raw_files'].values() for k,r in rows.items()}==recount['raw_files'],'all whole raw-file coordinates')
 need(source['coordinates']==recount['source_coordinates'] and len(source['coordinates'])==30,'all 150 source and thirty article-only costs fixed')
 need(p['common']==['U_B'] and p['applications']==dict(zip(ORIGINALS,['B1','B2','B3','B4','B5'])) and p['all_current_common_and_applications_whole'] and p['prior_two_common_papers_not_added'],'one whole unified common and complete applications')
 need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'] and p['units']==UNITS and p['primary']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace'),'unchanged full primary and thirty sensitivities')
 need(not p['N001_original_PDF_available'] and p['N001_representation']=='literal_authored_rendering' and p['source_representations_unchanged'],'no invented N001 PDF')
 need(p['L040_cover_in_primary'] and all(r['source_representations']['N001']=='literal_authored_rendering' for r in source['coordinates']),'literal original representation and full cover')
 need([len(c['raw_files'][cat]) for cat in ['programs','drivers','formal']]==[4,2,2] and p['complete_programs']==4 and p['operational_drivers_separate']==2 and p['formal_files_separate']==2 and p['partial_declarations']==14,'four full programs, two drivers and fourteen partial declarations')
 need(p['program_roles']==[r['role'] for r in ip['programs']]==['required_finite_primitive_inputs','finite_validation','finite_validation','required_only_for_auxiliary_n8_and_validation_of_branching'],'exact program proof/validation roles')
 for cat in ['programs','drivers','formal']:
  need(set(c['raw_files'][cat])=={r['path'] for r in ip[cat]},'whole raw-file roster')
  for r in ip[cat]:need(all(c['raw_files'][cat][r['path']][k]==r[k] for k in ['bytes','sha256','role']),'exact complete raw file and role')
 need(p['raw_and_printed_are_alternatives'] and p['whole_comparisons']==['written','including_printed_programs','including_raw_programs'],'three complete denominator boundaries without double counting')
 need(p['unknown_costs']==c['unknown_costs'] and all(v is None for v in p['unknown_costs'].values()),'unknown costs null')
 need(all(p[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new scientific credit')
 need([p[k] for k in ['ordinary_coordinates','whole_fractions','conditional_fractions','article_only_fractions','total_exact_fractions']]==[30,90,150,120,360],'complete main and cover-sensitivity accounting')

def fraction(n,d):
 need(isinstance(n,int) and isinstance(d,int) and n>0 and d>0,'positive exact costs');f=Fraction(n,d)
 with localcontext() as c:c.prec=42;decimal=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)

def calculate(c,source,p):
 rows=[]
 for old in source['coordinates']:
  v,n,u=[old[k] for k in ['variant','normalization','unit']];docs={k:r['metrics'][v][n][u] for k,r in c['documents'].items()};originals=dict(old['sources']);apps={k:docs[a] for k,a in p['applications'].items()};common=docs['U_B'];written=common+sum(apps.values());total=sum(originals.values());files={cat:{k:r['metrics'][n][u] for k,r in rs.items()} for cat,rs in c['raw_files'].items()};raw=sum(files['programs'].values());printed=docs['CODE'];denoms=dict(written=written,including_printed_programs=written+printed,including_raw_programs=written+raw);article=total-originals['L040']+old['L040_article_only']
  rows.append(dict(variant=v,normalization=n,unit=u,source_costs=originals,source_representations=old['source_representations'],source_sum=total,document_costs=docs,common_theory=common,applications=apps,all_applications=sum(apps.values()),written_denominator=written,printed_program_cost=printed,raw_program_cost=raw,denominators=denoms,whole={k:fraction(total,d) for k,d in denoms.items()},conditional={k:fraction(originals[k],apps[k]) for k in ORIGINALS},article_only_sensitivity=dict(L040_article_cost=old['L040_article_only'],source_sum=article,whole={k:fraction(article,d) for k,d in denoms.items()},L040_conditional=fraction(old['L040_article_only'],apps['L040']),all_replacement_costs_unchanged=True,other_four_conditionals_unchanged=True),raw_file_costs=files,operational_driver_cost=sum(files['drivers'].values()),partial_formal_cost=sum(files['formal'].values())))
 primary=next(r for r in rows if all(r[k]==v for k,v in p['primary'].items()))
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic='B',title=p['title'],originals=ORIGINALS,source_rows=65,proof_contexts=56,coordinates=30,main_exact_fractions=240,cover_sensitivity_fractions=120,total_exact_fractions=360,rows=rows,primary=primary,source_representations_unchanged=True,N001_original_PDF_cost=None,N001_current_representation='literal_authored_rendering',complete_current_common_charged_once=True,all_five_applications_complete=True,whole_programs=4,raw_printed_alternatives=True,conditional_acquisition=p['conditional_acquisition'],operational_drivers=2,partial_formal_files=2,partial_declarations=14,unknown_costs=p['unknown_costs'],new_source_credit=0,new_question_credit=0,new_formal_credit=0)

def validate_results(r,c,s,p):
 need(r==calculate(c,s,p),'all exact costs, fractions, source representations and cover sensitivities')
 need(len(r['rows'])==30 and r['total_exact_fractions']==360,'complete coordinate/fraction grid')
 for z in r['rows']:
  need(z['written_denominator']==z['common_theory']+sum(z['applications'].values()),'entire common once and every complete application')
  for f in list(z['whole'].values())+list(z['conditional'].values())+list(z['article_only_sensitivity']['whole'].values())+[z['article_only_sensitivity']['L040_conditional']]:need(f['numerator']*f['reduced_denominator']==f['denominator']*f['reduced_numerator'],'exact rational identity')

def controls(c,s,ip,review,recount,p,r):
 tests=[]
 def reject(name,call):
  try:call()
  except (ValueError,KeyError,TypeError):tests.append(name);return
  raise ValueError('accepted mutation '+name)
 for name,edit in [('omit fifth application',lambda q:q['applications'].pop('L040')),('add earlier common too',lambda q:q['common'].append('old_U')),('invent N001 PDF',lambda q:q.update(N001_original_PDF_available=True)),('drop L040 cover in primary',lambda q:q.update(L040_cover_in_primary=False)),('double-charge raw and printed',lambda q:q.update(raw_and_printed_are_alternatives=False)),('drop complete program',lambda q:q.update(complete_programs=3)),('promote validation',lambda q:q['program_roles'].__setitem__(1,'required_finite_primitive_inputs')),('omit raw sensitivity',lambda q:q['variants'].remove('raw_untrimmed')),('unknown proof cost zero',lambda q:q['unknown_costs'].update(retained_external_proofs=0)),('new formal credit',lambda q:q.update(new_formal_credit=14)),('drop separate driver',lambda q:q.update(operational_drivers_separate=1))]:
  q=copy.deepcopy(p);edit(q);reject(name,lambda q=q:validate_inputs(c,s,ip,review,recount,q))
 q=copy.deepcopy(s);q['coordinates'][0]['sources']['L040']=1;reject('change accepted original cost',lambda:validate_inputs(c,q,ip,review,recount,p))
 q=copy.deepcopy(s);q['coordinates'][0]['L040_article_only']=1;reject('change direct article-only input',lambda:validate_inputs(c,q,ip,review,recount,p))
 q=copy.deepcopy(c);q['documents']['B5']['pages']=10;reject('omit final bibliography page',lambda:validate_inputs(q,s,ip,review,recount,p))
 q=copy.deepcopy(c);q['raw_files']['programs'].pop('programs/boundary_example.g');reject('prune full auxiliary program',lambda:validate_inputs(q,s,ip,review,recount,p))
 for name,edit in [('conditional omits context',lambda z:z['rows'][0]['conditional']['L040'].update(denominator=1)),('wrong reduced fraction',lambda z:z['rows'][0]['whole']['written'].update(reduced_numerator=1)),('cover sensitivity alters denominator',lambda z:z['rows'][0]['article_only_sensitivity']['whole']['written'].update(denominator=1)),('printed programs counted twice',lambda z:z['primary'].update(printed_program_cost=1)),('missing source PDF priced zero',lambda z:z.update(N001_original_PDF_cost=0))]:
  q=copy.deepcopy(r);edit(q);reject(name,lambda q=q:validate_results(q,c,s,p))
 return tests

def compute():
 manifests();p=load(H/'protocol.json');c=load(H/'inputs/author_counts.json');s=load(H/'inputs/retained_source_counts.json');ip=load(H/'inputs/policy.json');review=load(H/'input_review/review.json');recount=load(H/'input_review/recount.json')
 validate_inputs(c,s,ip,review,recount,p);r=calculate(c,s,p);validate_results(r,c,s,p);return r,controls(c,s,ip,review,recount,p,r)
