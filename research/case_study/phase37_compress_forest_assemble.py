"""Assemble a new integrated three-paper manuscript from reviewed private inputs.

All source and phase36 files are read-only inputs. No length ratio is assigned.
"""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
INPUTS={
 'phase36_compress_forest_manuscript.md':'f006b562bfd49aba28d6d7f76fe46fa4bedc8a10ef24f9dfbf2e6d5a3ee9fcaa',
 'phase36_compress_forest_N008_extension.md':'4135acdce5fb3177cf8edb92b5444543f96d67e10a563a5f5833ad0c88d2effc',
 'phase36_compress_forest_recent_audit.json':'da82ed214679c25234d34f8444a3a87fd2056a9271b5b4d205a20a3d9ba73958',
 'phase36_compress_forest_N008_recent_audit.json':'23cbf5feb2a87955e21819814df50b5c6ec41f2b24fee27cb747cfe581a24032',
}
def sha(data): return hashlib.sha256(data).hexdigest()
for name,digest in INPUTS.items():
 assert sha((ROOT/name).read_bytes())==digest,name
old=(ROOT/'phase36_compress_forest_manuscript.md').read_text()
ext=(ROOT/'phase36_compress_forest_N008_extension.md').read_text()
def between(s,start,end):
 a=s.index(start); b=s.index(end,a)
 return s[a:b]
def replace_once(s,old,new):
 assert s.count(old)==1,(old[:120],s.count(old))
 return s.replace(old,new,1)

core=between(old,'## 1. Conventions','## 6. The twelve')
core=replace_once(core,
 'All groups and sets in this manuscript are finite. Write',
 'All type sets and forests are finite, as are the domains of the symmetric groups. The normal-quotient bounds and numerical invariants \\(\\mu,\\mu^{\\prime}\\) are used for finite groups; the relative parabolic-generation formula and the Frattini results explicitly allow arbitrary groups with finite rank where stated. Their coset sets may be infinite. The p-group classification is for finite p-groups. Write')
core=replace_once(core,'A flag is a pairwise incident set; a chamber has every type.',
 'A flag is a pairwise incident set; a chamber has every type. Every flag of a geometry is required to extend to a chamber.')
core=replace_once(core,'We always keep the specified flag-transitive group action as part of the pair.',
 'We keep the specified group action as part of the pair. The N001/N003 source coset convention includes flag transitivity; for the firm-RWPRI assertions it follows from Lemma E0 below.')
core=replace_once(core,'The pair is **PRI** if every \\(H_i\\) is maximal in \\(G\\), and **WPRI** if at least one is. The residual versions are RPRI and RWPRI. In these terms RWPRI is precisely:',
 'For a group acting on a geometry, the pair is **PRI** if its action on every type is primitive, and **WPRI** if its action on at least one type is primitive. The residual versions, applied in each residue including the whole geometry, are RPRI and RWPRI. For flag-transitive coset data these say that every, or at least one, corresponding type stabilizer is maximal; RWPRI is precisely:')
core=replace_once(core,'A subgroup is **quasi-maximal** if the interval from it to the ambient group in the subgroup lattice is a chain, equivalently if it has a unique saturated subgroup chain to that group;',
 'For the finite groups in the N001 branch, a subgroup is **quasi-maximal** if the interval from it to the ambient group in the subgroup lattice is a chain, equivalently if it has a unique saturated subgroup chain to that group;')
core=replace_once(core,'None of the twelve target conclusions is used as background.',
 'None of the declared target conclusions is used as background.')
core=replace_once(core,'Elementary finite group theory, permutation parity,',
 'Elementary group theory, permutation parity,')
# Add the independently reviewed finite-rank flag-transitivity proof once.
e0=between(ext,'**Lemma E0','The same choices are independent')
e0=replace_once(e0,"**Lemma E0 (the source's flag-transitivity convention is automatic here).**",
 '**Lemma E0 (residual weak primitivity and flags).**')
e0=replace_once(e0,"This justifies the source's subgroup translation without inserting an unprinted flag-transitivity hypothesis into its firm-RWPRI conclusions.",
 'Thus the firm-RWPRI results below need no extra assumption of flag transitivity or residual connectedness.')
