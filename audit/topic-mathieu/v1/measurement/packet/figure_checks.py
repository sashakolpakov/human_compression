"""Inspect actual rectangle paths in the two vector cost representations."""
import re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
from calculate import need
from presentation import COLORS
NS={'s':'http://www.w3.org/2000/svg'}
def near(a,b):return abs(a-b)<0.00001

def expected(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];app=['U','A1','CLASSES','ROWS']
 groups=[('written',50000,[[('source',c['L073'])],[(k,c[k])for k in app]]),('computational',145000,[[(k,c[k])for k in app+['CODE']]+[('required_raw_data',raw['required_raw_data'])],[(k,c[k])for k in app]+[('programs',raw['programs']),('required_raw_data',raw['required_raw_data'])]]),('conditional',50000,[[('source',c['L073'])],[(k,c[k])for k in app[1:]]])]
 W=11.4*72;H=4.5*72;aw=W*(.98-.075)/(3+.42*2);ah=H*(.86-.30);out={}
 for j,(panel,limit,columns)in enumerate(groups):
  for i,parts in enumerate(columns):
   base=0
   for key,val in parts:
    x=W*.075+j*aw*1.42+((i-.4)+.49)*aw/1.98;y=H*(1-.30)-(base+val)*ah/limit
    out[f'cost-{panel}-{i}-{key}']=[x,y,.8*aw/1.98,val*ah/limit];base+=val
 return out,H

def svg_rectangles(raw):
 root=ET.fromstring(raw);out={}
 for g in root.findall('.//s:g',NS):
  gid=g.get('id','')
  if not gid.startswith('cost-'):continue
  need(gid not in out,'unique SVG cost id');p=g.findall('s:path',NS);need(len(p)==1,'one rectangle per cost')
  d=p[0].get('d','');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','cost is literal rectangle')
  nums=[float(z)for z in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',d)]
  need(len(nums)==8,'four rectangle vertices');x=nums[::2];y=nums[1::2]
  need(near(x[0],x[3])and near(x[1],x[2])and near(y[0],y[1])and near(y[2],y[3]),'axis-aligned bars')
  out[gid]=[min(x),min(y),max(x)-min(x),max(y)-min(y)]
 return out

def compare_svg(raw,e):
 a=svg_rectangles(raw);need(set(a)==set(e),'all21 cost bars')
 for k,v in e.items():need(all(near(x,y)for x,y in zip(a[k],v)),'actual SVG bar '+k)

def pdf_rectangles(path):
 reader=PdfReader(path);need(len(reader.pages)==1,'one-page cost plot');p=reader.pages[0];stack=[];color=None;points=[];rows=[]
 allowed=[tuple(int(h[i:i+2],16)/255 for i in [1,3,5])for h in COLORS.values()]
 for args,op in ContentStream(p.get_contents(),p.pdf).operations:
  if op==b'q':stack.append(color)
  elif op==b'Q':color=stack.pop()
  elif op==b'rg':color=tuple(float(x)for x in args)
  elif op==b'm':points=[tuple(float(x)for x in args)]
  elif op==b'l':points.append(tuple(float(x)for x in args))
  elif op==b're':points=[]
  elif op in [b'f',b'B',b'f*',b'B*']:
   if len(points)==4 and color is not None and any(all(near(x,y)for x,y in zip(color,c))for c in allowed):
    x=[p[0]for p in points];y=[p[1]for p in points]
    if near(x[0],x[3])and near(x[1],x[2])and near(y[0],y[1])and near(y[2],y[3]):rows.append([min(x),min(y),max(x)-min(x),max(y)-min(y)])
   points=[]
  elif op in [b'n',b'S']:points=[]
 return rows,float(p.mediabox.height)

def check(path,r):
 e,H=expected(r);compare_svg((path/'costs.svg').read_bytes(),e);rows,height=pdf_rectangles(path/'costs.pdf');need(near(H,height),'PDF height')
 for k,(x,y,w,h)in e.items():
  target=[x,H-y-h,w,h];match=[i for i,a in enumerate(rows)if all(near(u,v)for u,v in zip(a,target))];need(len(match)==1,'actual PDF bar '+k);rows.pop(match[0])
 need(len(rows)==8,'exactly eight legend swatches remain')
 controls=[]
 def distort(z):
  tree=ET.fromstring(z);g=next(g for g in tree.findall('.//s:g',NS)if g.get('id')=='cost-written-0-source');p=g.find('s:path',NS);d=p.get('d');a=re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',d);a[5]=str(float(a[5])+2);a[7]=str(float(a[7])+2);p.set('d',f'M {a[0]} {a[1]} L {a[2]} {a[3]} L {a[4]} {a[5]} L {a[6]} {a[7]} z');return ET.tostring(tree)
 for name,fn in [('distorted actual SVG height',distort),('missing SVG rectangle',lambda z:z.replace(b'cost-computational-1-required_raw_data',b'missing-cost',1))]:
  try:compare_svg(fn((path/'costs.svg').read_bytes()),e)
  except ValueError:controls.append(dict(name=name,rejected=True))
  else:raise ValueError('figure corruption accepted')
 return dict(actual_svg_cost_bars=len(e),actual_pdf_cost_bars=len(e),legend_swatches=8,controls=controls)
