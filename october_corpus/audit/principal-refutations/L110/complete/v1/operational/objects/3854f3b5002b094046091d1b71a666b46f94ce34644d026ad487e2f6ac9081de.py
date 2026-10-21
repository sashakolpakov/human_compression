from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');F=S/'computation/f009';Y=S/'geometry/suzuki_incidence'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('computation/f009/sharing_session_bootstrap01')
for row in json.loads((F/'sharing_session_bootstrap01/plan01.json').read_text())['inputs']:c.binding(row)
r=json.loads(Path('/private/tmp/f009_initial_sharing_bootstrap_root_controls01.json').read_text());assert r['status']=='PASS_INITIAL_SHARING_BOOTSTRAP_REQUEST' and len(r['checks'])==12
c.add('/private/tmp/f009_initial_sharing_bootstrap_root_controls01.json');c.add(__file__)
c.finish('computation/f009/sharing_session_bootstrap_root_review','ACCEPTED_F009_INITIAL_SHARING_READ_ONLY_BOOTSTRAP_REQUEST',dict(author='finite_recoveries',reviewer='root',authorized_probes=1,automatic_successor=False,review=[
 'Read the exact proposed full-size bootstrap, owner, unchanged native resource guard and all owner deltas. The strict1324 dictionary acceptance and separately accepted initial-sharing caller are fixed inputs. The actual-loader/import preflights precede full parsing.',
 'The executable is copied byte for byte to a fresh temporary path outside the scientific tree. It independently acquires both210004-key dictionaries, compares their complete states/read sets, applies the initial-only immutable-content operation and ordinary garbage collection, emits canonical bytes and compares the entire459076751-byte journal through both private readers.',
 'Fresh twelve request/resource controls passed with no dictionary parse or scientific target. One2400second read-only probe retains4GiB sampledRSS,4GiB free-space floor,512MiB totaloutput and0.5second owned-process-family sampling. Limits are operational samples with possible overshoot, not mathematical resource bounds.',
 'The probe invokes no scientific writer and may not authorize its own successor. Own-PID before/after observations can measure initial storage savings, but do not bound a future combined writer peak. No mathematical coverage, original completion, conjecture, Lean or compression credit.'
 ]))
c=m.Closure();c.packet('geometry/suzuki_incidence/prime_residue_extensions');O=Y/'prime_residue_extensions_root01'
for p in O.iterdir():
    if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/prime_residue_extensions_root_review','ACCEPTED_L110_PRIME_SUBFIELD_RESIDUE_NONEXTENSION',dict(author='j3_recovery',reviewer='root',review=[
 'Read all four proof pages and viewed their native renderings. Checked the explicit inherited subgroup-classification, odd-dihedral maximality, strict-intersection, affine uniqueness and prime-degree obstruction inputs. Fresh root native compilation preserved all four page texts; all613 exact input bindings were acquired.',
 'The maximal subfield has exponentd prime and ambient exponentdr. Multiplicative order modulo2^d−1 and torus coprimality force every containing proper simple subfield to have degreed; embedded uniqueness then identifies it. Remaining full-split-dihedral and affine overgroups are confined respectively to the ambient split normalizer and unique point stabilizer.',
 'Maximal subgroups ofD_(2pℓ),including the excludedℓ=p case, give the exact induced intersections. The first residue cannot combine an affine overgroup with an odd dihedral subgroup inside a point stabilizer. The second aligns prime subfields through their common reflection and forces intersectionSz(2)oforder20,contradicting the prescribed prime dihedral.',
 'For the third residue the other two parabolics must have the same prime split-torus parameter. Their common full torus, strict intersections and the point-stabilizer exclusion force their common subgroup to be the affineA_t. Embedded affine uniqueness proves equality of the two subfields; equal abstract sizes alone are never used.',
 'This proves the three specified nonextension assertions for rank-four families with a maximal prime-split-torus Suzuki parabolic, including the source remaining second-case candidate. It does not reinstate any composite exhaustive classification or itself complete L110. No new search, conjecture, Lean or compression credit.'
 ]))
