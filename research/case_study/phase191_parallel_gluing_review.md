# Independent review of parallel gluing and simultaneous matching

## Decision and scope

**Accept the corrected partial gluing contract in the frozen phase187 manuscript.**
The eight-point construction is a counterexample to the sufficiency direction of
Buekenhout–Huybrechts–Pasini, Lemma 3.4, as printed on p. 365. It satisfies the
source's actual assumptions, including property (O). The replacement criterion,
the stated connection with typed coset Helly, the diagonal-orbit description,
the automorphism fiber product and the uniqueness criterion are correct with
the manuscript's type-preservation and parallelism qualifications.

This is **zero whole-source principal credit and zero open-conjecture credit**.
The source's parallel expansion and its many applications are not derived here.
The correction's historical priority has not been investigated. Acceptance does
not assert that no earlier correction exists.

The author freeze is `phase187_manifest.json`, SHA256
`5506e0c10b748e74c3554fbcfb29e0c7d1ea6f5bd103204cfd8ffd0c1426189d`.
Its main proof is `phase187_parallel_gluing.md`, SHA256
`21cae2585eeef2c516a881e5262f8272c3affac7a17ba3f96c63e299a5cc1cd0`.
All 23 author bindings were checked before and after the fresh replay. Two
screening notes also occur in that manifest; this review does not convert their
prospective source contracts into accepted results.

## Primary source and hypotheses

The primary source is F. Buekenhout, C. Huybrechts and A. Pasini, *Parallelism in
diagram geometry*, Bulletin of the Belgian Mathematical Society–Simon Stevin
1(3) (1994), 355–397, 43 physical pages. The bound file is
`sources/phase187_parallelism1994.pdf`, SHA256
`6ed25cefb93b1be3bf6c378ea0e5f718b9c9f3b130a4fe9feb25b95973983a06`.
The primary download is
[the journal PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BBMS/Bulletin/bul943/PASINI.PDF).

I read the source's complete definitions and gluing discussion, §§2–3, through
the end of §3.6. This is a review of that component, not a full reading or
replacement of all 43 pages. I visually checked printed pp. 356, 357, 358, 362,
364 and 365, including the formula and quantifiers in Lemma 3.4. The companion
text has control-character substitutions, so the page images govern these
checks. Exact image and source bindings are in `phase191_reading.json`.

The relevant assumptions are as follows.

| Source locator | Actual requirement | Binding in the example |
|---|---|---|
| §2.1, p. 356 | Every maximal flag has all types; distinct incident objects have different types | Incidence is point membership; every point and line extends to a point–line flag |
| §2.1.3, p. 357 | Isomorphisms preserve types throughout §3.4 | Point types remain separately labeled in the positive theorem |
| §2.1.4, p. 358 | Firmness is at least two chamber extensions of every proper flag | Base lines have two or four points; every base point has four lines |
| §2.2.1, p. 358 | A parallelism satisfies (P1), (P2), and existence of a parallel representative through every point | Each of the four classes is a partition; the rank-two form of (P2) follows from uniqueness |
| §§2.2.3, 2.5, pp. 359–361 | Direction geometry and induced action of parallel-preserving automorphisms | Four directions form a rank-one geometry; the induced image has order two |
| §3.1, p. 362 | A finite family of at least two geometries, with isomorphic direction geometries | Three copies of the same rank-two geometry |
| §3.4.2, p. 364 | “distinct elements of the same type have different 0-shadows” | The twelve line subsets are distinct; point 0-shadows are singleton sets |
| Lemma 3.4, p. 365 | The displayed product-membership condition for every two distinct indices | All six ordered instances hold |

Neither §3.1 nor §3.4 imposes linear-space incidence, equal block sizes,
existence of orders, thickness or flag-transitivity. The discussion of finite
geometries with orders in §2.4 is local to that discussion. In particular, it
cannot be imported as an additional hypothesis of Lemma 3.4. The example is
also firm and residually connected, although these extra properties are not
needed to refute the stated lemma.

## Review of the positive theory

Write \(H_j=\operatorname{im}\rho_j\), where \(\rho_j\) is the direction
action of the parallel-preserving automorphism group \(A_j\) of the factor.
For matchings \(\alpha_j,\beta_j:\Delta_j\to\Delta\), a family of local
maps glues precisely when the elements
\[
 \beta_j\rho_j(\varphi_j)\alpha_j^{-1}
\]
are independent of \(j\). Each element of \(H_j\) lifts by definition. Thus
existence of a glued isomorphism is exactly
\[
 \bigcap_j\beta_jH_j\alpha_j^{-1}\ne\varnothing.
\]
The coordinatewise map and its coordinatewise inverse preserve all source
incidences. There is no further condition on independently chosen lifts.