core=replace_once(core,'The following are the unexpanded mathematical inputs.',e0+'The following are the unexpanded mathematical inputs.')
extra_inputs=r'''

**PΦ (finite-p-group Frattini quotient).** For every finite p-group \(P\), the quotient \(P/\Phi(P)\) is an elementary abelian p-group, hence a finite-dimensional vector space over \(\mathbb F_p\). Here \(\Phi(P)\) is the intersection of the maximal subgroups. We retain this elementary group-theoretic fact in the form recalled in [ACK05], page 174. Zorn's lemma is retained for the explicitly infinite-group maximal-overgroup arguments. Neither input is a classification of p-group geometries.

For the action-isomorphism convention in Corollary B7, we retain the classical fact that every automorphism of \(S_n\) is inner for \(n\geq7\). Choosing instead the source's equivalence of conjugate coset data gives the same stated marking correspondence.

Two earlier results quoted in [ACK05] remain explicit source imports, not conclusions proved here. Its Theorem 4.1 quotes Gaschütz: if a finite Frattini-free group \(F\) has socle \(S=A\times D\), with \(A\) the product of abelian simple factors and \(D\) the product of nonabelian simple factors, then \(F=A\rtimes K\), where \(D=\operatorname{Inn}(S)\leq K\leq\operatorname{Aut}(S)=\operatorname{Aut}(A)\times\operatorname{Aut}(D)\), and the maximal \(K\)-invariant subgroups of \(A\) have trivial intersection. Its final paragraph quotes Archer's earlier reduction of RPRI geometries that are not direct sums to primitive group actions after removal of the action kernel. These retained results are not used to prove results E0–E5 or any of Corollaries C1–C11; their original proofs are outside this intake.
'''
core=replace_once(core,'## 2. A common forest and flag theorem',extra_inputs+'\n## 2. A common forest and flag theorem')
core=replace_once(core,'(a) For \\(N\\unlhd G\\),','(a) For finite \\(G\\) and \\(N\\unlhd G\\),')
old_statement=r'''(b) A source coset geometry of rank \(r\) with Borel subgroup \(B\) has \(r\leq\mu'(G,B)\). If it is RWPRI, choose any'''
new_statement=r'''(b) A source coset geometry for finite \(G\), of rank \(r\) and Borel subgroup \(B\), has \(r\leq\mu'(G,B)\). More generally, for any finite-rank firm RWPRI geometry with specified group \(G\), possibly infinite, choose any'''
core=replace_once(core,old_statement,new_statement)
core=replace_once(core,r'''In particular \(r\leq\mu(G,B)\), and the family is strongly independent relative to \(B\).''',
 r'''The family is strongly independent relative to \(B\). When \(G\) is finite, this also gives \(r\leq\mu(G,B)\).''')
core=replace_once(core,r'''For (b), (G1) makes the difference in (4.3) nonempty, since its intersection with \(H_i\) is \(B\).''',
 r'''For (b), (G1) makes the difference in (4.3) nonempty, since its intersection with \(H_i\) is \(B\). For a general finite-rank firm RWPRI geometry, Lemma E0 gives flag transitivity and distinct intersections, so the same panel choices exist.''')
core=replace_once(core,r'''Finally \(H_J\cap H_K=H_{J\cup K}\) becomes (1.1), establishing strong relative independence. ∎''',
 r'''Finally \(H_J\cap H_K=H_{J\cup K}\) becomes (1.1), establishing strong relative independence. This part of the proof uses firmness and residual maximality, with no finiteness of \(G\) or separate assumption (G2). ∎''')

# Insert every new Frattini proof once; eliminate duplicate definitions/R proof.
e1=between(ext,'**Lemma E1','## 3. The new common theorem')
e1=replace_once(e1,'*Proof.* Order the proper overgroups of',
 '*Proof.* For finite \\(G\\), choose a proper overgroup of largest order. In general, order the proper overgroups of')
e23=between(ext,'**Theorem E2','## 4. Relative generating families')
e4=between(ext,'**Theorem E4','## 5. Coordinate geometry')
e5=between(ext,'**Theorem E5','## 6. Residual Frattini tests')
residual=between(ext,'For every proper \\(J\\subsetneq I\\)','The following corollaries constitute')
frattini='## 6. Frattini kernels and coordinate geometries\n\nIn this section the type set is finite, while the group may be infinite unless stated otherwise. The Frattini subgroup is the intersection of maximal subgroups, with an empty intersection understood as the whole group. The new normal-subgroup ladder and exact coset transport connect the common relative-generation formula to the 2005 geometry results.\n\n'
frattini+=e1+'### 6.1. Containment and exact kernel transport\n\n'+e23
frattini+='### 6.2. Relative generators and the corrected infinite scope\n\n'+e4
frattini+='### 6.3. Coordinates from the shared parabolic-generation formula\n\n'+e5
frattini+='### 6.4. Every residue supplies a Frattini test\n\n'+residual
frattini=frattini.replace('Theorem E5 (the coordinate specialization of (R))','Theorem E5 (the coordinate specialization of (4.4))')
frattini=frattini.replace('Apply the existing formula (R).','Apply Theorem R(b), equation (4.4).').replace('and (R) becomes (5.1).','and (4.4) becomes (5.1).')
# All old extension equation numbers become unique chapter-six numbers.
for a,b in [('2.1','6.1'),('3.1','6.2'),('3.2','6.3'),('3.3','6.4'),('5.1','6.5'),('5.2','6.6'),('6.1','6.7')]:
 # Protect simultaneous renumbering with tokens, including \tag.
 frattini=frattini.replace('('+a+')','(@'+a+'@)').replace('\\tag{'+a+'}','\\tag{@'+a+'@}')
