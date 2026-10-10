#!/usr/bin/env python3
"""Assemble a new integrated draft; never edit frozen component manuscripts."""
from pathlib import Path
import re,json,hashlib
P=Path(__file__).resolve().parent
A=(P/'phase37_compress_forest_manuscript.md').read_text();B=(P/'phase37_compress_twogroups_manuscript.md').read_text();bridge=(P/'phase38_primitive_saturation.md').read_text()
sha=lambda b:hashlib.sha256(b).hexdigest()
def section(t,n):
 m=re.search(r'^## '+str(n)+r'\. .*$',t,re.M);e=re.search(r'^## ',t[m.end():],re.M);return t[m.end():m.end()+e.start() if e else len(t)].strip()
def between(t,a,b):return t[t.index(a):t.index(b)]
def arefs(t):
 t=re.sub(r'\\tag\{([1-6]\.\d+)\}',r'\\tag{A\1}',t)
 t=re.sub(r'\(([1-6]\.\d+)\)',r'(A\1)',t)
 return t
bsect={2:8,3:9,4:10,5:11,6:12,7:13,8:14,9:15,10:16}
def brefs(t):
 t=re.sub(r'(?<=\\tag\{)([2-9]|10)\.([1-9])',r'Q\1.\2',t)
 t=re.sub(r'\(([2-9]|10)\.([1-9])\)',r'(Q\1.\2)',t)
 t=re.sub(r'\b(Lemma|Theorem|Corollary) ([2-9]|10)\.([1-9])',r'\1 Q\2.\3',t)
 t=t.replace('Lemma Q2.1','Theorem K(a)')
 t=re.sub(r'§§(\d+)[–—-](\d+)',lambda m:'§§'+str(bsect.get(int(m[1]),int(m[1])))+'–'+str(bsect.get(int(m[2]),int(m[2]))),t)
 t=re.sub(r'(?<!§)§(?!§)(\d+)',lambda m:'§'+str(bsect.get(int(m[1]),int(m[1]))),t)
 return t
