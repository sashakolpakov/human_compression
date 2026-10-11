#!/usr/bin/env python3
"""Distinct arithmetic, CSV and actual vector-geometry review of Diagonal v2."""
from pathlib import Path
import argparse, copy, csv, hashlib, itertools, json, math, re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='53bfa0d55a9c834014f53a74798cee0b9e65ed1f7a42b184891889362a172fce'
INPUT='4e7991712d5e186c5d0eca9a8173f245a2d1a584eadb1187ef952cef48caec04'
REVIEW='aaba6c23e49f13b3a761fde6c0fac4c5ff1d91c2ba8659488a8881eda3446381'
COLORS=['#738799','#397c86','#b68145']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(ok,msg):
    if not ok:raise ValueError('DISTINCT_DIAGONAL_REJECT: '+msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def manifest(root,pin):
    need(sha((root/'manifest.json').read_bytes())==pin,'frozen manifest')
    for row in load(root/'manifest.json')['exports']:
        p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'relative export')
        data=(root/p).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'whole frozen export')
def fraction(n,d):
    need(n>0 and d>0,'positive costs');g=math.gcd(n,d)
    order=len(str(n))-len(str(d))
    if (n<d*10**order if order>=0 else n*10**(-order)<d):order-=1
    places=41-order;q,r=divmod(n*10**places,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    digits=str(q).rjust(places+1,'0')
    dec=digits[:-places]+'.'+digits[-places:]
    return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=dec)
def derive(packet):
    counts=load(packet/'inputs/author_counts.json');audit=load(packet/'input_review/recount.json')
    need(audit['documents']=={k:r['metrics'] for k,r in counts['documents'].items()},'accepted distinct PDF costs')
    need(audit['text_only_sensitivity']=={k:r['metrics'] for k,r in counts['text_only_sensitivity'].items()},'accepted distinct text-only costs')
    need(audit['raw_files']=={k:r['metrics'] for rows in counts['raw_files'].values() for k,r in rows.items()},'accepted distinct full raw files')
    need([len(counts['raw_files'][k]) for k in ['programs','required_drivers','drivers','formal']]==[19,2,4,3],'all declared files')
    rows=[]
    for v,n,u in itertools.product(['raw_untrimmed','raw_selected','calibrated_selected','text_only_sensitivity'],['NFC','NFKC'],UNITS):
        doc={k:(audit['text_only_sensitivity'][k][n][u] if v=='text_only_sensitivity' else metrics[v][n][u]) for k,metrics in audit['documents'].items()}
        file={cat:{p:audit['raw_files'][p][n][u] for p in vals} for cat,vals in counts['raw_files'].items()}
        sources={k:doc[k] for k in ['N007','N006']};apps={'N007':doc['A1'],'N006':doc['A2']+doc['A2nine']+doc['A2HN']}
        numerator=sum(sources.values());written=doc['U']+sum(apps.values());program=sum(file['programs'].values());decoders=sum(file['required_drivers'].values())
        rows.append(dict(variant=v,normalization=n,unit=u,original_costs=sources,source_sum=numerator,document_costs=doc,common_theory=doc['U'],
          application_costs=apps,all_applications=sum(apps.values()),written_denominator=written,whole_program_cost=program,required_decoder_cost=decoders,
          whole_software_cost=program+decoders,program_inclusive_denominator=written+program+decoders,complete_printed_program_denominator=None,
          old_single_printed_validation_cost=doc['CODEold'],raw_file_costs=file,operational_driver_cost=sum(file['drivers'].values()),partial_formal_cost=sum(file['formal'].values()),
          whole={'written':fraction(numerator,written),'including_whole_raw_software':fraction(numerator,written+program+decoders)},
          conditional={k:fraction(sources[k],apps[k]) for k in sources}))
    return rows,counts
