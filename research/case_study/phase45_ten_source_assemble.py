#!/usr/bin/env python3
"""Assemble a NEW, explicitly unreviewed full proof manuscript; no frozen edits."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def read(name):
    return (ROOT / name).read_text()

def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

def parts(text):
    marks = list(re.finditer(r'^## (\d+)\. (.+)$', text, re.M))
    out = {}
    for i, m in enumerate(marks):
        end = marks[i+1].start() if i+1 < len(marks) else len(text)
        out[int(m[1])] = text[m.start():end]
    return out

U = read('phase39_compress_unified_manuscript.md')
O = read('phase40_compress_operations_manuscript.md')
V = read('phase41_chiral_cover_manuscript.md')
T = read('phase45_ten_source_toroid_bridge.md')
us = parts(U.split('## Appendix A.')[0])
os = parts(O.split('## References and retained inputs')[0])
vs = parts(V)

intro = r'''# Marked kernels, coordinates and geometric recognition

**Private continuous proof manuscript, 10 October 2026. New integration;
independent review pending.**

The question addressed here is whether the principal results of specified
research manuscripts can be recovered as short corollaries of a smaller
collection of proved ideas. The candidate intake is N001, N003, N008, L032,
L035, F013, F016, L088, N013 and N016. Their exact versions, corrected scopes
and retained inputs are part of the mathematical contract. An intake list is
not a count of approved replacements, and this draft has no compression factor.

The useful object is a group with a distinguished family of parabolic
subgroups. Its chambers form a torsor when the action is regular: selecting a
base chamber identifies them with the group, and changing the base chamber
changes that identification by translation. Faces are the orbits of specified
parabolics. A finite torsor is representable by permutation matrices, but the
matrices do not eliminate the crucial information: one must retain the
marking, the parabolic partitions and their common-point properties. Ordinary
linear algebra alone neither proves the intersection property nor guarantees
that the resulting incidence system is a geometry.

The first common theorem isolates an exact obstruction. If two marked
subgroups have the correct intersection after applying a homomorphism, their
intersection before applying it is correct precisely when the kernel contains
no additional intersection. This gives both independent cyclic edge extensions
and the chirality-group criterion for a smallest regular cover. The proof is
one elementary lift of an element with prescribed image. Exact coset transport
through a kernel in the chamber stabilizer is another, separately proved,
statement: it preserves the whole geometry. Relative generation and a Frattini
ladder then turn finite p-group geometries into coordinate geometries, and
primitive saturation supplies the same base for the graded two-group argument.

Two further kinds of information remain essential. Forest cuts give actual
intersection partitions and laminar flag completion for symmetric groups;
these markings generally have no Boolean deletion maps. Endpoint conjugation
instead gives a subgroup of index at most two. Its algebraic obstruction is
an overlap and an intersection-closed support family, while a graph double
cover proves the required geometric flag completion. This operation handles
both the odd-endpoint J1 constructions and generalized-cube halving. The
coordinate section identifies the latter's toroidal lattices by a Gray-code
isomorphism of face posets and an exact affine marking, including the square
map's change of lattice basis. It never infers a geometry from its order alone.

The full forest recognition, cyclic-core classification, model presentations,
FAP arguments, residue-extension census, local mirror identifications and
minimal-cover proof are printed below. Every required finite program is in an
appendix. Several substantial older inputs remain explicit, including B97,
Whiston's two separate inputs, Burnside, the cyclic core bound, the complete
order-256 and J1 subgroup catalogues, Danzer's general construction, the stated
Coxeter classifications, the geometric extension and oriented-polytope
interfaces, and the older five tight chiral families. None becomes free because
it appears in a shared notation.

The new integration preserves all source corrections: the unrestricted
infinite Frattini converse, F013's auxiliary kernel assertions, diagonal
translation counts, chiral facet embeddings, L088's exchanged figure labels,
N013's rank-three exception and N016's nonidentity-power wording. L108's
Petrial paper remains outside the intake because its set-valued operation can
lose faithfulness. No open conjecture, new priority claim, or Lean verification
of the complete geometry is asserted.

The intended reconstruction is explicit: take a source statement in the
contract map, use its displayed corollary and the complete internal lemmas
named there, then retain only the declared background. The appendix programs
are part of that proof. Component reviews do not replace independent review
of this newly integrated text.

'''

# One convention section, including all extra geometric interfaces.
conventions = us[1]
vinput = vs[1].split('We retain the following standard geometric correspondence', 1)[1]
vinput = 'We retain the following standard geometric correspondence' + vinput
vinput = vinput.replace('needed to remove the local polytopality assumptions in the main criterion',
                       'needed to remove the local polytopality assumptions in the cover criterion')
conventions += '\n### Oriented geometry and the additional retained inputs\n\n' + vinput
conventions += '''
For the operation branch we retain Danzer's regular lattice-polytope
construction and its full semidirect-product group in the exact form stated
in §20, the classical finite/affine/compact-hyperbolic Coxeter classifications,
and the standard convex-polytope orders used there. The particular toroidal
lattices are proved in §9. The J1 branch retains TomLib's complete forty-class
subgroup table and its ambient permutation model, together with exact GAP
group, coset and orbit algorithms; its original geometry census is not an
input. The chiral branch retains the older five classified tight families
and their embedded chirality property, stated exactly in §22.3. All these
are substantial charged inputs. In the general coset sections use left
cosets; the operation certificate uses right cosets. Inversion identifies
the conventions, and every common-point or subgroup assertion is invariant
under that conversion. The scripts use their own explicitly given convention.

'''

# Strengthen K once. Both the former marked proof and N016's copy are replaced.
core = us[2].replace('**Theorem K (two uses of an exact kernel).**',
                    '**Theorem K (intersection transport and exact coset transport).**')
kernel_general = r'''
**(0) Three-subgroup transport.** Let \(\pi:H\to Q\) be a homomorphism,
\(C\le A\cap B\le H\), and suppose
\(\pi(A)\cap\pi(B)=\pi(C)\). Then
\[
 A\cap B=C\quad\Longleftrightarrow\quad A\cap B\cap\ker\pi\le C.
 \tag{K0}
\]
*Proof of (0).* Only the reverse implication needs proof. Given
\(x\in A\cap B\), choose \(c\in C\) with \(\pi(c)=\pi(x)\).
Then \(xc^{-1}\in A\cap B\cap\ker\pi\le C\), so \(x\in C\).
No finiteness, centrality or global surjectivity is needed. This is the
generic algebraic statement formalized as
`LeemansLift.intersection_of_image_and_kernel`; the complete proof is here.

'''
core = core.replace('**(a) Marked intersections.**', kernel_general + '**(a) Marked intersections.**', 1)
start = core.index('*Proof of (a).*')
end = core.index('∎', start) + 1
core = core[:start] + r'''*Proof of (a).* Apply (0) with
\(A=H_I\), \(B=H_J\), \(C=H_{I\cap J}\).
The image hypothesis is the quotient's IP, and the kernel condition is
exactly \(K_I\cap K_J=K_{I\cap J}\), since the reverse inclusion always
holds. This proves both directions. ∎''' + core[end:]

def op_namespace(text):
    text = text.replace('This is N013 Theorem 3.1,', 'This is N013 SOURCE_THEOREM_3_1,')
    for label in ['1.1','1.2','2.1','2.2','2.3','3.1','4.1','5.1','5.2','5.3','6.1','6.2','6.3']:
        text = re.sub(r'((?:[Ll]emma|[Ll]emmas|[Tt]heorem|[Cc]orollary) )'+re.escape(label)+r'\b',
                      lambda m:m[1]+'O'+label, text)
    text = text.replace('SOURCE_THEOREM_3_1', 'Theorem 3.1')
    text = text.replace('O1.1–1.2','O1.1–O1.2')
    text = re.sub(r'\((\d{1,2})\)',r'(O\1)',text)
    text = re.sub(r'\\tag\{(\d{1,2})\}',lambda m:r'\tag{O'+m[1]+'}',text)
    text = text.replace('PSL₂(O11)', 'PSL₂(11)')
    text = text.replace('Appendices A and B', 'Appendices B and C')
    text = text.replace('Appendix A', 'APPENDIX_J1_CONSTRUCT').replace('Appendix B','Appendix C')
    text = text.replace('APPENDIX_J1_CONSTRUCT', 'Appendix B')
    return text

recognition = op_namespace(os[1].split('\n',1)[1])
recognition = recognition.replace('A marking of a group G is', 'For this recognition interface a marking of a group G is',1)
recognition = '\n### Marked torsors and geometric recognition\n\n' + recognition
core = core.replace('**Theorem R (relative-generation core).**', recognition+'**Theorem R (relative-generation core).**',1)

# The square coordinates serve both ordinary and oriented applications.
square = us[9]
square += r'''
### An oriented square model for the later cover criterion

**Lemma L1 (the square linear-part quotient).** In the square tessellation
with vertices \(\mathbb Z[i]\), the rotations
\(u:z\mapsto iz\), \(v:z\mapsto iz+1\) are rotations about a vertex and
an adjacent face centre. Their centre coordinates are \(0\) and
\((1+i)/2\), respectively, and \((uv)^2=1\). They generate the full
orientation-preserving grid group: their quotient supplies a unit
translation, and conjugation by the quarter-turn supplies the other unit
translation. For a nonzero ideal \(J=(b+ic)\), the marked quotient is
\((\mathbb Z[i]/J)\rtimes C_4\). It is the usual square-map model whenever
the source parameters specify such a map. The geometric interpretation is
the literal quotient of the tessellation, not an inference from its order.

The linear-part map \(\ell\) sends both marked generators to \(i\), and
is injective on each of their cyclic subgroups: both generators have fourth
power one and linear part of exact order four. If the universal mirror
sends \((u,v)\) to \((u^{-1},u^2v)\), then \(\ell\mu\) is inversion
composed with \(\ell\). Thus both the relation kernel and its mirror lie
in the universal kernel of \(\ell\); the chirality subgroup is contained
in the translation subgroup. In particular it meets \(\langle v\rangle\)
trivially. Here the chirality subgroup is the image of the product of the
relation kernel and its mirror, as defined precisely in §22.1. The argument
uses only the regular marked quotient \(C_4\), and does not claim that a
one-cell quotient is an abstract polytope. ∎

### Cubical and halved lattices in every dimension

'''
tproof = between(T, '## 1. Coordinate conventions and the actual face poset\n', '## 4. Source and proof accounting')
tproof = re.sub(r'^## [23]\. (.+)$',r'### \1',tproof,flags=re.M)
tproof = tproof.replace('Compress_C §§3–4','§§18–19').replace('Compress_C §3','§18')
tproof = tproof.replace('ledger N8','the N013 polygon contract').replace('ledger N12','the N013 cube-input contract')
square += tproof

# Preserve the endpoint proof; rename only its internal labels and equations.
ops = []
for i,new in [(2,17),(3,18),(4,19),(5,20),(6,21)]:
    s=op_namespace(os[i])
    s=re.sub(r'^## '+str(i)+r'\.', '## '+str(new)+'.',s,count=1)
    if i==6:s=s.replace('### 6.2.', '### 21.1.')
    ops.append(s)
old='For p=4 it is the square toroid conventionally denoted {4,4}_(2,2). Identifying that particular translation lattice, and identifying the original dual generalized cube with {4,4}_(4,0), are retained conventional grid identifications, not deductions from equal orders.'
new='For p=4 it is the square toroid {4,4}_(2,2). The Gray-code face-poset proof, explicit cubical duality and lattice basis change in §9 prove this identification and identify the original dual generalized cube as {4,4}_(4,0).'
assert old in ops[3]
ops[3]=ops[3].replace(old,new)
old="The source's toroidal notation for cube input is {4,3^(n−4),3/3}_(4,0,…,0); both the original cubical toroid {4,3^(n−3),4}_(4,0,…,0) and the halved lattice label are retained standard affine-lattice identifications. They are separate from the exact group, order and residue proofs just given."
new="The source's toroidal notation for cube input is {4,3^(n−4),3/3}_(4,0,…,0). Section 9 identifies the original cubical toroid and its halving as actual marked face/chamber quotients by 4Z^(n−1), proving the lattice names in addition to the exact group, order and residue assertions above."
assert old in ops[3]
ops[3]=ops[3].replace(old,new)

# One cover branch; the duplicated K proof and square-model proof are removed.
cover='## 22. Mirror covers and their exact kernel obstruction\n\n'
for i in range(2,8):
    s=vs[i]
    s=re.sub(r'^## '+str(i)+r'\. (.+)$',r'### 22.'+str(i-1)+r'. \1',s,count=1,flags=re.M)
    s=s.replace('Lemma 3.1','Lemma V3.1').replace('Theorem 3.2','Theorem V3.2')
    s=s.replace('Section 2','§22.1').replace('Section 5','§22.4')
    s=re.sub(r'\((\d)\)',r'(V\1)',s)
    s=re.sub(r'\\tag\{(\d)\}',lambda m:r'\tag{V'+m[1]+'}',s)
    if i==4:
        start=s.index('**Square torus maps.**')
        end=s.index('**Five tight families.**')
        s=s[:start]+'''**Square torus maps.** For the chiral maps {4,4}_(b,c)
in the source's standard parameter convention, bc(b−c)≠0, Lemma L1 gives
X(K)∩⟨v⟩=1. Consequence 5 in §22.2 therefore proves source Example 3.8
for every such extension. No negative or noncanonical parameters are added
to the source contract; no degenerate one-cell map is needed.

'''+s[end:]
    if i==5:
        s=s.replace('The accompanying `phase41_chiral_cover_check.g`, replayed by `phase41_chiral_cover_check.py`,',
                    'The complete program in Appendix D')
    if i==7:
        s=s.split('The mathematical reduction is genuine:')[0]
    cover+=s+'\n'

corollaries=us[17].replace('## 17.', '## 23.',1)
corollaries=corollaries.replace('The labels below make the three-paper replacement contract explicit.',
'''The labels below preserve the complete Unified source contracts. The operation
contracts are already explicit in Corollaries O4.1, O5.1–O5.3, O6.1 and O6.3;
the mirror-cover contract is Theorem V3.2 with its five consequences, classified
applications and the complete finite minimality proof in §22.''')
corollaries+='''
**Corollary Z1 — N013's toroidal labels.** For the r-cube input, r≥3, the
dual generalized cube is {4,3^(r−2),4}_(4,0,…,0), and its halving is the
affine fork toroidal hypertope {4,3^(r−3),3/3}_(4,0,…,0). For r=2 the
two maps are {4,4}_(4,0) and {4,4}_(2,2). The complete face-poset,
marking and lattice proofs are Lemmas T1–T2 and the rank-three basis change
in §9, with regularity supplied by Corollary O4.1. ∎

**Corollary Z2 — N016's proved conclusions.** With the exact author-version
scope and retained inputs stated in §1 and §22, source Propositions
2.2–2.4, Theorem 3.1, Corollaries 3.3–3.4 and 3.7, Proposition 3.6,
Examples 3.5 and 3.8, the uniqueness implication and the finite pair of
minimal regular covers all follow from Theorem K(0), the local mirror
identities, the proved regular-end induction, Lemma L1, the retained
five-family input, and the exact Appendix D calculation. Each implication
and the prime-degree minimality argument is written in §22; the two
source multiplicity conjectures remain unproved. ∎

'''

accounting='''## 24. Shared proof, retained costs and source boundaries

Theorem K(0) replaces the two copies of the same image-lifting proof;
K(a) is its marked corollary. K(b) retains its distinct exact-coset proof.
Lemma L1 presents the square affine model and its linear-part obstruction
once, beside the full square-seed normal-form proof. The Gray-code bridge
adds a necessary proof previously retained as a lattice identification.
The relative-generation and primitive-coordinate core remains shared by
the finite-p and two-group branches. Endpoint conjugation shares geometric
recognition with the J1 census and generalized-cube applications, but is
not assumed to be a homomorphic image of the old marking.

The laminar forest proof cannot be deleted: adjacent tree transpositions
satisfy an odd braid relation that Boolean deletion would destroy. The
cyclic-model proof, its catalogue-relative order-256 census, all FAP cuts,
the complete J1 residue census and all mirror/local-polytopality arguments
also remain. No theorem of this manuscript claims to replace their
distinct hypotheses by a generic matrix computation. The newer marked
parabolic comparison theorem is not used: no application-specific product
injectivity has been established that would shorten the endpoint proof.

The necessary finite programs are printed in full in Appendices A–D.
Appendix A uses the complete SmallGroups order-256 catalogue; Appendices
B–C use the complete TomLib J1 subgroup table and exact algorithms;
Appendix D starts from bare finite presentations and uses exact GAP
algorithms without a finite-group catalogue. Existing exact-hash component
replays certify those unchanged programs; extraction and any new runner
are checked separately. Runtime versions, data hashes, logs and output
certificates remain charged audit artifacts. No new Lean formalization of
the complete arguments is claimed. A future common measurement must count
all proof prose and code, charge wrappers/outputs consistently and declare
the retained background. There is no numerical ratio in this draft.

L108 remains excluded: its Petrial objects are unlabelled traced sets and
can acquire an action kernel. For the complete tripartite geometry with
two objects of each type, its original C2³ action becomes C2² on the
Petrial with one face, refuting an unconditional embedding claim. That
operation is not a consequence of the endpoint theorem here. Ens's full
toroidal classification, the older tight-family classification, N009's
order-1024 census, and the phase46 minimal-cover exploration are not new
intake entries. N013's comparison with every example in its reference [9]
and its unused alternating-semiregular identification remain unproved
auxiliary assertions. Its Remark 4.1 is retained only with the rank
qualification proved in §20. The component ledgers retain every other
literal-versus-corrected boundary.

Exact source versions are the complete rendered N001 authored text,
twelve-page N003 author manuscript, nine-page N008 journal PDF, revised
L032 author PDF dated 8 November 2019, L035 arXiv:1802.08947v2,
F013 arXiv:2605.20691v1, F016 arXiv:2512.15511v1, L088's ten-page
journal PDF and N013 arXiv:2001.11082v1. N016 is the eight-page author
manuscript headed 25 July 2023; its 2024 journal publication is confirmed,
but the publisher full text was not acquired. The new integration reading
log distinguishes complete component proofs from inherited primary
readings. Component approval does not approve this altered assembly.

'''

appendix_a=between(U,'## Appendix A.','## References and exact source versions')
appendix_a='## Appendix A.'+appendix_a
# Use the full executable, including identifiers and output, instead of a second duplicate.
code_a=read('phase37_compress_twogroups_census.g')
appendix_a=re.sub(r'```gap\n.*?\n```',lambda m:'```gap\n'+code_a.rstrip()+'\n```',appendix_a,count=1,flags=re.S)
appendix_a=appendix_a.replace("Each row's\nidentifiers in §13 are recorded by the executable version accompanying\nthe ledger; only the exhaustive relation implications, not those\nidentifiers or anchored multiplicities, enter the infinite-parameter\nproof.","The program records the row identifiers in §13; only the exhaustive relation implications, not those identifiers or anchored multiplicities, enter the infinite-parameter proof.")
appendix_b=between(O,'## Appendix A.','## Appendix B.')
appendix_b='## Appendix B.'+appendix_b
appendix_c='## Appendix C.'+O.split('## Appendix B.',1)[1]
appendix_d='''## Appendix D. Complete chiral-cover finite certificate

This complete program begins with the literal source presentations,
constructs their mirror mixes, checks every relevant C+ intersection and
marked cover, verifies local chirality, and supplies the distinguishing
word. The abstract universal-property and minimality proofs are in §22.
Its bytes are identical to the frozen phase41 program.

```gap
'''+read('phase41_chiral_cover_check.g').rstrip()+'\n```\n\n'

refs='## References and exact source versions\n'+U.split('## References and exact source versions',1)[1]
oref=between(O,'## References and retained inputs','## Appendix A.')
oref=oref.replace('Corollary 6.3','Corollary O6.3').replace('in (9)','in (O9)')
oref=oref.replace('The construction theorem in (O9), conventional toroidal lattice identifications and standard convex-polytope orders remain retained',
                  'The construction theorem in (O9) and standard convex-polytope orders remain retained; the particular toroidal lattice identifications are proved in §9')
refs+='\n### Operations and covers\n'+oref
refs+='''
[Cun24] G. Cunningham, *Chiral polytopes whose smallest regular cover is a
polytope*, Journal of Combinatorial Theory, Series A 204 (2024), 105839,
DOI [10.1016/j.jcta.2023.105839](https://doi.org/10.1016/j.jcta.2023.105839).
Target: [author manuscript headed 25 July 2023](https://gabrielcunningham.com/WhichChiralPolytopes.pdf),
eight pages; publisher full text unacquired.

[CP21] G. Cunningham and D. Pellicer, *Tight chiral polytopes*, Journal of
Algebraic Combinatorics 54 (2021), 837–878. The five rows and embedded
chirality input retained in §22.3 were checked in arXiv:2009.04566,
Proposition 4.2 and Table 4; this older classification is not replaced.

[Ens18] E. Ens, *Rank 4 toroidal hypertopes*, Ars Mathematica Contemporanea
15 (2018), 67–79. The selected definitions, equations (3.1), (4.1) and
Theorem 4.3 were read to match the lattice convention in §9; the full
classification is neither assumed to prove that quotient nor counted.

'''

out=intro+conventions+core+''.join(us[i] for i in range(3,9))+square+''.join(us[i] for i in range(10,17))+''.join(ops)+cover+corollaries+accounting+appendix_a+appendix_b+appendix_c+appendix_d+refs
out=out.replace('This seven-source integration requires its own independent review; no seven-paper factor is assigned.',
                'This integration requires its own independent review; no factor is assigned.')
out=out.replace('Admission of all four manuscripts\nto any length numerator requires independent review of this assembled\ntext and the bound finite certificate, not merely historical reviews of\nseparate ingredients.',
                'The two-group source contracts require the full preceding text and bound finite certificate; their inherited review does not certify this changed assembly.')
out=out.replace('in source §22.4','in source Section 5')
target=ROOT/'phase45_ten_source_manuscript.md'
target.write_text(out)

code_blocks=re.findall(r'```gap\n(.*?)\n```',out,re.S)
expected=[code_a,read('phase40_compress_operations_check.g'),read('phase40_compress_operations_exhaustive.g'),read('phase41_chiral_cover_check.g')]
assert len(code_blocks)==4
assert all(x.rstrip()+'\n'==y.rstrip()+'\n' for x,y in zip(code_blocks,expected))
report={'status':'complete_body_assembled_author_crossreference_review_pending','manuscript_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'code_blocks':4,'all_code_blocks_match_frozen_programs':True,'claimed_ratio':None,'source_count_admitted':False,'unproved_conjectures_not_counted':True,'proof_removals':[{'old':'Unified K(a) lifting proof and N016 K lifting proof','new':'one general K(0), K(a) short specialization'},{'old':'separate N016 square affine/linear-part paragraph','new':'full Lemma L1 next to shared lattice seed; source corollary in §22.3'}],'new_required_proof':'full N013 Gray-code/affine toroidal bridge in §9','preserved':'all complete forest/cyclic/graded/geometry/census/mirror/local/minimality branches; all four executable programs','source_versions':'phase45_ten_source_adapter_map.json'}
(ROOT/'phase45_ten_source_assembly.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
