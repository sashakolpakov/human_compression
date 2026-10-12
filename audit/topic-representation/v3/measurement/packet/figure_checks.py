"""Check actual vector rectangles and graph paths, not just plotting data."""
import re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
from calculate import need
from presentation import COLORS,bars,graph
NS={'s':'http://www.w3.org/2000/svg'}
def near(a,b):return abs(a-b)<.00002
def nums(s):return [float(x)for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
def svg_rectangles(raw):
 out={};root=ET.fromstring(raw)
 for g in root.findall('.//s:g',NS):
  k=g.get('id','')
  if not k.startswith('cost-'):continue
  p=g.findall('s:path',NS);need(len(p)==1 and k not in out,'unique rectangle path');d=p[0].get('d','');v=nums(d)
  need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz'and len(v)==8,'literal four-corner rectangle')
  x=v[::2];y=v[1::2];need(near(x[0],x[3])and near(x[1],x[2])and near(y[0],y[1])and near(y[2],y[3]),'axis aligned rectangle')
  out[k]=[min(x),min(y),max(x)-min(x),max(y)-min(y)]
 return out

def compare_svg(raw,r,name):
 W,H,e=bars(r,name);a=svg_rectangles(raw);need(set(a)=={x['id']for x in e},'complete SVG bars')
 for x in e:need(all(near(q,v)for q,v in zip(a[x['id']],[x['x'],H-x['y']-x['h'],x['w'],x['h']])),'SVG actual geometry '+x['id'])

def pdf_rectangles(path):
 reader=PdfReader(path);need(len(reader.pages)==1,'one figure page');p=reader.pages[0];color=None;stack=[];points=[];out=[]
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
    if near(x[0],x[3])and near(x[1],x[2])and near(y[0],y[1])and near(y[2],y[3]):out.append([min(x),min(y),max(x)-min(x),max(y)-min(y)])
   points=[]
  elif op in [b'n',b'S']:points=[]
 return out,float(p.mediabox.height)

def check(root,r):
 count=0
 for name in ['costs','inventory']:
  compare_svg((root/(name+'.svg')).read_bytes(),r,name);W,H,e=bars(r,name);actual,ph=pdf_rectangles(root/(name+'.pdf'));need(near(ph,H),'PDF scale')
  for b in e:
   matches=[i for i,x in enumerate(actual)if all(near(u,v)for u,v in zip(x,[b['x'],b['y'],b['w'],b['h']]))];need(len(matches)==1,'actual PDF geometry '+b['id']);actual.pop(matches[0])
  need(not actual,'no unaccounted colored PDF bars');count+=len(e)
 g=graph(r);actual=__import__('json').loads((root/'document_graph.json').read_text());need(actual==g,'whole acquisition graph semantics')
 svg=ET.fromstring((root/'document_graph.svg').read_bytes());groups={x.get('id'):x for x in svg.findall('.//s:g',NS)}
 need({k for k in groups if k and k.startswith('node-')}=={'node-'+n['id']for n in g['nodes']},'all graph boxes')
 need({k for k in groups if k and k.startswith('edge-')}=={'edge-'+x['source']+'-'+x['target']for x in g['edges']},'all graph arrows')
 boxes={}
 for n in g['nodes']:
  p=groups['node-'+n['id']].find('s:path',NS);v=nums(p.get('d'));boxes[n['id']]=[min(v[::2]),min(v[1::2]),max(v[::2]),max(v[1::2])]
 def distance(pt,box):
  x,y=pt;a,b,c,d=box;return max(a-x,0,x-c,b-y,y-d)
 for e in g['edges']:
  ps=groups['edge-'+e['source']+'-'+e['target']].findall('s:path',NS);need(len(ps)==2,'arrow shaft and head');v=nums(ps[0].get('d'));need(distance(v[:2],boxes[e['source']])<12 and distance(v[-2:],boxes[e['target']])<12,'arrow endpoints')
  need(('stroke-dasharray'in ps[0].get('style',''))==(e['kind']in ['correspondence','optional_check']),'required/optional distinct arrow styles')
 controls=[];raw=(root/'costs.svg').read_bytes()
 for name,transform in [('missing bar',lambda z:z.replace(b'cost-whole-F010',b'not-a-bar',1)),('changed value',None)]:
  if transform is None:
   altered=__import__('copy').deepcopy(r);altered['primary']['costs']['F010']+=100
   try:compare_svg(raw,altered,'costs')
   except ValueError:controls.append(name)
   else:raise ValueError('distorted geometry accepted')
  else:
   try:compare_svg(transform(raw),r,'costs')
   except ValueError:controls.append(name)
   else:raise ValueError('missing bar accepted')
 return {'actual_SVG_bars':count,'actual_PDF_bars':count,'graph_nodes':len(g['nodes']),'graph_arrows':len(g['edges']),'figure_controls':controls}
