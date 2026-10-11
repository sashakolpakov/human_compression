#!/usr/bin/env python3
"""Apply the five independently requested documentary/closure repairs additively."""
import argparse,collections,hashlib,json
from pathlib import Path
def need(x,m):
    if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.study_root.resolve();old=root/'topic_B_logical_dag';need(not a.out.exists(),'fresh output')
    need(sha(old/'manifest.json')=='5fd2a84a613b166438cc2a836735afb6a05b0c7a1b15330c9157a97490368248','immutable v1 manifest')
    for row in json.loads((old/'manifest.json').read_text())['exports']:
        need(sha(old/row['path'])==row['sha256'],'immutable v1 export')
    g,c,p=[json.loads((old/name).read_text()) for name in ['logical_graph.json','coverage.json','protocol.json']]
    nodes={n['id']:n for n in g['nodes']}
    repairs=[]
    def edge(source,target,evidence,kind='proof_use',extra_locators=()):
        need(not any(e['source']==source and e['target']==target and e['kind']==kind for e in g['edges']),'new edge only')
        g['edges'].append(dict(source=source,target=target,kind=kind,evidence=evidence,
            target_evidence=nodes[target]['locators']+list(extra_locators),necessity_claim=False))
    edge('h.N008.T3.1.ladder','h.N008.T3.1.propagation',
         'The propagation calculation uses the maximal-intersection chain, first-failure index k and containment of Phi in earlier chain terms introduced in the ladder setup. The final contradiction belongs to the assembled Theorem 3.1, not to this prerequisite setup.', 'hypothesis_use')
    nodes['h.N008.T3.1.ladder']['scope_qualification']='For outgoing branch prerequisites this node supplies the maximal chain, first-failure index and prior containments only. Its broad printed locator also mentions the forthcoming propagation and final contradiction; those belong to the parent theorem assembly, so no circular prerequisite is intended.'
    repairs.append('Historical Frattini propagation now receives its actual chain/first-failure setup; the broad printed locator has an explicit assembly qualification.')
    rows={r['adapter']:r for r in c['rows']}
    rows['B4']['new_outputs'].append('B2.Extremal')
    repairs.append('The arbitrary-extremal-family strong-intersection clause includes B2.Extremal before applying the two constructive family arguments; no dependency is added to the generic Sign theorem.')
    rows['C11']['new_outputs'].append('B3.Frattini.containment')
    repairs.append('The action-core clause includes Frattini containment as well as the general core identity, so normality yields the source Phi(G) <= core_G(B) conclusion.')
    edge('ext.CFSG','ext.W1',
         'The source physical page 7 explicitly attributes classification dependence to the retained Whiston theorem. This records the cited proof input for W1 as well as W2, not logical indispensability or absence of another proof.',
         'retained_input_use',nodes['ext.CFSG']['locators'])
    repairs.append('The cited Whiston W1 argument has an explicit retained CFSG input, with no necessity or historical-priority claim.')
    edge('h.L030.L2.2','h.L030.L3.3',
         'The printed one-line bipartite-double argument cites odd cycles but also needs connectedness of the underlying Kneser graph. Lemma 2.2 supplies paths between every pair, including the n=2k+1 boundary excluded by the literal strict inequality in Lemma 2.1. This is an identifiable implicit premise, not an explicit printed citation.')
    nodes['h.L030.L3.3']['documentary_flags']+=['Its printed proof names only odd cycles. Underlying graph connectedness is an unexpanded premise supplied by Lemma 2.2.',
        'Printed Lemma 2.1 assumes n>2k+1, while the family also uses n=2k+1; the parity paths of Lemma 2.2 supply that boundary.']
    repairs.append('Historical bipartite-double connectedness has the implicit path premise and its exact parameter-boundary qualification.')
    logical=set(g['logical_edge_kinds']);pred=collections.defaultdict(list)
    for e in g['edges']:
        if e['kind'] in logical:pred[e['target']].append(e['source'])
    def closure(seed):
        seen=set(seed);todo=list(seed)
        for x in todo:
            for y in pred[x]:
                if y not in seen:seen.add(y);todo.append(y)
        return sorted(seen)
    for row in c['rows']:
        row['historical_closure']=closure([row['historical_output']]);row['new_closure']=closure(row['new_outputs'])
    g['new_output_closures']={k:closure([v]) for k,v in g['new_application_outputs'].items()}
    g['checks']=dict(nodes=len(nodes),edges=len(g['edges']),nodes_by_side=dict(collections.Counter(n['side'] for n in nodes.values())),
       nodes_by_category=dict(collections.Counter(n['category'] for n in nodes.values())),edges_by_kind=dict(collections.Counter(e['kind'] for e in g['edges'])),source_clauses=30)
    for name in ['manifest.json','logical_graph.json','coverage.json','protocol.json']:
        path=old/name;g['immutable_inputs'].append(dict(namespace='research',path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=sha(path)))
    g['immutable_inputs'].sort(key=lambda r:(r['namespace'],r['path']))
    g['schema']='topic_b_paired_logical_graph_v2';g['status']='AUTHOR_REVISION_PENDING_INDEPENDENT_ACCEPTANCE'
    g['revision_of']=dict(manifest='topic_B_logical_dag/manifest.json',sha256=sha(old/'manifest.json'))
    p['schema']='topic_b_logical_protocol_v2';p['additive_revision']=repairs
    c['scope_gaps']['N003']['retained_inputs']=['W1 and W2 with the cited Whiston proof dependence on CFSG','Cayley','Aut(S_n) inner for n >= 7']
    correction=dict(status='ADDITIVE_AUTHOR_REVISION_PENDING_INDEPENDENT_ACCEPTANCE',original_manifest_sha256=sha(old/'manifest.json'),repairs=repairs,
        added_edges=3,changed_clause_outputs=['B4','C11'],fixed_clause_count=30,manuscripts_changed=False,measurement_changed=False,new_source_credit=0,new_question_credit=0)
    a.out.mkdir(parents=True)
    for name,obj in [('logical_graph.json',g),('coverage.json',c),('protocol.json',p),('correction.json',correction)]:
        (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(g['checks']))
if __name__=='__main__':main()
