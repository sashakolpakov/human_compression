#!/usr/bin/env python3
"""Independent consolidation arithmetic and actual vector geometry."""
from pathlib import Path
import argparse, copy, csv, hashlib, importlib.util, json, math, re, subprocess
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='e7758a9185fe97edbe21ea14f0537a7fea73a9148646208b1cbf9f61510ff99c'

def need(ok,message):
    if not ok: raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def ratio(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(n//g) if d==g else f'{n//g}/{d//g}',decimal=f'{q//10**12}.{q%10**12:012d}')

def expected(public):
    # Reuse the earlier independent routes for unchanged topics, including
    # E's additional validation. No current author implementation is imported.
    path=public/'audit/overview/v1/independent_review/check.py'
    need(sha(path)=='3e16fff05f825a8d9e27723d63c52990a84af8bcd86805cc67a2b877d3488584','legacy independent route changed')
    spec=importlib.util.spec_from_file_location('prior_independent_overview',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    old=module.expected(public);out={}
    for k,(u,p,r,rows,opt) in old.items():out[k]={'common':{'whole_common_paper':u},'printed':p,'raw':r,'pairs':rows,'optional':opt}
    for k,folder in [('A','ac-extensions-measurement'),('B','b5-measurement'),('C','ac-extensions-measurement')]:
        data=load(public/f'audit/{folder}/v1/packet/results.json')['primary'][k]
        out[k]={'common':data['common_components'],'printed':data['printed_program_cost'],'raw':data['raw_program_alternative'],
                'pairs':[(p['source'],p['application'],p['source_cost'],p['application_cost']) for p in data['individual']],'optional':None}
    for k,folder,app in [('Matching','additional-measurements','M1'),('ChiralEnumeration','additional-measurements','CE1'),('Diagonal','diagonal-measurement','DG1')]:
        p=load(public/f'audit/{folder}/v1/packet/results.json')['primary'][k];c=p['document_costs']
        out[k]={'common':{'whole_common_paper':c['common']},'printed':c['program'],'raw':p['raw_costs'].get('complete_programs',p['raw_costs'].get('programs')),
                'pairs':[(p['source_id'],app,c['source'],c['application'])],'optional':None}
    return out

def arithmetic(data,ex):
    need(len(data['topics'])==13 and {t['topic'] for t in data['topics']}==set(ex),'topic set')
    need(data['original_manuscript_count']==33 and data['registry_manuscripts']==161 and data['accessible_originals']==104,'corpus counts')
    need(data['currently_admitted_originals']==34 and data['accessible_pending_complete_recovery']==70 and data['pending_source_retrieval']==57,'recovery scope')
    need(data['pooled_factor'] is None and data['cross_topic_deduplication'] is False and data['all_registry_manuscripts_completed'] is False,'scope')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'new credit')
    count=0;ids=[]
    for t in data['topics']:
        e=ex[t['topic']];u=sum(e['common'].values());p=e['printed'];r=e['raw'];rows=e['pairs'];opt=e['optional']
        ns=sum(x[2] for x in rows);na=sum(x[3] for x in rows)
        need(t['common_components']==e['common'],'complete common components')
        need((t['common_theory'],t['printed_program_cost'],t['raw_program_alternative'],t['source_sum'],t['applications_sum'],t['written_denominator'])==(u,p,r,ns,na,u+na),'full costs')
        need(t['source_ids']==[x[0] for x in rows] and t['source_count']==len(rows),'source IDs')
        need(t['conditional_prepaid']=={'full_common':u,'full_declared_printed_programs':p,'total':u+p},'whole acquisition')
        for key,den in [('written',u+na),('including_printed_programs',u+na+p),('including_raw_programs',None if r is None else u+na+r),('including_optional_validation',None if opt is None else u+na+p+opt)]:
            need(t[key]==(None if den is None else ratio(ns,den)),'fraction '+t['topic']+'/'+key);count+=den is not None
        need(t.get('optional_validation_printed')==opt,'optional validation')
        need(len(t['pairs'])==len(rows),'application count')
        for actual,want in zip(t['pairs'],rows):
            need(tuple(actual[k] for k in ['source','application','source_cost','application_cost'])==want,'application costs')
            need(actual['conditional']==ratio(want[2],want[3]),'conditional arithmetic');ids.append(want[0]);count+=1
        need(t['representation']==('literal_rendered_source_plus_raw_untrimmed_pdfs' if t['topic'] in ['B','C'] else 'calibrated_selected_pdf'),'representation')
        need(t['normalization']=='NFC' and t['unit']=='characters_without_whitespace','coordinate')
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknown cost')
    need(len(ids)==len(set(ids))==33 and count==72,'unique originals/fractions')
    pending=data['unmeasured'];need(len(pending)==1 and pending[0]['source']=='N006' and pending[0]['prior_N007_factor_not_transferred'] is True,'N006 scope')
    need(all(pending[0][k] is None for k in ['source_cost','common_theory','application_cost','program_cost','whole_factor','conditional_factor']),'N006 fictitious costs')
    return count

def expected_bars(data,stem):
    rows=[]
    if stem=='whole_topics':
        for t in data['topics']:
            segments=[('common-'+key,value,'common') for key,value in t['common_components'].items()]
            segments += [(p['application'],p['application_cost'],'application') for p in t['pairs']]
            rows.append((t['topic'],t['source_sum'],segments))
    else:
        pairs=[(t,p) for t in data['topics'] for p in t['pairs']]
        for t,p in pairs[:17] if stem=='conditional_1' else pairs[17:]:
            rows.append((t['topic']+'-'+p['source'],p['source_cost'],[(p['application'],p['application_cost'],'application')]))
    result=[]
    for i,(key,source,segments) in enumerate(rows):
        result.append(('bar-'+key+'-source','source',source,0,i,False));start=0
        for name,cost,role in segments:result.append(('bar-'+key+'-'+name,role,cost,start,i,True));start+=cost
    return result

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

def graphs(packet,data):
    total=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=expected_bars(data,stem);svg=svg_rects((packet/(stem+'.svg')).read_bytes())
        n=svg_costs(svg,bars);rects,height=pdf_rects(packet/(stem+'.pdf'))
        need(pdf_costs(rects,height,svg,bars,stem=='whole_topics')==n,'vector counts');total+=n
    need(total==127,'all127 bars');return total

def csv_check(packet,data):
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()))
    need(len(topics)==13 and len(apps)==33,'CSV counts')
    for row,t in zip(topics,data['topics']):
        values={'topic':t['topic'],'title':t['title'],'originals':t['source_count'],'representation':t['representation'],'sources':t['source_sum'],'common':t['common_theory'],'applications':t['applications_sum'],'written':t['written_denominator'],'written_factor':t['written']['decimal'],'printed_programs':t['printed_program_cost'],'printed_factor':t['including_printed_programs']['decimal'],'raw_programs':t['raw_program_alternative'],'raw_factor':None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal']}
        need(row=={k:'' if v is None else str(v) for k,v in values.items()},'topic CSV')
    for row,(t,p) in zip(apps,[(t,p) for t in data['topics'] for p in t['pairs']]):
        values={'topic':t['topic'],'title':t['title'],'source':p['source'],'application':p['application'],'source_cost':p['source_cost'],'application_cost':p['application_cost'],'conditional_exact':p['conditional']['exact_fraction'],'conditional_factor':p['conditional']['decimal'],'full_common_prepaid':t['common_theory'],'full_program_prepaid':t['printed_program_cost'],'source_representation':p['source_representation']}
        need(row=={k:str(v) for k,v in values.items()},'application CSV')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'author freeze')
    for row in load(a.packet/'manifest.json')['exports']:
        p=a.packet/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen file')
    protocol=load(a.packet/'protocol.json')
    for row in protocol['bindings'].values():
        raw=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=a.public_root)
        need(raw==(a.packet/row['local']).read_bytes() and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'committed input')
    data=load(a.packet/'results.json');ex=expected(a.public_root);nf=arithmetic(data,ex);ng=graphs(a.packet,data);csv_check(a.packet,data)
    reader=PdfReader(a.packet/'summary.pdf');need(len(reader.pages)==6,'reader pages')
    text='\n'.join(p.extract_text() or '' for p in reader.pages)
    need(all(p['source'] in text for t in data['topics'] for p in t['pairs']),'every original in reader')
    controls=[]
    mutations=[('common omitted',lambda r:r['topics'][1]['common_components'].pop('U_B_high_rank')),
               ('partial acquisition',lambda r:r['topics'][1]['conditional_prepaid'].update(full_common=14124)),
               ('pooled ratio',lambda r:r.update(pooled_factor=2)),('unknown zero',lambda r:r['topics'][0].update(external_proof_cost=0)),
               ('N006 borrowed ratio',lambda r:r['unmeasured'][0].update(whole_factor=1.007)),
               ('missing application',lambda r:r['topics'][2]['pairs'].pop()),
               ('printed plus raw',lambda r:r['topics'][1].update(including_raw_programs=ratio(124906,118790+13170+12330))),
               ('wrong representation',lambda r:r['topics'][1].update(representation='calibrated_selected_pdf'))]
    for name,mut in mutations:
        bad=copy.deepcopy(data);mut(bad)
        try:arithmetic(bad,ex)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    bars=expected_bars(data,'whole_topics');sv=svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(sv);key=bars[1][0];x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:svg_costs(bad,bars)
    except ValueError:controls.append('distorted SVG common bar')
    else:raise ValueError('distorted SVG accepted')
    rects,H=pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(rects);role,x,y,w,h=bad[0];bad[0]=(role,x,y,w+1,h)
    try:pdf_costs(bad,H,sv,bars,True)
    except ValueError:controls.append('distorted PDF source bar')
    else:raise ValueError('distorted PDF accepted')
    report={'status':'PASS_DISTINCT_OVERVIEW33','author_manifest_sha256':PIN,'committed_input_bindings':23,'topics':13,'distinct_originals':33,'exact_comparisons':nf,'actual_SVG_bars':ng,'actual_PDF_bars':ng,'CSV_rows':46,'reader_pages':6,'controls_rejected':controls,'author_implementation_imported':False,'prior_independent_routes_reused':True,'primary_reextraction':False,'new_mathematical_credit':0}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
