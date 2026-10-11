#!/usr/bin/env python3
"""Independent consolidation audit. Does not import the author's implementation."""
from pathlib import Path
import argparse,json,hashlib,math,csv,xml.etree.ElementTree as ET,copy
from pypdf import PdfReader
from pypdf.generic import ContentStream

def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(n,d):
    g=math.gcd(n,d);a,b=n//g,d//g;q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(a) if b==1 else f'{a}/{b}',decimal=f'{q//10**12}.{q%10**12:012d}')
def expected(public):
    def load(path):return json.loads((public/path).read_text())
    a=load('audit/topic-a/v2/measurement/admission.json')['primary']
    bc=load('audit/available-text/v1/packet/results.json')['primary']
    d=load('audit/topic-d/v2/measurement/admission.json')['primary']
    e=load('audit/topic-e/v2/summary.json')
    out={}
    out['A']=(a['costs']['full_umbrella'],a['costs']['complete_printed_program_appendix'],a['costs']['complete_raw_program_files'],[(r['source_id'],r['application_id'],r['factor']['numerator'],r['factor']['denominator']) for r in a['conditional_applications']],None)
    for k in ['B','C']:
        v=bc[k];out[k]=(v['common_theory'],v['printed_program_cost'],v['raw_program_alternative'],[(r['source'],r['application'],r['source_cost'],r['application_cost']) for r in v['individual']],None)
    out['D']=(d['common_theory'],d['printed_program_cost'],d['raw_program_cost'],[(r['source'],r['application'],r['source_cost'],r['application_cost']) for r in d['per_result']],None)
    out['E']=(e['common_theory'],e['required_program'],None,[(r['source'],'E'+str(i+1),r['full_source_length'],r['complete_application_length']) for i,r in enumerate(e['per_result_contract'])],e['optional_validation_program'])
    f=load('audit/topic-f/v2/measurement/admission.json')['primary'];c=f['costs']
    out['F']=(c['U_F'],c['CODE'],f['raw_costs']['complete_validation_programs'],[('L014','F1',c['L014'],c['F1'])],None)
    for k,folder,u,sid,aid in [('Affine','affine','U_Affine','L012','AF1'),('Representation','representation','U_R','F010','R1')]:
        v=load('audit/topic-'+folder+'/v2/measurement/admission.json')['primary'];c=v['document_costs']
        raw=v['raw_program_cost'] if k=='Affine' else v['raw_costs']['complete_validation_programs']
        out[k]=(c[u],c['CODE'],raw,[(sid,aid,c[sid],c[aid])],None)
    g=load('audit/topic-g/v2/measurement/admission.json')['primary'];c=g['document_costs']
    out['G']=(c['U_G'],c['CODE'],g['raw_costs']['complete_programs'],[(s,q['application'],c[s],c[q['application']]) for s,q in g['conditional'].items()],None)
    h=load('audit/topic-chamber/v2/measurement/packet/results.json')['primary'];c=h['documents']
    out['Chamber']=(c['U_H'],c['CODE'],h['raw_costs']['complete_mathematical_programs'],[(s,q['application'],c[s],c[q['application']]) for s,q in h['conditional'].items()],None)
    return out

