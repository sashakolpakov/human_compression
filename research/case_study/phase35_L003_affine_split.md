# The compact affine extension splits

This supplement leaves the frozen compact construction unchanged. Its only new input is a common fixed point modulo 2.

Use the four maps \(r_i(a)=M_i a+b_i\) and the group \(\Gamma\) of [the compact model](phase35_L003_affine_model.md). Let
\[
t=(1,0,1,1,0,0)^{\mathsf T}.
\]
Direct substitution gives
\[
\begin{array}{c|c|c}
i&b_i+M_it-t& (b_i+M_it-t)/2\\ \hline
0&(-2,0,0,0,0,0)&(-1,0,0,0,0,0)\\
1&(0,0,0,0,0,0)&(0,0,0,0,0,0)\\
2&(0,0,-2,0,0,0)&(0,0,-1,0,0,0)\\
3&(0,0,-2,-2,0,0)&(0,0,-1,-1,0,0).
\end{array}
\]
Thus every generator preserves the affine lattice \(t+2\mathbb Z^6\). Make the rational affine change of coordinates \(a=t+2c\). The new maps on \(c\) have linear parts \(M_i\) and the integral offsets in the final column.

The previously proved kernel \(2\mathbb Z^6\) becomes the full translation group \(\mathbb Z^6\). Write \(\widehat\Gamma\) for the changed-coordinate group. Every element is an integral affine map \((M,v)\), with \(M\in Q\). For every \(M\in Q\), some such element belongs to \(\widehat\Gamma\); composing on the left with translation by \(-v\), which already belongs to the group, gives \((M,0)\). Consequently
\[
\widehat\Gamma=\mathbb Z^6\rtimes Q,
\qquad \Gamma\cong\mathbb Z^6\rtimes Q,
\tag{1}
\]
where \(Q\) is the explicit integral linear group of order 1296, acting by the displayed six-dimensional matrices.

This is a direct proof of splitting, not an inference from the order or an extension-class assumption.

For every integer \(m\geq1\), the frozen compact proof identifies the kernel of reduction modulo \(2m\) as \(2m\mathbb Z^6\). The coordinate change carries this subgroup to \(m\mathbb Z^6\), and therefore
\[
H_m\cong (\mathbb Z/m\mathbb Z)^6\rtimes Q.
\tag{2}
\]
The marked identification with the old family gives the same statement for \(G_m\). In these coordinates, its distinguished generators are exactly the four pairs \((M_i,(b_i+M_it-t)/2)\), reduced in the translation coordinate modulo \(m\).

The \(Q\) factor in (2) remains the **abstract integral group** of order 1296. It is not replaced by its possibly smaller matrix image modulo \(m\). In particular \(m=1\) gives \(Q\), not the trivial permutation action on a one-point lattice. The semidirect product need not act faithfully on \((\mathbb Z/m\mathbb Z)^6\) through its usual affine action for every \(m\); the original action modulo \(2m\) is the faithful model retained by the construction.

The accompanying standard-library checker performs the four exact integer substitutions and binds the compact matrix source and its saved report. The group-theoretic step is the written argument above; the already frozen kernel computation is retained, not silently repeated.

    python3 phase35_L003_affine_split_check.py --output /tmp/affine-split-fresh.json

No identification of \(Q\) as a wreath product is used here, and no splitting of a universal source group is asserted. The separate unfilled universal group is not virtually solvable, whereas this group is virtually abelian.
