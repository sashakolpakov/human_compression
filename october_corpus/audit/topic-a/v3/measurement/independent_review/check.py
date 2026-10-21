#!/usr/bin/env python3
"""Independent accepted-vector arithmetic and actual SVG/PDF geometry. No author imports."""
from pathlib import Path
from math import gcd
from decimal import Decimal,localcontext
from collections import Counter
from copy import deepcopy
import argparse,csv,hashlib,json,re,unicodedata,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
PIN='cc2211a4fb04f7119abadce8969926043e046056b18961311ef198238ed12f70'
INPUT='321f406f81f2ffe5436785c7e23cf328c301faed3aa37a077b0693d53124f51d'
ADOPTION='6163f2a7928a2098373a6e010d3705295553d80b2f5e473084eca88ead1097ba'
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012'];APPS={s:'A'+str(i+1) for i,s in enumerate(SOURCES)}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];NORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace'];PRIMARY='calibrated_selected/NFC/characters_without_whitespace';CODE=['CODE_A','CODE_AFFINE','CODE_DIAGRAM'];ROLES={'required_program_or_data':11,'inherited_auxiliary':3,'current_operational_driver':2,'partial_formal_evidence':14}
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def fraction(a,b):
 g=gcd(a,b)
 with localcontext() as c:c.prec=45;decimal=format(Decimal(a)/Decimal(b),'.12f')
 return dict(source_cost=a,replacement_cost=b,numerator=a//g,denominator=b//g,decimal=decimal)
def whole_metrics(text,norm):
 s=unicodedata.normalize(norm,text);c=' '.join(s.split());return dict(whitespace_tokens=len(s.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',s)),characters_without_whitespace=sum(not x.isspace() for x in s),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))
def expected(data,inventory):
 need(set(data['documents'])==set(SOURCES+['U']+list(APPS.values())+CODE),'All20 complete documents')
 need([x['id'] for x in inventory]==list(data['raw_files_measured']),'Exact ordered30file inventory')
 items=[]
 for x in inventory:
  measured=data['raw_files_measured'][x['id']];need(x['file']==measured['file'] and x['role']==measured['role'],'Accepted raw role and identity');items.append(dict(x,metrics=measured['metrics']))
 need(Counter(x['role'] for x in items)==ROLES,'All11required/3aux/2driver/14Lean')
 groups={}
 for role in ROLES:
  rs=[x for x in items if x['role']==role];groups[role]=dict(files=len(rs),literal_bytes=sum(x['file']['bytes'] for x in rs),metrics={n:{u:sum(x['metrics'][n][u] for x in rs) for u in UNITS} for n in NORMS})
 out={}
 for v in VARIANTS:
  for n in NORMS:
   for u in UNITS:
    costs={key:x['metrics'][v][n][u] for key,x in data['documents'].items()};source=sum(costs[s] for s in SOURCES);apps=sum(costs[a] for a in APPS.values());total=costs['U']+apps
    out['/'.join([v,n,u])]=dict(variant=v,normalization=n,unit=u,document_costs=costs,source_sum=source,whole_common=costs['U'],application_sum=apps,whole_written=total,written=fraction(source,total),conditional={s:fraction(costs[s],costs[APPS[s]]) for s in SOURCES},separate_software=dict(printed_appendices={k:costs[k] for k in CODE},printed_sum=sum(costs[k] for k in CODE),raw_group_costs={k:x['metrics'][n][u] for k,x in groups.items()},software_inclusive_factor=None,historical_source_software_cost=None))
 c=out[PRIMARY]['document_costs'];s=0;t=c['U'];acq=[dict(stage=0,acquired='whole U',source_written=0,replacement_written=t,required_program_data_and_external_premises_separate=True)]
 for i,k in enumerate(SOURCES,1):
  s+=c[k];t+=c[APPS[k]];acq.append(dict(stage=i,acquired=APPS[k]+' for '+k,source_written=s,replacement_written=t,required_program_data_and_external_premises_separate=True))
 return out,items,groups,acq

def audit_result(r,data,inventory,p,policy):
 ex,items,groups,acq=expected(data,inventory)
 need(r['coordinates']==ex,'All270fractions/600documentcells/complete software alternative rows')
 need(r['primary_coordinate']==PRIMARY and r['primary']==ex[PRIMARY],'Fixed calibrated primary')
 need(r['source_ids']==SOURCES and r['applications']==APPS and p['source_order']==SOURCES and p['applications']==APPS and policy['source_to_application']==APPS,'Exact original/application routing')
 need(r['whole_file_inventory']==items and r['whole_file_group_costs']==groups,'All whole-file identities/roles/byte costs/metrics')
 need(r['primary_acquisition']==acq,'Full U before all eight full applications')
 need(policy['common_documents']==['U'] and policy['application_documents']==list(APPS.values()) and policy['required_complete_files']==11 and policy['programs_are_alternate_representations'],'Whole common and computational premise boundary')
 need(r['source_count']==8 and r['source_pages']==p['source_pages']==sum(data['documents'][s]['pages'] for s in SOURCES)==119,'Complete119sourcepages')
 need(r['whole_common_pages']==p['whole_common_pages']==data['documents']['U']['pages']==23,'Whole23pagecommon')
 need(r['application_pages']=={s:data['documents'][a]['pages'] for s,a in APPS.items()} and sum(r['application_pages'].values())==p['application_pages']==45,'All45applicationpages')
 need(r['printed_appendix_pages']=={k:data['documents'][k]['pages'] for k in CODE}==dict(CODE_A=21,CODE_AFFINE=8,CODE_DIAGRAM=1) and p['code_pages']==30,'Full three appendices')
 need(r['coordinate_count']==30 and r['exact_fraction_count']==270,'Full metric sensitivities')
 for name in ['software_inclusive_factors','optional_validation_inclusive_factors','historical_source_software_cost']:need(r[name] is None and p[name] is None,'Unknown historical software not zero or one-sided factor')
 need(r['full_formalization_cost'] is None and r['unknown_costs']==p['unknown_costs']==policy['unknown_costs'] and all(x is None for x in r['unknown_costs'].values()),'Retained proofs/graphics/software/formal costs unknown')
 need(not r['cross_topic_discount'] and not p['cross_topic_discount'] and r['no_extraction'] and r['no_scientific_or_formal_replay'],'No cross-topic reduction or proof/source rerun')
 need(all(r[k]==p[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'No new credit')
 need(p['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace') and p['required_files']==11 and p['raw_file_count']==30,'Fixed source-primary choice and all raw files')
 need(p['conditional_formula']=='source/local full application after acquiring wholeU and all actual required computational/data/retained premises','Actual full conditional acquisition')
 return ex,items,groups,acq

def csv_audit(packet,ex,items,acq):
 wanted={};fs=[];ds=[];ws=[]
 for key,c in ex.items():
  fs.append(dict(coordinate=key,comparison='written',**c['written']));fs.extend(dict(coordinate=key,comparison=s,**c['conditional'][s]) for s in SOURCES);ds.extend(dict(coordinate=key,document=k,cost=v) for k,v in c['document_costs'].items())
 for x in items:
  for n in NORMS:
   for u in UNITS:ws.append(dict(id=x['id'],path=x['file']['path'],role=x['role'],bytes=x['file']['bytes'],sha256=x['file']['sha256'],normalization=n,unit=u,cost=x['metrics'][n][u]))
 wanted.update({'fractions.csv':fs,'document_costs.csv':ds,'whole_files.csv':ws,'acquisition.csv':acq})
 for name,rows in wanted.items():
  with (packet/name).open(newline='') as f:got=list(csv.DictReader(f))
  need(got==[{k:str(v) for k,v in row.items()} for row in rows],'Every CSV record '+name)
 return {k:len(v) for k,v in wanted.items()}

def expected_rectangles(primary):
 # Independent affine coordinate conversion from the displayed axis contract.
 # Deliberately no author geometry or plotting helper, no expected metadata.
 d=primary['document_costs'];W=H=648.;left=.21*W;width=.70*W;out={}
 def box(key,panel,y,offset,cost):
  if panel=='top':bottom=.75*H;height=.14*H;ymin=-.55;yrange=2.1;maximum=max(primary['source_sum'],primary['whole_written'])*1.12
  else:bottom=.10*H;height=.53*H;ymin=-.6;yrange=9.2;maximum=max(d['U'],*[d[s] for s in SOURCES],*[d[a] for a in APPS.values()])*1.12
  out[key]=(left+width*offset/maximum,H-bottom-height*(y+.18-ymin)/yrange,width*cost/maximum,height*.36/yrange)
 box('bar-whole-source','top',1,0,primary['source_sum']);offset=0
 for k in ['U']+list(APPS.values()):box('bar-whole-'+k,'top',0,offset,d[k]);offset+=d[k]
 box('bar-acquire-U','bottom',8,0,d['U'])
 for i,s in enumerate(SOURCES):box('bar-source-'+s,'bottom',7-i+.2,0,d[s]);box('bar-application-'+s,'bottom',7-i-.2,0,d[APPS[s]])
 return out

def svg_boxes(text):
 doc=ET.fromstring(text);out={};ns={'s':'http://www.w3.org/2000/svg'}
 for e in doc.findall('.//s:g',ns):
  k=e.attrib.get('id','')
  if not k.startswith('bar-'):continue
  ps=e.findall('s:path',ns);need(len(ps)==1 and k not in out,'One unique actual bar');s=ps[0].attrib['d'];need(re.sub(r'[-+\d.eE\s]','',s)=='MLLLz','Four-point data rectangle');v=list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)));need(len(v)==8,'Rectangle coordinates');xs=v[::2];ys=v[1::2];need(abs(xs[1]-xs[2])<1e-7 and abs(xs[3]-xs[0])<1e-7 and abs(ys[0]-ys[1])<1e-7 and abs(ys[2]-ys[3])<1e-7,'Axis-aligned actual SVG rectangle');out[k]=(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
 return out

def pdf_boxes(path):
 rr=PdfReader(path);need(len(rr.pages)==1,'One chart page');p=rr.pages[0];need(float(p.mediabox.width)==648 and float(p.mediabox.height)==648,'Actual9inch square chart');color=None;stack=[];points=[];out=[];colors={(52,67,84),(40,110,153),(129,189,176)}
 for args,op in ContentStream(p.get_contents(),p.pdf).operations:
  if op==b'q':stack.append(color)
  elif op==b'Q':color=stack.pop()
  elif op==b'rg':color=tuple(round(float(x)*255) for x in args)
  elif op==b'm':points=[tuple(map(float,args))]
  elif op==b'l':points.append(tuple(map(float,args)))
  elif op==b're':points=[]
  elif op in [b'f',b'f*',b'B',b'B*']:
   if color in colors and len(points)==4:
    xs,ys=zip(*points);need(abs(xs[1]-xs[2])<1e-6 and abs(xs[3]-xs[0])<1e-6 and abs(ys[0]-ys[1])<1e-6 and abs(ys[2]-ys[3])<1e-6,'Actual PDF rectangle');out.append((min(xs),648-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
   points=[]
  elif op in [b'n',b'S']:points=[]
 return out

def checkboxes(got,want):
 need(set(got)==set(want),'All27 individual rectangle identities')
 for key,v in want.items():need(all(abs(a-b)<3e-6 for a,b in zip(got[key],v)),'Actual scale/stacking/baseline rectangle '+key)

def graph_audit(packet,primary):
 want=expected_rectangles(primary);s=(packet/'costs.svg').read_text();actual=svg_boxes(s);checkboxes(actual,want);pdf=pdf_boxes(packet/'costs.pdf');need(len(pdf)==27,'All27 actual PDF bars');left=list(pdf)
 for key,v in want.items():
  matches=[i for i,r in enumerate(left) if all(abs(a-b)<3e-6 for a,b in zip(r,v))];need(len(matches)==1,'PDF independent expected dimensions '+key);left.pop(matches[0])
 need(not left,'No extra colored data');g=read(packet/'plot_data.json');checkboxes(g['expected_rectangles'],want);need(g['bars']==27 and g['axis_origin_zero'] and g['software_costs_separate'] and not g['ratio_bars'],'Graph metadata reflects manuscript bars')
 for text in ['all axes start at zero','Conditional applications assume whole U','presentation data and retained mathematical premises already acquired.','Calibrated selected NFC']:need(text in s,'Visible chart acquisition/unit labels')
 return actual,want

def check(packet,study,public):
 need(sha((packet/'manifest.json').read_bytes())==PIN,'Exact numerical author freeze');m=read(packet/'manifest.json');need(len(m['exports'])==55,'55export scope')
 for e in m['exports']:
  f=Path(e['path']);need(not f.is_absolute() and '..' not in f.parts,'Safe export');b=(packet/f).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'Author export '+str(f))
 p=read(packet/'protocol.json');policy=read(packet/'inputs/input/policy.json');data=read(packet/'inputs/input/author_counts.json');inventory=read(packet/'inputs/input/raw_inventory.json');r=read(packet/'results.json')
 need(sha((packet/'inputs/input/manifest.json').read_bytes())==INPUT and sha((packet/'inputs/input_adoption/manifest.json').read_bytes())==ADOPTION,'Exact adopted inputs')
 bound=0
 for x in p['input_bindings']:
  raw=(packet/x['path']).read_bytes();need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'Input binding');folder=(packet/x['path']).parent
  for e in read(folder/'manifest.json')['exports']:
   b=(folder/e['path']).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'Full adopted input/review/adoption export');bound+=1
  if study:need(raw==(study/x['study_path']).read_bytes(),'Unchanged accepted input authority')
 adopt=read(packet/'inputs/input_adoption/adoption.json');need(adopt['status']=='ROOT_ACCEPTED_UNIFIED_A_MEASUREMENT_INPUTS' and adopt['numerical_evaluation_authorized'] and adopt['software_inclusive_factor'] is None,'Root count acceptance authorizes manuscript arithmetic')
 need(p['primary']['variant']==policy['primary']['variant']=='calibrated_selected' and p['primary']['unit']==policy['primary']['metric'] and p['primary']['normalization']==policy['primary']['normalization']=='NFC','Not chosen favorable primary')
 ex,items,groups,acq=audit_result(r,data,inventory,p,policy);csvs=csv_audit(packet,ex,items,acq);actual,want=graph_audit(packet,ex[PRIMARY])
 rawcells=0;rawhashes=0
 if study:
  for item in items:
   f=item['file'];root=study if f['root']=='study' else public;need(root is not None,'Explicit public root for rawfile');b=(root/f['path']).read_bytes();need(len(b)==f['bytes'] and sha(b)==f['sha256'],'Whole actual rawfile '+f['path']);rawhashes+=1
   for norm in NORMS:
    need(whole_metrics(b.decode('utf8'),norm)==item['metrics'][norm],'Independent raw metrics '+item['id']);rawcells+=5
 tex=(packet/'reader.tex').read_text();texts=[page.extract_text() or '' for page in PdfReader(packet/'reader.pdf').pages];need(len(texts)==3,'Full3page reader');alltext=' '.join('\n'.join(texts).split())
 for token in ['246,570','176,716','66,140','110576','1.395290','102 source dispositions','Historical source software is unknown','unextracted image labels','9, 10, 12 and 22','whole common paper','never added to the raw files']:
  need(token in alltext,'Reader full-cost/scope/unknown wording '+token)
 for c in ex.values():need(f"{Decimal(c['written']['decimal']):.6f}" in tex,'All30 displayed sensitivity values')
 for s in SOURCES:need(f"{Decimal(ex[PRIMARY]['conditional'][s]['decimal']):.6f}" in tex,'Every displayed conditional')
 need('after acquiring the entire common theory' in tex and 'actual required computations, presentation data and retained mathematical results' in tex and 'Executable programs are excluded from both sides' in tex and 'not full formalizations' in tex,'Conditional/symmetric/partial formal reader scope')
 controls=[]
 def reject(name,change):
  q=deepcopy(r);change(q)
  try:audit_result(q,data,inventory,p,policy)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('Accepted result mutation '+name)
 reject('free common paper',lambda q:q['coordinates'][PRIMARY].update(whole_common=0))
 reject('omit affine application',lambda q:q['coordinates'][PRIMARY].update(whole_written=q['coordinates'][PRIMARY]['whole_written']-q['coordinates'][PRIMARY]['document_costs']['A8']))
 reject('change source pairing',lambda q:q['applications'].update(L012='A7'))
 reject('change source count',lambda q:q['coordinates'][PRIMARY]['document_costs'].update(L012=1))
 reject('alter exact numerator',lambda q:q['coordinates'][PRIMARY]['written'].update(numerator=1))
 reject('inflate conditional decimal',lambda q:q['coordinates'][PRIMARY]['conditional']['N009'].update(decimal='9.000000000000'))
 reject('drop required presentation data',lambda q:q['whole_file_inventory'].pop(1))
 reject('mathematical driver treated auxiliary',lambda q:q['whole_file_inventory'][3].update(role='inherited_auxiliary'))
 reject('appendices double charged',lambda q:q['coordinates'][PRIMARY].update(whole_written=q['coordinates'][PRIMARY]['whole_written']+q['coordinates'][PRIMARY]['separate_software']['printed_sum']))
 reject('invent software factor',lambda q:q.update(software_inclusive_factors=1.2))
 reject('invent validation factor',lambda q:q.update(optional_validation_inclusive_factors=1.2))
 reject('unknown source software zero',lambda q:q.update(historical_source_software_cost=0))
 reject('unknown image cost zero',lambda q:q['unknown_costs'].update(unextracted_visible_image_labels=0))
 reject('free initial common acquisition',lambda q:q['primary_acquisition'][0].update(replacement_written=0))
 reject('favorable primary substituted',lambda q:q.update(primary_coordinate='raw_untrimmed/NFC/whitespace_tokens'))
 reject('add question credit',lambda q:q.update(new_question_credit=1))
 reject('omit sensitivity',lambda q:q['coordinates'].pop(next(iter(q['coordinates']))))
 for name,change in [('stretched actual common bar',lambda x:x.__setitem__('bar-acquire-U',(x['bar-acquire-U'][0],x['bar-acquire-U'][1],x['bar-acquire-U'][2]*1.1,x['bar-acquire-U'][3]))),('misstacked last application',lambda x:x.__setitem__('bar-whole-A8',(x['bar-whole-A8'][0]+10,*x['bar-whole-A8'][1:]))),('missing source bar',lambda x:x.pop('bar-source-L012'))]:
  q=deepcopy(actual);change(q)
  try:checkboxes(q,want)
  except ValueError:controls.append(name)
  else:raise ValueError('Accepted actual geometry mutation')
 # Mutate actual vector-path bytes while retaining a valid rectangle, then parse again.
 doc=ET.fromstring((packet/'costs.svg').read_text());ns={'s':'http://www.w3.org/2000/svg'}
 e=next(e for e in doc.findall('.//s:g',ns) if e.attrib.get('id')=='bar-acquire-U');path=e.find('s:path',ns)
 v=list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path.attrib['d'])));v[2]+=9;v[4]+=9
 path.attrib['d']='M %s %s L %s %s L %s %s L %s %s z'%tuple(v)
 try:checkboxes(svg_boxes(ET.tostring(doc,encoding='unicode')),want)
 except ValueError:controls.append('actual SVG path width altered')
 else:raise ValueError('Altered actual SVG path accepted')
 return dict(status='PASS_DISTINCT_NUMERICAL_ARITHMETIC_AND_GEOMETRY',author_manifest_sha256=PIN,input_manifest_sha256=INPUT,input_root_adoption_sha256=ADOPTION,adopted_exports_verified=bound,coordinates=30,exact_fractions=270,complete_document_cells=600,whole_file_metric_cells=300,actual_raw_file_bindings=rawhashes,independently_recounted_raw_cells=rawcells,CSV_rows=csvs,total_CSV_rows=sum(csvs.values()),actual_SVG_bars=27,actual_PDF_bars=27,reader_pages=3,reader_page_text_sha256=[sha(t.encode()) for t in texts],primary=ex[PRIMARY]['written'],conditionals=ex[PRIMARY]['conditional'],whole_file_roles=ROLES,unknown_costs=r['unknown_costs'],software_inclusive_factors=None,controls_rejected=controls,imports_numerical_author_modules=False,source_font_GAP_Lean_rerun=False,reviewer_prior_roles='Earlier affine scientific author and distinct unified input reviewer; current numerical author is enumeration_volume. Distinct unified science/root acceptance reused, not re-adjudicated.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output');r=check(a.packet,a.study_root,a.public_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
