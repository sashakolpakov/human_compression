#!/usr/bin/env python3
"""Distinct restored-factor audit; accepted inputs only, no author imports."""
from pathlib import Path
from decimal import Decimal,localcontext
from math import gcd
from copy import deepcopy
from collections import Counter
import argparse,json,csv,hashlib,re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
PIN='dabc27842ddf944f1d24405122c7d0244ec02b1fc356cde073658d7f8a873b2c'
ADOPTION='bb494cd0129bd41b675d240a24d0358e81b8e6444a9123a1ea7172dfbb780b30'
TOPICS={'Chamber':{'sources':['L008','N016'],'common':['U_H'],'applications':{'L008':['H1'],'N016':['H2']}},'ChiralEnumeration':{'sources':['L028'],'common':['U_CE'],'applications':{'L028':['CE1']}},'Operations':{'sources':['N005','N006','N007'],'common':['U'],'applications':{'N005':['A0'],'N006':['A2','A2nine','A2HN'],'N007':['A1']}}}
VARIANTS={'raw_without_listings':'raw_untrimmed','selected_without_listings':'raw_selected','calibrated_selected_without_listings':'calibrated_selected'}
NORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace'];PRIMARY='calibrated_selected_without_listings/NFC/characters_without_whitespace'
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
 with p.open(newline='')as f:return list(csv.DictReader(f))
