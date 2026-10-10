# Independent review: the equal-label polygon application

10 October 2026. **Accepted for the complete declared F014 principal-result
contract.** The written theorem holds for every integer n≥3, including the
exact universal presentation. The exceptional n=2 specialization appearing
in the source's second corollary is supplied separately. The proof warrants
one principal-source admission if F014 has not already received that credit.
It adds no open-question answer, no whole-paper reproduction claim, and no
measured compression ratio.

The intake-to-replacement statement is:

> Li–Zhang, arXiv:2505.09505v1, Theorems 1.3 and 3.4 and
> Corollaries 3.5–3.6 follow from the retained polygon construction plus
> *Even subsets of a polygon and an equal-label presentation*.

The retained polygon result is Montero–Ivić Weiss's construction, already
proved in frozen ModuleC. The exact presentation and displacement argument
remain attributed to Li–Zhang. Our application explicitly identifies the
marked constructions, closes the normality/order argument, and formally
verifies its general algebraic part.

## 1. Exact sources and scope

I read the complete mathematical text of the twelve-page F014 author edition,
the entire new application and its actual Lean source and both executable
checkers. I independently viewed F014 physical pages 7, 9, 10, 11 and N013 physical
pages 8–9. The exact source hashes are bound in the author manifest. The matrix
actions, inverse-action display, presentation's full parameter range, source
commutativity calculation and two corollaries were checked visually. The
N013 polygon paragraph is Section 4, physical/printed page 9.

F014 Theorem 1.3 asserts existence of a self-dual regular rank-three polytope
of type {n,n} with n2^n flags for every n≥3. Theorem 3.4 identifies the full
universal presentation, with every displacement relation 1≤k≤n−1. Both
conclusions are recovered; no restriction to odd n, prime n or tested small
orders occurs. Corollary 3.5 restricts to odd n. Corollary 3.6 historically
quantifies **prime** p≥2 and integer s≥0. The author's contract writes all
integers p≥2, which is a valid stronger specialization of the new theorem,
but is not the source's literal quantifier. This review records the source
and the extension separately. The case p=2,s=0 is not silently excluded.

The literal inverse-action multiplication on source page 7 is qualified, not
accepted. No assertion about a different arXiv or journal edition is made.
The higher-rank Conjecture 3.7 is outside this positive application; the
project's separate counterexample must retain its own proof and credit.
Recovering the main results does not claim recovery of every auxiliary
statement, introductory priority statement, or definition in the source.

## 2. Complete mathematical argument

The model uses the even-coordinate subspace E_n of the binary permutation
module on Z/nZ. With a(i)=i+1, b(i)=−i, s=ab and q=e_0+e_1, the marking
(0,s),(0,b),(q,s) is well defined under left semidirect multiplication.
The basis f_j=e_0+e_(n−j), 1≤j≤n−1, gives exactly the source matrices V,A
for b,a. Thus s has its source matrix U=AV and the source's last coordinate
vector is q. This establishes the actual representation and marking bridge,
not only equality of dimensions or group orders.

Halving the generalized cube produces precisely this marking after ordering
the new string. The duality is conjugation by the single coordinate flip in
the larger binary module. Equivalently its displacement is the cocycle
c(g)=e_0+ge_0. This proves that it is an involutory automorphism and that it
reverses the marking. The adjacent orders are exactly n.

The direct intersection proof is complete. The first dihedral maximal
parabolic has zero translation coordinate; its dual has coordinate c(g).
Their common elements are exactly the stabilizer of coordinate 0, namely the
middle reflection subgroup. The third maximal parabolic is the four-element
subgroup displayed in the paper; its two intersections follow from its
nonzero translation coordinate and duality. Within each rank-two parabolic,
the singleton intersections are trivial. Every smaller intersection reduces
to these cases, proving the full marked IP. Finally, conjugates of q span
all edge differences of the cycle, hence E_n; the markers generate the whole
semidirect product before its order is counted.

For the universal presentation, put x=r_0r_1, y=r_1r_2 and t_k=y^kx^k.
The periods extend the stated finite list of square relations to every
integer k. Taking inverses and then conjugating gives both order-reversed
identities used in equation 12. Substitution proves that any two t_i,t_j
commute. There are at most n−1 nontrivial generators, so their subgroup N
is finite elementary abelian of order at most 2^(n−1).