for a,b in [('2.1','6.1'),('3.1','6.2'),('3.2','6.3'),('3.3','6.4'),('5.1','6.5'),('5.2','6.6'),('6.1','6.7')]:
 frattini=frattini.replace('(@'+a+'@)','('+b+')').replace('\\tag{@'+a+'@}','\\tag{'+b+'}')

ab=between(old,'## 6. The twelve source-result corollaries','## 7. Coverage, dependencies')
ab=replace_once(ab,'## 6. The twelve source-result corollaries','## 7. Explicit source-result corollaries')
ab=replace_once(ab,'The labels below make the replacement contract explicit. Each statement uses the definitions and hypotheses above, and each proof uses the common results already established.',
 'The labels below make the three-paper replacement contract explicit. A1–A4 recover the four 1998 theorem clauses, B1–B8 the eight numbered 2002 results in the declared scope, and C1–C11 the stated 2005 consequences, with its false unrestricted infinite converse labeled as corrected. Each proof uses only common results proved above and the explicit retained background.')
cs=between(ext,'**C1 —','## 7. Complete numbered inventory')
cs=re.sub(r'\*\*C(\d+) —',r'**Corollary C\1 —',cs)
cs=cs.replace('This is (6.1),','This is (6.7),').replace('This is (3.3), E3 and E2.','This is (6.4), E3 and E2.')
# Strengthen the adapter label, not the proved scope.
cs=cs.replace('N008 Theorem 2.1, finite scope.','N008 Theorem 2.1, finite specialization and corrected infinite converse.')

