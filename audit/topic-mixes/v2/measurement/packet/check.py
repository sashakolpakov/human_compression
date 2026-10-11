#!/usr/bin/env python3
"""Author arithmetic and actual-vector integrity controls, not distinct acceptance."""
from pathlib import Path
import argparse,copy,csv,math,re,tempfile,xml.etree.ElementTree as ET
from compute import need,read,write,load_inputs,derive,csv_rows,ORDER,VARIANTS,NORMALS,UNITS

def validate(r,data):
 docs,raw,p,b=data
 need(r['coordinate_count']==len(r['coordinates'])==30 and r['exact_fraction_count']==90,'thirty coordinates/ninety fractions')
 for row,(v,n,u)in zip(r['coordinates'],[(v,n,u)for v in VARIANTS for n in NORMALS for u in UNITS]):
  need((row['variant'],row['normalization'],row['unit'])==(v,n,u),'coordinate order')
  d={k:x['metrics'][v][n][u]for k,x in docs.items()};need(row['document_costs']==d,'complete document values')
  nums=[d['F005']+d['L016'],d['F005'],d['L016']];dens=[d['U0']+d['U1']+d['A1']+d['A2']+d['A3'],d['A1']+d['A2'],d['A3']]
  need(list(row['comparisons'])==ORDER,'only written/conditional comparisons')
  for key,num,den in zip(ORDER,nums,dens):
   g=math.gcd(num,den);a=num//g;b=den//g;f=str(a)if b==1 else str(a)+'/'+str(b)
   need(row['comparisons'][key]==dict(numerator=num,denominator=den,reduced_numerator=a,reduced_denominator=b,exact_fraction=f,decimal=f'{num/den:.12f}'),'actual arithmetic '+key)
 need(r['primary']==r['coordinates'][2],'fixed primary')
 need(r==derive(*data),'all roles, unknown costs, full file vectors and scope')
 return dict(coordinates=30,exact_fractions=90,whole_PDF_cells=330,raw_cells=130)

def rectangle_bounds(points):
 xs=[p[0]for p in points];ys=[p[1]for p in points];return [min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)]
def plot_svg(svg,record,r):
 root=ET.fromstring(svg);found={}
 for group in root.iter():
  gid=group.attrib.get('id','')
  if not(gid.startswith('whole-')or gid.startswith('conditional-')):continue
  paths=[x for x in group if x.tag.endswith('path')];need(len(paths)==1,'one actual path for '+gid)
  path=paths[0].attrib['d'];need(not re.search('[CQAST]',path,re.I),'straight rectangular cost path')
  nums=[float(x)for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path)];need(len(nums)in (8,10),'four/five literal rectangle vertices')
  pts=list(zip(nums[::2],nums[1::2]));bb=rectangle_bounds(pts)
  need(set((round(x,5),round(y,5))for x,y in pts)==set((round(x,5),round(y,5))for x,y in [(bb[0],bb[1]),(bb[0]+bb[2],bb[1]),(bb[0]+bb[2],bb[1]+bb[3]),(bb[0],bb[1]+bb[3])]),'actual four rectangle corners')
  found[gid]=bb
 d=r['primary']['document_costs'];expected={}
 for keys,prefix,axis in [(['F005','L016'],'whole-',0),(['U0','U1','A1','A2','A3'],'whole-',0),(['F005'],'conditional-',1),(['A1','A2'],'conditional-',1),(['L016'],'conditional-',1),(['A3'],'conditional-',1)]:
  base=0
  for k in keys:expected[prefix+k]=(k,base,axis);base+=d[k]
 need(len(found)==record['bar_count']==12 and set(found)==set(expected),'all twelve full cost rectangles')
 need(len(record['axes'])==2 and all(a['minimum']==0 and a['points_per_unit']>0 for a in record['axes']),'zero-based positive axes')
 need(len(record['bars'])==12,'all rectangle records')
 for b in record['bars']:
  k,base,axis=expected[b['id']];need((b['document'],b['base_cost'],b['axis'],b['cost'])==(k,base,axis,d[k]),'actual full document ownership in rectangle')
  need(all(abs(x-y)<.00002 for x,y in zip(found[b['id']],b['svg'])),'actual SVG rectangle dimensions')
  ax=record['axes'][axis];need(abs(b['pdf'][3]-d[k]*ax['points_per_unit'])<.0001,'cost-proportional height')
  need(abs(b['pdf'][1]-(ax['zero_pdf_y']+base*ax['points_per_unit']))<.0001,'cost-proportional stacking')
  need(abs(b['svg'][0]-b['pdf'][0])<.0001 and abs(b['svg'][2]-b['pdf'][2])<.0001 and abs(b['svg'][3]-b['pdf'][3])<.0001,'same PDF/SVG dimensions')
 return 12

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
 return 12

