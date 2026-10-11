#!/usr/bin/env python3
"""Independent arithmetic from the earlier independent recount, plus actual plots."""
import argparse, copy, csv, hashlib, itertools, json, re
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

def need(ok, msg):
    if not ok: raise ValueError('DISTINCT_MEASUREMENT_REJECT: ' + msg)

IDS = {'Diagonal': ['N007','U','A1','CODE']}
PROGRAMS = {'Diagonal': ['papers/topic-diagonal/v1/programs/diagonal_models.g']}
V = ['raw_untrimmed','raw_selected','calibrated_selected']
N = ['NFC','NFKC']
U = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
     'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']

def arithmetic(result, recount):
    need(result['original_manuscripts']==1 and result['source_ids']==['N007'] and result['independent_topics']==1, 'one original')
    need(all(v is None for v in result['unknown_costs'].values()), 'unpriced costs')
    need(not result['full_formalization_claim'] and result['new_source_credit']==result['new_question_credit']==0, 'credit')
    keys = list(itertools.product(IDS,V,N,U))
    rows = {(r['topic'],r['variant'],r['normalization'],r['unit']):r for r in result['rows']}
    need(len(rows)==len(result['rows'])==30 and set(rows)==set(keys), 'all coordinates exactly once')
    fractions = {}
    for t,v,n,u in keys:
        r=rows[t,v,n,u]; s,c,a,p=[recount['documents'][k][v][n][u] for k in IDS[t]]
        raw=sum(recount['raw_files'][k][n][u] for k in PROGRAMS[t])
        need(r['source_id']==IDS[t][0] and r['document_costs']==dict(source=s,common=c,application=a,program=p), 'complete document costs')
        need(r['written_denominator']==c+a, 'full common acquisition')
        expected_raw={
            'programs':raw,
            'drivers':sum(recount['raw_files'][k][n][u] for k in ['papers/topic-diagonal/v1/check.py','papers/topic-diagonal/v1/build.py']),
            'formal':sum(recount['raw_files'][k][n][u] for k in recount['raw_files'] if k.endswith('.lean'))}
        need(r['raw_costs']==expected_raw, 'all raw inventories')
        acq=r['conditional_acquisition']
        need(acq['whole_common_cost']==c and acq['whole_printed_program_cost']==p and
             acq['whole_raw_program_cost']==raw and acq['printed_and_raw_are_alternatives'], 'conditional boundary')
        for name,d in [('written',c+a),('including_printed_programs',c+a+p),
                       ('including_raw_programs',c+a+raw),('conditional_application',a)]:
            q=r['comparisons'][name]; f=Fraction(s,d)
            with localcontext() as ctx:
                ctx.prec=40; dec=str(Decimal(s)/Decimal(d))
            need(q==dict(numerator=s,denominator=d,reduced_numerator=f.numerator,
                         reduced_denominator=f.denominator,decimal=dec),'exact fraction')
            fractions[(t,IDS[t][0],v,n,u,name)]=(s,d,dec)
    need(len(fractions)==120,'all fractions')
    for t in IDS:
        need(result['primary'][t]==rows[t,V[2],N[0],U[2]],'primary coordinate')
    return fractions

def bars(recount):
    expected=[]
    for topic,ids in IDS.items():
        s,c,a,p=[recount['documents'][k][V[2]][N[0]][U[2]] for k in ids]
        for suffix,role,cost,bottom in [('source','source',s,0),('common-written','common',c,0),
                 ('application-written','application',a,c),('common-printed','common',c,0),
                 ('application-printed','application',a,c),('program','program',p,c+a)]:
            expected.append(('bar-'+topic+'-'+suffix,role,cost,bottom))
    return expected

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
    need(len(got)==10 and [x[0] for x in got[-4:]]==['source','common','application','program'] and
         all(abs(x[1]-5.6)<1e-6 for x in got[-4:]),'four separately identified legend swatches')
    got=got[:-4];scale=got[0][1]/expected[0][2];base=got[0][2]
    for (role,h,low),(_,want,cost,bottom) in zip(got,expected):
        need(role==want and abs(h-scale*cost)<2e-5 and abs(low-base-scale*bottom)<2e-5,'PDF heights and stacking')
    return len(got)

def main():
    ap=argparse.ArgumentParser()
    for name in ['author','recount','out']:ap.add_argument('--'+name,type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    need(hashlib.sha256((a.author/'manifest.json').read_bytes()).hexdigest()=='fb42a35d96275d9cef80312b2184d60202e4e5d3e1c1ae6a51200afb1e871af0','author edition')
    for row in json.loads((a.author/'manifest.json').read_text())['exports']:
        b=(a.author/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'author export')
    need(hashlib.sha256(a.recount.read_bytes()).hexdigest()=='7409bb8556ddc2680ebf5c5abb7f573b7ba0083cd0086a354ed89009f43985b4','independent input recount')
    recount=json.loads(a.recount.read_text());result=json.loads((a.author/'results.json').read_text());values=arithmetic(result,recount)
    csvrows=list(csv.DictReader((a.author/'comparisons.csv').open()))
    seen={}
    for row in csvrows:
        k=tuple(row[x] for x in ['topic','source','variant','normalization','unit','comparison'])
        need(k not in seen,'no repeated CSV row');seen[k]=(int(row['numerator']),int(row['denominator']),row['decimal'])
    need(seen==values,'all CSV fractions')
    expected=bars(recount);svg=(a.author/'whole_costs.svg').read_bytes()
    sg=svg_check(svg,expected);pg=pdf_check(a.author/'whole_costs.pdf',expected)
    controls=[]
    for label,change in [('common omitted',lambda x:x['rows'][0]['document_costs'].update(common=0)),
                          ('factor changed',lambda x:x['rows'][0]['comparisons']['written'].update(denominator=1)),
                          ('graphics zero',lambda x:x['unknown_costs'].update(graphics=0)),
                          ('clause count as originals',lambda x:x.update(original_manuscripts=64))]:
        wrong=copy.deepcopy(result);change(wrong)
        try:arithmetic(wrong,recount)
        except ValueError:controls.append(label)
        else:raise ValueError('accepted invalid control')
    wrong=ET.fromstring(svg)
    for group in wrong.iter():
        if group.get('id')=='bar-Diagonal-common-written':
            path=next(x for x in group.iter() if x.tag.endswith('path'));path.set('d','M 0 0 L 1 0 L 1 1 L 0 1 z')
    try:svg_check(ET.tostring(wrong),expected)
    except ValueError:controls.append('actual bar distorted')
    else:raise ValueError('accepted invalid graph')
    text='\n'.join(p.extract_text() or '' for p in PdfReader(a.author/'measurement.pdf').pages)
    for t in IDS:
        for q in result['primary'][t]['comparisons'].values():need(f"{float(q['decimal']):.3f}" in text,'displayed rounded factor')
    report=dict(status='PASS_DISTINCT_ARITHMETIC_AND_GRAPH_REVIEW',exact_fractions=120,csv_rows=120,
                actual_svg_bars=sg,actual_pdf_bars=pg,stacking_checked=True,controls_rejected=controls,
                primary=result['primary'],scientific_replay=False,source_reextraction=False,
                new_source_credit=0,new_question_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))

if __name__=='__main__':main()
