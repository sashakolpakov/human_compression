#!/usr/bin/env python3
"""Independent exact-input, closure and reviewed-interface check for Topic D."""
from pathlib import Path
import argparse,copy,hashlib,json
LOGICAL={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'}
NEW_EDGES={('h.L066.16','h.L066.4'),('h.L066.16','h.L066.2'),('h.L074.subfields','h.L074.14'),('h.L104.oldsearch','h.L104.2'),('UD.PanelRecognition','program.search'),('UD.LocalTests','program.search'),('D1.Multiplicities','D1.Series')}
ABSENT={('program.predicates','program.search'),('D1.Ordered','D1.Series'),('D1.Reversal','D1.Series')}
REQUIRED={'program.exceptional','program.search','program.fusion','program.verify','program.predicates'}
def need(ok,why):
    if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(g,c):
    ns={n['id']:n for n in g['nodes']};need(len(ns)==len(g['nodes']),'duplicate node')
    need(g['edge_orientation']=='prerequisite -> use','direction')
    need(set(g['logical_edge_kinds'])==LOGICAL,'logical kinds')
    pairs={(e['source'],e['target']) for e in g['edges'] if e['kind'] in LOGICAL}
    need(NEW_EDGES<=pairs,'reviewed direct input missing')
    need(not ABSENT & pairs,'false direct dependency restored')
    need(('program.predicates','program.verify') in pairs,'actual verification import omitted')
    for e in g['edges']:
        need(e['source'] in ns and e['target'] in ns,'unknown node')
        if e['kind'] in LOGICAL:
            need(ns[e['source']]['side']!='verification' and ns[e['target']]['side']!='verification','evidence treated as theorem')
            need(not(ns[e['source']]['side']=='historical' and ns[e['target']]['side']=='new'),'source proof silently reused')
    parents={n:set() for n in ns}
    for a,b in pairs:parents[b].add(a)
    # Independent recursive traversal, with an active path detecting cycles.
    memo={}
    def ancestors(n,active=frozenset()):
        need(n not in active,'logical cycle')
        if n not in memo:
            result={n}
            for p in parents[n]:result |= ancestors(p,active|{n})
            memo[n]=result
        return memo[n]
    def closure(outs):return sorted(set().union(*(ancestors(n) for n in outs)))
    for n in ns:ancestors(n)
    total=0
    for row in c['rows']:
        for key,outs in [('historical_closure','historical_outputs'),('new_closure','new_outputs'),('retained_context_closure','retained_input_nodes')]:
            need(row[key]==closure(row[outs]),'wrong '+row['id']+' '+key);total+=1
    for source,outs in g['new_application_outputs'].items():
        need(g['new_output_closures'][source]==closure(outs),'application closure');total+=1
    for n,want in g['additional_current_outputs'].items():need(want==closure([n]),'additional closure');total+=1
    rows={r['id']:r for r in c['rows']}
    need(len(rows)==37,'fixed 37 rows')
    for n in ['L066.1','L066.2','L066.4']:need('h.L066.16' in rows[n]['historical_closure'],'odd degree lost')
    need('h.L074.subfields' in rows['L074.14']['historical_closure'],'generated group omitted from Lemma10')
    need('h.L104.oldsearch' in rows['L104.2']['historical_closure'],'nontrivial Borel exclusion missing')
    need(REQUIRED==set(g['required_mathematical_programs']),'all five whole programs')
    current=set().union(*(set(v) for v in g['new_output_closures'].values()))
    need(REQUIRED<=current,'required program outside complete proof')
    need(not set(g['diagnostic_programs']+g['operational_drivers']) & current,'diagnostic or driver as proof')
    need(not REQUIRED & set(g['new_output_closures']['L074']),'finite samples substituted for Suzuki theorem')
    need('UD.Normalizer' in ns and 'UD.Normalizer' not in current,'unused common statement hidden or falsely shared')
    need(all(n['cost'] is None for n in ns.values()),'unmeasured cost replaced by zero')
    need(g['compression_ratio'] is None and not g['new_source_credit'] and not g['new_question_credit'],'unauthorized numerical or result claim')
    need(rows['L104.4']['new_outputs']==[] and rows['L104.4']['coverage_kind']=='excluded','secondary J2 claims falsely recovered')
    for n in ['L074.6','L074.7','L074.8','L074.10','L074.16']:need(rows[n]['new_outputs']==[],'retained or unused old fact silently proved')
    f=g['formal_evidence'];need(f['initial_report_count']==10 and f['later_support_report_count']==28 and f['later_components']==[12,16] and not f['first_support_12_counted_again'] and not f['source_specific_instantiations_claimed'] and not f['divisor_number_theoretic_bridge_verified'],'formal scope')
    return dict(nodes=len(ns),typed_edges=len(g['edges']),logical_pairs=len(pairs),closures_checked=total)
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh report path')
    g=json.loads((a.packet/'logical_graph.json').read_text());c=json.loads((a.packet/'coverage.json').read_text());m=json.loads((a.packet/'manifest.json').read_text())
    for row in m['exports']:
        f=a.packet/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'export '+row['path'])
    roots={'research':a.study_root,'public':a.public_root}
    for row in g['immutable_inputs']:
        f=roots[row['namespace']]/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'input '+row['path'])
    original=json.loads((a.public_root/'papers/topic-d/v2/scope.json').read_text())
    need({r['id']:r for r in original['contracts']}=={r['id']:r['accepted_record'] for r in c['rows']},'accepted clauses changed')
    need(len(g['accepted_scope_spans'])==len(original['proof_spans'])==19,'original 19 proof contexts')
    result=inspect(g,c);controls=[]
    for s,t in sorted(NEW_EDGES):
        gg=copy.deepcopy(g);gg['edges']=[e for e in gg['edges'] if (e['source'],e['target'])!=(s,t)]
        try:inspect(gg,c)
        except RuntimeError as e:controls.append(dict(mutation='drop '+s+' -> '+t,rejected=True,reason=str(e)))
        else:raise RuntimeError('lost premise accepted')
    for label in ['false_search_import','diagnostic_premise','external_zero','excluded_claim','formal_overclaim']:
        gg,cc=copy.deepcopy(g),copy.deepcopy(c)
        if label=='false_search_import':gg['edges'].append(dict(source='program.predicates',target='program.search',kind='proof_use'))
        elif label=='diagnostic_premise':gg['edges'].append(dict(source='diagnostic.fields',target='D2.Polyhedra',kind='proof_use'))
        elif label=='external_zero':next(n for n in gg['nodes'] if n['side']=='external')['cost']=0
        elif label=='excluded_claim':next(r for r in cc['rows'] if r['id']=='L104.4')['new_outputs']=['D3.Verified']
        else:gg['formal_evidence']['source_specific_instantiations_claimed']=True
        try:inspect(gg,cc)
        except RuntimeError as e:controls.append(dict(mutation=label,rejected=True,reason=str(e)))
        else:raise RuntimeError('invalid scope accepted')
    report=dict(status='PASS_INDEPENDENT_GRAPH_BINDINGS_CLOSURES_AND_REVIEWED_INTERFACES',manifest_sha256=sha(a.packet/'manifest.json'),immutable_inputs=len(g['immutable_inputs']),exact_source_rows=37,accepted_contexts=19,**result,controls=controls,not_a_mathematics_replay=True,no_weights_or_ratios=True)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
