# An exact transfer annihilator for the third-excess count

10 October 2026. This is a new proof supplement developed during the independent audit of [the frozen transition calculation](phase22_excess3_transitions.md). It is distinct from that audit. It leaves all authored transition files unchanged and makes no publication-priority claim.

The supplement replaces the separate eventual-polynomiality input by a finite integer-vector identity. Correctness and completeness of the underlying graph still retain the finite-state theorem, the kernel census, and the recorded GAP/NQ calculations.

## 1. Operator and data convention

Use the frozen graph `phase22_excess3_final.graph.json`, SHA256
`b3cf789f5278c773636a9e440a06115dd023b11c0519bbe3c68a51ce33b3c0d6`.
It has 708 states and 1,522 directed edges. Each edge is a triple $(s,t,w)$, with one-based source and target state indices and a nonnegative excess increment $0\le w\le3$.

Work in the free abelian group $\mathbb Z^{2832}$, with basis $e_{s,k}$ for $1\le s\le708$ and $0\le k\le3$. The zero-based array coordinate of $e_{s,k}$ is $4(s-1)+k$. Vectors are columns. Define the integer linear operator $T$ by
\[
 T e_{s,k}=\sum_{(s,t,w)\text{ an edge}\atop k+w\le3}e_{t,k+w}.
\]
Thus $T$ advances the rank by one and discards terms above the excess budget. It includes every retained edge, with multiplicity if distinct edges contribute to the same coordinate.

The initial vector $v_5$ has one contribution $e_{s,k}$ for each saved initial row $[s,k]$. Put $v_d=T^{d-5}v_5$ for $d\ge5$. The established walk bijection means that $v_d(s,k)$ counts the ordered markings of rank $d$, total excess $k$, and final state $s$. Let $\ell(v)=\sum_s v(s,3)$, so $a_3(d)=\ell(v_d)$.

## 2. A finite exact certificate

The independently written [standard-library checker](phase22_excess3_annihilator.py) loads the entire graph, forms $v_7=T^2v_5$, and computes its first four differences under $\Delta=T-I$. It verifies, as equalities of integer vectors,
\[
 \Delta^3v_7=125e_{1,3},\qquad Te_{1,3}=e_{1,3}.
                                                        \tag{1}
\]
Consequently $\Delta^4v_7=0$. This is a zero test on all 2,832 coordinates, not merely on their sum.

The [saved report](phase22_excess3_annihilator.json) includes the complete sparse vectors, their hashes, and these summaries:

| Vector | Nonzero coordinates | Sums at excesses 0,1,2,3 |
|---|---:|---|
| $v_7$ | 847 | $(1,25,299,2499)$ |
| $\Delta v_7$ | 139 | $(0,5,134,1780)$ |
| $\Delta^2v_7$ | 17 | $(0,0,25,715)$ |
| $\Delta^3v_7$ | 1 | $(0,0,0,125)$ |
| $\Delta^4v_7$ | 0 | $(0,0,0,0)$ |

## 3. All later ranks follow algebraically

For every integer $n\ge0$, the commuting-operator binomial theorem gives
\[
 v_{7+n}=(I+\Delta)^n v_7
       =\sum_{j=0}^{3}\binom nj\Delta^jv_7.            \tag{2}
\]
Indeed $\Delta^4v_7=0$ implies $\Delta^jv_7=0$ for every $j\ge4$; terms with $j>n$ have binomial coefficient zero. Thus the finite certificate proves polynomial behavior for every later rank. Equivalently, $\Delta^4v_d=T^{d-7}\Delta^4v_7=0$ for all $d\ge7$.

Apply $\ell$ to (2). The exact Newton formula is
\[
 a_3(d)=2499+1780(d-7)+715\binom{d-7}{2}
                   +125\binom{d-7}{3}
       =\frac{125d^3-855d^2+2380d-2646}{6}
       \quad(d\ge7).                                 \tag{3}
\]
The graph's exact initial values $a_3(5)=584$ and $a_3(6)=1309$ agree with (3). Rank four is below the graph's initial rank and is handled by the separate complete phase21 census, whose 199 ordered markings also agree with (3). Therefore the formula holds for every $d\ge4$. The separate rank-three census gives 37, while the polynomial would give 29; that exception is retained explicitly.

This proof needs no independent theorem about eventual polynomiality and no inference from numerical agreement at several ranks. Its all-rank step is the exact operator identity (1), together with the finite-state interpretation of $T$.

## 4. Independent arithmetic checks and retained boundary

The same checker additionally verifies exact boundary-kernel matching, all edge weights from canonical pc-key lengths, all minimum-cost state labels by monotone relaxation, and the presence of every boundary-compatible edge allowed by the budget. There are 3,689 window boundary pairs and 2,185 budget exclusions. The edge-completeness check is conditional on the recorded group calculation that none of the budget-eligible candidates fails either compatibility test; it does not reconstruct those group tests in Python.

It recounts ranks 5 through 24 and matches every saved row. The interpretation of canonical pc-key length retains the recorded assertion that all relevant relative pc orders are two. The GAP/NQ group constructions, all actual subgroup intersections, and the correctness of the two extra deletion states remain retained computations. This is an independent implementation of finite-graph arithmetic, not an independent implementation of the group census.

Run, using Python 3 with no third-party packages:

```sh
python3 phase22_excess3_annihilator.py --inputs . --output scratch/annihilator.json
```

The input directory must contain the graph, window and gluing data, and the three phase21 census reports named in the saved report. Only the specified output is written. No historical file, author proof, public registry, or formal certificate is altered by this supplement.
