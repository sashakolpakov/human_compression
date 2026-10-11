#!/usr/bin/env python3
"""Independent overview43 arithmetic, partition and vector checks.
No import of overview author arithmetic, plotting or geometry helpers.
"""
import argparse,copy,csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream
NS={'s':'http://www.w3.org/2000/svg'}
SOFTWARE=['including_printed_programs','including_raw_programs','including_optional_validation']
def need(v,s):
    if not v:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decimal(n,d,places=12):
    q,r=divmod(n*10**places,d)
    if 2*r>d or 2*r==d and q%2:q+=1
    return str(q//10**places)+'.'+str(q%10**places).zfill(places)
def ratio(n,d):
    g=math.gcd(n,d);nn,dd=n//g,d//g
    return {'numerator':n,'denominator':d,'exact_fraction':str(nn)if dd==1 else f'{nn}/{dd}','decimal':decimal(n,d)}
def check_results(result,old,f,catalogue):
    need(result['topic_count']==len(result['topics'])==19,'nineteen topics')
    need(result['pooled_factor']is None and not result['cross_topic_deduplication'],'no pooling or free overlap')
    need(not result['software_inclusive_comparisons_available'],'no asymmetric software claim')
    oldby={x['topic']:x for x in old['topics']};ids=[];fractions=[]
    need(len(oldby)==19 and len(old['original_ids']if'original_ids'in old else [q['source']for t in old['topics']for q in t['pairs']])==42,'42 baseline')
    for t in result['topics']:
        s=sum(q['source_cost']for q in t['pairs']);a=sum(q['application_cost']for q in t['pairs']);u=sum(t['common_components'].values())
        need((s,a,u)==(t['source_sum'],t['applications_sum'],t['common_theory']),'complete paper sums')
        need(t['written_denominator']==u+a and t['written']==ratio(s,u+a),'whole-topic fraction')
        need(t['source_count']==len(t['pairs']) and t['source_ids']==[q['source']for q in t['pairs']],'topic source membership')
        fractions.append(t['written'])
        for q in t['pairs']:
            ids.append(q['source']);need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'conditional fraction')
            if'application_components'in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'complete companion sums')
            fractions.append(q['conditional'])
        need(all(t[k]is None for k in SOFTWARE),'software fields unavailable')
        if t['topic']!='F':
            expected=copy.deepcopy(oldby[t['topic']])
            for k in SOFTWARE:expected[k]=None
            expected['historical_acquisition_inventory']=expected.pop('conditional_prepaid')
            if'conditional_raw_alternative_prepaid'in expected:expected['historical_raw_acquisition_inventory']=expected.pop('conditional_raw_alternative_prepaid')
            expected.update(software_comparison_status='UNAVAILABLE_UNTIL_BOTH_SIDES_INVENTORIED',written_comparison_scope='Complete manuscript lengths at the stated representation; separate programs excluded on both sides.',embedded_validation_listings_screened=False,conditional_assumption='Whole common theory and the declared required dependencies already acquired. Optional validation is not a mathematical premise.')
            need(t==expected,'unrelated topic metadata or mathematics changed '+t['topic'])
        else:
            c=f['primary']['costs'];need(t['source_ids']==['L014','L007'],'F exact originals')
            need((s,u,a)==(c['L014']+c['L007'],c['U'],c['A1']+c['A2']),'accepted F cost closure')
            for q,k in zip(t['pairs'],['A1','A2']):need(q['source_cost']==c[q['source']]and q['application_cost']==c[k],'accepted F paired costs')
            need(t['representation']=='raw_untrimmed_pdf'and t['normalization']=='NFC'and t['unit']=='characters_without_whitespace','F coordinate')
            need(t['printed_program_cost']==c['CODE']and t['raw_program_alternative']==f['primary']['raw_costs']['programs'],'full F programs disclosed')
            need(f['boundary']['uniform_finite_premise_programs']==0 and f['boundary']['validation_programs']==9,'accepted F validation role')
            need(t['optional_validation_printed']==c['CODE'] and t['validation_cost_already_in_printed_inventory'] is True,'F validation inventory not duplicated')
            need(t['embedded_validation_listings_screened'] is True and t['source_dispositions']==63 and t['whole_common_pages']==7 and t['application_pages']==[5,6],'accepted F scope and full-page boundary')
            need(t['program_roles']=='Nine complete optional validation files; no program is a premise of a uniform proof. Four drivers and three Lean files are separate.','F exact program roles')
            need(t['conditional_assumption']=='Whole common theory and retained mathematical premises acquired; all nine programs are optional validation.','F actual conditional premises')
            need(t['historical_software_cost']is None and t['external_proof_cost']is None and t['complete_graphic_cost']is None and t['full_formalization_cost']is None,'unknown costs not zero')
            need(t['formal_declarations']==12 and t['new_generic_declarations']==3 and not t['full_source_formalized'],'bounded F formal evidence')
    need(len(ids)==len(set(ids))==43 and ids.count('L014')==ids.count('L007')==1,'43 unique originals')
    need(sorted(ids)==result['original_ids']==catalogue['measured_original_ids'],'programme partition')
    oldids={q['source']for t in old['topics']for q in t['pairs']};need(set(ids)-oldids=={'L007'}and oldids-set(ids)==set(),'only L007 added')
    need(len(fractions)==result['written_and_conditional_comparisons']==62,'62 comparisons')
    need(result['active_originals']==106 and result['accessible_pending_originals']==63 and result['archived_unavailable_originals']==55,'active partition')
    return fractions

