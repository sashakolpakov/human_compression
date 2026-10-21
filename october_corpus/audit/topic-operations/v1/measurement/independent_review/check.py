#!/usr/bin/env python3
"""Distinct arithmetic, CSV and actual vector-geometry review of Operations."""
from pathlib import Path
import argparse, copy, csv, hashlib, itertools, json, math, re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='c211bfc7a4ae9e0855874aa0584b0f8dfa85c855390e59fa49659b5b517ef978'
INPUT='3b0d503dcdd3fe778a05213523fa248109b06f6639df31a6ddbc9196cd1b8b03'
REVIEW='edb9e44fe49f5cd32ce66a909cef4e0324861d3026d9863417d23417768960d7'
COLORS=['#78879a','#327c82','#b47b37']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(ok,msg):
    if not ok:raise ValueError('DISTINCT_OPERATIONS_REJECT: '+msg)
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
def acquisition(common,sources,apps):
    out=[];own=0;old=0
    for k in ['U','N005','N006','N007']:
        di=common if k=='U' else apps[k];si=0 if k=='U' else sources[k]
        own+=di;old+=si
        row=dict(stage=k,current_increment=di,current_cumulative=own,matched_source_increment=si,matched_source_cumulative=old)
        if k=='U':row['scope']='Theory acquisition before any matched application; not a claim of zero historical theory cost.'
        out.append(row)
    return out

def derive(packet):
    counts=load(packet/'inputs/author_counts.json');audit=load(packet/'input_review/recount.json')
    need(audit['documents']=={k:r['metrics'] for k,r in counts['documents'].items()},'accepted distinct PDF costs')
    need(audit['text_only_sensitivity']=={k:r['metrics'] for k,r in counts['text_only_sensitivity'].items()},'accepted distinct text-only costs')
    need(audit['raw_files']=={k:r['metrics'] for rows in counts['raw_files'].values() for k,r in rows.items()},'accepted distinct full raw files')
    need([len(counts['raw_files'][k]) for k in ['programs','required_drivers','drivers','formal']]==[23,2,5,3],'all declared files')
    rows=[]
    for v,n,u in itertools.product(['raw_untrimmed','raw_selected','calibrated_selected','text_only_sensitivity'],['NFC','NFKC'],UNITS):
        doc={k:(audit['text_only_sensitivity'][k][n][u] if v=='text_only_sensitivity' else metrics[v][n][u]) for k,metrics in audit['documents'].items()}
        file={cat:{p:audit['raw_files'][p][n][u] for p in vals} for cat,vals in counts['raw_files'].items()}
        sources={k:doc[k] for k in ['N005','N006','N007']};apps={'N005':doc['A0'],'N006':doc['A2']+doc['A2nine']+doc['A2HN'],'N007':doc['A1']}
        numerator=sum(sources.values());written=doc['U']+sum(apps.values());program=sum(file['programs'].values());decoders=sum(file['required_drivers'].values())
        rows.append(dict(variant=v,normalization=n,unit=u,original_costs=sources,source_sum=numerator,document_costs=doc,common_theory=doc['U'],
          application_costs=apps,all_applications=sum(apps.values()),written_denominator=written,whole_program_cost=program,required_decoder_cost=decoders,
          whole_software_cost=program+decoders,program_inclusive_denominator=written+program+decoders,complete_printed_program_denominator=None,
          partial_printed_costs={k:dict(printed_cost=doc[k],replaced_raw_cost=sum(file['programs'][i] for i in ids),whole_file_ids=ids,not_a_complete_program_denominator=True) for k,ids in {'CODEold':['P.N007.diagonal_models'],'CODEnew':['P.N005.affine_example','P.N005.literal_twist','P.N005.presentation_identities']}.items()},acquisition=acquisition(doc['U'],sources,apps),raw_file_costs=file,operational_driver_cost=sum(file['drivers'].values()),partial_formal_cost=sum(file['formal'].values()),
          whole={'written':fraction(numerator,written),'including_whole_raw_software':fraction(numerator,written+program+decoders)},
          conditional={k:fraction(sources[k],apps[k]) for k in sources}))
    return rows,counts
