# Root semantic review of Hermitian transport

11 October 2026. **Accepted.** Root read the entire original Hermitian-unital
proof, the complete independent phase210 review, the transport supplement,
all thirteen new Lean proofs, the retained connectivity theorem, the GAP
program and the replay driver. Root also read the primary Construction 3
and Conjecture 1 from printed pages 565 and 569. The source-review agent's
visual inspection is retained; root does not claim a new complete reading
of the fourteen-page source here.

## The actual formal statement

The four-entry `Mat` structure acts by the usual column formula.
`GramIsometry` expands exactly Mᵀ J σ(M)=J for the hyperbolic Gram matrix.
Its equivalence with the entrywise special-unitary conditions also includes
ad−bc=1. Solving these equations checks the claimed semantic connection;
the predicate is not merely named after the desired group.

For v=(x,y), the basis matrix with columns v and (−σ(x),σ(y)) has
determinant N(v). Thus the nonzero-norm hypothesis is precisely what makes
the proposed transport invertible. The displayed formula is B_w B_v⁻¹.
When the norms agree, the determinant is one and the form is preserved.
This remains valid in characteristic two. The Lean existence, Gram,
transport and uniqueness proofs establish those entrywise statements over
any involutive field, without a finite counting assumption.

The uniqueness proof actually uses the unitary entry conditions and the
image of the first column to determine all four entries. It does not
assume uniqueness as an orbit hypothesis. The upper and lower matrices
satisfy the same actual equations. Their differences lie on the isotropic
coordinate axes, and nonzero norm forces both coordinates nonzero, so a
nonidentity root gives a genuine move. All thirteen formal statements
match the role assigned to them in the written proof.

## Geometric and finite-field interfaces

For K=F_(q²), the trace-zero line is δF_q with δ nonzero and δ² fixed.
Conjugation by diag(δ,1) sends both root families onto the complete upper
and lower elementary families over F_q. The elementary elimination and
diagonal factorization in the supplement prove generation, including q=2.
Together with unique transport, this establishes the transitive action
required by the retained connectivity lemma. These finite-field and group
identifications remain written, rather than silently included in Lean.

The source construction uses outside points, blocks, and original flags
with the three stated positive and negative incidence conditions. The
projective-to-shell map is bijective; two outside points have a common
residue flag exactly when their normalized difference is isotropic.
Every flag vertex has neighbors, so the connected shell graph proves the
whole block residue connected. Root checked the other residues, panels
and global connectivity independently from the definitions.

The PGU chamber argument normalizes an ordered isotropic point pair,
then identifies its complete projective stabilizer with the diagonal
torus. Its regular action on the nonzero secant parameter proves chamber
regularity. No PSU sufficiency is assumed when its orbit is smaller.
All arguments include q=2. The original question only requires q>2.

## Fresh execution and evidence boundaries

The public adapter verifies 32 frozen public bindings and runs the unchanged
mathematical programs and controls. It omits the private PDF/text hashes
and the old compiled object hashes, then freshly recompiles the two Lean
sources. The old private proof is supplied byte for byte under an archive
name because the earlier public version changed one bibliography link.
The two proof versions have identical mathematics. No frozen proof is edited.

The fresh replay passed in 11.085 seconds. It checks literal unital models
at q=2,3,4,5, full induced PGU chamber stabilizers and all 18,612 ordered
transport pairs. All fourteen formal declarations, including the retained
connectivity theorem, compile with standard axioms only. Two altered Lean
claims and two corrupted geometric calculations are rejected. The complete
all-q statement rests on the written proof and these general formal
components, not on extrapolating the finite models.

The complete source conjectural statement is accepted. Full formalization,
historical priority and whether the question was still open immediately
before this proof remain unestablished. This admission strengthens one
existing question entry and adds no new principal-source credit or ratio.
The previous pending-root-review label is preserved in frozen phase210
and superseded by this separate review.