scope=r'''## 8. Main-result contract and measurement boundary

The intake is exactly [BC98] (N001), [CC02] (N003, its twelve-page author version), and [ACK05] (N008, its nine-page journal PDF). The mathematical replacement contract is:

| Source | Declared main-result and subsidiary coverage | Qualifications |
|---|---|---|
| N001 | All four parts of Theorem 1, Corollaries A1–A4. The necessary residue structure is included in F/I/D. | Finite inductively minimal pairs of every rank at least one; B97 classification and uniqueness retained. |
| N003 | Theorems 1.1, 2.1, 3.1 and 3.2; Corollaries 2.2–2.4 and 3.3; the strong-independence consequence attached to Theorem 3.1. | General bounds taken for finite groups; symmetric-group classifications keep \(n\geq7\). Both W1 and the stronger CFSG-dependent W2 remain imported. |
| N008 | Theorem 2.1 in finite scope with a corrected infinite extension; Theorem 3.1 in full finite-rank geometric scope, including infinite groups; Proposition 3.2, Corollary 3.3, Theorem 3.4; Proposition 3.5 and Lemma 3.6; the finite-p-group Proposition 3.7 and Theorem 3.8; the §4.2 residue test and §4.3 action-kernel conclusion. | Its unrestricted infinite Theorem 2.1 converse is false, as the explicit Prüfer-product example shows. Theorem 3.8 is read in the finite-p-group context fixed by its section. Gaschütz's quoted Theorem 4.1 and Archer's quoted earlier primitive-group reduction remain source imports. |

N008's abstract-level quotient correspondence is realized as a bijection of indexed subgroup families for a fixed quotient map, with exact incidence isomorphisms. An equality of automorphism-orbit counts is not inferred. Lemma E0 ensures that the infinite geometric results do not acquire an unstated flag-transitivity or residual-connectedness hypothesis. Theorem R's parabolic induction is used once for both the N003 rank theory and the N008 coordinate classification.

The full source/dependency ledger binds every declared source formulation, location, common theorem, adapter, background input and status. Every proof needed for the declared conclusions appears in this manuscript. Source citations establish provenance or name expressly retained background; no project phase note is an external proof dependency. Forest intersections, laminar flag completion, the sign kernel, two-block overgroups, the module obstruction, extremal edge recognition, arbitrary-parabolic recovery, the Frattini ladder and coordinate classification all remain charged in the body. The little coordinate converse/count (6.6) is included as a common-theory consequence, not used to inflate source coverage.

Excluded material is identified rather than silently counted: N003's small-degree exceptional census, unnumbered general direct-product discussion and open questions; N008's historical SmallGroups counts, asymptotic suggestion, and referenced computational methods; source historical commentary and displayed illustrations. N001's auxiliary statements are not separately counted, although the structural content needed for its main theorem is proved. Other manuscripts, truncation classifications and full shadow intersection are outside this intake. The source-imported Gaschütz and Archer results are not purported new corollaries of the forest theory.

The assembled three-paper version requires its own independent integration and source-scope review even though its two constituent drafts have been internally reviewed. In particular the corrected main-result contract for N008 must be accepted before its full source length can enter a three-paper numerator. No manuscript ratio is assigned here. Earlier two-paper or matched-proof measurements are separate experiments and are not carried over. A later ratio must compare the three exact source bodies against this whole mathematical body, include all necessary appendices and dependency exposition, exclude references and acknowledgments consistently, and disclose the retained unexpanded background. Common mathematical rendering is needed before raw extraction-length differences can be treated as a robust compression factor.

'''
refs=old[old.index('## References and source versions'):]
refs=refs.replace('641–651','641–650')
refs+=r'''

[ACK05] C. Archer, P. Cara and J. Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries*, Beiträge zur Algebra und Geometrie **46**(1) (2005), 169–177. Target version: complete published nine-page PDF, identically retrieved from the [GWDG EMIS mirror](https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf) and the [Masaryk EMIS mirror](https://emis.muni.cz/journals/BAG/vol.46/no.1/b46h1car.pdf). The finite-p-group background is recalled on page 174; all target statements, scope corrections and the imported theorem inventory are version-bound in the companion contract.

[Gas53] W. Gaschütz, *Über die Φ-Untergruppe endlicher Gruppen*, Math. Z. **58** (1953), 160–170. Retained only in the structural form quoted as [ACK05] Theorem 4.1; the original proof was not independently acquired for this assembly.

[Arc04] C. Archer, *Direct sum decomposition of geometries based on maximal subgroups*, J. Geometry **79** (2004), 12–18. The primitive-group reduction quoted in [ACK05] §4.3 is retained as earlier work, not proved or used to establish the new Frattini/coordinate core.
'''
header=r'''# Forest cuts, relative generators and Frattini kernels

**Compress_A_v2 — integrated three-paper replacement manuscript, private review draft, 10 October 2026.**

## Abstract and scope

A tree determines symmetric groups on forest components and a laminar family of cuts. Unique paths give subgroup intersections, laminar atoms complete flags, and a sign kernel supplies the second extremal symmetric-group family. A shared relative-generation theorem then connects both maximum-rank geometry and finite-p-group coordinate geometry. We combine these mechanisms with a normal-subgroup ladder and exact coset-kernel transport to derive the declared main results of Buekenhout–Cara (1998), Cameron–Cara (2002), and Archer–Cara–Krempa (2005) in one text. The 1997 foundational classification and both Whiston inputs, including their retained classification dependence, remain explicit. The Frattini branch requires only elementary subgroup/vector-space facts, the finite-p-group Frattini quotient fact, and Zorn's lemma for its infinite-group statements. The source's false unrestricted infinite converse for relative generation is visibly corrected. No manuscript-length ratio or priority claim is made for this version.

'''
result=header+core+'\n'+frattini+'\n'+ab+'\n'+cs+'\n'+scope+refs
# Sanity checks for one shared R, all target labels, unique display tags, no external proof notes.
labels=re.findall(r'\*\*Corollary ([ABC]\d+) —',result)
expected=[f'A{i}' for i in range(1,5)]+[f'B{i}' for i in range(1,9)]+[f'C{i}' for i in range(1,12)]
assert labels==expected,labels
assert result.count('**Theorem R ')==1
assert result.count('**Lemma E0 ')==1
assert result.count('**Theorem E5 ')==1
assert '(R)' not in result
assert '@' not in result
assert result.count('\\[')==result.count('\\]') and result.count('\\(')==result.count('\\)')
tags=re.findall(r'\\tag\{([^}]+)\}',result)
assert len(tags)==len(set(tags)),tags
assert not re.search(r'\]\(phase\d',result)
output=ROOT/'phase37_compress_forest_manuscript.md'
output.write_text(result)
report={'date':'2026-10-10','status':'new_integrated_v2_pending_its_own_review','assembly_inputs':INPUTS,'output':{'path':output.name,'bytes':len(output.read_bytes()),'sha256':sha(output.read_bytes())},'substantive_changes':['Shared definitions and one R proof for all three papers','E0 moved to common geometry foundation','R(b) expressly states the already-proved arbitrary-group finite-rank firm-RWPRI form','All Frattini E1-E5 proofs integrated and equation numbers normalized','All23 source adapters in one corollary collection','Corrected infinite converse remains explicit','N003 journal pagination typo corrected641-651 to641-650, excluding any theorem-source change'],'checks':{'all23corollaries_present':True,'one_R_proof':True,'one_E0_proof':True,'all_display_tags_unique':True,'math_delimiters_balanced':True,'no_external_phase_proof_dependencies':True,'frozen_inputs_hash_verified':True},'measurement':{'three_paper_numerator_admitted':False,'ratio':None},'prior_files_modified':False}
(ROOT/'phase37_compress_forest_assembly.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['output'],indent=2))
