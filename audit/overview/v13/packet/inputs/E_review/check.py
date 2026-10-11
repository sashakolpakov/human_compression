#!/usr/bin/env python3
"""Independent E arithmetic and vector geometry; no numerical-author imports."""
from pathlib import Path
from decimal import Decimal,localcontext
from math import gcd
from copy import deepcopy
from collections import Counter
import argparse,csv,hashlib,json,re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
PIN='b5eba088d711072b33f830dc3b06ad833292d523fb08191b1ced4e408a9b44e3'
ADOPTION='99854aae4631351db39d6b248a811e09337b48d5c052628f04e2f89417ae4fef'
SOURCES=['L079','L083','L021','L056','L043'];APPS={'L079':'A2','L083':'A1','L021':'A3','L056':'A4','L043':'A5'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];NORMS=['NFC','NFKC'];UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace'];PRIMARY='raw_untrimmed/NFC/characters_without_whitespace'
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
def expected(data,policy):
 groups={k:[]for k in ['required_programs','required_data','optional_validation','operational_drivers','partial_formal']};allrows=[]
 roles={r['path']:r['role']for r in policy['programs_and_data']}
 for category,files in data['raw_files'].items():
  for path,row in files.items():
   if category=='programs_and_data':
    role=roles[path];group={'required finite proof':'required_programs','required certificate data':'required_data','validation only':'optional_validation'}[role]
   elif category=='operational_drivers':group='operational_drivers';role='operational'
   elif category=='formal_files':group='partial_formal';role='partial formal evidence'
   else:raise ValueError('unknown raw collection')
   item=dict(path=path,role=role,group=group,**row);groups[group].append(item);allrows.append(item)
 need({k:len(v)for k,v in groups.items()}==dict(required_programs=6,required_data=1,optional_validation=6,operational_drivers=5,partial_formal=7),'whole computational/formal role boundary')
 summary={k:dict(files=len(v),literal_bytes=sum(r['bytes']for r in v),metrics={n:{u:sum(r['metrics'][n][u]for r in v)for u in UNITS}for n in NORMS})for k,v in groups.items()}
 coordinates={}
 for v in VARIANTS:
  for n in NORMS:
   for u in UNITS:
    c={k:row['metrics'][v][n][u]for k,row in data['documents'].items()};src=sum(c[k]for k in SOURCES);app=sum(c[k]for k in APPS.values());den=c['U']+app
    coordinates['/'.join((v,n,u))]=dict(variant=v,normalization=n,unit=u,document_costs=c,source_sum=src,whole_common=c['U'],application_sum=app,whole_written=den,written=fraction(src,den),conditional={k:fraction(c[k],c[APPS[k]])for k in SOURCES},separate_software=dict(required_printed_with_data=c['REQUIRED'],optional_printed=c['VALIDATION'],raw={k:row['metrics'][n][u]for k,row in summary.items()},software_inclusive_factor=None,historical_source_software_cost=None))
 c=coordinates[PRIMARY];s=0;t=c['whole_common'];acq=[dict(stage=0,acquired='whole U',source_written=0,replacement_written=t,required_software_and_external_preconditions_separate=True)]
 for i,k in enumerate(SOURCES,1):
  s+=c['document_costs'][k];t+=c['document_costs'][APPS[k]];acq.append(dict(stage=i,acquired=APPS[k]+' for '+k,source_written=s,replacement_written=t,required_software_and_external_preconditions_separate=True))
 return coordinates,summary,allrows,acq

