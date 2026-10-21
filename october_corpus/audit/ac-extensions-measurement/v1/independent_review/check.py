#!/usr/bin/env python3
"""Root recomputation from the distinct recount and immutable earlier topics."""
import argparse, copy, csv, hashlib, itertools, json
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
from pypdf import PdfReader
from plot_checks import need, svg_check, pdf_check
import xml.etree.ElementTree as ET

V=['raw_untrimmed','raw_selected','calibrated_selected']
N=['NFC','NFKC']
U=['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
   'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
PAIRS=[('L032','A1'),('L034','A2'),('F016','A3'),('F013','A4'),('L035','A5'),('N009','A6')]
RECOUNT='604edbc386dbfd9e4023b2bcf175a787aba6e4bd3db7274bedac7b09d3a937fb'
AUTHOR='f9291cf0d4a5291ec7ba1bb671f6787ad1539af5fa9e2f212ad6b0c8a5ea6b23'

def read(path): return json.loads(path.read_text())
def checked(path, sha):
    need(hashlib.sha256(path.read_bytes()).hexdigest()==sha,'bound edition '+str(path))
    return read(path)
def exports(path, sha):
    m=checked(path/'manifest.json',sha)
    for x in m['exports']:
        b=(path/x['path']).read_bytes()
        need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'bound export '+x['path'])

def reconstruct(a,c,recount):
    values={}
    for v,n,u in itertools.product(V,N,U):
        fresh={k:x['metrics'][v][n][u] for k,x in recount['documents'].items()}
        olda={k:x['metrics'][n]['untrimmed' if v==V[0] else v][u] for k,x in a['documents'].items()}
        cold=[x for x in c['rows'] if (x['topic'],x['PDF_variant'],x['normalization'],x['unit'])==('C',v,n,u)]
        need(len(cold)==1,'unique old C coordinate');cold=cold[0]
        for t in ['A','C']:
            def raw(category):
                return sum(x['metrics'][n][u] for path,x in recount['raw_files'][category].items() if '/topic-'+t.lower()+'/' in path)
            if t=='A':
                pairs=[(s,k,olda[s],olda[k],'complete_PDF_'+v) for s,k in PAIRS]
                pairs.append(('L128','A7',fresh['L128'],fresh['A7'],'complete_PDF_'+v))
                common={'U_A':olda['U_A']}
                code={'previous_complete_appendix':olda['code'],'A_CODE_NEW':fresh['A_CODE_NEW']}
                rawold=sum(x['metrics'][n][u] for x in a['complete_raw_program_files'])
            else:
                pairs=[tuple(x[k] for k in ['source','application','source_cost','application_cost','source_representation']) for x in cold['individual']]
                pairs.append(('L068','C5',fresh['L068'],fresh['C5'],'complete_PDF_'+v))
                common={'U_C':cold['common_theory'],'U_C_INC':fresh['U_C_INC']}
                code={'previous_complete_appendix':cold['printed_program_cost'],'C_CODE_NEW':fresh['C_CODE_NEW']}
                rawold=cold['raw_program_alternative']
            values[t,v,n,u]=dict(pairs=pairs,common=common,code=code,rawold=rawold,
                rawnew=raw('new_programs'),drivers=raw('drivers'),formal=raw('formal'))
    return values

def arithmetic(result, expected):
    need(result['original_manuscripts']==12 and result['additional_originals']==2 and result['new_topics']==0,'unique originals')
    need(result['existing_topics']==['A','C'] and result['coordinates_per_topic']==30 and result['exact_fractions']==540,'scope')
    need(result['new_source_credit']==result['new_question_credit']==0 and not result['full_formalization_claim'],'scientific credits')
    need(all(x is None for x in result['unknown_costs'].values()),'unpriced costs')
    need(all(result[k] for k in ['source_contracts_unchanged','prior_numerical_packets_unchanged','full_common_charged_per_topic','all_declared_whole_programs_charged']),'full retained closure')
    rows={tuple(x[k] for k in ['topic','variant','normalization','unit']):x for x in result['rows']}
    need(set(rows)==set(expected) and len(rows)==len(result['rows'])==60,'all coordinates')
    fractions={}
    def exact(q,s,d):
        f=Fraction(s,d)
        with localcontext() as ctx:
            ctx.prec=40; dec=str(Decimal(s)/Decimal(d))
        need(q==dict(numerator=s,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=dec),'exact fraction')
        return s,d,dec
    for key,e in expected.items():
        t,v,n,u=key;r=rows[key];s=sum(x[2] for x in e['pairs']);ap=sum(x[3] for x in e['pairs'])
        co=sum(e['common'].values());pc=sum(e['code'].values());rc=e['rawold']+e['rawnew']
        need(r['original_manuscripts']==len(e['pairs']) and r['source_sum']==s and r['applications']==ap,'source/application sums')
        need(r['common_components']==e['common'] and r['common_theory']==co and r['written_denominator']==co+ap,'full common')
        need(r['printed_program_components']==e['code'] and r['printed_program_cost']==pc,'full printed code')
        need(r['raw_program_components']==dict(previous_complete_files=e['rawold'],new_complete_file=e['rawnew']) and r['raw_program_alternative']==rc,'full raw code')
        need(r['shared_program_already_charged_once']==(t=='C'),'shared code once')
        need(r['new_auxiliary_inventory']==dict(drivers=e['drivers'],partial_formal_sources=e['formal']),'raw auxiliary inventory')
        need(r['conditional_acquisition']==dict(full_common=co,full_printed_programs=pc,full_raw_programs=rc,printed_and_raw_are_alternatives=True),'complete conditional prepayment')
        for kind,d in [('written',co+ap),('including_printed_programs',co+ap+pc),('including_raw_programs',co+ap+rc)]:
            fractions[t,'all',v,n,u,kind]=exact(r['whole'][kind],s,d)
        need(len(r['individual'])==len(e['pairs']),'application roster')
        for got,want in zip(r['individual'],e['pairs']):
            need(tuple(got[k] for k in ['source','application','source_cost','application_cost','source_representation'])==want,'whole original and application')
            fractions[t,want[0],v,n,u,'conditional_application']=exact(got['conditional'],want[2],want[3])
    for t,v in [('A',V[2]),('C',V[0])]: need(result['primary'][t]==rows[t,v,N[0],U[2]],'primary representation')
    need(len(fractions)==540,'all 540 fractions')
    return fractions