def arithmetic(result,ex):
    need(len(result['topics'])==10 and {r['topic'] for r in result['topics']}==set(ex),'topic set')
    ids=[];count=0
    need(result['pooled_factor'] is None and not result['cross_topic_deduplication'] and not result['all_registry_manuscripts_completed'],'programme scope')
    need(result['original_manuscript_count']==27 and result['registry_manuscripts']==161 and result['later_scientific_contracts_not_measured_here']==['F015','L028'],'original count')
    need(all(result[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'invented credit')
    for t in result['topics']:
        u,p,r,rows,opt=ex[t['topic']];ns=sum(x[2] for x in rows);na=sum(x[3] for x in rows)
        need((t['common_theory'],t['printed_program_cost'],t['raw_program_alternative'],t['source_sum'],t['applications_sum'],t['written_denominator'])==(u,p,r,ns,na,u+na),'full accepted costs '+t['topic'])
        need(t['conditional_prepaid']=={'full_common':u,'full_declared_printed_programs':p,'total':u+p},'whole acquisition')
        need(t['source_count']==len(rows) and t['source_ids']==[q[0] for q in rows],'source identity')
        for key,den in [('written',u+na),('including_printed_programs',u+na+p),('including_raw_programs',None if r is None else u+na+r),('including_optional_validation',None if opt is None else u+na+p+opt)]:
            need(t[key]==(None if den is None else fraction(ns,den)),'exact fraction '+t['topic']+' '+key)
            count+=den is not None
        need(t['optional_validation_printed']==opt,'optional programme')
        need(len(t['pairs'])==len(rows),'pair count')
        for a,b in zip(t['pairs'],rows):
            need((a['source'],a['application'],a['source_cost'],a['application_cost'])==b,'complete pair')
            need(a['conditional']==fraction(b[2],b[3]),'conditional fraction');count+=1;ids.append(b[0])
        need(t['representation']==('literal_rendered_source_plus_raw_untrimmed_pdfs' if t['topic'] in ['B','C'] else 'calibrated_selected_pdf'),'representation')
        need(t['normalization']=='NFC' and t['unit']=='characters_without_whitespace','unit')
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknown costs')
    need(len(ids)==len(set(ids))==27 and count==57,'distinct originals or fractions')
    return count

def graphs(packet,result):
    nsvg=npdf=0
    for stem,conditional in [('whole_topics',False),('conditional_applications',True)]:
        svg=ET.fromstring((packet/(stem+'.svg')).read_text());bars=[e for e in svg if e.get('id','').startswith('bar-')]
        rows=[(t,p) for t in result['topics'] for p in t['pairs']] if conditional else [(t,None) for t in result['topics']]
        maxcost=max(max(p['source_cost'],p['application_cost']) if p else max(t['source_sum'],t['written_denominator']) for t,p in rows);scale=720/maxcost
        expect=[]
        for i,(t,p) in enumerate(rows):
            y=60+i*(36 if p else 57);pre='bar-'+t['topic']+'-'+(p['source']+'-' if p else '')
            expect.append((pre+'source',170,y,p['source_cost'] if p else t['source_sum']))
            if p:expect.append((pre+'application',170,y+13,p['application_cost']))
            else:expect.extend([(pre+'common',170,y+17,t['common_theory']),(pre+'applications',170+t['common_theory']*scale,y+17,t['applications_sum'])])
        need(len(bars)==len(expect),'SVG count')
        for b,(key,x,y,cost) in zip(bars,expect):
            need(b.get('id')==key and int(b.get('data-cost'))==cost,'SVG id/value')
            need(abs(float(b.get('x'))-x)<1e-7 and float(b.get('y'))==y and abs(float(b.get('width'))-cost*scale)<1e-7 and float(b.get('height'))==10,'SVG actual geometry')
        reader=PdfReader(packet/(stem+'.pdf'));page=reader.pages[0];height=float(page.mediabox.height);poly=[];found=[]
        for args,op in ContentStream(page.get_contents(),reader).operations:
            if op==b'm':poly=[tuple(map(float,args))]
            elif op==b'l':poly.append(tuple(map(float,args)))
            elif op==b'f':
                if len(poly)==4 and poly[0][0]>=170 and height-poly[0][1]>=60 and abs(poly[0][1]-poly[2][1]-10)<1e-6:found.append(poly)
                poly=[]
        need(len(found)==len(expect),'PDF count')
        for poly,(_,x,y,cost) in zip(found,expect):
            pts=[(x,height-y),(x+cost*scale,height-y),(x+cost*scale,height-y-10),(x,height-y-10)]
            need(all(abs(a-b)<1e-5 for actual,want in zip(poly,pts) for a,b in zip(actual,want)),'PDF actual geometry')
        nsvg+=len(bars);npdf+=len(found)
    return nsvg,npdf

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    result=json.loads((a.packet/'results.json').read_text());ex=expected(a.public_root);nf=arithmetic(result,ex);nb,np=graphs(a.packet,result)
    topics=list(csv.DictReader((a.packet/'topics.csv').open()));apps=list(csv.DictReader((a.packet/'applications.csv').open()))
    need(len(topics)==10 and len(apps)==27,'CSV rows')
    for row,t in zip(topics,result['topics']):
        for key,value in {'topic':t['topic'],'originals':t['source_count'],'representation':t['representation'],'sources':t['source_sum'],'common':t['common_theory'],'applications':t['applications_sum'],'written':t['written_denominator'],'written_factor':t['written']['decimal'],'printed_programs':t['printed_program_cost'],'printed_factor':t['including_printed_programs']['decimal'],'raw_programs':'' if t['raw_program_alternative'] is None else t['raw_program_alternative'],'raw_factor':'' if t['including_raw_programs'] is None else t['including_raw_programs']['decimal']}.items():need(row[key]==str(value),'CSV topic cell')
    flattened=[(t,p) for t in result['topics'] for p in t['pairs']]
    for row,(t,p) in zip(apps,flattened):
        expectedrow={'topic':t['topic'],'source':p['source'],'application':p['application'],'source_cost':p['source_cost'],'application_cost':p['application_cost'],'conditional_factor':p['conditional']['decimal'],'full_common_prepaid':t['common_theory'],'full_program_prepaid':t['printed_program_cost']}
        need(row=={k:str(v) for k,v in expectedrow.items()},'CSV application cell')
    controls=[]
    for name,mut in [('omit common',lambda r:r['topics'][0].__setitem__('common_theory',0)),('invent pooled ratio',lambda r:r.__setitem__('pooled_factor',12)),('omit program',lambda r:r['topics'][2].__setitem__('printed_program_cost',0)),('claim all161',lambda r:r.__setitem__('all_registry_manuscripts_completed',True)),('unknown zero',lambda r:r['topics'][0].__setitem__('external_proof_cost',0))]:
        bad=copy.deepcopy(result);mut(bad)
        try:arithmetic(bad,ex)
        except ValueError:controls.append(name)
        else:raise ValueError('control accepted '+name)
    out=dict(status='PASS_INDEPENDENT_CONSOLIDATION_RECOUNT',exact_fractions=nf,distinct_originals=27,topics=10,CSV_rows=37,actual_SVG_bars=nb,actual_PDF_bars=np,controls_rejected=controls,author_implementation_imported=False,source_reextraction=False,new_proof_review=False,packet_result_sha256=digest(a.packet/'results.json'))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
