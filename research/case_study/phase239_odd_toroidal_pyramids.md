# Finite minimal covers of all exceptional square-torus pyramids

Author-frozen for independent review, phase239, 10 October 2026. The new statement concerns
finite covers. It is distinct from the theorem about unrestricted regular
covers in phase216. The isolated parameter n=3 is treated in the frozen
phase224 packet; the argument below extends its fixed quotient uniformly.

## 1. The statement and the earlier results used

For an integer n≥3, let T_n be the regular square torus {4,4}_(n,0), with
vertices (Z/nZ)^2, and let P_n be its pyramid. Write G_n=Mon(P_n), with the
four generators s_0,...,s_3 given by flag adjacency.

**Theorem.** For every n≥3 and every prime ell not dividing 2n, there is a
finite regular polytopal cover of P_n whose marked group H_(n,ell) maps onto
G_n with kernel isomorphic to (F_ell)^642. In particular, for every odd n≥3,
P_n has infinitely many pairwise nonisomorphic finite minimal regular
polytopal covers. For each permitted prime one can choose such a minimal
cover with degree ell^e over G_n, where 1≤e≤642.

This is not a classification of the minimal covers, and it does not select
a minimal descendant or determine its degree. The statement does not settle
the finite-cover question for arbitrary polytopes.

Here are the earlier mathematical inputs and their roles.

* Cunningham, Pellicer and Williams, *Stratified operations on maniplexes*,
  Algebraic Combinatorics 5 (2022), 267–287, Definition 3.1 and Proposition 3.3
  (printed pp. 273–274), give the five-layer description of a pyramid. Their
  Theorem 4.3 (p. 282), summarizing Pellicer–Williams (2018), says that among
  pyramids over regular toroidal maps the monodromy fails the intersection
  property precisely for the square tori {4,4}_(n,0) with n odd. We retain
  this nonpolytopality classification. We do not claim its proof as new,
  nor infer it merely from a group order or from a few parameters.
* Monson and Schulte, *Finite Polytopes have Finite Regular Covers*,
  arXiv1209.1167v1, Theorem 3.4, already give a finite regular cover of every
  finite polytope. Their Example 3.7 treats P_3. Mere finite-cover existence
  is therefore not the additional conclusion here.
* The surface theorem of phase211 and its independent review218 produce
  covers of the particular group D of order 3840 used below, with kernel
  (F_ell)^642 for every prime. The exact cell witness is the same one as in
  frozen224. The coprime pullback theorem of phase126 and the minimal-kernel
  argument of phase211 are also reused.

The new argument is the uniform passage G_n→E→D. It proves that the kernel
of this passage cannot kill an intersection defect for any n≥3. This is a comparison with the stated sources, not an exhaustive historical
priority claim. No formula
for the full order of G_n from the 2018 classification is assumed. The fixed
finite calculation and the elementary integer argument have different
roles: the former checks a group of order 61440 once; the latter proves that
this single calculation applies to all n.

## 2. Affine coordinates for flags and the five layers

Let L be the group of the eight signed permutation matrices in dimension2.
Use the following affine isometries of the integral square grid:

    r_0(x,y)=(1−x,y),   r_1(x,y)=(y,x),   r_2(x,y)=(x,−y).       (1)

Their linear parts are R_0=diag(−1,1), R_1 the coordinate swap, and
R_2=diag(1,−1). The linear group is L≅D_8. Reducing the translations modulo n
gives the affine group B_n=(Z/nZ)^2⋊L. It acts regularly on the flags of T_n:
an affine isometry is determined by the image of the flag consisting of
(0,0), the horizontal edge from(0,0) to(1,0), and the unit square above it.
Conversely every torus flag determines one translation and one of the eight
orientations. This remains faithful for n≥3. Formula(1) sends that flag to
its three adjacent flags. Under this identification adjacency on a flag
label g∈B_n is right multiplication by r_i.

