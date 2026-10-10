# Independent review: Equal-label polytopes and quadratic symmetries

10 October 2026. Root review of the two frozen phase124 packages. This is
a question-solving result, separate from replacement of known principal
results. The complete all-label conjecture remains unresolved.

## Admitted mathematical scope

For every rank d >= 3, the written arguments construct finite regular
polytopes satisfying the exact relations of Li–Zhang, Conjecture 3.7, at
labels n, 2n and 4n whenever

    n = 3; n = 2^e + 1 (e >= 2); or n = 2^e - 1 (e >= 3).

Label 4 is also admitted. The universally presented groups themselves
are identified at labels 3 and 4: respectively S_(d+1) and
UT_(d+1)(F_2). The latter assertion retains the published presentation
theorem of Biss–Dasgupta. No universal-group assertion is admitted at
the other labels. In particular labels 8, 11 and 13 are not covered.
There is no complete Lean certificate or historical-priority clearance.

The source is Mingchao Li and Wei-Juan Zhang, *Regular 3-polytopes of
type {n,n}*, [arXiv:2505.09505v1](https://arxiv.org/html/2505.09505v1),
Conjecture 3.7, PDF page 11. Root checked the exact statement and the
finite-group convention in Definition 2.2 against the private primary
extraction and primary HTML. Its literal demand is existence of a
quotient with exact type and the listed relations. Identification of
the entire universal presentation is a stronger assertion. These two
contracts must not be conflated. The arXiv record still displays only
v1; bounded title, author and conjecture searches did not establish
whether these specializations have appeared elsewhere.

## Complete proof reading

Root read all four mathematical notes and all three Python checkers.
The following were checked algebraically, beyond their finite examples.

1. **Binary upper triangular matrices.** Consecutive elementary
   transvections generate every allowed upper triangular entry. A
   standard parabolic consists exactly of the blocks determined by its
   retained path edges. Entrywise intersection therefore proves full IP,
   including disconnected supports. Adjacent products have exact order
   four. For a consecutive triple, the two adjacent squares are matrix
   units at (i,i+2) and (i+1,i+3), whose two products vanish. This proves
   the k=2 relation; outer commutation proves k=1,3.

2. **Label three.** The corresponding interval subgroups of S_(d+1)
   have the required intersections. Both extra words follow from outer
   commutation and adjacent order three. Identifying the entire group
   additionally retains the classical type-A Coxeter presentation.

3. **Whole-ambient quadratic identity.** For Q(z)=0 and u,v perpendicular
   to z, direct expansion of the displayed T_u formula gives
   T_u T_v = T_(u+v). The coefficient of z contains the necessary
   Q(u)B(x,z) correction. For Q(u)=1, the product of the symmetries in
   u and u+z is T_u. Conjugation by an isometry fixing z sends T_u to
   T_(g(u)). These are identities on the whole ambient space, even when
   the three-dimensional support is degenerate. On a constant-coefficient
   triple, z=e+h is singular and perpendicular to its span. The generated
   translation subgroup has exponent two and is normalized by A=ab;
   C=bc=A^(-1)(ac). Hence C^k A^k belongs to that subgroup for every
   integer k, proving all the source power relations.

4. **Retained symmetry construction.** Root read the relevant primary
   sections of Brooksbank–Ferrara–Leemans,
   [arXiv:1709.02219v2](https://arxiv.org/abs/1709.02219v2): Proposition
   3.3, Remark 3.5, Lemma 5.3, Remark 5.4, Proposition 5.5 and the proof
   of Theorem 1.4. They supply the stated intersection property with
   full adjacent orders q+1 for q>=4 and q-1 for q>=8. Constant
   coefficients are allowed. No theorem for arbitrary divisors of
   q+/-1 is imported. No assertion that every odd-dimensional example
   generates the full isometry group is needed. Choosing an eigenvalue
   of exact order q+/-1 gives the required coefficient and exact order.

5. **Parity fiber.** On a connected interval the common Goursat
   quotient is a 2-group, whereas neighboring involutions have products
   of odd order. All those images coincide. The two parity characters
   force the common quotient to be exactly C2. Disconnected supports
   split into commuting direct factors by the original IP. For two
   supports, their component-overlap bipartite graph is a forest:
   an interval of smallest right endpoint has at most one neighbor.
   Zero parity sums at vertices force zero edge values by leaf deletion.
   This proves every parabolic intersection in the mix and the exact
   order formula. It does not assume that arbitrary mixes preserve IP.

6. **Actual parity character.** The quadratic factor is embedded in an
   even-dimensional nonsingular ambient space before taking the required
   parabolic. Its polar determinant is alpha^D, so the Dickson character
   applies and sends each symmetry to one. Root independently read
   Nebe–Parker, *Equivariant quadratic forms in characteristic 2*,
   [published HTML](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.12748),
   sections 2.1 and 3, including the paragraph before Lemma 3.1.
   The nonsingular polarization and rank(g-I) modulo two homomorphism
   match precisely. Taylor's underlying proof remains a retained
   citation, not a proof reproduced here. The unitriangular factor's
   first-superdiagonal sum is its parity character. These give exact
   adjacent orders 2n and 4n and preserve every extra power word.

7. **Universal label-four adapter.** With involutions a,b and
   u=[a,b]=(ab)^2, both nested commutators in the retained presentation
   equal u^(-2). Thus they are equivalent to (ab)^4=1. Two adjacent
   such commutators are involutions, so their commutation is equivalent
   to the k=2 source word. The k=1,3 words are redundant. This proves
   equality of defining normal closures in both directions, not merely
   a map onto a finite matrix image. Root checked Theorem 1, the
   commutator convention and the even-parameter proof passages in the
   [author-hosted Biss–Dasgupta PDF](https://sites.math.duke.edu/~dasgupta/papers/Unipotent.pdf).
   The paper credits the binary presentation to Biss (1998). Access was
   through extracted PDF text: local download failed and the screenshot
   tools supplied no viewable raster. No visual typography inspection
   or local PDF hash is claimed. The retained formulas agree with the
   extracted theorem and the proof passages; rendering that source
   remains an explicit access limitation.

8. **Deletion obstruction.** Killing a while fixing b,c maps the k=2
   word to (bc)^4. Exact order n>=3 then forces n=4. This excludes the
   proposed deletion strategy at all remaining labels, including even
   labels, without asserting nonexistence of their polytopes.

## Fresh computational evidence

Root executed all three original scripts under optimized Python, with
new output paths. Every run passed. Removing only the timing field gives
the original frozen reports exactly.

| Check | Exact finite coverage |
|---|---|
| Symmetric and binary triangular models | Six models at ranks 3–5; all 1,400 unordered support pairs; exact subgroup profiles and source words |
| Quadratic models | 42 markings over F4,F8,F16,F32 at ranks 3–8; 2,310 power words; 8,448 translation-parameter pairs and 144 conjugations |
| Quadratic IP | Three complete subgroup enumerations; 208 support pairs; orders 8,160, 896 and 1,152 |
| Parity mixes | Six complete models; 416 support pairs in each of the two factors and the mix; 76 power words; exact component fibers |

The rank-three label-nine quadratic image has order 1,152, whereas the
source's group has order 4,608. This is concrete evidence that matrix
images must not silently be treated as faithful universal presentations.
The saved author controls remain separately identified; this review does
not relabel their executions as fresh root controls. The new public
verification wrapper checks frozen bytes, compares the three fresh root
reports, and optionally reruns the bounded computations.

## Attribution and claim boundary

The elementary matrix, quadratic and parity-fiber arguments are the
repository's written derivations. This statement describes their role in
this proof, not their historical novelty. The BFL intersection theorem,
Dickson invariant, Biss–Dasgupta presentation, classical type-A
presentation, finite-field facts and the group/polytope correspondence
remain attributed inputs. Goursat's argument and general marked mixing
are established methods.

This review admits a partial question result, not an additional source
whose principal published results have been compressed. No compression
ratio, infinite factor, complete conjecture solution or end-to-end
formal certification is assigned. The frozen earlier notes contain
older, narrower scope statements; the additive universal-four and
parity notes supersede those limitations only in the precise ranges
listed at the start of this review.
