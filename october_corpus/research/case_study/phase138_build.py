#!/usr/bin/env python3
"""Integrate the reviewed six-source mathematics without mutating its predecessors."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parent

def read(name,digest):
 b=(ROOT/name).read_bytes()
 if hashlib.sha256(b).hexdigest()!=digest:raise RuntimeError('changed predecessor '+name)
 return b.decode()
def main():
 parser=argparse.ArgumentParser();parser.add_argument("--output-dir",type=Path,required=True);args=parser.parse_args()
 if args.output_dir.exists() or args.output_dir.is_symlink():raise RuntimeError('Refusing existing output directory')
 u=read('phase123_umbrella_manuscript_v2.md','d6c5d4b087c4bb4cab29f4729314dfc1dbaa640410d1d0ca9a73f33651058e2c')
 a=read('phase117_two_group_application.md','d8b037be2e356416056eb3772be5e020ee7e598cd621ad6e79f0dab79a84c56f')
 h=read('phase130_typed_helly_L034.md','b52accdbd852b2383f3f5aa5a138e05190495ada91358cca633a71684e861b03')
 read('phase130_geometry_erratum.md','79b17120464c7890f7feab95f5884f0f64e50432a9be3d8d8bac18eec6cb8d68')
 read('phase138_N009_decomposition_erratum.md','3805d1f8b4c89fee526f996b340eef61a80574d4938a49d68b7b3ce142ee0a94')
 helly=h[h.index('Write right cosets'):h.index('## 2. The square quotient')]
 helly=helly.replace('A family of subgroups has **typed coset Helly** if every finite pairwise intersecting family of their right cosets, at most one of each type, has a common element. ','')
 helly=helly.replace('assume the base marking gives a regular hypertope.','assume the base marking gives a regular hypertope and every marked generator in every attached group is an involution.')
 helly=helly.replace('The generators remain nonidentity involutions because their base images are such.','Each constructed generator is a tuple whose base coordinate and every nontrivial attached coordinate are involutions; hence its square is the identity. Its base image is nonidentity, so its order is exactly two.')
 helly=helly.replace('\\tag{H1}','\\tag{4.6}').replace('\\tag{H2}','\\tag{4.7}').replace('(H1)','(4.6)').replace('(H2)','(4.7)')
 helly+=r'''A sufficient alternative to local involutivity is that every support has size at least two: each singleton local parabolic is then proper, and injectivity into its nonidentity involutory base image forces the local marker to have order two. This is a sufficient condition, not an equivalent reformulation. Without either condition the geometric corollary fails. With a singleton type set and support, the quotient \(C_4\to C_2\) is injective on its only proper parabolic, the trivial subgroup. U.SK then constructs \(C_4\), whose distinguished generator has order four. In rank three, adjoining two independent \(C_2\) markers gives \(C_4\times C_2^2\) with the same defective singleton attachment and a four-element panel.

'''
 u=u.replace('## 4. Comparison through one exceptional parabolic','## 4. Coset comparison and coordinate-kernel geometry')
 u=u.replace('## 5. Retained objects and orbit multiplicities','### 4.1. Helly transfer through coordinate kernels\n\n'+helly+'## 5. Retained objects and orbit multiplicities')
 u=u.replace('We derive local recognition, deletion maps, lower-central identities and separator factorizations from the same proof.','We derive local recognition, deletion maps, lower-central identities and separator factorizations from the same proof. Exact coordinate profiles also transfer typed coset Helly; with the necessary involutory local markings this gives regular geometries.')
 u=u.replace('This is a private working manuscript, dated 10 October 2026. Its theorem identifiers are stable interfaces for the companion application manuscripts. The provenance and formal-coverage ledger is separate from the mathematical exposition. The manuscript does not claim a historical novelty assessment or a completed formalization.\n\n','')
 u=u.replace('together with the order-1024 study [GLP18].','together with the order-1024 study [GLP18] and the three-generator hypertope construction [HFLh].')
 u+='\n[HFLh] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-hypertopes with \\(2^n\\) chambers*, arXiv:1901.09034v1, 23 January 2019. The exact presentation and corrected structural displays are treated in Module A.\n'
 mark='The application interface is mathematical rather than merely notational.'
 u=u.replace(mark,'The coordinate-kernel theorem U.SK.Helly additionally requires exact kernel profiles and base IP to move pairwise intersections to a common fiber. Its geometric corollary requires actual involutory local markers, as well as a regular base geometry. These obligations are checked for the three dihedral pair attachments in Module A.\n\n'+mark)
 u=u.replace('The separate provenance ledger binds the exact predecessor proofs, the new interfaces and the limited existing Lean certificates.','The separate provenance ledger binds the exact predecessor proofs, the new interfaces and the limited existing Lean certificates. The coordinate-kernel Helly proof was developed as the common geometric step for the three-generator hypertope construction and is integrated here with its necessary local-involutivity hypothesis. The affine and source-presentation arguments remain in Module A. These additions make no historical novelty or open-conjecture claim.')
 intro=r'''# Module A: Construction and classification of two-group polytopes and hypertopes

## Abstract

We develop construction and classification methods for regular polytopes and hypertopes whose automorphism groups have two-power order. A forest of noncommuting generators determines a canonical class-two quotient. Its square-lattice sections provide local kernels that can be attached independently by the supported-kernel theorem of *Marked groups, kernels and intersections*. This yields prescribed edge orders, square sections and three-generator hypertope types, with exact orders and complete presentations. Conversely, a fixed class-two quotient reduces bounded-order classification to an exhaustive invariant-kernel problem. We combine this reduction with cyclic-core and central-descent arguments to recover the high-type rank-three families and the full order-1024 classification, including named facets and corrected presentations. The same local models also support regular, chiral and alternating extensions. Source conclusions, retained geometric inputs and corrections are stated explicitly.

## Introduction

Local sections serve two complementary purposes in finite incidence geometry. One may prescribe them and construct a marked group realizing those prescriptions, or constrain their orders and classify every group that can occur. The same kernel coordinates can organize both tasks. In the construction direction, a local quotient is attached to a subset of the marker labels. In the classification direction, a canonical nilpotent quotient confines the search to normal subgroups of one finite group.

The starting point is a vertex-and-edge model for a forest diagram. The intersection property forces independent edge commutators in degree two, so every finite marked two-group with that diagram has the same class-two quotient (§2). The affine square group supplies exact local kernels and two useful quotient decompositions (§3). The supported-kernel theorem of the companion paper [U] then assembles prescribed edge orders and consecutive square sections. Its coordinate-kernel Helly theorem upgrades three dihedral attachments to an actual regular hypertope. A separate sharp order bound identifies the source's complete presentation (§4).

The reverse direction begins with a bounded cyclic core, reducing the high-type rank-three problem to eight explicit models (§5). Central descent and complete binary lifting link the bounded quotients (§6). One invariant-kernel census, followed by complete presentation and marked-isomorphism checks, yields the order-1024 classification (§7). Finally, free geometric extensions use the amalgam theorem of [U] and precisely stated earlier constructions (§8).

The six applications are the prescribed-order theorem of Hou, Feng and Leemans [HFLa], their high-type rank-three classification [HFLb], their three-generator hypertope construction [HFLh], the common-quotient theorem of Hou and Schulte [HS26], the square-section and extension theorems of Cunningham, Feng, Hou and Schulte [CFHS25], and the order-1024 classification of Gomi, Loyola and De Las Peñas [GLP18]. Their original results retain that attribution. The general algebraic proofs occur once in [U]; this paper supplies the actual marked maps, local injectivity, geometric hypotheses and source-presentation identifications needed to use them. Earlier cyclic-core, geometric-assembly and infinite-decomposition theorems remain explicit retained inputs. All finite classification data and the complete certificate interface are specified in Appendix C.

'''
 a=intro+a[a.index('## 1. Markings'):]
 a=a.replace('The general facts used from U are listed with provisional exact signatures.','The general facts used from U are listed with their exact interfaces.')
 a=a.replace('Their complete proofs occur once in U, not in the application proof cost again.','Their complete proofs occur once in U; each application below verifies the stated hypotheses.')
 anchor='* **U.Nilpotent/U.Ladder**:'
 a=a.replace(anchor,r'''* **U.SK.Helly/U.SK.Geometry**: a marked quotient with base IP and an exact direct-product coordinate profile transfers typed coset Helly from the base. If the base is a regular hypertope and every local marker is an involution, U.SK therefore gives a regular hypertope with the constructed full type-preserving group. In the pair-support case local involutivity also follows from proper-singleton injectivity.
'''+'\n'+anchor)
 a=a.replace('The type is their consecutive\nproduct orders.','The type is their consecutive\nproduct orders. A regular hypertope is a thin, residually connected incidence geometry with a chamber-transitive type-preserving automorphism group. It need not have a string diagram; its rank-three type here records all three pair-product orders.')
 affine=h[h.index('For \\(\\delta\\ge0\\)'):h.index('## 3. The complete three-generator')]
 affine=affine.replace('Thus \\(Q_\\delta=H_{\\delta+5}\\) in A,','Thus \\(Q_\\delta=H_{\\delta+5}\\),')
 affine='### 3.1. Complete square quotients and their decompositions\n\n'+affine
 affine=affine.replace('For completeness the two square decompositions used by the source can be proved','**Proposition A3.2 (the two square decompositions).** The source presentations \\(M_2\\) and \\(M_1\\) have the decompositions displayed below. They hold')
 affine=affine.replace('in the same affine model for every integer','in the same affine model for every integer')
 # Explicit proof marker before the already complete affine argument.
 affine=affine.replace('Here bcba is translation','\n\n*Proof.* Here bcba is translation',1)
 affine=affine.replace('These arguments specify the actions by the original affine generators. They prove the needed decompositions rather than identifying groups from equal orders alone.','These arguments specify the actions by the original affine generators and prove the decompositions, rather than only equality of orders. \\(\\square\\)')
 affine=affine.replace('q\\ge2','q\\ge1').replace('including \\(D_4=C_2^2\\).','including \\(D_2=C_2\\) and \\(D_4=C_2^2\\).').replace('each is \\(D_{2q}\\).','each is \\(D_{2q}\\), since its reflection has nonidentity linear part, also when q=1.').replace('of order q in each case.','of order q in each case. Each reflection retains its nonidentity linear part, so the two factors have order 2q also at q=1.')
 a=a.replace('## 4. Prescribed local sections from supported kernels',affine+'## 4. Prescribed local sections from supported kernels')
 a=a.replace('Every selected pair has product order \\(m_S\\) and every unselected pair retains\nits old order.','Every selected pair has product order \\(m_S\\) and every unselected pair retains\nits old order. If the base marking gives a regular hypertope, so does the constructed marking, with full type-preserving group H.')
 a=a.replace('base product order. ∎','base product order. For the geometric assertion the local dihedral markers are involutions, and the supports are pairs. Thus the corrected U.SK.Geometry applies to the regular base and proves the required flag property as well as IP. ∎',1)
 construction=h[h.index('Fix integers \\(n\\ge10'):h.index('## 4. Source contract')]
 construction=construction.replace('[HFL19, Theorem 3.2]','[HFLh, Theorem 3.2]').replace('**Theorem A.H (the source construction as an attachment).**','**Theorem A.H (three-generator hypertope presentation).**')
 pstart=construction.index('*Proof.* Start with');pend=construction.index('The marked tuple in H satisfies')
 construction=construction[:pstart]+r'''*Proof.* Apply A4.1 to \(Q_\delta=H_{\delta+5}\), with all three pair supports and target orders \(2^s,2^t,2^\ell\). The base pair orders are \(4,4,2\); the attached maps are therefore \(D_{2^{s+1}}\to D_8\), \(D_{2^{t+1}}\to D_8\) and \(D_{2^{\ell+1}}\to D_4\). Section 3 supplies the base deletions and its regular string-polytope geometry. Each local marking consists of dihedral reflections, so A4.1's geometric clause applies. It constructs a regular hypertope with group H and the exact three pair orders, with
\[
 |H|=2^{\delta+5}\,2^{s-2}\,2^{t-2}\,2^{\ell-1}=2^n.
\]
The local orders and proper-parabolic injections used here are precisely those checked in A4.1; no independent second assembly proof is needed.

'''+construction[pend:]
 construction=construction.replace('Section 2 identifies that quotient','Section 3 identifies that quotient')
 a=a.replace('**Theorem A4.2 (square kernels on a forest).**','### Three-generator hypertopes\n\n'+construction+'### Prescribed square sections\n\n**Theorem A4.2 (square kernels on a forest).**')
 mapping={'H3':'A-S1','H4':'A-S3','H5':'A-S4','H6':'A-S5','H7':'A-S6','H8':'A-S7','H9':'A-H1','H10':'A-H2','H11':'A-H3'}
 for x,y in mapping.items():a=a.replace('('+x+')','('+y+')').replace('\\tag{'+x+'}','\\tag{'+y+'}')
 # The new affine decomposition also repairs an inherited source pairing.
 old_start=a.index('The retained decompositions are')
 old_end=a.index('Only the finite scope is used;',old_start)
 a=a[:old_start]+r'''The square and diagonal decompositions are now supplied by A3.2, including s=1. In the marking used here they are
\[
 (\langle a,c^b\rangle\times\langle c,a^b\rangle)\rtimes\langle b\rangle,
 \qquad
 (\langle b,b^{ac}\rangle\times\langle b^a,b^c\rangle)\rtimes\langle a,c\rangle,
\]
respectively. Each factor has order 2s and the complements have orders two and four. To check the marking in the second expression, its two pairs of reflection axes are x−y=0,1 and x+y=1,0; their products translate by (−1,1) and (1,1). The perpendicular factors, independent translations and complement parity check are exactly those in A3.2. The source instead prints the pairs \(\langle b,b^a\rangle\), \(\langle b^c,b^{ac}\rangle\). That pairing is erroneous for general s: \(bb^a=(ba)^2\) has order two, so its first factor always has order four. The classification is retained; this structural correction and its proof are not assumed from it. '''+a[old_end:]
 # Source correction is paid in the application, rather than retaining an external erratum.
 corr=r'''The [HFLh] structural display reverses the square and diagonal parity cases on both pp. 7 and 8 of the retained author version. Its stated dihedral exponents are nonintegral in those respective parities. The affine quotient calculation in §3 gives the corrected assignments in (A-H3), agreeing with the source's preceding calculation. The second cyclic subgroup's displayed definition also repeats the first pair word; its correct generator is \((bc)^4\), as used in Theorem A.H. These literal erroneous displays are not asserted as true. Proposition A3.2 rederives both decompositions of [HFLh, Lemma 3.1], already attributed there to McMullen–Schulte, for every integer \(q\ge2\). Theorem A.H recovers its complete principal Theorem 3.2 with these stated corrections. It does not prove Conjecture 3.3 or infer nonexistence from the construction.

'''
 corr+='The diagonal factor pairing quoted in [GLP18, Lemma 5.1(ii)] is also corrected in §7.4. Its printed first factor has order four independently of the lattice parameter; A3.2 supplies the correct two factors and complement for every positive parameter. The affine center proofs and finite classification certificates do not use the erroneous pairing. The source’s two-family classification remains a separate retained input.\n\n'
 a=a.replace('The exact intake is the five specified editions',corr+'The exact intake is the six specified editions')
 row='| [HFLh], Theorem 3.2 and auxiliary Lemma 3.1 | Exact three-generator presentation, order, pair orders, regular geometry, cyclic kernel product and corrected quotient structure | §3 affine words/decompositions; A4.1 with U.SK.Geometry; A.H sharp presentation bound via U.Order |\n'
 a=a.replace('| [HS26], Theorems 1.1–1.2 |',row+'| [HS26], Theorems 1.1–1.2 |')
 a=a.replace('before independent review.','with their retained verified executions.',1)
 a=a.replace('python3 -B -O research/leemans/phase78_n009_integration_run.py','python3 -B -O research/case_study/phase78_n009_integration_run.py')
 a=a.replace('From the research directory\'s parent, run:','From the public repository root, run:')
 a=a.replace('plus the actual\nU dependency closure and all written hypotheses in A.', 'plus the complete\nshared U body and all written hypotheses in A.')
 a=a.replace('## References and source-version boundary','## References and source-version boundary\n\n[U] *Marked groups, kernels and intersections*, companion manuscript, version 3.\n\n[HFLh] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-hypertopes with \\(2^n\\) chambers*, arXiv:1901.09034v1, 23 January 2019. The retained author PDF has eleven pages, SHA-256 `9d15089679be3828ff9291b4926ef3e3bd1a602449c67ce76ea17c7d9d1a6bfd`. The structural parity and repeated-pair-word corrections are given in §9; no journal-version collation is inferred.\n')
 for name,s in [('phase138_umbrella_v3.md',u),('phase138_module_A_v2.md',a)]:
  out=args.output_dir/name
  if out.exists():raise RuntimeError('Refusing existing manuscript '+name)
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(s)
  print(name,len(s.encode()),hashlib.sha256(s.encode()).hexdigest())
if __name__=='__main__':main()
