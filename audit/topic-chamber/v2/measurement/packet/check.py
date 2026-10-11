#!/usr/bin/env python3
"""Author arithmetic, scope, plot and reader controls; not independent review."""
import argparse,copy,csv,io,json,math,re,xml.etree.ElementTree as ET
from pathlib import Path
from compute import read,write,need,calculate,quotient,UNITS,FORMS,VARIANTS,PAIRS

def verify(result,expected,protocol):
    need(result['boundary']==protocol['boundary'],'Exact denominator, conditional acquisition and unknown-cost boundary')
    need(result['accepted_manifests']==protocol['accepted_manifests'],'Three accepted input pins')
    need(result['source_ids']==['L008','N016'] and result['principal_source_manuscripts']==2 and result['detailed_source_rows']==27 and result['proof_contexts']==22,'Two complete manuscripts, not clause inflation')
    need(all(result[k] for k in ['no_new_source_credit','no_new_question_credit','no_new_formal_credit']) and not result['primary_text_exported'],'No new credits or primary text')
    need(len(result['coordinates'])==30 and result['exact_fractions']==150 and result['combined_fractions']==90 and result['conditional_fractions']==60,'All thirty coordinates and 150 exact comparisons')
    coordinates={(r['variant'],r['normalization'],r['unit']):r for r in result['coordinates']}
    need(len(coordinates)==30 and set(coordinates)=={(v,f,u) for v in VARIANTS for f in FORMS for u in UNITS},'Complete unique coordinates')
    for e in expected['coordinates']:
        r=coordinates[e['variant'],e['normalization'],e['unit']]
        for k in ['documents','raw_costs','program_costs_by_role','source_sum','written_denominator','acquisition']:
            need(r[k]==e[k],'Complete accepted costs: '+k)
        for k in e['combined']:need(r['combined'][k]==e['combined'][k],'Exact combined fraction: '+k)
        for k in e['conditional']:need(r['conditional'][k]==e['conditional'][k],'Exact conditional fraction: '+k)
    need(result['primary']==coordinates[tuple(protocol['primary_coordinate'])],'Declared primary coordinate')

def bars(svg,result):
    root=ET.fromstring(svg);ns={'s':'http://www.w3.org/2000/svg'}
    p=result['primary'];d=p['documents'];expected={'bar-total-source':p['source_sum'],'bar-total-common':d['U_H'],'bar-total-applications':d['H1']+d['H2']}
    expected.update({'bar-component-'+k:d[k] for k in ['U_H','L008','H1','N016','H2','CODE']})
    found={x.attrib['id']:x for x in root.iter() if x.attrib.get('id','').startswith('bar-')};need(set(found)==set(expected),'All nine actual SVG bars')
    scales={}
    for name,value in expected.items():
        paths=found[name].findall('s:path',ns);need(len(paths)==1,'One literal bar path')
        text=paths[0].attrib['d'];pairs=re.findall(r'[ML]\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)',text)
        need(len(pairs)==4,'Rectangular actual SVG bar');ys=[float(y) for x,y in pairs];height=max(ys)-min(ys);group='total' if name.startswith('bar-total-') else 'component';scales.setdefault(group,[]).append(height/value)
    for group,values in scales.items():need(min(values)>0 and max(values)-min(values)<1e-9,'Actual SVG heights follow complete costs: '+group)
    return len(expected)

def csv_check(text,result):
    rows=list(csv.DictReader(io.StringIO(text)));expected=[]
    for r in result['coordinates']:
        for name,v in list(r['combined'].items())+[(s+'_conditional',x['comparison']) for s,x in r['conditional'].items()]:
            expected.append(dict(variant=r['variant'],normalization=r['normalization'],unit=r['unit'],comparison=name,**{k:str(v[k]) for k in ['numerator','denominator','reduced_numerator','reduced_denominator','decimal']}))
    need(rows==expected,'All 150 exact CSV comparisons');return len(rows)

