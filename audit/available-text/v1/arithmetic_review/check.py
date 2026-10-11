#!/usr/bin/env python3
"""Independent B/C full-text arithmetic, reader and actual bar checks."""
import argparse,copy,csv,hashlib,io,json,math,re,xml.etree.ElementTree as ET
from pathlib import Path
PIN='63b5d7d90a49598547db9a14427a37e798d9d8b015f622d148ec25ab2bc1ae53'
INPUT='9bd3fd3a79b84e60d445b51bf03268b006965d1416c11484f2e0bd9af76187f2'
PREVIOUS={'B':('audit/topic-b/v2/measurement/packet/results.json','0a5603e4dea16e929ef230c93844acec67b37b3f17cb49574b32568c8c56d63e'),'C':('audit/topic-c/v2/measurement/packet/results.json','15340bf5900afd12187dbcc2309203355e3b39da6b341e3bba4e7b5b71463780')}
def need(x,m):
    if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bind(p,pin):
    need(sha(p/'manifest.json')==pin,'Frozen manifest')
    for r in read(p/'manifest.json')['exports']:need(sha(p/r['path'])==r['sha256'] and (p/r['path']).stat().st_size==r['bytes'],'Exact frozen export')
def f(n,d):
    g=math.gcd(n,d);return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=format(n/d,'.12f'))
def expected_rows(old,inputs):
    rows=[]
    for topic,missing in [('B','N001'),('C','L108')]:
        for c in old[topic]['coordinates']:
            variant,norm,unit=c['variant'],c['normalization'],c['unit'];s=inputs['documents'][missing]['metrics'][norm][unit];common=c['common_theory'];appcosts=[];sourcecosts=[];individual=[]
            need(c['unknown_source']==missing and c['complete_source_sum'] is None,'Old PDF unknown left immutable')
            for x in c['per_result']:
                sc=s if x['source']==missing else x['source_cost'];app=x['application_cost'];sourcecosts.append(sc);appcosts.append(app);individual.append(dict(source=x['source'],application=x['application'],source_representation='literal_authored_rendering' if x['source']==missing else 'complete_PDF_'+variant,source_cost=sc,application_cost=app,comparison=f(sc,app)))
            total=sum(sourcecosts);apps=sum(appcosts);need(len(individual)==4 and apps==c['all_applications'],'All four full applications');printed=raw=0;whole={'written':f(total,common+apps)}
            if topic=='C':
                printed=c['complete_printed_program_cost'];raw=c['complete_raw_program_cost'];whole['including_printed_programs']=f(total,common+apps+printed);whole['including_raw_programs']=f(total,common+apps+raw)
            rows.append(dict(topic=topic,PDF_variant=variant,normalization=norm,unit=unit,comparison_status='primary_boundary' if variant=='raw_untrimmed' else 'mixed_furniture_sensitivity',rendered_original=missing,rendered_cost=s,common_theory=common,applications=apps,written_denominator=common+apps,printed_program_cost=printed,raw_program_alternative=raw,source_sum=total,whole=whole,individual=individual))
    return rows

def check_result(r,rows):
    need(r['rows']==rows,'All 60 full-cost coordinates and 360 independently calculated fractions')
    prim={t:next(x for x in rows if (x['topic'],x['PDF_variant'],x['normalization'],x['unit'])==(t,'raw_untrimmed','NFC','characters_without_whitespace')) for t in ['B','C']};need(r['primary']==prim,'Untrimmed primary boundary')
    need(r['original_manuscripts']==8 and r['new_source_credit']==0 and r['new_question_credit']==0 and r['full_graphic_and_external_costs'] is None,'Eight originals and exact credit/unknown boundary')
    need(not r['source_text_exported'] and not r['historical_PDF_coordinates_changed'],'No source text or immutable PDF mutation')
    p=r['policy'];need(p['primary_coordinate']==['raw_untrimmed','NFC','characters_without_whitespace'] and p['whole_common_once_per_topic'] and not p['cross_topic_discount'],'Complete independent topic acquisition')
    need(p['conditional_acquisition']=={'B':'Full U_B; no required mathematical program.','C':'Full U_C and both whole required programs.'},'Conditional prepayment')
    return prim

def csv_check(text,rows):
    expected=[]
    for r in rows:
        for key,v in list(r['whole'].items())+[(x['source']+'_conditional',x['comparison']) for x in r['individual']]:expected.append([r['topic'],r['PDF_variant'],r['normalization'],r['unit'],key,*[str(v[k]) for k in ['numerator','denominator','reduced_numerator','reduced_denominator','decimal']]])
    records=list(csv.reader(io.StringIO(text)));need(records[1:]==expected and len(expected)==360,'Every exact CSV fraction once');return len(expected)

def bars(svg,topic,primary):
    root=ET.fromstring(svg);groups={x.attrib['id']:x for x in root.iter() if x.attrib.get('id','').startswith('bar-')};values=[primary['common_theory']]
    for r in primary['individual']:values.extend([r['source_cost'],r['application_cost']])
    need(set(groups)=={f'bar-{topic}-{i}' for i in range(9)},'All nine complete actual bars');scales=[]
    for i,value in enumerate(values):
        ps=[x for x in groups[f'bar-{topic}-{i}'].iter() if x.tag.endswith('path')];need(len(ps)==1,'One actual rectangle');pairs=re.findall(r'[ML]\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)',ps[0].attrib['d']);need(len(pairs)==4,'Actual rectangle corners');ys=[float(y) for _,y in pairs];scales.append((max(ys)-min(ys))/value)
    need(min(scales)>0 and max(scales)-min(scales)<1e-9,'Actual plot heights proportional to costs');return 9

