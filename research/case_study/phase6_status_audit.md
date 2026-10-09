# Phase 6: priority and status audit

Audit date: 2026-10-10. This is a bounded literature audit, not an assertion of priority or proof that no earlier solution exists. The four project proofs remain **proposed resolutions with internal reviews**. No later primary publication explicitly settling any of the four exact targets was identified in this search. That negative search result does not certify that the targets remained open until this project.

## L102: the one-dimensional affine spread question

Buekenhout, Dehaye and Leemans, *RWPRI and (2T)1 flag-transitive linear spaces*, Beiträge zur Algebra und Geometrie 44 (2003), 25–46: [primary paper](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf). Section 5.1.2, printed page 39, asks whether its remaining spread case is necessarily Desarguesian; Theorem 6.1(1) retains this case. The target requires both local primitivity conditions, not merely flag transitivity of an affine group.

The project [descent proof](phase4_old_problem_audit.md) handles a spread of proper nonzero F_p-subspaces in F_(p^d), with a subgroup of ΓL(1,p^d) primitive on the spread and its member stabilizers irreducible on their members. It identifies the spread with the one-dimensional F_(p^l)-subspaces. Its existence converse uses the designated affine scalar group when (p^d−1)/(p^l−1) is prime. This is a narrow case identification, not a new classification of all affine flag-transitive spaces.

Later primary literature examined or rechecked:

- Pauley–Bamberg, *A construction of one-dimensional affine flag-transitive linear spaces*, Finite Fields and Their Applications 14 (2008), 537–548, [DOI](https://doi.org/10.1016/j.ffa.2007.07.006), [author copy](https://cage.ugent.be/~bamberg/Research_files/A%20construction%20of%201D%20affine%20flagtrans%20linear%20spaces.pdf): its cyclic spread construction does not impose both local primitivity assumptions.
- Feng–Lu, *New families of flag-transitive linear spaces*, [arXiv:2108.03848](https://arxiv.org/abs/2108.03848), and Jameson–Sheekey, *Cyclic 2-Spreads in V(6,q) and Flag-Transitive Affine Linear Spaces*, [arXiv:2309.06872](https://arxiv.org/abs/2309.06872), concern broader cyclic spread constructions. For the latter parameter family the pencil size q^4+q^2+1 factors into two nontrivial integers; these examples do not meet the prime pencil condition derived in our one-dimensional case.
- Guan–Zhou, *Extremely primitive groups and linear spaces*, Czech Mathematical Journal 66 (2016), 445–455, [primary paper](https://dml.cz/bitstream/handle/10338.dmlcz/145735/CzechMathJ_66-2016-2_12.pdf), and Lee–Verret, *Extremely primitive groups and linear spaces*, Designs, Codes and Cryptography 91 (2023), 3227–3240, [primary preprint](https://arxiv.org/abs/2211.02198), use extreme primitivity on point suborbits. This differs from the two local conditions here. Lee–Verret Theorems 1.1–1.2 and the refinement framework were read; no claim that those theorems settle this exact spread question was found.

**Status boundary:** no explicit later resolution found; the project application of cyclic semilinear descent is a priority candidate only. The broader non-Desarguesian spread literature cannot be used to refute or settle the narrower question without checking the local actions.

## L092: the Hermitian-unital construction

Leemans, *A generalization of a construction due to Van Nypelseer*, Beiträge zur Algebra und Geometrie 46 (2005), 561–574: [primary paper](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf). Conjecture 1 in Section 4.6, printed page 569, asserts firmness, residual connectedness and flag transitivity of Γ(U_H(q)) for every prime power q>2. Its three types are unital points, blocks, and incident point–block pairs, with the modified incidences of Construction 3.

The project [proof](hermitian_unital_proof.md) identifies the difficult residue with a norm shell on which SU(2,q) acts regularly, and proves connectivity through root subgroup moves. The chamber action comes from PGU(3,q).

A potentially confusing later paper was checked in its final form: Delaby–Leemans–Tranchida, *Geometries with trialities arising from linear spaces*, Algebraic Combinatorics 9 (2026), [DOI and final text](https://alco.centre-mersenne.org/articles/10.5802/alco.482/). Theorems 1.1–1.2 concern a different construction Δ using three copies of flags. The restriction to Hermitian unitals with q=2 or 4 there is not a restriction on the 2005 construction Γ. Its Theorem 4.2 also restates a linear-space classification; it does not supply a new proof of the L102 remaining RWPRI case.

**Status boundary:** no later primary explicit settlement of the 2005 conjecture was found. The two unital geometries must remain distinct in any status or novelty statement.

## L114: printed Suzuki realization questions

Leemans, *The rank 3 geometries of the simple Suzuki groups Sz(q)*, Note di Matematica 19 (1999), 43–63: [primary paper](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837). Its final discussion distinguishes the candidate subgroup configurations in Theorems 5.3–5.5 from their realization; it verifies the relevant small-group case Sz(8).

The later paper L110, *The residually weakly primitive pre-geometries of the Suzuki simple groups*, Note di Matematica 20 (2000/01), 1–20, [primary paper](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995), republishes rank-three candidate shapes and develops higher ranks. Its page 11 discussion separately raises flag-transitivity issues. Reprinting a candidate diagram is not by itself a coordinate proof of simultaneous subgroup embeddings or of residual weak primitivity. Conversely, an embedding does not prove flag transitivity.

The project [first realization note](phase5_suzuki_realization.md) and [higher-case note](phase5_suzuki_higher.md) give all-parameter decisions for the listed Theorem 5.3 and 5.5 shapes, retaining the source subgroup-classification inputs. In Theorem 5.5, shapes 1, 2, 3, 5 and 9 are ruled out under the stated geometric conditions; shapes 4, 6, 7, 8 and 10 are realized. These are proposed corrections/completions, rather than a claim that every historical author regarded every case as open subsequently.

Later papers with nearby titles answer different questions. *On the rank of Suzuki polytopes: An answer to Hubard and Leemans* (2021), [DOI](https://doi.org/10.1016/j.disc.2021.112331), proves that chiral polytopes with an almost simple Suzuki automorphism group have rank three. Leemans–Stokes–Tranchida, *Flag transitive geometries with trialities and no dualities coming from Suzuki groups* (2025), [primary preprint](https://arxiv.org/abs/2311.13522), constructs another family; its triality conditions do not constitute an audit of the old catalogue.

**Status boundary:** no later explicit correction or settlement of these exact printed realization issues was found. Our source-level distinction between candidate subgroups, RWPRI and flag transitivity is essential.

## L043: the PSL(2,q) field conjectures

Leemans–Moerenhout–O’Reilly-Regueiro, *Projective linear groups as automorphism groups of chiral polytopes*, Journal of Geometry 108 (2017), 675–702: [journal](https://doi.org/10.1007/s00022-016-0367-6), [primary preprint](https://arxiv.org/abs/1606.08017). Conjecture 6.1 asks, for odd prime p and odd e_1,e_2>1, for primitive j_i in F_(p^e_i) such that, putting u_i=j_i+j_i^−1, the quantity u_1²u_2²−4(u_1²+u_2²) is a square in F_(p^lcm(e_1,e_2)). Conjecture 6.2 asserts the required middle-parabolic intersection for the displayed matrix construction when e_1,e_2 are coprime. The exact matrices and quantifiers are retained in the project [intersection proof](psl2_intersection_proof.md); [square proof](psl2_square_proof.md) addresses the first conjecture.

There is positive later status evidence: Section 7 of Leemans–Vandenschrick, *On chiral polytopes having a group PSL(3,q) as automorphism group*, Journal of the London Mathematical Society (2022), [accepted final paper](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf), printed manuscript page 24, still identifies the missing PSL(2,p^d) family with p^d≡3 mod 4, d>1 not a prime power. This establishes a later historical open-status checkpoint, not current open status.

The 2016 arXiv record still has one version. Tranchida, *Triples of involutions in PGL(2,q) and their incidence geometries*, Innovations in Incidence Geometry 22 (2025), 25–46, [primary preprint](https://arxiv.org/abs/2411.10299), was checked through its introductory principal theorems. Its strongly non-self-polar triangle criterion concerns regular rank-three hypertopes, not these chiral rank-four field conjectures. No explicit settlement was found in the later citation/keyword searches.

**Status boundary:** no claim of a first solution follows merely from these searches. The project's proposed classification consequence still requires its written group-generation and chirality arguments, not only the finite-field calculation.

## Cara 2003 and general-framework prior art

Cara, *Truncations of inductively minimal geometries*, Discrete Mathematics 267 (2003), 63–74, [DOI](https://doi.org/10.1016/S0012-365X(02)00603-9), remains **abstract/metadata only** in this intake. Attempts through the publisher article/PDF endpoint, Elsevier API, institutional author page and indexed repositories did not return the full paper. An open-archive metadata label did not yield a readable full text. Therefore the independent [weighted-tree theorem](phase6_weighted_tree.md) must not be presented as a theorem-by-theorem recovery of Cara's entire paper. Its model-level proof and finite checks were independently reviewed separately.

The new network intake records N005–N007, three Piedade–Tranchida preprints from 2025–2026 on operations on coset geometries. N005 is particularly relevant prior art for any broad extension framework; its Section 1.1, Proposition 2.2 and selected construction definitions/theorem statements were read. This is not a whole-paper proof audit. Exact reading scope and retained admissibility inputs appear in [network intake](phase6_network_intake.json). No compression ratio or general-framework novelty is inferred from the intake.

## Search boundary and reproducibility

This phase used exact-title, author, conjecture, construction and group-family searches; primary journal/preprint pages; author publication lists; and a bounded citation discovery pass. OpenAlex records and citing lists were used only for discovery. They contain incomplete citation counts and, for the old Suzuki items, incorrect dates. Their silence is not evidence of an open problem. Titles outside the exact targets were screened; not every citing paper was read in full. Existing primary full texts and the substantive sections identified above were used for mathematical comparisons. No authors were contacted.

The companion JSON records exact source anchors, proof artifacts, reading scope and search limitations. External full texts remain excluded from the public package. No pre-existing proof/checker/certificate was changed by this audit.
