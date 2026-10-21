"""Exact six-original manuscript arithmetic from root-adopted input vectors only."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import csv,hashlib,io,json
R=Path(__file__).resolve().parent
POLICY='008f73ed89d259fb1b56b4f5132466b650ae96f201ec8d9885e63f0b352a4d73'
IDS=['N001','N003','N008','L030','L040','L047'];APPS=dict(zip(IDS,['B1','B2','B3','B4','B5','B6']))
V=['raw_untrimmed','raw_selected','calibrated_selected'];N=['NFC','NFKC'];U=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
PRIMARY=(V[0],N[0],U[2]);GROUPS=['required_or_auxiliary_programs','optional_validation','operational_drivers','partial_formal_files']
def load(p):return json.loads(Path(p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,m):
 if not b:raise ValueError(m)
def key(x):return tuple(x[k]for k in ['variant','normalization','unit'])
def fraction(n,d):
 need(type(n)is int and type(d)is int and n>0 and d>0,'positive whole integer costs');f=Fraction(n,d)
 with localcontext()as c:c.prec=42;decimal=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def bind(root,r):
 p=Path(r['path']);need(not p.is_absolute()and'..'not in p.parts,'relative binding');b=(root/p).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'exact '+str(p))
def inputs():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==POLICY,'fixed numerical protocol');bind(R,load(R/'protocol_freeze.json')['protocol'])
 for r in p['input_bindings']:
  bind(R,r);folder=R/Path(r['path']).parent
  for e in load(folder/'manifest.json')['exports']:bind(folder,e)
 for r in p['additional_bindings']:bind(R,r)
 for r in load(R/'prior/manifest.json')['exports']:
  if r['path']in ['results.json','protocol.json']:bind(R/'prior',r)
 if(R/'manifest.json').exists():
  for r in load(R/'manifest.json')['exports']:bind(R,r)
 admission=load(R/'inputs/root_review/admission.json');review=load(R/'inputs/root_review/review.json');c=load(R/'inputs/current/author_counts.json');roster=load(R/'inputs/current/precount/raw_inventory.json');prior=load(R/'prior/results.json')
 need(admission['status']=='ROOT_ADOPTED_DISTINCT_MEASUREMENT_INPUTS'and admission['originals']==IDS,'authoritative six-source admission')
 need(sha((R/'inputs/root_review/admission.json').read_bytes())=='f8140db7208fac58d195e8a90d0cd0c38eb5ab742551cd25fa90bd49fa6e9d72','metadata correction bound')
 need(review['status']=='ACCEPTED_DISTINCT_INPUT_REVIEW_AND_ROOT_ADOPTION'and review['author_manifest']['sha256']==p['author_input_manifest_sha256'],'distinct root adopted exact inputs')
 need(load(R/'prior/root_review/review.json')['author_manifest_sha256']==sha((R/'prior/manifest.json').read_bytes()),'accepted prior numerical records')
 need(p['source_order']==c['originals']==IDS and p['applications']==APPS and p['common_components']==['U_B','U_B6'],'all sources/apps/common')
 need((p['variants'],p['normalizations'],p['units'])==(V,N,U)and tuple(p['primary'][x]for x in ['variant','normalization','unit'])==PRIMARY,'fixed30 grid')
 need(c['total_main_document_cells']==480 and c['total_raw_cells']==170 and c['whole_programs']==10 and c['drivers']==5 and c['partial_Lean_files']==2,'accepted full cells/files')
 need(list(c['documents'])==['U_B','B1','B2','B3','B4','B5','CODE','L047','U_B6','B6','CODE6'],'exact11 PDF vectors plus5 inherited sources')
 need({k:z['pages']for k,z in c['documents'].items()}==dict(U_B=16,B1=3,B2=4,B3=4,B4=5,B5=11,CODE=7,L047=12,U_B6=10,B6=3,CODE6=7),'whole pages')
 need(len(roster['files'])==17 and len({r['file']['sha256']for r in roster['files']})==17 and roster['extra_stored_required_data']==[],'complete current whole contents')
 need((roster['required_or_auxiliary_programs'],roster['optional_validation_programs'],roster['drivers'],roster['Lean_files'])==(8,2,5,2),'preserve roles')
 return p,c,roster,prior

def inventory(c,roster):
 result=[]
 for z in roster['files']:
  if z['inherited']:a=c['raw_files'][z['category']][z['old_path']];need(a['sha256']==z['file']['sha256']and a['bytes']==z['file']['bytes'],'old raw binding')
  else:a=c['new_raw_files'][z['id']];need(a['file']==z['file'],'new raw binding')
  need(a['role']==z['role'],'unchanged role');group={'drivers':GROUPS[2],'formal':GROUPS[3]}.get(z['category'],GROUPS[1]if z['role']=='finite_validation'else GROUPS[0])
  result.append(dict(z,group=group,mathematical_premise=group==GROUPS[0],metrics=a['metrics']))
 return result

def derive(p,c,roster,prior):
 files=inventory(c,roster);groups={g:{'files':sum(x['group']==g for x in files),'literal_bytes':sum(x['file']['bytes']for x in files if x['group']==g),'metrics':{n:{u:sum(x['metrics'][n][u]for x in files if x['group']==g)for u in U}for n in N}}for g in GROUPS}
 old={key(x):x for x in prior['rows']};rows=[]
 for src in c['source_coordinates']:
  v,n,u=key(src);d={k:x['metrics'][v][n][u]for k,x in c['documents'].items()};s=dict(src['sources']);need(d['L047']==s['L047'],'source alias counted once');a={k:d[z]for k,z in APPS.items()};common=d['U_B']+d['U_B6'];total=sum(s.values());den=common+sum(a.values());cond={k:fraction(s[k],a[k])for k in IDS};o=old[(v,n,u)]
  need({k:s[k]for k in IDS[:-1]}==o['source_costs']and all(cond[k]==o['conditional'][k]for k in IDS[:-1]),'all150 prior conditional records exact')
  need(all(d[k]==val for k,val in o['document_costs'].items()),'all210 prior own PDF cells exact')
  rc={g:groups[g]['metrics'][n][u]for g in GROUPS};article=total-s['L040']+src['L040_article_only']
  stages=[dict(stage=0,acquire=['U_B'],source_written=0,replacement_written=d['U_B'])];ss=0;aa=d['U_B']
  for k in IDS:
   if k=='L047':
    aa+=d['U_B6'];stages.append(dict(stage=len(stages),acquire=['U_B6'],source_written=ss,replacement_written=aa))
   ss+=s[k];aa+=a[k];stages.append(dict(stage=len(stages),source=k,acquire=[APPS[k]],source_written=ss,replacement_written=aa))
  x=dict(variant=v,normalization=n,unit=u,source_costs=s,source_representations=src['source_representations'],document_costs=d,source_sum=total,common_components={k:d[k]for k in ['U_B','U_B6']},whole_common=common,applications=a,application_sum=sum(a.values()),whole_written=den,written=fraction(total,den),conditional=cond,prior_whole_written=o['whole']['written'],article_only_sensitivity=dict(L040_article_cost=src['L040_article_only'],source_sum=article,written=fraction(article,den),L040_conditional=fraction(src['L040_article_only'],a['L040']),all_replacement_costs_unchanged=True,other_five_conditionals_unchanged=True),separate_software=dict(printed_components={k:d[k]for k in ['CODE','CODE6']},whole_printed_programs=d['CODE']+d['CODE6'],whole_raw_programs=rc[GROUPS[0]]+rc[GROUPS[1]],raw_groups=rc,raw_and_printed_are_alternatives=True,software_inclusive_factor=None,historical_source_software_cost=None),acquisition=stages,addition=dict(source=s['L047'],common=d['U_B6'],application=a['L047']))
  need(x['article_only_sensitivity']['L040_conditional']==o['article_only_sensitivity']['L040_conditional'],'old30 article conditionals exact');rows.append(x)
 need({key(x)for x in rows}=={(v,n,u)for v in V for n in N for u in U},'all30 unique coordinates')
 primary=next(x for x in rows if key(x)==PRIMARY)
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic='B',title=p['title'],source_ids=IDS,applications=APPS,primary_coordinate=list(PRIMARY),coordinates=rows,coordinate_count=30,main_exact_fractions=210,article_sensitivity_fractions=60,all_exact_fractions=270,primary=primary,primary_acquisition=primary['acquisition'],inherited_conditional_fractions_preserved=150,prior_article_conditionals_preserved=30,common_pages={'U_B':16,'U_B6':10},application_pages=dict(zip(APPS.values(),p['application_pages'])),source_pages=p['source_pages'],whole_file_inventory=files,whole_file_groups=groups,archival_audit_tools=roster['archival_review_tools'],extra_stored_required_data=[],printed_program_pages={'CODE':7,'CODE6':7},required_acquisition=dict(common_components=['U_B','U_B6'],required_or_auxiliary_whole_files=[x['id']for x in files if x['mathematical_premise']],required_whole_bytes=groups[GROUPS[0]]['literal_bytes'],optional_validation_not_required=True,no_sibling_application_premise=True,conservative_complete_topic_union_not_minimal_graph=True,retained_external_cost=None),software_inclusive_factor=None,optional_validation_inclusive_factor=None,collective_conditional_factor=None,pooled_factor=None,unknown_costs=dict(N001_original_PDF=None,historical_source_software=None,external_classical_proofs=None,graphics_and_layout=None,group_libraries_and_catalogues=None,full_formalization=None),input_cells=dict(main_PDF=450,literal_authored_rendering=30,L040_article_sensitivity=30,whole_raw_files=170),source_scope={'L047':'Accepted corrected principal rank theorem and 58 dispositions. The 23 finer ancillary Table3 reports remain explicitly outside regenerated scope, although all source text stays counted. Conjecture1.1 is source-recorded and previously resolved in L044; no new question answer.','prior_five':'All prior accepted contracts, corrections, retained inputs and exclusions unchanged. N001 is complete literal authored text, not an invented PDF.'},symmetry='All executable software excluded symmetrically. Required computations remain premises. Mathematical algorithm/proof prose and whole tables remain counted.',partial_Lean_declarations=14,complete_Lean=False,new_source_credit=0,new_question_credit=0,new_formal_credit=0,prior_software_inclusive_values='Historical only; bound under prior/ but no current software scalar.',roles=p['roles'],no_source_extraction_or_scientific_replay=True)

def csvtext(headers,rows):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=headers,lineterminator='\n');w.writeheader();w.writerows(rows);return s.getvalue()
def outputs(r):
 costs=[];fracs=[];acq=[]
 for x in r['coordinates']:
  base={k:x[k]for k in ['variant','normalization','unit']}
  for k,z in x['source_costs'].items():costs.append(dict(base,document=k,role='source',cost=z))
  for k,z in x['document_costs'].items():
   if k=='L047':continue
   role='common'if k in ['U_B','U_B6']else'program_alternative'if k.startswith('CODE')else'application';costs.append(dict(base,document=k,role=role,cost=z))
  pairs=[('written',x['written'])]+[('conditional_'+k,z)for k,z in x['conditional'].items()]+[('L040_article_whole',x['article_only_sensitivity']['written']),('L040_article_conditional',x['article_only_sensitivity']['L040_conditional'])]
  fracs.extend(dict(base,comparison=k,**z)for k,z in pairs)
  acq.extend(dict(base,stage=z['stage'],source_written=z['source_written'],replacement_written=z['replacement_written'])for z in x['acquisition'])
 raw=[]
 for x in r['whole_file_inventory']:
  for n in N:
   for u in U:raw.append(dict(id=x['id'],path=x['file']['path'],role=x['role'],group=x['group'],required=x['mathematical_premise'],bytes=x['file']['bytes'],sha256=x['file']['sha256'],normalization=n,unit=u,cost=x['metrics'][n][u]))
 return {'results.json':json.dumps(r,indent=2,ensure_ascii=False)+'\n','document_costs.csv':csvtext(['variant','normalization','unit','document','role','cost'],costs),'fractions.csv':csvtext(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'],fracs),'acquisition.csv':csvtext(['variant','normalization','unit','stage','source_written','replacement_written'],acq),'raw_files.csv':csvtext(['id','path','role','group','required','bytes','sha256','normalization','unit','cost'],raw)}
if __name__=='__main__':
 p,c,roster,prior=inputs();r=derive(p,c,roster,prior)
 for name,text in outputs(r).items():(R/name).write_text(text)
 print(json.dumps({'primary':r['primary']['written'],'conditional':r['primary']['conditional'],'common':r['primary']['common_components'],'files':{g:{k:v for k,v in x.items()if k!='metrics'}for g,x in r['whole_file_groups'].items()}}))
