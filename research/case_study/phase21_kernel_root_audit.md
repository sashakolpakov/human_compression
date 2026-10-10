# Root review of the invariant-kernel method and N009 adapters

10 October 2026. **PASS within the stated finite and written scope.**
The associated JSON binds the reviewed sources, reports and fresh runs.

Root checked the universal-group proof, the invariant index-two ladder,
the exact kernel-profile criterion, and the implementation. Deleting marked
generators respects both the path relations and the nilpotency law, so the
universal marking has actual IP. Deletion also proves the required
restriction of gamma3 directly. A desired excess-three quotient has a
unique kernel inside gamma3 of index eight, by the canonical class-two
quotient and the order calculation.

Every invariant index-two step is a hyperplane in the Frattini/commutator
coinvariant quotient. A two-group acting on the nonzero characters has
a fixed character by the odd orbit count. This proves that the ladder
reaches every kernel of the specified index. The final code explicitly
checks all ambient relative pc orders are two before using binary keys,
so its canonical pc generating sequences give injective subgroup keys.
No expected census count or author presentation filters the search.

Kernel profiles have exact meets if and only if the quotient marking has
actual IP, since their images in the canonical quotient already have IP.
The small-kernel test uses unordered distinct subset pairs; diagonal pairs
are identities and reversed pairs add no condition. Every accepted group
is nevertheless built and checked on all ordered pairs of marked subsets.
Rejected profiles are justified by the proved equivalence, rather than
an assumption that IP descends to quotients.

Root freshly ran the frozen guarded code at rank four with GAP 4.15.1
and NQ 2.5.11. It found 1,483 kernels, rejected 1,284 by 73,880 small-kernel
meet comparisons, and directly verified all 50,944 meets of the 199
accepted markings. Eleven are fixed by reversal, giving 105 classes.
The thirteen type counts agree individually with N009 Table 6. This
reruns the author's cases; it does not add parameter coverage. The root
log's optional-checkpoint syntax warnings arise because that run requested
no checkpoint files; the census completed successfully.

Root also reviewed the complete central-quotient and relator-lift argument.
The unique dihedral product normal form reduces the central obstruction
to five words. The Burnside-basis argument excludes the last mixed word,
and the two quotient cases preserve the marked intersections. The
iteration correctly stops at C2^3. The three lift patterns and the
presentation order sandwich recover the specified source results, with
no assertion that every arbitrary relator choice succeeds. Root compared
the exact theorem statements on printed pp.7–9 of the private primary
extraction; this was selected reading, not a whole-paper audit.

For Theorem 5.5, root compared the two relator lists against printed p.20
and freshly ran the unchanged checker. Todd–Coxeter enumeration over the
trivial subgroup gives 1,024 cosets in each raw presentation. The resulting
regular permutation images have order 1,024, providing both bounds on
the presented group orders. Both have type (4,4,4), oriented facet orders
(128,64), and all 512 combined marked meets pass. The two ordered markings
are distinct. No nilpotent-class relators are added in this test.

The named facet groups require more than their orders: the previously
reviewed first- and second-excess classifications give uniqueness of
the type-(4,4) markings at orders 64 and 128. The complete rank-four
census has exactly two accepted markings with these oriented facets.
Together these facts establish the stated two-case classification.

The finite census retains the exact GAP/NQ algorithms. It is not a Lean
formalization or a proof of an all-rank third-excess formula. The central
adapters and rank-four census do not recover the source's rank-three
order-1024 list or every other displayed presentation. No whole-paper
credit, matched proof-length ratio, priority claim or infinity marker
is assigned by this review.
