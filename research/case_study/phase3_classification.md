# Cyclic cores and binary extension data for L035

This note targets Hou–Feng–Leemans, *Existence of regular 3-polytopes of order
2^n*, arXiv1802.08947v2, Theorem1.3 (catalogue L035, also published under the
title *2-groups behaving as automorphism groups of regular 3-polytopes*).
The principal task here is completeness of the eight high-type families,
not existence alone. The proof below closes all three branches. The third uses
an independently reproduced finite seed: all marked {4,8} groups of order256,
enumerated from the GAP SmallGroups library. This library and the explicitly
stated cyclic-core theorem remain retained ingredients, not consequences of
the binary extension calculus.

## 1. A bounded quotient theorem

Let (G;a,b,c) be a rank-three string C-group of order2^(t+s), of type
{4,2^t}. Put r=bc, m=2^t, d=(ab)^2, and assume t>=s-2.
Then

    A=<r^(2^(s-2))> is normal in G,
    |G/A|=2^(2s-2),
    G/A is a string C-group of type {4,2^(s-2)}.       (1)

Here the core estimate is the explicit retained theorem of Lucchini: if a
cyclic proper subgroup M of a finite group H has core K, then
|M:K|<|H:M|. This is Proposition2.9 in the source, citing Isaacs,
*Finite Group Theory*, Theorem2.20.

Proof. The rotation subgroup H=<ab,bc> has index at most2. It cannot equal G:
the three distinguished involutions form an irredundant generating set of a
finite2-group, so the Burnside basis theorem gives d(G)=3. Thus |G:H|=2.
For M=<r>, Lucchini gives |M:Core_H(M)|<2^(s-1), hence this index is at most
2^(s-2). Consequently A is characteristic in the cyclic core, so H normalizes
it; b inverts r, and therefore G normalizes it. The order assertion follows.
The left parabolic <a,b> meets A trivially, by IP. Since A is contained in
the right parabolic <b,c>, the images of those two parabolics still intersect
in <bA>. Their orders and independence follow at once. This proves (1).

Every commutator of G centralizes A: conjugation on A maps into the abelian
group Aut(A). In particular,

    [d,r^(2^(s-2))]=1.                              (2)

Also the unique involution z=r^(m/2) of A is central in G whenever A is
nontrivial. For s=3,4,5 the quotient orders are16,64,256, independent of t.
This improves the reduction from one central-involution step at a time to a
single bounded quotient.

## 2. Completeness of the first branch

For s=3, G/A has type {4,2} and order16. Its presentation forces it to be
D8×C2. Therefore [d,r] belongs to A. Write h=[d,r]. Since h commutes with r,
(2) gives h^2=[d,r²]=1. Thus h is1 or z. The identities a²=b²=c²=1,
[a,c]=1, (ab)^4=1 also give d^c=d^r, so

    [d,c]=z^ε,   ε in {0,1}.                        (3)

These are precisely the two relation patterns of G1 and G2. This proves
necessity without an induction or a finite census. The models in Section4
show that both possibilities have order8m and full IP; the normal forms there
also prove uniqueness as marked groups.

## 3. Completeness of the second branch

For s=4, G/A has type {4,4} and order64. It is the unique marked square-grid
quotient with that order. Here is the needed uniqueness argument, rather than
an appeal to a polytope list.

The universal group [4,4] is W=Z²⋊D8, with the explicit affine generators and
normal-form proof in compression_phase2.md. The kernel of a marked quotient
of type {4,4} lies in the orientation-preserving subgroup: the same Burnside
basis argument makes the quotient's rotation subgroup index2. The kernel has
no nontrivial torsion. Indeed a finite-order planar isometry fixes a point;
the square tiling moves that point into its fundamental triangle, whose
stabilizer is one of the three finite standard parabolics. All three embed in
the marked quotient by the pair orders and IP. An orientation-preserving
Euclidean isometry of infinite order is a translation. The kernel is therefore
a D8-invariant sublattice Λ of Z², with index64/8=8.

