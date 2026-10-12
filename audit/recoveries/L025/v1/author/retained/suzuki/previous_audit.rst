# Independent audit of the Suzuki pentagon proof

9 October2026. I read suzuki_cycle_proof.md, the complete Lean source,
catalogue_L025.txt §3.2, and Bray–Bäärnhielm arXiv1706.05697 equations1–5.
I found no missing hypothesis, cycle-count factor, or matrix-convention gap
in the proposed proof for q=2^(2e+1), e>=1.

**Source identification.** L025 Conjecture3.2 concerns precisely the graph
with vertex stabilizer E_q:C_(q−1), circle nucleus n, and edge stabilizer of
the unordered ovoid pair {n,p}, with p in the circle's orbit of size q.
The recognition paper's matrices agree exactly with the proof:
z(a)=U(0,a), t(λ)=M'(λ), and w is its antidiagonal matrix T.
There is no exponent or transpose change. Its lower-triangular point
stabilizer uses the row-vector convention on the ovoid; this is independent
of the subsequent choice of left cosets for the graph.

For additional detail in the subgroup identification, the displayed Suzuki
matrices give U(x,y)^2=U(0,x^(θ+1)). Hence the involutions in U, together
with the identity, are precisely Z. After moving (n,p) to (∞,0), the source's
elementary abelian group of order q must therefore be Z. Its intersection
with the unordered-pair stabilizer fixes both points individually and has
order q−1, so it is exactly the diagonal T. Thus H=ZT, and the edge
stabilizer is K=<T,w>. Inversion takes the source's right-coset incidence
graph to the left-coset version without changing adjacency.

The triangular matrices give H∩wHw=T and H∩K=T. This also excludes
parallel edges: the stabilizer in H of the neighbor wH equals the
stabilizer of the edge K, so incident edge cosets correspond bijectively
to neighbors. The double-coset adjacency graph is therefore the exact
simple graph in the source, not a simplification of a multigraph.

**Counting and girth.** The four field parameters describe every length-five
walk beginning with H,wH uniquely. At each successive step, parameter zero
returns to the preceding vertex, even though the chosen representative of
the current coset contains earlier z-factors. The closure condition is
exactly W∈H. The three forced zero entries imply bc=1, ab=1, c=a and d=b;
conversely the displayed full matrix equals z(a^-1)t(a²/(θa)). The identity
θ²(x)=x² is used in identifying this torus parameter, and is valid for all
the stated fields.

The triangle obstruction and the square obstruction concern entries that
actually vanish throughout H. In particular the square proof correctly
uses W12=(θa)b, not W42=b, which need not vanish in H. I independently
recomputed its three displayed entries: W42=b, W21=a(θb), W12=(θa)b.
There are no triangles or squares. A closed nonbacktracking length-five
walk is consequently a simple pentagon; a repetition at the closing
junction would also create a shorter cycle. Each undirected pentagon
through the fixed directed edge has one such traversal. No factor2 or5
is required, so the count is q−1 per edge.

**Formal scope.** I independently recompiled the unchanged Lean file to
/private/tmp/SuzukiPentagons.audit.olean. Compilation exited0. Its SHA256
matches the existing certificate:

    3080fd0aca19b8de8739d023ef3c92f1f3aa97b032a79e31e308b6e67384b4c2

The reported axioms are only propext, Classical.choice and Quot.sound.
The theorem five_in_borel_iff proves the complete matrix-membership
equivalence over a characteristic-two field equipped with a ring
automorphism θ satisfying θ∘θ=squaring. Its BorelPart is explicitly
the set ZT used here, not the full Suzuki point stabilizer UT. The file
also proves the triangle/square entry identities and all sixteen closing
matrix entries. There is no finite-field search or unproved Lean axiom
hidden in those statements.

The finite-field instance, identification of ZT with the source subgroup,
coset-walk bijection, simplicity, girth implication, and cardinal count q−1
remain written mathematics. The finite Suzuki group order and ovoid action
are standard structural inputs. The optional connectivity argument uses
the standard maximality of the split-torus normalizer; it is unnecessary
for the pentagon count. Thus the accurate claim is a formally verified
matrix core inside a reviewed written proof, not a fully formalized graph
theorem. The q=8 coset-graph check is consistent and counts undirected
cycles correctly, but is not the all-q justification.

The root subsequently updated the proof's verification section to record
the completed symbolic and formal certificates; its mathematical argument
is unchanged. I have not performed a new priority search in this audit;
absence of a later published resolution and novelty remain separate
bibliographic questions.
