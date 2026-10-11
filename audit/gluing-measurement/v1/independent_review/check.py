#!/usr/bin/env python3
"""Distinct arithmetic and visible vector checks; no author implementation imports."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,math,re
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='d52e82dc1b613ae9cb9f43937bc514f7818b3da92a58c3ffd87eccfbb611bc80'
IPIN='0b82b7ba065bacb6ccfac7515667503617c57ec0db1f810a064dcf23468be9c1'
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']
FORMS=['NFC','NFKC']
def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frozen(p,pin):
    need(sha(p/'manifest.json')==pin,'frozen manifest')
    for r in load(p/'manifest.json')['exports']:
        f=p/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'exact export '+r['path'])
def ratio(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=f'{q//10**12}.{q%10**12:012d}')
def arithmetic(data,recount):
    need(data['source_ids']==['L010'] and data['source_records']==23,'one original, not23 originals')
    need(data['whole_documents']==['L010','U1','U2','A1','CODE'] and data['physical_pages']==[15,5,6,5,4],'all complete documents')
    rows=data['coordinates'];need(len(rows)==30,'thirty coordinates')
    coords=[(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS]
    need([(r['variant'],r['normalization'],r['unit'])for r in rows]==coords,'complete coordinate order')
    for r,(v,f,u) in zip(rows,coords):
        costs={k:recount['documents'][k]['metrics'][v][f][u]for k in ['L010','U1','U2','A1','CODE']}
        raw={k:sum(z['metrics'][f][u]for z in files.values())for k,files in recount['raw_files'].items()}
        need(r['costs']==costs and r['raw_costs']==raw,'independent full-document costs')
        s=costs['L010'];common=costs['U1']+costs['U2'];app=costs['A1'];w=common+app
        need(r['totals']==dict(source=s,common=common,applications=app,written=w,with_printed_programs=w+costs['CODE'],with_raw_programs=w+raw['programs']),'complete distinct denominators')
        den={'written':w,'including_printed_programs':w+costs['CODE'],'including_raw_programs':w+raw['programs'],'conditional_application':app}
        need(r['comparisons']=={k:ratio(s,d)for k,d in den.items()},'all exact integer fractions')
        need(r['conditional_acquisition']==dict(whole_common_papers=['U1','U2'],common_cost=common,printed_program_package=costs['CODE'],raw_program_package_alternative=raw['programs'],complete_local_application=app),'whole prepaid common and software')
    need(data['primary']==rows[22],'primary calibrated NFC nonspace coordinate')
    b=data['boundary']
    need(b['whole_common_once']==['U1','U2'] and b['whole_application'] and not b['old_B_common_imported'] and not b['cross_topic_discount'],'whole common boundary')
    need(b['whole_validation_programs']==3 and b['uniform_finite_program_premises']==0 and b['separate_drivers']==3 and b['separate_formal_files']==2 and b['partial_Lean_declarations']==10 and not b['whole_source_formalized'],'program and formal roles')
    need(b['unknown_costs']==dict(full_graphics=None,historical_software=None,retained_external_proofs=None,full_formalization=None),'unknown remains unknown')
    need((data['coordinate_count'],data['exact_fraction_count'],data['combined_fractions'],data['conditional_fractions'])==(30,120,90,30),'complete totals')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no mathematical credits')
    return 120
def csvs(packet,data):
    costs=list(csv.DictReader((packet/'costs.csv').open()));fractions=list(csv.DictReader((packet/'fractions.csv').open()))
    ec=[];ef=[]
    for r in data['coordinates']:
        c={k:r[k]for k in ['variant','normalization','unit']}
        for k,v in r['costs'].items():ec.append(dict(c,kind='PDF',component=k,cost=str(v)))
        for k,v in r['raw_costs'].items():ec.append(dict(c,kind='raw_file_group',component=k,cost=str(v)))
        for k,v in r['comparisons'].items():ef.append(dict(c,comparison=k,**{a:str(b)for a,b in v.items()}))
    need(costs==ec and fractions==ef,'all CSV cells and row order')
    return len(costs)+len(fractions)
def numbers(s):return list(map(float,re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',s)))
def svg_groups(path,prefix):
    return {x.get('id'):[y for y in x if y.tag.endswith('path')]for x in ET.parse(path).iter()if x.get('id','').startswith(prefix)}
def rect(path):
    d=path.get('d');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','rectangle path')
    p=numbers(d);need(len(p)==8,'four rectangle vertices');xs=p[::2];ys=p[1::2]
    need(len(set(xs))==len(set(ys))==2,'axis aligned rectangle')
    return min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
def bar_geometry(rects,c,raw):
    wanted={'cost-source-L010':c['L010'],**{'cost-written-'+k:c[k]for k in ['U1','U2','A1']},**{'cost-component-'+k:c[k]for k in ['U1','U2','A1','CODE']},'cost-component-raw-programs':raw['programs']}
    need(set(rects)==set(wanted),'nine visible bars')
    x,y,w,h=rects['cost-source-L010'];base=y+h;scale=h/c['L010'];bottom=base
    wx=rects['cost-written-U1'][0]
    need(wx>x+w,'distinct source and written bars')
    for k in ['U1','U2','A1']:
        xx,yy,ww,hh=rects['cost-written-'+k]
        need(abs(xx-wx)<1e-6 and abs(ww-w)<1e-6 and abs(yy+hh-bottom)<2e-6 and abs(hh-scale*c[k])<2e-6,'actual written stack costs')
        bottom=yy
    cx,cy,cw,ch=rects['cost-component-U1'];scale2=ch/c['U1'];step=rects['cost-component-U2'][0]-cx
    need(scale>0 and scale2>0 and step>cw,'positive bars and separate components')
    for i,k in enumerate(['U1','U2','A1','CODE','raw-programs']):
        xx,yy,ww,hh=rects['cost-component-'+k];cost=wanted['cost-component-'+k]
        need(abs(xx-cx-i*step)<3e-6 and abs(ww-cw)<2e-6 and abs(yy+hh-base)<2e-6 and abs(hh-scale2*cost)<2e-6,'actual component geometry')
    return 9
def pdf_polygons(path,colors,vertices):
    reader=PdfReader(path);need(len(reader.pages)==1,'single figure PDF');page=reader.pages[0]
    rgb=None;stack=[];points=[];out=[];curved=False
    for args,op in ContentStream(page.get_contents(),reader).operations:
        if op==b'q':stack.append(rgb)
        elif op==b'Q':rgb=stack.pop()
        elif op==b'rg':rgb=tuple(round(float(a),6)for a in args)
        elif op==b'g':rgb=(round(float(args[0]),6),)*3
        elif op==b'm':points=[tuple(map(float,args))];curved=False
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op in [b'c',b'v',b'y']:curved=True
        elif op in [b'f',b'f*',b'B',b'B*']:
            if rgb in colors and len(points)==vertices and not curved:out.append((rgb,points))
            points=[]
        elif op in [b'n',b'S']:points=[]
    return out,float(page.mediabox.height)
def color(hexvalue):return tuple(round(int(hexvalue[i:i+2],16)/255,6)for i in [0,2,4])
def compare_pdf_bars(packet,groups,c,raw):
    palette={color(x)for x in ['687785','426b9a','7c8eb4','70a59a','bd874e','d4b38f']}
    actual,height=pdf_polygons(packet/'costs.pdf',palette,4)
    need(len(actual)==12,'nine PDF bars plus three legends')
    bars=actual[:4]+actual[7:];legends=actual[4:7]
    keys=['cost-source-L010']+['cost-written-'+k for k in ['U1','U2','A1']]+['cost-component-'+k for k in ['U1','U2','A1','CODE','raw-programs']]
    rects={}
    for key,(rgb,pts)in zip(keys,bars):
        expected_rgb=color(re.search(r'fill: #([a-f0-9]{6})',groups[key][0].get('style'))[1])
        xs={x for x,y in pts};ys={y for x,y in pts}
        need(rgb==expected_rgb and len(xs)==len(ys)==2,'actual PDF bar role and alignment')
        rects[key]=(min(xs),height-max(ys),max(xs)-min(xs),max(ys)-min(ys))
    need({rgb for rgb,_ in legends}=={color(x)for x in ['426b9a','7c8eb4','70a59a']},'three legend colors')
    for _,pts in legends:
        need(abs(max(x for x,y in pts)-min(x for x,y in pts)-16)<2e-6 and abs(max(y for x,y in pts)-min(y for x,y in pts)-5.6)<2e-6,'actual legend swatches')
    # Constrained layout resolves font metrics separately in the PDF and SVG
    # backends. Check each figure's cost scale, not equality of canvas positions.
    return bar_geometry(rects,c,raw)
def document_graph(packet,data):
    g=load(packet/'document_graph.json');nodes={n['id']:n for n in g['nodes']};c=data['primary']['costs'];raw=data['primary']['raw_costs']
    need(set(nodes)=={'L010','U1','U2','A1','CODE','external'},'all six documents')
    need(all(nodes[k]['cost']==v for k,v in c.items()) and nodes['external']['cost']is None and nodes['CODE']['raw_alternative_cost']==raw['programs'],'visible document costs')
    edges={('U1','U2'):'proof_use',('U1','A1'):'proof_use',('U2','A1'):'proof_use',('external','A1'):'retained_proof_use',('L010','A1'):'source_correspondence',('CODE','U1'):'validation_only',('CODE','U2'):'validation_only',('CODE','A1'):'validation_only'}
    need({(e['source'],e['target']):e['kind']for e in g['edges']}==edges and len(g['edges'])==8,'all typed dependencies')
    groups=svg_groups(packet/'document_graph.svg','edge-');need(set(groups)=={'edge-'+s+'-'+t for s,t in edges},'all eight visible arrows')
    patches=svg_groups(packet/'document_graph.svg','patch_');boxes={}
    for i,k in enumerate(['L010','U1','U2','external','A1','CODE'],2):
        v=numbers(patches['patch_'+str(i)][0].get('d'));boxes[k]=(min(v[::2]),min(v[1::2]),max(v[::2]),max(v[1::2]))
    def distance(pt,box):
        x,y=pt;l,t,r,b=box
        return math.hypot(max(l-x,0,x-r),max(t-y,0,y-b))
    triangles=[]
    for (s,t),kind in edges.items():
        paths=groups['edge-'+s+'-'+t];need(len(paths)==2,'visible shaft and arrowhead')
        shaft=numbers(paths[0].get('d'));head=numbers(paths[1].get('d'));need(len(shaft)==6 and len(head)==6,'quadratic shaft and triangle head')
        need(all(abs(a-b)<1e-6 for a,b in zip(shaft[-2:],head[2:4])),'arrowhead at target end')
        need(1<distance(shaft[:2],boxes[s])<8 and 1<distance(head[2:4],boxes[t])<8,'arrow connects actual source and target boxes')
        dashed='stroke-dasharray' in paths[0].get('style','')
        need(dashed==(kind in ['source_correspondence','validation_only']),'visible proof/validation distinction')
        triangles.append((color('8a969d' if dashed else '435561'),list(zip(head[::2],head[1::2]))))
    actual,height=pdf_polygons(packet/'document_graph.pdf',{color('8a969d'),color('435561')},3)
    need(len(actual)==8,'eight actual PDF arrowheads')
    for c,pts in triangles:
        target=sorted((x,height-y)for x,y in pts)
        ix=[i for i,(rgb,p)in enumerate(actual)if rgb==c and all(abs(a-b)<3e-6 for p,q in zip(sorted(p),target)for a,b in zip(p,q))]
        need(len(ix)==1,'actual PDF arrowhead matches SVG');actual.pop(ix[0])
    return 8
def acquisition(packet,data):
    a=load(packet/'acquisition.json');p=data['primary'];c=p['costs'];raw=p['raw_costs']
    need(len(a['routes'])==2,'two acquisition representations')
    for route,rep in zip(a['routes'],['printed','raw']):
        code=c['CODE']if rep=='printed'else raw['programs'];inc=[c['U1'],c['U2'],code,c['A1']];total=0
        need(route['program_representation']==rep and len(route['steps'])==4,'one whole route')
        for step,name,v in zip(route['steps'],['U1','U2','complete_validation_package','A1'],inc):
            total+=v;need(step==dict(acquired=name,increment=v,total=total),'each common/whole program paid once')
        need(route['total']==total,'acquisition total')
    need(a['conditional_application_cost']==c['A1'] and a['source_cost']==c['L010'] and a['external_proof_cost']is None and a['graphics_cost']is None,'qualified acquisition')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    frozen(a.packet,PIN);frozen(a.input_review,IPIN)
    data=load(a.packet/'results.json');recount=load(a.input_review/'recount.json')
    nf=arithmetic(data,recount);nc=csvs(a.packet,data);acquisition(a.packet,data)
    groups=svg_groups(a.packet/'costs.svg','cost-');rects={k:rect(p[0])for k,p in groups.items()}
    nb=bar_geometry(rects,data['primary']['costs'],data['primary']['raw_costs']);np=compare_pdf_bars(a.packet,groups,data['primary']['costs'],data['primary']['raw_costs']);ne=document_graph(a.packet,data)
    controls=[]
    for label,mut in [('omit source',lambda d:d.update(source_ids=[])),('omit common',lambda d:d['coordinates'][0]['costs'].update(U2=0)),('omit prepaid program',lambda d:d['coordinates'][0]['conditional_acquisition'].update(printed_program_package=0)),('omit coordinate',lambda d:d['coordinates'].pop()),('corrupt ratio',lambda d:d['coordinates'][0]['comparisons']['written'].update(denominator=1)),('wrong primary',lambda d:d.update(primary=d['coordinates'][0])),('unknown costs zero',lambda d:d['boundary']['unknown_costs'].update(full_graphics=0)),('invent full Lean',lambda d:d['boundary'].update(whole_source_formalized=True)),('cross-topic discount',lambda d:d['boundary'].update(cross_topic_discount=True)),('validation as premise',lambda d:d['boundary'].update(uniform_finite_program_premises=3))]:
        bad=copy.deepcopy(data);mut(bad)
        try:arithmetic(bad,recount)
        except ValueError:controls.append(label)
        else:raise ValueError('accepted negative control '+label)
    bad=copy.deepcopy(rects);x,y,w,h=bad['cost-written-U2'];bad['cost-written-U2']=(x,y,w,h+1)
    try:bar_geometry(bad,data['primary']['costs'],data['primary']['raw_costs'])
    except ValueError:controls.append('distorted visible common bar')
    else:raise ValueError('accepted distorted bar')
    reader=PdfReader(a.packet/'reader.pdf');need(len(reader.pages)==2,'two complete reader pages')
    text='\n'.join(p.extract_text()for p in reader.pages)
    need(all(str(x)in text for x in [27081,12299,16117,11565,39981,13371,12768,53352,52749]),'visible complete-document amounts')
    need(all(str(x)in text for x in ['0.677347','0.507591','0.513394','2.341634']),'visible factors')
    report=dict(status='PASS_DISTINCT_GLUING_NUMERICAL',author_manifest_sha256=PIN,input_review_manifest_sha256=IPIN,
        independent_recount_used=True,author_implementation_imported=False,coordinates=30,exact_fractions=nf,
        CSV_rows=nc,actual_SVG_bars=nb,actual_PDF_bars=np,visible_document_nodes=6,visible_typed_arrows=ne,
        actual_PDF_arrowheads=8,reader_pages=2,controls_rejected=controls,new_scientific_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
