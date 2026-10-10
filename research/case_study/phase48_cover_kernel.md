# Exact quotient intersections: formal certificate

Private author package, 10 October 2026. This certifies the algebraic core of phase46 Lemma 1 and its locally injective corollary. It does not formalize the later polytope recognition, support classification, central-kernel count, or the general cover conjecture.

Let f:H→G be any group homomorphism, A,B≤H, and N=ker(f). Then

    f(A)∩f(B)=f(A∩B)
       iff N∩AB=(N∩A)(N∩B).

Every product here is a subset product, not a subgroup join. No finiteness, centrality, or surjectivity is assumed. This is a downward quotient criterion distinct from the earlier `LeemansLift.intersection_of_image_and_kernel`, which lifts an already-known intersection of images through a residual-kernel condition.

The proof is short. If ab∈N with a∈A,b∈B, equality of image intersections provides c∈A∩B with f(c)=f(a)=f(b⁻¹). Thus ab=(ac⁻¹)(cb) factors through N∩A and N∩B. Conversely, if f(a)=f(b), factor ab⁻¹=uv with u∈N∩A,v∈N∩B. Then u⁻¹a=vb belongs to A∩B and maps to f(a). The opposite subset inclusions are automatic.

If L≤H contains N and L∩A=L∩B=1, the right-hand product is {1}. Writing D=L∩AB gives the equivalent defect criterion

    f(A)∩f(B)=f(A∩B) iff N∩D={1}.

Normality of L is unnecessary for this algebraic conclusion. The actual quotient specialization takes any normal M≤L and f:H→H/M; its kernel is exactly M. In the polytopal application one separately retains normality and, for rotation groups, mirror invariance where needed to interpret the groups as regular marked covers.

The module `formal/QuotientIntersectionCriterion.lean` contains four checked theorems in namespace `MathCompression.QuotientIntersectionCriterion`:

| Declaration | Scope |
|---|---|
| `image_inf_iff_kernel_product` | Arbitrary homomorphism, complete equivalence |
| `quotient_inf_iff_kernel_product` | Actual quotient H/M, arbitrary normal M |
| `image_inf_iff_trivial_defect` | ker(f)≤L and L∩A=L∩B=1 |
| `quotient_inf_iff_trivial_defect` | Actual intermediate quotient by normal M≤L |

The proof imports only pinned mathlib modules. It does not import any existing project certificate or assume the target criterion as an axiom. The author build uses Lean 4.32.2 and the unchanged dependency manifest whose mathlib revision is `905b95818eb32af7874a58b427f50c1711a5e96c`. The fresh checked build took 5.13 seconds. The general kernel-product theorem depends on `propext` and `Quot.sound`; the other declarations also use `Classical.choice`. There are no unproved placeholders or native-evaluation axioms.

Replay from the private research directory with a new output path:

    python3 phase48_cover_kernel_check.py \
      --packages /Users/sasha/bogachev/formal/.lake/packages \
      --output-dir /private/tmp/phase48-cover-kernel-fresh

The runner checks the Lean version, every pinned dependency revision, tracked-file cleanliness, the exact four axiom reports, and source stability during compilation. It writes only into the new output directory. Existing compiled dependency objects remain trusted inputs; it does not rebuild all of mathlib. The bound report and log record the author run. Complete independent replay and public export are not claimed at author freeze.

All phase41, phase44, and phase46 originals remain unchanged. The open finite-cover question and literature-status limitations in phase44/46 remain unchanged. This is one new algebraic certificate candidate, not a new source-compression claim.