def validate(data,rows):
    need(data['rows']==rows,'all40 complete coordinates and160 fractions')
    primary=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
    need(data['primary']==primary,'complete primary row')
    need(data['originals']==['N007','N006'] and data['source_rows']=={'N007':32,'N006':27},'unchanged two-original contract')
    need([data[k] for k in ['ordinary_coordinates','text_only_coordinates','exact_whole_fractions','exact_conditional_fractions','total_exact_fractions']]==[30,10,80,80,160],'all coordinates counted')
    need(data['complete_printed_program_alternative'] is None and data['source_exceptions_outside_this_edition']==['Fi22','Fi24prime'],'no fictitious printed route or imported exceptions')
    need(data['external_bytes']==dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249,not_character_counts=True,full_runtime_cost=None,proof_cost=None),'separate inherited external bytes, unknown full costs')
    need(data['unknown_costs']==dict(retained_classification_proofs=None,source_historical_software=None,full_graphics=None,full_formalization=None),'unknowns not zero')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no scientific credit')
    need('Whole enlarged U' in data['conditional_acquisition'] and 'both required decoding drivers' in data['conditional_acquisition'],'full acquisition declared')
    return primary
def csvs(packet,rows,counts):
    def read(name):return list(csv.DictReader((packet/name).open()))
    def strrow(d):return {k:str(v) for k,v in d.items()}
    costs=[];fracs=[];raw=[]
    for r in rows:
        coordinate={k:r[k] for k in ['variant','normalization','unit']}
        costs.append(strrow(dict(**coordinate,source_N007=r['original_costs']['N007'],source_N006=r['original_costs']['N006'],common=r['common_theory'],
          application_N007=r['application_costs']['N007'],application_N006=r['application_costs']['N006'],written=r['written_denominator'],whole_programs=r['whole_program_cost'],
          required_decoders=r['required_decoder_cost'],software_inclusive=r['program_inclusive_denominator'],old_single_printed_validation=r['old_single_printed_validation_cost'],
          operational_drivers_separate=r['operational_driver_cost'],partial_formal_separate=r['partial_formal_cost'])))
        for kind in ['whole','conditional']:
            for key,f in r[kind].items():fracs.append(strrow(dict(**coordinate,comparison=kind+'_'+key,**f)))
    for category,files in counts['raw_files'].items():
        for path,row in files.items():
            for norm,unit in itertools.product(['NFC','NFKC'],UNITS):
                raw.append(strrow(dict(category=category,path=path,role=row['role'],bytes=row['bytes'],sha256=row['sha256'],normalization=norm,unit=unit,cost=row['metrics'][norm][unit])))
    need(read('costs.csv')==costs,'40 complete cost CSV rows');need(read('fractions.csv')==fracs,'160 fraction CSV rows');need(read('raw_files.csv')==raw,'280 per-file CSV rows')
def svg_rectangles(data):
    out=[]
    for el in ET.fromstring(data).iter():
        if not el.tag.endswith('path'):continue
        match=re.search(r'fill: (#[0-9a-f]{6})',el.get('style',''))
        if not match or match[1] not in COLORS:continue
        d=el.get('d','');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','literal SVG rectangle')
        values=list(map(float,re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',d)));need(len(values)==8,'four SVG corners')
        xs=values[::2];ys=values[1::2];need(len(set(xs))==len(set(ys))==2,'axis-aligned SVG bar')
        out.append((match[1],min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)))
    return out
def pdf_rectangles(path):
    reader=PdfReader(path);need(len(reader.pages)==1,'single chart page');page=reader.pages[0]
    rgb=None;stack=[];points=[];rects=[]
    colors={tuple(round(int(c[i:i+2],16)/255,6) for i in [1,3,5]):c for c in COLORS}
    for args,op in ContentStream(page.get_contents(),reader).operations:
        if op==b'q':stack.append(rgb)
        elif op==b'Q':rgb=stack.pop()
        elif op==b'rg':rgb=tuple(round(float(x),6) for x in args)
        elif op==b'g':rgb=(round(float(args[0]),6),)*3
        elif op==b'm':points=[tuple(map(float,args))]
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op in [b'f',b'B',b'f*',b'B*']:
            if rgb in colors and len(points)==4:
                xs={p[0] for p in points};ys={p[1] for p in points};need(len(xs)==len(ys)==2,'PDF rectangle')
                rects.append((colors[rgb],min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)))
            points=[]
        elif op in [b'n',b'S']:points=[]
    return rects,float(page.mediabox.height)
