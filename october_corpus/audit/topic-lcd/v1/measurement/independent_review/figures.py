#!/usr/bin/env python3
"""Independent direct SVG/PDF rectangle and directed-arrow inspection."""
import json,re,math,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream
from arithmetic import need,read,DOCS,ROLES
NS='{http://www.w3.org/2000/svg}'
def nums(t):return [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',t)]
def near(a,b):return abs(a-b)<2e-4
def box(points):return (min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)-min(x for x,y in points),max(y for x,y in points)-min(y for x,y in points))
def points(path):
 x=nums(path);return list(zip(x[::2],x[1::2]))
def rect(ps):
 need(len(ps)==4 and len({round(x,4) for x,y in ps})==2 and len({round(y,4) for x,y in ps})==2,'four actual rectangle vertices')
 return box(ps)
def point_dist(p,b):
 x,y=p;l,t,w,h=b;return max(l-x,x-l-w,t-y,y-t-h,0)
def identity():return (1,0,0,1,0,0)
def compose(a,b):
 A,B,C,D,E,F=a;G,H,I,J,K,L=b
 return (A*G+C*H,B*G+D*H,A*I+C*J,B*I+D*J,A*K+C*L+E,B*K+D*L+F)
def transform(m,p):
 a,b,c,d,e,f=m;x,y=p;return(a*x+c*y+e,b*x+d*y+f)
def pdf_paths(path):
 r=PdfReader(path);need(len(r.pages)==1,'one vector figure page');p=r.pages[0];state=(identity(),None,());stack=[];pathpts=[];ops=[];allpaths=[]
 for args,op in ContentStream(p.get_contents(),p.pdf).operations:
  if op==b'q':stack.append(state)
  elif op==b'Q':state=stack.pop()
  elif op==b'cm':state=(compose(state[0],tuple(map(float,args))),state[1],state[2])
  elif op==b'rg':state=(state[0],tuple(map(float,args)),state[2])
  elif op==b'd':state=(state[0],state[1],tuple(map(float,args[0])))
  elif op==b'm':pathpts=[transform(state[0],tuple(map(float,args)))];ops=['m']
  elif op==b'l':pathpts.append(transform(state[0],tuple(map(float,args))));ops.append('l')
  elif op==b'c':
   pts=list(zip(map(float,args[::2]),map(float,args[1::2])));pathpts.extend(transform(state[0],x) for x in pts);ops.append('c')
  elif op==b're':
   x,y,w,h=map(float,args);pathpts=[transform(state[0],q) for q in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]];ops=['re']
  elif op in [b'B',b'B*',b'f',b'f*',b'S']:
   if pathpts:allpaths.append({'points':pathpts[:],'ops':ops[:],'fill':state[1],'dash':state[2],'paint':op.decode()})
   pathpts=[];ops=[]
  elif op==b'n':pathpts=[];ops=[]
 return allpaths,float(p.mediabox.height)
def svg_groups(path):
 root=ET.fromstring(path.read_text());return root,{g.get('id'):g for g in root.iter(NS+'g') if g.get('id')}
def rectangles(p,r,name):
 root,groups=svg_groups(p/(name+'.svg'));H=float(root.get('height').removesuffix('pt'));found={}
 vals=r['primary']['costs'] if name=='costs' else r['primary']['raw_costs']
 if name=='costs':expected=['cost-whole-'+k for k in DOCS]+['cost-local-'+k for k in ['L050','A_L050','F017','A_F017']]
 else:expected=['cost-inventory-'+k for k in ROLES]
 need({k for k in groups if k.startswith('cost-')}==set(expected),'all actual bars')
 paths,ph=pdf_paths(p/(name+'.pdf'));need(near(H,ph),'same PDF figure extent')
 colored=[]
 for x in paths:
  if x['paint'] in ['f','f*','B','B*'] and x['fill'] and not all(near(v,1) for v in x['fill']) and x['ops']==['m','l','l','l']:colored.append(rect(x['points']))
 need(len(colored)==len(expected),'complete PDF colored rectangles')
 for key in expected:
  paths_svg=list(groups[key].iter(NS+'path'));need(len(paths_svg)==1,'one named bar path')
  d=paths_svg[0].get('d');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','closed SVG rectangle')
  b=rect(points(d));actual=(b[0],H-b[1]-b[3],b[2],b[3]);found[key]=actual
  match=[i for i,x in enumerate(colored) if all(near(q,v) for q,v in zip(x,actual))];need(len(match)==1,'matching actual PDF bar '+key);colored.pop(match[0])
  value=vals[key.split('-',2)[2]];need(value>0,'positive bar input')
 # Independently verify a common ratio in each panel and the declared zero baselines.
 if name=='costs':
  for stack in [['L050','F017'],['U_LCD','A_L050','A_F017']]:
   y=70
   for k in stack:
    b=found['cost-whole-'+k];need(near(b[1],y) and near(b[3],vals[k]*0.0016) and near(b[2],75),'whole stacked acquisition scale/baseline');y+=b[3]
  for k in ['L050','A_L050','F017','A_F017']:
   b=found['cost-local-'+k];need(near(b[1],70) and near(b[3],vals[k]*.004) and near(b[2],50),'conditional actual bar scale')
 else:
  for k in ROLES:
   b=found['cost-inventory-'+k];need(near(b[1],60) and near(b[3],vals[k]*.0012) and near(b[2],55),'inventory actual bar scale')
 # Numerical labels must actually be in the vector text, not just metadata.
 text=' '.join(t.text or '' for t in root.iter(NS+'text'))
 for k in vals:
  if any(x.endswith('-'+k) for x in expected):need(f'{vals[k]:,}' in text,'visible exact vector bar label')
 return len(expected)
