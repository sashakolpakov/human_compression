#!/usr/bin/env python3
"""Separate the complete census from two explicit readings of the source labels."""
import argparse, collections, itertools, json, re
from pathlib import Path

def need(ok,msg):
    if not ok: raise ValueError(msg)
def read(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
ORDERS={'A5':60,'1':1,'2':2,'3':3,'4':4,'22':4,'S3':6,'D8':8,'Q8':8,'23':8,'D10':10,'A4':12,'D12':12,'24':16,'2× D8':16,'232':16,'322':18,'F21':21,'S4':24,'242':32,'2222':16,'2322':32,'324':36,'243':48,'22A4':48,'22D8':32,'2422':64,'24A4':192}
PAIRS=[(0,1),(0,2),(1,2)]

def index(data,n,arity):
    need(len(data['triples'])==n,'complete class list')
    need([w['witness'] for w in data['triples']]==list(range(1,n+1)),'unique ordered class IDs')
    inv={}
    for w in data['triples']:
        need(w['signatures'],'nonempty signature family')
        for s in w['signatures']:
            need(len(s)==arity,'signature arity')
            key=tuple(s);need(key not in inv or inv[key]==w['witness'],'signature separation')
            inv[key]=w['witness']
    return inv

def complements(signatures):
    sizes={1:1,2:6,3:7,4:7,5:8,6:2,7:12,8:11};out=set()
    for s in signatures:
        t=s[:3]
        for bits in itertools.product([False,True],repeat=t.count(8)):
            flips=dict(zip([i for i in range(3) if t[i]==8],bits));values=[]
            for k,(i,j) in enumerate(PAIRS):
                x=s[3+k];a=flips.get(i,False);b=flips.get(j,False)
                if a and b:x=22-sizes[t[i]]-sizes[t[j]]+x
                elif a:x=sizes[t[j]]-x
                elif b:x=sizes[t[i]]-x
                values.append(x)
            out.add(tuple(t+values+s[6:]))
    return out

def parse(label):
    m=re.fullmatch(r'M(\d{3})\((.*)\)',label);need(m,'label syntax')
    t=list(map(int,m[1]));body=m[2].split(':');tokens=[x.strip() for x in body[0].split(',')]
    need(len(body)<=2 and len(tokens)==3 and all(re.fullmatch(r'\d[12]?',x) for x in tokens),'intersection syntax')
    return t,[int(x[0]) for x in tokens],[int(x[1]) if len(x)>1 else None for x in tokens],int(body[1]) if len(body)==2 else None

def build(source,rows,broad,canonical,pairs,mog):
    inv=index(broad,431,9);cinv=index(canonical,431,9);pinv=index(pairs,81,4)
    for w,c in zip(broad['triples'],canonical['triples']):
        need(w['borel_id']==c['borel_id'] and complements(c['signatures'])=={tuple(s)for s in w['signatures']},'complete independent complement orbit')
    need([r['row'] for r in rows]==list(range(1,432)),'complete physical source rows')
    refined={(tuple(x['types']),x['intersection_size']):{int(k):v for k,v in x['subscript_orders'].items()} for x in source['refined_pairs']}
    explicit={};pair_receipts=[]
    for k,x in enumerate(source['explicit_refined_pair_objects'],1):
        cases=[y for y in mog['explicit_pair_cases'] if y['pair']==k]
        need(len(cases)==4 and {y['completion']for y in cases}=={1,2,3,4},'all four pair completions')
        vals={(tuple(y['canonical_object_membership']),tuple(y['stabilizer_orders']),tuple(y['actual_pair_id']),y['actual_intersection_size']) for y in cases}
        need(len(vals)==1,'coordinate independent pair result')
        y=cases[0];valid=all(y['canonical_object_membership']) and y['stabilizer_orders']==y['expected_stabilizer_orders']
        key=tuple(x['types']+[y['actual_intersection_size'],y['actual_pair_id'][0]])
        pair_id=pinv.get(key) if valid else None
        need(not valid or pair_id is not None,'literal valid pair belongs to complete pair census')
        explicit[x['label']]={'valid':valid,'order':y['actual_pair_id'][0],'pair_class':pair_id,'provisional_e4':x['label']=='M88(7_1)'}
        pair_receipts.append({'label':x['label'],**explicit[x['label']],'printed_order':x['printed_pair_order'],'actual_pair_id':y['actual_pair_id']})
    colon={}
    for k,x in enumerate(source['colon_cases'],1):
        cases=[y for y in mog['completion_cases'] if y['case']==k]
        need(len(cases)==4 and len({(y['flag_transitive'],tuple(y['census_witnesses'])) for y in cases})==1,'coordinate independent colon result')
        colon[re.sub(r'[\s_]+','',x['label'])]=cases[0]['census_witnesses']
    byid={w['witness']:w for w in broad['triples']};result=[];borels=set()
    for row in rows:
        need(row['Borel_text'] in ORDERS,'interpreted printed Borel shape');t,v,sub,col=parse(row['label_text']);porders=[];eorders=[];undefined=[];provisional=[]
        for k,(i,j) in enumerate(PAIRS):
            if sub[k] is None:porders.append(None);eorders.append(None);continue
            porders.append(refined[(tuple([t[i],t[j]]),v[k])][sub[k]])
            label=f'M{t[i]}{t[j]}({v[k]}_{sub[k]})';obj=explicit[label]
            eorders.append(obj['order'] if obj['valid'] else None)
            if not obj['valid']:undefined.append(label)
            if obj['provisional_e4']:provisional.append(label)
        def candidates(idx,orders):
            return sorted({w for s,w in idx.items() if list(s[:6])==t+v and all(o is None or s[6+k]==o for k,o in enumerate(orders))})
        variants={'canonical_pair_order':candidates(cinv,porders),'source_pair_order':candidates(inv,porders),'explicit_pair_objects':None if undefined else candidates(inv,eorders)}
        # A colon is an actual displayed triple, not just its numeric shadow label.
        if col is not None:
            label=re.sub(r'[\s_]+','',row['label_text']);need(label in colon,'all colon labels transcribed')
            variants['explicit_pair_objects']=colon[label]
        for ids in variants.values():
            if ids is not None:
                for w in ids:borels.add((row['row'],w,row['Borel_text']))
        result.append({**row,'pair_orders_p112':porders,'literal_pair_orders_p114':eorders,'undefined_literal_pair_labels':undefined,'provisional_literal_pair_labels':provisional,'candidates':variants,'candidate_Borel_ids':{str(w):byid[w]['borel_id'] for ids in variants.values() if ids is not None for w in ids}})
    return {'status':'COMPLETE_CORRECTED_CENSUS_WITH_SEPARATE_SOURCE_READINGS','pair_classes':81,'triple_classes':431,'separating_pair_signatures':len(pinv),'separating_triple_signatures':len(inv),'canonical_triple_signatures':len(cinv),'source_rows':result,'literal_pair_receipts':pair_receipts,'replacement_pairs':pairs['triples'],'replacement_triples':canonical['triples'],'source_complement_policy':'Every endecad may be replaced independently by its complement, as permitted in L073 pp2–3. Canonical signatures are a separate table convention.','historical_geo_numbering_recovered':False,'unconditional_all_source_labels_matched':False},sorted(borels)

def finish(report,shapes):
    verdict={(r['source_row'],r['witness']):r['shape_compatible'] for r in shapes['rows']}
    summaries={}
    for variant in ['canonical_pair_order','source_pair_order','explicit_pair_objects']:
        assignments=collections.defaultdict(list);bad=[];undefined=[]
        for row in report['source_rows']:
            ids=row['candidates'][variant]
            if ids is None:undefined.append(row['row']);continue
            good=[i for i in ids if verdict[row['row'],i]]
            row.setdefault('shape_compatible',{})[variant]=good
            if not good:bad.append(row['row'])
            for i in good:assignments[i].append(row['row'])
        summaries[variant]={'compatible_rows':sum(len(v) for v in assignments.values()),'distinct_classes':len(assignments),'incompatible_rows':bad,'undefined_rows':undefined,'collisions':[{'class':i,'rows':rs} for i,rs in sorted(assignments.items()) if len(rs)>1],'unassigned_classes':sorted(set(range(1,432))-set(assignments))}
    report['summaries']=summaries;return report

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--finish',action='store_true');a=p.parse_args()
    out=a.work
    if a.finish:
        x=finish(read(out/'reconciliation_pre.json'),read(out/'Borel_check.json'));write(out/'reconciliation.json',x);print(json.dumps(x['summaries'],sort_keys=True));return
    x,b=build(read(a.data/'phase180_source_notation.json'),read(a.data/'phase164_L073_table_contract.json')['rows'],read(out/'source_triples.json'),read(out/'canonical_triples.json'),read(out/'source_pairs.json'),read(out/'codes/mog_check.json'))
    write(out/'reconciliation_pre.json',x);(out/'Borel_inputs.g').write_text('sourceBorelRows:='+json.dumps(b,ensure_ascii=False)+';;\n');print('L073_RECONCILIATION_PREPARED',len(b))
if __name__=='__main__':main()