def vector_costs(svg,pdf,height,p):
    need(len(svg)==len(pdf)==7,'all7 chart bars')
    values=[p['source_sum'],p['written_denominator'],p['program_inclusive_denominator'],p['original_costs']['N007'],p['application_costs']['N007'],p['original_costs']['N006'],p['application_costs']['N006']]
    need([x[0] for x in svg]==COLORS+[COLORS[i] for i in [0,1,0,1]],'source/application/software roles')
    for start,end in [(0,3),(3,7)]:
        base=svg[start][1];scale=svg[start][3]/values[start];barheight=svg[start][4];step=svg[start+1][2]-svg[start][2]
        need(scale>0 and step>barheight>0,'positive uniform chart rows')
        for i in range(start,end):
            _,x,y,w,h=svg[i]
            need(abs(x-base)<3e-6 and abs(w-values[i]*scale)<3e-6 and abs(h-barheight)<3e-6 and abs(y-svg[start][2]-(i-start)*step)<1e-5,'actual SVG widths and row positions')
    for s,q in zip(svg,pdf):
        want=(s[0],s[1],height-s[2]-s[4],s[3],s[4])
        need(q[0]==want[0] and all(abs(a-b)<3e-6 for a,b in zip(q[1:],want[1:])),'actual PDF bar matches SVG geometry')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');manifest(a.packet,PIN);manifest(a.packet/'inputs',INPUT);manifest(a.packet/'input_review',REVIEW)
    rows,counts=derive(a.packet);data=load(a.packet/'results.json');p=validate(data,rows);csvs(a.packet,rows,counts)
    svg=svg_rectangles((a.packet/'costs.svg').read_bytes());pdf,height=pdf_rectangles(a.packet/'costs.pdf');vector_costs(svg,pdf,height,p)
    reader=PdfReader(a.packet/'reader.pdf');need(len(reader.pages)==2,'two complete reader pages');text='\n'.join(page.extract_text() or '' for page in reader.pages)
    need(all(f'{n:,}' in text for n in [78889,69895,19859,11771,38265,383279,11015,394294,464189,21960689,2516249]),'whole reader costs and external bytes')
    controls=[]
    for name,mut in [('omit HN companion',lambda x:x['rows'][0]['application_costs'].update(N006=1)),('omit decoder',lambda x:x['rows'][1].update(required_decoder_cost=0)),('discard witness',lambda x:x['rows'][2]['raw_file_costs']['programs'].popitem()),('alter reduced fraction',lambda x:x['rows'][3]['whole']['written'].update(reduced_numerator=1)),('omit text-only row',lambda x:x['rows'].pop()),('invent printed route',lambda x:x.update(complete_printed_program_alternative=3161)),('unknown proof zero',lambda x:x['external_bytes'].update(proof_cost=0)),('formal credit',lambda x:x.update(new_formal_credit=17))]:
        bad=copy.deepcopy(data);mut(bad)
        try:validate(bad,rows)
        except ValueError:controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    for kind in ['SVG','PDF']:
        bad=copy.deepcopy(svg if kind=='SVG' else pdf);color,x,y,w,h=bad[0];bad[0]=(color,x,y,w+1,h)
        try:vector_costs(bad if kind=='SVG' else svg,bad if kind=='PDF' else pdf,height,p)
        except ValueError:controls.append('distorted '+kind+' bar')
        else:raise ValueError('accepted distorted '+kind)
    report=dict(status='PASS_DISTINCT_DIAGONAL_V2_ARITHMETIC',author_manifest_sha256=PIN,coordinates=40,exact_fractions=160,cost_csv_rows=40,fraction_csv_rows=160,raw_file_csv_rows=280,actual_SVG_bars=7,actual_PDF_bars=7,reader_pages=2,controls_rejected=controls,author_implementation_imported=False,source_extraction_repeated=False,new_scientific_credit=0,primary=p)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
