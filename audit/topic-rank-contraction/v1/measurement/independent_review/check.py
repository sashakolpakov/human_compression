#!/usr/bin/env python3
"""Independent integer/CSV/vector check. Imports no calculation-author module."""
import argparse, copy, csv, hashlib, json, math, re
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader

PIN = '7eb6e66ff1fdd291624a52ef86f2d54906c8a723aad6f9e6f99fbf9593782330'
def need(b, m):
    if not b: raise ValueError(m)
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(packet, data):
    a = read(packet/'inputs/author_counts.json')
    other = read(packet/'input_review/recount.json')
    need(a['documents'] == other['document_counts'], 'distinct input counts')
    expected = {}
    for v in ['raw_untrimmed', 'raw_selected', 'calibrated_selected']:
        for n in ['NFC', 'NFKC']:
            for unit in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:
                docs = {k:d['metrics'][v][n][unit] for k,d in a['documents'].items()}
                raw = {k:sum(d['metrics'][n][unit] for d in files.values()) for k,files in a['raw_files'].items()}
                expected[v,n,unit] = docs, raw
    actual = {(x['variant'],x['normalization'],x['unit']):x for x in data['coordinates']}
    need(len(actual) == len(data['coordinates']) == 30 and actual.keys() == expected.keys(), 'complete coordinate domain')
    for key,(d,raw) in expected.items():
        x = actual[key]; s,u,t,p = (d[k] for k in ['L037','U','A1','CODE'])
        need(x['document_costs'] == d and x['written_cost'] == u+t, 'whole written documents')
        need(x['printed_program_cost'] == p and x['raw_program_cost'] == raw['programs'], 'whole alternative program')
        need(x['driver_cost_separate'] == raw['drivers'] and x['formal_file_cost_separate'] == raw['formal'], 'separate inventories')
        need(x['conditional_acquisition'] == dict(whole_common=u,complete_printed_program_option=p,complete_raw_program_option=raw['programs'],printed_total=u+p,raw_total=u+raw['programs']), 'conditional acquisition')
        pairs = [(x['comparisons'][k],den) for k,den in [('written_papers',u+t),('including_printed_program',u+t+p),('including_raw_program_alternative',u+t+raw['programs'])]]+[(x['conditional_application'],t)]
        for f,den in pairs:
            g=math.gcd(s,den); rn,rd=s//g,den//g
            need(f == dict(numerator=s,denominator=den,reduced_numerator=rn,reduced_denominator=rd,exact_fraction=str(rn) if rd==1 else f'{rn}/{rd}',factor=s/den), 'exact integer fraction')
    need(data['primary'] == actual['raw_untrimmed','NFC','characters_without_whitespace'], 'raw primary')
    need(data['whole_common_charged_once'] and data['all_application_pages_charged'] and not data['old_Topic_B_common_free_premise'] and not data['cross_topic_discount'], 'common theory boundary')
    need(data['source_rows']==22 and data['proof_contexts']==20 and data['originals']==1, 'original versus clauses')
    for k in ['retained_external_proof_cost','full_graphic_layout_cost','historical_software_cost','full_formalization_cost','minimal_mathematical_complexity']:
        need(data[k] is None, 'unknown '+k)
    need(not data['programme_boundary']['full_source_formalized'] and data['programme_boundary']['scoped_declarations']==4 and data['new_question_credit']==0, 'formal and question limits')
    for v in ['raw_untrimmed','raw_selected','calibrated_selected']:
        for n in ['NFC','NFKC']:
            for k in ['written_papers','including_printed_program','including_raw_program_alternative']:
                fs=[c['comparisons'][k]['factor'] for key,c in actual.items() if key[:2]==(v,n)]
                need(data['sensitivity_ranges'][v][n][k]==dict(minimum=min(fs),maximum=max(fs)), 'sensitivity range')
    return actual

def csvs(packet, coords):
    counts={}
    for name,count in [('overall_costs',90),('conditional_costs',30),('document_costs',120),('software_costs',120)]:
        rows=list(csv.DictReader((packet/(name+'.csv')).open()))
        need(len(rows)==count, 'CSV row count'); seen=set()
        for row in rows:
            key=tuple(row[k] for k in ['variant','normalization','unit']); c=coords[key]
            if name=='overall_costs': label=row['comparison']; fields=c['comparisons'][label]
            elif name=='conditional_costs':
                label='application';fields=c['conditional_application']
                need(row['source']=='L037' and row['application']=='A1' and row['prepaid'].startswith('Acquire the entire local common paper U and the complete declared program'), 'conditional CSV scope')
            elif name=='document_costs': label=row['document'];fields={'cost':c['document_costs'][label]}
            else: label=row['role'];fields={'cost':c[label]}
            need(key+(label,) not in seen, 'duplicate CSV coordinate');seen.add(key+(label,))
            need(all(row[k]==str(v) for k,v in fields.items()), 'CSV complete value')
        counts[name]=count
    return counts