def audit_result(result,data,policy,protocol):
 ex,groups,inventory,acq=expected(data,policy)
 need(result['coordinates']==ex,'all thirty complete coordinate objects, exact fractions and separate inventories')
 need(result['primary_coordinate']==PRIMARY and result['primary']==ex[PRIMARY],'fixed raw primary')
 need(result['whole_file_inventory']==inventory and result['whole_file_group_costs']==groups,'whole file costs, bytes, roles and metrics')
 need(result['primary_acquisition']==acq,'complete cumulative common/application acquisition')
 need(result['source_ids']==SOURCES and result['applications']==APPS,'actual source/application pairing')
 need(protocol['source_order']==SOURCES and protocol['applications']==APPS,'protocol pairing')
 need(policy['applications']=={k:[v]for k,v in APPS.items()},'routing to accepted inputs')
 need(protocol['common']==['U']and protocol['all_written']==['U','A1','A2','A3','A4','A5']and policy['written_documents']==protocol['all_written'],'whole common/apps paid')
 need(result['source_pages']==sum(data['documents'][k]['pages']for k in SOURCES)==67 and result['whole_common_pages']==20,'complete source/common pages')
 need(result['application_pages']=={k:data['documents'][a]['pages']for k,a in APPS.items()}==dict(L079=1,L083=2,L021=5,L056=2,L043=4),'full application pages')
 need(result['physical_appendices']==dict(required_with_data=20,optional=7),'whole appendices')
 need(result['original_count']==5 and result['coordinate_count']==30 and result['exact_fraction_count']==180,'count scope')
 need(result['software_inclusive_factors']is None and result['historical_source_software_cost']is None,'no software-inclusive factor/unknown source zero')
 need(all(x is None for x in result['unknown_costs'].values()) and result['unknown_costs']==protocol['unknown_costs'],'external unknowns null')
 need(protocol['conditional_optional_validation_required']is False and protocol['programme_inventory']==dict(required_programs=6,required_data_files=1,optional_programs=6,operational_drivers=5,formal_files=7,partial_declarations=42,new_partial_declarations=9,printed_required_includes_JSON=True,printed_and_raw_alternatives_never_added=True),'actual programme and formal scope')
 need(result['source_registration_or_question_credit']==0 and result['no_source_extraction'] and result['no_science_replay'],'no new credit/rerun')
 return ex,groups,inventory,acq

def csv_audit(H,ex,inventory,acq):
 def equality(name,expected_rows):
  observed=rows(H/name);wanted=[{k:str(v)for k,v in row.items()}for row in expected_rows];need(observed==wanted,'exact CSV '+name);return len(observed)
 fs=[];ds=[]
 for k,c in ex.items():
  fs.append(dict(coordinate=k,comparison='written',**c['written']))
  fs.extend(dict(coordinate=k,comparison=s,**c['conditional'][s])for s in SOURCES)
  ds.extend(dict(coordinate=k,document=s,cost=value)for s,value in c['document_costs'].items())
 whole=[]
 for row in inventory:
  for n in NORMS:
   for u in UNITS:whole.append(dict(path=row['path'],role=row['role'],group=row['group'],bytes=row['bytes'],sha256=row['sha256'],normalization=n,unit=u,cost=row['metrics'][n][u]))
 return {n:equality(n,v)for n,v in [('fractions.csv',fs),('document_costs.csv',ds),('whole_files.csv',whole),('acquisition.csv',acq)]}

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
 need(float(p.mediabox.width)==648 and float(p.mediabox.height)==540,'actual chart canvas dimensions')
 return rects

def expected_geometry(c):
 # Independently computed from the declared 9x7.5-inch figure and explicit
 # axis rectangles; no author transform function or expected-rectangle data.
 W,H=648,540;left=W/5;aw=W*.72;out={};cost=c['document_costs']
 def box(name,axis,y,offset,value):
  if axis=='top':bottom=H*.71;ah=H*.17;ymin=-.55;yrange=2.1;maxx=c['source_sum']*1.12
  else:bottom=H*.11;ah=H*.48;ymin=-.6;yrange=6.2;maxx=max(cost['U'],*[cost[k]for k in SOURCES])*1.12
  out[name]=(left+aw*offset/maxx,H-(bottom+ah*(y+.18-ymin)/yrange),aw*value/maxx,ah*.36/yrange)
 box('bar-whole-source','top',1,0,c['source_sum']);offset=0
 for k in ['U']+[APPS[s]for s in SOURCES]:box('bar-whole-'+k,'top',0,offset,cost[k]);offset+=cost[k]
 box('bar-acquire-U','bottom',5,0,cost['U'])
 for i,s in enumerate(SOURCES):box('bar-source-'+s,'bottom',4-i+.2,0,cost[s]);box('bar-application-'+s,'bottom',4-i-.2,0,cost[APPS[s]])
 return out

