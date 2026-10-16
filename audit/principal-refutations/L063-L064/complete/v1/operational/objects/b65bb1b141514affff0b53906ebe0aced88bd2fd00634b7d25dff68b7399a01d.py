from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

P=S/'geometry/psl2_rank_two/scalar_orbits'
assert sha(P/'manifest.json')=='06ca17e7140e11ec1db39e72def60bfd1aec6b7a17d9a555358954899b9cedb1'
r=json.loads(Path('/private/tmp/l063_scalar_orbits_root01/report.json').read_text());assert r['native_pages']==5 and r['dependencies']==154
c=m.Closure();c.packet('geometry/psl2_rank_two/scalar_orbits');c.add(__file__)
for p in Path('/private/tmp/l063_scalar_orbits_root01').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L063_L064_SCALAR_ORBITS_AND_UNORDERED_COUNTS'
c.finish('geometry/psl2_rank_two/scalar_orbits_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',review=[
 'Read the complete five-page proof and six source-claim joins; viewed all five freshly rebuilt native pages. Fresh replay acquires154 dependencies and gives five byte-identical native pages. The fixed source Section2 explicitly uses unordered sets of parabolics; Tables1 and5 and the appendix formulas are compared under that convention.',
 'The Borel normalizer is exactly B: its unique unipotent fixed point forces affine form, aK=K forces the multiplier into K*, and a nonidentity scalar forces the translation into K. Inside a subfield group the given full-order unipotent subgroup is Sylow and its normalizer is the Borel, justifying the unique containing H. Thus planes through K are precisely projective lines of F/K; the inner normalizer acts trivially and field automorphisms supply the residual orbit action.',
 'The affine extension argument retains all translations and the given scalar subgroup. If the translation space is larger than K, maximality forces a dimension-one quotient; if it equals K then every affine element already belongs to B. This establishes the displayed family, not a global exhaustion of all nonaffine overgroups.',
 'For E16:3 subgroups the multiplier field degree divides both2 and oddprime r, so scalar stabilizer is F4*. Dividing the Gaussian plane count gives(4^(r-1)-1)/15. For pairs through the fixed line the count is instead(4^(r-1)-1)/3. These distinct counts are not conflated.',
 'Burnside analysis correctly handles r2,r3 and r>3 separately. Relative trace excludes nonzero fixed vectors for the order-r Frobenius; semilinear fixed quotient is F_(2^r)/F2. At r3 the commuting semilinear involution exchanges the two nontrivial eigenspaces, proving both occur. Fixed-line counts5,0,2,3,2,0 give two outer classes.',
 'In characteristic3 the PSL affine normalizer has only slope1 because-1 is nonsquare in the odd extension. Containing A4 groups form the additive torsor F/F3, and unordered differences identify v with-v. This halves the printed inner counts; the outer sign and Frobenius already make that identification, leaving their printed counts unchanged. At degree3 the unipotent quotient action fixes two nonzero vectors and Burnside gives two classes. The explicit translation conjugator proves the missing identification without a census.',
 'Original formulas and classical subgroup/automorphism facts are attributed; the common parameter-space derivation and convention correction are identified. Accept these six claim groups only. Neither L063 nor L064 is yet complete; no new original/refutation, open conjecture, Lean or compression credit.'
]))

P=S/'computation/f012/unit_triangle_work';assert sha(P/'manifest.json')=='ad9f6b925a145dc29d887fef1112aae4c720408e5613f816b5edbba8cb1c77f3'
c=m.Closure();c.packet('computation/f012/unit_triangle_work');c.add(__file__);c.add('/private/tmp/f012_unit_triangle_root01.json')
status='ACCEPTED_F012_UNIT_CORNER_UNIQUE_TRIANGLE'
c.finish('computation/f012/unit_triangle_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the entire one-page proof and literal saved-state reader; viewed the native page. The lemma assumes precisely a simple six-regular graph with cyclic orders and corner sums at least7 on each simple triangle and four-cycle.',
 'A unit corner forces the other two triangle corners to be antipodal. Any second common neighbor uses both still-available distance2 positions, hence has opposite corner3; its distances from the first antipodes are1. The resulting simple four-cycle has sum1+1+3+1=6, a contradiction. Distinctness of all four vertices follows from simplicity and the second-neighbor assumption.',
 'Fresh read-only acquisition of all five actual parents verifies the three fixed hexagons, their intersections0,3,17 and costs3,1,3. All five already satisfy the uniqueness restriction, so none is excluded. No completion or production search was run.',
 'Accept the conditional mathematical restriction and its fixed-parent application only. Production pruning requires separate implementation and equivalence review; no source or conjecture completion is inferred.'
]))

P=S/'geometry/sporadic_polytopes/endpoint_method_work/ru8_timing_diagnostic_work'
assert sha(P/'manifest.json')=='50c72e367eb6890ceae81a9ec112bf36bc946bc83c61cbdd304fea88de60b13d'
assert sha(P/'request.json')=='4464e482fcf7ddd4ac51035ce75d226265418564831afbdb7ec1c8509303803a'
r=json.loads(Path('/private/tmp/ru8_timing_root_preflight01.json').read_text());assert r['inputs']==23286 and r['target_runs']==0
c=m.Closure();c.packet('geometry/sporadic_polytopes/endpoint_method_work/ru8_timing_diagnostic_work');c.add(__file__);c.add('/private/tmp/ru8_timing_root_preflight01.json')
for p in Path('/private/tmp/ru8_timing_root_controls01').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_RU8_TIMING_DIAGNOSTIC_V1'
c.finish('geometry/sporadic_polytopes/endpoint_method_work/ru8_timing_diagnostic_root_review',status,dict(status=status,author='l070_publication',reviewer='root',review=[
 'Read the diagnostic argument, every fusion/batch/owner diff, whole owner and fixed-sequence controls. Added integer counters, Runtime calls and Info messages do not influence the seed stream, membership checks, orbit keys, dictionary, disjointness, closure or final mass. All mathematical group operations remain in their original order.',
 'Fresh three-case literal controls return exactly the accepted representatives and order for the identical seed sequence and emit ten timing records. Four resource boundaries, exact driver and duplicate-owner rejection pass. Fresh preflight acquires23286 inputs without a target call.',
 'Release the one exact request4464e482fcf7ddd4ac51035ce75d226265418564831afbdb7ec1c8509303803a for cell8/2,30seconds,1024MiB GAP workspace,32MiB sampled output,4GiB launch reserve and2GiB sampled floor. GAP workspace is not a whole-process RSS cap. Owner kills and waits for its direct GAP child and launches no successor.',
 'This diagnostic earns no numerical result credit even if it finishes. CPU counters omit unmeasured work and include instrumentation overhead; they can guide the next method investigation but are not a claimed speedup or mathematical resource bound. Retain the failed direct-key300-second run unchanged and Ru15/16.'
]))