def vector_rectangles(packet):
    root=ET.parse(packet/'costs.svg').getroot(); ns={'s':'http://www.w3.org/2000/svg'}
    svg=[]; ticks=[]
    for g in root.findall('.//s:g',ns):
        ident=g.attrib.get('id','')
        if ident.startswith('xtick_'):
            path=g.find('.//s:path',ns)
            if path is not None:
                xy=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.attrib['d'])))
                ticks.append(xy[0])
        if not ident.startswith('patch_'): continue
        path=g.find('s:path',ns)
        if path is None:continue
        xy=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.attrib['d'])))
        if len(xy)!=8:continue
        x=xy[::2]; y=xy[1::2]
        if 10<max(y)-min(y)<30: svg.append([min(x),min(y),max(x)-min(x),max(y)-min(y)])
    need(len(ticks)>=3 and abs((ticks[2]-ticks[1])-(ticks[1]-ticks[0]))<2e-6,'uniform actual tick coordinates')
    origin=ticks[0]; scale=(ticks[1]-origin)/2500
    p=PdfReader(packet/'costs.pdf').pages[0]; pdf=[];poly=[]
    for a,o in p.get_contents().operations:
        if o==b'm': poly=[list(map(float,a))]
        elif o==b'l': poly.append(list(map(float,a)))
        elif o in [b'f',b'B']:
            if len(poly)==4:
                x,y=zip(*poly)
                if 10<max(y)-min(y)<30:pdf.append([min(x),float(p.mediabox.height)-max(y),max(x)-min(x),max(y)-min(y)])
            poly=[]
    need(len(svg)==len(pdf)==9,'nine actual data rectangles per vector format')
    expected=[[(0,15530)],[(0,6937),(6937,10555)],[(0,6937),(6937,10555),(17492,2925)],[(0,6937),(6937,10555),(17492,2501)]]
    for rows in [svg,pdf]:
        groups={}
        for x,y,w,h in rows:groups.setdefault(round(y,4),[]).append((x,w))
        need(len(groups)==4,'four vector cost rows')
        for (_,group),want in zip(sorted(groups.items()),expected):
            need(len(group)==len(want),'complete row components')
            for (x,w),(start,length) in zip(sorted(group),want):
                need(abs((x-origin)/scale-start)<.001 and abs(w/scale-length)<.001,'actual vector zero origin, width and stacking')
    need(all(all(abs(a-b)<2e-6 for a,b in zip(x,y)) for x,y in zip(sorted(svg),sorted(pdf))),'SVG/PDF geometric agreement')
    return {'SVG_rectangles':9,'PDF_rectangles':9,'bars':4,'actual_zero_origin':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'reviewed numerical edition')
    for e in read(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'immutable numerical export')
    data=read(a.packet/'results.json');coords=check(a.packet,data);counts=csvs(a.packet,coords);geometry=vector_rectangles(a.packet)
    controls=[]
    def reject(name,mutator):
        d=copy.deepcopy(data);mutator(d)
        try:check(a.packet,d)
        except (ValueError,KeyError):controls.append(name);return
        raise ValueError('accepted corruption '+name)
    reject('missing coordinate',lambda d:d['coordinates'].pop())
    reject('free common paper',lambda d:d['coordinates'][0]['comparisons']['written_papers'].__setitem__('denominator',1))
    reject('conditional acquisition missing code',lambda d:d['coordinates'][0]['conditional_acquisition'].__setitem__('raw_total',0))
    reject('wrong exact fraction',lambda d:d['coordinates'][0]['conditional_application'].__setitem__('exact_fraction','2'))
    reject('wrong raw code',lambda d:d['coordinates'][0].__setitem__('raw_program_cost',0))
    reject('free cross topic theory',lambda d:d.__setitem__('cross_topic_discount',True))
    reject('external cost zero',lambda d:d.__setitem__('retained_external_proof_cost',0))
    reject('promote Lean coverage',lambda d:d['programme_boundary'].__setitem__('full_source_formalized',True))
    reject('claim question solved',lambda d:d.__setitem__('new_question_credit',1))
    reject('wrong sensitivity range',lambda d:d['sensitivity_ranges']['raw_untrimmed']['NFC']['written_papers'].__setitem__('minimum',0))
    report=dict(status='PASS_DISTINCT_L037_NUMBERS',coordinates=30,exact_fractions=120,csv_rows=counts,geometry=geometry,independent_negative_controls=controls,primary=data['primary'],author_modules_imported=False,new_extraction=False,science_repeated=False)
    a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
