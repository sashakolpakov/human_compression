#!/usr/bin/env python3
"""Distinct numerical/CSV/vector review. Imports only this review's helpers."""
import argparse,copy,csv,hashlib,json,math,pathlib,re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
from derive import derive,need,read,sha,UNITS,FORMS,PRIMARY
from numeric_review import check_result,controls,DOCS,ROLES
from geometry_review import run as geometry,svg,expected,compare,close,NS
PIN='2b9f3078221231d7db32b17d20517531ca3956ba5caa8fbab6f18b3b2bf645d3'
COMPARE=['written','conditional_F010','conditional_L126']
def verify_packet(root):
    p=root/'manifest.json';need(sha(p.read_bytes())==PIN,'exact numerical author freeze');m=read(p)
    for x in m['exports']:
        b=(root/x['path']).read_bytes();need(len(b)==x['bytes']and sha(b)==x['sha256'],'numerical export '+x['path'])
    return len(m['exports'])
def table(path,header,rows):
    with path.open(newline='')as f:got=list(csv.reader(f))
    need(got==[header]+[[str(v)for v in r]for r in rows],'complete CSV '+path.name);return len(rows)
def csv_checks(packet,rows,counts,inventory):
    costs=[];fracs=[];raw=[]
    for r in rows:
        for k in DOCS:costs.append([r['variant'],r['normalization'],r['unit'],'PDF',k,r['costs'][k]])
        for k in ROLES:costs.append([r['variant'],r['normalization'],r['unit'],'raw-role',k,r['raw_costs'][k]])
        for k in COMPARE:fracs.append([r['variant'],r['normalization'],r['unit'],k]+[r['comparisons'][k][c]for c in ['numerator','denominator','reduced_numerator','reduced_denominator','decimal']])
    for r in inventory['files']:
        for form in FORMS:
            for unit in UNITS:raw.append([r['key'],r['role'],r['bytes'],r['sha256'],form,unit,counts['raw_files'][r['key']]['metrics'][form][unit]])
    return {'costs':table(packet/'costs.csv',['variant','normalization','unit','representation','key','cost'],costs),'fractions':table(packet/'fractions.csv',['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'],fracs),'raw_files':table(packet/'raw_files.csv',['file','role','whole_bytes','sha256','normalization','unit','cost'],raw)}
EDGES=[('F010','R1','correspondence'),('L126','R2','correspondence'),('U_R','R1','common'),('U_R','R2','common'),('data','certificate','required_input'),('certificate','R2','required_input'),('optional','R1','optional_check'),('optional','R2','optional_check'),('external','U_R','retained_input'),('external','R1','retained_input'),('external','R2','retained_input')]
POS={'F010':(90,265),'L126':(702,265),'U_R':(396,265),'R1':(220,145),'R2':(565,145),'external':(396,375),'data':(696,28),'certificate':(535,28),'optional':(135,28)}
def plot_data_check(data,oracle):
    need(set(data)=={'costs','inventory'},'both complete plot data panels')
    d=oracle['primary']['documents'];raw=next(x['whole_role_counts']for x in oracle['raw_inventory']if x['normalization']=='NFC'and x['unit']==UNITS[2])
    for name in ['costs','inventory']:
        W,H,want=expected(oracle,name);got=data[name];need(len(got)==len(want)and {r['id']for r in got}==set(want),'exact plot data rows')
        for r in got:
            key=r['id'].split('-',2)[2];need(r['key']==key and r['value']==(d[key]if key in d else raw[key]),'plot data actual count')
            x,y,w,h=want[r['id']];need(all(close(a,b)for a,b in zip([r['x'],r['y'],r['w'],r['h']],[x,H-y-h,w,h])),'plot data independent dimension')
def graph_data(g,oracle):
    d=oracle['primary']['documents'];raw=next(x['whole_role_counts']for x in oracle['raw_inventory']if x['normalization']=='NFC'and x['unit']==UNITS[2]);want={k:('source'if k in DOCS[:2]else'written',d[k])for k in DOCS[:5]};want.update(certificate=('required',raw[ROLES[0]]),data=('required',raw[ROLES[1]]),optional=('optional',raw[ROLES[2]]),external=('retained',None))
    need(len(g['nodes'])==9 and {x['id']:(x['kind'],x['cost'])for x in g['nodes']}==want,'all nine actual document/evidence nodes')
    need([(x['source'],x['target'],x['kind'])for x in g['edges']]==EDGES,'all eleven typed document arrows')
    need(g['not_a_theorem_DAG']and g['node_counts_are_not_ratios']and g['initial_acquisition']==['U_R','actual retained classical premises']and g['additional_L126_required']==['certificate','data']and g['optional_checks_required']is False and g['no_sibling_application_dependency'],'graph interpretation/acquisition')
