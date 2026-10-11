"""Inspect actual rectangle paths in the two vector cost representations."""
import re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
from calculate import need
from presentation import COLORS
NS={'s':'http://www.w3.org/2000/svg'}
def near(a,b):return abs(a-b)<0.00001

def expected(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];app=['U','A1','A2']
 groups=[('written',80000,[[('L014',c['L014']),('L007',c['L007'])],[(k,c[k])for k in app]]),('validation',30000,[[('CODE',c['CODE'])],[('programs',raw['programs'])]]),('conditional',50000,[[('L014',c['L014'])],[('A1',c['A1'])],[('L007',c['L007'])],[('A2',c['A2'])]])]
 W=11.4*72;H=4.5*72;aw=W*(.98-.075)/(3+.42*2);ah=H*(.86-.30);out={}
 for j,(panel,limit,columns)in enumerate(groups):
  span=1.1*(len(columns)-.2);xmin=-.4-.05*(len(columns)-.2)
  for i,parts in enumerate(columns):
   base=0
   for key,val in parts:
    x=W*.075+j*aw*1.42+(i-.4-xmin)*aw/span;y=H*(1-.30)-(base+val)*ah/limit
    out[f'cost-{panel}-{i}-{key}']=[x,y,.8*aw/span,val*ah/limit];base+=val
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
 a=svg_rectangles(raw);need(set(a)==set(e),'all11 cost bars')
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
 need(len(rows)==7,'exactly seven legend swatches remain')
 controls=[]
 def distort(z):
  tree=ET.fromstring(z);g=next(g for g in tree.findall('.//s:g',NS)if g.get('id')=='cost-written-0-L014');p=g.find('s:path',NS);d=p.get('d');a=re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',d);a[5]=str(float(a[5])+2);a[7]=str(float(a[7])+2);p.set('d',f'M {a[0]} {a[1]} L {a[2]} {a[3]} L {a[4]} {a[5]} L {a[6]} {a[7]} z');return ET.tostring(tree)
 for name,fn in [('distorted actual SVG height',distort),('missing SVG rectangle',lambda z:z.replace(b'cost-validation-1-programs',b'missing-cost',1))]:
  try:compare_svg(fn((path/'costs.svg').read_bytes()),e)
  except ValueError:controls.append(dict(name=name,rejected=True))
  else:raise ValueError('figure corruption accepted')
 return dict(actual_svg_cost_bars=len(e),actual_pdf_cost_bars=len(e),legend_swatches=7,controls=controls)


def graph_check(path,r):
 from presentation import graph
 data=__import__('json').loads((path/'document_graph.json').read_text());need(data==graph(r),'exact whole-document graph semantics')
 root=ET.fromstring((path/'document_graph.svg').read_bytes());groups={g.get('id'):g for g in root.findall('.//s:g',NS)}
 nodeids={'node-'+x['id']for x in data['nodes']};edgeids={'edge-'+x['source']+'-'+x['target']for x in data['edges']}
 need({k for k in groups if k and k.startswith('node-')}==nodeids,'all seven actual boxes');need({k for k in groups if k and k.startswith('edge-')}==edgeids,'all nine actual arrows')
 def nums(p):return [float(x)for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',p.get('d',''))]
 boxes={}
 for k in nodeids:
  v=nums(groups[k].find('s:path',NS));boxes[k[5:]]=(min(v[::2]),min(v[1::2]),max(v[::2]),max(v[1::2]))
 def distance(point,box):
  x,y=point;a,b,c,d=box;return max(a-x,0,x-c,y-d,b-y)
 for e in data['edges']:
  ps=groups['edge-'+e['source']+'-'+e['target']].findall('s:path',NS);need(len(ps)==2,'shaft plus arrowhead');v=nums(ps[0]);need(distance(v[:2],boxes[e['source']])<12 and distance(v[-2:],boxes[e['target']])<12,'actual prerequisite-to-use endpoint '+str(e))
  dashed='stroke-dasharray' in ps[0].get('style','');need(dashed==(e['kind']in ['source_correspondence','validation_association']),'logical and nonlogical arrow styles')
 return dict(nodes=len(nodeids),arrows=len(edgeids),direction='prerequisite or associated evidence to application',direct_retained_inputs=['U','A1','A2'],validation_edges_are_not_proof_dependencies=True)
