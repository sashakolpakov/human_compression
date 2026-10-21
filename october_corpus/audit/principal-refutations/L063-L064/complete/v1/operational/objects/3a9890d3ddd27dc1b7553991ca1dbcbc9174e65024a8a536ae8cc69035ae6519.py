from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

Y=S/'geometry/suzuki_incidence';P=Y/'higher_publication_work'
assert sha(P/'registration_candidate01/manifest.json')=='3f3a25a05cdbe7c4f0a0c40407bb7f3a5d45b3d165971106cb0e11630a7d1fcb'
assert sha(P/'integration01/manifest.json')=='c84ce6b8f4ad45e128c7bfaf6f55953b54ec6b7f715074548dda24c6ea8eb888'
assert json.loads(Path('/private/tmp/l110_candidate_root01.json').read_text())['fully_treated']==97
assert json.loads(Path('/private/tmp/l110_install_inputs_root01.json').read_text())['payload_files']==1428
c=m.Closure()
for n in ['higher_publication_work/registration_candidate01','higher_publication_work/integration01','higher_source_root_review','higher_publication_operational_root_review']:c.packet('geometry/suzuki_incidence/'+n)
for p in [__file__,'/private/tmp/l110_candidate_root01.json','/private/tmp/l110_install_inputs_root01.json']:c.add(p)
status='ACCEPTED_L110_SOURCE_COMPLETION_REGISTRATION'
c.finish('geometry/suzuki_incidence/higher_publication_registration_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',review=[
 'Read the entire candidate checker, installation wrapper, finalizer and installed verifier. The semantic partition adds L110 alone:97 complete,8 outstanding,92 ordinary recoveries,9 principal refutations,101 principal dispositions and53 measured originals. Source principal counterexample remains counted once. All105 mathematical originals occur exactly once in the completed/outstanding partition.',
 'Reviewed the complete README, completion and protocol diffs; viewed the two changed protocol pages. The105-page reading volume is described as a full proof collection, with no compression factor or complete corrected classification claimed. Stronger unproved variants remain explicit.',
 'Fresh read-only candidate check passed4012 bindings, four count damage controls and three documentary-boundary controls. Fresh exact installation-input check passed1428 files,185644421 bytes and273 explicit premises. No source-premise bytes or new Markdown paths enter the payload.',
 'The installer binds the clean70bc355bc5dff1ea86b1b42ac836bfa3136bd71a predecessor, validates all paths and bytes before mutation, retains overwritten bytes in history and requires a4GiB reserve. Existing verifier functions are preserved by AST comparison; only dispatch changes. Final root gate and tracked manifest are still required after installation.',
 'Accept this exact source-completion transition. No new conjecture, Lean, ordinary-recovery or measurement credit; the stopping condition remains complete reviewed treatment of105 then stop.'
]))

Z=S/'geometry/suzuki_subgroups';P=Z/'publication_work'
assert sha(P/'portable_handoff/manifest.json')=='4ddb1c00101f0b2f1bbeb79faf06101bd8b296a528af9fe24b3e43f62ae55331'
r=json.loads((P/'root_portable02/report.json').read_text());assert r['logical_files']==34333 and r['rebuilt_pages']==36 and r['status']=='PASS_PUBLIC_L115_COMPLETE_CORRECTED_SOURCE_TREATMENT'
c=m.Closure();c.packet('geometry/suzuki_subgroups/publication_work/portable_handoff');c.packet('geometry/suzuki_subgroups/principal_root_review');c.add(__file__);c.add('/private/tmp/l115_portable_streams_root01.json')
for p in(P/'root_portable02').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L115_PORTABLE_COMPLETE_SOURCE_TREATMENT'
c.finish('geometry/suzuki_subgroups/publication_operational_root_review',status,dict(status=status,author='l070_publication',reviewer='root',review=[
 'Read the whole portable checker and mathematical replay adapter. Exact retained pure arithmetic and finite-incidence readers are acquired; only JSON integer-key normalization joins diagram comparisons. No new factorization, group census, private fallback or altered scientific predicate is used.',
 'Fresh replay passed71.50seconds,34333 logical files,21132 verified payload objects and2583 explicit documentary/environment premise objects. It certifies180 integers with694 prime certificates,60 numerical rows,29 diagrams,75 inner classes and70 source claims; twelve source-damage controls pass. Codec path, corruption and bounded-stream controls pass.',
 'All eight manuscripts rebuild to36 pages. A separate fresh comparison finds every rebuilt page drawing stream and every embedded font program identical to the accepted PDF. Original exact imported manuscripts remain retained. This is additional native assurance, not fresh mathematical proof credit.',
 'Inspected the documentary/environment classifications and recognized source/library families; three project transfer-metadata files are retained as payload rather than premises. Exact originals and their native page excerpts are documentary premises; scientific outputs and review records remain in the public transport. Stage01 failure is retained and stage02 changes only the declared normalization.',
 'Accept portable packaging of the already accepted complete corrected L115 treatment. Registration against the next public predecessor remains separate. This gate changes no catalogue count, conjecture tally, Lean status or compression factor.'
]))

