#!/usr/bin/env python3
"""Author controls for the consolidated reader; independent numerical review is separate."""
import argparse, copy, csv, hashlib, io, json, re, tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
import build

HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise ValueError(msg)

def graph_check(text,result,conditional):
    root=ET.fromstring(text);bars={x.attrib['id']:x for x in root.iter() if x.get('id','').startswith('bar-')}
    rows=[(t,q) for t in result['topics'] for q in t['pairs']] if conditional else [(t,None) for t in result['topics']]
    maxcost=max(max(q['source_cost'],q['application_cost']) if q else max(t['source_sum'],t['written_denominator']) for t,q in rows)
    expected={};factor=720/maxcost
    for i,(t,q) in enumerate(rows):
        y=60+i*(36 if conditional else 57);prefix=f"bar-{t['topic']}-{q['source']+'-' if q else ''}"
        expected[prefix+'source']=(q['source_cost'] if q else t['source_sum'],170,y)
        if q: expected[prefix+'application']=(q['application_cost'],170,y+13)
        else:
            expected[prefix+'common']=(t['common_theory'],170,y+17)
            expected[prefix+'applications']=(t['applications_sum'],170+t['common_theory']*factor,y+17)
    need(set(bars)==set(expected),'actual SVG bar inventory')
    for k,(cost,x,y) in expected.items():
        b=bars[k];need(int(b.get('data-cost'))==cost,'actual SVG cost')
        need(abs(float(b.get('width'))-cost*factor)<1e-7,'actual SVG width')
        need(abs(float(b.get('x'))-x)<1e-7 and float(b.get('y'))==y,'actual SVG position')
        need(float(b.get('height'))==10,'actual SVG height')
    return len(bars)

def pdf_polygons(path):
    reader=PdfReader(path);page=reader.pages[0];pathpts=[];polygons=[]
    for args,op in ContentStream(page.get_contents(),reader).operations:
        if op==b'm': pathpts=[tuple(float(z) for z in args)]
        elif op==b'l': pathpts.append(tuple(float(z) for z in args))
        elif op==b'f':
            if len(pathpts)==4:polygons.append(pathpts)
            pathpts=[]
    return polygons,float(page.mediabox.height)

def pdf_geometry_check(polygons,height,svg):
    expected=[]
    for el in ET.fromstring(svg):
        if el.get('id','').startswith('bar-'):
            x,y,w,h=(float(el.get(k)) for k in ['x','y','width','height'])
            expected.append([(x,height-y),(x+w,height-y),(x+w,height-y-h),(x,height-y-h)])
    actual=[p for p in polygons if p[0][0]>=170 and height-p[0][1]>=60 and abs(p[0][1]-p[2][1]-10)<1e-6]
    need(len(actual)==len(expected),'actual PDF bar count')
    for actualp,expectedp in zip(actual,expected):
        need(all(abs(a-e)<1e-5 for ap,ep in zip(actualp,expectedp) for a,e in zip(ap,ep)),'actual PDF bar geometry')
    return len(actual)

