#!/usr/bin/env python3
"""Arithmetic, complete-boundary and actual vector-bar controls for the F005 report."""
from pathlib import Path
import argparse,copy,csv,json,math,re,xml.etree.ElementTree as ET
from compute import need,read,write,inputs,derive,csv_rows,ORDER,VARIANTS,FORMS,UNITS

def validate(r,data):
 c,policy,boundary,bindings,p=data
 need(r['coordinate_count']==len(r['coordinates'])==30,'all thirty coordinates')
 for row,(v,n,u)in zip(r['coordinates'],[(v,n,u)for v in VARIANTS for n in FORMS for u in UNITS]):
  need((row['variant'],row['normalization'],row['unit'])==(v,n,u),'coordinate order')
  d={k:x['metrics'][v][n][u]for k,x in c['documents'].items()};raw={g:sum(x['metrics'][n][u]for x in files.values())for g,files in c['raw_files'].items()}
  need(row['document_costs']==d and row['raw_costs']==raw,'whole document and raw file costs')
  den=[d['U']+d['A1']+d['A2'],d['A1']+d['A2'],sum(d[k]for k in ['U','A1','A2','CODE1','CODE2']),d['U']+d['A1']+d['A2']+raw['programs']]
  need(list(row['comparisons'])==ORDER,'four exact comparison identities')
  for key,base in zip(ORDER,den):
   g=math.gcd(d['F005'],base);num=d['F005']//g;bottom=base//g;frac=str(num)if bottom==1 else str(num)+'/'+str(bottom)
   need(row['comparisons'][key]==dict(numerator=d['F005'],denominator=base,reduced_numerator=num,reduced_denominator=bottom,exact_fraction=frac,decimal=f"{d['F005']/base:.12f}"),'complete exact fraction '+key)
 need(r['primary']==r['coordinates'][2],'fixed raw untrimmed NFC nonspace primary')
 need(r==derive(*data),'complete scope, acquisition and unknown-cost metadata')
 return dict(coordinates=30,exact_fractions=120,whole_PDF_cells=180,raw_cells=70)

def rectangle_bounds(points):
 xs=[p[0]for p in points];ys=[p[1]for p in points];return [min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)]
def plot_svg(svg,record,r):
 root=ET.fromstring(svg);found={}
 for group in root.iter():
  gid=group.attrib.get('id','')
  if not gid.startswith('cost-'):continue
  paths=[x for x in group if x.tag.endswith('path')];need(len(paths)==1,'one actual path for '+gid)
  path=paths[0].attrib['d'];need(not re.search('[CQAST]',path,re.I),'straight rectangular cost path')
  nums=[float(x)for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path)];need(len(nums)in (8,10),'four/five literal rectangle vertices')
  pts=list(zip(nums[::2],nums[1::2]));bb=rectangle_bounds(pts)
  need(set((round(x,5),round(y,5))for x,y in pts)==set((round(x,5),round(y,5))for x,y in [(bb[0],bb[1]),(bb[0]+bb[2],bb[1]),(bb[0]+bb[2],bb[1]+bb[3]),(bb[0],bb[1]+bb[3])]),'actual four rectangle corners')
  found[gid]=bb
 d=r['primary']['document_costs'];expected={}
 expected['cost-source']=('F005',0,0)
 for col,keys in [(1,['U','A1','A2']),(2,['U','A1','A2','CODE1','CODE2'])]:
  b=0
  for k in keys:expected['cost-total-'+str(col)+'-'+k]=(k,b,0);b+=d[k]
 for k in ['U','A1','A2','CODE1','CODE2']:expected['cost-component-'+k]=(k,0,1)
 need(len(found)==record['bar_count']==14 and set(found)==set(expected),'all fourteen full cost rectangles')
 need(len(record['axes'])==2 and all(a['minimum']==0 and a['points_per_unit']>0 for a in record['axes']),'zero-based positive axes')
 need(len(record['bars'])==14,'all rectangle records')
 for b in record['bars']:
  k,base,axis=expected[b['id']];need((b['document'],b['base_cost'],b['axis'],b['cost'])==(k,base,axis,d[k]),'actual full document ownership in rectangle')
  need(all(abs(x-y)<.00002 for x,y in zip(found[b['id']],b['svg'])),'actual SVG rectangle dimensions')
  ax=record['axes'][axis];need(abs(b['pdf'][3]-d[k]*ax['points_per_unit'])<.0001,'cost-proportional height')
  need(abs(b['pdf'][1]-(ax['zero_pdf_y']+base*ax['points_per_unit']))<.0001,'cost-proportional stacking')
  need(abs(b['svg'][0]-b['pdf'][0])<.0001 and abs(b['svg'][2]-b['pdf'][2])<.0001 and abs(b['svg'][3]-b['pdf'][3])<.0001,'same PDF/SVG dimensions')
 return 14