def nums(s):return list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)))
def graph_svg(raw):
    root=ET.fromstring(raw);groups={x.get('id'):x for x in root.findall('.//s:g',NS)}
    need({x for x in groups if x.startswith('node-')}=={'node-'+k for k in POS},'actual nine SVG boxes')
    need({x for x in groups if x.startswith('edge-')}=={'edge-'+a+'-'+b for a,b,k in EDGES},'actual eleven SVG arrows')
    for k,(x,y)in POS.items():
        paths=groups['node-'+k].findall('s:path',NS);need(len(paths)==1,'one actual node box');v=nums(paths[0].get('d'));need(len(v)==8 and all(close(a,b)for a,b in zip(v,[x-77,440-y+23,x+77,440-y+23,x+77,440-y-23,x-77,440-y-23])),'actual node coordinates '+k)
    for a,b,kind in EDGES:
        paths=groups['edge-'+a+'-'+b].findall('s:path',NS);need(len(paths)==2,'actual arrow shaft and head');v=nums(paths[0].get('d'));head=nums(paths[1].get('d'));need(len(v)==6 and len(head)==6,'actual curve/triangle')
        need(('stroke-dasharray'in paths[0].get('style',''))==(kind in ['optional_check','correspondence']),'actual optional/correspondence line style')
        A=(POS[a][0],440-POS[a][1]);B=(POS[b][0],440-POS[b][1]);dx,dy=B[0]-A[0],B[1]-A[1];norm=math.hypot(dx,dy);t=min(77/abs(dx)if dx else 100,23/abs(dy)if dy else 100)
        for x,y in zip(v[::2],v[1::2]):need(abs((x-A[0])*dy-(y-A[1])*dx)/norm<.02,'arrow belongs to actual source-target line')
        start=(A[0]+t*dx,A[1]+t*dy);end=(B[0]-t*dx,B[1]-t*dy)
        need(abs(math.hypot(v[0]-start[0],v[1]-start[1])-2)<.025,'arrow source boundary')
        need(abs(math.hypot(v[4]-end[0],v[5]-end[1])-(2+.8*math.sqrt(1.25)))<.025,'arrow target boundary')
        need(close(head[2],v[4])and close(head[3],v[5]),'head at actual target')
    return {'nodes':9,'arrows':11,'dashed_evidence_or_correspondence':4}
def graph_pdf(path):
    p=PdfReader(path);need(len(p.pages)==1,'one-page document graph');pg=p.pages[0];need((float(pg.mediabox.width),float(pg.mediabox.height))==(792,440),'complete document graph canvas');color=None;stack=[];points=[];boxes=[];heads=[]
    for args,op in ContentStream(pg.get_contents(),p).operations:
        if op==b'q':stack.append(color)
        elif op==b'Q':color=stack.pop()
        elif op==b'rg':color=tuple(map(float,args))
        elif op==b'g':color=(float(args[0]),)*3
        elif op==b'm':points=[tuple(map(float,args))]
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op in (b'f',b'f*',b'B',b'B*'):
            if color and all(abs(a-b)<1e-8 for a,b in zip(color,[243/255,244/255,245/255])):need(len(points)==4,'PDF graph box path');boxes.append(points)
            if color and all(abs(a-b)<1e-8 for a,b in zip(color,[82/255,98/255,114/255])):need(len(points)==3,'PDF arrow head path');heads.append(points)
            points=[]
        elif op in (b'n',b'S'):points=[]
    need(len(boxes)==9 and len(heads)==11,'actual PDF graph nodes/arrows')
    for x,y in POS.values():need(sum(all(close(a,b)for pt,want in zip(row,[(x-77,y-23),(x+77,y-23),(x+77,y+23),(x-77,y+23)])for a,b in zip(pt,want))for row in boxes)==1,'each expected PDF box')
    return {'nodes':len(boxes),'arrowheads':len(heads)}
def rounded(q):
    n,d=q['numerator'],q['denominator'];v,r=divmod(n*10**6,d)
    if 2*r>d or 2*r==d and v%2:v+=1
    return f'{v//10**6}.{v%10**6:06d}'