The source construction is indeed a geometry. Given a flag of tuples, project
it to a flag in each factor. Its directions form a flag in the common direction
geometry, which extends to a chamber there. In each factor choose a point
incident with its projected flag, using its already specified point if that
point type occurs in the glued flag. The geometry axiom supplies such a point
when it has not been specified. Take through that point the unique local
representative of every direction in the chosen direction chamber. The
parallelism axioms make these representatives a chamber containing the
projected flag. Matching these chambers gives a chamber of the glued geometry
containing the original flag. This is the retained construction, not a new
construction attributable to phase187.

Under (O), the manuscript correctly reconstructs any type-preserving
isomorphism from local maps. Equality of a coordinate gives equality of its
point shadow, hence equality of the image coordinate. Tuples in one direction
can be joined by changing one coordinate at a time. Because there are at least
two factors, consecutive tuples share a coordinate; their image directions
therefore agree. Local object maps are consequently well defined. Incidence
of a local pair can be checked after extending it to a point and filling the
other factors with parallel representatives through arbitrary points. The
same argument for the inverse proves an isomorphism, rather than only a
one-sided incidence map.

For clarity, the no-(O) statement also has a complete reconstruction argument.
Suppose an isomorphism preserves the glued parallelism, and two source tuples
have the same \(j\)-coordinate \(z\). They have the same direction. Their
images consequently have parallel \(j\)-coordinates. Choose a point incident
with \(z\); such a point exists because every flag extends to a chamber.
Both image coordinates are incident with the image of that point. Uniqueness
of a parallel representative through a point makes the two coordinates equal.
This proves independence of the tuple chosen to define the local image of
\(z\), without (O). The inverse and local incidence argument just given
then apply. This is precisely the mechanism of source Lemma 3.2. Its reuse
should remain attributed to that lemma.

Inverting the common-lift sets gives right cosets
\[
 P_j(\alpha_j\beta_j^{-1}),\qquad
 P_j=\alpha_jH_j\alpha_j^{-1}.
\]
For right cosets \(P_jr_j,P_kr_k\), nonempty intersection is equivalent to
\(r_jr_k^{-1}\in P_jP_k\). Substitution gives exactly the printed expression
\(\alpha_j\beta_j^{-1}\beta_k\alpha_k^{-1}\), with the stated right-to-left
composition convention. Corollary 2.2 therefore follows. Conversely, varying
\(\beta_j\) realizes every right coset of \(P_j\). The requirement that the
test work for every subfamily is needed to obtain typed Helly as defined in
the retained umbrella; the manuscript correctly includes it. I checked the
definition and anchored proof of U.Helly, §4 of `phase138_umbrella_v3.md`.
Subgroup intersection properties alone do not supply the needed common lift.

After fixing identifications of the direction geometries, the diagonal action
on \(\prod_jD/H_j\) gives the claimed orbit classification. The two-factor
case is the usual double-coset classification. The compatible tuples of local
automorphisms form the asserted fiber product. Its projection onto the
intersection of the direction images is surjective because every image
element lifts in every factor, independently. Its kernel is exactly the
product of the local kernels. A splitting has not been proved and is not
used. This review accepts the exact sequence and fiber product; it does not
certify an unrestricted semidirect-product interpretation of the notation in
source Theorem 3.6.

Proposition 3.1 is correct. Transitivity on the product of coset spaces forces
the common stabilizer of all but one base coordinate to move the remaining
coordinate arbitrarily. This is precisely the displayed factorization.
Conversely the factorization hypotheses persist after deleting a factor;
induction moves all but one coordinate to the base, and their common
stabilizer moves the last. Thus the source's uniqueness theorem survives the
failure of its preceding pairwise lemma. The native GAP program also checks
this equivalence for all 216 ordered triples of subgroups of \(S_3\); 34
triples satisfy it. That finite diagnostic supplements the proof and is not
the proof of the general proposition.

## Literal counterexample and independent reconstruction

On \(\mathbb Z/8\mathbb Z\), take the four classes
\[
\begin{aligned}
 P_0&=\{01,23,45,67\},& P_1&=\{12,34,56,70\},\\
 P_2&=\{0145,2367\},& P_3&=\{1256,0347\}.
\end{aligned}
\]
The two-point blocks form an eight-cycle, so any point permutation preserving
all blocks is in its dihedral group. Rotation by one and reflection
\(x\mapsto-x\) preserve all blocks and the four-class partition. Both induce
\(a=(0\ 1)(2\ 3)\) on the directions. Thus the full type-preserving base
group has order 16, its direction image is \(H=\{1,a\}\), and its kernel
has order eight. Shadow separation means no additional line permutation
fixing all points is possible.

Put \(s=(1\ 2)\), \(t=(1\ 3)\), \(b=(0\ 2)(1\ 3)\), and choose
\(\alpha=(1,s,t)\), \(\beta=(1,s,at)\). The lift sets are
\[
 \{1,a\},\qquad \{1,b\},\qquad \{a,b\}.
\]
Each pair intersects, but the total intersection is empty. The printed
product formula itself passes in all six ordered cases. Independent of the
replacement theorem, the source's literal tuple construction gives these
invariants:

