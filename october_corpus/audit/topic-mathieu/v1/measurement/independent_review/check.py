#!/usr/bin/env python3
"""Distinct L073 arithmetic, full-file CSV and vector check; no author imports."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,math,re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
PIN='1f7256e911cc3bf0797672e4237a7ef8fe6e6b24cbcca30d13142c82c7dc2d36'
def need(b,m):
    if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=f'{q//10**12}.{q%10**12:012d}')
def inputs(packet):
    p=load(packet/'protocol.json');items={}
    for r in p['inputs']:
        f=packet/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'bound input');items[r['key']]=load(f)
    for key,pin in [('input_manifest','bbef6f90211122f5b5db138bfadd8bb1538bd88f1d6dd7b41dd175e268512de2'),('review_manifest','e33647116d0bd471cba28eb43448090153f7a6dde8b3e366fbaaa30670a50467')]:need(sha(packet/'inputs'/(key+'.json'))==pin,'accepted input/review')
    for name,files in [('input_manifest',{'policy':'policy.json','counts':'author_counts.json','boundary':'accounting_boundary.json','input_protocol':'protocol.json','modular_acceptance':'modular_acceptance.json'}),('review_manifest',{'review':'review.json','recount':'recount.json'})]:
        owned={r['path']:r for r in items[name]['exports']}
        for key,file in files.items():
            f=packet/'inputs'/(key+'.json');need(sha(f)==owned[file]['sha256'] and f.stat().st_size==owned[file]['bytes'],'accepted manifest owns actual copied record')
    need(items['review']['status']=='ACCEPTED_UNCHANGED_INPUTS','independent input acceptance')
    a=items['counts'];r=items['recount'];need(a['documents']==r['document_counts'],'all180 independent document cells')
    for group,files in a['raw_files'].items():
        for path,row in files.items():need(all(row[k]==r['raw_counts'][group][path][k] for k in ['bytes','sha256','metrics']),'all220 raw cells independently agree')
    return items
def derive(items):
    a=items['counts'];rows={}
    for v in ['raw_untrimmed','raw_selected','calibrated_selected']:
        for n in ['NFC','NFKC']:
            for unit in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:
                c={k:d['metrics'][v][n][unit] for k,d in a['documents'].items()};raw={g:sum(d['metrics'][n][unit] for d in files.values()) for g,files in a['raw_files'].items()};s=c['L073'];u=c['U'];ap=sum(c[k] for k in ['A1','CLASSES','ROWS']);w=u+ap;data=raw['required_raw_data'];pc=c['CODE'];rc=raw['programs']
                rows[v,n,unit]=dict(variant=v,normalization=n,unit=unit,costs=c,raw_costs=raw,totals=dict(source=s,common=u,applications=ap,written=w,including_printed_programs_and_data=w+pc+data,including_raw_programs_and_data=w+rc+data),comparisons=dict(written=frac(s,w),including_printed_programs_and_data=frac(s,w+pc+data),including_raw_programs_and_data=frac(s,w+rc+data),conditional_application=frac(s,ap)),conditional_acquisition=dict(whole_common=['U'],whole_application=['A1','CLASSES','ROWS'],common_cost=u,printed_program_cost=pc,raw_program_cost=rc,mandatory_raw_data_cost=data,printed_upfront=u+pc+data,raw_upfront=u+rc+data,local_application_cost=ap,unknown_retained_costs_remain=True))
    return rows
def validate(d,rows,items):
    need(len(d['coordinates'])==30 and {(r['variant'],r['normalization'],r['unit']):r for r in d['coordinates']}==rows,'all complete sums and120 exact fractions')
    primary=rows['raw_untrimmed','NFC','characters_without_whitespace'];need(d['primary']==primary,'fixed primary')
    need(d['source_ids']==['L073'] and (d['source_clauses'],d['source_rows'],d['rank_two_classes'],d['rank_three_classes'])==(14,431,81,431),'one corrected complete original')
    need(d['coordinate_count']==30 and d['exact_fraction_count']==120 and d['combined_fractions']==90 and d['conditional_fractions']==30,'coordinate summary')
    b=d['boundary'];need(b['written_documents']==['U','A1','CLASSES','ROWS'] and b['application_documents']==['A1','CLASSES','ROWS'] and b['whole_common_once'] and b['whole_application_pages']==24,'complete common and all companion papers')
    for k,v in dict(whole_programs=7,mandatory_data_files=2,mandatory_data_bytes=83965,programs_bytes=34695,separate_drivers=3,separate_driver_bytes=20542,separate_generated_outputs=10,separate_output_bytes=1567120,formal_files=0,formal_declarations=0).items():need(b[k]==v,'whole-file inventory '+k)
    for k in ['programs_are_required_mathematical_inputs','printed_and_raw_alternatives','data_paid_in_both_computational_routes','printed_code_is_not_printed_data_substitute','no_cross_topic_discount','no_free_old_umbrella','no_L095_special_theorem','no_unavailable_geo_identities_claimed','predecessor_is_retained_not_new_original']:need(b[k] is True,'retained scope '+k)
    need(len(b['unknown_costs'])==4 and all(v is None for v in b['unknown_costs'].values()),'unknown costs not zero')
    need(d['whole_documents']==['L073','U','A1','CLASSES','ROWS','CODE'] and d['physical_pages']==[9,2,5,10,9,11],'whole46 input pages')
    need(all(d[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no mathematical credits from numbers')
    for group,files in items['counts']['raw_files'].items():
        want=[dict(path=path,bytes=row['bytes'],sha256=row['sha256'],role=row['role']) for path,row in files.items()];need(d['raw_inventory'][group]==want,'all22 whole raw files')
    return primary
def csvs(packet,rows,items):
    costs=list(csv.DictReader((packet/'costs.csv').open()));fractions=list(csv.DictReader((packet/'fractions.csv').open()));files=list(csv.DictReader((packet/'raw_files.csv').open()));need((len(costs),len(fractions),len(files))==(300,120,220),'complete CSV rows')
    seen=set()
    for r in costs:
        key=tuple(r[k] for k in ['variant','normalization','unit']);slot=key+(r['kind'],r['component']);need(slot not in seen,'unique cost cell');seen.add(slot);values=rows[key]['costs'] if r['kind']=='PDF' else rows[key]['raw_costs'];need(int(r['cost'])==values[r['component']],'cost CSV cell')
    seen=set()
    for r in fractions:
        key=tuple(r[k] for k in ['variant','normalization','unit']);slot=key+(r['comparison'],);need(slot not in seen,'unique fraction cell');seen.add(slot);need(all(r[k]==str(v) for k,v in rows[key]['comparisons'][r['comparison']].items()),'fraction CSV cell')
    seen=set()
    for r in files:
        slot=tuple(r[k] for k in ['group','path','normalization','unit']);need(slot not in seen,'unique raw-file cell');seen.add(slot);x=items['counts']['raw_files'][r['group']][r['path']];need(int(r['literal_bytes'])==x['bytes'] and r['sha256']==x['sha256'] and int(r['cost'])==x['metrics'][r['normalization']][r['unit']],'whole raw CSV cost')
    return 640
def vector_check(packet,p):
    c=p['costs'];raw=p['raw_costs'];app=['U','A1','CLASSES','ROWS'];panels=[('written',[[('source',c['L073'])],[(k,c[k]) for k in app]]),('computational',[[(k,c[k]) for k in app+['CODE']]+[('required_raw_data',raw['required_raw_data'])],[(k,c[k]) for k in app]+[('programs',raw['programs']),('required_raw_data',raw['required_raw_data'])]]),('conditional',[[('source',c['L073'])],[(k,c[k]) for k in app[1:]]])]
    parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True));root=ET.parse(packet/'costs.svg',parser).getroot();ns={'s':'http://www.w3.org/2000/svg'};svg={}
    for index,(panel,columns) in enumerate(panels,1):
        ax=next(g for g in root.findall('.//s:g',ns) if g.get('id')==f'axes_{index}');ticks=[]
        for g in ax.findall('.//s:g',ns):
            ident=g.get('id','')
            if ident.startswith('ytick_'):
                path=g.find('.//s:path',ns);comments=[e.text for e in g.iter() if e.tag is ET.Comment]
                if path is not None and comments:
                    xy=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))));ticks.append((xy[1],float(comments[0].strip().replace(',',''))))
            if ident.startswith('cost-'):
                path=g.find('s:path',ns);nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))));need(len(nums)==8,'four cost vertices');xs,ys=nums[::2],nums[1::2];need(ident not in svg,'unique actual cost id');svg[ident]=(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
        need(len(ticks)>=3 and ticks[0][1]==0,'actual zero vertical origin');origin=ticks[0][0];scale=(origin-ticks[1][0])/ticks[1][1];need(all(abs(y-(origin-value*scale))<3e-6 for y,value in ticks),'actual linear vertical scale')
        for col,parts in enumerate(columns):
            bottom=0
            for key,value in parts:
                x,y,w,h=svg[f'cost-{panel}-{col}-{key}'];need(abs(h/scale-value)<.002 and abs((origin-y-h)/scale-bottom)<.002,'actual complete cost and stacked baseline');bottom+=value
    need(len(svg)==21,'exactly21 cost rectangles')
    page=PdfReader(packet/'costs.pdf').pages[0];pdf=[];poly=[]
    for a,o in page.get_contents().operations:
        if o==b'm':poly=[tuple(map(float,a))]
        elif o==b'l':poly.append(tuple(map(float,a)))
        elif o in [b'f',b'B',b'f*',b'B*']:
            if len(poly)==4:
                xs,ys=zip(*poly);pdf.append((min(xs),float(page.mediabox.height)-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
            poly=[]
    for box in svg.values():need(sum(all(abs(x-y)<3e-6 for x,y in zip(box,b)) for b in pdf)==1,'each actual PDF bar equals SVG')
    width=next(iter(svg.values()))[2];need(sum(abs(b[2]-width)<3e-6 for b in pdf)==21,'no extra PDF cost bar')
    return 21
def acquisition_graph(packet,p):
    c=p['costs'];raw=p['raw_costs'];a=load(packet/'acquisition.json');g=load(packet/'document_graph.json')
    def steps(pairs):
        total=0;out=[]
        for key,value in pairs:
            total+=value;out.append(dict(acquired=key,increment=value,total=total))
        return out
    apps=[(k,c[k]) for k in ['A1','CLASSES','ROWS']]
    need(a['written_route']==steps([('U',c['U'])]+apps),'whole written acquisition')
    need(a['source_cost']==c['L073'] and a['retained_proof_cost'] is None and a['graphics_cost'] is None,'source and unknown acquisition costs')
    need(len(a['routes'])==2,'two alternative acquisition routes')
    for route,kind,code in zip(a['routes'],['printed','raw'],[c['CODE'],raw['programs']]):
        pairs=[('U',c['U']),('complete_program_representation',code),('both_mandatory_JSON',raw['required_raw_data'])]+apps
        want=dict(program_representation=kind,steps=steps(pairs),total=sum(v for _,v in pairs),upfront=sum(v for _,v in pairs[:3]),local_application=sum(v for _,v in apps))
        need(route==want,'complete computational acquisition')
    nodes={n['id']:n for n in g['nodes']};need(len(nodes)==len(g['nodes'])==6,'six distinct coarse nodes')
    for key,pages,cost in [('L073',9,c['L073']),('U',2,c['U']),('application',24,sum(v for _,v in apps))]:need(nodes[key]['pages']==pages and nodes[key]['cost']==cost,'whole document graph cost')
    need(nodes['application']['components']==[dict(id=k,pages=pages,cost=c[k]) for k,pages in [('A1',5),('CLASSES',10),('ROWS',9)]],'all application graph companions')
    for k,v in dict(printed_pages=11,printed_cost=c['CODE'],raw_alternative_cost=raw['programs'],program_bytes=34695).items():need(nodes['programs'][k]==v,'complete graph programs')
    need(nodes['data']['cost']==raw['required_raw_data'] and nodes['data']['literal_bytes']==83965 and nodes['retained']['cost'] is None,'mandatory graph data and retained unknown')
    want={('U','application','required_input'),('programs','application','required_input'),('data','programs','required_input'),('retained','U','retained_input'),('retained','programs','retained_input'),('L073','application','source_correspondence')}
    need(len(g['edges'])==6 and {(e['source'],e['target'],e['kind']) for e in g['edges']}==want,'coarse dependency edges and correspondence distinction')
    return dict(nodes=6,edges=6,written_steps=4,computational_routes=2,computational_steps_per_route=6,fine_theorem_DAG=False)
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'frozen numerical edition')
    for e in load(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'frozen numerical export')
    item=inputs(a.packet);rows=derive(item);d=load(a.packet/'results.json');primary=validate(d,rows,item);ncsv=csvs(a.packet,rows,item);nv=vector_check(a.packet,primary);graph=acquisition_graph(a.packet,primary)
    controls=[]
    for name,mut in [('drop companion tables',lambda d:d['coordinates'][0]['costs'].update(CLASSES=0)),('drop both JSONs',lambda d:d['coordinates'][0]['raw_costs'].update(required_raw_data=0)),('round exact fraction',lambda d:d['coordinates'][0]['comparisons']['written'].update(decimal='0.3')),('free acquisition',lambda d:d['coordinates'][0]['conditional_acquisition'].update(printed_upfront=0)),('both code alternatives added',lambda d:d['coordinates'][0]['totals'].update(including_raw_programs_and_data=1)),('wrong primary',lambda d:d.update(primary=d['coordinates'][0])),('claim historical identities',lambda d:d['boundary'].update(no_unavailable_geo_identities_claimed=False)),('claim predecessor original',lambda d:d['boundary'].update(predecessor_is_retained_not_new_original=False)),('unknown cost zero',lambda d:d['boundary']['unknown_costs'].update(full_graphics=0)),('whole application shortened',lambda d:d['boundary'].update(whole_application_pages=5)),('incomplete mandatory data',lambda d:d['boundary'].update(mandatory_data_bytes=23929))]:
        bad=copy.deepcopy(d);mut(bad)
        try:validate(bad,rows,item)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted corruption '+name)
    report=dict(status='PASS_DISTINCT_L073_NUMBERS',coordinates=30,exact_fractions=120,CSV_rows=ncsv,actual_SVG_rectangles=nv,actual_PDF_rectangles=nv,acquisition_graph=graph,independent_controls=controls,author_modules_imported=False,primary_extraction_repeated=False,science_repeated=False,primary=primary)
    a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