Identify Z² with Z[i]. Stability under a quarter-turn makes Λ an ideal of the
Gaussian integers. Since Z[i] is Euclidean, an ideal of index8 is generated
by an element of norm8; all such elements are associates of2+2i. Thus
Λ=2<(1,1),(1,-1)> is unique. In this affine quotient [d,r²]=1.

It follows that h=[d,r²] lies in A. Since h commutes with r, (2) gives h²=1.
Therefore

    [d,r²]=z^ε,   ε in {0,1},                       (4)

which are exactly G3 and G4. There is no finite computational seed in this
necessity proof. Section4 supplies existence and marked normal forms.

## 4. Eight finite extension models from at most four binary generators

All commutators below use [x,y]=x^(-1)y^(-1)xy and x^r=r^(-1)xr.
First construct a small group D with a distinguished central involution z,
then an automorphism T of D. In every case T fixes z.

* Branch s=3: D=<d0,z> is elementary abelian of order4, and
  T(d0)=d0 z^ε.
* Branch s=4: D=<d0,d1,z> is elementary abelian of order8, and
  T(d0)=d1, T(d1)=d0 z^ε.
* Branch s=5: D has normal forms d0^u d1^v d2^w z^e, with all four
  generators involutions, z central, [d0,d2]=1 and
  [d0,d1]=[d1,d2]=z^β. Put
  T(d0)=d1, T(d1)=d2, T(d2)=d0 d1 d2 z^ν.
  Here β,ν are independently0 or1.