| Invariant | Gluing by \(\alpha\) | Gluing by \(\beta\) |
|---|---:|---:|
| Tuple lines by common direction | 64, 16, 16, 16 | 32, 32, 32, 8 |
| Total tuple lines | 112 | 104 |
| Three point-type sizes | 8, 8, 8 | 8, 8, 8 |
| Total objects | 136 | 128 |
| Flags by size 0 through 4 | 1, 136, 1056, 2816, 2048 | 1, 128, 1056, 2816, 2048 |
| Connected residues of rank at least two | 1193 | 1185 |
| Panels with two completions | 1536 | 1536 |
| Panels with four completions | 1280 | 1280 |

Different total object counts preclude even a type-permuting isomorphism.
This establishes a counterexample to the printed lemma without using the
new common-lift theorem as the nonisomorphism certificate.

The reviewer program `phase191_independent_gluing.g` uses native GAP set
stabilizers for the full base group. It constructs all \(12^3\) block tuples
before imposing the source's matching equations, then builds the incidence
graph. It recursively enumerates all cliques as flags, checks extension of
every proper flag and absence of larger flags, checks firmness of every panel,
and explores every rank-at-least-two residue. This differs from the author's
direction-first tuple construction and enumeration by prescribed type sets.
The program reads neither the author program nor its saved output. GAP acts
on the right, so the translated third matching is `t*a`; the convention is
documented and tested explicitly.

The two calculations agree on all invariants in the table. The review replay
also rejects reversal of that matching product and deletion of point–line
incidences; the latter is detected by the residue-connectivity check. The
author's three additional negative controls reject a globally compatible
matching, duplicate line shadows and an altered formal coset. Thus the final
replay has five rejected controls, two originating in the independent review.

## Formal scope and replay

The full Lean file was read and freshly compiled with Lean 4.32.2. Its twelve
declarations prove the general common-image/coherent-family equivalence and
the stated finite Klein-group identities, subgroup closures, coset equality,
pairwise intersections, empty total intersection and regular-action
faithfulness. The observed axioms are `Classical.choice` and `propext`.
There is no `sorryAx` and no additional axiom. The file imports only `Std`.

It does **not** formalize incidence geometries, their reconstruction, the
twelve-line base automorphism group, the source's complete lemma, or the
general diagonal-orbit and uniqueness results. The correspondence between
the four-element calculation and the geometric example is a written and
computational bridge. Twelve declarations must not be described as twelve
fully formalized geometric theorems.

Fresh execution used Python 3.14.6, GAP 4.15.1 and the bound Lean 4.32.2
compiler. The exact author replay JSON was reproduced byte for byte. The
accepted independent report is `phase191_evidence/report.json`, SHA256
`e657e668ce970df71f1a171993a6378b087515f12b1cb98534662c7ab560c338`.
The first exploratory reviewer-driver run expected the incidence-deletion
mutation to be rejected at flag extension; it was actually rejected earlier
at residual connectivity. The final driver records that observed check. No
author or mathematical input changed as a result.

To reproduce the accepted run, choose a fresh output directory:

```sh
python3 phase191_verify.py \
  --output-dir /private/tmp/phase191_new_review \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean
```

## Attribution and accounting

The underlying construction, direction action and reconstruction of glued
isomorphisms are borrowed from Buekenhout–Huybrechts–Pasini. A simultaneous
choice already occurs in the first line of their Lemma 3.4 proof. The failure
is its replacement by separately satisfiable pairwise choices. Accordingly,
the common-lift formulation should not be advertised as an unrelated new
theory replacing the source's own geometric idea.

The project contribution is the explicit correction, its exact binding to
the existing U.Helly interface, the finite geometric counterexample and the
auditable proof and certificate organization. The orbit and uniqueness
arguments are retained mathematics with a direct proof; the fiber-product
statement avoids assuming a splitting. The source's two-factor result remains
valid under its stated shadow-separation scope. None of this establishes a
claim about the value or repetitiveness of an entire research group.

The four author core files contain 31,440 UTF-8 bytes: the written proof,
Python checker, portable author driver and Lean source. The independent GAP
program and review driver add 12,969 bytes. Charging the complete retained
umbrella adds 61,576 bytes, giving 105,985 bytes before this review's written
supplement. `phase191_costs.json` additionally charges this complete review
text in its conservative review-inclusive proof allocation, and separates
logs and audit records. The primary PDFs and software toolchains remain
explicit retained dependencies; they are not represented as newly compressed
mathematical text. The two screening notes are outside the gluing proof cost.

There is no matched complete-source numerator, so there is no manuscript,
page or byte compression ratio for this partial contract. No additional
whole-paper principal result, solved open conjecture or new fully formalized
geometry should be inferred from its admission.
