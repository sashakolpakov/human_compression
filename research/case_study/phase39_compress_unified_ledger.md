# Unified seven-source target and dependency ledger

Status: complete private author draft; new integration review pending. No seven-paper factor. Thirty-four adapters are a contract inventory; they do not count independent papers or new theorems. Every necessary written proof is in the continuous manuscript; the full finite census algorithm is in Appendix A.

## Source bindings and reading limits

- `sources/phase16_N001_browser_record.txt` — 30487 bytes, SHA-256 `222d5742392a4c40c0468d473bfba99b50f34a70eb0ac90200006314d3c5b207`.
- `sources/network_independent_generators.pdf` — 65142 bytes, SHA-256 `43f3f2b1cbb7dacc55f12572ef78a5bb574bcfe745aba6cc0c10291256e611a2`.
- `sources/phase10_N003_extracted.txt` — 22824 bytes, SHA-256 `165ef2f20f7b5b3f04021205e002e0f22d2249b035bbc480de10f21986d14310`.
- `sources/phase16_N001_academia.html` — 5602 bytes, SHA-256 `db0144ae1e0bb84ee3bb1ebb311143aea5769dc8112a5a9cc5eceb9e26440ec2`.
- `phase12_N003_source_scope.json` — 5950 bytes, SHA-256 `3ed1b2d1c7b4c575202ace4a61d00211e9867e404189d39b2bba24bf2181e03f`.
- `phase16_older_source_access.md` — 4231 bytes, SHA-256 `d7bf0efba838fb2c0bb03fe3afe9a3e3a8a7e4a18f1ab679a543362887377169`.
- `sources/phase16_frattini_geometries.pdf` — 181798 bytes, SHA-256 `cfbd53bc367ecaea644214eb0f64fc5db0c20d63096fdc239cf5d61c3f72c5c9`.
- `sources/phase16_frattini_geometries.txt` — 24071 bytes, SHA-256 `056823e93c4da84e0fb8f9425ebb2a1f27efc78b7ce6bb18a69b09c0b102f128`.
- `sources/catalogue_L032.pdf` — 299557 bytes, SHA-256 `3f670cf785ac3147c2b5ee501b595241a567910d8a94a096b26b78f8dcb76c66`.
- `sources/catalogue_L032.txt` — 21975 bytes, SHA-256 `3da8d9dda3c81091be4b5a202db75133b3dfd86f4fb67a1490ca9a98d1a99320`.
- `sources/catalogue_L035.pdf` — 383276 bytes, SHA-256 `2b663945333acc52a3b655ba15fa59bae213c8857824f54bc296d32cf872d3a0`.
- `sources/catalogue_L035.txt` — 73884 bytes, SHA-256 `a79dc93c209e4731de2fe6f4c28ace6248b36c749660d07fc8a37742277f3e0f`.
- `sources/catalogue_F013.pdf` — 394696 bytes, SHA-256 `27576c1b5598c7a17e4a58bac937ebdd1684f79891fd3b452e8527b511ec5a93`.
- `sources/catalogue_F013.txt` — 32529 bytes, SHA-256 `e2a9126a22d157718507cba9954e28f0c916d72aa6b53e1aaad67dc7dccb94cc`.
- `sources/symmetric_2groups2025.pdf` — 463339 bytes, SHA-256 `87da14f4af4e24fbbceb7a6208234dba1974ece0d4c51d2b00802df8bf2cd495`.
- `sources/symmetric_2groups2025.txt` — 56735 bytes, SHA-256 `8c7dd8d12977606347f4d51580a78550bf72c4d81e0db6ada362c8afd03e8cb2`.

Exact versions, primary locators and all reading limitations are preserved in the JSON. N001 remains the complete authored browser body with extraction damage, not an acquired PDF. N003 uses the12-pageauthorversion, N008 the9-pagejournalPDF. L032/L035/F013/F016 use the exact frozen primary PDF versions already reviewed. Retained background originals were not all newly read. No source proof is silently replaced by a citation to an internal project note.

## Full target formulations and proof adapters

### A1 — N001 Theorem 1(1)

For every inductively minimal finite pair (Gamma,G), the pair is RWPRI and has properties (2T)_1 and (IP)_2.

Source: `sources/phase16_N001_browser_record.txt`, span `18373:18790`, SHA `4667f5c86394581748d80cc4ce31ce439d719031ffbc2fefde78a7fa7c701961`.

Common result: F, I, D.

**Corollary A1 — N001 Theorem 1(1).** Every inductively minimal pair satisfies RWPRI, \((2T)_1\), and \((IP)_2\).

*Proof.* B97 and Lemma D identify it with an unweighted tree geometry. Apply Proposition I, including its leaf argument in every residue and its explicit two-edge residues. ∎

Retained inputs: B97, Coset, Elementary.

Replacement span `91063:91354`, SHA `6938f60959afce26b84ce7b4c409b801df4138e7fc63fee92e832dd92b7ad448`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### A2 — N001 Theorem 1(2)

An inductively minimal pair of even rank is PRI.

Source: `sources/phase16_N001_browser_record.txt`, span `18373:18790`, SHA `4667f5c86394581748d80cc4ce31ce439d719031ffbc2fefde78a7fa7c701961`.

Common result: F, O, I, D.