def compare_boxes(actual,want):
 need(set(actual)==set(want),'all 18 exact bar identities')
 for k,v in want.items():need(all(abs(a-b)<3e-6 for a,b in zip(actual[k],v)),'actual zero-based bar geometry '+k)

def graph_audit(H,c):
 want=expected_geometry(c);svg=rectangles_svg((H/'costs.svg').read_text());compare_boxes(svg,want);pdf=rectangles_pdf(H/'costs.pdf');need(len(pdf)==18,'all18 actual PDF rectangles')
 unused=list(pdf)
 for key,v in want.items():
  found=[i for i,r in enumerate(unused)if all(abs(a-b)<3e-6 for a,b in zip(r,v))];need(len(found)==1,'actual PDF dimension '+key);unused.pop(found[0])
 need(not unused,'no extra coloured data bars');compare_boxes(read(H/'plot_data.json')['expected_rectangles'],want)
 text=(H/'costs.svg').read_text();need('raw extraction' in text and 'all axes start at zero' in text and 'mandatory JSON' in text and 'retained mathematical premises' in text,'graph labels and acquisition prerequisites')
 return want

def review(H,study=None):
 need(sha((H/'manifest.json').read_bytes())==PIN,'exact frozen author manifest');m=read(H/'manifest.json');need(len(m['exports'])==37,'37 declared exports')
 for row in m['exports']:
  path=Path(row['path']);need(not path.is_absolute()and '..'not in path.parts,'safe export');b=(H/path).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'export '+str(path))
 protocol=read(H/'protocol.json');need(sha((H/'inputs/adoption/manifest.json').read_bytes())==ADOPTION,'accepted input adoption')
 for row in protocol['bindings']:
  b=(H/row['path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact adopted input copy');directory=Path(row['path']).parent
  if Path(row['path']).name!='manifest.json':
   entry=next(x for x in read(H/directory/'manifest.json')['exports']if x['path']==Path(row['path']).name);need(entry['bytes']==row['bytes']and entry['sha256']==row['sha256'],'manifest export membership')
  if study:need((study/row['source_path']).read_bytes()==b,'exact original accepted copy')
 adoption=read(H/'inputs/adoption/adoption.json');need(adoption['status']=='ROOT_ACCEPTED_EXPANDED_E_MEASUREMENT_INPUTS'and adoption['numerical_evaluation_authorized']and not adoption['software_inclusive_factors_permitted'],'distinct input acceptance authorizes only manuscript factors')
 data=read(H/'inputs/input/author_counts.json');policy=read(H/'inputs/input/policy.json');result=read(H/'results.json');ex,groups,inventory,acq=audit_result(result,data,policy,protocol)
 verified=[]
 if study:
  for r in inventory:
   b=(study/r['path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'full current raw file '+r['path']);verified.append(r['path'])
 csvcounts=csv_audit(H,ex,inventory,acq);boxes=graph_audit(H,ex[PRIMARY]);tex=(H/'reader.tex').read_text();texts=[p.extract_text()or''for p in PdfReader(H/'reader.pdf').pages];need(len(texts)==3,'three full reader pages')
 need('Magma' in texts[2] and 'quotient algorithm' in texts[2] and 'data fields incorrectly say GAP' in texts[2],'explicit historical L043 software correction')
 need('raw, untrimmed' in tex and 'Optional validation is not a theorem premise' in tex and 'software-inclusive factor remains null' in tex,'visible primary/symmetry/conditional qualifications')
 for token in ['140,286','89,810','57,473','32,337','1.562031']:need(token in '\n'.join(texts)or token.replace(',','')in '\n'.join(texts),'reader primary value '+token)
 # Compare the six primary and thirty sensitivity displayed rounded values.
 for c in ex.values():need(f"{Decimal(c['written']['decimal']):.6f}"in tex,'all displayed sensitivity factors')
 for s in SOURCES:need(f"{Decimal(ex[PRIMARY]['conditional'][s]['decimal']):.6f}"in tex,'displayed conditional')
 controls=[]
 for name,change in [('free common',lambda r:r['coordinates'][PRIMARY].update(whole_common=0)),('wrong application pairing',lambda r:r['applications'].update(L079='A1')),('missing whole app',lambda r:r['coordinates'][PRIMARY].update(whole_written=1)),('wrong fraction',lambda r:r['coordinates'][PRIMARY]['written'].update(numerator=1)),('wrong decimal',lambda r:r['coordinates'][PRIMARY]['conditional']['L043'].update(decimal='6.000000000000')),('drop JSON',lambda r:r['whole_file_inventory'].pop(12)),('promote optional code to required',lambda r:r['whole_file_inventory'][6].update(group='required_programs')),('optional count zero',lambda r:r['whole_file_group_costs']['optional_validation'].update(files=0)),('invent software factor',lambda r:r.update(software_inclusive_factors=2)),('unknown graphics zero',lambda r:r['unknown_costs'].update(full_graphics_formula_layout=0)),('free initial acquisition',lambda r:r['primary_acquisition'][0].update(replacement_written=0)),('substitute selected primary',lambda r:r.update(primary_coordinate='raw_selected/NFC/characters_without_whitespace'))]:
  q=deepcopy(result);change(q)
  try:audit_result(q,data,policy,protocol)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('mutation accepted '+name)
 for name,change in [('bar stretched',lambda d:d.__setitem__('bar-whole-source',(129.6,80,600,15))),('conditional bar omitted',lambda d:d.pop('bar-application-L043'))]:
  q=deepcopy(boxes);change(q)
  try:compare_boxes(q,boxes)
  except ValueError:controls.append(name)
  else:raise ValueError('geometry mutation accepted')
 return dict(status='PASS_INDEPENDENT_NUMERICAL_AND_VECTOR_AUDIT',author_manifest_sha256=PIN,input_adoption_manifest_sha256=ADOPTION,coordinates=30,exact_fractions=180,complete_document_cells=390,whole_file_metric_cells=250,whole_files=25,whole_file_bindings_checked=len(verified),csv_rows=csvcounts,total_csv_rows=sum(csvcounts.values()),actual_SVG_rectangles=18,actual_PDF_rectangles=18,primary=ex[PRIMARY]['written'],conditionals=ex[PRIMARY]['conditional'],role_counts={k:v['files']for k,v in groups.items()},controls_rejected=controls,reader_pages=3,reader_page_text_sha256=[sha(x.encode())for x in texts],unknown_costs=result['unknown_costs'],software_inclusive_factors=None,source_extraction_or_science_replayed=False,imports_numerical_author_modules=False,review_role='Distinct current arithmetic/reader review. Prior old-E common proof authorship and earlier E audits disclosed; accepted new science/input/root records are reused, not independently readjudicated here.')

def main():
 here=Path(__file__).resolve().parent
 if(here/'manifest.json').exists():
  for row in read(here/'manifest.json')['exports']:
   b=(here/row['path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'frozen independent review export')
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path);a.add_argument('--out',type=Path,required=True);x=a.parse_args();need(not x.out.exists(),'fresh report output');r=review(x.packet,x.study_root);x.out.parent.mkdir(parents=True,exist_ok=True);x.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS independent180 fractions/640 component cells/18SVG+18PDF bars/'+str(len(r['controls_rejected']))+' controls')
if __name__=='__main__':main()
