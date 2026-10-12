#!/usr/bin/env python3
"""Read actual vector rectangles; derive their dimensions from accepted costs.
Adapted low-level SVG/PDF parsing from the prior distinct overview/Mix review.
No numerical-author plotting or transform helper is imported.
"""
import re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
from derive import need
NS={'s':'http://www.w3.org/2000/svg'}
ROLES=['required_finite_certificate','required_graph_data','optional_validation','current_orchestration_driver','partial_formal_evidence']
def close(a,b):return abs(a-b)<3e-6
def svg(raw):
    root=ET.fromstring(raw);out={}
    for g in root.findall('.//s:g',NS):
        name=g.get('id','')
        if not name.startswith('cost-'):continue
        p=g.findall('s:path',NS);need(name not in out and len(p)==1,'one unique cost rectangle');d=p[0].get('d','');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','literal SVG cost rectangle');v=list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',d)));need(len(v)==8 and close(v[1],v[3])and close(v[2],v[4])and close(v[5],v[7])and close(v[6],v[0]),'four rectangle corners');out[name]=[min(v[0],v[2]),min(v[1],v[5]),abs(v[2]-v[0]),abs(v[5]-v[1])]
    return out

def pdf(path):
    reader=PdfReader(path);need(len(reader.pages)==1,'one-page chart');p=reader.pages[0];H=float(p.mediabox.height);W=float(p.mediabox.width);color=None;stack=[];points=[];out=[]
    for args,op in ContentStream(p.get_contents(),reader).operations:
        if op==b'q':stack.append(color)
        elif op==b'Q':color=stack.pop()
        elif op==b'rg':color=tuple(map(float,args))
        elif op==b'g':color=(float(args[0]),)*3
        elif op==b'm':points=[tuple(map(float,args))]
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op==b're':points=[]
        elif op in (b'f',b'f*',b'B',b'B*'):
            if len(points)==4 and color and not all(close(x,1)for x in color)and max(color)-min(color)>.02:
                x,y=zip(*points);need(close(y[0],y[1])and close(x[1],x[2])and close(y[2],y[3])and close(x[3],x[0]),'literal PDF rectangle');out.append([min(x),H-max(y),max(x)-min(x),max(y)-min(y)])
            points=[]
        elif op in (b'n',b'S'):points=[]
    return W,H,out

def expected(oracle,name):
    d=oracle['primary']['documents'];raw=next(x['whole_role_counts']for x in oracle['raw_inventory']if x['normalization']=='NFC'and x['unit']=='characters_without_whitespace');out={}
    if name=='costs':
        W,H=792,300
        for x,keys in [(65,['F010','L126']),(180,['U_R','R1','R2'])]:
            y=70
            for key in keys:
                height=d[key]/500;out['cost-whole-'+key]=[x,H-y-height,60,height];y+=height
        for i,key in enumerate(['F010','R1','L126','R2']):
            height=d[key]*9/2000;out['cost-local-'+key]=[390+80*i,H-70-height,46,height]
    else:
        W,H=792,265
        for i,key in enumerate(['CODE']+ROLES):
            value=d['CODE']if key=='CODE'else raw[key];height=value*11/2500;out['cost-inventory-'+key]=[52+125*i,H-65-height,62,height]
    return W,H,out

def compare(a,b):
    need(set(a)==set(b),'actual full bar identities')
    for k,v in b.items():need(all(close(x,y)for x,y in zip(a[k],v)),'actual bar dimension '+k)

def run(packet,oracle):
    records={}
    for name in ['costs','inventory']:
        W,H,want=expected(oracle,name);actual=svg((packet/(name+'.svg')).read_text());compare(actual,want);w,h,rows=pdf(packet/(name+'.pdf'));need((w,h)==(W,H),'whole chart canvas');need(len(rows)==len(want),'actual PDF bar count')
        for key,target in want.items():
            found=[i for i,row in enumerate(rows)if all(close(a,b)for a,b in zip(row,target))];need(len(found)==1,'actual PDF bar '+key);rows.pop(found[0])
        records[name]=dict(bars=len(want),canvas=[W,H],actual_dimensions=actual)
    return records