F=S/'computation/f004';P=F/'q8_branch53_union_handoff01'
assert sha(P/'manifest.json')=='700e0e862600eea5a3e691e940dfb8755795d9340929ccd6409cd17b99f0cf24'
result=Path('/private/tmp/f004_branch53_root01/result.json');assert sha(result)=='d950f1e3e4265f296ac290924cc2430f47ebd816391f2c727e74625cd0705be0'
r=json.loads(result.with_name('receipt.json').read_text());assert r['terminal']=='RETURNED' and r['returncode']==0 and r['error'] is None
c=m.Closure();c.packet('computation/f004/q8_branch53_union_handoff01');c.add(__file__)
for p in result.parent.iterdir():
 if p.is_file():c.add(p)
status='ACCEPTED_F004_Q8_COMPLETE_BRANCH53'
c.finish('computation/f004/q8_branch53_root_adoption',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the unchanged complete-union composer, exact request and resource owner. The70 child positions form the full disjoint branch53 partition; completed acquired children19 and22 and all direct child receipts are explicitly joined. No timed-out prefix supplies completion credit.',
 'Fresh distinct read-only composition returned in1099.94seconds with179961856B sampled peak family RSS and empty stderr. Its686177-byte result is byte-identical to the separately acquired author result d950f1e3e4265f296ac290924cc2430f47ebd816391f2c727e74625cd0705be0. The1800second,2GiB sampled RSS,64MiB output and4GiB floor limits were retained.',
 'Accept the empty complete branch53 at fixed job[53,5]. This supplies one q8 root branch and permits its ledger count to move505to506 of686, not a complete q8 row or a completed F004 original. No new group target was run by this acquisition.'
]))

P=S/'geometry/psl2_rank_two'
assert sha(P/'arc_actions_independent_review/manifest.json')=='8d6b6969092481239346873c70d9c23c28d28b661abbf1720b1ea5ba140a57b5'
c=m.Closure();c.packet('geometry/psl2_rank_two/arc_actions');c.packet('geometry/psl2_rank_two/arc_actions_independent_review');c.add(__file__)
status='ROOT_ADOPTED_L063_ALL44_LOCAL_ARC_VALUES'
c.finish('geometry/psl2_rank_two/arc_actions_root_adoption',status,dict(status=status,author='root',distinct_reviewer='j3_recovery',review=[
 'Adopt the distinct review after reading its entire report. The six-page root-authored proof was read and freshly rebuilt by the reviewer, who viewed all six pages and all44 source assignments. This is root adoption of a distinct review, not independent review of my own proof.',
 'The group-action arguments prove all44 local arc-transitivity values conditional on actual embedded configurations. Degree-two extension, affine stabilizers, the S4/D24 obstruction, distinct four-group kernels and the S4/D16 path chain are explicitly checked. Both orientations and the source orientation/name typos are covered.',
 'Native text agrees. The recorded differing raster dimensions result from105dpi versus100dpi and are not a mathematical comparison failure. Counts, existence, full automorphism upper bounds and whole-source completion remain separate.'
]))

Q=P/'full_automorphisms';assert not(Q/'manifest.json').exists()
(Q/'scope.json').write_text(json.dumps(dict(status='AUTHOR_L063_D16_FULL_AUTOMORPHISMS_PENDING_DISTINCT_REVIEW',author='root',pages=3,source='L063 p386',native_pages_directly_viewed=True,classical_premises=['Tutte cubic stabilizer bound48','PSL2 prime simplicity and automorphism group','maximal S4 and outer exchange of its two classes'],whole_original_credit=0),indent=2)+'\n')
exports=[]
for p in sorted(Q.rglob('*')):
 if p.is_file():exports.append(dict(path=str(p.relative_to(Q)),bytes=p.stat().st_size,sha256=sha(p)))
(Q/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_L063_D16_FULL_AUTOMORPHISMS_PENDING_DISTINCT_REVIEW',exports=exports),indent=2)+'\n')
print('full_automorphisms',sha(Q/'manifest.json'))
