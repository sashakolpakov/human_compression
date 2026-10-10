# Cyclic TPP with abelian Frattini subgroup: every prime

10 October 2026. Written extension of the
[binary argument](phase11_abelian_frattini.md). Independent internal review
is in progress. No publication-priority claim is made.

## 1. Statement

**Theorem.** Let G be a finite nilpotent group whose Frattini subgroup is
abelian. If cyclic subgroups A,B,C have the triple product property

    abc=1, a∈A, b∈B, c∈C  implies a=b=c=1,

then |A||B||C|≤|G|.

For p=2 the proof is the complete binary square-action argument in the
companion note. Here we prove the result for every odd prime p, using
only elementary finite-p-group facts and three-dimensional linear algebra.
The nilpotent statement then follows by direct products of Sylow subgroups.
This neither asserts the inequality for arbitrary subgroup triples nor
settles it for every finite p-group.

## 2. The reduction for a general prime

Fix a prime p and choose a counterexample P of minimum order among finite
p-groups with abelian Frattini subgroup. This class is closed under subgroups
and quotients: Φ(H)=H^p[H,H]≤Φ(P), and Φ(P/N)=Φ(P)N/N.

Exactly as in the binary proof, a central subgroup of one cyclic factor
can be quotiented out without changing the violation ratio. A proper
pair-generated subgroup reduces the problem by induction and the injection
of cosets of C∩H in C into cosets of H in P. These reductions give

    A∩Z(P)=B∩Z(P)=C∩Z(P)=1,
    ⟨A,B⟩=⟨A,C⟩=⟨B,C⟩=P.

Thus P/Φ(P)≅C_p², and the three cyclic generators have distinct nonzero
projective directions in this quotient. In particular all factors are
nontrivial. Write their violation ratio as r=|A||B||C|/|P|, a power of p.
If r≥p², take the maximal subgroup corresponding to A's direction.
The triple A,B^p,C^p lies in it, retains TPP, and has violation ratio
r/p>1, contradicting minimality. Consequently

    |A||B||C|=p|P|.                                    (1)

All factors have order at least p². To see this, write α≥β≥γ for their
orders. The subgroup of order p in A cannot be normal: conjugation by a
p-group on a normal group of order p is trivial, whereas A avoids Z(P).
Choose a conjugate A^g with a different order-p subgroup. Then A∩A^g=1.
A maximal subgroup containing A is normal in P and contains A^g, whence
α²≤|P|/p. Equation (1) gives p²α≤βγ, and therefore γ≥p².

Set K=Φ(P), an abelian group. The triple A^p,B^p,C^p still has TPP,
so its multiplication homomorphism into K has trivial kernel. By (1),
its image has order |P|/p²=|K|. We obtain the actual direct product

    K=⟨x⟩×⟨y⟩×⟨z⟩,
    x=a^p, y=b^p, z=c^p,                              (2)

with all three factors nontrivial. Their images x,y,z form a basis of
V=K/pK, a three-dimensional vector space over F_p. This conclusion uses
the abelianness of K, rather than numerical equality alone.

## 3. The norm identities for conjugation

Use right conjugation, and let S,T be the automorphisms of K induced by
a,b. They commute and have order dividing p, because a^p,b^p,[a,b] lie
in the abelian K. They fix x and y respectively. Put

    d=[b,a]=b⁻¹a⁻¹ba∈K.

Then a^b=ad⁻¹ and b^a=bd. Write K additively. Raising these identities
to the p-th power gives

    (T−I)x=−(I+S+⋯+S^(p−1))d,
    (S−I)y= (I+T+⋯+T^(p−1))d.                        (3)

The same identities hold on V. In characteristic p, the polynomial identity

    1+X+⋯+X^(p−1)=(X−1)^(p−1)

