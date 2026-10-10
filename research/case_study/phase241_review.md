# Independent review of the projective matrix centralizer core

**Verdict: accept the six declarations in the stated normal-form scope.**
No change to frozen phase237 is required. This is additional formal
verification of the existing projective-line proof; it adds no principal
source contract and proves no new open question.

The reviewed author manifest is `phase237_manifest.json`, SHA256
`2095e96025bb4978babe7ee2e64d23267c8d0a3452c8a815a2bebe0cdb3ef98f`.
The complete formal source has SHA256
`98a746e4b34c5dcf3da4c4bf575d8a2517dfa59d2a4a4b44e869c044335df78f`.
All ten author exports were verified against the manifest. I read the
complete Lean source, the scope note and the runner. I also checked all
nine revisions in the existing formal dependency manifest against clean
working source trees; the author runner itself checks only the Mathlib
revision. Precompiled dependency objects remain trusted.

## Mathematical reading

The predicate `projectivelyCommutes A B` is exactly the existence of a
nonzero scalar c with AB=cBA. It does not build in a centralizer
classification. Invertibility is imposed separately by determinants.

For M=[[u,v],[w,z]] and D=diag(l,1), projective commutation gives
ul=clu, v=clv, wl=cw, z=cz. If c≠1, the diagonal entries vanish;
invertibility then makes v,w nonzero, forcing cl=1 and l=c. This
contradicts l²≠1. Hence c=1, and l≠1 forces v=w=0. This is the actual
content of `off_diagonal_zero`, with both l≠0 and the determinant
hypothesis present.

For an invertible diagonal M, commutation with [[0,d],[1,0]] gives
u=cz and z=cu; the cancellation of d uses its explicit nonzero
hypothesis. Consequently u²=z², so M is a nonzero scalar multiple of
I or diag(−1,1). This is valid over every field, including characteristic
two, where the two alternatives coincide. The file does not assume odd
characteristic unnecessarily in this semisimple theorem.

For U=[[1,1],[0,1]], the analogous entry equations first force the
projective scalar to1, then w=0 and u=z. An additional commutation with
[[-1,d],[0,1]] forces the second projective scalar to1 and 2v=0.
Here the characteristic hypothesis is essential and appears explicitly
as `(2:F)≠0`. The resulting matrix is a nonzero scalar multiple of I.
The free parameter d is allowed to be zero, correctly.

The trace-zero identity is an entrywise identity, with division by2
justified. Its determinant corollary uses l≠1; it does not improperly
require the original diagonal matrix to be invertible. These two
declarations supply the displayed normal-form representative, not a
formal descent theorem.

The actual proofs use matrix multiplication, determinants, field
cancellation and polynomial identities. There are no custom axioms,
proof holes, native decision procedures, assumed subgroup membership,
or conclusions smuggled into the hypotheses.

## Independent replay and controls

The fresh author-runner replay at `/private/tmp/phase241_fresh237`
compiled all six declarations under Lean4.32.2 and the pinned Mathlib
revision. Every axiom report is confined to propext, Classical.choice
and Quot.sound. Both modified versions failed elaboration as required.
The review package preserves the resulting report and logs.

There is a small terminology distinction: the runner replaces the
nondegeneracy inequalities by their complementary equalities. These
are tests in the excluded boundary regimes, not literal logical
weakenings of the original hypotheses. Compiler failure by itself would
not establish that the changed mathematical conclusion is false.

The independent `phase241_matrix_controls.py` therefore verifies actual
counterexamples to both changed assertions. Over F5, take l=−1,d=1 and
M=[[0,1],[1,0]]. It is invertible, commutes projectively with diag(−1,1)
using scalar−1, and commutes with the second matrix using scalar1.
It is neither kind of diagonal scalar matrix in the conclusion. Over
F2, take M=U=[[1,1],[0,1]] and d=0. The second matrix is I; all stated
commutation hypotheses hold, but M is not scalar.

The same independent program checks every invertible matrix over F3,
F5 and F7 against all parameters satisfying the corresponding original
hypotheses. This gives52,224 semisimple configurations and16,656
unipotent configurations, with352 and68 joint-hypothesis hits
respectively; all conclusions hold. The semisimple parameter set over
F3 is empty, and this is recorded rather than counted as positive
evidence. These finite diagnostics check the interpretation of the
matrix predicates; the general result is supplied by Lean.

## Exact admission boundary

Accepted: the two entry lemmas, the split semisimple and unipotent
centralizer conclusions, the trace-zero identity and its determinant
corollary. These are material formal components of the phase230 common
proof, not merely abstract group interfaces.

Still written: conjugacy to these forms over an algebraic closure,
transport under change of basis, the quotient interface to PGL,
descent of the trace-zero representative to the original field,
the Dickson subgroup inputs and the finite classification applications.
Neither the full centralizer-descent lemma nor either source
classification is wholly formalized by this packet. The author's scope
note states this accurately.

Reproduce the independent diagnostics with
`python3 -B -O phase241_matrix_controls.py`; reproduce the formal replay
with the invocation in `phase237_scope.md` and a new output path.
The only suggested editorial clarification is to describe the two
mutations as excluded-boundary tests when reporting them publicly.
Frozen phase237 and all public files were left unchanged.
