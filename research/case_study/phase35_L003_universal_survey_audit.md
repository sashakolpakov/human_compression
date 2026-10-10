# Written review of the universal-family consequence and source scope

Date: 2026-10-10. Reviewer: `survey_audit`. Result: **PASS**. This is a complete written review of `phase35_L003_all_universal.md` and `phase35_L003_problem92_scope.md`, bound to the final author versions in the companion JSON. No new executable claim or current-literature search is made.

## The universal-group argument

The six-relator presentation of the Coxeter group's even subgroup matches the source rotational presentation. In particular the Coxeter relation on $r_1r_3=x^{-1}z$ is equivalent to the displayed relation on $zx$, because these words are inverses, and the analogous observation applies to $r_2r_3$. The distinguished involution conjugates each of $x,y,z$ to its inverse; this means the generator-defined automorphism, not inversion of every arbitrary group element.

I checked the local-lattice argument excluding hidden rotational relators. With the displayed matrices $R$ and $S$, both $a\mathbb Z^2$ and $a\langle(1,1),(-1,2)\rangle$ are invariant under the rotation and the reflection. Explicitly, $S(1,1)=(1,1)$ and $S(-1,2)=(1,1)-(-1,2)$. These are precisely the two parameter forms needed by all four local residues. The interpretation of the local orientation-preserving normal closure as the corresponding translation lattice is an explicitly retained toroidal-presentation input.

For the local triangle that omits $r_0$, its own reflection $h$ still suffices: $r_0h$ lies in the global even subgroup, and conjugation by $r_0$ factors as local conjugation by $h$ followed by conjugation by that even element. Thus each local relator's global even normal closure is preserved. Their joint normal closure is preserved as well. Since all added relators are even, the sign homomorphism survives and splits through $r_0$. This proves the stated semidirect-product identification with the literal source rotational group; it is not merely a quotient in one direction.

The finite local upper bounds and their attained finite images give actual maximal-parabolic injections in $U_s\to G_s$. They do not require knowing the ambient order of $U_s$. All-maximal-parabolic quotient transport therefore supplies both subgroup IP and typed coset Helly upstairs, even when $U_s$ is infinite. The usual marked coset construction then supplies the regular geometry and full type-preserving automorphism group.

The universality assertion has the correct marked scope. Every competing regular object with the same ordered marked local groups satisfies the Coxeter and four torus words, hence receives the generator-preserving epimorphism. Its local restrictions are isomorphisms because the corresponding finite local groups have the same prescribed order. There is no claim that two finite quotients coincide or that unmarked local isomorphism types alone determine an ambient marking.

Finally, if $6\mid s$, the last relation for $U_s$ holds in $U_6$, giving the required surjection onto the previously certified infinite group. The argument proves infinitude in those cases and makes no extrapolation to the other parameters.

## Literal source interpretation

The source-scope note agrees with my separately recorded primary reading of the end of §8, Table 8 and Problem 9.2. The numbered question asks about an infinite family with the displayed parameter pattern; its wording does not itself include universal finiteness or an explicit universal quantifier over every integer. The preceding paragraph supplies finite-existence context, while the table lists finite universal examples. Keeping those three scopes separate is necessary.

The exact all-integer finite construction is sufficient for that finite-existence interpretation. Its universal extension now supplies actual universal regular geometries as well, with no assertion that all of them are finite. If a family must literally contain the four previously displayed objects, retaining those four source examples and using the new constructions at later parameters is legitimate; the new quotients at the first four parameters need not equal the source groups.

The statement that priority remains unverified is appropriate. In particular, neither this review nor the source-scope note has read the complete theorems of Zhang's 2024 abelian-cover paper. The mathematical consequence must not be promoted to an independently established historical-first resolution on this evidence.

## Dependencies and independence

Retained inputs are the source toroidal presentations/lattice model, the reviewed tensor local and geometric theorems, the separate small-parameter finite certificates, the abstract quotient-transport theorem and the frozen parameter-six infinitude certificate. I authored the retained tensor model and independently reviewed its geometric completion; that involvement is disclosed rather than describing this as an independent reconstruction of every earlier ingredient. The new universal and source-interpretation arguments above were reviewed in full. No author or public file was modified.
