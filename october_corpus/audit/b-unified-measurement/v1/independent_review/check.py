#!/usr/bin/env python3
"""Distinct complete arithmetic and actual vector review of unified B."""
from pathlib import Path
import argparse,copy,csv,hashlib,itertools,json,math,re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
PIN='5b04d4bb4b10cf085bb57a591d91d4e01e0508b4c684bb9b78d1942111095a05'
INPUT='e6f86129f414b960078738c0ae43cc799a78a3053c88af99965d605c9371c0b0'
REVIEW='67eded6cc8c36562cca175820827038f04dce4b7b7e1b69cb3893375c9532194'
COLORS=['#738799','#397c86','#b68145','#645b89']
IDS=['N001','N003','N008','L030','L040']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(ok,msg):
    if not ok:raise ValueError('DISTINCT_B_REJECT: '+msg)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def manifest(root,pin):
    need(sha((root/'manifest.json').read_bytes())==pin,'frozen manifest')
    for r in load(root/'manifest.json')['exports']:
        p=Path(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe export')
        b=(root/p).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'whole exact export')
def fraction(n,d):
    need(n>0 and d>0,'positive costs');g=math.gcd(n,d)
    order=len(str(n))-len(str(d))
    if (n<d*10**order if order>=0 else n*10**(-order)<d):order-=1
    places=41-order;q,r=divmod(n*10**places,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    digits=str(q).rjust(places+1,'0')
    dec=digits[:-places]+'.'+digits[-places:]
    if r==0:dec=dec.rstrip('0').rstrip('.')
    return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=dec)
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
def derive(packet):
    c=load(packet/'inputs/author_counts.json');audit=load(packet/'input_review/recount.json');source=load(packet/'inputs/retained_source_counts.json')
    need(audit['documents']=={k:r['metrics'] for k,r in c['documents'].items()},'accepted PDF scalars')
    need(audit['raw_files']=={k:r['metrics'] for vals in c['raw_files'].values() for k,r in vals.items()},'accepted whole raw files')
    need(audit['source_coordinates']==source['coordinates'],'accepted literal sources and article sensitivity')
    need([len(c['raw_files'][k]) for k in ['programs','drivers','formal']]==[4,2,2],'all eight raw files')
    rows=[]
    for v,n,u in itertools.product(['raw_untrimmed','raw_selected','calibrated_selected'],['NFC','NFKC'],UNITS):
        old=next(z for z in audit['source_coordinates'] if (z['variant'],z['normalization'],z['unit'])==(v,n,u))
        doc={k:metrics[v][n][u] for k,metrics in audit['documents'].items()}
        raw={cat:{k:audit['raw_files'][k][n][u] for k in vals} for cat,vals in c['raw_files'].items()}
        original=old['sources'];apps={k:doc['B'+str(i+1)] for i,k in enumerate(IDS)};total=sum(original.values());common=doc['U_B'];written=common+sum(apps.values());programs=sum(raw['programs'].values());printed=doc['CODE']
        denoms={'written':written,'including_printed_programs':written+printed,'including_raw_programs':written+programs};article=total-original['L040']+old['L040_article_only']
        rows.append(dict(variant=v,normalization=n,unit=u,source_costs=original,source_representations=old['source_representations'],source_sum=total,document_costs=doc,common_theory=common,applications=apps,all_applications=sum(apps.values()),written_denominator=written,printed_program_cost=printed,raw_program_cost=programs,denominators=denoms,whole={k:fraction(total,d) for k,d in denoms.items()},conditional={k:fraction(original[k],apps[k]) for k in IDS},article_only_sensitivity=dict(L040_article_cost=old['L040_article_only'],source_sum=article,whole={k:fraction(article,d) for k,d in denoms.items()},L040_conditional=fraction(old['L040_article_only'],apps['L040']),all_replacement_costs_unchanged=True,other_four_conditionals_unchanged=True),raw_file_costs=raw,operational_driver_cost=sum(raw['drivers'].values()),partial_formal_cost=sum(raw['formal'].values())))
    return rows,c
def validate(data,rows):
    need(data['rows']==rows,'all30 complete coordinates and360 exact fractions')
    p=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==('raw_untrimmed','NFC','characters_without_whitespace'))
    need(data['primary']==p,'unchanged raw full primary convention')
    need(data['originals']==IDS and data['source_rows']==65 and data['proof_contexts']==56,'five complete input contracts')
    need([data[k] for k in ['coordinates','main_exact_fractions','cover_sensitivity_fractions','total_exact_fractions']]==[30,240,120,360],'full comparison grid')
    need(data['source_representations_unchanged'] and data['N001_original_PDF_cost'] is None and data['N001_current_representation']=='literal_authored_rendering','no invented original PDF')
    need(all(data[k] for k in ['complete_current_common_charged_once','all_five_applications_complete','raw_printed_alternatives']),'whole theory and papers, software alternatives')
    need([data[k] for k in ['whole_programs','operational_drivers','partial_formal_files','partial_declarations']]==[4,2,2,14],'complete files with partial formal scope')
    need(data['unknown_costs']=={'historical_original_N001_PDF':None,'full_graphics':None,'retained_external_proofs':None,'primitive_catalogue_construction':None,'historical_software':None,'full_formalization':None},'unknown costs not zero')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new scientific credit')
    need('Entire current U_B' in data['conditional_acquisition'] and 'all four complete declared programs' in data['conditional_acquisition'],'whole acquisition assumption')
    return p
