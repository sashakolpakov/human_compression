"""Independent integer/gcd arithmetic on root-accepted input cells; no author calculator."""
import csv,json,math
from decimal import Decimal,localcontext
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012','L121','L003']
PAIRS={s:'A'+str(i)for i,s in enumerate(SOURCES,1)}
COMMON=['U','U_HEX','U_STRUCT']
BUNDLES={a:([a]if a!='A10'else['A10_MAIN','A10_STRUCT','A10_CORR','A10_768'])for a in PAIRS.values()}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];NORMS=['NFC','NFKC']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
PRIMARY='calibrated_selected/NFC/characters_without_whitespace'
CLASS_COUNTS={'required_program':28,'required_data':71,'operational':17,'optional_validation':5,'partial_formal':16,'output_receipt':66}
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def f(a,b):
 need(type(a)is type(b)is int and a>0 and b>0,'positive integral complete costs');g=math.gcd(a,b)
 with localcontext()as c:
  c.prec=80;value=Decimal(a)/Decimal(b);decimal=format(value,'.12f');six=format(value,'.6f')
 return dict(source_cost=a,replacement_cost=b,numerator=a//g,denominator=b//g,decimal=decimal,display_six=six)
def without_display(x):return{k:v for k,v in x.items()if k!='display_six'}
def derive(packet):
 c=read(packet/'inputs/input/author_counts.json');ip=read(packet/'inputs/input/precount/policy.json');inv=read(packet/'inputs/input/precount/raw_inventory.json');old=read(packet/'prior/results.json')
 need(ip['source_ids']==SOURCES and ip['common_documents']==COMMON and ip['application_documents']==BUNDLES,'accepted complete10source scope')
 docs=c['documents'];coordinates={}
 for v in VARIANTS:
  for n in NORMS:
   for u in UNITS:
    key='/'.join([v,n,u]);d={k:x['metrics'][v][n][u]for k,x in docs.items()};app={k:sum(d[t]for t in ts)for k,ts in BUNDLES.items()};common={k:d[k]for k in COMMON};ss=sum(d[s]for s in SOURCES);uu=sum(common.values());aa=sum(app.values())
    coordinates[key]=dict(document_costs=d,common_costs=common,application_costs=app,source_sum=ss,whole_common=uu,application_sum=aa,whole_written=uu+aa,written=f(ss,uu+aa),conditional={s:f(d[s],app[PAIRS[s]])for s in SOURCES})
 raw={};groups={k:dict(files=0,literal_bytes=0,metrics={n:{u:0 for u in UNITS}for n in NORMS})for k in CLASS_COUNTS};required=[]
 for item in inv['contents']:
  k=item['id'];r=c['raw_files_measured'][k];need(all(item[x]==r[x]for x in ['sha256','bytes','occurrence_ids','roles','coarse_roles','accounting_class','mathematical_premise','inherited_A9_raw_id']),'accepted raw content metadata')
  raw[k]=dict(id=k,**r);group=groups[r['accounting_class']];group['files']+=1;group['literal_bytes']+=r['bytes']
  for n in NORMS:
   for u in UNITS:group['metrics'][n][u]+=r['metrics'][n][u]
  if r['mathematical_premise']:required.append(k)
 need({k:r['files']for k,r in groups.items()}==CLASS_COUNTS,'six disjoint accounting classes');need(len(required)==99 and len(raw)==203 and sum(len(r['occurrence_ids'])for r in raw.values())==253,'complete whole closure')
 p=coordinates[PRIMARY];ss=0;rr=p['whole_common'];stages=[dict(stage=0,acquired='All three common manuscripts',source_written=0,replacement_written=rr,required_program_data_and_external_premises_separate=True)]
 for i,s in enumerate(SOURCES,1):
  ss+=p['document_costs'][s];rr+=p['application_costs'][PAIRS[s]];stages.append(dict(stage=i,acquired=PAIRS[s]+' for '+s,source_written=ss,replacement_written=rr,required_program_data_and_external_premises_separate=True))
 return dict(coordinates=coordinates,primary=p,groups=groups,raw=raw,required=required,stages=stages,source_pages=sum(docs[s]['pages']for s in SOURCES),common_pages=sum(docs[k]['pages']for k in COMMON),application_pages={a:sum(docs[k]['pages']for k in ks)for a,ks in BUNDLES.items()},old=old,unknown_costs=ip['unknown_costs'])
def verify_result(r,o):
 need(r['source_ids']==SOURCES and r['source_count']==10 and r['applications']==PAIRS and r['application_documents']==BUNDLES and r['common_documents']==COMMON,'whole10source route')
 need(r['source_pages']==o['source_pages']==152 and r['whole_common_pages']==o['common_pages']==41 and r['application_pages']==o['application_pages']and sum(r['application_pages'].values())==63,'whole native page boundary')
 need(r['old_partial_printed_appendix_pages']==dict(CODE_A=21,CODE_AFFINE=8,CODE_DIAGRAM=1),'partial historical appendices only')
 need(r['primary_coordinate']==PRIMARY and r['coordinate_count']==30 and r['exact_fraction_count']==330 and r['inherited_conditional_fractions_preserved']==240,'fixed policy extent')
 need(set(r['coordinates'])==set(o['coordinates']),'30 coordinates')
 count=preserved=0
 for key,e in o['coordinates'].items():
  v,n,u=key.split('/');a=r['coordinates'][key];old=o['old']['coordinates'][key]
  need((a['variant'],a['normalization'],a['unit'])==(v,n,u),'coordinate labels')
  for field in ['document_costs','common_costs','application_costs','source_sum','whole_common','application_sum','whole_written']:need(a[field]==e[field],'complete cost '+field)
  need(a['written']==without_display(e['written']),'whole exact gcd/fraction/decimal');count+=1
  need(set(a['conditional'])==set(SOURCES),'all10 conditionals')
  for s in SOURCES:
   need(a['conditional'][s]==without_display(e['conditional'][s]),'conditional exact gcd/fraction/decimal '+s);count+=1
   if s in SOURCES[:8]:need(a['conditional'][s]==old['conditional'][s],'all240 old conditional records');preserved+=s in SOURCES[:8]
  need(a['prior_whole_written']==old['written']and a['prior_L121_conditional']==old['conditional']['L121'],'historical fractions exact')
  need(a['change']==dict(extra_source=e['document_costs']['L003'],extra_common=e['whole_common']-old['whole_common'],previous_L121_application=old['document_costs']['A9'],current_L121_application=e['application_costs']['A9'],L003_application=e['application_costs']['A10']),'complete before-after accounting')
  for k,value in old['document_costs'].items():
   if k!='A9':need(e['document_costs'][k]==value,'unchanged21 PDF coordinates')
  sw=a['separate_software'];need(sw==dict(old_partial_printed_appendices={k:e['document_costs'][k]for k in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']},complete_enlarged_printed_cost=None,raw_group_costs={k:g['metrics'][n][u]for k,g in o['groups'].items()},software_inclusive_factor=None,historical_source_software_cost=None),'separate complete inventory, no scalar')
 need(r['primary']==r['coordinates'][PRIMARY],'primary alias is full matching record')
 need(r['whole_file_inventory']==list(o['raw'].values())and r['whole_file_group_costs']==o['groups'],'all203 whole contents and all60 class metric sums')
 need(r['primary_acquisition']==o['stages'],'all11 complete cumulative stages')
 for name in ['complete_enlarged_printed_program_representation','software_inclusive_factors','optional_validation_inclusive_factors','historical_source_software_cost','full_formalization_cost']:need(r[name]is None,'unknown '+name)
 need(r['unknown_costs']==o['unknown_costs']and all(v is None for v in r['unknown_costs'].values()),'external and graphics unknown')
 need(r['cross_topic_discount']is False and r['no_extraction']and r['no_scientific_or_formal_replay'],'no hidden discount/re-extraction')
 need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no new credit from arithmetic')
 need((count,preserved)==(330,240),'exact fraction accounting')
 return count,preserved

def verify_csvs(packet,o):
 expected={};fr=[];doc=[];raw=[]
 for key,e in o['coordinates'].items():
  for comp,fraction in [('written',e['written'])]+list(e['conditional'].items()):fr.append(dict(coordinate=key,comparison=comp,**without_display(fraction)))
  for k,v in e['document_costs'].items():doc.append(dict(coordinate=key,document=k,cost=v))
 for k,r in o['raw'].items():
  for n in NORMS:
   for u in UNITS:raw.append(dict(id=k,accounting_class=r['accounting_class'],bytes=r['bytes'],sha256=r['sha256'],normalization=n,unit=u,cost=r['metrics'][n][u]))
 expected={'fractions.csv':fr,'document_costs.csv':doc,'whole_files.csv':raw,'acquisition.csv':o['stages']}
 for name,rows in expected.items():
  with(packet/name).open(newline='')as f:actual=list(csv.DictReader(f))
  want=[{k:str(v)for k,v in r.items()}for r in rows];need(actual==want,'all literal CSV cells/order '+name)
 return {k:len(v)for k,v in expected.items()}
