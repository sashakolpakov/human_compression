#!/usr/bin/env python3
"""Portable integrity, typed closure and scope checks, not mathematical re-proofs."""
from pathlib import Path
from collections import Counter, deque
import argparse, copy, hashlib, json

SHA=lambda b:hashlib.sha256(b).hexdigest()
LOGICAL={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'}
OTHER={'attribution','comparison','validation','formal_scope','operational'}
REQUIRED={'program.kernel64','program.affine64','program.census384','program.fixed','program.kernel66','program.affine66'}
EXCLUDED={'L012.problem1.1','L012.table1','L012.seed_uniqueness'}
BASE='papers/topic-affine/v2/'

def need(ok,why):
    if not ok:raise ValueError(why)

def tally(g):
    return dict(nodes=len(g['nodes']),edges=len(g['edges']),
      nodes_by_side=dict(Counter(x['side'] for x in g['nodes'])),
      nodes_by_category=dict(Counter(x['category'] for x in g['nodes'])),
      edges_by_kind=dict(Counter(x['kind'] for x in g['edges'])),source_clauses=33)

def validate(g,c,p,roots):
    need(g['edge_orientation']==p['edge_orientation']=='prerequisite -> use','edge direction')
    need(set(g['logical_edge_kinds'])==set(p['logical_edge_kinds'])==LOGICAL,'logical edge kinds')
    need(set(g['nonlogical_edge_kinds'])==set(p['nonlogical_edge_kinds'])==OTHER,'other edge kinds')
    need(g['source_order']==p['source_order']==['L012'],'closed source scope')
    need(g['compression_ratio'] is None and g['new_source_credit']==g['new_question_credit']==0,'no new factor or credit')
    need(not g['measurement']['weights_assigned'] and not g['measurement']['exclusive_partition_assigned'],'no unreviewed weights')
    need(g['measurement']['whole_common_paper_paid'] and g['measurement']['complete_six_programs_paid'] and g['measurement']['unused_common_statements_not_removed'],'complete paper/program cost boundaries preserved')
    ins={(r['namespace'],r['path']):r for r in g['immutable_inputs']}
    need(len(ins)==len(g['immutable_inputs']),'unique immutable bindings')
    texts={}
    for (ns,path),r in ins.items():
        need(ns in roots and not Path(path).is_absolute() and '..' not in Path(path).parts,'safe retained path')
        b=(roots[ns]/path).read_bytes();need(len(b)==r['bytes'] and SHA(b)==r['sha256'],'retained bytes '+path)
    spans=set()
    def span(s):
        key=s['namespace'],s['path'];need(key in ins,'bound locator')
        if key not in texts:texts[key]=(roots[key[0]]/key[1]).read_text()
        t=texts[key];a,b=s['start_codepoint'],s['end_codepoint_exclusive']
        need(0<=a<b<=len(t),'nonempty context')
        need(SHA(t[a:b].encode())==s['sha256_utf8'],'exact context hash')
        need(t.count('\n',0,a)+1==s['first_line'] and t.count('\n',0,b-1)+1==s['last_line'],'line context')
        spans.add((key,a,b))
    ns={n['id']:n for n in g['nodes']};need(len(ns)==len(g['nodes']),'unique nodes')
    for n in ns.values():
        need(n['cost'] is None,'unknown/unmeasured cost not zero')
        need(n['locators'],'every node has an actual context')
        for s in n['locators']:span(s)
    pred={n:set() for n in ns};succ={n:set() for n in ns};pairs=set()
    for e in g['edges']:
        a,b,k=e['source'],e['target'],e['kind']
        need(a in ns and b in ns and a!=b,'distinct edge endpoints')
        need(k in LOGICAL|OTHER,'valid typed edge')
        need((a,b,k) not in pairs,'no duplicated typed edge');pairs.add((a,b,k))
        need(e['evidence'] and e['target_evidence'] and e['necessity_claim'] is False,'documentary evidence, not minimality')
        for s in e['target_evidence']:span(s)
        if k in LOGICAL:
            need(ns[a]['side']!='verification' and ns[b]['side']!='verification','no Lean/diagnostic/driver mathematical premise')
            need(not(ns[a]['side']=='historical' and ns[b]['side']=='new'),'historical attribution not an unpriced current premise')
            need(not(ns[a]['side']=='new' and ns[b]['side']=='historical'),'no anachronistic historical proof')
            pred[b].add(a);succ[a].add(b)
    deg={n:len(pred[n]) for n in ns};todo=deque(n for n,d in deg.items() if d==0);seen=0
    while todo:
        n=todo.popleft();seen+=1
        for x in succ[n]:
            deg[x]-=1
            if deg[x]==0:todo.append(x)
    need(seen==len(ns),'logical DAG acyclic')
    def closure(ids):
        result=set(ids);q=list(ids)
        while q:
            for x in pred[q.pop()]:
                if x not in result:result.add(x);q.append(x)
        return sorted(result)
    original=json.loads((roots['public']/(BASE+'scope.json')).read_text())
    rows={r['id']:r for r in c['rows']};old={r['id']:r for r in original['source_rows']}
    need(len(rows)==len(c['rows'])==c['source_clause_count']==p['accepted_contract_rows']==33,'all 33 distinct clauses')
    need(set(rows)==set(old),'same closed scope IDs')
    for id,r in rows.items():
        need(r['accepted_record']==old[id],'unchanged accepted record '+id)
        for key,side in [('historical_outputs','historical'),('new_outputs','new'),('retained_input_nodes','external')]:
            need(all(x in ns and ns[x]['side']==side for x in r[key]),'route side '+id)
        need(r['historical_closure']==closure(r['historical_outputs']) and r['new_closure']==closure(r['new_outputs']) and r['retained_context_closure']==closure(r['retained_input_nodes']),'actual row closure '+id)
        need(r['cost'] is None,'unmeasured row')
    for id in EXCLUDED:
        need(rows[id]['coverage_kind']=='excluded' and rows[id]['new_outputs']==[] and rows[id]['qualification_context_nodes']==['AF.Exclusions'],'no excluded source claim recovered')
    for id in ['retained.Burnside','retained.Lucchini','retained.SmallGroups','retained.RS']:
        need(not rows[id]['new_outputs'] and rows[id]['retained_input_nodes'],'classical theorem remains retained')
    need(rows['L012.question.type2']['coverage_kind']=='historically_answered_question' and rows['L012.question.type2']['new_outputs']==['AF.KnownAnswer'],'known question answer, no new credit')
    need(rows['L012.L4.5.branch0']['coverage_kind']=='corrected_source_statement' and ns['h.L4.5.0']['documentary_flags'] and ns['h.T1.3']['documentary_flags'],'literal source sign qualification')
    need(ns['h.C5.2']['documentary_flags'],'source cross-reference typo remains explicit')
    need(set(g['required_mathematical_programs'])==set(p['required_programs'])==REQUIRED,'all six complete required programs')
    need(g['diagnostic_programs']==['diagnostic.controls'] and g['operational_drivers']==['driver.check','driver.integrity'],'three auxiliary roles')
    need(all(ns[x]['side']=='new' and ns[x]['category']=='required_program' for x in REQUIRED),'required code role')
    for x in g['diagnostic_programs']+g['operational_drivers']:need(ns[x]['side']=='verification','auxiliary not logical')
    need(g['formal_evidence']==dict(report_count=9,module_counts=[2,3,4],evidence_only=True,application_instantiations_formalized=False),'nine declarations only; scoped coverage')
    main=sorted({x for r in rows.values() if r['coverage_kind'] in ['proved_principal_component','corrected_source_statement'] and not r['id'].startswith('new.') for x in r['new_outputs']})
    need(g['new_application_outputs']=={'L012':main} and g['new_output_closures']=={'L012':closure(main)},'full principal route')
    need(REQUIRED<=set(closure(main)),'all six programs remain in actual principal dependency closure')
    full=sorted({x for r in rows.values() for x in r['new_outputs']})
    need(g['full_record_outputs']==full and g['full_record_closure']==closure(full),'all inherited output interfaces')
    for x,cl in g['additional_current_outputs'].items():need(cl==closure([x]),'additional output closure')
    common={n['id'] for n in ns.values() if n['side']=='new' and n['document']=='U_Affine' and n['category']=='proved_statement'}
    need(g['unused_common_statement_nodes']==sorted(common-set(closure(main))),'unused statements explicit, not removed from cost')
    required_edges=[('UA.K0','UA.K'),('UA.K','UA.SK'),('AL.1','AL.RawInvariant'),('AL.RawInvariant','program.affine66'),
      ('program.kernel64','AF.Affine64'),('program.affine64','AF.Affine64'),('AL.2','AF.Affine64'),
      ('program.kernel66','AF.Affine66'),('program.affine66','AF.Affine66'),('AL.2','AF.Affine66'),
      ('AL.3','AF.Period64'),('AL.3','AF.Period66'),('AL.PresentationExtension','AF.SourcePeriods'),
      ('program.fixed','AF.Seed384'),('program.fixed','AF.SignExample'),('program.census384','AF.Census384'),
      ('ext.Lucchini','AF.CyclicDescent'),('ext.SmallGroups','program.census384'),
      ('AF.EqualGeneration','AF.KnownAnswer'),('AF.EqualIP','AF.KnownAnswer'),
      ('h.P2.8','h.T4.3'),('h.P2.8','h.T5.1'),('h.L4.5.0','h.T1.3'),('h.P2.9','h.L4.7.descent')]
    for a,b in required_edges:need(a in pred[b],'required actual interface '+a+' -> '+b)
    need(('UA.SK','AL.4','comparison') in pairs and 'UA.SK' not in pred['AL.4'],'the independently proved one-edge specialization is not an imported premise')
    need(not any(a in ['ext.Atlas','ext.CoxeterMoser','ext.ConderTight','ext.ConderBound','ext.MW20','ext.LZ25','ext.Magma','ext.QuotientCriteria'] and k in LOGICAL and ns[b]['side']=='new' for a,b,k in pairs),'no historical external dependency silently imported into complete current proof')
    need(len(g['accepted_scope_spans'])==p['accepted_proof_context_spans']==len(original['proof_regions'])==17,'all exact accepted regions')
    for key,s in g['accepted_scope_spans'].items():
        r=original['proof_regions'][key];span(s)
        need(s['path']==BASE+r['path'] and (s['start_codepoint'],s['end_codepoint_exclusive'],s['sha256_utf8'])==(r['start'],r['end'],r['sha256']),'unchanged accepted TeX span')
    need(g['checks']==tally(g),'exact inventory')
    need(g['source_bindings']['L012']['physical_pages']==17 and g['source_bindings']['L012']['pdf_cost'] is None,'exact unweighted primary edition')
    return dict(**tally(g),immutable_inputs=len(ins),exact_contexts=len(spans),row_closures_checked=99,
      principal_routes_checked=1,additional_routes_checked=len(g['additional_current_outputs']),logical_acyclic=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output file')
    g=json.loads((a.packet/'logical_graph.json').read_text());c=json.loads((a.packet/'coverage.json').read_text());p=json.loads((a.packet/'protocol.json').read_text())
    roots={'research':a.study_root,'public':a.public_root};result=validate(g,c,p,roots);controls=[]
    for label in ['omitted_row','span_changed','edge_reversed','logical_cycle','missing_actual_kernel','missing_lattice_adapter','code_dropped','formal_as_premise','historical_as_premise','excluded_recovered','classical_claimed_proved','sign_correction_hidden','wrong_formal_count','unknown_cost_zero','known_answer_new_credit','source_bindings_changed','unused_theory_discount','stale_inventory']:
        gg,cc,pp=copy.deepcopy(g),copy.deepcopy(c),copy.deepcopy(p)
        if label=='omitted_row':cc['rows'].pop()
        elif label=='span_changed':gg['nodes'][0]['locators'][0]['sha256_utf8']='0'*64
        elif label=='edge_reversed':gg['edge_orientation']='use -> prerequisite'
        elif label=='logical_cycle':
            e=copy.deepcopy(next(e for e in gg['edges'] if (e['source'],e['target'])==('UA.K0','UA.K')));e['source'],e['target']=e['target'],e['source'];gg['edges'].append(e)
        elif label in ['missing_actual_kernel','missing_lattice_adapter']:
            pair=('program.kernel64','AF.Affine64') if label=='missing_actual_kernel' else ('AL.RawInvariant','program.affine66')
            gg['edges']=[e for e in gg['edges'] if (e['source'],e['target'])!=pair]
        elif label=='code_dropped':gg['required_mathematical_programs'].pop()
        elif label=='formal_as_premise':next(e for e in gg['edges'] if e['kind']=='formal_scope')['kind']='proof_use'
        elif label=='historical_as_premise':next(e for e in gg['edges'] if e['source']=='h.T4.3' and e['kind']=='attribution')['kind']='proof_use'
        elif label=='excluded_recovered':next(r for r in cc['rows'] if r['id']=='L012.table1')['new_outputs']=['AF.ExistenceRange']
        elif label=='classical_claimed_proved':next(r for r in cc['rows'] if r['id']=='retained.Burnside')['new_outputs']=['AF.DihedralQuotient']
        elif label=='sign_correction_hidden':next(n for n in gg['nodes'] if n['id']=='h.L4.5.0')['documentary_flags']=[]
        elif label=='wrong_formal_count':gg['formal_evidence']['report_count']=18
        elif label=='unknown_cost_zero':gg['nodes'][0]['cost']=0
        elif label=='known_answer_new_credit':gg['new_question_credit']=1
        elif label=='source_bindings_changed':gg['immutable_inputs'][0]['sha256']='0'*64
        elif label=='unused_theory_discount':gg['measurement']['unused_common_statements_not_removed']=False
        elif label=='stale_inventory':gg['checks']['edges']+=1
        if label!='stale_inventory':gg['checks']=tally(gg)
        try:validate(gg,cc,pp,roots)
        except ValueError as exc:controls.append(dict(name=label,rejected=True,reason=str(exc)))
        else:raise RuntimeError('corruption accepted '+label)
    report=dict(status='PASS_AUTHOR_LOGICAL_BINDINGS_SCOPE_AND_CONTROLS',**result,negative_controls=controls,
      independent_semantic_review=False,primary_text_exported=False,weights_assigned=False,
      compression_ratio=None,new_source_credit=0,new_question_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['nodes_by_category','edges_by_kind','negative_controls']}))
if __name__=='__main__':main()