asecs={i:section(A,i) for i in range(1,9)};bsecs={i:section(B,i) for i in range(1,11)}
# Proof R is moved ahead of both applications, with its complete proof retained.
r=asecs[4][:asecs[4].index('**Lemma M')].strip();ext=asecs[4][asecs[4].index('**Lemma M'):]
e3=between(asecs[6],'**Theorem E3','The quotient by')
kproof=e3[e3.index('*Proof.*'):].strip()
kstmt=e3[:e3.index('*Proof.*')].replace('**Theorem E3 (exact coset-kernel transport).**','**(b) Exact coset transport.**')
k='''**Theorem K (two uses of an exact kernel).**

**(a) Marked intersections.** Let \\(\\pi:H\\twoheadrightarrow Q\\) preserve a marking, and suppose the image marking has IP. Put \\(K=\\ker\\pi\\), \\(H_I=\\langle r_i:i\\in I\\rangle\\), and \\(K_I=K\\cap H_I\\). Then the marking in \\(H\\) has IP if and only if \\(K_I\\cap K_J=K_{I\\cap J}\\) for all subsets.

*Proof of (a).* Necessity follows by intersection with \\(K\\). For \\(x\\in H_I\\cap H_J\\), its image lies in \\(Q_{I\\cap J}\\). Choose \\(y\\in H_{I\\cap J}\\) with \\(\\pi y=\\pi x\\). Then \\(xy^{-1}\\in K_I\\cap K_J=K_{I\\cap J}\\), so \\(x\\in H_{I\\cap J}\\). ∎

'''+kstmt+'\n'+kproof.replace('*Proof.*','*Proof of (b).*')
fr=asecs[6]
fr=fr[fr.index('**Lemma E1'):fr.index('### 6.3.')]
fr=fr.replace('### 6.1. Containment and exact kernel transport','### Containment and quotient actions').replace('### 6.2. Relative generators and the corrected infinite scope','### Relative generators and the corrected infinite scope')
fr=fr.replace(e3,'**Corollary E3 (exact coset-kernel transport).** All assertions of Theorem K(b) apply whenever the normal subgroup lies in the Borel. This is the coset-geometry specialization of the common kernel theorem, including pregeometries and infinite groups.\n\n')
# The primitive bridge is used only for the shared Frattini/basis arguments;
# independent new face-index and gamma3-fiber results are not appended.
saturation=r'''**Theorem S (primitive saturation and relative coordinates).** Let a finite p-group \(P\) have an irredundant generating marking \((r_i:i\in V)\), with \(|V|=d\), and put \(F=\Phi(P)\). For \(P_U=\langle r_i:i\in U\rangle\),
\[
 \Phi(P_U)=P_U\cap F,\qquad
 P_UF=\pi^{-1}\operatorname{span}(\bar r_i:i\in U),
 \quad [P:P_UF]=p^{d-|U|}.                           \tag{S.1}
\]
These saturated parabolics intersect according to intersection of label sets. Each omission subgroup has the unique maximal overgroup \(M_i=P_{V\setminus\{i\}}F\). Its coset action is the unique primitive coarsening of that omission action; all such actions together give the complete d-partite geometry with p elements of each type and faithful chamber-regular group \(P/F\).

More generally, if \(B\lhd P\), \(F\le B\), and \((s_i:i\in I)\) generates \(P\) irredundantly relative to \(B\), then \(P/B\) has basis \((s_iB)\) and
\[
 \langle B,s_i:i\in U\rangle/B
      =\operatorname{span}(s_iB:i\in U).                \tag{S.2}
\]
Its omission geometry is the complete \(|I|\)-partite p-point geometry. Finally, if the original marking consists of involutions and \(p=2\), then \(F=P'\), and \(\Phi(P_U)=P_U'\) for every parabolic.

*Proof.* Burnside's basis theorem makes \((\bar r_i)\) a basis of \(P/F\). The image of \(P_U\) has dimension \(|U|\), so its elementary abelian quotient has kernel \(P_U\cap F\) and order \(p^{|U|}\). It follows that \(\Phi(P_U)\le P_U\cap F\). Since \(P_U\) has \(|U|\) generators, Burnside gives \([P_U:\Phi(P_U)]\le p^{|U|}\); equality of the two bounds proves the kernel identity. The inverse-image, intersection and index assertions follow from coordinate subspaces. Every maximal subgroup contains \(F\) and has index p; containing an omission subgroup therefore forces equality with the preimage of its coordinate hyperplane. This proves uniqueness and primitivity. Cosets prescribe independent coordinate values; every assignment extends to a vector. Their intersection kernel is \(F\), and the quotient translations act regularly on chambers.

For the relative assertion, \(P/B\) is elementary abelian because \(B\ge F\). The images span, and a nontrivial linear relation would express one \(s_i\) modulo \(B\) in terms of the others, contrary to irredundancy. They therefore form a basis, proving (S.2) and the same coordinate-geometry statements. For involution generators, the abelianization is elementary abelian of exponent two. Thus \(P'\le\Phi(P)\), while the elementary abelian quotient by \(P'\) gives \(\Phi(P)\le P'\). The same argument applies to each parabolic. ∎
'''
coord=asecs[6][asecs[6].index('**Theorem E5'):]
oldproof=between(coord,'*Proof.*','Conversely, writing')
newproof=r'''*Proof.* The normal-subgroup ladder E2 gives \(\Phi(P)\le B\). Since \(P/\Phi(P)\) is abelian, \(B\) is normal. Theorem R(b) supplies the irredundant relative marking and every parabolic formula. Apply the relative clause (S.2) of Theorem S: it gives the stated basis and all coordinate cosets. Every assignment is a chamber; fixing a further coordinate has index p, hence is maximal. Therefore the geometry is RPRI and a direct sum of primitive p-point geometries. Its action kernel is \(B\) by normality and Theorem K(b), and the quotient translations act regularly on chambers. ∎

'''
coord=coord.replace(oldproof,newproof).replace('### 6.4. Every residue supplies a Frattini test','### Every residue supplies a Frattini test')
# Merge definitions; targeted statements are made explicit again in final adapters.
defs=bsecs[1][:bsecs[1].index('The precise numbered targets are:')]
binputs=bsecs[1][bsecs[1].index('We retain the regular-polytope'):]
# Merge imported background instead of retaining two Burnside/Frattini proofs.
conv=asecs[1]+'\n\n'+brefs(defs)+'\n\n'+brefs(binputs)+r'''

For finite p-groups, the PΦ input is used together with Burnside's basis theorem: irredundant generating markings map to bases of the Frattini quotient. Theorem S proves the required compatibility with every marked subgroup; that compatibility is not an imported classification. Equation labels beginning A or Q and theorem labels beginning Q are unique internal labels in this manuscript. They are not references to another manuscript. All necessary proofs are printed below.
'''
# Remove B's copied kernel proof: theorem K already establishes it.
delete=bsecs[2][bsecs[2].index('**Lemma 2.2'):]
# Replace repeated elementary Frattini justifications by the one common theorem.
q5=brefs(bsecs[5]).replace('IP gives irredundancy, so Burnside gives\n\\(G/G\'=C_2^d\\) and \\(G\'\\cap\\langle r_i\\rangle=1\\).', 'IP gives irredundancy. Theorem S gives \\(G/G\'=C_2^d\\) and \\(G\'\\cap\\langle r_i\\rangle=1\\).')
parts=[('# Common kernels, primitive coordinates and marked geometries',None)]
intro='''**Compress_Unified — private seven-source integrated review draft, 10 October 2026.**

A subgroup kernel can transport either marked intersections or a whole coset geometry. A relative-generation theorem identifies the parabolics of residually weakly primitive geometries; the Frattini ladder and a single primitive-saturation theorem then turn finite p-group geometries into coordinate geometries. This common core also controls the marked two-group constructions. The symmetric branch needs its own tree-component and laminar-flag arguments, while the two-group branch uses deletion maps, square lattices and graded support. The resulting source corollaries cover the declared main-result contracts of N001, N003, N008, L032, L035, F013 and F016.

This is a new integration requiring independent review. It retains B97, both Whiston inputs including CFSG-dependent W2, Burnside and the specified geometric and cyclic-core inputs. The full all-parameter cyclic classification and its finite census algorithm remain in the body. The false unrestricted infinite Frattini converse and the specified false F013 auxiliary assertions stay visibly corrected. Seven-paper numerator admission and a seven-paper compression factor are not claimed. The earlier four-paper factor is a different, frozen experiment.
'''
sections=[('Conventions and all retained inputs',arefs(conv)),('Exact kernels, relative generation and the Frattini ladder',arefs(k+'\n\n'+r+'\n\n'+fr)),('One primitive-coordinate theorem and its geometry specialization',arefs(saturation+'\n\n'+coord)),('Symmetric groups from forest cuts and laminar flags',arefs(asecs[2])),('Two-block overgroups and inductively minimal property tests',arefs(asecs[3])),('Extremal symmetric markings',arefs(ext)),('Recognition of all maximum-rank symmetric geometries',arefs(asecs[5])),('Deletion maps, compatible products and cyclic edge kernels',brefs(delete)),('The common square-lattice seed',brefs(bsecs[3])),('Prescribed rank, order and type',brefs(bsecs[4])),('The canonical class-two quotient from graded support',q5),('Bounded cyclic cores and all binary extension models',brefs(bsecs[6])),('Completeness and exact presentation recognition',brefs(bsecs[7])),('Prescribed square sections and their universal presentation',brefs(bsecs[8])),('Alternating assembly and infinite extensions',brefs(bsecs[9])),('Corrections and exclusions in the two-group branch',brefs(bsecs[10])),('Every source result as an explicit corollary',arefs(asecs[7]))]
text=parts[0][0]+'\n\n'+intro+'\n\n'+'\n\n'.join('## '+str(i)+'. '+h+'\n\n'+s for i,(h,s) in enumerate(sections,1))
# Retain complete appendix, never only an external-code link.
appendix=brefs(B[B.index('## Appendix A.'):])
# Global cross-reference correction for A numerical source references only.
# The source names Theorem1.1 etc in adapter titles are intentionally unchanged.
text=text.replace('equation (A4.4)','equation (A4.4)')
text+='\n\n'+appendix+'\n\n## References and exact source versions\n\n'+A[A.index('## References and source versions')+len('## References and source versions'):].strip()+'\n\n'+'''[HFLa] D.-D. Hou, Y.-Q. Feng and D. Leemans, *On regular polytopes of 2-power order*, revised author PDF dated 8 November 2019, journal 2020, DOI 10.1007/s00454-019-00119-5. Exact retained primary file: `sources/catalogue_L032.pdf`.

[HFLb] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-polytopes of order 2^n*, arXiv:1802.08947v2, 22 January 2019; journal catalogue title *2-groups behaving as automorphism groups of regular 3-polytopes*. Exact retained primary file: `sources/catalogue_L035.pdf`.

[HS26] D.-D. Hou and E. Schulte, *String C-groups of 2-power order project onto a common string C-group*, arXiv:2605.20691v1, submitted 20 May 2026, PDF dated 21 May. Exact retained primary file: `sources/catalogue_F013.pdf`.

[CFHS25] G. Cunningham, Y.-Q. Feng, D.-D. Hou and E. Schulte, *Symmetric polytopes whose automorphism groups are 2-groups*, arXiv:2512.15511v1, submitted 17 December 2025, PDF dated 18 December. Exact retained primary file: `sources/symmetric_2groups2025.pdf`.
'''
# Assembly-created file is a draft, never an overwrite of a frozen original.
out=P/'phase39_compress_unified_manuscript.md'
with out.open('x') as f:f.write(text)
account={'status':'initial_integrated_draft_pending_adapter_completion_and_review','component_bindings':{n:sha((P/n).read_bytes()) for n in ['phase37_compress_forest_manuscript.md','phase37_compress_twogroups_manuscript.md','phase38_primitive_saturation.md']},'operations':[{'proof':'B kernel IP lift','before_copies':1,'after_copies':1,'change':'Moved into common Theorem K(a); old B occurrence removed, uses redirected.'},{'proof':'A exact coset transport','before_copies':1,'after_copies':1,'change':'Moved into common Theorem K(b); E3 is an internal adapter.'},{'proof':'A relative-generation R','before_copies':1,'after_copies':1,'change':'Moved before both applications, full infinite scope retained.'},{'proof':'finite-p coordinate basis and quotient geometry','before':'A E5 repeats spanning, independence, coordinate assignments; bridge repeats the same relative argument','after':'One Theorem S relative-coordinate proof; E5 invokes it, Frattini restriction serves two-group marking arguments','removed_old_E5_proof_codepoints':len(oldproof),'replacement_E5_adapter_codepoints':len(newproof)},{'proof':'full primitive bridge extra gamma3 and face-index results','change':'Not appended: they do not remove another necessary source-proof obligation in this integration.'},{'proof':'symmetric tree and two-group deletion','change':'Both remain; odd braid obstructs a common Boolean-deletion proof.'},{'proof':'cyclic classification and finite census','change':'Complete models, lift classification, bare-presentation order proofs and Appendix A retained unchanged apart from internal labels.'}],'no_net_shortening_claim':True,'ratio':None,'prior_frozen_files_modified':False}
(P/'phase39_compress_unified_assembly.json').write_text(json.dumps(account,indent=2)+'\n')
print('manuscript',len(text),'codepoints',sha(text.encode()))
