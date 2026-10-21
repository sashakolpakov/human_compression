#!/usr/bin/env python3
"""Distinct complete-file arithmetic and vector audit. No author imports."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,math,re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
PIN='b4232452cba25cae64bef0091a4adc947d8f679418fe73f1d439b5966ff587b7'
def need(b,m):
    if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=f'{q//10**12}.{q%10**12:012d}')
def inputs(packet):
    p=load(packet/'protocol.json');items={}
    for r in p['inputs']:
        f=packet/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'bound input');items[r['key']]=load(f)
    for key,pin in [('input_manifest','fb6b56fa264b35faec3ac8151023cf5ad083d25e5e9eed0ffce68f5e0ce9e439'),('review_manifest','32dae3ac7ef573d886c774f513136d7e29ebd3e7e119a9761e6ab7a50e1c1588')]:need(sha(packet/'inputs'/(key+'.json'))==pin,'accepted input and independent review')
    for name,files in [('input_manifest',{'policy':'policy.json','counts':'author_counts.json','input_protocol':'protocol.json'}),('review_manifest',{'review':'review.json','recount':'recount.json'})]:
        owned={r['path']:r for r in items[name]['exports']}
        for key,file in files.items():
            f=packet/'inputs'/(key+'.json');need(sha(f)==owned[file]['sha256'] and f.stat().st_size==owned[file]['bytes'],'accepted manifest owns copied input')
    need(items['review']['status']=='ACCEPTED_UNCHANGED_DISTINCT_L020_MEASUREMENT_INPUTS','distinct input acceptance')
    a=items['counts'];r=items['recount']
    for key,row in a['documents'].items():need(all(row[k]==r['documents'][key][k] for k in ['pdf_sha256','metrics']),'all150 independently recounted PDF cells')
    for group,files in a['raw_files'].items():
        for path,row in files.items():need(all(row[k]==r['raw_files'][group][path][k] for k in ['bytes','sha256','metrics']),'all80 independently recounted raw cells')
    need(items['policy']['primary']==p['primary'] if 'primary' in items['policy'] else p['primary']==['raw_untrimmed','NFC','characters_without_whitespace'],'preselected coordinate')
    return items
def derive(items):
    a=items['counts'];rows={}
    for v in ['raw_untrimmed','raw_selected','calibrated_selected']:
        for n in ['NFC','NFKC']:
            for unit in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:
                c={k:d['metrics'][v][n][unit] for k,d in a['documents'].items()};raw={g:sum(d['metrics'][n][unit] for d in files.values()) for g,files in a['raw_files'].items()};s=c['L020'];u=c['U'];ap=c['A1']+c['COUNTER'];w=u+ap;pc=c['CODE'];rc=raw['programs']
                rows[v,n,unit]=dict(variant=v,normalization=n,unit=unit,costs=c,raw_costs=raw,totals=dict(source=s,common=u,applications=ap,written=w,with_printed_programs=w+pc,with_raw_programs=w+rc),comparisons=dict(written=fraction(s,w),including_printed_programs=fraction(s,w+pc),including_raw_programs=fraction(s,w+rc),conditional_application=fraction(s,ap)),conditional_acquisition=dict(whole_common=['U'],whole_application=['A1','COUNTER'],common_cost=u,printed_program_cost=pc,raw_program_cost=rc,printed_upfront=u+pc,raw_upfront=u+rc,local_application_cost=ap,unknown_retained_costs_remain=True))
    return rows
def validate(d,rows,items):
    need(len(d['coordinates'])==30 and {(r['variant'],r['normalization'],r['unit']):r for r in d['coordinates']}==rows,'all complete sums and120 exact fractions')
    p=rows['raw_untrimmed','NFC','characters_without_whitespace'];need(d['primary']==p,'fixed primary')
    need(d['source_ids']==['L020'] and d['source_dispositions']==19,'one original and19 dispositions')
    need((d['coordinate_count'],d['exact_fraction_count'],d['combined_fractions'],d['conditional_fractions'])==(30,120,90,30),'complete numerical summary')
    b=d['boundary'];need(b['written_documents']==['U','A1','COUNTER'] and b['application_documents']==['A1','COUNTER'] and b['whole_common_once'] and b['whole_application_pages']==6,'complete common and both local papers')
    for k,v in dict(whole_programs=3,program_bytes=11533,separate_drivers=3,separate_driver_bytes=15947,separate_formal_files=2,separate_formal_bytes=6855,partial_Lean_declarations=15,whole_source_formalized=False).items():need(b[k]==v,'whole file inventory '+k)
    need(b['program_roles']==['required_finite_certificates_for_three_source_examples','bounded_validation_not_uniform_premise','transparent_S18_certificate_supporting_complete_written_proof'],'distinct actual program roles')
    for k in ['printed_raw_alternatives','old_program_appendix_replaced','no_free_old_B','no_cross_topic_discount']:need(b[k] is True,'scope '+k)
    need(b['unknown_costs']=={k:None for k in ['full_retained_classical_proofs','complete_runtime_implementation','historical_software','graphics_and_layout','full_formalization']},'unknown costs remain null')
    need(b['source_correction']==items['policy']['source_correction'] and b['retained_intro_Table1']==items['policy']['retained_intro_Table1'] and b['retained_limits']==items['policy']['background_qualifications'],'scientific correction and retained census scope')
    need(d['whole_documents']==['L020','U','A1','COUNTER','CODE'] and d['physical_pages']==[19,5,3,3,3],'all33 complete input pages')
    need(all(d[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'numbers assign no mathematical credit')
    for group,files in items['counts']['raw_files'].items():
        owned={r['path']:r for r in items['policy'][group]};want=[]
        for path,row in files.items():
            q=owned[path];want.append(dict(path=path,bytes=row['bytes'],sha256=row['sha256'],role=q.get('logical_role',q.get('role','operational_driver'))))
        need(d['raw_inventory'][group]==want,'whole raw file inventory')
    return p
def csvs(packet,rows,items):
    costs=list(csv.DictReader((packet/'costs.csv').open()));fractions=list(csv.DictReader((packet/'fractions.csv').open()));files=list(csv.DictReader((packet/'raw_files.csv').open()));need((len(costs),len(fractions),len(files))==(240,120,80),'all440 CSV rows')
    seen=set()
    for r in costs:
        key=tuple(r[k] for k in ['variant','normalization','unit']);slot=key+(r['kind'],r['component']);need(slot not in seen,'unique cost row');seen.add(slot);values=rows[key]['costs'] if r['kind']=='PDF' else rows[key]['raw_costs'];need(int(r['cost'])==values[r['component']],'actual cost CSV')
    seen=set()
    for r in fractions:
        key=tuple(r[k] for k in ['variant','normalization','unit']);slot=key+(r['comparison'],);need(slot not in seen,'unique fraction row');seen.add(slot);need(all(r[k]==str(v) for k,v in rows[key]['comparisons'][r['comparison']].items()),'actual fraction CSV')
    seen=set()
    for r in files:
        slot=tuple(r[k] for k in ['group','path','normalization','unit']);need(slot not in seen,'unique raw-file row');seen.add(slot);x=items['counts']['raw_files'][r['group']][r['path']];need(int(r['literal_bytes'])==x['bytes'] and r['sha256']==x['sha256'] and int(r['cost'])==x['metrics'][r['normalization']][r['unit']],'actual whole-file CSV')
    return 440
def vector_check(packet,p):
    c=p['costs'];raw=p['raw_costs'];app=['U','A1','COUNTER'];panels=[('written',[[('source',c['L020'])],[(k,c[k]) for k in app]]),('computational',[[(k,c[k]) for k in app+['CODE']],[(k,c[k]) for k in app]+[('programs',raw['programs'])]]),('conditional',[[('source',c['L020'])],[(k,c[k]) for k in app[1:]]])]
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
                path=g.find('s:path',ns);nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))));need(len(nums)==8,'four bar vertices');xs,ys=nums[::2],nums[1::2];need(ident not in svg,'unique actual bar');svg[ident]=(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
        need(len(ticks)>=3 and ticks[0][1]==0,'zero vertical origin');origin=ticks[0][0];scale=(origin-ticks[1][0])/ticks[1][1];need(all(abs(y-(origin-value*scale))<3e-6 for y,value in ticks),'linear actual vertical scale')
        for col,parts in enumerate(columns):
            bottom=0
            for key,value in parts:
                x,y,w,h=svg[f'cost-{panel}-{col}-{key}'];need(abs(h/scale-value)<.002 and abs((origin-y-h)/scale-bottom)<.002,'actual stacked cost geometry');bottom+=value
    need(len(svg)==15,'exactly15 complete cost rectangles')
    page=PdfReader(packet/'costs.pdf').pages[0];pdf=[];poly=[]
    for a,o in page.get_contents().operations:
        if o==b'm':poly=[tuple(map(float,a))]
        elif o==b'l':poly.append(tuple(map(float,a)))
        elif o in [b'f',b'B',b'f*',b'B*']:
            if len(poly)==4:
                xs,ys=zip(*poly);pdf.append((min(xs),float(page.mediabox.height)-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
            poly=[]
    for box in svg.values():need(sum(all(abs(x-y)<3e-6 for x,y in zip(box,b)) for b in pdf)==1,'actual PDF rectangle equals SVG')
    width=next(iter(svg.values()))[2];need(sum(abs(b[2]-width)<3e-6 for b in pdf)==15,'no extra cost rectangles')
    return 15
def acquisition_graph(packet,p):
    c=p['costs'];raw=p['raw_costs'];a=load(packet/'acquisition.json');g=load(packet/'document_graph.json')
    def steps(pairs):
        total=0;out=[]
        for key,value in pairs:total+=value;out.append(dict(acquired=key,increment=value,total=total))
        return out
    apps=[(k,c[k]) for k in ['A1','COUNTER']];need(a['written_route']==steps([('U',c['U'])]+apps),'complete written acquisition')
    need(a['source_cost']==c['L020'] and a['retained_proof_cost'] is None and a['graphics_cost'] is None,'source and unknown acquisition cost')
    need(len(a['routes'])==2,'two computational alternatives')
    for route,kind,code in zip(a['routes'],['printed','raw'],[c['CODE'],raw['programs']]):
        pairs=[('U',c['U']),('complete_program_representation',code)]+apps;want=dict(program_representation=kind,steps=steps(pairs),total=sum(v for _,v in pairs),upfront=c['U']+code,local_application=sum(v for _,v in apps));need(route==want,'whole computational acquisition')
    nodes={n['id']:n for n in g['nodes']};need(len(nodes)==len(g['nodes'])==6,'six unique coarse nodes')
    for key,pages in [('L020',19),('U',5),('A1',3),('COUNTER',3)]:need(nodes[key]['pages']==pages and nodes[key]['cost']==c[key],'whole graph document')
    need(nodes['CODE']['printed_pages']==3 and nodes['CODE']['printed_cost']==c['CODE'] and nodes['CODE']['raw_alternative_cost']==raw['programs'] and nodes['retained']['cost'] is None,'whole graph programs and unknown premise')
    want={('U','A1','proof_use'),('COUNTER','A1','proof_use'),('retained','U','retained_input'),('retained','COUNTER','retained_input'),('CODE','A1','required_finite_certificate'),('CODE','U','validation_only'),('CODE','COUNTER','validation_only'),('L020','A1','source_correspondence')}
    need(len(g['edges'])==8 and {(e['source'],e['target'],e['kind']) for e in g['edges']}==want,'all actual proof and evidence relationships')
    ns={'s':'http://www.w3.org/2000/svg'};root=ET.parse(packet/'document_graph.svg').getroot();ids={e.get('id') for e in root.findall('.//s:g',ns)}
    need({k for k in ids if k and k.startswith('edge-')}=={'edge-'+a+'-'+b for a,b,_ in want},'all eight actual graph arrows')
    return dict(nodes=6,edges=8,written_steps=3,computational_routes=2,computational_steps_per_route=4,fine_theorem_DAG=False)
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');need(sha(a.packet/'manifest.json')==PIN,'frozen numerical edition')
    for e in load(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'frozen numerical export')
    item=inputs(a.packet);rows=derive(item);d=load(a.packet/'results.json');primary=validate(d,rows,item);ncsv=csvs(a.packet,rows,item);nv=vector_check(a.packet,primary);graph=acquisition_graph(a.packet,primary);controls=[]
    for name,mut in [('omit whole counterproof',lambda d:d['coordinates'][0]['costs'].update(COUNTER=0)),('omit common',lambda d:d['coordinates'][0]['costs'].update(U=0)),('round fraction',lambda d:d['coordinates'][0]['comparisons']['written'].update(decimal='1.2')),('free computational acquisition',lambda d:d['coordinates'][0]['conditional_acquisition'].update(printed_upfront=0)),('add two code alternatives',lambda d:d['coordinates'][0]['totals'].update(with_raw_programs=1)),('wrong primary',lambda d:d.update(primary=d['coordinates'][0])),('free older B common',lambda d:d['boundary'].update(no_free_old_B=False)),('unknown cost zero',lambda d:d['boundary']['unknown_costs'].update(graphics_and_layout=0)),('counterproof excluded from application',lambda d:d['boundary'].update(whole_application_pages=3)),('full Lean claim',lambda d:d['boundary'].update(whole_source_formalized=True)),('add old appendix',lambda d:d['boundary'].update(old_program_appendix_replaced=False))]:
        bad=copy.deepcopy(d);mut(bad)
        try:validate(bad,rows,item)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted corruption '+name)
    report=dict(status='PASS_DISTINCT_L020_NUMBERS',coordinates=30,exact_fractions=120,CSV_rows=ncsv,actual_SVG_rectangles=nv,actual_PDF_rectangles=nv,acquisition_graph=graph,independent_controls=controls,author_modules_imported=False,primary_extraction_repeated=False,science_repeated=False,primary=primary)
    a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
