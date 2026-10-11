#!/usr/bin/env python3
"""Author checks of admitted values, exported tables, actual SVG/PDF bars and scope."""
from pathlib import Path
import argparse, copy, hashlib, json, re, xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
import build

NS={'s':'http://www.w3.org/2000/svg'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def near(a,b):return abs(a-b)<0.000003
def expected_geometry(spec):
    whole=spec['kind']=='whole_topics';W=734.4;H=576 if whole else 619.2
    left=.37 if whole else .34;maxcost=max(max(r['source'],sum(x['cost'] for x in r['segments'])) for r in spec['rows'])
    sx=W*(.91-left)/(maxcost*1.13);length=len(spec['rows'])-.43;sy=H*.86/(length*1.1);ymin=-.285-.05*length
    result={}
    for i,r in enumerate(spec['rows']):
        result['bar-'+r['id']+'-source']=[W*left,H*.06+(i-.285-ymin)*sy,r['source']*sx,.25*sy]
        start=0
        for p in r['segments']:
            result['bar-'+r['id']+'-'+p['id']]=[W*left+start*sx,H*.06+(i+.035-ymin)*sy,p['cost']*sx,.25*sy];start+=p['cost']
    return result,H

def svg_rectangles(raw):
    root=ET.fromstring(raw);result={}
    for g in root.findall('.//s:g',NS):
        gid=g.get('id','')
        if not gid.startswith('bar-'):continue
        need(gid not in result,'duplicate bar id');paths=g.findall('s:path',NS);need(len(paths)==1,'one path per bar')
        s=paths[0].get('d','');need(re.sub(r'[-+\d.eE\s]','',s)=='MLLLz','bar must be literal rectangle')
        a=[float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
        need(len(a)==8 and near(a[1],a[3]) and near(a[2],a[4]) and near(a[5],a[7]) and near(a[6],a[0]),'rectangle coordinates')
        result[gid]=[a[0],a[1],a[2]-a[0],a[5]-a[1]]
    return result

def compare_geometry(actual,expected):
    need(set(actual)==set(expected),'bar identities/count differ')
    for key,value in expected.items():need(all(near(a,b) for a,b in zip(actual[key],value)),'bar geometry '+key)

def pdf_rectangles(path):
    p=PdfReader(path).pages[0];need(len(PdfReader(path).pages)==1,'one-page graph')
    color=None;stack=[];points=[];rows=[]
    allowed=[(52/255,67/255,84/255),(40/255,110/255,153/255),(129/255,189/255,176/255),(97/255,162/255,148/255)]
    for args,op in ContentStream(p.get_contents(),p.pdf).operations:
        if op==b'q':stack.append(color)
        elif op==b'Q':color=stack.pop()
        elif op==b'rg':color=tuple(float(x) for x in args)
        elif op==b'm':points=[tuple(float(x) for x in args)]
        elif op==b'l':points.append(tuple(float(x) for x in args))
        elif op==b're':points=[]
        elif op in [b'f',b'B',b'f*',b'B*']:
            if len(points)==4 and color is not None and any(all(near(a,b) for a,b in zip(color,c)) for c in allowed):
                x0,y0=points[0];x1,y1=points[1];x2,y2=points[2];x3,y3=points[3]
                if near(y0,y1) and near(x1,x2) and near(y2,y3) and near(x0,x3):rows.append([min(x0,x1),min(y0,y2),abs(x1-x0),abs(y2-y0)])
            points=[]
        elif op in [b'n',b'S']:points=[]
    return rows,float(p.mediabox.height)

def compare_pdf(rects,H,expected,legend_count):
    unused=list(rects)
    for k,(x,y,w,h) in expected.items():
        target=[x,H-y-h,w,h];matches=[i for i,a in enumerate(unused) if all(near(u,v) for u,v in zip(a,target))]
        need(len(matches)==1,'missing/distorted PDF bar '+k);unused.pop(matches[0])
    need(len(unused)==legend_count,'extra colored PDF rectangles')