def validate(data,rows):
    need(data['rows']==rows,'all40 complete coordinates and200 fractions')
    primary=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
    need(data['primary']==primary,'complete primary row')
    need(data['originals']==['N005','N006','N007'] and data['source_rows']=={'N005':81,'N006':27,'N007':32},'three-original complete contract')
    need([data[k] for k in ['ordinary_coordinates','text_only_coordinates','exact_whole_fractions','exact_conditional_fractions','total_exact_fractions']]==[30,10,80,120,200],'all coordinates counted')
    need(data['complete_printed_program_alternative'] is None and data['source_exceptions_outside_this_edition']==['Fi22','Fi24prime'],'no fictitious printed route or imported exceptions')
    need(data['external_bytes']==dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249,not_character_counts=True,full_runtime_cost=None,proof_cost=None),'separate inherited external bytes, unknown full costs')
    need(data['unknown_costs']==dict(retained_classification_proofs=None,source_historical_software=None,full_graphics=None,full_formalization=None),'unknowns not zero')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no scientific credit')
    need(all(s in data['conditional_acquisition'] for s in ['whole 21-page common theory','all 23 whole mathematical/validation files','both complete required decoding drivers','required external data']),'full acquisition declared')
    return primary
def csvs(packet,rows,counts):
    def read(name):return list(csv.DictReader((packet/name).open()))
    def s(d):return {k:str(v) for k,v in d.items()}
    costs=[];fracs=[];raw=[];acq=[];part=[]
    for r in rows:
        c={k:r[k] for k in ['variant','normalization','unit']}
        vals=dict(common=r['common_theory'],written=r['written_denominator'],whole_programs=r['whole_program_cost'],required_decoders=r['required_decoder_cost'],software_inclusive=r['program_inclusive_denominator'],operational_drivers_separate=r['operational_driver_cost'],partial_formal_separate=r['partial_formal_cost'])
        vals.update({'source_'+k:v for k,v in r['original_costs'].items()});vals.update({'application_'+k:v for k,v in r['application_costs'].items()})
        costs.append(s(dict(**c,**vals)))
        for kind in ['whole','conditional']:
            for key,f in r[kind].items():fracs.append(s(dict(**c,comparison=kind+'_'+key,**f)))
        for stage in r['acquisition']:acq.append(s(dict(**c,**{k:v for k,v in stage.items() if k!='scope'})))
        for k,v in r['partial_printed_costs'].items():part.append(s(dict(**c,appendix=k,printed_cost=v['printed_cost'],replaced_raw_cost=v['replaced_raw_cost'],whole_files=len(v['whole_file_ids']),complete_program_factor='not_defined')))
    for category,files in counts['raw_files'].items():
        for name,row in files.items():
            for norm,unit in itertools.product(['NFC','NFKC'],UNITS):raw.append(s(dict(category=category,id=name,role=row['role'],bytes=row['bytes'],sha256=row['sha256'],normalization=norm,unit=unit,cost=row['metrics'][norm][unit])))
    for name,expected in [('costs.csv',costs),('fractions.csv',fracs),('raw_files.csv',raw),('acquisition.csv',acq),('partial_printed_alternatives.csv',part)]:need(read(name)==expected,'complete CSV '+name)
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
    need(len(svg)==len(pdf)==3,'all3 chart bars')
    values=[p['source_sum'],p['written_denominator'],p['program_inclusive_denominator']]
    need([x[0] for x in svg]==COLORS,'source/written/software roles')
    base=svg[0][1];scale=svg[0][3]/values[0];bh=svg[0][4];step=svg[1][2]-svg[0][2]
    need(scale>0 and step>bh>0,'positive uniform chart rows')
    for i,(_,x,y,w,h) in enumerate(svg):need(abs(x-base)<3e-6 and abs(w-values[i]*scale)<3e-6 and abs(h-bh)<3e-6 and abs(y-svg[0][2]-i*step)<1e-5,'actual SVG widths and row positions')
    for s,q in zip(svg,pdf):
        want=(s[0],s[1],height-s[2]-s[4],s[3],s[4])
        need(q[0]==want[0] and all(abs(a-b)<3e-6 for a,b in zip(q[1:],want[1:])),'actual PDF bar matches SVG geometry')