**Corollary A2 — N001 Theorem 1(2).** An inductively minimal pair of even rank is PRI.

*Proof.* Its tree has one more vertex than its rank, hence an odd number of vertices. No edge cut is balanced, so Proposition I applies. ∎

Retained inputs: B97, Coset, Elementary.

Replacement span `91354:91582`, SHA `cc65e5c02f047fe1970045e46d32b7b12df07a20375506193a372fa4efbe4952`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### A3 — N001 Theorem 1(3)

For an inductively minimal pair, failure of PRI implies QPRI; failure of PRI occurs exactly when the connected diagram has a middle (a nonend whose deletion components have equal cardinality).

Source: `sources/phase16_N001_browser_record.txt`, span `18373:18790`, SHA `4667f5c86394581748d80cc4ce31ce439d719031ffbc2fefde78a7fa7c701961`.

Common result: F, O, I, D.

**Corollary A3 — N001 Theorem 1(3).** If an inductively minimal pair is not PRI, it is QPRI; failure of PRI occurs exactly when its diagram has a middle. In fact every inductively minimal pair is QPRI.

*Proof.* Proposition I translates a middle into a balanced nonleaf cut, and Lemma O gives the unique chain from that stabilizer to the full group. All other stabilizers are maximal, so their intervals are chains too. This also disambiguates the source's phrase “this is the case”: the middle characterizes failure of PRI, not QPRI by itself. ∎

Retained inputs: B97, Coset, Elementary.

Replacement span `91582:92130`, SHA `a5b45f63680487e502e7430779b36cf431019d3886bdf52739fe28aa914f41c1`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### A4 — N001 Theorem 1(4)

An inductively minimal pair is RPRI if and only if its diagram is a complete graph.

Source: `sources/phase16_N001_browser_record.txt`, span `18373:18790`, SHA `4667f5c86394581748d80cc4ce31ce439d719031ffbc2fefde78a7fa7c701961`.

Common result: F, O, I, D.

**Corollary A4 — N001 Theorem 1(4).** An inductively minimal pair is RPRI if and only if its diagram is complete.

*Proof.* Proposition I gives RPRI exactly for stars, whose line graphs are exactly the complete diagrams. ∎

Retained inputs: B97, Coset, Elementary.

Replacement span `92130:92354`, SHA `24e10f12d6c5ddb53fc307aa6269d4289a3c9299d70853846363d16d8d9f4e8a`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B1 — N003 Theorem 1.1

For a normal subgroup N of G, mu(G) <= mu(G/N)+mu_prime(N). If N is abelian, mu(G) <= mu(G/N)+mu_prime_G(N), with G acting on N by conjugation. The printed source says a group; this contract takes finite G.

Source: `sources/phase10_N003_extracted.txt`, span `2266:3462`, SHA `463348d264108108b73878ffd72d7026bbafb9a5692dfb9721c96448f02cd0a2`.

Common result: R(a).

**Corollary B1 — N003 Theorem 1.1, finite-group scope.** For \(N\unlhd G\), \(\mu(G)\leq\mu(G/N)+\mu'(N)\); if \(N\) is abelian, \(\mu(G)\leq\mu(G/N)+\mu'_G(N)\).

*Proof.* Apply Theorem R(a). The finiteness restriction is part of this intake contract; no assertion about infinite maxima is added. ∎

Retained inputs: Elementary.

Replacement span `92354:92655`, SHA `e75e658ece625d784c5e7cf86966483209845dbc6a3c5b31c90b877ea36d6ca7`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B2 — N003 Theorem 2.1

For n >= 7, every independent generating set S of S_n of size n-1 is S(T), the edge transpositions of a labelled tree T, or {s} union {(s t)^epsilon(t): t in S(T) except s}, where s in S(T) and epsilon(t) in {+1,-1}. Conversely every set of either form is an independent generating set of S_n.

Source: `sources/phase10_N003_extracted.txt`, span `4215:8878`, SHA `27bdc24ea1ff88805969de7f15a0ab942757d7731e05e6b23c1dffe5090b9d72`.

Common result: F, P, R(a), M, E.

**Corollary B2 — N003 Theorem 2.1.** If \(n\geq7\), every independent generating set \(S\) of \(S_n\) of size \(n-1\) has, for some tree \(T\) on \(\{1,\ldots,n\}\), one of the forms
\[
S=S(T)=\{\tau_e:e\in E(T)\},\qquad
S=\{s\}\cup\{(s\tau_e)^{\epsilon_e}:e\ne d\},
\quad s=\tau_d,\quad\epsilon_e\in\{1,-1\}.
\]
Conversely every displayed set is an independent generating set.

*Proof.* Theorem E is the forward direction; Theorems F and P give generation and independence in both converse directions. ∎

Retained inputs: W1, W2, Elementary.

Replacement span `92655:93161`, SHA `ce163ae9e440efb8bf22b3d9d28c94f4c6a058c0488a11d2ef47695de16a35b4`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B3 — N003 Corollary 2.2

For the two families of Theorem 2.1, the numbers of actual unordered generating sets are n^(n-2) and (n-1)n^(n-2), respectively; identifying each 3-cycle with its inverse changes the second count to binomial(n,2)(n-1)^(n-3). Degree n >= 7 is inherited from that theorem.

