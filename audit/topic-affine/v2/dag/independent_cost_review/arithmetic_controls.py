#!/usr/bin/env python3
"""Exercise independent arithmetic after integrity checks, using in-memory mutations."""
import argparse
import copy
import json
from pathlib import Path
import arithmetic


def run(study, packet):
    baseline = arithmetic.check(study, packet)
    actual_read = arithmetic.read
    cases = []
    v,f,u = 'calibrated_selected','NFC','characters_without_whitespace'
    def add(label, name, mutate, reason):
        cases.append((label, packet/name, mutate, reason))
    def increment(d): d[v][f][u] += 1
    add('alter one owner metric','weights.json',lambda d:increment(d['owner_costs']['UA.K']), 'Every independent owner metric')
    add('alter document total','weights.json',lambda d:increment(d['document_costs']['U_Affine']), 'Every document weight')
    add('duplicate a physical owner in an interface','weights.json',lambda d:d['node_interfaces']['UA.K']['owners'].append('UA.K'), 'Distinct existing')
    add('omit a complete required raw program','weights.json',lambda d:d['raw_program_alternative'].pop('program.kernel64'), 'Complete raw inventory')
    add('invent zero external cost','weights.json',lambda d:d['node_interfaces']['ext.FiniteGroups'].update(known_weight=0), 'Unknown proof cost')
    add('omit a logical prerequisite','weights.json',lambda d:d['individual_node_closures']['AF.ExistenceRange']['logical_nodes'].pop(), 'Exact logical prerequisite closure')
    add('omit a physical passage from a closure','weights.json',lambda d:d['individual_node_closures']['UA.K']['owners'].pop(), 'Union before sum')
    add('double count shared route text','weights.json',lambda d:increment(d['individual_node_closures']['UA.K']['known_extracted_subtotal']), 'Route subtotal')
    add('double charge printed code in the raw alternative','weights.json',lambda d:increment(d['individual_node_closures']['program.kernel64']['raw_program_alternative_subtotal']), 'Whole raw alternative')
    add('erase unknown dependency','weights.json',lambda d:d['individual_node_closures']['ext.FiniteGroups'].update(unknown_inputs=[]), 'Unknown dependencies preserved')
    add('claim expanded dependency cost zero','weights.json',lambda d:d['individual_node_closures']['UA.K'].update(expanded_dependency_cost=0), 'Unmeasured cost stays null')
    add('drop unused common text from acquisition','acquisition.json',lambda d:d['stages'][0]['complete_owner_ids'].pop(), 'Acquire complete local document')
    add('undercharge cumulative acquisition','acquisition.json',lambda d:increment(d['stages'][2]['cumulative_cost']), 'Cumulative complete library')
    add('apply a cross-topic discount','acquisition.json',lambda d:d.update(cross_topic_discount=True), 'Acquisition cost boundary')
    add('invent proof ratio from graph size','weights.json',lambda d:d.update(compression_ratio=1.2), 'Unmeasured global costs')
    add('claim a new solved question','weights.json',lambda d:d.update(new_question_credit=1), 'No new credit')
    old_partition=actual_read(study/'topic_Affine_dag_costs/partition.json')
    add('restore grammatically incomplete kernel passage','partition.json',
        lambda d:d['documents'].update(L012=copy.deepcopy(old_partition['documents']['L012'])), 'Complete kernel subject')
    reports=[]
    for label,path,mutate,reason in cases:
        def altered(p):
            d=actual_read(p)
            if p == path:
                mutate(d)
            return d
        arithmetic.read=altered
        try:
            arithmetic.check(study,packet)
        except ValueError as exc:
            arithmetic.require(reason in str(exc), 'Control failed for unrelated reason: '+label+' / '+str(exc))
            reports.append(dict(name=label,rejected=True,reason=str(exc)))
        else:
            raise ValueError('Corruption accepted: '+label)
        finally:
            arithmetic.read=actual_read
    return dict(status='PASS_INDEPENDENT_ARITHMETIC_CONTROLS',baseline=baseline,controls=reports,
                method='Frozen bytes and integrity checks are left intact. The independent reader mutates one in-memory semantic object; rejection must match the declared arithmetic or policy reason.',
                controls_are_mathematical_proof_tests=False,primary_text_exported=False)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True)
    p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();arithmetic.require(not a.out.exists(),'fresh output')
    r=run(a.study_root,a.packet);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(r['status'],len(r['controls']))