def bars(expected):
    out=[]
    for t,v in [('A',V[2]),('C',V[0])]:
        e=expected[t,v,N[0],U[2]]
        s=sum(x[2] for x in e['pairs']);a=sum(x[3] for x in e['pairs']);c=sum(e['common'].values());p=sum(e['code'].values())
        for name,role,cost,bottom in [('source','source',s,0),('common-written','common',c,0),('application-written','application',a,c),('common-printed','common',c,0),('application-printed','application',a,c),('program','program',p,c+a)]:
            out.append(('bar-'+t+'-'+name,role,cost,bottom))
    return out

def main():
    p=argparse.ArgumentParser()
    for k in ['author','input-review','public-root','out']:p.add_argument('--'+k,type=Path,required=True)
    q=p.parse_args();need(not q.out.exists(),'fresh output');q.out.mkdir(parents=True)
    exports(q.author,AUTHOR);exports(q.input_review,RECOUNT)
    a=checked(q.public_root/'audit/topic-a/v2/measurement/results.json','3be443f9c4b81fc8f3271b4b76934482a6a1d91df32803ace30c9f7bebbc6c5f')
    c=checked(q.public_root/'audit/available-text/v1/packet/results.json','5e2a72716609b460b87d96c8906bbfc619a2f315b5ab030b9d94700fe9bb3dbb')
    expected=reconstruct(a,c,read(q.input_review/'recount.json'));r=read(q.author/'results.json');f=arithmetic(r,expected)
    seen={}
    for x in csv.DictReader((q.author/'comparisons.csv').open()):
        key=tuple(x[k] for k in ['topic','source','variant','normalization','unit','comparison'])
        need(key not in seen,'unique CSV row');seen[key]=(int(x['numerator']),int(x['denominator']),x['decimal'])
    need(seen==f,'all CSV values')
    b=bars(expected);svg=(q.author/'whole_costs.svg').read_bytes()
    sn=svg_check(svg,b);pn=pdf_check(q.author/'whole_costs.pdf',b)
    controls=[]
    for label,mutate in [('erase common',lambda z:z['rows'][0].update(common_theory=0)),('erase old program',lambda z:z['rows'][1].update(raw_program_alternative=0)),('double shared code',lambda z:z['rows'][1]['raw_program_components'].update(previous_complete_files=1)),('alter exact factor',lambda z:z['rows'][0]['whole']['written'].update(denominator=1)),('erase whole conditional acquisition',lambda z:z['rows'][0]['conditional_acquisition'].update(full_common=0)),('unknown to zero',lambda z:z['unknown_costs'].update(external=0)),('clauses as manuscripts',lambda z:z.update(original_manuscripts=290))]:
        wrong=copy.deepcopy(r);mutate(wrong)
        try:arithmetic(wrong,expected)
        except ValueError:controls.append(label)
        else:raise ValueError('control accepted')
    for gid in ['bar-A-common-written','bar-C-application-printed']:
        root=ET.fromstring(svg)
        for group in root.iter():
            if group.get('id')==gid:
                next(x for x in group.iter() if x.tag.endswith('path')).set('d','M 0 0 L 1 0 L 1 1 L 0 1 z')
        try:svg_check(ET.tostring(root),b)
        except ValueError:controls.append('distorted '+gid)
        else:raise ValueError('graph control accepted')
    pages=PdfReader(q.author/'measurement.pdf').pages;need(len(pages)==2,'reader extent')
    text='\n'.join(x.extract_text() or '' for x in pages)
    for row in r['primary'].values():
        for val in list(row['whole'].values())+[x['conditional'] for x in row['individual']]:
            need(f"{float(val['decimal']):.3f}" in text,'printed primary factor')
    report=dict(status='PASS_DISTINCT_NUMERICAL_REVIEW',coordinates=60,exact_fractions=540,csv_rows=540,svg_bars=sn,pdf_bars=pn,baselines_and_stacking=True,independent_controls=controls,primary=r['primary'],new_scientific_credit=0,new_question_credit=0,source_extraction_repeated=False,scientific_programs_executed=False)
    (q.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='primary'}))

if __name__=='__main__':main()