Source: `sources/phase10_N003_extracted.txt`, span `8878:10229`, SHA `a7c7f019cd0295a028117ac3e4c6c639ff1c41993970c82948fb661880107a35`.

Common result: F, P, M, E; B3 count adapter.

**Corollary B3 — N003 Corollary 2.2.** For \(n\geq7\), the number of actual unordered generating sets of the first form is \(n^{n-2}\). The number of actual unordered sets of the second form is \((n-1)n^{n-2}\). If a three-cycle and its inverse are identified independently in such a set, the second number becomes
\[
\binom n2(n-1)^{n-3}.
\]

*Proof.* Ordinary sets recover their unique edge trees, so Cayley's formula gives the first count. A twisted set has a unique odd member \(s=(a\ b)\). Multiplying each of its other actual members \(h\) by \(s\) recovers a transposition. If \(h=(s\tau_e)^{-1}\), the recovered edge is the conjugate \(s\tau_es\); for an adjacent edge this switches its attachment from \(a\) to \(b\), and for a disjoint edge it changes nothing. Contracting \(\{a,b\}\) gives the same tree before and after any switches. Every such independent switch therefore preserves the tree property. Consequently actual twisted sets are in bijection with trees having one distinguished edge, via the canonical set \(\{s\}\cup\{s\tau_e:e\ne d\}\). This gives \((n-1)n^{n-2}\). Modulo inversion of the three-cycles, the data are exactly the pair \(\{a,b\}\) and a labelled tree on the \(n-1\) blocks obtained by contracting it. Cayley's formula gives the last count. ∎

Retained inputs: W1, W2, Cayley, Elementary.

Replacement span `93161:94444`, SHA `08057925146becaf6466b031ecc37238799f6b45cf1fb0be14e8d6103e830c6d`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B4 — N003 Corollary 2.3

For n >= 7 every independent generating set (s_i:i in I) of S_n of size n-1 is strongly independent: with G_J=<s_i:i not in J>, G_J intersect G_K = G_(J union K) for all J,K subsets of I.

Source: `sources/phase10_N003_extracted.txt`, span `10229:11674`, SHA `57431b75a2948d603335cbda8c26a4123c4036e90e7b76211b47588b55967741`.

Common result: F, P, M, E.

**Corollary B4 — N003 Corollary 2.3.** Every independent generating set of \(S_n\) of size \(n-1\), for \(n\geq7\), is strongly independent.

*Proof.* Use Theorem E to recognize the marking and Theorems F and P for all subset intersections, including the empty subset. ∎

Retained inputs: W1, W2, Elementary.

Replacement span `94444:94716`, SHA `fd15200d803bac1f337cfc5cb825042ffc05581fd3d62f66eaed3a98e2f704b8`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B5 — N003 Corollary 2.4

For n >= 7 and B <= S_n, mu(S_n,B)=n-1 implies B=1.

Source: `sources/phase10_N003_extracted.txt`, span `11674:12459`, SHA `a6af4799dbf6914a0688d32cf0454f5e9dac55b9e64051eb681e447ae88831f4`.

Common result: F, P, O, M, E.

**Corollary B5 — N003 Corollary 2.4.** If \(n\geq7\), \(B\leq S_n\), and \(\mu(S_n,B)=n-1\), then \(B=1\).

