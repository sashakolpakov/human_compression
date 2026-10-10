# An infinite image of the hexagonal presentation at multiples of six

Private result, 10 October 2026. This note proves an algebraic obstruction for the displayed presentation associated with L003 Problem 9.2. It does **not** prove nonexistence of finite hypertopes with the prescribed residues, nor settle the literal open problem or establish current priority.

## 1. Exact source target and its limits

The primary source is M. E. Fernandes, D. Leemans and A. Ivić Weiss, *Hexagonal extensions of toroidal maps and hypermaps*, Springer Proceedings in Mathematics and Statistics **234** (2018), 147–170. The [author-repository manuscript](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf) is stored privately as `sources/catalogue_L003.pdf`; its internal pages 17–19 contain the presentation, Table 8 and Problem 9.2. Those sections were read directly.

Problem 9.2 asks whether Table 8's fifth through eighth lines belong to an infinite family with residue parameters

\[
 ((3,0),(2,0),(1,1),(s,0)),\qquad s\geq2.
\]

Table 8 is labelled as finite universal hypertopes. Immediately before the problem, page 18 describes the intended extrapolation as “an infinite family of finite hypertopes”. The problem sentence itself does not explicitly include either *finite* or *universal*. These differences matter: infinitude of a presented universal group does not prevent finite quotients with the same local residues, and excluding infinitely many parameter values does not exclude an infinite family on other values.

The later primary paper Fernandes–Leemans–Piedade–Weiss, [*Two families of locally toroidal regular 4-hypertopes arising from toroids*](https://dipot.ulb.ac.be/dspace/bitstream/2013/301629/3/FLPWrev.pdf), Contemporary Mathematics **764** (2021), 89–100, proves the **first** Table 8 family in Theorem 4.3. Its §5 also corrects residue identifications in the second and third rows. Thus a presented parameter must not be silently treated as the exact isomorphism type of an actual residue. Neither that section nor the bounded searches in the companion record established a later resolution of Problem 9.2.

## 2. The presented group

Write $P_s$ for the group on $x,y,z$ with relators

\[
\begin{gathered}
x^6,\quad y^3,\quad z^2,\quad(zx)^3,\quad(zy)^6,\quad(x^{-1}y)^2,\\
(y^{-1}x^{-2})^3,\quad(zx^3)^2,\\
\bigl(x^{-1}z(y^{-1}z)^2\bigr)\bigl(zx(zy)^2\bigr),
\quad\bigl(y(zy)^2\bigr)^s.
\end{gathered}
\]

This is the source's rotational presentation after the four parameter pairs have been substituted. Calling it $P_s$ avoids assuming that the corresponding coset system is a hypertope or has the exact advertised residues.

**Theorem.** If $s$ is a positive multiple of six, then $P_s$ is infinite. At $s=6$, the element $(xyxz)^2$ has infinite order in an explicit rational monomial representation of degree 216.

## 3. Elementary integer-voltage certificate

Here is the general verification principle. Let each generator $a$ have a permutation $p_a$ of a finite set $\Omega$ and an integer function $v_a:\Omega\to\mathbb Z$. It acts on $\Omega\times\mathbb Z$ on the right by

\[
(i,n)^a=(p_a(i),n+v_a(i)).
\]

Its inverse sends $(i,n)$ to $(p_a^{-1}(i),n-v_a(p_a^{-1}(i)))$. A word therefore gives a permutation of $\Omega$ and a total voltage at each starting state. It is the identity on the infinite set exactly when its permutation is the identity and all these finitely many voltages vanish. Consequently, testing each defining relator at each state establishes a homomorphism from the presented group. If a word fixes a state and adds a nonzero integer there, its successive powers are distinct.

Equivalently, on a 216-dimensional rational row space use the monomial matrix defined by

\[
e_i M_a=2^{v_a(i)}e_{p_a(i)}.
\]

The same voltage check proves each relator matrix is the identity. A loop of voltage −1 gives a diagonal entry $1/2$ in its matrix; its powers cannot equal the identity. This is a standard voltage/Schreier-action argument, not a claimed new general principle.

The complete literal data are in [phase32_L003_voltage.json](phase32_L003_voltage.json): three permutations on 216 states and three weight lists, all weights in $\{-1,0,1\}$. The standalone [checker](phase32_L003_voltage_check.py) uses only integer arithmetic and the Python standard library. It independently builds the ten source words from their factored expressions, including inverses, and verifies:

1. Every generator is a bijection.
2. All ten $s=6$ relators act identically at all 216 starting states: 2,160 exact checks.
3. The word $(xyxz)^2$ fixes **every** state and has voltage −1 at state 1.
4. The parameter word $y(zy)^2$ has exact order six in this representation.

Item 3 proves the infinite-order assertion: the same word's $k$-th power sends $(1,0)$ to $(1,-k)$ for every integer $k$, by the action law. The code checks some powers as a diagnostic; the assertion for all powers follows from this displayed formula, not extrapolation. Item 4 implies that the same representation satisfies the last relator for every positive $s$ divisible by six. All other relators are independent of $s$. This proves the theorem.

Run without modifying the saved report:

```sh
python3 phase32_L003_voltage_check.py \
  --data phase32_L003_voltage.json \
  --output /tmp/L003-voltage-review.json
```

The [saved report](phase32_L003_voltage_check.json) records the exact input/checker hashes and translation vector.

## 4. Discovery, not a necessary trust dependency

The initial GAP computation mapped $P_6$ onto $C_6=\langle c\rangle$ by $x\mapsto c,\ y\mapsto c^4,\ z\mapsto c^3$. It found kernel abelian invariants $2,2,3,3$, and free abelian rank six for the next derived subgroup, of total index 216. The scripts `phase32_L003_probe.g` and `phase32_L003_find_voltage.py`, the former's saved log and permutation action, preserve that route. The finder solves a homogeneous rational linear system on the labelled Schreier graph after setting spanning-tree voltages to zero. It found a six-dimensional solution space and the small integer solution in the final data.

The infinitude proof does **not** rely on correctness of GAP's subgroup rewriting, the asserted kernel index, the abelianization computation, SymPy's nullspace algorithm, or any recognition of a finite quotient. It only uses the final literal permutations and weights and the exact relator checks. Those discovery programs are diagnostic provenance, not substitute proofs of geometry.

## 5. What this does and does not answer

The finite groups listed in the source at $s=2,3,4,5$ do not justify extrapolating the same presented groups to finite groups for every $s\geq2$. The theorem rules out that particular extrapolation, already at six, and for all its multiples.

It leaves open in this investigation:

- Whether $P_s$ yields an actual universal hypertope with exact residues at these or other parameters.
- Whether suitable finite quotients realize the same exact local geometries.
- Whether an infinite family of finite universal examples exists on other parameter values.
- The full contemporary status and priority of the original Problem 9.2.

No significant-open-problem resolution marker or whole-paper reduction is attached to this result. The new obstruction is an infinite-image certificate for an exact source presentation.
