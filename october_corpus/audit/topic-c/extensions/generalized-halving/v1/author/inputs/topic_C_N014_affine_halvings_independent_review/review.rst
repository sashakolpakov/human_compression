Independent review: affine endpoint halvings
============================================

Accepted within the bounded marked-group scope, without a requested correction.
The author freeze is e7acbf6915bc92b54cf9392c499d81b8ec4b8082622e2946a798f6fed7ff556e.
The entire four-page proof and literal Section 5, physical pages 16--21, were
read. All four current pages and these six source pages were directly viewed.

The reviewer previously authored related Topic C/common affine material and
reviewed other affine applications, but did not author this root note. This
review independently checks its actual uniform proofs. Earlier finite N014
review evidence is bound for provenance; the acceptance here is not inferred
from a sample or from an earlier acceptance flag.

Universal groups and embeddings
-------------------------------
The adjacent swaps and endpoint sign change generate the full signed group.
Multiplying x by its linear part gives translation e1+e2; its signed orbit spans
D. In the second group, adjacent swaps and y generate the even-sign group.
The third zero coordinate is essential in obtaining all signed pair vectors
for n>=3. These arguments prove both equalities, including both containments.

The Coxeter argument is complete: exchanging the duplicated endpoint nodes is
an automorphism of the proposed abstract presentation. Adjoining an involution
with this action gives a genuine semidirect product. Eliminating the duplicated
node gives precisely the retained old Coxeter presentation, including the
four-bond relation and every conjugate relation. Thus there is an embedding,
not merely an affine image of the presentation. The second duplication is
valid also in the low-dimensional square/four-leaf cases. It uses parity of
negative signs, which is different from determinant parity. No false general
endpoint-converse statement is invoked.

Periods and complete presentations
----------------------------------
For either actual affine subgroup, restriction of W -> W/Lambda has kernel
D intersect Lambda. The linear complement has trivial intersection with that
kernel, so the displayed semidirect products preserve the markings. The five
lattice rows follow from the parity of s times the coordinate sum, and for
k=n from parity of nst in s(2v+t1). All listed indices follow by dividing the
ambient integer-lattice index by two. The proposed D basis has determinant
two; every listed period basis lies in D under its stated parity condition.
The translation/conjugation presentation has the usual normal form T^v p,
and its affine realization proves that no additional relations are imposed.

Literal source words and normal closures
----------------------------------------
The affine composition convention is consistent throughout. The k=n words
are u squared, with u^n translation by the all-one vector. The two k=1 words
have linear parts z2 and z2 zn and square to translation 2e1. The k=2 words
are translations by e1+e2. The special n=3 word in Proposition 5.12 gives the
same translation, and the n=4 explicit source word fits the stated general
expression. Powers in every parity branch were checked against the actual
source pages, not only against the author's summary.

The normal closure of a translation inside D semidirect P is exactly its
integer P-orbit span: translations centralize one another and P supplies all
conjugates. The all-one orbit under the full signed group spans E=2Z^n+Z1.
Under the even-sign group it spans M=2D+Z1, since pair-indicator vectors span
D for n>=3. For odd n, 1-ei belongs to D, giving M=E. For even n, all 2ei have
one coset modulo 2D, giving index at most two; parity excludes index one.
This proves the exact extra factor two in the even-n double-halving branch.
The odd k=1 and odd ns,k=n branches give relative indices 2^(n-1), as stated.
The embedding proof makes these exact quotient-order factors, not merely
lower bounds from an auxiliary finite model.

Source boundary and attribution
-------------------------------
The classical cubical realization, source lattice conventions and halving
operations remain attributed inputs. The lattice and subgroup calculations
are accepted uniformly for n>=3,s>=2,k in {1,2,n}. Source hypotheses ensuring
geometric nondegeneracy, the validity of subsequent geometric operations and
Section 5.3's complete diagrams are not certified by this note. The literal
printed relations remain necessary relations. The correction is to their
claimed sufficiency as complete presentations; no assertion about a later
journal revision is made. No whole-original, conjecture, Lean or metric
credit is granted.

Independent diagnostic and replay
---------------------------------
check_algebra.py constructs exact homogeneous integer matrices independently,
uses orbit traversal for translation normal closures and Hermite normal forms
for lattice comparison. It imports no author code. The grid n=3..7,s=2..6,
k in {1,2,n} yields 75 parameter triples, 150 literal relators and 240 Coxeter
pair checks. Four explicitly false weakenings fail at their arithmetic tests.
These samples supplement the preceding full written proof review; they are
not a substitute for the uniform proof. A fresh two-pass build has exactly
the four frozen page texts and no layout diagnostics.
