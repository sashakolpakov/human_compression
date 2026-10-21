import argparse, copy, csv, hashlib, itertools, json, re

from decimal import Decimal, localcontext

from fractions import Fraction

from pathlib import Path

import xml.etree.ElementTree as ET

from pypdf import PdfReader

from pypdf.generic import ContentStream

def need(ok, msg):
    if not ok: raise ValueError('DISTINCT_MEASUREMENT_REJECT: ' + msg)

def svg_check(data,expected):
    root=ET.fromstring(data); got={}
    for group in root.iter():
        if not group.get('id','').startswith('bar-'): continue
        path=next(x for x in group.iter() if x.tag.endswith('path'))
        nums=list(map(float,re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',path.get('d'))))
        need(len(nums)==8,'SVG rectangle')
        xs=nums[::2]; ys=nums[1::2]
        need(len(set(xs))==len(set(ys))==2,'axis-aligned SVG rectangle')
        got[group.get('id')]=(max(ys)-min(ys),max(ys))
    need(set(got)=={x[0] for x in expected},'SVG completeness')
    scale=got[expected[0][0]][0]/expected[0][2]; base=got[expected[0][0]][1]
    for gid,_,cost,bottom in expected:
        height,low=got[gid]
        need(abs(height-scale*cost)<2e-5 and abs(base-low-scale*bottom)<2e-5,'SVG heights and stacking')
    return len(got)

def pdf_check(path,expected):
    colors={tuple(round(x/255,6) for x in rgb):role for rgb,role in
            [((98,108,118),'source'),((66,107,154),'common'),((112,165,154),'application'),((189,135,78),'program')]}
    reader=PdfReader(path); need(len(reader.pages)==1,'one plot page')
    rgb=None; stack=[]; pts=[]; got=[]
    for args,op in ContentStream(reader.pages[0].get_contents(),reader).operations:
        if op==b'q': stack.append(rgb)
        elif op==b'Q': rgb=stack.pop()
        elif op==b'rg': rgb=tuple(round(float(x),6) for x in args)
        elif op==b'g': rgb=(round(float(args[0]),6),)*3
        elif op==b'm': pts=[tuple(map(float,args))]
        elif op==b'l': pts.append(tuple(map(float,args)))
        elif op in [b'f',b'f*',b'B',b'B*']:
            if rgb in colors and len(pts)==4:
                xs={x for x,y in pts};ys={y for x,y in pts}
                need(len(xs)==len(ys)==2,'PDF rectangle')
                got.append((colors[rgb],max(ys)-min(ys),min(ys)))
            pts=[]
    need(len(got)==len(expected)+4 and [x[0] for x in got[-4:]]==['source','common','application','program'] and
         all(abs(x[1]-5.6)<1e-6 for x in got[-4:]),'four separately identified legend swatches')
    got=got[:-4];scale=got[0][1]/expected[0][2];base=got[0][2]
    for (role,h,low),(_,want,cost,bottom) in zip(got,expected):
        need(role==want and abs(h-scale*cost)<2e-5 and abs(low-base-scale*bottom)<2e-5,'PDF heights and stacking')
    return len(got)