The last D has order16: its multiplication is the binary-coordinate law
(u,v,w,e)(u',v',w',e')=(u+u',v+v',w+w',
e+e'+β(vu'+wv')). This is associative by bilinearity. The displayed T
preserves all relations and has order dividing4. The first two cases have
the same elementary verification.

Adjoin a rotation r of order m acting by x^r=T(x), and identify its half-turn
with z:

    N=(D⋊<r>)/<z r^(-m/2)>.

The notation specifies right conjugation by r. For the present parameters
m is divisible by32, so T^(m/2)=1; the identified subgroup is central of
order2 and meets D trivially. Hence |N|=|D|m/2, and r retains order m.

There are commuting involutory automorphisms A,C of N as follows:

    A(r)=d0 r, A(d0)=d0;
    C(r)=r^(-1), C(d_i)=T^(1-i)(d0), C(z)=z.

In branches s=3,4, A fixes every element of D. In branch s=5, it fixes
d0,d1,z and sends d2 to d2 z^β. These formulas respect the defining
relations and z=r^(m/2). For example, in the last branch
(d0 r)^4=r^4 z^ν, so A preserves that identification since8 divides m/2.
The identities A²=C²=1 and AC=CA follow on r,d0, which generate N.

Set G=N⋊<a,c>, where a,c induce A,C and generate C2². Define b=rc.
Then a,b,c are involutions, [a,c]=1, bc=r, and (ab)²=d0. Thus the pair
orders are4,m,2 and |G| is respectively8m,16m,32m.

The parabolic intersection is transparent. The images of a,b in G/N are
independent, whereas <b,c> has image <cN>. The only possible elements of
<a,b>∩<b,c> are1,b,d0,d0b. The normal form in N gives d0 not in <r>;
hence the intersection is exactly< b>. This proves full rank-three IP.

The defining twist words evaluate to (3), (4), and, in the final branch,

    [a,r²]²=z^β,       [a,r⁴]=z^ν.                  (5)

Consequently the eight constructions realize precisely the source's eight
marked relation patterns.

For actual groups in the first two branches, these normal forms also prove
uniqueness. Put d_i=d^r^i. In branch1, (3) gives d1=d0 z^ε. In branch2,
(4) gives d2=d0 z^ε. Conjugation by a fixes d0 and d1; applying it to the
last equation, and using centrality of z, forces [d0,d1]=1. Thus every
element collects into exactly the displayed extension model. There can be
no additional group of the same order. This proves the first four marked
classification families with a common extension argument.

Explicitly, d1^a=d1, while d2^a=(d1^(d0 r))=(d1^d0)^r.
The equation d2=d0 z^ε is fixed by a; comparing gives d1^d0=d1.

## 5. The finite seed and completeness of the third branch

The exact census phase3_256_census.g checks all1651 order256 groups in the
SmallGroups library with abelianization C2³. All other groups are excluded
because three independent involutory generators force precisely that
abelianization. It anchors r at every conjugacy class of order8 elements
outside the Frattini subgroup; c ranges over every centralizer orbit of
involutions inverting r and independent modulo Φ(G); a ranges over every
involution commuting with c, outside the plane spanned by r,c modulo Φ(G),
and with |ab|=4, where b=rc. Burnside's theorem certifies generation, and an
explicit parabolic intersection test certifies IP. Thus no eligible marking
is omitted.

All92 resulting anchored triples satisfy exactly one of these four patterns,
where now r has order8 and d=(ab)²:

| Pattern | Relations | Anchored triples | SmallGroup ID |
|---|---|---:|---|
| I | [a,r²]²=1, [a,r⁴]=1 |64|[256,5078]|
| II | [a,r²]²=r⁴, [a,r⁴]=1 |4|[256,6665]|
| III | [d,r²]=r⁴ |16|[256,6661]|
| IV | [(r²)^a,r]=r⁴ |8|[256,6665]|

Only these relation implications, not a count of isomorphism orbits, are
needed for the proof. The 92 counts depend on the stated anchoring scheme.
The log records GAP4.15.1 and completes in about51 seconds. This is an
independent exhaustive reproduction of the finite seed, while retaining
the SmallGroups classification through order256 as an explicit input.

Return to m=2^t>=32 and A=<r⁸>. PatternIII would give
h=[d,r²]=r^e with e≡4 mod8. Since d centralizes A, h⁴=[d,r⁸]=1, but
r^(4e) has exponent of 2-adic valuation4 and is nontrivial for m>=32.
Thus patternIII cannot lift.

For patternIV put x=(r²)^a. It would give [x,r]=r^e with e≡4 mod8,
so r^x=r^(1-e). The unit1-e≡5 mod8 has order m/4 modulo m: the elementary
binomial induction gives v2((1-e)^(2^j)-1)=j+2. However
x^(m/8)=(r^(m/4))^a belongs to A, because r^(m/4) belongs to A and A is
normal. It must centralize r, contradicting that unit order. PatternIV also
cannot lift.

In patternsI andII, [a,r⁴] belongs to A. Therefore conjugation by a sends
r⁴ to r^(4-8j), an odd power of r⁴. Hence M=<r⁴> is normal in G.
The quotient G/M is a marked {4,4} group of order128. The Gaussian-lattice
argument from Section3 now has index16 and gives the unique lattice4Z².

Set N=<d,r>. The identities r^a=d r, d^a=d, r^c=r^(-1), d^c=d^r show
that N is normal. Its index is4: the quotient is generated by commuting
involutions aN,cN, and their independence follows modulo the Frattini
subgroup, where N has image spanned by rΦ(G). The normal cyclic group M
is central in N, because d is a commutator and r centralizes its own powers.

In the affine quotient modulo4Z² the conjugates d_i=d^(r^i) have linear
part −I and translation parts (0,0),(0,2),(2,2),(2,0), for i=0,1,2,3.
They generate an elementary abelian group of order8, with
d3=d0 d1 d2. Upstairs, therefore, every [d_i,d_j] lies in central M and
has order at most2. Write [d0,d1]=z^β. Invariance under r gives
[d1,d2]=z^β. Since d3=d0 d1 d2 u for some central u∈M,
invariance also gives

    [d1,d2]=[d2,d3]=[d2,d0][d2,d1],

forcing [d0,d2]=1. Thus (d0 d1 d2)²=1; the fact that d3 is an involution
forces u²=1, so u=z^ν. These are exactly the two binary parameters of the
third extension model. Conjugating once more gives d4=d0. Consequently
<d_i,z> has precisely the16 normal forms of Section4, and its central
product with <r> has order8m. The commuting involutions a,c form a
complement of order4, with their actions forced by r^a=d0r and r^c=r^-1.
This identifies G with exactly one of the four displayed models. No further
induction, lift enumeration, or order1024 census is needed.

## 6. The source presentations are exactly these models

The preceding classification identifies actual groups of the stated order.
To avoid silently substituting a finite quotient for one of the source's
bare presentations, the following order upper bounds identify those
presentations too. Write P for one such presentation, and z=r^(m/2).
Initially z is an element of order at most2; the constructed model will
show its order is exactly2.

For G1,G2 the extra relation is [d,c]=z^ε. If ε=1, a centralizes z because
it centralizes both d and c; b,c centralize z because they invert r.
If ε=0, d is central. In either case the relations collect into the first
model, with at most8m elements. The model is a quotient with exactly8m,
so the presentation has that order and equals it.

For G3,G4, write d_i=d^(r^i). The extra relation gives d2=d0 z^ε.
If ε=0, applying a and using d1^a=d1 immediately forces [d0,d1]=1.
Suppose ε=1. Since [d0,r²]=z and z²=1, conjugation by d0 inverts z and
therefore fixes it. Thus z commutes with r and every d_i. Put
j=[d0,d1]. Applying a to d2=d0z gives z^a=jz. Since a fixes d0,d1,
it fixes j, and a²=1 forces j²=1. The two involutions d0,d1 therefore
centralize j. Before using j²=1, the identity is j^r=[d1,d2]=[d1,d0z]=j^(-1);
it now gives j^r=j. Conjugation
by c exchanges d0,d1, and also fixes j. Hence j is central. Collecting
the four conjugates of d0 gives

    (d0r)^4=j r⁴.

Since m/8 is even, z^a=(d0r)^(m/2)=z, so j=1. In both cases the second
model's abelian D and its cyclic shift relations follow, giving at most16m
normal forms. The model supplies16m, proving equality with G3 or G4.

For G5–G8, put w=[a,r²]. The relations are w²=z^β and [a,r⁴]=z^ν.
If β=1, conjugation by a inverts w, so it fixes z=w²; if ν=1, conjugation
by a inverts [a,r⁴], so again fixes z. If both are zero, a centralizes r⁴
and hence z. Thus z is central in every case. The second relation then
makes M=<r⁴> normal, of order at most m/4. Modulo M the presentation is
the affine group W=[4,4] with the additional relation [a,r²]²=1. In its
explicit affine action [a,r²] is translation by (−2,0), so this relation
and its conjugates kill exactly4Z². The quotient has order128, and

    |P| <= 128(m/4)=32m.

The constructed model has order32m and satisfies every defining relation.
Therefore P has exactly that order and is the model. This also supplies
the source's presentation-order and IP conclusions without its long
permutation representation graphs.

## 7. Universal checks and precise certificate scope

The formulas for A,C are all-parameter identities, not extrapolations from a
computer run. On D, check the at most three involution relations, the three
displayed commutators, and the images under T. These give T⁴=1 and
A T(x)=T(A(x)^d0), C T(x)=T^(-1) C(x). Thus r↦d0r and r↦r^-1 respect the
semidirect product. Their respective fourth powers satisfy

    (d0r)^4=r⁴                 in branches1 and2,
    (d0r)^4=r⁴ z^ν            in branch3.

Because m is divisible by32, these identities preserve both r^m=1 and
r^(m/2)=z. The formulas on r,d0 show A²=C²=1 and AC=CA. This proves
the asserted automorphisms for every admissible m.

The independent exact script phase3_extension_check.py verifies all eight
models at n=10, including every multiplication triple in D, every pair for
each T, and every one of131072 homomorphism-pair checks for A,C per model.
It then constructs all1024 elements, verifies generation, the pair orders,
and the parabolic intersection. All eight pass. These computations check
the models and formulas; the preceding written argument proves all m.

The retained structural inputs in the completed branches are Lucchini's
cyclic-core theorem, the Burnside basis theorem, the explicit affine [4,4]
normal form already proved in phase2, and the Euclidean algorithm for Z[i].
The third branch additionally retains the complete SmallGroups library at
order256 and its independently executed marked-triple census. No larger
finite2-group census is used. Together with the all-parameter existence proof
in compression_phase2.md, this recovers both principal Theorems1.2 and1.3 of
L035. It is a reduction with explicit structural and finite catalogue inputs,
not a claim that every group classification follows from vector-space linear
algebra alone.
