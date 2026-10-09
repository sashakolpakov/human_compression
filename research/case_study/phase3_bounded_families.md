# Fixed-excess classifications as finite linear-congruence quotients

This gives a general theorem behind the eight-family reduction in
phase3_classification.md. It proves a bound independent of the long edge
order, and a uniform classification procedure using a finite list of
quotients and linear congruences of fixed dimension. It does not prove that
the number of families eventually stabilizes, or establish priority for
these consequences of cyclic cores and group extensions.

## 1. Exact classification by an affine solution module

Fix s>=3. Put

    l=2^(s-2),   h=2^(2s-2).

Let t>=s-1, k=t-s+2 and n=2^k. Consider marked rank-three string C-groups
(G;a,b,c) of order2^(t+s) and type {4,2^t}. Isomorphisms preserve the three
ordered generators. Their canonical subgroup

    A=<(bc)^l>

is cyclic of order n and normal, and Q=G/A is a marked string C-group of
order h and type {4,l}. This is the bounded-core theorem already proved
in phase3_classification.md, using Lucchini's cyclic-core bound in the
index-two rotation subgroup. The degenerate second parameter l=2 when
s=3 is deliberately included.

Identify A additively with R=Z/nZ by identifying the canonical generator
η=(bc)^l with1. Fix one marked quotient (Q;ā,b̄,c̄). Its action on A is
determined by

    ρ(b̄)=ρ(c̄)=−1,     ρ(ā)=u,     u²=1 in R*.

There are at most four possibilities for u. For k>=3 they are
1,−1,1+2^(k-1),−1+2^(k-1); for smaller k remove repetitions and nonunits.
Keep only choices extending to a homomorphism ρ:Q→R*. This is a finite
test on the fixed quotient. Every coefficient below is now specified.

The unknowns are a normalized function f:Q×Q→R and three shifts x_a,x_b,x_c.
Normalization means f(1,g)=f(g,1)=0. Impose the linear cocycle equations

    ρ(g)f(h,j)−f(gh,j)+f(g,hj)−f(g,h)=0.             (1)

On R×Q define multiplication by

    (x,g)(y,h)=(x+ρ(g)y+f(g,h),gh).                 (2)

Normalization gives identity (0,1), and (1) is exactly associativity.
Thus (2) is an extension group E_f with cyclic kernel R and prescribed
action; inverses exist by the usual one-step solution in R×Q. Put

    a=(x_a,ā), b=(x_b,b̄), c=(x_c,c̄).

Impose these six further equations in E_f:

    a²=b²=c²=(ac)²=(ab)^4=1,    (bc)^l=(1,1).       (3)

They are affine linear equations in f and the shifts. Indeed, while a
word is evaluated, its successive Q-coordinates are already known.
Each multiplication adds one scalar multiple of a marking shift and
one value f(g,h); no two unknowns are multiplied. All words in (3) have
length bounded in terms of s alone. The only nonzero constant is the
kernel coordinate1 in the final equation.

Let S_(Q,ρ,k) be the resulting affine solution module. It has at most
h²+3 coordinates, or (h−1)²+3 after normalization. The cocycle and word
equations form a linear-congruence system over Z/2^kZ, of dimension
independent of t. This is arithmetic over a finite ring, not ordinary
Gaussian elimination over a field; integer Smith forms or exact modular
linear algebra are appropriate.

Every solution gives a group of the required order and type, with IP.
The last equation in (3) puts all of the kernel in <a,b,c>; their images
generate Q, so they generate E_f. Since b̄c̄ has order l and (bc)^l has
order n, bc has order nl=2^t. The image of ab has order4, and (3) gives
order exactly4 upstairs. The left dihedral parabolic <a,b> therefore
maps injectively to its quotient, whereas <b,c> contains the full kernel.
An element of their intersection projects into <b̄>; injectivity on
<a,b> makes the intersection exactly <b>. This proves rank-three IP,
including independence. No incidence-graph search remains.

Conversely, choose a section of any group in the stated class. Multiplying
section elements gives a normalized f satisfying (1), and expressing its
marked generators in those coordinates gives a solution of (3). Thus the
construction is exhaustive.

## 2. Linear equivalence, and an exact counting formula

Let v:Q→R be any normalized1-cochain, v(1)=0, and put

    δv(g,h)=v(g)+ρ(g)v(h)−v(gh).

Changing section gives the equivalence

    (f,x_a,x_b,x_c)
       ~ (f+δv, x_a−v(ā), x_b−v(b̄), x_c−v(c̄)).    (4)