def plot_pdf(pdf,record):
 from pypdf import PdfReader
 from pypdf.generic import ContentStream
 reader=PdfReader(pdf);need(len(reader.pages)==1,'one complete plot page');content=ContentStream(reader.pages[0].get_contents(),reader);points=[];rects=[]
 for args,op in content.operations:
  if op==b'm':points=[tuple(map(float,args))]
  elif op==b'l':points.append(tuple(map(float,args)))
  elif op==b're':
   x,y,w,h=map(float,args);points=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
  elif op in [b'f',b'f*',b'B',b'B*']:
   if len(points)in (4,5):
    bb=rectangle_bounds(points)
    if all(abs(x-bb[0])<1e-4 or abs(x-bb[0]-bb[2])<1e-4 for x,y in points)and all(abs(y-bb[1])<1e-4 or abs(y-bb[1]-bb[3])<1e-4 for x,y in points):rects.append(bb)
   points=[]
  elif op in [b'S',b's',b'n']:points=[]
 for b in record['bars']:need(sum(all(abs(x-y)<.0001 for x,y in zip(bb,b['pdf']))for bb in rects)==1,'one actual PDF filled rectangle '+b['id'])
 return 14

def run(a):
 data=inputs(a);r=read(a.results_dir/'results.json');summary=validate(r,data)
 with (a.results_dir/'comparisons.csv').open(newline='')as f:rows=list(csv.DictReader(f))
 need(rows==[{k:str(v)for k,v in x.items()}for x in csv_rows(r)],'all120 exact CSV rows')
 need(read(a.results_dir/'input_bindings.json')==data[3],'companion accepted bindings')
 geometry=read(a.results_dir/'plot_geometry.json');svg=(a.results_dir/'complete_costs.svg').read_text();plot_svg(svg,geometry,r);plot_pdf(a.results_dir/'complete_costs.pdf',geometry)
 from build_reader import reader
 import tempfile
 with tempfile.TemporaryDirectory()as d:
  reader(r,Path(d));need((Path(d)/'measurement.tex').read_bytes()==(a.results_dir/'measurement.tex').read_bytes(),'complete exact reader values and qualifications')
 rejected=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,IndexError)as e:rejected.append(dict(name=name,reason=str(e)));return
  raise ValueError('CONTROL_ACCEPTED: '+name)
 def mutation(name,change):
  x=copy.deepcopy(r);change(x);reject(name,lambda:validate(x,data))
 for name,change in [
  ('drop common from written',lambda x:x['coordinates'][0]['comparisons']['written_papers'].__setitem__('denominator',x['coordinates'][0]['application_cost'])),
  ('make exceptional proof free',lambda x:x['coordinates'][0]['comparisons']['conditional_application'].__setitem__('denominator',x['coordinates'][0]['document_costs']['A1'])),
  ('omit exceptional appendix',lambda x:x['coordinates'][0]['comparisons']['including_printed_programs'].__setitem__('denominator',x['coordinates'][0]['written_denominator']+x['coordinates'][0]['document_costs']['CODE1'])),
  ('double-charge printed and raw',lambda x:x['coordinates'][0]['comparisons']['including_raw_programs_alternative'].__setitem__('denominator',x['coordinates'][0]['written_denominator']+x['coordinates'][0]['printed_program_cost']+x['coordinates'][0]['raw_costs']['programs'])),
  ('silently add driver costs',lambda x:x['coordinates'][0]['comparisons']['written_papers'].__setitem__('denominator',x['coordinates'][0]['written_denominator']+x['coordinates'][0]['raw_costs']['drivers'])),
  ('wrong exact reduction',lambda x:x['coordinates'][0]['comparisons']['written_papers'].__setitem__('reduced_denominator',1)),
  ('hide common/program prepayment',lambda x:x.__setitem__('conditional_prepaid','no acquisition')),
  ('drop complete raw program',lambda x:x['raw_file_inventory']['programs'].pop(next(iter(x['raw_file_inventory']['programs'])))),
  ('change primary',lambda x:x.__setitem__('primary',x['coordinates'][22])),
  ('omit coordinate',lambda x:x['coordinates'].pop()),
  ('graphics unknown becomes zero',lambda x:x['unknown_costs'].__setitem__('full_graphics',0)),
  ('runtime unknown becomes zero',lambda x:x['unknown_costs'].__setitem__('runtime',0)),
  ('overlap discount',lambda x:x.__setitem__('overlap_discount',True)),
  ('cross-topic discount',lambda x:x.__setitem__('cross_topic_discount',True)),
  ('claim all source formalized',lambda x:x.__setitem__('whole_source_formalized',True)),
  ('solve three final problems',lambda x:x.__setitem__('unanswered_final_problems',0)),
  ('count source rows as originals',lambda x:x.__setitem__('original_manuscripts',35)),
  ('erase literal correction',lambda x:x['accepted_literal_counterexample_targets'].pop()),
  ('remove medial convention',lambda x:x['accepted_qualified_counterexample_targets'].clear()),
  ('claim new priority',lambda x:x.__setitem__('historical_priority_claim',True))]:mutation(name,change)
 # Exercise actual SVG geometry, not only a decorative metadata hash.
 root=ET.fromstring(svg);g=next(x for x in root.iter()if x.attrib.get('id')=='cost-source');path=next(x for x in g if x.tag.endswith('path'));numbers=list(re.finditer(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path.attrib['d']));n=numbers[1];path.set('d',path.attrib['d'][:n.start()]+str(float(n.group())+8)+path.attrib['d'][n.end():]);reject('distorted actual source rectangle',lambda:plot_svg(ET.tostring(root,encoding='unicode'),geometry,r))
 z=copy.deepcopy(geometry);z['bars'][1]['base_cost']+=1;reject('wrong acquisition stacking',lambda:plot_svg(svg,z,r))
 z=copy.deepcopy(geometry);z['axes'][0]['minimum']=1;reject('nonzero graph baseline',lambda:plot_svg(svg,z,r))
 z=copy.deepcopy(geometry);z['bars'][0]['pdf'][3]+=3;reject('wrong actual PDF rectangle height',lambda:plot_pdf(a.results_dir/'complete_costs.pdf',z))
 report=dict(status='PASS_AUTHOR_ARITHMETIC_BOUNDARY_AND_VECTOR_CONTROLS',**summary,csv_rows=120,actual_svg_bars=14,actual_pdf_bars=14,negative_controls=len(rejected),controls=rejected,independent_arithmetic_review=False,source_or_science_replayed=False)
 need(not a.out.exists(),'fresh report');write(a.out,report);print('PASS120 exact fractions/CSV rows,14 SVG+14 PDF rectangles,'+str(len(rejected))+' controls.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--results-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);run(ap.parse_args())
