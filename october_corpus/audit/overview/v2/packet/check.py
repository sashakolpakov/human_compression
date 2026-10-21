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

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh report path')
    own=Path(__file__).resolve().parent
    if (own/'manifest.json').exists():
        for b in json.loads((own/'manifest.json').read_text())['exports']:
            p=own/b['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==b['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==b['sha256'],'frozen export '+b['path'])
    protocol,data=build.load_inputs(a.public_root);expected=build.make(data,protocol)
    r=json.loads((a.packet/'results.json').read_text());build.validate(r);need(r==expected,'generated admitted data equality')
    for name,value in build.csv_text(r).items():need((a.packet/name).read_text()==value,'CSV '+name)
    need((a.packet/'summary.tex').read_text()==build.tex(r),'full reader source')
    specs={k:build.plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']}
    need(json.loads((a.packet/'plot_data.json').read_text())==specs,'plot ownership/cost table')
    svg_total=pdf_total=0;geometry={};pdfs={}
    for k,s in specs.items():
        geom,H=expected_geometry(s);geometry[k]=geom
        actual=svg_rectangles((a.packet/(k+'.svg')).read_bytes());compare_geometry(actual,geom);svg_total+=len(actual)
        rects,height=pdf_rectangles(a.packet/(k+'.pdf'));need(near(H,height),'graph dimensions');pdfs[k]=(rects,height)
        compare_pdf(rects,H,geom,3 if k=='whole_topics' else 2);pdf_total+=len(geom)
    doc=PdfReader(a.packet/'summary.pdf');need(len(doc.pages)==6,'complete six-page reader')
    text='\n'.join(p.extract_text() or '' for p in doc.pages)
    for token in ['N006','unmeasured','N007','thirty-three','raw','common','programs']:need(token in text,'reader scope '+token)
    need('\ufffd' not in text and not any(ord(c)<32 and c not in '\n\t\r' for c in text),'reader extraction controls')
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError):controls.append({'name':name,'rejected':True})
        else:raise ValueError('negative control accepted: '+name)
    for name,mut in [
       ('cross_topic_discount',lambda x:x.update(cross_topic_deduplication=True)),
       ('pooled_factor',lambda x:x.update(pooled_factor=1.2)),
       ('registry_completed',lambda x:x.update(all_registry_manuscripts_completed=True)),
       ('new_source_credit',lambda x:x.update(new_source_credit=1)),
       ('N006_borrowed_factor',lambda x:x['unmeasured'][0].update(whole_factor=1.00655)),
       ('N006_zero_cost',lambda x:x['unmeasured'][0].update(source_cost=0)),
       ('common_component_omitted',lambda x:x['topics'][1]['common_components'].pop('U_B_high_rank')),
       ('C_incidence_note_omitted',lambda x:x['topics'][2]['common_components'].pop('U_C_INC')),
       ('conditional_partial_acquisition',lambda x:x['topics'][1]['conditional_prepaid'].update(full_common=14124)),
       ('external_cost_zero',lambda x:x['topics'][0].update(external_proof_cost=0)),
       ('B_PDF_representation_substitution',lambda x:x['topics'][1].update(representation='calibrated_selected_pdf')),
       ('raw_plus_printed',lambda x:x['topics'][0].update(including_raw_programs=build.ratio(x['topics'][0]['source_sum'],x['topics'][0]['written_denominator']+x['topics'][0]['raw_program_alternative']+x['topics'][0]['printed_program_cost']))),
       ('pruned_complete_code',lambda x:x['topics'][1].update(printed_program_cost=0)),
       ('duplicate_source',lambda x:x['topics'][0]['pairs'][0].update(source='L034')),
       ('missing_application',lambda x:x['topics'][0]['pairs'].pop()),
       ('E_raw_invented',lambda x:x['topics'][4].update(raw_program_alternative=1)),
       ('E_optional_pruned',lambda x:x['topics'][4].update(optional_validation_printed=0))]:
        bad=copy.deepcopy(r);mut(bad);reject(name,lambda:build.validate(bad))
    g=copy.deepcopy(geometry['whole_topics']);key=next(iter(g));g[key][2]+=1
    reject('SVG_distorted_width',lambda:compare_geometry(g,geometry['whole_topics']))
    g=copy.deepcopy(geometry['conditional_1']);g.pop(next(iter(g)))
    reject('SVG_missing_application',lambda:compare_geometry(g,geometry['conditional_1']))
    rects,H=copy.deepcopy(pdfs['whole_topics']);rects[0][2]+=1
    reject('PDF_distorted_width',lambda:compare_pdf(rects,H,geometry['whole_topics'],3))
    rects,H=copy.deepcopy(pdfs['conditional_2']);rects.pop(0)
    reject('PDF_missing_bar',lambda:compare_pdf(rects,H,geometry['conditional_2'],2))
    report={'status':'PASS','input_bindings':len(protocol['bindings']),'topics':13,'distinct_originals':33,
            'exact_primary_comparisons':72,'SVG_bars':svg_total,'PDF_bars':pdf_total,'complete_common_segments':15,
            'complete_application_segments':33,'reader_pages':6,'reader_text_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'semantic_controls':controls,'independent_review':False,'no_primary_extraction':True,'no_scientific_replay':True}
    build.dump(a.out,report);print(json.dumps(report))

if __name__=='__main__':main()