The isomorphism on coordinates is (x,g)↦(x−v(g),g). It fixes the kernel
generator and quotient pointwise. Conversely every such extension
isomorphism has this form. An isomorphism of marked groups necessarily
fixes the canonical kernel generator (bc)^l and induces the unique
marking-preserving identification of the chosen quotient. Therefore (4)
is exactly marked group isomorphism, not merely a sufficient equivalence.

This linear gauge action is free on S. A stabilizer v has δv=0 and
v(ā)=v(b̄)=v(c̄)=0. The derivation identity
v(gh)=v(g)+ρ(g)v(h), together with generation of Q by the marking, forces
v=0 everywhere. Consequently the exact number of marked isomorphism
classes for the fixed quotient and action is

    |S_(Q,ρ,k)| / n^(h−1).                         (5)

If nonempty, S is a coset of the kernel of its homogeneous linear system.
Hence the number in (5) is a power of2. More intrinsically, the classes
form an affine space over a finite abelian2-group: the homogeneous
solution module divided by the image of the normalized1-cochains.
This is an affine module over Z/2^kZ, not necessarily a vector space.

Thus the entire classification is obtained from at most four fixed-size
affine systems for each member of a finite quotient catalogue. The
catalogue is an explicit retained input; obtaining it may require genuine
finite-group classification or enumeration. The extension arithmetic
after it is supplied is linear.

## 3. A uniform bound independent of t

Let N_s be the number of marked isomorphism classes of quotients Q of
order h and type {4,l}. Then the number of marked groups G under
consideration is at most

    C_s = 16 l N_s h^(h²),                         (6)

independently of t. One completely numerical, very crude replacement is
N_s<=(h!)³, obtained by putting the three quotient generators in their
regular permutation representation on h points. Thus (6) is an explicit
bound depending only on s, even without an available quotient catalogue.

Here is a proof that does not assume eventual stability of cohomology.
For one fixed Q-action, equivalence classes of extensions with a specified
kernel generator are H²(Q,R), by the section calculation above. This
group has exponent dividing h. In fact, if f is a cocycle and
b(g)=sum_(x∈Q) f(g,x), summing (1) over its final argument gives

    h f(g,j)=ρ(g)b(j)−b(gj)+b(g)=δb(g,j).

Also the cocycle group is a subgroup of (Z/nZ)^(h²), so it needs at most
h² abelian generators. An elementary proof projects onto one coordinate,
lifts a generator of the cyclic image, and proceeds inductively on the
kernel. Its quotient H² needs no more generators. Since its exponent
divides h, its order is at most h^(h²), uniformly in k.

It remains to bound marked lifts within one extension. Fix reference
lifts a0,b0,c0. Write potential lifts as η^x a0, η^y b0, η^v c0.
Conjugation by η^w changes y by−2w, because b0 inverts the kernel.
Thus every marked isomorphism class has a representative with y=0 or1.
Since b0c0 centralizes the kernel, the equation (bc)^l=η is a single
congruence

    l(y−v)+constant = 1 modulo n.

For each y it has at most gcd(l,n)<=l solutions v. Finally the relation
ac=ca is a congruence of the form

    2x=(1−u)v+constant modulo n,

which has at most two solutions x. Other relations only remove choices.
Therefore each extension has at most4l marked lift classes. Multiply by
the at most four actions, h^(h²) extension classes, and N_s quotients to
obtain (6).

## 4. What this does and does not unify

For s=3 the finite quotient is D8×C2. For s=4 it is the unique square-grid
quotient of order64. For s=5 the bounded order256 census in
phase3_classification.md supplies the finite relation patterns. The
explicit binary models there solve the corresponding extension problems
and additionally give short, closed presentations. The theorem above
explains why a fixed finite amount of extension data suffices for every
larger long-edge exponent, rather than supplying a new opaque seed at
each order.

The independent [linear-system checker](phase3_cocycle_linear_check.py)
implements the s=3 quotient D8×C2 with3381 equations in228 unknowns.
It solves over Z/2^kZ for k=3,4,6,8 and every u²=1 action. Exactly the
actions u=1 and u=1+2^(k−1) have solutions; each has2^(15k) solutions,
and hence one marked class after dividing by the free gauge group of
that order. The other two actions have no solution. All cases pass,
as do144 independent brute-force checks of the modular solver on small
systems. The [saved result](phase3_cocycle_linear_check.json) uses exact
integer arithmetic and enumerates no upstairs groups. These finite checks
corroborate the framework; they are not a proof of stabilization or an
all-k count.

