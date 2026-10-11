#!/usr/bin/env python3
"""Author mutation and actual failed-chamber controls; no independent-review claim."""
import copy,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('L073_reconcile',R/'programs/reconcile.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def load(p):return json.loads(p.read_text())
def check(work):
    args=[load(R/'data/phase180_source_notation.json'),load(R/'data/phase164_L073_table_contract.json')['rows'],load(work/'source_triples.json'),load(work/'canonical_triples.json'),load(work/'source_pairs.json'),load(work/'codes/mog_check.json')]
    result=[]
    def reject(name,fn):
        x=copy.deepcopy(args);fn(x)
        try:m.build(*x)
        except (ValueError,KeyError,IndexError,TypeError):result.append(name)
        else:raise ValueError('missed negative control '+name)
    reject('omit_triple_class',lambda x:x[2]['triples'].pop())
    reject('omit_pair_class',lambda x:x[4]['triples'].pop())
    reject('omit_physical_source_row',lambda x:x[1].pop())
    reject('duplicate_witness_identifier',lambda x:x[2]['triples'][1].update(witness=1))
    reject('shared_class_signature',lambda x:x[2]['triples'][1]['signatures'].append(x[2]['triples'][0]['signatures'][0]))
    reject('omit_canonical_signature',lambda x:x[3]['triples'][0].update(signatures=[]))
    # A noncanonical signature must remain in the source complement family.
    index=next(i for i,(b,c) in enumerate(zip(args[2]['triples'],args[3]['triples'])) if len(b['signatures'])>len(c['signatures']))
    reject('silently_impose_canonical_endecads',lambda x:x[2]['triples'][index].update(signatures=x[3]['triples'][index]['signatures']))
    reject('malformed_literal_label',lambda x:x[1][0].update(label_text='M111(0,0)'))
    reject('uninterpreted_Borel_label',lambda x:x[1][0].update(Borel_text='undefined-group'))
    reject('omit_literal_pair_completion',lambda x:x[5]['explicit_pair_cases'].pop())
    reject('completion_dependent_pair_result',lambda x:x[5]['explicit_pair_cases'][0].update(actual_pair_id=[1,1]))
    reject('omit_colon_completion',lambda x:x[5]['completion_cases'].pop())
    reject('invent_colon_flag_transitivity',lambda x:x[5]['completion_cases'][0].update(flag_transitive=True))
    # These two are actual finite countermodels to replacing chamber tests by local generation alone.
    for case,orders in [(1,[2520,2520,1920]),(2,[2520,1920,1920])]:
        rows=[r for r in args[5]['completion_cases'] if r['case']==case]
        m.need(len(rows)==4 and all(r['residue_generated_orders']==orders and not r['flag_transitive'] and all(a>b for a,b in r['Helly_actual_expected']) for r in rows),'actual local-generation countermodel')
        result.append('local_generation_does_not_imply_flag_transitivity_case_'+str(case))
    return result
