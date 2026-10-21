from pathlib import Path
import hashlib, importlib.util, json, sys
sys.dont_write_bytecode = True
S = Path('/Users/sasha/medusa/research/leemans')
spec = importlib.util.spec_from_file_location('flat', S/'reboot_20261013/component_adoption_flat_v2.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def accept(relative, expected, result, status, name, review, extras=()):
    p = S/relative
    assert hashlib.sha256((p/'manifest.json').read_bytes()).hexdigest() == expected
    c = m.Closure(); c.packet(relative); c.add(result); c.add(__file__)
    for folder in extras:
        for f in Path(folder).rglob('*'):
            if f.is_file(): c.add(f)
    c.finish(name, status, dict(status=status, author='project component authors', reviewer='root', review=review))

r = json.loads(Path('/private/tmp/l115_principal_root02.json').read_text())
assert r['claims'] == 70 and r['controls']['damage_checks'] == 12 and r['acquired_dependencies'] == 34262
assert json.loads(Path('/private/tmp/l115_native_root02/report.json').read_text())['status'] == 'PASS'
accept('geometry/suzuki_subgroups/principal_v2', '8c15732e2041adc45ba02f88119c6823673e33272ae2c5526ab3d7dbe83cacf9',
 '/private/tmp/l115_principal_root02.json', 'ACCEPTED_L115_COMPLETE_CORRECTED_SOURCE_TREATMENT',
 'geometry/suzuki_subgroups/principal_root_review', [
 'Read the complete five-page classification assembly, two-page arithmetic note and all70 source-claim rows. Viewed all seven native pages. A fresh two-pass TeX build of both papers reproduced every drawing stream and embedded font program. Reused the six exact previously reviewed complete proof notes; no finite census was repeated.',
 'The rank-two reduction follows from maximality, generation and the common representative of an incident pair. The subfield-cover argument uses the normalizer condition in the finite two-group followed by the scalar-subspace interval; the remaining maximal-subgroup cases are exactly the accepted normalizer and subfield classifications. Classical Suzuki, Tits and Lueneburg results remain explicitly attributed premises.',
 'Compared formulas(3)-(5), the complete family domain and the local double-transitivity conclusion directly with the accepted subfield manuscript. No absolute/relative-degree coprimality has been added. The complete60-row integer certificate,29-diagram graph comparison and all positive primitivity marks are acquired through their distinct accepted component reviews.',
 'The original Table6 divisor condition, omitted central covers, numerical corrections,25/26 residue and multiplicity interchange,27/29 quasiprimitivity errors and final exponent glyph are all explicit. The review required the Lemma6.1 rank-greater-than-one domain; source text confirms it and v2 corrects the overbroad v1 prose without changing predicates or mathematical data.',
 'Fresh whole-source check passed34262 input bindings and12 damaged-input controls. This accepts completion of the fixed mathematical source after its existing principal refutation, including a complete corrected specified-group classification. It does not claim unmarked graph-isomorphism classification, new conjecture credit, Lean verification, compression measurement or public registration.'
 ], ['/private/tmp/l115_native_root02'])

r = json.loads(Path('/private/tmp/l110_source_root02/report.json').read_text())
assert r['status'] == 'PASS_L110_COMPLETE_SOURCE_ASSEMBLY' and r['source_claims'] == 63 and r['volume_pages'] == 105
accept('geometry/suzuki_incidence/higher_source_synthesis02', '3f39e0437a328a4b1363fc06a76694515db18561e8f298c295c44a3511b26ee8',
 '/private/tmp/l110_source_root02/report.json', 'ACCEPTED_L110_COMPLETE_SOURCE_TREATMENT_WITH_CORRECTIONS',
 'geometry/suzuki_incidence/higher_source_root_review', [
 'Read the revised five-page overview and every row of the63-claim ledger, and directly viewed the volume cover and all five new overview pages. Fresh replay rebuilt the overview, both necessity papers and the complete105-page volume; all48 proof imports remain exact, all imported drawing streams and font programs agree, and the source and proof dependencies remain unchanged.',
 'The earlier mathematical hold remains retained. Canonical existence was insufficient for the five conditional extension assertions. The separately reviewed split necessity paper now treats R7/R9 and its repeated branch; the torus necessity paper treats R10/R11/R13, including the formerly missing derivation of the input field degrees. The root-authored torus paper received j3_recovery distinct review before this assembly; this is not a new independent discovery claim.',
 'The original page5 convention explicitly excludes Sz(2) from Suzuki type, so the simple bottom used in R10/R11/R13 is a source premise. Full torus complements, the nonsplit rotation-order restriction and the distinction between conditional necessities and the false global exhaustion are explicit. The source index and divisibility corrections are recorded rather than silently assumed.',
 'The component proofs dispose of every construction, including impossible prescribed lattices, the universal scalar codimension obstruction, and the repeated-prime pure-field boundary. The separate scalar geometry supplement proves actual geometry, flag transitivity and local double transitivity; it does not retroactively change the older conservative proof. Quoted classical structure and the outside-intake dihedral classification remain attributed premises.',
 'The remaining future flag-transitivity problem for corrected5/7 and arbitrary relative positions is explicitly open; it is not an asserted theorem whose proof was omitted. No repaired global classification or quantitative almost-all assertion is claimed. Eight damaged-input/optimization checks passed. This accepts complete fixed-source disposition only, without new principal refutation, ordinary recovery, conjecture, Lean, compression or public registration credit.'
 ], ['/private/tmp/l110_source_root02'])

r = json.loads(Path('/private/tmp/l114_registration_root_check02.json').read_text())
assert r['status'] == 'PASS_L114_REGISTRATION_CANDIDATE' and r['fully_treated'] == 96 and r['outstanding'] == 9
accept('geometry/suzuki_incidence/publication_work/registration_candidate02', '491373a090e31c63943f777384b0a78285643b09c03abcef84e559a7eb433e42',
 '/private/tmp/l114_registration_root_check02.json', 'ACCEPTED_L114_SOURCE_COMPLETION_REGISTRATION_CANDIDATE',
 'geometry/suzuki_incidence/publication_registration_root_review', [
 'Read the exact candidate checker, changed narratives and machine-count delta. Root replay passed2661 operational routes,263 documentary premise boundaries,four count damage controls and three boundary damage controls. Only L114 changes completion status; the92 ordinary recoveries,9 principal refutations,101 principal dispositions and all measurements remain unchanged.',
 'Candidate02 preserves the accepted scientific transport and the candidate01 native protocol byte-for-byte. Eight historical Markdown objects have opaque bin names with identical bytes; nine route occurrences and eight reference-bearing metadata files are the only propagated change. There are no new public Markdown paths and no original source document bytes in the publication payload.',
 'The proposed registration is95 to96 fully treated mathematical originals, with nine remaining. The L114 narrative accurately distinguishes complete disposition of61 source claims from an unproved corrected global classification. Its68-page assembled reading volume is not advertised as a compression factor. This approves the exact candidate for installation after separate installer verification; it does not claim the public worktree was already changed or pushed.'
 ])