def check_csv(out,result):
    read=lambda name:list(csv.DictReader((out/name).open(newline='')))
    topics=read('topics.csv');apps=read('applications.csv');programs=read('program_inventory.csv')
    need(len(topics)==len(programs)==19 and len(apps)==43,'CSV row counts')
    aq=iter(apps)
    for t,row,pr in zip(result['topics'],topics,programs):
        need(row==dict(topic=t['topic'],title=t['title'],originals=str(t['source_count']),representation=t['representation'],sources=str(t['source_sum']),common=str(t['common_theory']),applications=str(t['applications_sum']),written=str(t['written_denominator']),factor=t['written']['decimal']),'topic CSV')
        for q in t['pairs']:
            r=next(aq);need(r==dict(topic=t['topic'],source=q['source'],application=q['application'],source_cost=str(q['source_cost']),application_cost=str(q['application_cost']),conditional_exact=q['conditional']['exact_fraction'],conditional_factor=q['conditional']['decimal'],whole_common_cost=str(t['common_theory']),assumption=t['conditional_assumption']),'application CSV')
        def st(v):return ''if v is None else str(v)
        need(pr==dict(topic=t['topic'],printed_programs=st(t['printed_program_cost']),raw_programs=st(t['raw_program_alternative']),mandatory_data=st(t.get('mandatory_data_cost')),optional_printed=st(t.get('optional_validation_printed')),optional_already_in_printed=str(t.get('validation_cost_already_in_printed_inventory',False)),source_software_cost='unknown',symmetric_software_factor='unknown',roles=t.get('program_roles','')),'program CSV exact disclosure')
    return 81

def expected_specs(r):
    whole=[];cond=[]
    for t in r['topics']:
        own=[]
        for q in t['pairs']:
            seg=[(q['application']+'-'+k,v)for k,v in t.get('application_components',{}).get(q['application'],{q['application']:q['application_cost']}).items()]
            own+=seg;cond.append((t['topic']+'-'+q['source'],q['source_cost'],seg))
        whole.append((t['topic'],t['source_sum'],[('common-'+k,v)for k,v in t['common_components'].items()]+own))
    return {'whole_topics':whole,'conditional_1':cond[:21],'conditional_2':cond[21:]}

