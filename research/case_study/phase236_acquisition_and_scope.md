# Phase 236: acquisition decision and exact working target

The assigned older candidates were checked before moving to the authorized fallback.

* L085, *Almost simple groups of Suzuki type acting on polytopes*: the original DOI is 10.1090/S0002-9939-06-08448-6. The publisher PDF returned HTTP403 on the fresh attempt; author URL variants were unavailable. ULB's recorded deposit is marked restricted intranet. No login or author contact was attempted. `sources/phase5_L085.pdf` and `_ulb.pdf` are HTML responses. Crucially, `sources/phase16_L085_author.response` is a genuine PDF **of the later Kiefer–Leemans L074 counting paper**, not the original L085. It cannot establish original-primary intake.
* L089, *On inductively minimal geometries that satisfy the intersection property*: the primary ScienceDirect URL for PII S0097316505000038 returned403. The VUB institutional record was found, but no complete primary was obtained. `sources/catalogue_L089.pdf` is login HTML.
* L109, *The residually weakly primitive geometries of the dihedral groups*: the author abstract and bibliographic records were found; no complete primary was obtained. No source credit follows from these abstracts.

The exact-title searches included the three full titles, the Suzuki DOI, `szpoly.pdf`, `imgip.pdf`, and title+filetype:pdf variants. These were bounded acquisition searches, not claims of exhaustive unavailability.

Root then authorized L012/L014 as the preferred fallback. The working source is **L014**, the complete twelve-page primary `sources/regular_4pm2025.pdf` (arXiv2407.10388v1,15July2024). The full text has now been read. L012 is not yet part of this contract.

The three principal targets are its Theorems1.1,1.2,1.3 (the last with explicit construction Theorem5.1): the normal Sylow p-kernel and its two generators; classification of the abelian/tight case; and the nonabelian {p,2p} family for every odd prime p and every m≥3.

The literal marking displayed in Theorem1.2 on physicalp2 has a defect confirmed visually: it says r1=xy r0, while the same presentation says x^r0=x and y^r0=y^-1. Its square is x², not1. The body uses r1=xy r2 in its B×D case. The corrected model assigns x order p^b, y order p^a with1≤a≤b, r0 fixesx and invertsy, r2 invertsboth, and r1=xy r2. Its type is {2p^a,p^b}. This correction will be kept separate from the attribution of the classification. No claim is made that the published journal edition retains the author's v1 typo.

The proposed common construction uses A=Z[ζ_p]/(ζ_p−1)^(m−1), P=A⋊C_p, and commuting involutions from complex conjugation and negation. It directly models the source's generators s_i=(ζ_p−1)^(i−1). The arithmetic and the exact source-presentation bridge still require complete written proof and tests before freeze.

For the tight⇒abelian direction, the exact retained input is Cunningham–Pellicer, *Classification of tight regular polyhedra*, arXiv1408.6703v2, Theorem1.1 on physicalp2: an odd face parameter and an even vertex parameter admit a tight regular polyhedron exactly when the latter divides twice the former, and the polyhedron is unique. The primary PDF and theorem were read through the web tool at https://arxiv.org/pdf/1408.6703v2. Local curl acquisition currently fails DNS; no local primary PDF bytes or hash are claimed. The retained theorem is also explicitly the input used by L014, not a result to be attributed to this project.
