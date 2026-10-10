# Odd kernels and cyclotomic polyhedra

The [complete eight-page paper](research/case_study/phase236_odd_kernel_manuscript.pdf)
([readable source](research/case_study/phase236_odd_kernel_manuscript.md))
recovers the three principal theorems of Hou, Feng, Leemans and Qu,
*String C-groups of order $4p^m$*, in the specified arXiv edition.
The [independent review](research/case_study/phase248_review.md) accepts
the complete principal contract, including the necessary correction to
one displayed marking.

| Source result | What the replacement proves | Earlier inputs and limits |
|---|---|---|
| Theorem 1.1 | A normal Sylow $p$-subgroup with two generators, the endpoint Klein four complement, and the stated divisibility of both type parameters | Odd prime $p$, $m\ge2$, nondegenerate rank-three string C-group; elementary Sylow theory retained |
| Theorem 1.2 | The odd kernel is abelian exactly when the marking is tight; the complete abelian family and its marked uniqueness, up to duality | The printed v1 marking is corrected. Cunningham–Pellicer’s tight classification is retained for the converse |
| Theorems 1.3 and 5.1 | For every odd prime $p$ and $m\ge3$, the nonabelian family of order $4p^m$ and type $\{p,2p\}$, with the exact source presentation and automorphisms | This is the stated construction, not a classification of every nonabelian kernel |

## The common ideas

An involution outside an odd normal subgroup determines an inverted orbit
under the Klein four complement. Two orbit elements generate the odd
kernel. In the abelian case, the four character projectors reduce this
to two cyclic components. The intersection property then determines the
allowable relative orders and recovers the complete tight family.

For the nonabelian construction, put

$$A=\mathbb Z[\zeta_p]/(\zeta_p-1)^{m-1},\qquad
P=A\rtimes C_p.$$

Multiplication by $\zeta_p$ defines the action. Complex conjugation and
additive negation supply the two commuting reflections. The powers
$(\zeta_p-1)^{i-1}$ are the source's named generators. One lattice
calculation gives their individual orders, the order of $P$, every
presentation relation and the automorphism formulas. The marking's
intersection property follows from a prime-index subgroup argument.
The proof covers all parameters; finite models test its implementation.

This is the first complete application for **Topic F: Odd kernels and
cyclotomic polyhedra**. Its reusable material is contained in the paper.
A separate topic umbrella and further applications have not yet been
completed, so no multi-paper compression claim is made.

## Attribution and the correction

**[B] Results and earlier methods.** The three principal results are due
to Hou–Feng–Leemans–Qu. The Sylow and orbit arguments are their arguments
made explicit; character projectors are classical. The tightness converse
uses precisely the odd/even cases of Cunningham–Pellicer,
[*Classification of tight regular polyhedra*](https://arxiv.org/pdf/1408.6703v2),
Theorem 1.1. That theorem and the group–polytope correspondence remain
cited inputs.

**[I] Replacement argument.** The cyclotomic lattice and its exact
presentation bridge replace the source's longer binomial and
automorphism verification. They recover the named generators and
marking, not only an abstract group with the same order. Historical
priority for this organization has not been established.

**[E] Source correction.** In arXiv:2407.10388v1, the displayed
$r_1=xy r_0$ has square $x^2\ne1$ under its stated action. The body of
the paper uses the applicable $xy r_2$ marking. The replacement uses it
and assigns the larger exponent to $x$. The [ledger](research/case_study/phase236_source_ledger.json)
records both changes explicitly. No claim is made that the later journal
edition retains the defect.

## Verification and measurement

Fresh public checks pass seven cyclotomic and four abelian examples,
with all 64 subset-intersection equations for each. A separate GAP
program starts from the literal source presentation and checks five
parameters, including cases with trivial listed generators. Three
semantic rejection controls and a composite-index counterexample pass.
Lean verifies [five specified supporting declarations](research/case_study/formal/OddKernelIntersection.scope.md).
It does not yet verify the full cyclotomic arithmetic or classification.
See the [publication review](provenance/phase125_review.md).

The intake is one twelve-page primary manuscript and the replacement is
eight pages, with required programs and retained theorems stated. These
page counts are an inventory, **not a measured compression ratio**:
the exact source scope, typography, required certificates and topic
umbrella must be accounted for consistently. The introductory census and
historical survey are outside the recovered principal contract.
No open conjecture is proved by this application.

From the repository root, use a fresh output directory and local tool paths:

```sh
python3 -B -O research/case_study/phase236_check.py \
  --out /tmp/NEW-odd-kernel-check \
  --gap GAP --lean LEAN_4_32_2 --packages PINNED_PACKAGES
```

The frozen manuscript retains its original review-edition header. The
later independent review and publication record establish its accepted
status. The first PDF page also retains a minor source-title emphasis
artifact; it does not alter the mathematics.