def run(a):
 data=load_inputs(a.inputs,a.prior_inputs,a.input_review);r=read(a.results_dir/'results.json');summary=validate(r,data)
 with(a.results_dir/'comparisons.csv').open(newline='')as f:rows=list(csv.DictReader(f))
 need(rows==[{k:str(v)for k,v in x.items()}for x in csv_rows(r)],'all90 CSV rows')
 need(read(a.results_dir/'input_bindings.json')==data[3],'exact acceptance bindings')
 geometry=read(a.results_dir/'plot_geometry.json');svg=(a.results_dir/'complete_costs.svg').read_text();plot_svg(svg,geometry,r);plot_pdf(a.results_dir/'complete_costs.pdf',geometry)
 from build_reader import reader,document_graphs
 with tempfile.TemporaryDirectory()as t:
  tmp=Path(t);reader(r,tmp);document_graphs(r,tmp)
  for name in ['measurement.tex','document_graphs.json','document_graphs.svg','document_graphs.pdf']:need((tmp/name).read_bytes()==(a.results_dir/name).read_bytes(),'exact reader/paired graph '+name)
 rejected=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,IndexError)as e:rejected.append(dict(name=name,reason=str(e)));return
  raise ValueError('CONTROL_ACCEPTED: '+name)
 def mutation(name,fn):
  z=copy.deepcopy(r);fn(z);reject(name,lambda:validate(z,data))
 for name,fn in [
  ('omit old common',lambda x:x['coordinates'][0]['comparisons']['whole_topic'].__setitem__('denominator',x['coordinates'][0]['written_denominator']-x['coordinates'][0]['document_costs']['U0'])),
  ('omit new common',lambda x:x['coordinates'][0]['comparisons']['whole_topic'].__setitem__('denominator',x['coordinates'][0]['written_denominator']-x['coordinates'][0]['document_costs']['U1'])),
  ('omit exceptional application',lambda x:x['coordinates'][0]['comparisons']['conditional_MX1'].__setitem__('denominator',x['coordinates'][0]['document_costs']['A1'])),
  ('invent one-sided validation-inclusive factor',lambda x:x['coordinates'][0]['comparisons'].__setitem__('with_validation',x['coordinates'][0]['comparisons']['whole_topic'])),
  ('historical software zero',lambda x:x.__setitem__('historical_software_cost',0)),
  ('omit required certificate',lambda x:x['required_files'].pop()),
  ('hide optional program',lambda x:x['whole_raw_file_inventory']['programs'].pop(next(iter(x['whole_raw_file_inventory']['programs'])))),
  ('wrong exact reduction',lambda x:x['coordinates'][1]['comparisons']['whole_topic'].__setitem__('reduced_denominator',1)),
  ('missing conditional acquisition',lambda x:x.__setitem__('conditional_prepaid','none')),
  ('change primary',lambda x:x.__setitem__('primary',x['coordinates'][22])),
  ('drop coordinate',lambda x:x['coordinates'].pop()),
  ('unknown graphics zero',lambda x:x['unknown_costs'].__setitem__('full_graphics',0)),
  ('overlap discount',lambda x:x.__setitem__('overlap_discount',True)),
  ('full formalization',lambda x:x.__setitem__('end_to_end_formalization',True)),
  ('count clauses as originals',lambda x:x.__setitem__('original_count',54)),
  ('erase source qualification',lambda x:x['source_scope_limits'].pop()),
  ('originality inference',lambda x:x.__setitem__('historical_originality_inference',True))]:mutation(name,fn)
 root=ET.fromstring(svg);g=next(x for x in root.iter()if x.attrib.get('id')=='whole-F005');path=next(x for x in g if x.tag.endswith('path'));nums=list(re.finditer(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path.attrib['d']));n=nums[1];path.set('d',path.attrib['d'][:n.start()]+str(float(n.group())+8)+path.attrib['d'][n.end():]);reject('distorted actual source rectangle',lambda:plot_svg(ET.tostring(root,encoding='unicode'),geometry,r))
 z=copy.deepcopy(geometry);z['bars'][1]['base_cost']+=1;reject('wrong cumulative stacking',lambda:plot_svg(svg,z,r))
 z=copy.deepcopy(geometry);z['axes'][0]['minimum']=1;reject('nonzero baseline',lambda:plot_svg(svg,z,r))
 z=copy.deepcopy(geometry);z['bars'][0]['pdf'][3]+=3;reject('wrong actual PDF rectangle',lambda:plot_pdf(a.results_dir/'complete_costs.pdf',z))
 report=dict(status='PASS_AUTHOR_COMPLETE_BOUNDARY_AND_VECTOR_CHECK',**summary,csv_rows=90,actual_svg_bars=12,actual_pdf_bars=12,negative_controls=len(rejected),controls=rejected,paired_document_graphs_exact=True,software_inclusive_ratio=None,independent_numerical_review=False,source_or_science_replayed=False)
 need(not a.out.exists(),'fresh report');write(a.out,report);print('PASS90fractions/CSV,12SVG+12PDF bars,'+str(len(rejected))+'controls')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--inputs',type=Path,required=True);a.add_argument('--prior-inputs',type=Path,required=True);a.add_argument('--input-review',type=Path,required=True);a.add_argument('--results-dir',type=Path,required=True);a.add_argument('--out',type=Path,required=True);run(a.parse_args())