def reader_check(packet,rows):
    tex=(packet/'reader.tex').read_text();pages=PdfReader(packet/'reader.pdf').pages;need(len(pages)==3,'whole reader three pages');texts=[p.extract_text()for p in pages];text=' '.join(' '.join(texts).split());p=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==PRIMARY)
    need('This is expansion, not achieved whole-topic compression.'in text,'actual rendered expansion disclosure')
    for q in p['comparisons'].values():need(rounded(q)in texts[0],'primary rounded exact fraction')
    labels=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed characters','Collapsed UTF-8 bytes']
    for label,unit in zip(labels,UNITS):
        r=next(r for r in rows if r['variant']=='calibrated_selected'and r['normalization']=='NFC'and r['unit']==unit);line=label+' & '+' & '.join(rounded(r['comparisons'][k])for k in COMPARE)
        need(line in tex,'exact six-place sensitivity '+label)
        for k in COMPARE:need(rounded(r['comparisons'][k])in texts[2],'rendered sensitivity '+label)
    raw=next(r for r in rows if r['variant']=='raw_untrimmed'and r['normalization']=='NFC'and r['unit']==UNITS[2]);need(rounded(raw['comparisons']['written'])in texts[2],'rounded raw sensitivity')
    for phrase in ['Neither application is','The nine optional checks are not acquisition prerequisites.','These are actual','proof inputs','Software-inclusive factors are unknown,','The broader Section','programmes are not claimed solved.']:need(phrase in text,'actual reader scope '+phrase)
    return {'pages':3,'rounded_fraction_displays':19,'page_text_sha256':[sha(t.encode())for t in texts]}
def reject(name,fn):
    try:fn()
    except (ValueError,KeyError):return {'name':name,'rejected':True}
    raise ValueError('negative control accepted '+name)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--author-root',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh review output');a.out.mkdir(parents=True);packet=a.author_root;study=a.study_root
    exports=verify_packet(packet);protocol=read(packet/'protocol.json');oracle=derive(study)
    for r in protocol['inputs']:
        data=(packet/r['path']).read_bytes();need(len(data)==r['bytes']and sha(data)==r['sha256']and data==(study/r['source_packet']/r['source_export']).read_bytes(),'copied accepted input '+r['path'])
    result=read(packet/'results.json');rows=check_result(result,oracle,study,protocol);counts=read(study/'topic_Representation_L126_measurement_independent_review/independent_counts.json')
    for r in result['raw_file_inventory']['files']:
        b=(study/r['path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'whole raw file '+r['key'])
    csv_counts=csv_checks(packet,rows,counts,result['raw_file_inventory']);geom=geometry(packet,oracle);plot_data_check(read(packet/'plot_data.json'),oracle);g=read(packet/'document_graph.json');graph_data(g,oracle);gs=graph_svg((packet/'document_graph.svg').read_text());gp=graph_pdf(packet/'document_graph.pdf');rr=reader_check(packet,rows);need(read(packet/'acquisition.json')==result['acquisition'],'separate exact acquisition')
    negative=controls(result,oracle,study,protocol)
    bar=svg((packet/'costs.svg').read_text());want=expected(oracle,'costs')[2];changed=copy.deepcopy(bar);changed.pop(next(iter(changed)));negative.append(reject('missing_actual_bar',lambda:compare(changed,want)));changed2=copy.deepcopy(bar);changed2[next(iter(changed2))][3]+=1;negative.append(reject('wrong_actual_bar_height',lambda:compare(changed2,want)))
    bad=copy.deepcopy(g);bad['edges'].append({'source':'R1','target':'R2','kind':'common'});negative.append(reject('graph_hidden_sibling',lambda:graph_data(bad,oracle)));bad2=copy.deepcopy(g);bad2['nodes']=[x for x in bad2['nodes']if x['id']!='data'];negative.append(reject('graph_omit_required_JSON',lambda:graph_data(bad2,oracle)))
    xml=(packet/'document_graph.svg').read_text().replace('id="edge-data-certificate"','id="lost-data-certificate"');negative.append(reject('missing_drawn_required_arrow',lambda:graph_svg(xml)))
    xml2=(packet/'document_graph.svg').read_text().replace('stroke-dasharray: 2.96,1.28;','');negative.append(reject('optional_drawn_as_solid_premise',lambda:graph_svg(xml2)))
    report={'status':'PASS_DISTINCT_NUMERICAL_REVIEW','author_manifest_sha256':PIN,'author_exports':exports,'accepted_input_cells':350,'coordinates':30,'whole_written_fractions':30,'conditional_fractions':60,'CSV_rows':csv_counts,'whole_raw_file_hashes':17,'actual_vectors':geom,'document_graph_SVG':gs,'document_graph_PDF':gp,'reader':rr,'negative_controls':negative,'primary':oracle['primary'],'all_whole_sensitivity_factors_below_one':all(r['comparisons']['written']['numerator']<r['comparisons']['written']['denominator']for r in rows),'fresh_source_extraction':False,'science_replayed':False,'software_inclusive_factor':None}
    (a.out/'independent_derivation.json').write_text(json.dumps(oracle,indent=2,ensure_ascii=False)+'\n');(a.out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':report['status'],'fractions':90,'CSV_rows':sum(csv_counts.values()),'bars_each_format':15,'controls':len(negative)}))
if __name__=='__main__':main()
