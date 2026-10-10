# The Hermitian residue labels from one rank-one Cayley graph

We retain the complete Hermitian proof in hermitian_unital_proof.md, including its identification of the block residue with a norm shell and its elementary identification SU(2,q)≅SL(2,q). The present argument adds the diameter and gonality labels needed to audit Figure2 of L092. It does not repeat the conjecture proof or claim its discovery again.

Throughout q>2. For a bipartite incidence graph, write (d₀,g,d₁) for the two vertex-type diameters and half its girth, in the source's convention.

**Theorem H.Labels.** In the literal Construction3 on UH(q), the original-point residue has parameters (4,3,4). The original-block residue, ordered by outside points and flag objects, has parameters
\[
(5,4,6)\quad\text{if q is even},\qquad
(6,4,6)\quad\text{if q is odd}.
\tag{H1}
\]
The original-flag residue is K(q,q²−1).

## 1. The common Cayley graph

Let W be the Hermitian plane in the retained norm-shell construction and let
\[
X=\{v\in W:h(v,v)=-1\}.
\]
Its points form the point type of the block residue. Two distinct points v,w are collinear exactly when h(v−w,v−w)=0. The group SU(W) acts regularly on X, as proved in the retained argument.

Fix v₀∈X and choose an orthogonal basis beginning with v₀ and with both vectors of norm−1. A determinant-one unitary matrix has the form
\[
\begin{pmatrix}a&b\\-b^q&a^q\end{pmatrix},
\qquad a^{q+1}+b^{q+1}=1.
\]
A direct calculation gives h(gv₀−v₀,gv₀−v₀)=tr(g)−2. Consequently the point graph is the Cayley graph of SU(W)≅SL(2,q) whose connection set consists of all nonidentity trace-two matrices. These are precisely the nonidentity unipotents. The identification by conjugation in the retained proof preserves traces.

Every noncentral element of SL(2,q) has distance at most two from1. This is immediate for trace two. Otherwise conjugate the element to g=(a b;c d) with c≠0; such a basis exists because a nonscalar transformation does not preserve every one-dimensional subspace. Put
\[
u=\begin{pmatrix}1&s\\0&1\end{pmatrix},
\qquad s=\frac{\operatorname{tr}(g)-2}{c}\ne0.
\]
Then tr(u⁻¹g)=2 and u⁻¹g≠1, so g is a product of two connection elements. In even characteristic the only central element is1, and the diameter is two. In odd characteristic −1 is not a product of two connection elements: if −1=uv and tr(u)=2, then tr(v)=tr(−u⁻¹)=−2≠2. It is a product of three, since −u⁻¹ is noncentral and hence a product of two. Thus the diameter is three, and the only point at distance three from a given point is its antipode.

The incidence graph has no four-cycles by partial linearity. It also has no six-cycles. To see this, normalize three pairwise adjacent points to1,u,v. Conjugate u to (1 s;0 1), s≠0. From tr(v)=tr(u⁻¹v)=2, the lower-left entry of v is zero, and its determinant then forces both diagonal entries to be1. Hence u and v lie in the same upper root group. In the norm-shell coordinates this root group moves points along a single isotropic affine direction, so all three points lie on the same flag object. They cannot form a six-cycle using three distinct flag objects.

There is an eight-cycle. Take nonidentity upper and lower unipotents u,v. The four points1,u,uv,v form a quadrangle in the point graph: their successive quotients are unipotent, whereas tr(uv) and tr(u⁻¹v) differ from2. Its diagonals are therefore absent. Its four joining flag objects are distinct, producing an eight-cycle in the incidence graph. The gonality is exactly four.

## 2. The two incidence diameters

Every flag object has q neighboring points. In odd characteristic at most one of them can be the antipode of a prescribed point; in even characteristic every point is within point-graph distance two. Thus every point–flag distance is at most five, in either characteristic.

Some point–flag distance is five. A fixed point has q+1 neighboring flags. Since the incidence graph has girth eight, its flags at distance three number exactly (q+1)(q−1)q. Hence only
\[
(q+1)\bigl(1+q(q-1)\bigr)=q^3+1
\]
flags lie within distance three, whereas the total number is (q+1)(q²−1). Their difference is (q−2)(q+1)>0. Combined with the point-graph diameters, this gives point-type diameter five for even q and six for odd q.

Any two flag objects are at distance at most six: choose a point on the first and a point on the second which is not its antipode, and use the point-graph bound. To see that six occurs, use hyperbolic coordinates
\[
h((x,y),(x,y))=xy^q+x^qy.
\]
Fix b≠0 and c∈Fq*∖{1}. The shell lines F_b and F_{cb}, with constant second coordinates b and cb, are distinct flag objects of the same isotropic direction. Each contains q points. For (x,b)∈F_b and (x′,cb)∈F_{cb}, the shell equations give
\[
h((x,b)-(x',cb),(x,b)-(x',cb))
 =c+c^{-1}-2=(c-1)^2/c\ne0.
\]
Thus no point of one flag is collinear with a point of the other. The flags have neither a common point nor a path of length four; their distance is six. This proves (H1).

## 3. The original-point residue

Fix the deleted unital point Q. The remaining points split into q² classes of q points, one class for each block through Q. Two remaining points are collinear in this residue exactly when they belong to different classes. Its point graph is therefore complete multipartite, and the largest point–point distance in the incidence graph is four.

A remaining block meets q+1 different classes. Every point not on that block is collinear with at least one of its points, so every point–block distance is at most three. Two blocks have distance at most four by the same argument. Disjoint remaining blocks exist: fix one block L and choose x∉L∪{Q}; at most q+1 blocks through x meet L, and at most one further block contains Q, whereas q²>q+2. Thus the line-type diameter is four as well.

Choose x,y in different Q-classes, and choose z outside the union of Qx,Qy and xy. Such z exists since q³+1>3(q+1). These three points give a proper triangle in the residual linear space. Partial linearity excludes four-cycles, so its gonality is three. This proves (4,3,4). The complete-bipartite flag residue was already proved in the retained Hermitian argument.

## 4. Complete comparison with the printed table

The right-hand label of every literal row is (4,3,4). The left-hand label is (6,4,6) for q=3,5,7,9,11,13 and (5,4,6) for q=4,8,16. Therefore the left q=5 and q=8 labels and the right q=5,q=8,q=11 labels in the printed Figure2 disagree with the literal construction. All remaining diameter/gonality labels agree. The separate phase186_hermitian_figure_audit.md gives the panel-order discrepancies at q=5,8,11 and the q=16 object-count discrepancies.

Together these two notes pay every numerical label in Figure2 by uniform formulas. The finite check uses cosets of the q+1 root groups in SL(2,q), the incidence model established above, for the nine displayed values of q. It is a check of the group/coset model and the written source-isomorphism bridge; it does not independently rebuild all projective unital coordinates at q=16. The new all-q diameter proof is written mathematics and has not been formalized in Lean.