def graph(p,r):
 g=read(p/'document_graph.json');nodes={n['id']:n for n in g['nodes']};edges={(e['source'],e['target']):e['kind'] for e in g['edges']}
 wanted={('L050','A_L050'):'correspondence',('F017','A_F017'):'correspondence',('U_LCD','A_L050'):'common',('U_LCD','A_F017'):'common',('required','U_LCD'):'declared_preacquisition',('retained','U_LCD'):'retained_acquisition',('optional','U_LCD'):'optional_check'}
 need(edges==wanted and len(g['edges'])==7,'exact directional dependency/correspondence boundaries')
 need(set(nodes)==set(DOCS+['required','retained','optional']) and g['not_a_theorem_DAG'] and g['node_counts_are_not_ratios'] and g['not_a_minimal_scientific_dependency_graph'] and g['no_sibling_application_dependency'] and not g['optional_checks_required'] and g['raw_and_manuscript_units_not_added'],'whole-document graph scope')
 for k in DOCS:need(nodes[k]['cost']==r['primary']['costs'][k],'whole document graph cost')
 raw=r['primary']['raw_costs'];need(nodes['required']['cost']==sum(raw[k] for k in ROLES[:4]) and nodes['retained']['cost'] is None and nodes['optional']['cost']==raw['optional_validation'],'separate required/optional/unknown graph costs')
 root,groups=svg_groups(p/'document_graph.svg');H=390
 need({k for k in groups if k.startswith('node-')}=={'node-'+k for k in nodes} and {k for k in groups if k.startswith('edge-')}=={'edge-'+a+'-'+b for a,b in edges},'all SVG boxes/arrows')
 boxes={}
 pdf,ph=pdf_paths(p/'document_graph.pdf');need(near(ph,H),'graph PDF scale');pboxes=[rect(x['points']) for x in pdf if x['paint']=='B' and x['ops']==['m','l','l','l']];shafts=[x for x in pdf if x['paint']=='S' and x['ops']==['m','c']];heads=[x for x in pdf if x['paint']=='B' and x['ops']==['m','l','l']]
 need(len(pboxes)==8 and len(shafts)==7 and len(heads)==7,'actual PDF boxes/arrows')
 for k,n in nodes.items():
  d=next(groups['node-'+k].iter(NS+'path')).get('d');b=rect(points(d));b=(b[0],H-b[1]-b[3],b[2],b[3]);boxes[k]=b
  need(any(all(near(a,c) for a,c in zip(b,x)) for x in pboxes),'actual PDF node box')
 for (src,dst),kind in edges.items():
  curves=list(groups['edge-'+src+'-'+dst].iter(NS+'path'));need(len(curves)==2,'SVG arrow shaft/head')
  ps=points(curves[0].get('d'));start=(ps[0][0],H-ps[0][1]);end=(ps[-1][0],H-ps[-1][1]);dashed=kind in ['correspondence','optional_check']
  need(point_dist(start,boxes[src])<4 and point_dist(end,boxes[dst])<4,'actual SVG arrow direction')
  need(('stroke-dasharray' in curves[0].get('style',''))==dashed,'optional/correspondence SVG style')
  candidates=[x for x in shafts if all(near(a,b) for a,b in zip(x['points'][0],start)) and all(near(a,b) for a,b in zip(x['points'][-1],end))];need(len(candidates)==1 and bool(candidates[0]['dash'])==dashed,'actual PDF arrow direction/style')
  ends=[x for x in heads if any(all(near(a,b) for a,b in zip(pt,end)) for pt in x['points'])];need(len(ends)==1,'actual arrowhead at target end')
  dx,dy=end[0]-start[0],end[1]-start[1]
  need(all((x-end[0])*dx+(y-end[1])*dy<1e-3 for x,y in ends[0]['points']),'arrowhead points forward')
 return {'nodes':8,'arrows':7,'SVG_and_PDF_direction_checked':True}
def check(p,r):
 return {'actual_SVG_bars':rectangles(p,r,'costs')+rectangles(p,r,'inventory'),'actual_PDF_bars':17,'graph':graph(p,r)}
