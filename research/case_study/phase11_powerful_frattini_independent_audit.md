# Independent audit: the powerful-Frattini obstruction

10 October 2026. Private internal review by the survey-audit agent.
**PASS: no mathematical gap found** in
[phase11_powerful_frattini.md](phase11_powerful_frattini.md), conditional
on its explicitly retained powerful-group theorems. This is not external
peer review, a publication-priority determination, or a formal proof.

## Retained source checked independently

I independently opened Lubotzky–Mann's primary
[author-uploaded rendered text](https://www.researchgate.net/publication/265533173_Powerful_p-groups_I_Finite_groups),
*Powerful p-groups. I. Finite groups*, Journal of Algebra 105 (1987),
484–505, [DOI](https://doi.org/10.1016/0021-8693(87)90211-0).
The relevant selections are printed pages 486–490 and 499–501.

Theorem 1.11's forward proof explicitly handles an arbitrary generating
list, not merely the existence of some suitable basis. Theorem 4.1.11
states the corresponding ordered-product conclusion for the given list
at p=2. Corollary 1.9 and Proposition 4.1.9 give generators for the power
subgroups. Theorems 1.3 and 4.1.3 give power iteration. Theorems 1.1 and
4.1.1, with Corollaries 1.2 and 4.1.2, supply the powerful-embedding
properties used in the argument. The source's fourth-power definition at
p=2 matches the note.

Access was to the author-uploaded rendered primary text. No locally
verified PDF hash is claimed. I did not read or audit every theorem of
that paper, and no third-party source text is copied into this artifact.

## Induction and the unconditional generator bound

Theorem A takes a minimum counterexample among all finite p-groups, so
every smaller subgroup or quotient needed by the argument is admissible.
Theorem B instead uses the stated hereditary condition. Subgroups preserve
that condition directly. For a subgroup H/N of a quotient P/N, its
Frattini subgroup is Φ(H)N/N, a quotient of the powerful group Φ(H);
powerfulness survives this quotient by its defining commutator containment.
Thus the minimum-counterexample reductions are justified for both theorems.

The previously audited elementary reductions give ratio p, distinct
projective Frattini directions, center-free cyclic factors and minimum
factor order p². They do not require an abelian kernel up to this point.
The p-th-power cyclic factors X,Y,Z have TPP and order product |Φ(P)|.
If they generated a proper subgroup H of Φ(P), that exact triple would
violate the inequality in H, a smaller admissible group. Consequently
they generate Φ(P) without assuming powerfulness. This establishes the
claimed unconditional bound d(Φ(P))≤3.

## Ordered coordinates and the dimension-three conclusion

Under the additional powerfulness assumption, the retained theorem supplies
actual surjectivity X×Y×Z→K in the prescribed order. The domain has exactly
|K| elements, so this specific map is bijective. This is materially stronger
than numerical equality plus TPP alone, which would not justify injectivity.

The retained power-generator theorem gives generators x^p,y^p,z^p of K^p,
and the same ordered-product theorem applies again. Restricting the already
injective original multiplication map to X^p×Y^p×Z^p remains injective.
Each original factor is nontrivial, so each drops in order by p. Therefore
|K:K^p|=p³ exactly. Since Φ(K)=K^p for powerful K, the three distinguished
images form a basis of K/K^p. No minimality of the original generating
list was silently assumed in invoking the source theorem.

## Graded power maps, including the even prime

For L=K^(p^i), the retained iteration identity identifies L^p and L^(p²)
with the next two displayed layers. For odd p, L/L^(p²) has class at most
two: its derived subgroup lies in L^p/L^(p²), which is central and has
exponent dividing p. The class-two product-power formula therefore makes
the p-th-power map multiplicative modulo L^(p²). At p=2, the powerful
definition makes L/L⁴ abelian, which directly gives the required square
congruence. There is no appeal to an arbitrary nonlinear power map being
a homomorphism.

Elements of L^p have p-th powers in L^(p²), so the map is well-defined
on L/L^p. Its image contains all the p-th powers generating the target;
as a homomorphic image, it is the whole target. The groups at each layer
are elementary abelian, making these maps linear. They are characteristic
power constructions and hence equivariant under every automorphism of K.

Their composition is the stated top-power map, since iterating the group
power operation gives the indicated p^(r−1)-th power of the original
element. The exponent is exactly p^r: the retained power-generator theorem
kills K^(p^r), and a named generator attains this order. Thus the top
target is elementary abelian and the map has a nonzero coordinate image.
The r=1 case is valid separately: powerful exponent-p groups are abelian,
so the displayed identity map has the required properties.

## Transporting the action obstruction

K^p is characteristic in K and normal in P. In P/K^p its image is abelian,
so the previously audited norm identities apply without treating K itself
as abelian. The actions of a and b on K/K^p commute and have p-th powers
equal to the identity because their relevant inner automorphisms act
trivially on this quotient. At p=2 the extra c=abf square compatibility is
available; at odd p the already proved norm argument needs no such formula.

The top-power map is equivariant for these same conjugations. In the odd
case, a nonzero image of x or y is fixed; if both images vanish, the image
of z is nonzero and its corrections vanish. In the binary case, either
the actions are trivial or their correction line is a fixed coordinate.
A nonzero image of that line is fixed; if the line maps to zero, all
corrections vanish and another nonzero coordinate image is fixed.

The resulting fixed element is an actual nonidentity power of x, y or z,
and hence lies in an original cyclic factor. It commutes with both
generators of P, contradicting the center-free reduction. This completes
both stated theorems under the retained input.

## Scope retained

The argument does not establish subgroup closure for the larger condition
that Φ(P) alone is powerful. It therefore does not prove the inequality
for every group satisfying only that condition. Its uniform class is
explicitly hereditary; its minimum-counterexample obstruction is a separate
statement. The note correctly retains this distinction. It invokes neither
a group catalogue nor a classification of finite p-groups. No new finite
census or Lean execution was performed for this audit.
