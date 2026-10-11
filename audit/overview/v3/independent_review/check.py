#!/usr/bin/env python3
"""Independent consolidation arithmetic and actual vector geometry."""
from pathlib import Path
import argparse, copy, csv, hashlib, importlib.util, json, math, re, subprocess
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='cef9498931b3abd646babe4cdbdb8e15ee87cf5a52c25febee7ff9e3239a83e0'

def need(ok,message):
    if not ok: raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def ratio(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(n//g) if d==g else f'{n//g}/{d//g}',decimal=f'{q//10**12}.{q%10**12:012d}')

def svg_rects(raw):
    out={}
    for element in ET.fromstring(raw).iter():
        key=element.get('id','')
        if not key.startswith('bar-'):continue
        need(key not in out,'duplicate vector ID')
        paths=[x for x in element if x.tag.endswith('path')];need(len(paths)==1,'one rectangle per bar')
        d=paths[0].get('d','');need(re.sub(r'[-+\d.eE\s]','',d)=='MLLLz','literal rectangle path')
        nums=list(map(float,re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',d)))
        need(len(nums)==8,'rectangle coordinates');xs=nums[::2];ys=nums[1::2]
        need(len(set(xs))==len(set(ys))==2,'axis alignment')
        out[key]=(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
    return out

def svg_costs(actual,bars):
    need(set(actual)=={b[0] for b in bars},'vector bar completeness')
    first=bars[0];base=actual[first[0]][0];scale=actual[first[0]][2]/first[2];height=actual[first[0]][3]
    source_y={};replacement_y={}
    for key,role,cost,start,row,replacement in bars:
        x,y,w,h=actual[key]
        need(abs(w-scale*cost)<3e-6 and abs(x-base-scale*start)<3e-6 and abs(h-height)<3e-6,'actual vector costs and stacking')
        ys=replacement_y if replacement else source_y
        if row in ys:need(abs(ys[row]-y)<3e-6,'stack row alignment')
        else:ys[row]=y
    need(set(source_y)==set(replacement_y),'two rows per original')
    separation=replacement_y[0]-source_y[0];spacing=source_y[1]-source_y[0]
    need(separation>height and spacing>separation+height and scale>0,'ordered separate rows')
    for row,y in source_y.items():need(abs(y-source_y[0]-row*spacing)<3e-5 and abs(replacement_y[row]-y-separation)<3e-6,'uniform source/application row positions')
    return len(actual)

def pdf_rects(path):
    colors={tuple(round(x/255,6) for x in c):r for c,r in [((52,67,84),'source'),((40,110,153),'common'),((129,189,176),'application'),((97,162,148),'application')]}
    reader=PdfReader(path);need(len(reader.pages)==1,'single graph page');page=reader.pages[0]
    rgb=None;stack=[];points=[];rects=[]
    for args,op in ContentStream(page.get_contents(),reader).operations:
        if op==b'q':stack.append(rgb)
        elif op==b'Q':rgb=stack.pop()
        elif op==b'rg':rgb=tuple(round(float(x),6) for x in args)
        elif op==b'g':rgb=(round(float(args[0]),6),)*3
        elif op==b'm':points=[tuple(map(float,args))]
        elif op==b'l':points.append(tuple(map(float,args)))
        elif op in [b'f',b'B',b'f*',b'B*']:
            if rgb in colors and len(points)==4:
                xs={p[0] for p in points};ys={p[1] for p in points}
                need(len(xs)==len(ys)==2,'PDF rectangle')
                rects.append((colors[rgb],min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)))
            points=[]
        elif op in [b'n',b'S']:points=[]
    return rects,float(page.mediabox.height)

def pdf_costs(rects,height,svg,bars,whole):
    expected=[]
    for key,role,_,_,_,_ in bars:
        x,y,w,h=svg[key];expected.append((role,x,height-y-h,w,h))
    legend=['source','common','application'] if whole else ['source','application']
    need(len(rects)==len(expected)+len(legend),'PDF bars and legends')
    for actual,want in zip(rects,expected):
        need(actual[0]==want[0] and all(abs(a-b)<3e-6 for a,b in zip(actual[1:],want[1:])),'actual PDF bar geometry')
    tail=rects[len(expected):]
    need([p[0] for p in tail]==legend and all(p[3]>0 and p[4]>0 for p in tail),'legend swatches')
    return len(expected)
def expected(public):
    path=public/'audit/overview/v2/independent_review/check.py'
    need(sha(path)=='7b151f2166a8b866fe40a4a69b31e3ae9505ad24c2588775b9a6a8b6f1f7c70c','prior independent routes')
    spec=importlib.util.spec_from_file_location('overview33_root_routes',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    out=mod.expected(public)
    b=load(public/'audit/b-unified-measurement/v1/packet/results.json')['primary']
    d=load(public/'audit/diagonal-measurement/v2/packet/results.json')['primary']
    out['B']=dict(common={'whole_current_common':b['common_theory']},printed=b['printed_program_cost'],raw=b['raw_program_cost'],pairs=[(k,'B'+str(i+1),b['source_costs'][k],b['applications'][k]) for i,k in enumerate(['N001','N003','N008','L030','L040'])],optional=None,components={'B'+str(i+1):{'B'+str(i+1):b['applications'][k]} for i,k in enumerate(['N001','N003','N008','L030','L040'])},files=b['raw_file_costs'])
    out['Diagonal']=dict(common={'whole_current_common':d['common_theory']},printed=None,raw=d['whole_software_cost'],pairs=[(k,'DG'+str(i+1),d['original_costs'][k],d['application_costs'][k]) for i,k in enumerate(['N007','N006'])],optional=None,components={'DG1':{'N007_complete':d['document_costs']['A1']},'DG2':{k:d['document_costs'][k] for k in ['A2','A2nine','A2HN']}},files=d['raw_file_costs'])
    return out
def arithmetic(data,ex):
    need(len(data['topics'])==13 and {t['topic'] for t in data['topics']}==set(ex),'all13 topics')
    need([data[k] for k in ['original_manuscript_count','registry_manuscripts','accessible_originals','currently_admitted_originals','accessible_pending_complete_recovery','pending_source_retrieval']]==[34,161,104,34,70,57],'fixed original accounting')
    need(data['pooled_factor'] is None and data['cross_topic_deduplication'] is False and data['all_registry_manuscripts_completed'] is False,'no invented pooled or completion claim')
    need(data['unmeasured']==[] and data['pending_numerical_acceptance']==[] and data['pending_overview_review'],'immutable author-stage scope')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new mathematical credit')
    ids=[];count=0
    for t in data['topics']:
        e=ex[t['topic']];u=sum(e['common'].values());p=e['printed'];r=e['raw'];rows=e['pairs'];opt=e['optional'];ns=sum(x[2] for x in rows);na=sum(x[3] for x in rows)
        need(t['common_components']==e['common'],'all complete common papers')
        need((t['common_theory'],t['printed_program_cost'],t['raw_program_alternative'],t['source_sum'],t['applications_sum'],t['written_denominator'])==(u,p,r,ns,na,u+na),'complete costs')
        need(t['source_ids']==[x[0] for x in rows] and t['source_count']==len(rows),'source identities')
        if t['topic']=='Diagonal':
            prepaid=dict(full_common=u,full_declared_raw_software=r,total=u+r,required_external_data_already_acquired=True,external_bytes_separate=True)
            need(t['raw_program_components']==dict(nineteen_full_files=383279,both_required_decoders=11015),'all witnesses and both decoders')
            need(t['old_single_validation_printed_alternative']==3161 and t['no_complete_printed_route'] and t['graphic_proxy_sensitivities_required'],'no old single-file printed route, qualified graphics')
            need(t['external_bytes']==dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249),'separate external data')
        else:prepaid=dict(full_common=u,full_declared_printed_programs=p,total=u+p)
        need(t['conditional_prepaid']==prepaid,'complete prior acquisition')
        for key,den in [('written',u+na),('including_printed_programs',None if p is None else u+na+p),('including_raw_programs',None if r is None else u+na+r),('including_optional_validation',None if opt is None else u+na+p+opt)]:
            need(t[key]==(None if den is None else ratio(ns,den)),'exact fraction '+t['topic']+'/'+key);count+=den is not None
        need(t.get('optional_validation_printed')==opt and len(t['pairs'])==len(rows),'optional input and application count')
        for actual,want in zip(t['pairs'],rows):
            need(tuple(actual[k] for k in ['source','application','source_cost','application_cost'])==want,'actual complete application')
            need(actual['conditional']==ratio(want[2],want[3]),'conditional fraction');ids.append(want[0]);count+=1
        if t['topic'] in ['B','Diagonal']:
            need(t['application_components']==e['components'] and t['separate_raw_inventory']==e['files'],'complete companions and file costs')
        need(t['representation']==('literal_rendered_source_plus_raw_untrimmed_pdfs' if t['topic'] in ['B','C'] else 'calibrated_selected_pdf'),'exact topic representation')
        need(t['normalization']=='NFC' and t['unit']=='characters_without_whitespace','declared metric')
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknown costs null')
    need(len(ids)==len(set(ids))==34 and count==72,'unique originals and complete fractions')
    return count
def expected_bars(data,stem):
    rows=[]
    def segments(t,p):return [(p['application']+'-'+k,v,'application') for k,v in t.get('application_components',{}).get(p['application'],{p['application']:p['application_cost']}).items()]
    if stem=='whole_topics':
        for t in data['topics']:
            seg=[('common-'+k,v,'common') for k,v in t['common_components'].items()]
            for p in t['pairs']:seg.extend(segments(t,p))
            rows.append((t['topic'],t['source_sum'],seg))
    else:
        pairs=[(t,p) for t in data['topics'] for p in t['pairs']]
        for t,p in pairs[:17] if stem=='conditional_1' else pairs[17:]:rows.append((t['topic']+'-'+p['source'],p['source_cost'],segments(t,p)))
    bars=[]
    for i,(key,source,segs) in enumerate(rows):
        bars.append(('bar-'+key+'-source','source',source,0,i,False));start=0
        for name,cost,role in segs:bars.append(('bar-'+key+'-'+name,role,cost,start,i,True));start+=cost
    return bars
def graphs(packet,data):
    total=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=expected_bars(data,stem);svg=svg_rects((packet/(stem+'.svg')).read_bytes());n=svg_costs(svg,bars);rects,h=pdf_rects(packet/(stem+'.pdf'));need(pdf_costs(rects,h,svg,bars,stem=='whole_topics')==n,'actual PDF bars');total+=n
    need(total==133,'all133 actual bars');return total
def csv_check(packet,data):
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(topics)==13 and len(apps)==34,'47 CSV rows')
    def strs(d):return {k:'' if v is None else str(v) for k,v in d.items()}
    for row,t in zip(topics,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],printed_factor=None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strs(expected),'every topic CSV cell')
    for row,(t,p) in zip(apps,[(t,p) for t in data['topics'] for p in t['pairs']]):
        diag=t['topic']=='Diagonal';expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative'] if diag else t['printed_program_cost'],acquisition_representation='whole_raw_software_and_external_data' if diag else 'whole_printed_programs',source_representation=p['source_representation'])
        need(row==strs(expected),'every application CSV cell')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'author freeze')
    for z in load(a.packet/'manifest.json')['exports']:
        p=a.packet/z['path'];need(p.stat().st_size==z['bytes'] and sha(p)==z['sha256'],'exact export')
    protocol=load(a.packet/'protocol.json');need(len(protocol['bindings'])==12,'all12 bound inputs')
    locations={'B':'audit/b-unified-measurement/v1','Diagonal':'audit/diagonal-measurement/v2'}
    for key,z in protocol['bindings'].items():
        raw=(a.packet/z['local']).read_bytes();need(len(raw)==z['bytes'] and hashlib.sha256(raw).hexdigest()==z['sha256'],'input scalar binding')
        if z['commit'] is not None:other=subprocess.check_output(['git','show',z['commit']+':'+z['path']],cwd=a.public_root)
        else:
            topic=key.split('_')[0];name='manifest.json' if key.endswith('manifest') else 'review.json' if key.endswith('review') else 'results.json';folder='independent_review' if '_root_' in key else 'packet';other=(a.public_root/locations[topic]/folder/name).read_bytes()
        need(raw==other,'committed or currently admitted exact input')
    data=load(a.packet/'results.json');ex=expected(a.public_root);nf=arithmetic(data,ex);ng=graphs(a.packet,data);csv_check(a.packet,data)
    prior=load(a.packet/'inputs/previous_results.json');old={t['topic']:t for t in prior['topics']}
    need(all(t==old[t['topic']] for t in data['topics'] if t['topic'] not in ['B','Diagonal']),'all11 unchanged complete topic records')
    reader=PdfReader(a.packet/'summary.pdf');need(len(reader.pages)==6,'six complete reader pages');text='\n'.join(p.extract_text() or '' for p in reader.pages);need(all(p['source'] in text for t in data['topics'] for p in t['pairs']),'all34 originals visible')
    controls=[]
    for name,mut in [('omit common',lambda x:x['topics'][1]['common_components'].clear()),('partial acquisition',lambda x:x['topics'][1]['conditional_prepaid'].update(full_common=14124)),('omit HN companion',lambda x:x['topics'][-1]['application_components']['DG2'].pop('A2HN')),('omit decoder',lambda x:x['topics'][-1]['raw_program_components'].update(both_required_decoders=0)),('invent printed route',lambda x:x['topics'][-1].update(including_printed_programs=ratio(78889,73056))),('pool topic costs',lambda x:x.update(pooled_factor=2)),('unknown cost zero',lambda x:x['topics'][0].update(external_proof_cost=0)),('missing original',lambda x:x['topics'][2]['pairs'].pop()),('stale pending N006',lambda x:x['unmeasured'].append('N006')),('wrong representation',lambda x:x['topics'][1].update(representation='calibrated_selected_pdf'))]:
        bad=copy.deepcopy(data);mut(bad)
        try:arithmetic(bad,ex)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    bars=expected_bars(data,'whole_topics');sv=svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(sv);key=bars[1][0];x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:svg_costs(bad,bars)
    except ValueError:controls.append('distorted SVG common')
    else:raise ValueError('distorted SVG accepted')
    rects,H=pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(rects);role,x,y,w,h=bad[0];bad[0]=(role,x,y,w+1,h)
    try:pdf_costs(bad,H,sv,bars,True)
    except ValueError:controls.append('distorted PDF original')
    else:raise ValueError('distorted PDF accepted')
    report=dict(status='PASS_DISTINCT_OVERVIEW34',author_manifest_sha256=PIN,input_bindings=12,topics=13,distinct_originals=34,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=47,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_routes_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()