The flags of P_n are the pairs(k,g), with 0≤k≤4 and g∈B_n. The generator
s_i, 0≤i≤3, acts by

    (k,g) ↦ (k, g r_i)       if k<3−i,
             (k+1,g)        if k=3−i,
             (k−1,g)        if k=4−i,
             (k,g r_(i−1))  if k>4−i.                         (2)

The two moving-layer cases insert or remove the apex in the flag. For a
base flag(v,e,f), layer k corresponds to insertion position j=4−k in

    (apex,cone(v),cone(e),cone(f)),
    (v,cone(v),cone(e),cone(f)),
    (v,e,cone(e),cone(f)),
    (v,e,f,cone(f)),
    (v,e,f,base facet).

Thus (2) is the flag action of the stated face poset, with 40n^2 flags.
The replay additionally checks the explicit coordinate-to-face bijection
and all four adjacency relations for n=3 and n=5. Those finite checks test
the conventions; the description above is the argument for arbitrary n.

Every word in the s_i acts as a permutation of the five layers and, on each
input layer, right multiplication by an element of B_n. This gives a
faithful embedding G_n≤B_n^5⋊S_5: an action which fixes all flag labels has
trivial layer permutation and trivial multiplier on every layer. On
forgetting translations we obtain a marked epimorphism

    rho_n:G_n→E≤L^5⋊S_5.                                    (3)

The group E is independent of n. It is generated on the 40 pairs(k,M),
M∈L, by the same formula(2), with r_i replaced by R_i. The kernel K_n embeds
in ((Z/nZ)^2)^5. Consequently

    |K_n| divides n^10.                                     (4)

This bound suffices; equality is not needed anywhere below.

## 3. The translation kernel on the common end intersection

Put A_n=G_n,012, B'_n=G_n,123, C_n=G_n,12 and T'_n=A_n∩B'_n. We use primes
on B'_n and T'_n only to distinguish them from the base affine group B_n and
the torus T_n.

**Lemma 1.** The restriction of rho_n to T'_n is injective.

**Proof.** A word in s_0,s_1,s_2 fixes layer 0. On each of layers 1,...,4 every
local multiplier occurring along the word belongs to <r_0,r_1>; this follows
directly from(2), since a nontrivial r_2 from s_2 can occur only in layer 0.
The group F=<r_0,r_1> consists of the eight integral isometries fixing
h=(1/2,1/2). For M∈L its unique element with linear part M is

    x ↦ Mx+(1−M)h.                                         (5)

Its translation entries are 0 or 1, and the map F→L is an isomorphism. In
particular an element of F with trivial linear part is the identity after
reduction modulo any n. Hence an element of K_n∩A_n can have a translation
coordinate only in layer 0.

Dually a word in s_1,s_2,s_3 fixes layer 4, and all its local multipliers on
layers 0,...,3 belong to V=<r_1,r_2>. This is the linear group fixing the
origin, so an element of K_n∩B'_n can have a translation coordinate only in
layer 4. An element of K_n∩T'_n has both support restrictions, and all five
coordinates are therefore trivial. Its layer permutation is trivial by
membership in K_n. The faithful embedding in Section 2 gives that the
element is the identity. ∎

For the middle layers there is a further restriction. An element of T'_n
fixes layers 0 and4 and permutes layers 1,2,3. On any one of these middle
input layers its affine multiplier is both an element of F modulo n and
an element of V modulo n. Its translation part is therefore zero modulo n.
By(5) that part has entries 0 or 1; since n≥3, both entries vanish integrally.
It follows that the linear part M satisfies

    M(1,1)=(1,1).                                          (6)

Of the eight signed permutation matrices exactly two satisfy(6): the
identity and the coordinate swap. Notice why the integral representative
matters: a conclusion about an arbitrary translation would not follow from
its vanishing modulo n.

## 4. One finite group calculation for every parameter

In E set A=E012, B=E123, C=E12 and T=A∩B. Define J to be the elements of T
whose multipliers on input layers 1,2,3 all satisfy(6). This is a subgroup:
T preserves the set of these three layers, and the two allowed matrices
form a subgroup. Section 3 gives

    rho_n(T'_n)≤J,     rho_n(C_n)=C,     rho_n|_(T'_n) injective.   (7)

