from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
P=S/'computation/f009/validated_cache_resume01'
assert sha(P/'manifest.json')=='72f97fa580e80f7fd7634bf7ab99d31d2c2817a2cdebaf97c1a725ca96ca02dc'
assert sha(P/'plan01.json')=='b26afbf5803c115cd4c5a8c7ee4ab2a427f1fdb535356e0c789bba016edf6fce'
assert len(json.loads(Path('/private/tmp/f009_validated_owner_controls_root01.json').read_text())['checks'])==29
c=m.Closure();c.packet('computation/f009/validated_cache_resume01');c.packet('computation/f009/validated_cache_calls_root_review');c.add(__file__)
for p in ['/private/tmp/f009_validated_owner_controls_root01.json','/private/tmp/f009_validated_owner_preflight_root01.json']:c.add(p)
status='ACCEPTED_F009_VALIDATED_CACHE_TWO_INTERVAL_OWNER'
c.finish('computation/f009/validated_cache_resume_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the whole owner and exact predecessor diff. Only validate and gate change: the specific accepted initialization and profile, actual import closure, preserved failed startup and exact gate status. The execution main and resource guard remain identical. Two independent initial dictionary acquisitions still occur inside the guard, not via a new standalone full-size probe.',
 'Fresh29 damage/boundary controls and actual owner preflight pass, including parent1324, exact210004-key dictionary, distinct snapshot and coverage acceptances, old actual-loader mismatch, concrete writer inventory, caller gate and absent-output conditions.',
 'Release exact plan b26afbf5803c115cd4c5a8c7ee4ab2a427f1fdb535356e0c789bba016edf6fce: at most two300second writer intervals,600total targetseconds,7200second owner,4GiB sampled familyRSS and free-spacefloor,2GiB sampled output. Owner controls its process group and terminal resource stops; no automatic successor or cap change.',
 'The historical bootstrap is only an observation. The new writer has no guaranteed time or memory improvement; a timeout before request stops with zero credit and no collector/successor. Every completed prefix still needs the two independent transition acquisitions. No whole-source credit is released.'
]))

P=S/'computation/f004/q8_branch54_inventory01'
assert sha(P/'manifest.json')=='2e150c26668296973d005be1b348ae92a6524909da3735d36bddc46e9423c19a'
assert sha(P/'plan01.json')=='d301d348ad0c1374af24ea2dd3604c4ad3038c84e13579b6df3bc4b348982122'
assert len(json.loads(Path('/private/tmp/f004_q8_branch54_controls_root01.json').read_text())['checks'])==11
c=m.Closure();c.packet('computation/f004/q8_branch54_inventory01');c.packet('computation/f004/q8_branch53_root_adoption');c.add(__file__)
for p in ['/private/tmp/f004_q8_branch54_controls_root01.json','/private/tmp/f004_q8_branch54_preflight_root01.json']:c.add(p)
status='ACCEPTED_F004_Q8_BRANCH54_PREFIX_INVENTORY_OWNER'
c.finish('computation/f004/q8_branch54_inventory_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the full owner, exact predecessor diff and controls. The acquired ledger removes only completed[53,5], leaving506/686 complete and180pending. This request concerns[54,5], not the earlier rank-six branch54 work. The existing prefix caller and inventory reader are unchanged.',
 'Fresh11 request/resource controls and actual scientific-plan validation pass. The exact field8,branch54,rank5,depth3 inventory and literal returned inventory status are checked. The owner cannot continue from an incomplete inventory or resource stop.',
 'Release exact plan d301d348ad0c1374af24ea2dd3604c4ad3038c84e13579b6df3bc4b348982122 for one600second target with900second dispatch and300second reader,4GiB freefloor,2GiB familyRSS and256MiB output. No candidate evaluation or automatic successor is authorized by this request.',
 'An acquired inventory is not branch completion. The result still needs distinct root adoption; no numerical source row, original, conjecture or compression credit follows from launching it.'
]))

P=S/'geometry/psl2_rank_two';assert sha(P/'subdivision_automorphisms_independent_review/manifest.json')=='7ecd805c5d1c3c9e3dea81cafabce222aaacc4b33da774cf7c96a9631827f0c4'
c=m.Closure();c.packet('geometry/psl2_rank_two/full_automorphisms');c.packet('geometry/psl2_rank_two/subdivision_automorphisms_independent_review');c.add(__file__)
status='ROOT_ADOPTED_L063_D16_FULL_AUTOMORPHISMS'
c.finish('geometry/psl2_rank_two/subdivision_automorphisms_root_adoption',status,dict(status=status,author='root',distinct_reviewer='j3_recovery',review=[
 'Read the entire distinct review and adopt its conclusion. The reviewer checked all three proof pages, four source primes and exact native rebuild; all native pages agree. Root authorship and distinct mathematical review are explicit.',
 'Suppression yields a simple cubic graph by local primitivity and the more-than-two-vertices hypothesis. Tutte bounds the extension index by2. The self-normalizing stabilizer kills the centralizer, so the full group embeds in AutG preserving the S4 class; outer interchange excludes the proper extension.',
 'The result is conditional on the stated embedded configurations and attributed classical premises. All four specified full-Aut assertions are covered; S4/S4, whole-source completion and measured compression remain separate.'
]))