def svg_geometry(path,rows):
    xml=ET.fromstring(path.read_bytes(),parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    ticks=[]
    for node in xml.findall('.//s:g',NS):
        if node.get('id','').startswith('xtick_'):
            labels=[x.text.strip()for x in node.iter()if x.tag is ET.Comment]
            numeric=[v for v in labels if re.fullmatch(r'[\d,]+',v)]
            line=node.find('.//s:path',NS)
            if numeric and line is not None:
                xy=[float(v)for v in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?',line.get('d',''))]
                ticks.append((int(numeric[0].replace(',','')),xy[0]))
    ticks.sort();need(len(ticks)>=2 and ticks[0][0]==0,'visible zero-based numeric ticks')
    scale=(ticks[-1][1]-ticks[0][1])/(ticks[-1][0]-ticks[0][0]);origin=ticks[0][1]
    for value,x in ticks:need(abs(x-(origin+value*scale))<2e-6,'linear numeric ticks')
    rects={}
    for node in xml.findall('.//s:g',NS):
        key=node.get('id','')
        if not key.startswith('bar-'):continue
        paths=node.findall('s:path',NS);need(len(paths)==1 and key not in rects,'one actual path per bar')
        d=paths[0].get('d','');nums=[float(v)for v in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?',d)]
        need(len(nums)==8,'four bar vertices')
        x0,y0,x1,y1,x2,y2,x3,y3=nums
        need(abs(y0-y1)+abs(x1-x2)+abs(y2-y3)+abs(x0-x3)<1e-6,'actual rectangle')
        rects[key]=[min(x0,x1),min(y0,y2),abs(x1-x0),abs(y2-y0)]
    expected=set();ys=[];heights=[]
    for key,source,segments in rows:
        sourcekey='bar-'+key+'-source';expected.add(sourcekey);r=rects[sourcekey]
        need(abs(r[0]-origin)<2e-6 and abs(r[2]-source*scale)<8e-6,'source actual width '+key)
        heights.append(r[3]);ys.append(r[1]);running=0;ay=None
        for name,value in segments:
            rid='bar-'+key+'-'+name;expected.add(rid);rr=rects[rid]
            need(abs(rr[0]-origin-running*scale)<8e-6 and abs(rr[2]-value*scale)<8e-6,'complete segment actual width '+rid)
            need(rr[1]>r[1]and abs(rr[3]-r[3])<2e-6,'bar pairing')
            if ay is None:ay=rr[1]
            need(abs(ay-rr[1])<1e-6,'same stacked row');running+=value
    need(set(rects)==expected,'exact actual bar membership')
    need(all(a<b for a,b in zip(ys,ys[1:]))and max(heights)-min(heights)<2e-6,'source ordering and heights')
    return rects,float(xml.get('viewBox').split()[3]),{'scale_from_visible_ticks':scale,'zero':origin,'bars':len(rects)}

def pdf_geometry(path,svgrects,H):
    pdf=PdfReader(path);need(len(pdf.pages)==1,'graph is single page');page=pdf.pages[0]
    stack=[];fill=None;points=[];rects=[];matrix=(1.,0.,0.,1.,0.,0.)
    def transform(p):
        x,y=map(float,p);a,b,c,d,e,f=matrix;return(a*x+c*y+e,b*x+d*y+f)
    colors={(52,67,84),(40,110,153),(129,189,176),(97,162,148)}
    for args,op in ContentStream(page.get_contents(),page.pdf).operations:
        if op==b'q':stack.append((fill,matrix))
        elif op==b'Q':fill,matrix=stack.pop()
        elif op==b'rg':fill=tuple(round(float(v)*255)for v in args)
        elif op==b'm':points=[transform(args)]
        elif op==b'l':points.append(transform(args))
        elif op==b're':points=[]
        elif op in (b'f',b'B',b'f*',b'B*'):
            if fill in colors and len(points)==4:
                xs=[p[0]for p in points];ys=[p[1]for p in points]
                if len(set(xs))==len(set(ys))==2:rects.append([min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)])
            points=[]
        elif op in (b'S',b'n'):points=[]
        elif op==b'cm':
            a,b,c,d,e,f=matrix;A,B,C,D,E,F=map(float,args)
            matrix=(a*A+c*B,b*A+d*B,a*C+c*D,b*C+d*D,a*E+c*F+e,b*E+d*F+f)
    need(abs(float(page.mediabox.height)-H)<1e-6,'same page geometry')
    for key,(x,y,w,h)in svgrects.items():
        target=[x,H-y-h,w,h];hits=[i for i,r in enumerate(rects)if max(abs(a-b)for a,b in zip(r,target))<2e-6]
        need(len(hits)==1,'literal PDF rectangle '+key);rects.pop(hits[0])
    need(len(rects)==(3 if 'whole_topics'in path.name else 2),'only colored legend rectangles remain')


def check_catalogues(previous,current):
    old={r['original_id']:r for r in previous['entries']};new={r['original_id']:r for r in current['entries']}
    need(len(old)==len(new)==106 and set(old)==set(new),'exact106 active originals')
    changed=[k for k in old if old[k]!=new[k]];need(set(changed)=={'L014','L007'},'only two source records changed')
    return changed

def check_reader(path,result):
    pages=[p.extract_text() for p in PdfReader(path).pages];need(len(pages)==6,'six reader pages')
    names={'Representation':'Represent.','ChiralEnumeration':'Chiral','RankContraction':'Rank contr.','LocallyProjective':'Locally proj.','MathieuCensus':'Mathieu','RankAugmentation':'Rank augm.'}
    num=lambda x:'–'if x is None else f'{x:,}'
    count=0
    for t in result['topics']:
        name=names.get(t['topic'],t['topic'])
        cells=[name,str(t['source_count'])]+[num(t[k]) for k in ['source_sum','common_theory','applications_sum','written_denominator']]+[decimal(t['source_sum'],t['written_denominator'],3)]
        need(' '.join(cells) in pages[0].splitlines(),'actual PDF complete topic row '+name);count+=1
        for q in t['pairs']:
            cells=[name,q['source'],q['application'],num(q['source_cost']),num(q['application_cost']),decimal(q['source_cost'],q['application_cost'],3)]
            need(' '.join(cells) in pages[2].splitlines(),'actual PDF full application row '+q['source']);count+=1
        cells=[name,num(t['printed_program_cost']),num(t['raw_program_alternative']),num(t.get('mandatory_data_cost'))]
        need(' '.join(cells) in pages[5].splitlines(),'actual PDF software inventory '+name);count+=1
    return {'pages':6,'actual_PDF_table_rows':count,'page_text_hashes':[hashlib.sha256(t.encode()).hexdigest()for t in pages]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--artifacts',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh review output');a.out.mkdir(parents=True)
    m=a.candidate/'manifest.json';need(sha(m)=='4da624cc48c891c089e05823f88c218a4113f2ad5319fd632c5479dfffc2c26a','accepted author freeze')
    exports=load(m)['exports'];need(len(exports)==39,'39 frozen exports')
    for b in exports:
        rel=Path(b['path']);need(not rel.is_absolute()and '..'not in rel.parts,'safe export');p=a.candidate/rel
        need(p.stat().st_size==b['bytes']and sha(p)==b['sha256'],'frozen export '+b['path'])
    proto=load(a.candidate/'protocol.json');ins={}
    for key,b in proto['inputs'].items():
        p=a.candidate/b['path'];need(p.stat().st_size==b['bytes']and sha(p)==b['sha256'],'input binding '+key);ins[key]=load(p)
    for key,b in proto['inputs'].items():
        raw=subprocess.check_output(['git','show',proto['baseline_commit']+':'+b['public_path']],cwd=a.public_root) if b.get('committed_baseline') else (a.public_root/b['public_path']).read_bytes()
        need(len(raw)==b['bytes']and hashlib.sha256(raw).hexdigest()==b['sha256'],'public accepted input '+key)
    for label,key in [('previous','previous_corpus'),('current','current_corpus')]:
        need(proto['external_catalogue_bindings'][label]==ins[key]['active_catalogue'],'explicit and inherited catalogue binding')
    result=load(a.artifacts/'results.json');fractions=check_results(result,ins['previous_results'],ins['F_results'],ins['current_corpus']);csvrows=check_csv(a.artifacts,result)
    oldb=ins['previous_corpus']['active_catalogue'];newb=ins['current_corpus']['active_catalogue'];cats=[]
    for b in (oldb,newb):
        p=a.public_root/b['path'];need(p.stat().st_size==b['bytes']and sha(p)==b['sha256'],'actual106 catalogue binding');cats.append(load(p))
    changed=check_catalogues(*cats)
    reader=check_reader(a.artifacts/'summary.pdf',result)
    specs=expected_specs(result);vectors={}
    for name,rows in specs.items():
        rectangles,H,rec=svg_geometry(a.artifacts/(name+'.svg'),rows);pdf_geometry(a.artifacts/(name+'.pdf'),rectangles,H);vectors[name]=rec
    report={'status':'PASS','independent_arithmetic':'integer gcd and integer ties-to-even rounding; no author imports','exact_fractions':len(fractions),'CSV_rows':csvrows,'topic_count':19,'originals':43,'unchanged_topic_costs':18,'unchanged_active_records':104,'changed_records':changed,'reader':reader,'vector_charts':vectors,'SVG_bars':sum(v['bars']for v in vectors.values()),'PDF_bars':sum(v['bars']for v in vectors.values()),'software_inclusive_factors':None,'source_software_cost':None,'new_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
