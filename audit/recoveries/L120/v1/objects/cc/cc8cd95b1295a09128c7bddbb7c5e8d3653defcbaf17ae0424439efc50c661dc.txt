# An exact rank-four representation of PSU4(11)

10 October 2026. Original finite phase-fifteen construction. This is a single-group certificate, not a uniform theorem or a publication-priority claim.

In $E=\mathbb F_{11}[i]$, $i^2=-1$, take $t=2,x=9,y=2$, so $t^2+x^2+y^2=1$. Set $a=2i$, $b=9+2i$, $c=-9+2i$ and use the four matrices of [the sphere template](phase15_unitary_generation.md). Their projective images generate a rank-four string C-group of type $\{4,60,10\}$ for $\operatorname{PSU}_4(11)$.

The [standalone GAP checker](phase15_unitary_example_check.g) verifies determinant one and preservation of the identity Hermitian form. It constructs the orbit of a totally isotropic two-space. The orbit has 15984 elements, exactly the standard number $(q+1)(q^3+1)$ of maximal totally isotropic two-spaces in dimension four. The four induced permutations generate a group of order

$$11^6(11^2-1)(11^3+1)(11^4-1)/4=1036388695478400.$$

The scalar center of SU4 has order four and fixes every plane. Thus the permutation action is a quotient of the generated projective subgroup, which is contained in PSU4. Equality with the displayed PSU4 order forces the projective subgroup to be the whole PSU4 and makes its induced action faithful. This is an order sandwich using explicit matrices; no simple-group recognizer or presumed faithful action is required.

The checker verifies that all four induced generators are involutions, that distant generators commute, and that adjacent products have orders 4,60,10. It constructs the 16 subgroups indexed by all subsets of the four marked generators. For every ordered pair of subsets $I,J$, it calculates and compares the actual permutation-subgroup intersection with the subgroup indexed by $I\cap J$. All 256 equalities pass. Thus the full intersection property is checked directly.

The retained inputs are exact GAP finite-field and permutation-group arithmetic and the standard unitary group-order formula. The auxiliary rank-one order-greater-than-five generation criterion is not applied here. The symbolic identities and the general proof remain separate evidence. The checker writes no files itself; the accompanying log records its fresh execution.