The normality argument does not assume a quotient prematurely. Equation 14
shows x^(-1)Nx⊆N. Conjugation preserves finite order, giving equality.
The middle reflection sends t_k to t_(−k), and y=t_1x^(-1). Therefore N is
normal under all generators. Its quotient is a quotient of the dihedral
group of order 2n. This gives the universal upper bound n2^n. The generated
coordinate model attains this bound and satisfies every relator, so its
marked epimorphism from the presented group is an isomorphism. This step
rules out a larger infinite or finite universal group.

The n=2 adapter is C2^3 with its independent coordinate involutions. It has
all marked intersections, the required two adjacent orders, eight flags,
and an automorphism reversing the coordinates. The standard McMullen–Schulte
string-C-group correspondence is explicitly retained in passing to the
regular polytope. The direct proof does not need the disputed source product.

I found no mathematical gap in the accepted scope.

## 3. Convention correction and attribution

The source defines a homomorphism into matrices acting on column vectors
but then inserts the inverse matrix in a left semidirect multiplication.
Under these literal conventions the display is nonassociative. For n=3,
the two bracketings given in the application have translation coordinates
e_0+e_1 and e_1+e_2. I independently checked the calculation and the printed
formula. This is a correction of the displayed convention. It is not a
refutation of the main construction, which the consistent action and basis
bridge recover. A consistently defined right action could also repair it.

N013 already states the self-dual polygon output, its vertex/edge/face
counts and genus; its regularity and full group are supplied by the preceding
construction and the retained ModuleC proof. Li–Zhang's presentation proof
already contains the essential commuting-displacement argument. The new
application does not claim either existence or that commutativity mechanism
as a newly discovered theorem. The explicit source-to-source marked basis
identification, closed normality argument, convention diagnostic and formal
proof are its local contributions. No exhaustive historical-priority
conclusion is inferred.

## 4. Formal and computational verification

All ten author exports and four retained bindings match the frozen manifest.
A fresh independent execution of `phase229_lean_check.py` passed in 1.33 seconds.
I read the full definitions and proof terms before accepting the five
selected declarations. They establish arbitrary-group displacement
commutativity, the exact conjugation identity, commutativity of the generated
subgroup, the finite-period adapter from the actual finite relation list,
and its combined specialization. Integer remainders, including negative
indices and zero, are handled in the adapter. The only reported axioms are
propext, Classical.choice and Quot.sound; no native evaluation is used.

This is substantive but partial formal verification. N's normality and
cardinality, the semidirect representation, matrix-basis calculation,
parabolic intersections, polytope correspondence and the final universal
presentation theorem are written proofs. They have not been composed into
one Lean theorem. Dependency objects are cached as disclosed by the runner;
this review does not claim a fresh rebuild of all Mathlib dependencies.

The author's finite diagnostic reproduces byte exactly for n=3,…,10.
Separately I wrote a native GAP realization on Omega×F2, using literal
permutations rather than importing the author's group-product code. It
checks n=3,4,5,6,7,8,11,13, all 64 marked-intersection pairs at each value,
exact adjacent and full-group orders, the complete extra-relator list,
and marker reversal. It also checks the exceptional C2^3 model. An altered
translation is rejected. A separate S4 example shows why period relations
alone do not imply displacement commutativity: x=(1234), y=(1243) both have
fourth power1, but yx and y²x² do not commute. None of these samples replaces
the unbounded written or formal arguments.

## 5. Product structure and next accounting step

The dependency graph correctly records the retained generalized-cube/halving
route through C.Polygon, followed by the marked identification, presentation
and parameter adapters. Its role is explanatory; it does not contain weights
or justify removing the earlier proof's retained inputs. The full chosen
topic umbrella remains charged within the topic, and another topic pays its
own whole umbrella independently.

The complete application renders to five ordinary A4 pages at 11 points.
Every page was visually inspected. The original long dependency display 18
was overfull; the review renderer records a two-line layout of precisely
that display, retaining every word and arrow. Frozen author text is unchanged.
The final render has no overfull boxes or missing glyphs, and one harmless
underfull paragraph. The last page contains the final bibliography entry;
no artificial padding was added.

This is a complete short application recovering one principal source through
an existing shared construction. It is not itself a 20–25-page multi-source
volume. No source/replacement page ratio is licensed by this rendering, and
no chronological sawtooth has been measured. The next accounting step is to
place it in its chosen topic and charge the entire umbrella plus all complete
local application proofs and declared required artifacts under one matched
metric. Its mathematical principal contract may be admitted now; those
measurement and broader product tasks remain separate.
