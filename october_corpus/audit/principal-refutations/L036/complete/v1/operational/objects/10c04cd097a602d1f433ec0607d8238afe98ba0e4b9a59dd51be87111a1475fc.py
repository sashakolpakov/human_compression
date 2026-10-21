from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');F=S/'computation/f009';P=S/'geometry/primitive_pairs';B=S/'algebra/subgroup_atlas'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('computation/f009/streaming_session_resume01');c.packet('computation/f009/streaming_session_bootstrap_result_root_review')
for row in json.loads((F/'streaming_session_resume01/plan01.json').read_text())['inputs']:c.binding(row)
q=Path('/private/tmp/f009_streaming_resume_root_controls01.json');r=json.loads(q.read_text())
if r['status']!='PASS_STREAMING_RESUME_CONTROLS'or len(r['checks'])!=18 or not r['guard_byte_identical']:raise ValueError('request controls')
c.add(q);c.add(Path('/private/tmp/f009_streaming_resume_root_controls01.stderr'));c.add(Path(__file__))
c.finish('computation/f009/streaming_session_resume_root_review','ACCEPTED_F009_STREAMING_TWO_INTERVAL_REMAINDER_REQUEST',dict(
 reviewer='root',author='finite_recoveries',
 review=['Read the exact request, full owner and changes, guards and controls. The scientific caller is the independently accepted streaming edition; only owner bindings and prefix checks differ from the acquired owner.',
 'The accepted dictionary has175109 keys and prefix895 coverage is separately acquired. The old stopped interval beginning895 contributes no receipt or cache premise. Actual successful bootstrap results and both separate admissions are bound.',
 'All18 fresh root request and resource controls passed. The native owned-process-group guard is byte-identical to the acquired guard. Limits remain4GiB combined RSS,4GiB free reserve,2GiB output and7200seconds total wall, with sampled rather than continuous observations.',
 'The two300second writer intervals are a maximum of600 scientific seconds, not a claim to cover all remaining13581 roots. Returned completed roots need independent acquisition. Two initial dictionaries occupy about1.75GiB in the actual bootstrap and two emitted caches about774MB; writer and growth costs remain subject to the combined guard.'
 ],
 scope='One bounded two-interval invocation from895 only. Held until prior queue obligations release the substantial lane. No automatic successor, source credit, conjecture, Lean or measurement.',
 start=895,intervals=2,seconds_per_interval=300,target_budget_seconds=600,authorized_initial_invocations=1,target_runs=0,source_credit=0))

c=m.Closure();c.packet('geometry/primitive_pairs/m11_graph_request01');W=P/'m11_graph_request01'
req=json.loads((W/'request.json').read_text())
for row in req['bindings']:c.binding(row)
data=json.loads((W/'inputs.json').read_text());registry=json.loads((B/'structural_atoms_v1/registry.json').read_text())
if data['group_model']!=registry['models'][0]:raise ValueError('literal acquired model')
spec=importlib.util.spec_from_file_location('source_join',B/'structural_labels_pilot_v1/source_join.py');j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
if data['subgroup_generators']!=j.m11_generators((B/'numeric_work/m11_literal02/groups.g').read_text()):raise ValueError('literal subgroup representatives')
numeric=json.loads((B/'numeric_work/m11_literal02/numeric.json').read_text())
if sorted(x['child']for x in numeric['edges']if x['parent']==39)!=sorted(data['maximal_class_positions']):raise ValueError('maximal class selection')
for p in(P/'m11_graph_controls_root01').iterdir():
 if p.is_file():c.add(p)
c.add(Path(__file__))
c.finish('geometry/primitive_pairs/m11_graph_request_root_review','ACCEPTED_L036_M11_LITERAL_GRAPH_REQUEST',dict(
 reviewer='root',author='j3_recovery',
 review=['Read the complete finite-permutation program, coverage/girth/design argument, owner and four owner controls. Independently joined the literal model and all39 subgroup arrays to acquired L054 records; the five selected classes are exactly the maximal edges below class39.',
 'Closure under the two generating permutations gives complete subgroup conjugacy orbits and then every unordered pair orbit. Explicit conjugators identify actual intersections with acquired representatives; subgroup names are not inferred from orders.',
 'Literal right-coset partitions and common element assignments produce precisely the incidence graph. Inversion identifies this graph with the left-coset convention. All-root breadth-first distances give eccentricities and girth; every non-tree edge creates a closed walk containing a cycle, and a shortest cycle yields the matching upper bound from a root on it.',
 'The design calculation checks every subset at each reached strength, records witnesses at the first failure, and separately handles repeated full blocks. The fixed250000-subset cap retains partial status rather than asserting an unchecked strength.',
 'Fresh root small controls passed for C6,C8,K2,3, repeated complete blocks, explicit non-design witnesses and asymmetric adjacency. All four fresh owner controls passed, including interruption cleanup, final input mutation and post-return output violation.',
 'One60second Python call is bounded by the exact1GiB address-space setting,16MiB output,4GiB launch reserve and2GiB emergency floor. Address space is distinct from whole-family RSS. Final input rehash and child reap are mandatory; no successor is released.'
 ],
 scope='Acquire the remaining M11 numerical graph data only. The old six-case IP2 census is not used. Exact returned evidence, intersection naming, source Tables3/4 joins and whole-source synthesis remain subsequent obligations.',
 authorized_initial_invocations=1,target_runs=0,new_subgroup_census=False,source_completion_credit=0))