def acquisition_vectors(packet,p):
    paths={}
    for e in ET.fromstring((packet/'acquisition.svg').read_bytes()).iter():
        if not e.tag.endswith('path') or 'clip-path' not in e.attrib:continue
        style=e.get('style','');match=re.search(r'stroke: (#[0-9a-f]{6})',style)
        if match and match[1] in COLORS[:2] and style.startswith('fill: none;'):
            need(re.sub(r'[-+\d.eE\s]','',e.get('d',''))=='MLLLL','five SVG acquisition points')
            vals=list(map(float,re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',e.get('d',''))))
            paths[match[1]]=list(zip(vals[::2],vals[1::2]))
    need(set(paths)==set(COLORS[:2]),'two plotted acquisition lines')
    own=[0]+[x['current_cumulative'] for x in p['acquisition']];old=[0]+[x['matched_source_cumulative'] for x in p['acquisition']]
    base=paths[COLORS[0]][0];scale=(base[1]-paths[COLORS[0]][-1][1])/old[-1];step=paths[COLORS[0]][1][0]-base[0]
    need(scale>0 and step>0,'positive SVG axes')
    for color,values in zip(COLORS,[old,own]):
        need(len(paths[color])==5,'all acquisition stages')
        for i,(x,y) in enumerate(paths[color]):need(abs(x-base[0]-i*step)<4e-6 and abs(y-base[1]+values[i]*scale)<4e-6,'actual SVG acquisition cost')
    pdf=PdfReader(packet/'acquisition.pdf');page=pdf.pages[0];height=float(page.mediabox.height);color=None;stack=[];points=[];found={}
    for args,op in ContentStream(page.get_contents(),pdf).operations:
        if op==b'q':stack.append(color)
        elif op==b'Q':color=stack.pop()
        elif op==b'RG':color=tuple(round(float(x),6) for x in args)
        elif op==b'G':color=(round(float(args[0]),6),)*3
        elif op==b'm':points=[tuple(map(float,args))]
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op==b'S':
            for c in COLORS[:2]:
                rgb=tuple(round(int(c[i:i+2],16)/255,6) for i in [1,3,5])
                if color==rgb and len(points)==5:found[c]=points
            points=[]
        elif op in [b'n',b'f',b'B',b'f*',b'B*']:points=[]
    need(set(found)==set(paths),'two actual PDF acquisition lines')
    for color in paths:
        for (x,y),(px,py) in zip(paths[color],found[color]):need(abs(x-px)<3e-6 and abs(height-y-py)<3e-6,'actual PDF acquisition equals SVG')
    data=load(packet/'plot_data.json');need(data['cost_bars']==[p['source_sum'],p['written_denominator'],p['program_inclusive_denominator']] and data['current_cumulative']==own and data['matched_original_cumulative']==old and data['axes_start_at_zero'] and not data['claim_of_sawtooth'],'plot metadata accurate')
    return dict(actual_SVG_points=10,actual_PDF_points=10)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');manifest(a.packet,PIN);manifest(a.packet/'inputs',INPUT);manifest(a.packet/'input_review',REVIEW)
    rows,counts=derive(a.packet);data=load(a.packet/'results.json');p=validate(data,rows);csvs(a.packet,rows,counts)
    svg=svg_rectangles((a.packet/'costs.svg').read_bytes());pdf,height=pdf_rectangles(a.packet/'costs.pdf');vector_costs(svg,pdf,height,p)
    acq=acquisition_vectors(a.packet,p)
    reader=PdfReader(a.packet/'reader.pdf');need(len(reader.pages)==3,'three complete reader pages');text='\n'.join(page.extract_text() or '' for page in reader.pages)
    need(all(f'{n:,}' in re.sub(r',\s+',',',text) for n in [200891,158594,58215,49595,38479,12305,392833,11015,403848,562442,21960689,2516249]),'whole reader costs and external bytes')
    controls=[]
    for name,mut in [('omit HN companion',lambda x:x['rows'][0]['application_costs'].update(N006=1)),('omit decoder',lambda x:x['rows'][1].update(required_decoder_cost=0)),('discard witness',lambda x:x['rows'][2]['raw_file_costs']['programs'].popitem()),('alter reduced fraction',lambda x:x['rows'][3]['whole']['written'].update(reduced_numerator=1)),('omit text-only row',lambda x:x['rows'].pop()),('invent printed route',lambda x:x.update(complete_printed_program_alternative=3161)),('unknown proof zero',lambda x:x['external_bytes'].update(proof_cost=0)),('formal credit',lambda x:x.update(new_formal_credit=17)),('free initial theory',lambda x:x['rows'][0]['acquisition'][0].update(current_increment=0)),('omit N005 original',lambda x:x['rows'][0]['original_costs'].pop('N005'))]:
        bad=copy.deepcopy(data);mut(bad)
        try:validate(bad,rows)
        except ValueError:controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    for kind in ['SVG','PDF']:
        bad=copy.deepcopy(svg if kind=='SVG' else pdf);color,x,y,w,h=bad[0];bad[0]=(color,x,y,w+1,h)
        try:vector_costs(bad if kind=='SVG' else svg,bad if kind=='PDF' else pdf,height,p)
        except ValueError:controls.append('distorted '+kind+' bar')
        else:raise ValueError('accepted distorted '+kind)
    report=dict(status='PASS_DISTINCT_OPERATIONS_ARITHMETIC',author_manifest_sha256=PIN,coordinates=40,exact_fractions=200,cost_csv_rows=40,fraction_csv_rows=200,raw_file_csv_rows=330,actual_SVG_bars=3,actual_PDF_bars=3,acquisition_vectors=acq,acquisition_integer_cells=640,reader_pages=3,controls_rejected=controls,author_implementation_imported=False,source_extraction_repeated=False,new_scientific_credit=0,primary=p)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
