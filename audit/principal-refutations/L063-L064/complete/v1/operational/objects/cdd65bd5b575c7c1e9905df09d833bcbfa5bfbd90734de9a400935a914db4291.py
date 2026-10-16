from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
P=S/'geometry/psl2_rank_two/publication_work';D=P/'stage01/audit/principal-refutations/L063-L064/complete/v1';O=Path('/private/tmp/psl2_portable_root01')
r=json.loads((O/'report.json').read_text());assert r['status']=='PASS_PORTABLE_L063_L064_SOURCE_COMPLETION' and r['source_claims']==dict(L063=122,L064=28) and r['native_pages']==52
c=m.Closure();c.packet('geometry/psl2_rank_two/source_synthesis_root_review');c.add(D/'manifest.json')
for row in json.loads((D/'manifest.json').read_text())['exports']:c.add(P/'stage01'/row['path'],row)
for p in O.rglob('*'):
 if p.is_file():c.add(p)
c.add(__file__)
status='ACCEPTED_L063_L064_PORTABLE_COMPLETE_SOURCE_TREATMENT'
c.finish('geometry/psl2_rank_two/publication_operational_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',review=[
 'Read the entire portable checker, stage constructor and publication scope. The accepted segmented codec and transport reader are unchanged. Mathematical claims come from the separately accepted complete source treatment; the portable gate does not infer proofs from hashes or finite tests.',
 'Fresh independent portable replay passed in25.24seconds:1017 logical bindings,452 derived payload objects and232 distinct documentary/environment premises. All150 source claims and11 prior gates are retained; five ledger-damage controls, codec controls and two optimization guards pass.',
 'Replayed the four accepted field models, thirty-object duality and six order-bound cases. Two new TeX entry points rebuild; all52 native page rasters are byte-identical to the already visually reviewed and mathematically accepted volume. The ten imported proof editions remain exact.',
 'Inspected premise classifications and original-source/environment path families. Exact scholarly originals, source extracts and native images are documentary premises; installed programs, fonts and libraries are environment premises. Derived proof, code, finite results and review records remain transported payload. No private fallback or new Markdown path.',
 'Accept this exact portable package for joint registration of L063 and L064, retaining independent admissions and shared readable manuscript. Registration remains a separate transition. No new principal refutation, ordinary recovery, conjecture solution, Lean or compression measurement.'
]))
P=S/'computation/f004/q8_branch54_child9_inventory01';c=m.Closure();c.packet('computation/f004/q8_branch54_child9_inventory01');c.packet('computation/f004/q8_branch54_children1_8_root_adoption_v2');c.add(__file__)
status='ACCEPTED_F004_Q8_BRANCH54_CHILD9_FINAL_INVENTORY_REQUEST'
c.finish('computation/f004/q8_branch54_child9_inventory_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the complete owner, exact plan, all predecessor differences and damage controls. Only the owner validation substitutes branch54/child9 and the exact preceding1..8 adopted prefix; execution and resource guard remain unchanged.',
 'Fresh independent controls validate the actual prepared scientific plan and reject all nine declared scope/resource damages. The request binds corrected root adoption797fda95 and whole-job coverage506/686. Eight retained subtrees are not eight whole jobs.',
 'Release exactly one final inventory for branch54 child9:600second target,900second dispatcher,300second reader,2GiB sampled family RSS,256MiB observed growth and4GiB reserve. This constructs an inventory only, evaluates no candidates, and has no automatic successor. No completion credit is granted before actual acquisition.'
],released_target_calls=1,automatic_successor=False,whole_jobs_complete=506,whole_jobs_total=686,branch_closed_children=8,branch_total_children=70))