def reader_check(tex,result):
    p=result['primary'];d=p['documents'];need('two complete source manuscripts' in tex and 'not 27 manuscripts' in tex,'Reader source count')
    need('whole common paper and both complete programs' in tex and 'These representations are alternatives' in tex,'Conditional prepayment and code alternatives')
    need('all-rank finite minimal-cover multiplicity' in tex and 'remains unresolved' in tex,'Separate finite question')
    need('This is not a complete' in tex and 'Lean verification' in tex,'Partial formalization')
    need('their text remains in the' in tex and 'complete-source numerator' in tex,'L008 ancillary text retained in whole source length')
    need('N016\'s publisher PDF was not available' in tex,'Exact author edition')
    for k,v in d.items():need(str(v) in tex,'All complete document values in reader')

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
    for k in ['inputs','input_review','input_adoption']:p.add_argument('--'+k.replace('_','-'),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh check output');protocol=read(a.packet/'protocol.json');expected=calculate({k:getattr(a,k) for k in ['inputs','input_review','input_adoption']},protocol);r=read(a.packet/'results.json');verify(r,expected,protocol);n=csv_check((a.packet/'comparisons.csv').read_text(),r);svg=(a.packet/'complete_costs.svg').read_text();nb=bars(svg,r);tex=(a.packet/'measurement.tex').read_text();reader_check(tex,r)
    controls=[]
    mutations=[('drop_common_cost',lambda x:x['coordinates'][0].update(written_denominator=x['coordinates'][0]['written_denominator']-x['coordinates'][0]['documents']['U_H'])),('change_source_cost',lambda x:x['coordinates'][0]['documents'].update(L008=1)),('prune_diagnostic',lambda x:x['coordinates'][0]['program_costs_by_role'].update(diagnostic=0)),('double_charge_programs',lambda x:x['coordinates'][0]['combined']['including_printed_programs'].update(denominator=x['coordinates'][0]['combined']['including_printed_programs']['denominator']+x['coordinates'][0]['raw_costs']['complete_mathematical_programs'])),('omit_coordinate',lambda x:x['coordinates'].pop()),('alter_conditional_fraction',lambda x:x['coordinates'][0]['conditional']['L008']['comparison'].update(numerator=1)),('shift_primary',lambda x:x.update(primary=x['coordinates'][0])),('drop_conditional_prepayment',lambda x:x['boundary'].update(conditional='Nothing prepaid')),('zero_unknown_graphics',lambda x:x['boundary'].update(graphics_and_formula_layout_cost=0)),('claim_all_rank_finite',lambda x:x['boundary'].update(full_all_rank_finite_cover_answer=True)),('inflate_sources_to_clauses',lambda x:x.update(principal_source_manuscripts=27)),('claim_new_credit',lambda x:x.update(no_new_question_credit=False)),('omit_raw_driver',lambda x:x['coordinates'][0]['raw_costs'].update(complete_operational_drivers=0)),('claim_complete_Lean',lambda x:x['boundary'].update(end_to_end_formalized=True))]
    for name,mut in mutations:
        x=copy.deepcopy(r);mut(x)
        try:verify(x,expected,protocol)
        except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('Accepted mutation '+name)
    root=ET.fromstring(svg);target=next(x for x in root.iter() if x.attrib.get('id')=='bar-component-H1');path=next(x for x in target.iter() if x.tag.endswith('path'));path.attrib['d']=re.sub(r'([ML]\s*[-+0-9.eE]+\s+)([-+0-9.eE]+)',lambda m:m[1]+str(float(m[2])*1.2),path.attrib['d'])
    try:bars(ET.tostring(root,encoding='unicode'),r)
    except ValueError as e:controls.append({'name':'distort_actual_bar_height','rejected':True,'reason':str(e)})
    else:raise ValueError('Distorted SVG accepted')
    for old,new in [('whole common paper and both complete programs','some common lemmas'),('remains unresolved','is solved'),('These representations are alternatives','Both representations are paid')]:
        try:reader_check(tex.replace(old,new),r)
        except ValueError as e:controls.append({'name':'reader_'+old,'rejected':True,'reason':str(e)})
        else:raise ValueError('Misleading reader accepted')
    a.out.mkdir(parents=True);out=dict(status='PASS_AUTHOR_NUMERICAL_SCOPE_READER_AND_ACTUAL_PLOT_CHECKS',exact_fractions=150,CSV_rows=n,actual_SVG_bars=nb,controls=controls,independent_review=False);write(a.out/'report.json',out);print(json.dumps(out))
if __name__=='__main__':main()
