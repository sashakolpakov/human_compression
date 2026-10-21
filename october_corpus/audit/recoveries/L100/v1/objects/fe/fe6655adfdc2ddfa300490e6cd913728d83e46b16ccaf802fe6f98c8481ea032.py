import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,json
from pathlib import Path
from endpoint_comparison import compare_endpoints
P=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise ValueError(s)
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();O=args.out;need(not O.exists(),'fresh output');O.mkdir()
    inv=json.loads((P/'diagram_inventory02.json').read_text())['rows'];cmp=json.loads((P/'diagram_comparison01.json').read_text())['rows'];data=json.loads((P/'literal_diagrams01/diagrams.json').read_text())['records']
    positives=damages=ordered_reversals=0
    for source,join in zip(inv,cmp):
        hit=join['candidates'][0];actual=data[hit['catalogue_index']-1];perm=[hit['source_node_to_catalogue_type'][n['position']]-1 for n in source['nodes']]
        checks,bad=compare_endpoints(source,actual,perm);need(not bad,'all ordered endpoints match')
        for edge in source['edges']:
            if '/'not in edge['printed_label']:continue
            single=copy.deepcopy(source);single['edges']=[edge];good,_=compare_endpoints(single,actual,perm);positives+=1
            for endpoint in [0,2]:
                damaged=copy.deepcopy(single);parts=list(map(int,edge['printed_label'].split('/')));parts[endpoint]+=1
                damaged['edges'][0]['printed_label']='/'.join(map(str,parts));need(compare_endpoints(damaged,actual,perm)[1],'changed printed endpoint rejected');damages+=1
            types=good[0]['catalogue_types'];index=next(i for i,p in enumerate(actual['pairs'])if set(p['types'])==set(types))
            for endpoint in [0,1]:
                damaged=copy.deepcopy(actual);pair=damaged['pairs'][index];e=pair['types'].index(types[endpoint]);pair['eccentricities'][e]=[pair['eccentricities'][e][0],999]
                need(compare_endpoints(single,damaged,perm)[1],'nonuniform actual endpoint rejected');damages+=1
            reversed_actual=copy.deepcopy(actual);pair=reversed_actual['pairs'][index];pair['types'].reverse();pair['eccentricities'].reverse()
            need(not compare_endpoints(single,reversed_actual,perm)[1],'actual pair storage orientation transported');ordered_reversals+=1
            if good[0]['expected_endpoints'][0]!=good[0]['expected_endpoints'][1]:
                wrong=copy.deepcopy(actual);wrong['pairs'][index]['types'].reverse()
                need(compare_endpoints(single,wrong,perm)[1],'wrong endpoint/type orientation rejected');damages+=1
    need(positives==8,'eight literal numerical triples')
    row=next(q for q in inv if q['label']=='3.5');need(any(set(e['nodes'])=={'L','R'}and e['printed_label']=='single'for e in row['edges']),'visible3.5 base bond restored')
    need(next(q for q in cmp if q['label']=='3.5')['minimum_mismatches']==0,'3.5 matches')
    need([q['label']for q in cmp if q['minimum_mismatches']]==['5.1','5.2'],'only two remaining proposed preprint corrections')
    report=dict(status='PASS_L100_SOURCE_JOIN_EDITORIAL_AND_ENDPOINT_CONTROLS',positive_triples=positives,damaged_endpoints=damages,storage_orientation_controls=ordered_reversals,
                original_v1_preserved=True,new_group_or_coset_or_construction_runs=0,source_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