The exact permutation calculation starts solely from the eight displayed
matrices and the layer formula. It returns

    |E|=61440,  |A|=|B|=12288,  |C|=24,  |T|=3072,  |J|=48.  (8)

On ten points use the same four permutations as frozen224:

    d0=[3,4,1,2,5,6,7,8,9,10],
    d1=[1,2,5,6,3,4,8,7,10,9],
    d2=[1,2,3,4,7,8,5,6,10,9],
    d3=[2,1,4,3,6,5,9,10,7,8].

Let D=<d0,d1,d2,d3>. The assignments s_i↦d_i define an epimorphism pi:E→D.
Writing N_0=ker pi, the calculation checks actual subgroup equalities

    |D|=3840,    |N_0|=16,
    N_0∩J=N_0∩C,    |N_0∩C|=2.                              (9)

The map is constructed by GAP's checked GroupHomomorphismByImages, not its
unchecked variant. The list defining J is tested to be exactly a subgroup,
and (9) is tested as subgroup equality. A control omitting(6) fails:
N_0∩T is not contained in C. Thus the affine restrictions do substantive
work and cannot be replaced by the much larger orientation intersection.

Let q_n=pi∘rho_n and N_n=ker q_n. Since rho_n is onto E, its restriction
N_n→N_0 is onto with kernel K_n. Equations(4) and(9) give

    |N_n|=16|K_n| divides16n^10.                             (10)

**Lemma 2.** N_n∩T'_n=N_n∩C_n for every n≥3.

**Proof.** Let x∈N_n∩T'_n. By(7), rho_n(x) belongs to J, and it belongs to
N_0 because q_n(x)=1. By(9) it belongs to C. Choose c∈C_n with
rho_n(c)=rho_n(x); such a c exists by(7). Both c and x belong to T'_n, so
Lemma 1 gives x=c. Thus x∈C_n. The reverse containment follows from C_n≤T'_n.
∎

This proves the required kernel condition uniformly. It does not assume
that rho_n(T'_n)=J, or that T'_n has order48, or that G_n has a particular
order beyond finiteness. None of those stronger statements is needed.

## 5. The two end groups and the coprime pullback

We record explicitly the small general fact about rank-four polytopes used
here. The first three monodromy generators act on the disjoint union of
the flags of its facets. If x belongs to G01∩G12, it fixes every vertex and
every 2-face. As an element of G01, it acts on each polygonal 2-face by a
fixed word in s_0,s_1. Write this word in dihedral normal form as a power of
s_0s_1, optionally followed by s_1. The presence of that last factor is
determined by word parity and is the same on every 2-face. Fixing every
vertex forces the rotation power to be trivial on every polygon. The
resulting action is therefore everywhere the identity, or everywhere s_1.
This proves G01∩G12=G1. Duality proves G12∩G23=G2. The recursive intersection
criterion gives that both end subgroups of any rank-four polytope's
monodromy are string C-groups. In particular A_n and B'_n are C-groups.

The frozen surface for D has 3840 vertices, 7680 edges and 3200 faces. Its Euler
characteristic is −640; it is orientable. The complements associated with
the three required parabolic unions have respectively 2704, 3199, 3199 faces
and are connected. The surface theorem of phase211 therefore gives, for
every prime ell, a finite marked C-group Q_ell→D with kernel(F_ell)^642.
The replay uses precisely the four permutations in Section 4 and reruns
that retained cell construction. Its output is not extrapolated in ell;
the written homology theorem supplies that quantifier.

Choose ell not dividing2n. By(10), ker(Q_ell→D) and N_n have coprime orders.
Let H be the subgroup of Q_ell×_D G_n generated by the paired marks. The
coprime pullback theorem gives, for every set I of marks,

    H_I = (Q_ell)_I ×_(D_I) (G_n)_I.                         (11)

For clarity, the argument requires no split extension. If e is the exponent
of ker(Q_ell→D) and u∈N_n∩(G_n)_I, choose an e-th root v of u in its cyclic
subgroup. Lifting v to a paired generated element(a,v) and taking its e-th
power gives(1,u). This isolates the full kernel in each parabolic and proves
(11) from surjectivity of the two coordinate projections.

Because Q_ell is a C-group, (11) then gives, for J'=I∩I',

    H_I∩H_I' = (1×(N_n∩(G_n)_I∩(G_n)_I')) H_J'.             (12)

