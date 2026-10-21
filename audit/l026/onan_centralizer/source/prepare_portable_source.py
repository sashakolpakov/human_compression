"""Prepare private portable Source declarations, never read/copy model/tree data."""
from pathlib import Path
import ast
import hashlib
import json
import os

S=Path('/Users/sasha/medusa/research/leemans')
N=S/'geometry/onan_regular_maps/permutation_model'
P=Path('/Users/sasha/medusa/math_compression')
D=S/'maintenance/reproducibility/l026_onan_centralizer'
AUTHOR='/root/unit_actual_review'
OPENED={}


def pin_source(p,expected=None):
    p=Path(p);a=p.lstat()
    assert p.is_file()and not p.is_symlink()and p.resolve(strict=True)==p
    assert a.st_nlink==1 and a.st_size<=2*2**20
    raw=p.read_bytes();assert a==p.lstat()
    q=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    if expected is not None:assert q['sha256']==expected
    OPENED[q['path']]=q
    return q,raw


def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(raw,bytes):raw=(json.dumps(raw,sort_keys=True,indent=2)+'\n').encode()
    assert len(raw)<=2*2**20
    with p.open('xb')as f:assert f.write(raw)==len(raw);f.flush();os.fsync(f.fileno())
    return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def public_pin(name,q):
    return dict(path=name,bytes=q['bytes'],sha256=q['sha256'])


