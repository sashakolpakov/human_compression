from pathlib import Path
import json,sys,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('computation/f009/streaming_io_work')
c.add(Path('/private/tmp/f009_streaming_root_controls01.json'));c.add(Path('/private/tmp/f009-streaming-root-01.png'));c.add(Path(__file__))
r=json.loads(Path('/private/tmp/f009_streaming_root_controls01.json').read_text())
if r['status']!='PASS_STREAMING_IO_VALUE_CONTROLS' or r['count']!=34:raise ValueError('root controls')
c.finish('computation/f009/streaming_io_root_review','ACCEPTED_F009_STREAMING_DICTIONARY_IO_EQUIVALENCE',dict(
 reviewer='root',author='finite_recoveries',
 review=['Read the entire helper, controls, one-page proof and allocation findings; directly viewed the complete native proof page.',
 'The induction on canonical records proves exact concatenation, including context, iteration order, entry validation and newlines. Literal chunk comparison and final EOF check are equivalent to whole-file byte equality for a valid admitted dictionary.',
 'Streaming SHA256 computes the same path, length and digest as the acquired file pin, provided the file remains unchanged; the existing input and final checks remain required.',
 'Fresh independent controls passed all34 cases against the AST bodies of the actual previous functions, including ordering, boundary lengths, invalid entries and byte damage.',
 'The actual prior RSS stop is retained. The claimed allocation improvement eliminates full serialized-file temporaries, but does not bound the two dictionaries, allocator or writer. The stopped interval02 cache is only an allocation observation, not a coverage premise.'],
 scope='Equivalence of the narrow streaming helper only. Any new caller still requires full-size loading and resource checks. No target, root, source or conjecture credit.',
 controls=34,new_target_runs=0,source_row_credit=0))
c=m.Closure();c.packet('geometry/primitive_pairs/algorithm_scope');c.packet('geometry/primitive_pairs/algorithm_scope_independent_review');c.add(Path(__file__))
r=json.loads((S/'geometry/primitive_pairs/algorithm_scope_independent_review/review.json').read_text())
if r['status']!='ACCEPTED_L036_COSET_ACTION_SCOPE_CORRECTION' or r['author']!='/root' or r['reviewer']!='/root/j3_recovery':raise ValueError('distinct review')
c.finish('geometry/primitive_pairs/algorithm_scope_review_adoption','ADOPTED_L036_COSET_ACTION_SCOPE_DISTINCT_REVIEW',dict(
 author='root',reviewer='j3_recovery',adopter='root',
 review=['Adopts the distinct agent review of the root-authored proof, rather than describing root self-review as independent.',
 'The independent reviewer read the complete two-page proof and original source pages4-5, replayed the exact example and checked a separate coordinate enumeration of all six ordered pairs of distinct maximal subgroups in C2 squared.',
 'The corrected algorithm keeps the original subgroup K and pulls back only the point stabilizer. Complete maximal-subgroup representatives and an exact final Aut(G) equivalence test remain premises.',
 'The correction concerns arbitrary finite groups; the simple sporadic group numerical tables remain separate unpaid source obligations.'],
 scope='Reviewed algorithm-scope correction and finite counterexample only; no whole L036 completion or new principal-refutation credit.',
 source_completion_credit=0,new_principal_refutation=0))
