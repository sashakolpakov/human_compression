# Parallel gluing and simultaneous matching

The [written application](research/case_study/phase187_parallel_gluing.md)
and its [independent review](research/case_study/phase191_parallel_gluing_review.md)
recover the matching, reconstruction, orbit and uniqueness arguments for
parallel gluings. The application uses the existing coset-intersection
interface in [U](UMBRELLA.md). It also corrects a pairwise sufficiency
claim in the 1994 source. This is a partial source contract, outside the
fixed 161-work registry.

## The common argument

Each factor geometry has a group of parallel-preserving automorphisms
and an induced group H_j on its directions. Matching maps α_j identify
those direction geometries with a common one. For a second set of
matchings β_j, the exact isomorphism criterion is

```text
intersection over j of β_j H_j α_j⁻¹ is nonempty.
```

An element of this intersection supplies a single direction action
that lifts in every factor. Choosing those lifts gives the isomorphism
coordinate by coordinate. Conversely, an isomorphism recovers compatible
local maps when distinct objects of a type have distinct point shadows.
Without that shadow assumption the criterion classifies isomorphisms
preserving the specified parallelism. Types remain individually fixed.

This common argument yields the diagonal-orbit classification, the
two-factor double-coset description, the exact automorphism fiber product
and the uniqueness criterion. Pairwise intersection suffices when the
conjugated direction groups satisfy U's typed coset Helly property.
The application proves that binding explicitly; an arbitrary family of
subgroups need not satisfy it.

## Source, correction and attribution

The source is F. Buekenhout, C. Huybrechts and A. Pasini,
*Parallelism in diagram geometry*, **1994**, pp. 355–397
([primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BBMS/Bulletin/bul943/PASINI.PDF)).
The construction, reconstruction and orbit method remain attributed to
that paper. Its own proof already expresses simultaneous lifting before
replacing it with the insufficient pairwise test. Our contribution here
is the explicit correction, its application of U.Helly, the counterexample
and the checked proof organization. Historical priority of the correction
has not been established.

Three copies of an eight-point geometry provide a literal counterexample
to Lemma 3.4 on p. 365. Their direction-action constraints become
`{1,a}`, `{1,b}`, `{a,b}` in a Klein four-group. Every pair intersects;
all three do not. All six ordered instances of the printed test hold,
yet the resulting gluings contain **136 and 128 objects**, respectively.
Both are firm and residually connected. Their different sizes establish
nonisomorphism even if type permutations are permitted.

The [eleven-row source ledger](research/case_study/phase191_source_contract.json)
separates borrowed results, the corrected statement and the use of U.
The parallel-expansion theory and examples in the rest of the source
remain outside this admission. This is not a solved open conjecture or
a replacement of the whole paper.

## Verification and cost

Two independent implementations reconstruct the example: a Python
permutation enumeration and a native GAP set-stabilizer calculation.
They agree on the full base group, direction action, objects, flags,
panels and every residue of rank at least two. The fresh public replay
also rejects five deliberate changes to the hypotheses or certificates.

[SimultaneousMatching.lean](research/case_study/formal/SimultaneousMatching.lean)
proves twelve declarations concerning simultaneous lifting and the
finite coset obstruction. Its [scope](research/case_study/formal/SimultaneousMatching.scope.md)
excludes the full geometric reconstruction. It imports only `Std`;
the printed reports use `Classical.choice` and `propext`, without a
native-evaluation axiom.

Run the public check with Python, GAP 4.15.1 and Lean 4.32.2, using a
fresh output directory:

```sh
python3 -B -O research/case_study/phase195_public_check.py \
  --output-dir /tmp/NEW-gluing-check --gap /path/to/gap --lean /path/to/lean
```

Primary PDFs are not required for this execution. The frozen reviewer
driver is also retained as provenance; its original private-checkpoint
inputs are distinguished from the public adapter.

The written application, author checker, author driver and Lean source
cost **31,440 UTF-8 bytes**. Full U, the independent GAP program, public
adapter and complete written review supplement bring the conservative
package cost to **123,587 bytes**. Logs and audit records are separate.
There is no matched whole-source numerator and therefore no compression
ratio for this partial contract. The existing A–D editions and their
measurements are unchanged. See the [root admission](research/case_study/phase195_root_admission.md).