*Proof.* Theorem E proves the stronger conclusion from \(\mu'(S_n,B)=n-1\); W1 bounds either invariant by \(n-1\). ∎

Retained inputs: W1, W2, Elementary.

Replacement span `94716:94942`, SHA `18956eecd8fc4226ff595a4de72012b8eb123bd692868364d1fd6c04d02cfe8a`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B6 — N003 Theorem 3.1 and its immediately stated consequence

A source coset geometry for G with Borel B has rank <= mu_prime(G,B). An RWPRI source coset geometry has rank <= mu(G,B), and choices s_i in H_(I minus {i}) outside H_i form a strongly independent relative generating family. The printed source does not impose finite G; this contract takes finite G.

Source: `sources/phase10_N003_extracted.txt`, span `15338:16287`, SHA `cf1ba5a35e8215ae099c9e3b80d37223f01fe64cbf829361c1afc7bb7894249c`.

Common result: R(b).

**Corollary B6 — N003 Theorem 3.1 and its stated strong-independence consequence, finite-group scope.** A coset geometry for \(G\) with Borel subgroup \(B\) has rank at most \(\mu'(G,B)\). If it is RWPRI, its rank is at most \(\mu(G,B)\), and the panel choices (A4.3) give a strongly independent relative generating family.

*Proof.* This is Theorem R(b), including equality (A4.4) for every parabolic. ∎

Retained inputs: Coset, Elementary.

Replacement span `94942:95348`, SHA `4f33c73b34ec7c2597c25c013ec0e6ca3ecd5bc95c3ffb4fb99b320ee853cd88`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B7 — N003 Theorem 3.2

For n >= 7 there is a bijection between independent generating sets of S_n of size n-1, modulo simultaneous conjugation and inversion of individual generators, and RWPRI coset geometries for S_n of rank n-1. The specified group action is retained and set order/type labels may be renamed.

Source: `sources/phase10_N003_extracted.txt`, span `16602:20029`, SHA `df4c8a861620b71bab566f61c376cd80f09fb95ec7906c247bd644b2e11c2be1`.

Common result: F, P, O, R, M, E, G.

**Corollary B7 — N003 Theorem 3.2.** For \(n\geq7\), independent generating sets of size \(n-1\), modulo conjugation and inversion of individual generators, correspond bijectively to RWPRI coset geometries of rank \(n-1\) for \(S_n\), with the specified action and type renaming understood.

*Proof.* Apply the existence and uniqueness parts of Theorem G. Triviality of the Borel follows from Theorem E; cyclic panels of orders two or three give exactly the stated inversion ambiguity. ∎

Retained inputs: W1, W2, Coset, AutSn, Elementary.

Replacement span `95348:95837`, SHA `f32eaa657a1991ea7f70784e70f0d3e78ff58357bb2779a68dff2e496cd467e8`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### B8 — N003 Corollary 3.3

For n >= 7 every source coset geometry of S_n of rank n-1 is RWPRI, without an initial RWPRI hypothesis.

Source: `sources/phase10_N003_extracted.txt`, span `20029:20201`, SHA `ea124ab8b96e81128eb0d4373b2ff82c59edc792fc7990bfd6bf2a14e3aee6ac`.

Common result: F, P, O, R, M, E, G.

**Corollary B8 — N003 Corollary 3.3.** Every source coset geometry for \(S_n\) of rank \(n-1\), with \(n\geq7\), is RWPRI.

*Proof.* Apply the arbitrary-parabolic part of Theorem G. Its balanced-cut and panel argument is needed: merely classifying an extracted independent marking does not identify an arbitrary geometry's original parabolics. ∎

Retained inputs: W1, W2, Coset, Elementary.

Replacement span `95837:96185`, SHA `1338055bcb383f16b75c51c8325f56a5ad1fe11adb3337c0711ca743b384a303`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C1 — N008 Theorem 2.1

For B<=G and Phi=Phi(G), a family (s_i) is an independent generating family of G relative to B iff (Phi s_i) is an independent generating family of G/Phi relative to BPhi/Phi.

Source: `sources/phase16_frattini_geometries.txt`, span `6793:10729`, SHA `450e28c4a6958ecb2172b948a2c21b1c25dc71813099f90bf4ba10d8a2fa5a28`.

Common result: E1,E4.

**Corollary C1 — N008 Theorem 2.1, finite specialization and corrected infinite converse.** Relative independent generating families in a finite group descend to and lift from its Frattini quotient, relative to the image of \(B\). This is E4. Its printed unrestricted infinite converse is replaced by E4's explicit additional hypothesis and the preceding counterexample.

Retained inputs: Elementary, Zorn_if_infinite_extension.

Replacement span `96185:96557`, SHA `e3b96a4d59b7474181abd44beb81140d77090dc055c71a72fd5353d5d54738ca`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C2 — N008 Theorem 3.1

A firm RWPRI coset geometry satisfies Phi(G)<=H_i for every type i, including infinite G.

Source: `sources/phase16_frattini_geometries.txt`, span `10729:12848`, SHA `b6288396d76834283d9f72e7eb35011683fe420ffe07b9f640bcd42778a11ffd`.

Common result: E0,E1,E2.

**Corollary C2 — N008 Theorem 3.1.** In any finite-rank firm RWPRI coset geometry, \(\Phi(G)\leq H_i\) for every type, including infinite groups. Lemma E0 and firmness give the lattice hypotheses, and E2 yields the stronger \(\Phi(G)\leq B\).

Retained inputs: Elementary, Zorn_if_infinite_group.

Replacement span `96557:96801`, SHA `c77b56df7882711a702df18bb81e52c7355477995c827c4a7d76c3b0353721bf`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C3 — N008 Proposition 3.2

If N is normal in G and N<=H_i for every type of a coset pregeometry, that pregeometry is isomorphic to the coset pregeometry (G/N,(H_i/N)).

Source: `sources/phase16_frattini_geometries.txt`, span `12848:13046`, SHA `9ec8f0f72f3bd6a57318e3055626b658e80418ad1a79eda4e17dfd084b8a0d18`.

Common result: E3; common Theorem K(b) through Corollary E3.

**Corollary C3 — N008 Proposition 3.2.** A coset pregeometry whose type subgroups contain \(N\unlhd G\) is isomorphic to the pregeometry of their images in \(G/N\). This is E3 without any flag-transitivity assumption.

Retained inputs: Elementary_subgroup_correspondence.

Replacement span `96801:97020`, SHA `30f9daf4cddeedfc348ae3cf0851facd5aedcb997c46dfc5244723425ccd4cdb`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C4 — N008 Corollary 3.3

A firm RWPRI coset geometry (G,(H_i)) is isomorphic to (G/Phi(G),(H_i/Phi(G))).

Source: `sources/phase16_frattini_geometries.txt`, span `13046:13303`, SHA `3eed453339f8226976fac185db90174ab58e0c5617bd1b69d780f590d2b67450`.

Common result: E0,E2,E3; common Theorem K(b) through Corollary E3.

**Corollary C4 — N008 Corollary 3.3.** Every firm RWPRI coset geometry is isomorphic to its Frattini-quotient coset geometry. Combine C2 with E3.

Retained inputs: Elementary, Zorn_if_infinite_group.

Replacement span `97020:97167`, SHA `685ad07a483e93207729d6985a9b3f3b6d6686f164b530cf89611a261b55828f`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C5 — N008 Theorem 3.4

Every firm RWPRI geometry is isomorphic to a firm RWPRI geometry for a Frattini-free group.

Source: `sources/phase16_frattini_geometries.txt`, span `13303:14628`, SHA `ea2b599c6298f1c6e88a75c59187fc16fddf6b3a3931e71ca2e0ce916987ed11`.

Common result: E0,E2,E3 and maximal-subgroup correspondence; common Theorem K(b) through Corollary E3.

**Corollary C5 — N008 Theorem 3.4.** Every firm RWPRI geometry is isomorphic to one for a Frattini-free group. Apply C4 and the maximal-subgroup correspondence following E3. Quotient and pullback give the fixed-indexed-family bijection motivating the paper.

Retained inputs: Elementary, Zorn_if_infinite_group.

Replacement span `97167:97426`, SHA `238729e93912ad8bd7a6370b24d292db2aa9b8f6d2026b872c2c5b47b3a6910b`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C6 — N008 Proposition 3.5

A rank-two coset pregeometry (G,(H_1,H_2)) is a direct sum iff H_1 H_2=G.

Source: `sources/phase16_frattini_geometries.txt`, span `14628:14928`, SHA `b217eecabcf09d2d1ddab13349a6850c7e2dccf03bc0944c1db0fab3e264996b`.

Common result: Exact coset-product proof after E5.

**Corollary C6 — N008 Proposition 3.5.** A rank-two coset pregeometry is a direct sum exactly when \(H_1H_2=G\). This is the coset-product calculation after E5, with no finiteness or normality assumption.

Retained inputs: Elementary.

Replacement span `97426:97632`, SHA `c52982a1eb7c26ebc5ed69773b8cb4194c7f5b75b382df1e0d7b4bb21ebeb6bb`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C7 — N008 Lemma 3.6

For proper U,W<F_p^k with W not contained in U, if U is maximal and U intersect W is maximal in U, then W is maximal in F_p^k.

Source: `sources/phase16_frattini_geometries.txt`, span `14928:15082`, SHA `0de0814560a31374c6a65f0c3063cdf628c4431ba5f9c504a1044d8462676808`.

Common result: Dimension proof after E5.

**Corollary C7 — N008 Lemma 3.6.** If \(U,W<\mathbb F_p^k\), \(W\not\subseteq U\), \(U\) is maximal and \(U\cap W\) is maximal in \(U\), then \(W\) is maximal in \(\mathbb F_p^k\). This is the dimension calculation after E5.

Retained inputs: Elementary_vector_spaces.

Replacement span `97632:97858`, SHA `2e1d530eef6951a90b3d20d8f0b7e16b99f3d2f75becd752982bba794532e792`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C8 — N008 Proposition 3.7

A firm coset geometry of a finite p-group is RWPRI iff it is RPRI.

Source: `sources/phase16_frattini_geometries.txt`, span `15082:16216`, SHA `b7f9b26b414f8caf33245f25a99c205c427fb8a718efdfc11ba5a890e1ef2e47`.

Common result: Theorems R(b), E2, S and E5.

**Corollary C8 — N008 Proposition 3.7.** A firm coset geometry of a finite p-group is RWPRI if and only if it is RPRI. E5 proves the nontrivial implication; the converse is immediate from the definitions.

Retained inputs: Elementary, PΦ, Burnside_basis.

Replacement span `97858:98064`, SHA `63cd51706c06544b77c299e0699130758fc7b914188dd2f7e106c9580682db7e`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C9 — N008 Theorem 3.8

A firm RWPRI coset geometry of a p-group is a direct sum of primitive rank-one geometries. The source section fixes finite p-groups, although this theorem sentence omits the word finite.

Source: `sources/phase16_frattini_geometries.txt`, span `16216:17203`, SHA `e64f3c38c2a9408ee3e03b3dc94283963c576d59db781d65351a93fd7e162110`.

Common result: Theorems R(b), E2, S and E5.

**Corollary C9 — N008 Theorem 3.8, finite-p-group context.** Every firm RWPRI coset geometry of a finite p-group is a direct sum of primitive geometries of rank one. This is E5; each summand has exactly \(p\) points.

Retained inputs: Elementary, PΦ, Burnside_basis.

Replacement span `98064:98282`, SHA `bcf9193ad359f78e623e65fbb1f110008b48bc2093c6ce34077fbb5655b0bd86`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C10 — N008 Section4.2

For every residue at a flag of type J, Phi(H_J)<=H_J intersect H_i for every remaining type i; this is necessary, not sufficient.

Source: `sources/phase16_frattini_geometries.txt`, span `18463:19655`, SHA `5b8d9385ec704c9d8271bcdf972f91e0588f27ea2fd6a356dc92648e1cb9c7cd`.

Common result: E2,E3, equationA6.7.

**Corollary C10 — N008 §4.2.** For each standard flag of type \(J\), \(\Phi(H_J)\) must lie in every \(H_J\cap H_i\), \(i\notin J\). This is (A6.7), derived by applying E2 in each residue.

Retained inputs: Elementary, Zorn_if_infinite_group.

Replacement span `98282:98472`, SHA `13669c1f46c23d7d5cee5bc31827d4bfa6df22fe34d0c6a9f8f290e3177760eb`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### C11 — N008 Section4.3

The largest normal subgroup of G contained in B is core_G(B)=intersection_i core_G(H_i); quotienting yields the faithful coset action, and for firm RWPRI geometries this kernel contains Phi(G). The separately cited Archer2004 classification at the end of this section is retained, not newly proved.

Source: `sources/phase16_frattini_geometries.txt`, span `19932:20621`, SHA `51dcc56be4b231963388408499bb88eaa05220f62e284a87c2054f2321371be8`.

Common result: E2,E3, equationA6.4; common Theorem K(b) through Corollary E3.

**Corollary C11 — N008 §4.3, action-kernel assertion.** The largest normal subgroup of \(G\) contained in the Borel is \(\operatorname{core}_G(B)=\bigcap_i\operatorname{core}_G(H_i)\). Quotienting by it preserves the geometry and makes the action faithful; for firm RWPRI geometries it contains \(\Phi(G)\). This is (A6.4), E3 and E2.

Retained inputs: Elementary, Zorn_if_infinite_group_for_Frattini_containment.

Replacement span `98472:98808`, SHA `8949e40a9717c6e446a9d4d3a62536af5395b615bc9e9232b9fd0430814464ff`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D1 — L032 Theorem 1.2

**Corollary D1 — L032 Theorem 1.2.** For every \(d\ge3\), \(n\ge5\) and \(k_1,\ldots,k_{d-1}\ge2\) with \(\sum_i k_i\le n-1\), there is a regular rank-\(d\) polytope with automorphism group of exact order \(2^n\) and type \(\{2^{k_1},\ldots,2^{k_{d-1}}\}\).

Source: `sources/catalogue_L032.txt`, span `4673:4887`, SHA `918b01d61ace54eda1f4bf39cbdf8339b2f509400186e268be4efaf97c614dbf`.

Common result: Q2.2,Q2.4,Q3.1,Q4.1.

Corollary Q4.1 constructs its marked string C-group using the single square seed and independent cyclic edge kernels. Apply the retained regular-polytope correspondence. ∎

Retained inputs: Regular_polytope_Cgroup, Gaussian_integer_Euclidean_geometry.

Replacement span `98808:99249`, SHA `2328c6919056f5bf82bb1875ead246e2a7443e14870fe738853222b71cf4baa0`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D2 — L035 Theorem 1.2

**Corollary D2 — L035 Theorem 1.2.** For \(n\ge10\), \(s,t\ge2\) and \(s+t\le n-1\), there is a regular rank-three polytope of order \(2^n\) and type \(\{2^s,2^t\}\).

Source: `sources/catalogue_L035.txt`, span `2875:3034`, SHA `b411e7d94ef26100683a2a4f379457c4ae788c541c4b2411cffd661a9e7ff164`.

Common result: Q4.1,D1.

Set \(d=3\) in D1. The construction and proof are shared, with no second seed. ∎

Retained inputs: Regular_polytope_Cgroup, Gaussian_integer_Euclidean_geometry.

Replacement span `99249:99508`, SHA `49dd369f227fb654d446cb1a1b767552b5dacad818861dfa73e3e95c1be1c354`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D3 — L035 Theorem 1.3(1–3), all eight presentations

**Corollary D3 — L035 Theorem 1.3, all three parts and eight presentations.** Let \(n\ge10\). Every marked rank-three string C-group of order \(2^n\) and type \(\{4,2^{n-s}\}\), for \(s\in\{3,4,5\}\), is exactly one of the following marked presentations. Put \(m=2^{n-s}\), \(r=bc\), \(d_0=(ab)^2\), and \(z=r^{m/2}\). All have common relations
\[
a^2=b^2=c^2=(ac)^2=(ab)^4=r^m=1.
\]
For \(s=3\), add \([d_0,c]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_1,G_2\). For \(s=4\), add \([d_0,r^2]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_3,G_4\). For \(s=5\), add
\[
[a,r^2]^2=z^\beta,\qquad [a,r^4]=z^\nu,
\]
with \((\beta,\nu)=(0,0),(1,0),(0,1),(1,1)\), giving \(G_5,G_6,G_7,G_8\), respectively. Conversely each bare presentation has the stated exact order, type and IP; the alternatives are distinct as marked string C-groups.

Source: `sources/catalogue_L035.txt`, span `3789:4992`, SHA `eb05d590bbfbd29ca447e231c5a9e5afe75bb734bdd04555f1c7dee550dd1ce1`.

Common result: Q3.1,Q6.1,Q7.1,Appendix A.

Theorem Q6.1 gives the bounded cyclic quotient. The explicit models and invariant relations in §12 construct and distinguish every listed marking. Theorem Q7.1 gives completeness, excludes the nonlifting order-256 relation patterns and identifies every bare presentation by its order bound. The complete finite relation computation and its exhaustiveness proof are in Appendix A. Thus the converse does not assume the presented group already has the desired order or IP. ∎

Retained inputs: Burnside_basis, Lucchini_cyclic_core, SmallGroups_256_completeness, Gaussian_integer_Euclidean_geometry.

Replacement span `99508:100829`, SHA `4da3a768c0efcec79f3ef6388ff397b53b4467c0c250bdf930be5cd8e2ef6ec2`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D4 — F013 Theorem 1.1

**Corollary D4 — F013 Theorem 1.1.** Every finite nondegenerate two-group string C-group of rank \(d\ge2\) admits a marked epimorphism onto the canonical string C-group \(G(C_d)\) of order \(2^{2d-1}\).

Source: `sources/catalogue_F013.txt`, span `2770:3006`, SHA `6e08702fb9925058e4965fd2433330e7ef553c2504b6c923a1821fa98ed48b46`.

Common result: S,Q5.1,Q5.2,Q5.3,Q5.4.

Its noncommuting diagram is a path. Theorem Q5.3 identifies its quotient by \(\gamma_3(G)\) with the explicit vertex-and-edge model. Corollary Q5.4 identifies that model with \(G(C_d)\). The Frattini/basis input is the common Theorem S, and the graded support proof is included in §11. ∎

Retained inputs: Burnside_basis, Finite_nilpotency_graded_Lie.

Replacement span `100829:101331`, SHA `e1632379c0e1a8b45c26762897bb05dfc73ace16d05e64a898bb697b535d8783`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D5 — F013 Theorem 1.2

**Corollary D5 — F013 Theorem 1.2.** Every finite nondegenerate regular rank-\(d\) polytope with two-group automorphism group, \(d\ge2\), covers \(C_d\).

Source: `sources/catalogue_F013.txt`, span `3006:3162`, SHA `9cfa759af129aa4828fdc14fbeb945b025e5021fa8952beefe332c234dbe166c`.

Common result: Q5.4,D4.

Apply D4 and the retained marked quotient/cover correspondence. The false auxiliary source kernel is not needed; §16 proves its precise failure. ∎

Retained inputs: Burnside_basis, Finite_nilpotency_graded_Lie, Marked_quotient_cover.

Replacement span `101331:101643`, SHA `a6856f343965effb2259d9350fca33123e3647b25eac164b4da3cf52d2552f75`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D6 — F016 Theorem 5.1(a–d)

**Corollary D6 — F016 Theorem 5.1(a–d).** For \(d\ge3\) and \(n_3,\ldots,n_d\ge5\), there is a finite regular rank-\(d\) polytope whose consecutive rank-three sections are exactly \(\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\), where each square map has automorphism group of order \(2^{n_j}\). Its group has order \(2^{\sum_{j=3}^d n_j-3(d-3)}\). For \(d\ge4\) it is \((d-4,d-1)\)-flat and hence flat. It has FAP with respect to its co-\((d-4)\)-faces, co-\((d-3)\)-faces and facets, with the rank-three co-\((-1)\)-face interpreted as the whole-polytope cut.

Source: `sources/symmetric_2groups2025.txt`, span `22646:23043`, SHA `27003fdfc527f6b58241dcaeb7fa4dcaea181b1833ff5d988155d76614609bb7`.

Common result: Q2.2,Q2.3,Q3.1,§14.

The square recognition theorem and compatible product Q2.3 give the exact local sections. Equation (Q8.1) gives the order. The last product factorization gives flatness through the retained coset-face criterion, and Q2.2 supplies the actual deletion retractions and all FAP cuts. These arguments, including the rank-three convention, are all in §14. ∎

Retained inputs: Regular_polytope_Cgroup, Gaussian_integer_Euclidean_geometry.

Replacement span `101643:102563`, SHA `954ee00f04dc4a342e9c23ebb3242a8897e44db2cd1b3dd5789b9ced9bb1826b`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D7 — F016 Theorem 5.3

**Corollary D7 — F016 Theorem 5.3.** The automorphism group in D6 is precisely the quotient of the universal regular polytope group of generalized type \(\{\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\}\) by
\[
[(r_ir_{i+1})^2,(r_{i+2}r_{i+3})^2]=1
\quad(0\le i\le d-4).
\]

Source: `sources/symmetric_2groups2025.txt`, span `30226:30474`, SHA `2d0e88859bc65bf5c02ddbaae1b91241257c83590c020bcee8198cc8648633e6`.

Common result: Q2.2,Q8.1,§14.

Section 14 proves Boolean deletions and IP for the bare local presentation, so the universal regular polytope exists by the ordinary C-group correspondence. Lemma Q8.1 makes the third-lower-central triple kernels normal. The local lattice indices, global class-two bound and order comparison identify the quotient with the actual product construction. This retains the source's entire presentation claim and repairs the diagonal-translation order step. ∎

Retained inputs: Regular_polytope_Cgroup, Gaussian_integer_Euclidean_geometry.

Replacement span `102563:103297`, SHA `5789eaaba488142c4f68adc8bdcb38a177a12364a5bcb104d95b2aa8d992563f`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D8 — F016 Theorem 6.1(a–b)

**Corollary D8 — F016 Theorem 6.1(a–b).** Let \(d\ge4\), \(n_3,\ldots,n_{d-1}\ge5\), and \(m_{d-1}\ge5\). There is an alternating semiregular rank-\(d\) polytope with regular facet types
\[
(n_3,\ldots,n_{d-2},n_{d-1}),\qquad
(n_3,\ldots,n_{d-2},m_{d-1}).
\]
Its full automorphism group has order
\[
2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}
\]
if the last parameters differ, and twice this order if they agree. At \(d=4\), the shared list is empty and the common facet of the two facets is a square. The remaining co-\((d-4)\)-section is not separately prescribed.

Source: `sources/symmetric_2groups2025.txt`, span `38193:38628`, SHA `8b5d68533a15b8f0e16b97209475044886fc5d859ff04788a8c1fef9b7536d19`.

Common result: Q2.3,§15.

Use D6 for the two facet groups, Q2.3 for the branched compatible product, and the exact retained Monson–Schulte assembly/full-automorphism input in §15. The orders there give the displayed formula, while unequal facet orders exclude an interchange and equal marked constructions admit it. ∎

Retained inputs: Monson_Schulte_2020_5.3, Regular_polytope_Cgroup.

Replacement span `103297:104171`, SHA `4bdef6f81c42814ed402b7a6bed9fb47700138c14e7cef58391b7b0b35a7afad`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D9 — F016 Theorem 7.1

**Corollary D9 — F016 Theorem 7.1.** For a regular input polytope of rank \(d\ge3\) whose group is a finite or infinite two-group in the source's convention, its free regular extension has rank \(d+1\) and finitely generated infinite automorphism group with every finite-order element of two-power order.

Source: `sources/symmetric_2groups2025.txt`, span `42668:42871`, SHA `2d1ea4d54a0a19dfc3781234cbc8c51468bb0187684a2750b3740f748c6ae01a`.

Common result: Q9.1,§15.

The retained regular free-extension theorem gives the geometry and its amalgam. Lemma Q9.1 proves infinitude, finite generation and the finite-torsion assertion, including infinite input. ∎

Retained inputs: Regular_free_extension, Amalgam_normal_form.

Replacement span `104171:104677`, SHA `ccfecb247e3f179e301736c1150f54bd8c39cbb3568c2ec561b486e5495dfdb6`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D10 — F016 Theorem 7.2

**Corollary D10 — F016 Theorem 7.2.** For an oriented chiral input polytope of rank \(d\ge3\) with directly regular facets and finite or infinite two-group automorphism group, its free oriented chiral extension has rank \(d+1\) and a finitely generated infinite two-group in the same convention.

Source: `sources/symmetric_2groups2025.txt`, span `45068:45333`, SHA `b045c2c8f10b41e5aec6a8fa45345b69576f3cbf59d505ed58127ec875829e8e`.

Common result: Q9.1,§15.

The retained Schulte–Weiss theorem gives the geometry and amalgam over the facet rotation group. That rotation group embeds in the input group; its full facet group is an index-two extension, so Lemma Q9.1 transfers the torsion property and proves the extension conclusions. No full-facet embedding in the chiral group is assumed. ∎

Retained inputs: Schulte_Weiss_1995, Amalgam_normal_form.

Replacement span `104677:105317`, SHA `12e150b6b90031fb2f5ad87d14e356ad0fba02260df5cb6455bff8552f133f11`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

### D11 — F016 Theorem 7.3

**Corollary D11 — F016 Theorem 7.3.** Let two regular rank-\(d\) polytopes, \(d\ge3\), have isomorphic facets and finite or infinite two-group automorphism groups. Their universal alternating semiregular extension has rank \(d+1\) and finitely generated infinite two-group automorphism group, with the additional branch swap precisely when the two facets of the extension are isomorphic.

Source: `sources/symmetric_2groups2025.txt`, span `47369:47687`, SHA `097d03c0f60ccc54e7611255538bc756af76ccbddf92340034156f6689e5e798`.

Common result: Q9.1,§15.

The retained universal alternating-extension theorem gives the group amalgam and possible index-two extension. Lemma Q9.1 gives all three group properties in both cases. ∎

Retained inputs: Monson_Schulte_2012_2021, Amalgam_normal_form.

Replacement span `105317:105888`, SHA `cbeb7cfb5ba4e2d5e3b6b36a177dd5ba99687a0da0d7e19351b7e14b5f3dad60`.

Status: complete author argument, inherited scoped/corrected contract, pending new integration review.

## Retained dependencies and source corrections

B97 classification, Whiston W1 and the separate CFSG-dependent W2 remain explicit. Gaschütz and Archer are quoted source imports, not new proved targets. Burnside, finite nilpotency/graded Lie, Gaussian-integer and plane geometry, Lucchini cyclic-core theorem, SmallGroups order256 catalogue completeness, geometric alternating/free-extension interfaces and amalgam normal form are all retained and charged. Appendix A is inside the manuscript; required executable2455bytes and certificate396bytes remain separate costs. All original hash-bound logs/reviews stay unchanged.

The unrestricted infinite N008 converse and specified F013 auxiliary assertions are visibly corrected. Symmetric n≥7, finite numerical invariants/finite-p classification, L035n≥10 and F016standingd≥3 are preserved. All17four-paper clause rows and all10N008numbereditems (including retainedGaschütz) remain in the JSON inventory.

## What changed and what did not disappear

The common K theorem contains both real kernel arguments; moving them is not a saving by itself. Theorem S replaces the repeated relative-coordinate argument and provides the shared Frattini restriction used in the two-group branch. R and the ladder remain complete once. The entire symmetric Whiston/laminar branch survives because odd braid relations obstruct Boolean deletion. Complete lattice/cyclic model/finitecensus/presentation proofs survive. Extra bridge face-index consequences are omitted because they do not remove a required source proof. Numerical before/after block costs are in the accounting artifact; no net shortening is asserted.