def reader(tex,prim):
    for t,r in prim.items():
        need(f"\\frac{{{r['source_sum']}}}{{{r['written_denominator']}}}={r['source_sum']/r['written_denominator']:.6f}" in tex,'Exact combined reader fraction')
        for i in r['individual']:need(f"{i['source']}/{i['application']} & {i['source_cost']} & {i['application_cost']} & {i['source_cost']/i['application_cost']:.3f}" in tex,'Exact individual reader table')
    for text in ['untrimmed PDF text','previous PDF-only comparisons remain unchanged','both complete required programs have been acquired','alternatives, never two simultaneous charges','Expanded external proofs and complete','Missing figure','mixed-boundary sensitivities']:
        need(text in tex,'Reader qualification '+text)

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--rendered-inputs',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh output');bind(a.packet,PIN);bind(a.rendered_inputs,INPUT);old={}
    for t,(path,pin) in PREVIOUS.items():need(sha(a.public_root/path)==pin,'Old PDF record immutable');old[t]=read(a.public_root/path)
    need(len(old['B']['required_mathematical_programs'])==0 and len(old['C']['required_mathematical_programs'])==2,'Previous complete program roles')
    inputs=read(a.rendered_inputs/'counts.json');rows=expected_rows(old,inputs);r=read(a.packet/'results.json');prim=check_result(r,rows);n=csv_check((a.packet/'comparisons.csv').read_text(),rows);tex=(a.packet/'measurement.tex').read_text();reader(tex,prim);svgs={t:(a.packet/(t+'-costs.svg')).read_text() for t in prim}
    for t in prim:bars(svgs[t],t,prim[t])
    controls=[];mutations=[('drop_common',lambda x:x['rows'][0].update(common_theory=0)),('change_source',lambda x:x['rows'][0]['individual'][0].update(source_cost=1)),('swap_primary_to_trimmed',lambda x:x['primary']['B'].update(PDF_variant='raw_selected')),('unknown_graphics_zero',lambda x:x.update(full_graphic_and_external_costs=0)),('overwrite_old_PDF',lambda x:x.update(historical_PDF_coordinates_changed=True)),('omit_coordinate',lambda x:x['rows'].pop()),('omit_application',lambda x:x['rows'][0]['individual'].pop()),('inflate_manuscript_count',lambda x:x.update(original_manuscripts=70)),('new_credit',lambda x:x.update(new_question_credit=1)),('omit_conditional_prepayment',lambda x:x['policy']['conditional_acquisition'].update(C='None')),('cross_topic_discount',lambda x:x['policy'].update(cross_topic_discount=True)),('double_charge_code',lambda x:x['rows'][30]['whole']['including_printed_programs'].update(denominator=x['rows'][30]['whole']['including_printed_programs']['denominator']+x['rows'][30]['raw_program_alternative'])),('reverse_ratio',lambda x:x['rows'][0]['whole']['written'].update(numerator=1))]
    for name,mut in mutations:
        x=copy.deepcopy(r);mut(x)
        try:check_result(x,rows)
        except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('Accepted control '+name)
    for t in prim:
        xml=ET.fromstring(svgs[t]);g=next(x for x in xml.iter() if x.attrib.get('id')==f'bar-{t}-2');path=next(x for x in g.iter() if x.tag.endswith('path'));path.attrib['d']=re.sub(r'([ML]\s*[-+0-9.eE]+\s+)([-+0-9.eE]+)',lambda m:m[1]+str(float(m[2])*1.1),path.attrib['d'])
        try:bars(ET.tostring(xml,encoding='unicode'),t,prim[t])
        except ValueError as e:controls.append(dict(name=t+'_actual_bar_distortion',rejected=True,reason=str(e)))
        else:raise ValueError('Bar distortion accepted')
    for original in ['untrimmed PDF text','both complete required programs have been acquired','alternatives, never two simultaneous charges']:
        try:reader(tex.replace(original,'incorrect claim'),prim)
        except ValueError as e:controls.append(dict(name='reader_'+original,rejected=True,reason=str(e)))
        else:raise ValueError('Bad reader accepted')
    from pypdf import PdfReader
    pages=[p.extract_text() or '' for p in PdfReader(a.packet/'measurement.pdf').pages];need(len(pages)==3,'Three actual reader pages')
    a.out.mkdir(parents=True);result=dict(status='PASS_INDEPENDENT_B_C_RENDERED_COMPARISONS',coordinates=60,exact_fractions=360,CSV_rows=n,actual_bars=18,controls=controls,primary=prim,reader_page_text_sha256=[hashlib.sha256(s.encode()).hexdigest() for s in pages],no_author_arithmetic_import=True,immutable_previous_PDF_records_unchanged=True);(a.out/'recount.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['primary','controls']}))
if __name__=='__main__':main()