def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'));p.add_argument('--study-root',type=Path,default=Path('/Users/sasha/medusa/research/leemans'));p.add_argument('--locations',type=Path);p.add_argument('--packet',type=Path,default=HERE);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    spec=json.loads((HERE/'inputs.json').read_text());data=build.load_inputs(spec,a.public_root,a.study_root,None if a.locations is None else json.loads(a.locations.read_text()))
    expected=build.make(data);actual=json.loads((a.packet/'results.json').read_text())
    def validate(x):
        build.validate(x);need(x==expected,'pinned accepted input comparison')
    validate(actual)
    with tempfile.TemporaryDirectory() as td:
        build.write_csv(Path(td),expected)
        for f in ['topics.csv','applications.csv']:
            need((Path(td)/f).read_bytes()==(a.packet/f).read_bytes(),'CSV '+f)
    need((a.packet/'summary.tex').read_text()==build.tex(expected),'complete generated TeX')
    graphs=[('whole_topics.svg',False),('conditional_applications.svg',True)]
    bars=sum(graph_check((a.packet/f).read_text(),expected,c) for f,c in graphs)
    pdf_data=[]
    for f,c in graphs:
        polys,h=pdf_polygons(a.packet/f.replace('.svg','.pdf'))
        pdf_geometry_check(polys,h,(a.packet/f).read_text());pdf_data.append((polys,h,f))
    pages=PdfReader(a.packet/'summary.pdf').pages;need(len(pages)==5,'reader page count')
    texts=[x.extract_text() for x in pages];full=' '.join(texts)
    need('27 distinct original manuscripts' in full and '161-item' in full and 'F015' in full and 'L028' in full,'reader scope')
    need('untrimmed' in full and '0.970886' in full,'reader representation limitations')
    for t in expected['topics']:
        for val in [t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator']]:
            need(f'{val:,}' in texts[0],'reader complete cost')
        for q in t['pairs']:
            for token in [q['source'],q['application'],f"{q['source_cost']:,}",f"{q['application_cost']:,}",f"{float(q['conditional']['decimal']):.3f}"]:
                need(token in texts[3],'reader conditional cost')
    for c in full:
        need(ord(c)>=32 or c in '\n\t\r','PDF control glyph')
    controls=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError): controls.append({'name':name,'rejected':True});return
        raise ValueError('control admitted: '+name)
    def change(name,mut):
        x=copy.deepcopy(actual);mut(x);reject(name,lambda:validate(x))
    change('drop full common cost',lambda x:x['topics'][0].__setitem__('common_theory',0))
    change('drop an application',lambda x:x['topics'][0]['pairs'].pop())
    change('duplicate original identifier',lambda x:x['topics'][1]['pairs'][0].__setitem__('source','L032'))
    change('unknown historical software counted zero',lambda x:x['topics'][0].__setitem__('historical_software_cost',0))
    change('pooled cross-topic factor',lambda x:x.__setitem__('pooled_factor',2))
    change('cross-topic common discount',lambda x:x.__setitem__('cross_topic_deduplication',True))
    change('all161 completed overclaim',lambda x:x.__setitem__('all_registry_manuscripts_completed',True))
    change('replace B rendered boundary by calibrated PDF',lambda x:x['topics'][1].__setitem__('representation','calibrated_selected_pdf'))
    change('partial common prepayment',lambda x:x['topics'][0]['conditional_prepaid'].__setitem__('full_common',1))
    change('drop complete required program',lambda x:x['topics'][2].__setitem__('printed_program_cost',0))
    change('charge raw and printed together',lambda x:x['topics'][0].__setitem__('including_raw_programs',build.ratio(x['topics'][0]['source_sum'],x['topics'][0]['written_denominator']+x['topics'][0]['raw_program_alternative']+x['topics'][0]['printed_program_cost'])))
    change('invent E raw alternative',lambda x:x['topics'][4].__setitem__('raw_program_alternative',0))
    change('inflate original manuscript count',lambda x:x.__setitem__('original_manuscript_count',161))
    change('new source credit',lambda x:x.__setitem__('new_source_credit',1))
    for stem,cond in graphs:
        original=(a.packet/stem).read_text()
        for kind in ['width','x','delete']:
            r=ET.fromstring(original);el=next(z for z in r if z.get('id','').startswith('bar-'))
            if kind=='delete':r.remove(el)
            else:el.set(kind,str(float(el.get(kind))+7))
            bad=ET.tostring(r,encoding='unicode')
            reject(stem+' actual '+kind,lambda:graph_check(bad,expected,cond))
    for polys,h,stem in pdf_data:
        bad=copy.deepcopy(polys)
        bar=next(p for p in bad if p[0][0]>=170 and h-p[0][1]>=60 and abs(p[0][1]-p[2][1]-10)<1e-6)
        bar[1]=(bar[1][0]+13,bar[1][1])
        reject(stem+' PDF width distortion',lambda:pdf_geometry_check(bad,h,(a.packet/stem).read_text()))
    report=dict(status='PASS_AUTHOR_CONSOLIDATION_CHECK',input_pins=len(spec['bindings']),topics=10,distinct_originals=27,
        written_fractions=10,conditional_fractions=27,printed_program_fractions=10,raw_alternative_fractions=9,
        optional_validation_fractions=1,actual_svg_bars=bars,actual_pdf_bars=bars,reader_pages=5,controls=controls,
        source_reextraction=False,scientific_proof_replay=False,independent_numeric_review=False,
        results_sha256=hashlib.sha256((a.packet/'results.json').read_bytes()).hexdigest())
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 20 input pins, 57 exact displayed fractions, 84 actual bars, 5 reader pages, '+str(len(controls))+' controls')

if __name__=='__main__':main()
