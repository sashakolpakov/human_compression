# Independent review of the forced top-layer action

10 October 2026. **PASS.** I read the complete
[supplement](phase13_cyclic_tpp_top_action.md) and its Python checker,
against the retained power-layer and equal-order statements reviewed in
[the preceding audit](phase13_cyclic_tpp_minimality_audit.md).

The subgroup U is the actual highest nontrivial power subgroup of the
normal powerful N=P^8. Equal marked orders and genuine ordered-coordinate
bijectivity give its three independent involutions. It is therefore a
normal elementary abelian subgroup of order eight, including the boundary
e=4 where U=N. This is not inferred from TPP alone.

Every two-group action over F_2 has a nonzero fixed vector and an invariant
complete flag. Hence the image embeds in UT_3(F_2), a dihedral group of
order eight. An order-four linear map on three dimensions is regular
unipotent with a unique nonzero fixed vector. If such a map were a marked
generator action, its own marked involution would be that vector and
therefore fixed by the entire image, contrary to the retained
center-disjointness. Thus all three marked actions have order at most two.

If the image were nonabelian, it would be dihedral of order eight.
Its generating involutions S,T have ST of order four, and both elements
of ST Phi(R) have order four. The relation c in ab Phi(P), together with
surjectivity on Frattini subgroups, places the third action in that coset,
contradicting its already proved order bound. With right-conjugation
operators on column vectors, composition can reverse S and T; this causes
no change because ST and TS have the same coset modulo Phi(R). In the
surviving case the two actions commute exactly.

The order-one and order-two abelian images force a globally fixed marked
coordinate, so the image has order four. Its Frattini subgroup is trivial,
and the action kernel contains Phi(P). Their equal index four makes the
kernel exactly Phi(P), not merely a subgroup containing it.

For the marked uniqueness step, the nontrivial involutions give rank-one
square-zero D=S−I and E=T−I. Distinct image lines would force equal
two-dimensional kernels containing all three marked basis vectors, which
is impossible. A common image line, together with the three individual
fixed-vector conditions and the absence of globally fixed coordinates,
forces the displayed functionals and the line <u+v+w>. Substitution gives
exactly S=(1,5,3), T=(6,2,3), W=(6,5,4), and common fixed vectors 0 and 7.
Thus U∩Z(P)=<uvw>; no conclusion that Z(P) itself is cyclic is made.

I executed unchanged copies of the proof and checker in a fresh temporary
directory. The checker exited zero with no standard error and produced
output byte-identical to the author report. The separate result is
[phase13_cyclic_tpp_top_action_independent_run.json](phase13_cyclic_tpp_top_action_independent_run.json).
It exhausts all 168 matrices in GL_3(F_2), finds 100 eligible two-group
image pairs fixing the first two coordinates, tests 38 third-coset marked
cases, and leaves the one displayed action. Its Frattini calculation uses
all squares and commutators independently of the written dihedral argument.

This is a necessary-condition theorem for an unrestricted minimum
counterexample. The surviving central line contains no marked coordinate,
so there is no contradiction yet. The computation searches no group
extensions or finite-group catalogue, and neither the proof nor the check
settles the full cyclic-TPP conjecture. The earlier declared dependencies
remain retained; no new primary-source reading, complete formalization,
external peer review or priority determination is claimed.