For the two end intersections this is the correct common subgroup because
A_n and B'_n are C-groups. For the remaining top intersection Lemma 2 gives
the same conclusion. The recursive criterion proves H is a string C-group.
Its string relations hold in both coordinates and its marks remain distinct
and nonidentity under projection to G_n. Taking I to be all four marks in
(11) shows that H→G_n has precisely kernel(F_ell)^642. This proves the first
assertion of the theorem, including finiteness.

## 6. Infinitely many finite minimal covers when n is odd

For odd n≥3, the retained 2022 Theorem 4.3 says G_n is not a string C-group.
Every finite regular cover has a minimal regular quotient over P_n, since
its admissible normal-kernel lattice is finite. Choose a minimal descendant
R_(n,ell) of H_(n,ell). Its kernel over G_n is a quotient of(F_ell)^642, so
has order ell^e with 0≤e≤642. It cannot be trivial, since that would give the
non-C marked group G_n. Hence 1≤e≤642.

There are infinitely many primes not dividing the fixed integer 2n. For two
different such primes the positive kernel orders are distinct. A
rank-preserving isomorphism of regular polytopes identifies their universal
marked kernels: changing a base flag conjugates a stabilizer, and the
stabilizer is normal for a regular polytope. Consequently these minimal
covers are pairwise nonisomorphic, even without choosing a base flag.

**Corollary (transfer through the base map).** Let M be a finite abstract
polyhedron whose smallest reflexible cover is the marked regular square
torus T_n. Then the pyramid over M has the same marked monodromy group as
P_n. Consequently the finite covers constructed above cover its pyramid as
well. If n is odd, that pyramid also has infinitely many pairwise
nonisomorphic finite minimal regular covers.

Indeed the equality of marked monodromy groups is exactly Cunningham,
Pellicer and Williams, Theorem 3.4, printed p.274. A regular polytope covers
a given polytope precisely when its universal normal kernel is contained
in the latter's monodromy kernel: its trivial flag stabilizer automatically
satisfies the covering condition. Thus both pyramids have the same
admissible regular-cover kernels and the same minimal ones. This applies,
in particular, to the nonregular equivelar toroidal maps with this stated
smallest reflexible cover. The identification of such a base cover is an
input, not a classification newly proved here.

The distinction between finite and unrestricted covers is essential. The
new argument supplies finite covers with controlled prime-power kernels
for this whole exceptional family. It does not justify taking arbitrary
infinite covers from phase216 and replacing them by finite quotients while
retaining every parabolic intersection.

## 7. Verification and formal scope

`phase239_pyramid_check.py` rebuilds the 40-point orientation action, checks
the affine-to-literal flag correspondence at n=3 and n=5, checks(8)–(9) in
GAP, and replays the frozen surface witness. The omission of(6) is a
mathematical negative control; replacing the conclusion of Lemma 2 by its
hypothesis is not used as a test.

`formal/PyramidKernelTransport.lean` proves four elementary statements:
disjoint single-coordinate supports are trivial; a 0-or-1 coordinate vanishing
modulo n≥2 vanishes integrally; a trivial kernel on a subgroup gives
injectivity there; and an injective map on the intersection transports the
fixed kernel test of(9). The runner also replays the three frozen coprime
pullback theorems and six frozen minimal-kernel lemmas. All axiom reports
are confined to Lean's standard axioms. The matrix action, the full
geometric proof, GAP's algorithms and the retained 2022 classification are
not thereby formalized in Lean. The report keeps these scopes separate.