turns the two norms into (S−I)^(p−1) and (T−I)^(p−1).
We will show that both vanish whenever p is odd. Notice that the odd-prime
argument does not need the additional formula for c^p; the binary case
does need its square compatibility and is handled separately.

## 4. Odd primes: the two named coordinates are fixed

Write N=S−I and M=T−I. They are commuting nilpotent operators on V,
since N^p=M^p=0. Their nilpotency indices are at most three.

If p≥5, then N^(p−1)=M^(p−1)=0 immediately. Equation (3) now says
Tx=x and Sy=y. Both maps therefore fix x and y.

For p=3 we must also rule out a single Jordan block of length three.
Suppose N²≠0. Choose v with N²v≠0. The vectors v,Nv,N²v form a basis:
applying N² and then N to any proposed linear relation proves independence.
Every operator commuting with N is a polynomial of degree at most two
in N, because its value on v determines its values on this basis. Hence

    T=I+αN+βN²

for α,β∈F_3; the constant coefficient is one because T is unipotent.
Also ker N is one-dimensional and equals ⟨x⟩, since Nx=0 and x≠0.
If α≠0, then αI+βN is invertible, and
ker(T−I)=ker N. This would put y in ⟨x⟩, contradicting their independence.
Thus α=0, and M²=0. The second equation (3) then gives Ny=M²d=0,
again contradicting the independence of x,y. We conclude N²=0.
Interchanging S,x and T,y proves M²=0 as well.

Thus for every odd prime p the two norms vanish, and

    Sx=Tx=x,  Sy=Ty=y.                                (4)

The maps are unipotent on the one-dimensional quotient
V/⟨x,y⟩, so their induced maps there are the identity. Consequently

    Sz−z, Tz−z∈⟨x,y⟩.                                (5)

This is a statement about the reduction of the actions modulo pK.
The next step explicitly lifts it to actual elements of K.

## 5. A central element in one cyclic factor

Let the three factors in (2) have orders p^r_x,p^r_y,p^r_z, with all
exponents positive, and put r=max(r_x,r_y,r_z). For a generator w of
a factor of maximal order p^r, the image of p^(r−1)w under an
automorphism of K depends only on the coefficients modulo p in factors
of that same maximal order. Terms in shorter factors and coefficients
divisible by p in maximal factors vanish after multiplication by p^(r−1).

If x or y has maximal order, choose that generator w. Equation (4)
shows its element p^(r−1)w of order p is fixed by S,T. If neither does,
then z has strictly larger order than both x and y. Choose w=z;
equation (5) shows that every possible correction is in a shorter factor
modulo pK, and again p^(r−1)z is fixed by S,T.

In each case this is a nonidentity element of A, B or C commuting with
a,b, hence with P=⟨a,b⟩. This contradicts the center-free reductions.
The odd-prime theorem follows. Together with the binary companion proof,
it establishes the p-group result for every prime. ∎

## 6. Nilpotent products and precise coverage

A finite nilpotent group is the direct product of its Sylow subgroups,
and its Frattini subgroup is the product of their Frattini subgroups.
A cyclic subgroup likewise splits into its Sylow subgroups. Restricting
the three factors to any Sylow subgroup preserves TPP. Apply the p-group
theorem there and multiply the inequalities over the primes to obtain
the theorem of §1.

For the hypertope order conjecture, this includes the entire structural
class in which the derived 2-group has abelian Frattini subgroup, with
no bound on order or nilpotency class. The binary companion records
the geometric reduction and the source target. The odd-prime extension
also places that consequence inside a wider group-theoretic theorem.

No subgroup classification, finite group catalogue or bound on the
number of groups of a given order is retained. Standard finite-p-group
Frattini facts, the elementary linear algebra explicitly proved above,
and the binary action argument are the dependencies. Finite diagnostics
and any partial Lean certificate must be distinguished from a complete
formal proof of this nilpotent-group statement. Historical priority and
the unrestricted cyclic-TPP problem remain unverified/unresolved here.