def csvs(packet,rows,c):
    def read(name):return list(csv.DictReader((packet/name).open()))
    def string(d):return {k:str(v) for k,v in d.items()}
    costs=[];fracs=[];raw=[]
    for r in rows:
        xyz={k:r[k] for k in ['variant','normalization','unit']}
        costs.append(string(dict(**xyz,**{k:r[k] for k in ['source_sum','common_theory','all_applications','written_denominator','printed_program_cost','raw_program_cost','operational_driver_cost','partial_formal_cost']},**{'source_'+k:v for k,v in r['source_costs'].items()},**{'application_'+k:v for k,v in r['applications'].items()})))
        for kind in ['whole','conditional']:
            for k,f in r[kind].items():fracs.append(string(dict(**xyz,comparison=kind+'_'+k,**f)))
        for k,f in r['article_only_sensitivity']['whole'].items():fracs.append(string(dict(**xyz,comparison='article_only_whole_'+k,**f)))
        fracs.append(string(dict(**xyz,comparison='article_only_L040_conditional',**r['article_only_sensitivity']['L040_conditional'])))
    for cat,files in c['raw_files'].items():
        for path,z in files.items():
            for n,u in itertools.product(['NFC','NFKC'],UNITS):raw.append(string(dict(category=cat,path=path,role=z['role'],bytes=z['bytes'],sha256=z['sha256'],normalization=n,unit=u,cost=z['metrics'][n][u])))
    need(read('costs.csv')==costs,'30 complete cost rows');need(read('fractions.csv')==fracs,'all360 CSV fractions');need(read('raw_files.csv')==raw,'all80 per-file costs')
def vectors(svg,pdf,height,p):
    need(len(svg)==len(pdf)==15,'all15 actual bars')
    values=[p['source_sum'],p['written_denominator'],p['denominators']['including_printed_programs'],p['denominators']['including_raw_programs'],p['common_theory']]
    for k in IDS:values.extend([p['source_costs'][k],p['applications'][k]])
    need([s[0] for s in svg]==[COLORS[i] for i in [0,1,2,2,3]+[0,1]*5],'all chart roles')
    for start,end in [(0,4),(4,15)]:
        base=svg[start][1];scale=svg[start][3]/values[start];barheight=svg[start][4];step=svg[start+1][2]-svg[start][2]
        need(scale>0 and step>barheight>0,'uniform positive chart spacing')
        for i in range(start,end):
            _,x,y,w,h=svg[i]
            need(abs(x-base)<3e-6 and abs(w-values[i]*scale)<3e-6 and abs(h-barheight)<3e-6 and abs(y-svg[start][2]-(i-start)*step)<1e-5,'actual SVG width and position')
    for s,q in zip(svg,pdf):
        want=(s[0],s[1],height-s[2]-s[4],s[3],s[4])
        need(q[0]==want[0] and all(abs(a-b)<3e-6 for a,b in zip(q[1:],want[1:])),'actual PDF and SVG geometry agree')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    manifest(a.packet,PIN);manifest(a.packet/'inputs',INPUT);manifest(a.packet/'input_review',REVIEW)
    rows,c=derive(a.packet);data=load(a.packet/'results.json');p=validate(data,rows);csvs(a.packet,rows,c)
    svg=svg_rectangles((a.packet/'costs.svg').read_bytes());pdf,height=pdf_rectangles(a.packet/'costs.pdf');vectors(svg,pdf,height,p)
    reader=PdfReader(a.packet/'reader.pdf');need(len(reader.pages)==2,'two whole reader pages');text='\n'.join(x.extract_text() or '' for x in reader.pages)
    need(all(f'{n:,}' in re.sub(r'\s','',text) for n in [124906,44905,69265,114170,127340,126500,13170,12330]),'complete reader primary costs')
    controls=[]
    for name,mut in [('omit application',lambda x:x['rows'][0]['applications'].pop('L040')),('omit common',lambda x:x['rows'][1].update(common_theory=0)),('invent N001 PDF',lambda x:x.update(N001_original_PDF_cost=0)),('prune program',lambda x:x['rows'][2]['raw_file_costs']['programs'].popitem()),('omit cover',lambda x:x['rows'][3]['source_costs'].update(L040=1)),('false reduced fraction',lambda x:x['rows'][4]['whole']['written'].update(reduced_numerator=1)),('alter article denominator',lambda x:x['rows'][5]['article_only_sensitivity']['whole']['written'].update(denominator=1)),('omit raw coordinate',lambda x:x['rows'].pop()),('unknown cost zero',lambda x:x['unknown_costs'].update(retained_external_proofs=0)),('formal credit',lambda x:x.update(new_formal_credit=14))]:
        bad=copy.deepcopy(data);mut(bad)
        try:validate(bad,rows)
        except ValueError:controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    for kind in ['SVG','PDF']:
        bad=copy.deepcopy(svg if kind=='SVG' else pdf);color,x,y,w,h=bad[4];bad[4]=(color,x,y,w+1,h)
        try:vectors(bad if kind=='SVG' else svg,bad if kind=='PDF' else pdf,height,p)
        except ValueError:controls.append('distorted '+kind+' bar')
        else:raise ValueError('accepted distorted '+kind)
    report=dict(status='PASS_DISTINCT_UNIFIED_B_ARITHMETIC',author_manifest_sha256=PIN,coordinates=30,exact_fractions=360,cost_csv_rows=30,fraction_csv_rows=360,raw_file_csv_rows=80,actual_SVG_bars=15,actual_PDF_bars=15,reader_pages=2,controls_rejected=controls,author_implementation_imported=False,source_extraction_repeated=False,new_scientific_credit=0,primary=p)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
