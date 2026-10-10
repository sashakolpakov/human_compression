# Explicit transport on a Hermitian norm shell

This is an additive proof and formalization supplement to the independently reviewed `hermitian_unital_proof.md`. It does not alter that retained manuscript or count its conjecture answer a second time. The formulas below replace the finite counting argument for transitivity and freeness of the special unitary action on its nonzero norm shell. The finite-field interpretation, generation by root groups and the incidence-geometric applications are stated separately.

Let K be a commutative field with an involutive field automorphism σ, written x↦x̄. On K² use the Hermitian form

\[
h((x,y),(u,v))=x\bar v+y\bar u,
\qquad N(x,y)=x\bar y+\bar x y.
\]

For a matrix M=(a b;c d), determinant one together with MᵀJσ(M)=J, where J=(0 1;1 0), is equivalent to

\[
\bar a=a,\quad \bar d=d,\quad \bar b=-b,\quad \bar c=-c,
\qquad ad-bc=1.                                      \tag{1}
\]

Here M acts on column vectors. The equivalence follows by solving the two linear systems in the entries of σ(M), using ad−bc=1. Thus these entry conditions are the actual special unitary equations, not an abstract group with the expected order. They imply N(Mv)=N(v) by direct expansion.

**Transport theorem.** For v,w∈K² with N(v)=N(w)=k≠0, exactly one determinant-one unitary matrix carries v to w. Writing v=(x,y), w=(u,r), it is

\[
T_{w,v}=\frac1k
\begin{pmatrix}
u\bar y+\bar u y & u\bar x-\bar u x\\
r\bar y-\bar r y & r\bar x+\bar r x
\end{pmatrix}.                                      \tag{2}
\]

One derivation puts

\[
B_v=\begin{pmatrix}x&-\bar x\\y&\bar y\end{pmatrix}.
\]

Its determinant is k, and its two columns are orthogonal, of norms k and −k. Hence T_(w,v)=B_w B_v⁻¹ has determinant one, preserves h, and maps v to w. Formula (2) results by multiplying these two matrices. This argument works in characteristic two: the determinant k remains nonzero, so the two columns remain independent even when −k=k.

For uniqueness, a matrix satisfying (1) sends the second column (−x̄,ȳ) of B_v to (−ū,r̄) as soon as it sends (x,y) to (u,r). Its values on the two basis columns are therefore determined. Equivalently, solving the two equations Mv=w together with their σ-conjugates produces exactly (2). The Lean proof follows this latter entrywise calculation, avoiding an implicit appeal to Witt's extension theorem or any finite count.

For σ(t)=−t, the upper and lower matrices

\[
U_t=\begin{pmatrix}1&t\\0&1\end{pmatrix},\qquad
V_t=\begin{pmatrix}1&0\\t&1\end{pmatrix}
\]

satisfy (1). Their differences U_tv−v and V_tv−v lie on the two isotropic coordinate axes. When k≠0 and t≠0, these differences are nonzero: neither coordinate of v can vanish on such a shell. Thus these matrices supply actual edges, not just loops, in the isotropic-difference graph.

For the finite-field application K=F_(q²), σ(x)=x^q, choose δ≠0 with δ̄=−δ. The fixed field is F_q and every anti-fixed element is in δF_q. Conjugation by diag(δ,1) identifies (1) with SL(2,q), since δ² is fixed and nonzero. Under this conjugation, the two root families above become all upper and lower elementary matrices over F_q.

For completeness, their generation needs no group classification. If A=(a b;c d)∈SL(2,F) has a≠0, left multiplication by V_(−c/a) and right multiplication by U_(−b/a) give diag(a,a⁻¹). If a=0, then c≠0 and U_1A has nonzero upper-left entry. Finally

\[
W(t)=U_tV_{-t^{-1}}U_t=
\begin{pmatrix}0&t\\-t^{-1}&0\end{pmatrix},
\qquad W(t)W(-1)=\operatorname{diag}(t,t^{-1}).
\]

This gives generation uniformly, including F2. Combining generation, the transport theorem and the isotropic root moves proves connectivity of the shell graph. The retained proof identifies this graph with the point collinearity graph of a block residue; every flag vertex there has q neighbors, so the residue is connected.

The new Lean file `phase210_formal/HermitianPlaneTransport.lean` proves thirteen declarations: the equivalence with the Gram equations, invariance of the norm under σ, preservation of norm, existence and uniqueness of (2), and the six assertions about the two root families and their nonzero isotropic moves. They hold over an arbitrary involutive field. The existing `formal/ResidueConnectivity.lean` supplies the abstract generating-move connectivity theorem. The identification of the finite-field unitary group with SL2, its elementary generation, the projective-to-shell map and the chamber action are still written proofs. No complete formalization of the original conjecture is asserted.

The formula, elementary unitary linear algebra and root-generation argument are not claimed to be historically new. The contribution here is to supply and formally verify the exact missing general interface used by the retained proof. This supplement is new author work by the reviewing agent; its semantic fit should receive a separate root review before public admission, even though Lean checks the displayed statements.