def main():
    assert not D.exists()
    std,std_raw=pin_source(N/'check_standard_pair.py','acc28b910d81fe4c67b065f8da76cec5e62683d24a50729d70dab98b1546065c')
    pair,pair_raw=pin_source(N/'check_centralizer_pair_orbit.py','2dfcf3f91d69c2652109023ccd542ee7040cb2bcc1cfd5cdeace0632f70083b2')
    actual,actual_raw=pin_source(N/'centralizer_pair_orbit_distinct_actual_review.json',
        '764cb3c038dc6d9310f33d23ac3c1658b69708b99d4d48b2be4894e51d8b1502')
    actual_ex,actual_exraw=pin_source(N/'centralizer_pair_orbit_distinct_actual_execution.json',
        'aa22f6f589e5986954654c1ebb065525dfa99716e658a5717650a292cf99fab4')
    reviewed=json.loads(actual_raw);execution=json.loads(actual_exraw)
    assert execution['review']==actual
    standard_peer,_=pin_source(N/'standard_pair_distinct_source_review.json')
    standard_ex,_=pin_source(N/'standard_pair_distinct_source_execution.json')
    pair_peer,_=pin_source(N/'centralizer_pair_orbit_distinct_source_review.json')
    pair_ex,_=pin_source(N/'centralizer_pair_orbit_distinct_source_execution.json')
    old_dispatch,old_dispatch_raw=pin_source(P/'scripts/verify_snapshot.py',
        '544c695f611fe8f8186455fecefef4c9b96a3cda433e3829ac2bb519c969c05c')
    old_guide,old_guide_raw=pin_source(P/'docs/REPRODUCING.rst',
        'f6e2159d02a506b4c2bf0cca821f80b14f50b941ac3efa9678d2285c1939c6be')
    predecessor,predecessor_raw=pin_source(P/'scripts/g2_prefix8_certificates/registration.py',
        'e529c958248ca6504d813f9ef0787379917f5a689eeef4959a8ffba5292ca5b4')
    predecessor_policy,_=pin_source(P/'audit/f004/prefix8_certificates/publication_policy.json',
        '9393ac41fb6bf7b86b32543c1ef85625f217a128294ebaf811b8b7d93eb2ea5b')
    publication,publication_raw=pin_source(S/'maintenance/reproducibility/f004_prefix8_publication/root_publication_execution.json')
    baseline=json.loads(publication_raw)['commit']
    assert baseline=='4512492579d2809c32cadeda9250ae26ce661616'
    template,template_raw=pin_source(S/'maintenance/intake/onan_centralizer_portable_check_template.py')
    D.mkdir(parents=True)
    models=dict(
      c=dict(path='data/onan_centralizer/ONd2G1-p245520B0.g1',bytes=1893324,
             sha256='6f6c19692a8916ea66890461ce3fc12427b01baa23b0eaaf6a77da99cd2eb3a7'),
      d=dict(path='data/onan_centralizer/ONd2G1-p245520B0.g2',bytes=1827341,
             sha256='0c50acddb7cd7dd0e78b36bf0317e2d71074a715d3699108b18704d987867d22'))
    tree=dict(path='data/onan_centralizer/pairs.bin',bytes=806400,
              sha256='a3375939881a8d45eb849e3588a424ded561dd60af49220c1369ea79d7a6dd11')
    programs=dict(standard=public_pin('scripts/onan_centralizer/check_standard_pair.py',std),
                  pair=public_pin('scripts/onan_centralizer/check_centralizer_pair_orbit.py',pair))
    manifest=dict(schema='ONAN_CENTRALIZER_PORTABLE_INPUT_MANIFEST_V1',degree=245520,goal=161280,
      seed=[0,1],programs=programs,models=models,tree=tree,
      mathematical_scope=dict(named_model='ATLAS standard Aut(ON) action on245520 points',
        named_model_is_borrowed=True,inner_involution_class='2A',centralizer_upper_bound=161280,
        centralizer_upper_bound_is_borrowed=True,tree_nodes=161280,parent_edges=161279,
        matrix45D_homomorphism_proved=False,L026_complete=False,census_credit=0,
        conjecture_credit=0,whole_original_credit=0),
      primary_sources=[
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/permrep/ONd2G1-p245520B0',
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/subgroup/ONd2G1-max1W1',
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/subgroup/ONG1-max4W1',
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/ON/'],
      archival_private_audit_labels=[dict(role='distinct_private_pair_actual_review',bytes=actual['bytes'],sha256=actual['sha256']),
        dict(role='distinct_private_pair_actual_execution',bytes=actual_ex['bytes'],sha256=actual_ex['sha256'])],
      archival_labels_are_runtime_dependencies=False)
    manifest_ref=put(D/'proposed/data/onan_centralizer/manifest.json',manifest)
    assert template_raw.count(b'MANIFEST_SHA_PLACEHOLDER')==1
    wrapper_raw=template_raw.replace(b'MANIFEST_SHA_PLACEHOLDER',manifest_ref['sha256'].encode(),1)
    ast.parse(wrapper_raw)
    wrapper=put(D/'proposed/scripts/onan_centralizer/check.py',wrapper_raw)
    std_copy=put(D/'proposed/scripts/onan_centralizer/check_standard_pair.py',std_raw)
    pair_copy=put(D/'proposed/scripts/onan_centralizer/check_centralizer_pair_orbit.py',pair_raw)
    assert (std_copy['bytes'],std_copy['sha256'])==(std['bytes'],std['sha256'])
    assert (pair_copy['bytes'],pair_copy['sha256'])==(pair['bytes'],pair['sha256'])
    guide_append='''

Selected ON involution-centralizer certificate
---------------------------------------------

Read ``data/onan_centralizer/README.rst`` and its fixed manifest. The separate
entrypoint ``scripts/onan_centralizer/check.py`` can run nine standard-permutation
controls, the fixed standard word orders, thirteen pair-tree controls and direct
verification of the saved161280-pair tree. It uses ordinary isolated Python and
the standard library, with a fresh output directory outside the checkout.
Both full-degree model files and the entire806400-byte tree are explicit inputs.
The original check bodies remain byte-for-byte; the public entrypoint declares
only repository-relative I/O bindings and supplies no private fallback.

Named ATLAS model and the exact inner centralizer-order161280 classification are
borrowed premises. This certificate supplies no45D cover identification, complete
ON/Fi22 census, whole L026 recovery or conjecture credit. Existing102/105 original
registration and the earlier selected F004 cutoff3631/148 are unchanged. Root's
new additive registration must retain the45124925 predecessor in an explicit
frozen view and independently check the complete current delta; the old strict
registration is not claimed to pass an enlarged tree.
'''
    guide_append_ref=put(D/'guide_append.rst',guide_append.encode())
    readme='''A portable, conditional ON involution-centralizer certificate
=============================================================

This package checks an exact retained standard ATLAS Aut(ON) permutation model
and a saved full-degree ordered-pair tree. It does not identify an arbitrary
group from a few orders, identify the45-dimensional triple-cover matrices, or
complete L026, the ON/Fi22 census or a conjecture. All such credit is zero.

Named-model identification, simplicity and the complete maximal-subgroup list,
the unique inner involution class and its centralizer order161280 remain borrowed
primary/classification premises. The ATLAS links are listed in manifest.json.
The public parser authenticates the two whole cached files and constructs the
same right-action permutations; no GAP, NumPy, external package or private study
directory is required by this selected check.

From the repository root, use ordinary Python3.11 or newer without optimization.
Choose a fresh absolute output directory outside the checkout, with an existing
ordinary parent::

    python3 -E -B scripts/onan_centralizer/check.py \\
      --mode all --out /absolute/external/onan-centralizer-replay

Select one route with ``--mode standard-controls``, ``standard-pair``,
``pair-controls`` or ``check-centralizer``. The default ``all`` runs all four in
that order and keeps each original report plus a truthful portable receipt.
The old source files next to check.py are exact borrowed check bodies, not the
public entrypoints; their dormant historical private FILES constants are replaced
by the explicit repository-local facade before any original main is called.

The standard pair has w=(c*d^2)^2,a=w^-1*d^2*w,b=d. The checker verifies2/4/22
for c,d,cd, then2/4/11 for a,b,ab and19/31 for abb,abababbabb. Exact-order tests
use their complete fixed prime-divisor lists. Because a,b are in the named inner
ON and no retained proper maximal order contains both19 and31, they generate ON
conditional on those declared premises; this is not a presentation theorem.

Put z=ababb,t=z^10,x=[t,b]^14. The checker rechecks |z|20, |t|2 and that x,z
commute with t. It reconstructs161280 distinct ordered pairs of the full245520
point set from seed(0,1). Each of161279 nonroot records contains an earlier
parent and one of the two actual generator labels; the root has fixed sentinels.
The saved binary is exactly806400 bytes, little-endian uint32 parent/uint8 label.
No pair coordinates, word identities or matrix actions are accepted from a report.

For H=<x,z><=C_ON(t), that orbit proves |H|>=161280. The borrowed exact upper
bound |C_ON(t)|161280 therefore proves equality. This needs no faithful restricted
action or closure of the listed pairs; in particular, the720-point fixed set is
not used, since t lies in its kernel. A shorter orbit would not establish equality.

The public controls are the unchanged nine small permutation and thirteen S3 pair
controls. They are elementary fixtures, not fresh named-model identification.
The actual public replay, Source review, absence-of-private-access demonstration,
guarded memory/time fit, exact export hashes and additive registration are Root
publication obligations. Source preparation itself executed none of these modes
and neither opened nor copied the two model files or the tree.

The complete package declares those three payloads (4527065 bytes) rather than
depending on an installed runtime, private cache, whole workspace or opaque giant
operational history. The two original Source bodies and public facade are pinned.
The wrapper keeps both original mains and every scientific function unchanged;
only S/FILES, the pair helper provider, and explicit argv/output routing change.
The portable receipt names the facade as execution_program and the original
bodies as semantic sources; no old private CLI PASS is retargeted to this adapter.

Each selected invocation, including all four in ``all``, has an unchanged combined
30second/128MiB self budget. Root actual publication uses its256MiB/150second
supervisor with4GiB/10GiB admission and3GiB/8GiB runtime floors. Source inspection
claims no runtime fit. Output is external and bounded, with a64KiB portable receipt.
The snapshot registration check is metadata integrity, distinct from these
explicit mathematical/control replays; preserve the existing predecessor history.
'''
    readme_ref=put(D/'proposed/data/onan_centralizer/README.rst',readme.encode())
    payload_sources=[dict(source=dict(path=str(S/'corpus161_N006_sporadic/private_data'/Path(q['path']).name),
                      bytes=q['bytes'],sha256=q['sha256']),destination=q)for q in models.values()]
    payload_sources.append(dict(source=dict(path=str(N/'centralizer_pair_orbit_checks/seed_0_1/produce/output/pairs.bin'),
                         bytes=tree['bytes'],sha256=tree['sha256']),destination=tree))
    source_exports=[dict(source=q,destination=public_pin(name,q))for name,q in[
      ('scripts/onan_centralizer/check.py',wrapper),
      ('scripts/onan_centralizer/check_standard_pair.py',std_copy),
      ('scripts/onan_centralizer/check_centralizer_pair_orbit.py',pair_copy),
      ('data/onan_centralizer/manifest.json',manifest_ref),
      ('data/onan_centralizer/README.rst',readme_ref)]]
    recipe=put(D/'copy_recipe.json',dict(schema='ONAN_CENTRALIZER_SOURCE_ONLY_COPY_PROPOSAL_V1',
      payloads_declared_not_read_hashed_or_copied=payload_sources,source_exports=source_exports,
      declared_new_file_count=8,declared_payload_bytes=4527065,
      declared_new_bytes=4527065+sum(q['destination']['bytes']for q in source_exports),
      public_files_materialized=False,payloads_opened=False,git_calls=0,
      runtime_and_registration_acquired=False))
    inverse=put(D/'source_inverse.json',dict(schema='ONAN_CENTRALIZER_IO_FACADE_SOURCE_INVERSE_V1',
      whole_original_standard_Source_utf8=std_raw.decode(),whole_original_pair_Source_utf8=pair_raw.decode(),
      originals=[std,pair],copies=[std_copy,pair_copy],scientific_text_edits=[],
      copied_Source_whole_bytes_identical=True,
      explicit_io_bindings=['standard.S=ROOT','standard.FILES=relative manifest c,d paths and fixed SHA',
                            'pair.helper=public_helper returning same exact standard module',
                            'sys.argv=exact explicit original main CLI; restored in finally'],
      all_other_function_bodies_and_globals_unchanged=True,
      truthful_actual_execution_program=public_pin('scripts/onan_centralizer/check.py',wrapper),
      no_private_fallback=True,old_private_CLI_PASS_retargeted=False))
    registration=put(D/'registration_plan.json',dict(
      schema='ONAN_CENTRALIZER_EXPLICIT_ADDITIVE_REGISTRATION_PLAN_V1',baseline=baseline,
      baseline_authority=publication,old_dispatch=old_dispatch,old_guide=old_guide,
      predecessor_registration=predecessor,predecessor_policy=predecessor_policy,
      proposed_additions=[q['destination']for q in payload_sources+source_exports],
      guide_append=guide_append_ref,
      required_later_steps=[
        'Independently review this portable Source proposal before materialization or execution.',
        'Root materializes exactly8 ordinary files and fresh-hashes all3 original/exported payloads; Source copies and manifest are exact.',
        'Root executes all4 selected routes with a private-denial check, actual guard captures and closed known process scope.',
        'Author/review a narrow next registration layer: evaluate exact old g2 registration only in an explicit frozen45124925 Git view, retaining every original function and historical catalogue premise.',
        'Separately verify current index/blob/modes/delta against45124925, allowing only the finite8 package files plus genuinely new small Source/replay/registration proof documents and one dispatcher-main edit/guide append.',
        'Freeze actual complete publication roster only after real Source/replay proofs exist; no future proof/gate hash is declared here.',
        'Run exact registration before/after staging, retain current102/105/F004-F009-L026 pending and historicalF0043631/148, then commit/push only after Root review.'
      ],
      predecessor_CLI_passed_enlarged_tree=False,registration_source_authored=False,
      current_delta_checked=False,original_partition_changed=False,whole_original_credit=0))
    argument_text='''Private Source proposal for the portable ON centralizer check
=============================================================

Author Unit. This preparation reads Source and ordinary audit/publication metadata
only. It neither reads/hashes/copies a model/tree payload nor imports/compiles/runs
either target or its controls. It writes only this private Source proposal.

The five proposed Source/document files and three declared payloads form eight
new public files. Existing code is copied exactly: standardacc28 and pair2dfcf.
No scientific text edit occurs. The new check.py facade authenticates an exact
relative manifest and both complete Source bodies, loads them nonmain, then maps
standard.S/FILES to public paths and pair.helper to that very same standard module.
Both complete mains are invoked through explicit argv, restored in finally.
No other scientific function body/global is changed and no private resolver runs.
The wrapper receipt names the actual facade separately from both borrowed bodies.

The manifest contains the two acquired245520-point files and complete806400-byte
tree pin, not future results. Archive audit SHA labels are documentary; they are
not unresolved private runtime dependencies. Root must rehash/materialize/replay
the exact8 files and establish actual fit/private absence independently.

The existing public dispatcher is a strict g2 registration checker. It would
correctly reject undeclared additions. registration_plan.json therefore leaves
it and all existing papers/proofs/catalogue/counters untouched and declares an
explicit subsequent frozen45124925 predecessor plus separate strict whole current
delta layer. No old CLI pass on an enlarged tree, publication registration or Git
operation is claimed. The later current proof roster is dynamic, never guessed.

Expected Source review status: PASS_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE.
Expected canonical Source execution status:
COMPLETED_GENUINE_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE_REVIEW.
Peer/ex must bind current check.py, manifest, Sourcepacket, inverse, argument,
checks, real reviewer tool and a literal Source roster including mandatory late
preparation. Source author Unit; reviewer must differ. Controls/runtime/publication
remain unacquired by this proposal; named group/classification are borrowed.
'''
    argument=put(D/'PORTABLE.rst',argument_text.encode())
    checks=put(D/'source_checks.json',dict(schema='ONAN_CENTRALIZER_PORTABLE_SOURCE_ASSEMBLY_V1',
      scientific_Source_edits=0,whole_Source_copies_equal=True,source_wrapper_AST_parsed=True,
      payload_count=3,payload_bytes=4527065,payloads_read_or_hashed_or_copied=0,
      proposed_public_file_count=8,private_fallback=False,target_calls=0,target_imports=0,
      target_compiles=0,control_calls=0,public_writes=0,git_calls=0,
      registration_implementation_and_actuals_owed=True,whole_original_credit=0))
    own,_=pin_source(Path(__file__).resolve())
    required=list(OPENED.values())+[wrapper,std_copy,pair_copy,manifest_ref,readme_ref,
        guide_append_ref,recipe,inverse,registration,argument,checks]
    by={q['path']:q for q in required};required=[by[k]for k in sorted(by)]
    packet=put(D/'source_packet.json',dict(schema='ONAN_CENTRALIZER_PORTABLE_SOURCE_PACKET_V1',
      source_author=AUTHOR,program=wrapper,programs=dict(adapter=wrapper,standard=std_copy,pair=pair_copy),
      manifest=manifest_ref,inverse=inverse,argument=argument,checks=checks,copy_recipe=recipe,
      registration_plan=registration,guide_append=guide_append_ref,Source_assembler=own,
      required_source_inputs=required,
      expected_source_status='PASS_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE',
      expected_source_execution_status='COMPLETED_GENUINE_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE_REVIEW',
      expected_peer_basename='distinct_source_review.json',
      expected_execution_basename='distinct_source_execution.json',
      public_files_materialized=False,declared_payloads_not_read_hashed_or_copied=3,
      represented_calls=0,public_writes=0,git_calls=0,whole_original_credit=0))
    print(json.dumps(dict(status='FROZEN_SOURCE_ONLY_PORTABLE_ONAN_CENTRALIZER_PROPOSAL',
      program=wrapper,manifest=manifest_ref,source_packet=packet,inverse=inverse,argument=argument,
      checks=checks,copy_recipe=recipe,registration_plan=registration,
      Source_input_count=len(required),Source_input_bytes=sum(q['bytes']for q in required),
      declared_public_file_count=8,declared_public_bytes=4527065+sum(q['destination']['bytes']for q in source_exports),
      payload_bytes_read_hashed_copied=0,target_calls=0,public_writes=0,git_calls=0)))


if __name__=='__main__':main()