The bound alone does not prove that the counts eventually become constant.
It does not exhibit a parameter-free list of group presentations for every
s, or remove the quotient catalogue. The finite systems vary through the
ring Z/2^kZ and the possible high-bit units1±2^(k−1). Establishing eventual
stabilization would require another argument about those varying systems.

## 5. Extension to more involutory generators

A weaker core bound removes the rank-three restriction. Fix d>=3 and s>=2.
Consider groups of order2^(t+s) generated by an ordered list of d
involutions, with b,c the final two, |bc|=2^t, and every earlier generator
commuting with c. This includes every string C-group whose final pair has
the stated order. Assume t>=s and put

    L=2^(s−1), H=2^(2s−1), k=t−s+1.

Apply Lucchini directly in G, rather than in its rotation subgroup. The
canonical A=<(bc)^L> is normal cyclic of order2^k and G/A has order H.
The image of bc in the quotient has order exactly L.
For a fixed marked quotient its action on A has at most4^(d−2)
possibilities: b,c invert A, and every other involution acts by a unit
whose square is1. Let N_(s,d) be the finite number of possible marked
quotients of order H.

The extension count is at most H^(H²). Normalize the b-shift modulo2 as
before; there are at most L c-shifts compatible with (bc)^L=η. Commutation
with c leaves at most two choices for the shift of each of the other
d−2 generators. Hence the number of such marked groups is at most

    4^(d−2) · 2^(d−1) · L · N_(s,d) · H^(H²).       (7)

In particular the number of string C-groups in this larger class is
uniformly bounded as t grows. All prescribed involution, commutation,
and fixed-word relations are again affine linear equations in a cocycle
and d marking shifts, and the gauge action is free because the quotient
marking generates. The quotient need not itself retain IP in this general
rank. Thus the entire affine solution module must not be called a polytope
classification without an IP test. The next section gives that test using
only bounded finite quotients and one-dimensional cyclic arithmetic. The
rank-three theorem of Section1 avoids it by its injective left parabolic.

## 6. Exact IP filtering without constructing the large group

For completeness, the general-rank extension models admit a bounded
arithmetic intersection test even when their finite quotients fail IP.
Let E_f=R×Q be a candidate with marked involutions x_1,...,x_d. For a
subset I of indices, write H_I=<x_i:i∈I> and let Q_I be its image in Q.
The finite group Q_I is computed inside the fixed quotient. Choose, by a
spanning tree of its Cayley graph, a word for each q∈Q_I, and evaluate its
lift as g_(I,q)=(α_I(q),q), choosing g_(I,1)=1.

Schreier's subgroup argument says that H_I∩A is generated by the kernel
elements

    g_(I,q) x_i g_(I,q q_i)^(-1),   q∈Q_I, i∈I.

There are at most H d of them. Read their coordinates ξ_(I,q,i) in R and put

    d_I=gcd(n, all ξ_(I,q,i)),

where gcd(n,empty)=n. Then H_I∩A is exactly the subgroup of multiples of
d_I in R, and the fiber of H_I above q is

    { (x,q) : x≡α_I(q) modulo d_I }.              (8)

This follows directly from the Schreier generators and from multiplying a
chosen lift by all kernel elements. It does not require H_I normal in E_f.

Therefore H_I∩H_J=H_(I∩J) holds if and only if both of the following hold:

1. d_(I∩J)=lcm(d_I,d_J);
2. for every q in (Q_I∩Q_J)\Q_(I∩J),
   α_I(q) is not congruent to α_J(q) modulo gcd(d_I,d_J).

Indeed two fiber congruences intersect precisely when their constants
agree modulo that gcd. If they intersect, their common fiber is one
class modulo the lcm. Over Q_(I∩J), the inclusion H_(I∩J)⊂H_I∩H_J is
automatic, so equality of their kernels already gives equality of those
fibers. Condition2 excludes every additional quotient fiber.

Testing all pairs of subsets proves full IP. The number of quotient
elements, Schreier words and subset pairs depends only on s,d, while all
upstairs calculations are integer arithmetic modulo2^k. Exact generator
and pair orders can be tested similarly: if a word w has quotient order e
and w^e=(ξ,1), then |w|=e n/gcd(n,ξ). Thus neither IP nor type verification
requires enumeration of E_f, whose order grows exponentially with t.

Combined with the finite affine classification and the uniform candidate
bound (7), this gives a complete classification procedure for the stated
general-rank string C-groups, conditional on a finite catalogue of their
marked quotient groups. The affine equations, gauge quotient and cyclic
IP test are explicit. The finite catalogue remains a real input, and
stabilization as t grows remains unproved here.