def fraction(a,b):
 q=gcd(a,b)
 with localcontext()as c:c.prec=45;decimal=format(Decimal(a)/Decimal(b),'.12f')
 return dict(source_cost=a,replacement_cost=b,numerator=a//q,denominator=b//q,decimal=decimal)
def expected(data,baseline):
 topics={};documents={};unchanged=0;fractions=0
 for name,scope in TOPICS.items():
  ids=scope['sources']+scope['common']+sum(scope['applications'].values(),[]);coords={}
  for v in list(VARIANTS)+(['text_only_without_listings']if name=='Operations'else[]):
   for norm in NORMS:
    for unit in UNITS:
     new={};old={}
     for ident in ids:
      key=name+'/'+ident
      if v.startswith('text_only'):
       new[ident]=data['Operations_text_only_sensitivity'][key]['metrics'][norm][unit];old[ident]=baseline[key]['text_only_sensitivity']['metrics'][norm][unit]
      else:new[ident]=data['documents'][key]['metrics'][v][norm][unit];old[ident]=baseline[key]['metrics'][VARIANTS[v]][norm][unit]
      if ident not in ['L008','L028','N006']:need(new[ident]==old[ident],'unmasked whole document unchanged');unchanged+=1
     numerator=sum(new[k]for k in scope['sources']);common=sum(new[k]for k in scope['common']);apps={s:sum(new[k]for k in scope['applications'][s])for s in scope['sources']};den=common+sum(apps.values());key='/'.join((v,norm,unit))
     coords[key]=dict(variant=v,normalization=norm,unit=unit,document_costs=new,pre_listing_document_costs=old,excluded_cost_by_document={k:old[k]-new[k]for k in ids},source_sum=numerator,common_sum=common,application_bundle_costs=apps,whole_written=den,written=fraction(numerator,den),conditional={s:fraction(new[s],apps[s])for s in scope['sources']},software_inclusive_factor=None,historical_source_software_cost=None);fractions+=1+len(apps)
     for ident in ids:documents[name+'/'+ident+'/'+key]=new[ident]
  topics[name]=dict(scope=scope,coordinate_count=len(coords),coordinates=coords,primary_coordinate=PRIMARY,primary=coords[PRIMARY])
 need(unchanged==500 and fractions==310 and len(documents)==600,'complete input cell counts')
 return topics,documents

def audit_result(d,p,data,baseline,software):
 topics,documents=expected(data,baseline)
 need(p['topics']==TOPICS and p['primary']==dict(variant='calibrated_selected_without_listings',normalization='NFC',unit='characters_without_whitespace'),'exact adopted scope and fixed coordinate')
 need(d['topics']==topics and d['document_costs']==documents,'all100 coordinate objects and310 exact fractions')
 need(d['standard_coordinates_per_topic']==30 and d['Operations_extra_text_only_coordinates']==10 and d['exact_fractions']==310 and d['document_cells']==600,'all standard and text-only sensitivities')
 need(d['whole_file_roster']==software['records']and d['whole_file_count']==len(software['records'])==46,'whole unchanged files/roles/costs')
 need(p['optional_validation_is_a_prerequisite']is False and software['optional_validation_not_precondition']is True,'optional validation not a theorem premise')
 need(all(d[k]is None for k in ['software_inclusive_factors','historical_source_software_cost','full_graphics_external_proofs_and_formalization']),'software and external unknowns never zero')
 need([d[k]for k in ['programme_recovered','programme_pending','new_source_credit','new_question_credit']]==[43,63,0,0],'scope/credits unchanged')
 need(d['no_new_extraction_or_science_replay'],'no fresh input adjudication or science replay')
 return topics,documents

def csv_audit(H,topics,docs,software):
 fractions=[];wholes=[];apps=[]
 for name,t in topics.items():
  for coord,c in t['coordinates'].items():
   fractions.append(dict(topic=name,coordinate=coord,comparison='whole',**c['written']));fractions.extend(dict(topic=name,coordinate=coord,comparison=s,**c['conditional'][s])for s in TOPICS[name]['sources'])
  p=t['primary'];wholes.append(dict(topic=name,common=p['common_sum'],application_sum=sum(p['application_bundle_costs'].values()),**p['written']));apps.extend(dict(topic=name,source=s,application_bundle='+'.join(TOPICS[name]['applications'][s]),**p['conditional'][s])for s in TOPICS[name]['sources'])
 raw=[dict(topic=r['topic'],category=r['category'],path=r['file']['path'],bytes=r['file']['bytes'],sha256=r['file']['sha256'])for r in software['records']]
 tables={'fractions.csv':fractions,'topics.csv':wholes,'applications.csv':apps,'document_costs.csv':[dict(coordinate=k,cost=v)for k,v in docs.items()],'whole_files.csv':raw}
 for name,values in tables.items():need(rows(H/name)==[{k:str(v)for k,v in x.items()}for x in values],'independent CSV '+name)
 return {k:len(v)for k,v in tables.items()}

def rectangles_svg(text):
 doc=ET.fromstring(text);out={};ns={'s':'http://www.w3.org/2000/svg'}
 for e in doc.findall('.//s:g',ns):
  name=e.attrib.get('id','')
  if not name.startswith('bar-'):continue
  path=e.findall('s:path',ns);need(len(path)==1 and name not in out,'one unique rectangle path');v=path[0].attrib['d'];need(re.sub(r'[-+\d.eE\s]','',v)=='MLLLz','literal rectangle commands');a=list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',v)));need(len(a)==8,'four points');xs=a[::2];ys=a[1::2];need(abs(ys[0]-ys[1])<1e-7 and abs(xs[1]-xs[2])<1e-7 and abs(ys[2]-ys[3])<1e-7 and abs(xs[3]-xs[0])<1e-7,'rectangular SVG shape');out[name]=(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
 return out

def rectangles_pdf(path):
 rr=PdfReader(path);need(len(rr.pages)==1,'single chart page');p=rr.pages[0];color=None;stack=[];points=[];rects=[];colors={(52,67,84),(40,110,153),(129,189,176)}
 for args,op in ContentStream(p.get_contents(),p.pdf).operations:
  if op==b'q':stack.append(color)
  elif op==b'Q':color=stack.pop()
  elif op==b'rg':color=tuple(round(float(x)*255)for x in args)
  elif op==b'm':points=[tuple(map(float,args))]
  elif op==b'l':points.append(tuple(map(float,args)))
  elif op==b're':points=[]
  elif op in (b'f',b'f*',b'B',b'B*'):
   if color in colors and len(points)==4:
    xs,ys=zip(*points);need(abs(ys[0]-ys[1])<1e-6 and abs(xs[1]-xs[2])<1e-6 and abs(ys[2]-ys[3])<1e-6 and abs(xs[3]-xs[0])<1e-6,'rectangular PDF bar');rects.append((min(xs),float(p.mediabox.height)-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
   points=[]
  elif op in (b'n',b'S'):points=[]
 need(float(p.mediabox.width)==648 and float(p.mediabox.height)==576,'actual chart canvas dimensions')
 return rects

def compare_boxes(actual,want):
 need(set(actual)==set(want),'all 24 exact bar identities')
 for k,v in want.items():need(all(abs(a-b)<3e-6 for a,b in zip(actual[k],v)),'actual zero-based bar geometry '+k)

def expected_geometry(topics):
 W,H=648,576;left=.23*W;width=.69*W;out={};pairs=[(name,s,t['primary']['conditional'][s])for name,t in topics.items()for s in TOPICS[name]['sources']]
 topmax=max(t['primary']['source_sum']for t in topics.values())*1.08;bottommax=max(f['source_cost']for _,_,f in pairs)*1.08
 def bar(key,upper,y,start,value):
  bottom,height,ymin,yrange,xmax=(.66*H,.23*H,-.6,3.2,topmax)if upper else(.13*H,.40*H,-.55,6.1,bottommax)
  out[key]=(left+width*start/xmax,H-(bottom+height*(y+.15-ymin)/yrange),width*value/xmax,height*.30/yrange)
 for i,(name,t)in enumerate(topics.items()):
  c=t['primary'];y=2-i;bar('bar-whole-source-'+name,True,y+.18,0,c['source_sum']);bar('bar-common-'+name,True,y-.18,0,c['common_sum']);start=c['common_sum']
  for source,v in c['application_bundle_costs'].items():bar('bar-bundle-'+source,True,y-.18,start,v);start+=v
 for i,(_,source,f)in enumerate(pairs):bar('bar-pair-source-'+source,False,5-i+.18,0,f['source_cost']);bar('bar-pair-app-'+source,False,5-i-.18,0,f['replacement_cost'])
 return out

def graph_audit(H,topics):
 want=expected_geometry(topics);actual=rectangles_svg((H/'costs.svg').read_text());compare_boxes(actual,want);pdf=rectangles_pdf(H/'costs.pdf');need(len(pdf)==24,'24 actual PDF bars');unused=list(pdf)
 for name,v in want.items():
  found=[i for i,r in enumerate(unused)if all(abs(a-b)<3e-6 for a,b in zip(r,v))];need(len(found)==1,'actual PDF geometry '+name);unused.pop(found[0])
 need(not unused,'no extra coloured data bar');compare_boxes(read(H/'plot_data.json')['rectangles'],want)
 text=(H/'costs.svg').read_text();need('zero-based axes' in text and 'Optional validation is not a proof premise' in text,'zero axes and actual conditions visible')
 return want

def audit(H,study=None,public=None):
 need(sha((H/'manifest.json').read_bytes())==PIN,'exact author freeze');m=read(H/'manifest.json');need(len(m['exports'])==34,'whole export packet')
 for r in m['exports']:
  p=Path(r['path']);need(not p.is_absolute()and '..'not in p.parts,'safe bound export');b=(H/p).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'bound export '+str(p))
 p=read(H/'protocol.json');need(sha((H/'inputs/adoption/manifest.json').read_bytes())==ADOPTION,'exact root-adopted input boundary')
 for r in p['bindings']:
  b=(H/r['path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'adopted input copy')
  if Path(r['path']).name!='manifest.json':
   mf=read(H/Path(r['path']).parent/'manifest.json');e=next(z for z in mf['exports']if z['path']==Path(r['path']).name);need(e['sha256']==r['sha256']and e['bytes']==r['bytes'],'copied export manifest membership')
  if study:need((study/r['source_path']).read_bytes()==b,'literal original accepted record')
 a=read(H/'inputs/adoption/adoption.json');need(a['status']=='ROOT_ADOPTED_MATCHED_LISTING_INPUTS'and a['restored_factors_permitted_after_distinct_arithmetic_review']and not a['software_inclusive_factors_permitted'],'distinct authority and limits reused')
 data=read(H/'inputs/input/author_counts.json');baseline=read(H/'inputs/input/baseline_documents.json');software=read(H/'inputs/input/unchanged_software.json');d=read(H/'results.json');topics,docs=audit_result(d,p,data,baseline,software);csvcounts=csv_audit(H,topics,docs,software);boxes=graph_audit(H,topics)
 boundcount=0
 if study and public:
  for r in software['records']:
   f=r['file'];b=({'study':study,'public':public}[f['root']]/f['path']).read_bytes();need(len(b)==f['bytes']and sha(b)==f['sha256'],'complete required/optional/driver/formal byte route');boundcount+=1
 need(Counter((r['topic'],r['category'])for r in software['records'])=={('Chamber','programs'):2,('Chamber','drivers'):3,('Chamber','formal'):3,('ChiralEnumeration','programs'):3,('ChiralEnumeration','drivers'):1,('ChiralEnumeration','formal'):1,('Operations','programs'):23,('Operations','required_drivers'):2,('Operations','drivers'):5,('Operations','formal'):3},'actual complete role inventory')
 tex=(H/'reader.tex').read_text();texts=[z.extract_text()or''for z in PdfReader(H/'reader.pdf').pages];need(len(texts)==3,'complete three-page reader')
 for phrase in ['A factor below one means that the replacement papers are longer','Optional validation is not a theorem premise','All software-inclusive factors and unavailable historical software costs remain null']:
  need(phrase in tex,'reader boundary statement')
 need('Lemma 4.5 and its entire proof' in tex and 'Harada--Norton companion' in tex and 'two required decoding drivers' in tex,'kept proof/companions/mandatory decoders visible')
 for name,t in topics.items():
  c=t['primary'];need(f"{Decimal(c['written']['decimal']):.6f}"in tex,'displayed whole fraction')
  for v in c['conditional'].values():need(f"{Decimal(v['decimal']):.6f}"in tex,'displayed conditional fraction')
  vals=[Decimal(v['written']['decimal'])for k,v in t['coordinates'].items()if not k.startswith('text_only')]
  need(f'{min(vals):.6f}'in tex and f'{max(vals):.6f}'in tex,'whole sensitivity range')
 for key,c in topics['Operations']['coordinates'].items():
  if key.startswith('text_only'):need(f"{Decimal(c['written']['decimal']):.6f}"in tex,'all10 displayed text-only sensitivities')
 controls=[]
 def primary(q):return q['topics']['Operations']['coordinates'][PRIMARY]
 cases=[('whole common free',lambda q:primary(q).update(common_sum=0)),('omit HN companion',lambda q:q['topics']['Operations']['scope']['applications']['N006'].pop()),('restore source-only code',lambda q:primary(q)['document_costs'].update(N006=56001)),('wrong reduced numerator',lambda q:primary(q)['written'].update(numerator=1)),('wrong decimal',lambda q:primary(q)['conditional']['N006'].update(decimal='1.500000000000')),('drop text-only coordinate',lambda q:q['topics']['Operations']['coordinates'].pop('text_only_without_listings/NFC/whitespace_tokens')),('alter old unheld N016',lambda q:q['topics']['Chamber']['coordinates'][PRIMARY]['conditional']['N016'].update(numerator=1)),('software factor invented',lambda q:q.update(software_inclusive_factors=1)),('source software zero',lambda q:q.update(historical_source_software_cost=0)),('graphics zero',lambda q:q.update(full_graphics_external_proofs_and_formalization=0)),('drop required decoder',lambda q:q['whole_file_roster'].pop(next(i for i,r in enumerate(q['whole_file_roster'])if r['category']=='required_drivers'))),('validation made required',lambda q:q['whole_file_roster'][1]['inherited_role_record'].update(required_mathematical_premise=True)),('alter whole data bytes',lambda q:q['whole_file_roster'][0]['file'].update(bytes=1)),('new recovery credit',lambda q:q.update(programme_recovered=46)),('chosen primary changed',lambda q:q['topics']['Chamber'].update(primary_coordinate='raw_without_listings/NFC/characters_without_whitespace'))]
 for name,change in cases:
  q=deepcopy(d);change(q)
  try:audit_result(q,p,data,baseline,software)
  except(ValueError,KeyError):controls.append(name)
  else:raise ValueError('accepted bad control '+name)
 for name,change in [('stretched bar',lambda q:q.__setitem__('bar-common-Operations',(0,0,1,1))),('missing actual app bar',lambda q:q.pop('bar-pair-app-N006'))]:
  q=deepcopy(boxes);change(q)
  try:compare_boxes(q,boxes)
  except ValueError:controls.append(name)
  else:raise ValueError('accepted graphic control')
 return dict(status='PASS_DISTINCT_MATCHED_LISTING_NUMERICAL_AUDIT',author_manifest_sha256=PIN,accepted_input_adoption_sha256=ADOPTION,topic_coordinate_counts={k:len(v['coordinates'])for k,v in topics.items()},exact_fractions=310,adopted_document_cells=600,unchanged_prior_cells=500,CSV_rows=csvcounts,total_CSV_rows=sum(csvcounts.values()),whole_files=46,whole_file_bytes_verified=boundcount,actual_SVG_rectangles=24,actual_PDF_rectangles=24,independent_controls_rejected=controls,primary_whole={k:t['primary']['written']for k,t in topics.items()},primary_conditional={s:f for t in topics.values()for s,f in t['primary']['conditional'].items()},Operations_text_only_primary=topics['Operations']['coordinates']['text_only_without_listings/NFC/characters_without_whitespace']['written'],reader_pages=3,reader_page_text_sha256=[sha(t.encode())for t in texts],software_inclusive_factors=None,source_extraction_or_science_replayed=False,imports_author_modules=False,prior_role='Reviewer authored the input masks and earlier scientific/review components. This numerical review reuses distinct input review fdafacef and root adoption bb494cd0 without re-adjudicating its own inputs; current numerical author is enumeration_volume.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');r=audit(a.packet,a.study_root,a.public_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS310 fractions/600 cells/46 files/24SVG+24PDF bars/'+str(len(r['independent_controls_rejected']))+' controls')
if __name__=='__main__':main()
