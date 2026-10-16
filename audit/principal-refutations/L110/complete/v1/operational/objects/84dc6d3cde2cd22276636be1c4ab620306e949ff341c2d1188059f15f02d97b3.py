from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();F=S/'computation/f004'
c.packet('computation/f004/q11_branch68_union_handoff01')
root=F/'q11_branch68_union_root01';r=json.loads((root/'result.json').read_text())
assert (root/'result.json').read_bytes()==(F/'q11_branch68_union_handoff01/author01/result.json').read_bytes()
assert r['status']=='COMPLETE_FIXED_RANK4_CANDIDATE_UNION'
assert (r['common']['field'],r['common']['branch'],r['common']['rank'],r['candidate_count'],r['tuple_count'])==(11,68,4,3801,3)
assert [t['index'] for t in r['closed']]==list(range(1,3802))
assert [t['index'] for t in r['closed'] if t['tuple_count']]==[67,822,1303]
for row in r['verified_files']:c.binding(row)
for p in root.iterdir():
 if p.is_file():c.add(p)
assert json.loads((root/'receipt.json').read_text())['status']=='PASS'
c.add('/private/tmp/q11_union_root_reader01.py');c.add(__file__)
c.finish('computation/f004/q11_branch68_union_root_adoption','ACCEPTED_F004_Q11_COMPLETE_BRANCH68',dict(
 reviewer='root',author='finite_recoveries',field=11,branch=68,rank=4,candidate_count=3801,tuple_count=3,
 positive_indices=[67,822,1303],new_complete_jobs=1,proposed_complete_q11_jobs=61,total_q11_jobs=272,
 review=[
 'Read the six-part union scope, preserved original partial boundary, exact collector invocation and output guard. Reuse the independently accepted small-action inventory and unchanged candidate collector.',
 'A fresh bounded root collector reacquired all3801 candidates exactly once across six disjoint intervals. It returned PASS in102.87seconds, peak507838464 sampled RSS bytes, and its entire17517708-byte result is byte-identical to the author result.',
 'Rebound every one of the900 verified input/output files together with the complete package closure. The original partial receipt remains partial; only its closed prefix801..1477 is used.',
 'The three positive tuples at67,822,1303 are retained. This is complete coverage of one fixed branch, not an emptiness statement and not completion of the field or manuscript.',
 'Ledger authority is limited to removing the single job[68,4]. No automatic successor is included.'
 ],source_credit=0,whole_field_credit=0,fresh_gap_calls=0))

Y=S/'geometry/suzuki_incidence';p=Y/'panel_request02'
c=m.Closure();c.packet('geometry/suzuki_incidence/panel_request02')
req=json.loads((p/'request.json').read_text())
for row in req['bindings']:c.binding(row)
c.packet('geometry/primitive_pairs/table_request02_root_review')
for n in ['panels.py','run.py']:
 assert (p/n).read_bytes()==(Y/'panel_request01'/n).read_bytes()
old=(S/'geometry/primitive_pairs/table_request02/run.py').read_text()
expected=old.replace('One reviewed library export;','One reviewed literal panel calculation;').replace('HOLD_L036_MARK_EXPORT_DISK_RESERVE','HOLD_L114_SAVED_PANEL_DISK_RESERVE').replace('L036_MARK_EXPORT_TERMINAL','L114_SAVED_PANEL_TERMINAL')
assert expected==(p/'run.py').read_text()
assert (req['deadline_seconds'],req['output_cap_bytes'],req['authorized_invocations'],req['automatic_successor'])==(10,1048576,1,False)
c.add(__file__)
c.finish('geometry/suzuki_incidence/panel_request02_root_review','ACCEPTED_L114_ONE_SAVED_MARKING_PANEL_DIAGNOSTIC',dict(
 reviewer='root',author='j3_recovery',authorized_invocations=1,deadline_seconds=10,
 review=[
 'Read the complete literal matrix program and owner. Its input is one retained marking; each group closure has an explicit bound of14 or10. Candidate cosets exhaust incidence with the first base parabolic by representatives in that parabolic; literal intersection with the second is the correct second incidence test.',
 'The accepted owner differs only in one descriptive docstring and two status strings. Exact request hashes, input hashes, sampled time/output/disk bounds, owned child termination and final checks remain unchanged.',
 'Directly viewed source pages45 and46. Page45 explicitly defines the distinguished-chamber residue through intersection subgroups; page46 uses that residue for flags in C. Root earlier interpreted page46 alone too strongly as prescribing the full incidence panel; the author correctly identified the page45 definition, and this correction is retained here.',
 'The diagnostic outputs actual panels regardless of size. An enlarged panel alone is not a refutation of the stronger formulation assuming local double transitivity on actual panels. Any source application must specify its literal definitions and separately check all hypotheses.',
 'One tiny invocation is released; no ambient group census, successor, scientific result or whole-source completion is accepted by this request.'
 ],source_credit=0))
