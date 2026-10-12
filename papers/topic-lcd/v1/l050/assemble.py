#!/usr/bin/env python3
"""Assemble application proofs from fixed accepted notes; never edit predecessors."""
import argparse,difflib,hashlib,json
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def section_part(p,start,end):
 text=p.read_text();return text[text.index(start):text.index(end)]
def replace(s,old,new):
 if s.count(old)!=1:raise ValueError('nonunique replacement '+old[:90])
 return s.replace(old,new)
def cut(s,start,end,new):
 i=s.index(start);j=s.index(end,i);return s[:i]+new+s[j:]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args();PACKET=Path(__file__).resolve().parent;R=a.study_root;D=a.out or PACKET;rows=[]
 (D/'sections').mkdir(parents=True,exist_ok=True);(D/'data').mkdir(exist_ok=True)
 origins={k:'topic_LCD_'+v for k,v in [('module105','105_modules'),('module120','120_modules'),('module176','176_modules'),('module253','253_module'),('group120','120_graphcode_groups')]}
 def source(key):return (R/origins[key] if R else PACKET/'inputs'/key)/('proof.tex' if key=='group120' else 'modules.tex')
 def original_name(source):
  return str(source.relative_to(R)) if R else origins[source.parent.name]+'/'+source.name
 def save(source,name,original,new,description):
  (D/'sections'/name).write_text(new)
  rows.append({'source':original_name(source),'sha256':sha(source),'destination':'sections/'+name,'delta_description':description,'original_selected_text_sha256':hashlib.sha256(original.encode()).hexdigest(),'current_selected_text_sha256':hashlib.sha256(new.encode()).hexdigest()})
  (D/'data'/(name+'.diff')).write_text(''.join(difflib.unified_diff(original.splitlines(True),new.splitlines(True),fromfile=original_name(source),tofile='sections/'+name)))
 p=source('module105');old=section_part(p,r'\section{The graph and the two principal codes}',r'\end{document}');s=old
 s=cut(s,r'\section{The graph and the two principal codes}',r'Let $A$ be the adjacency matrix',r'\section{The codes on 105 flags}'+'\n\nThe graph is the one fixed in Section~1. Here write $C=C_{105}$ and\n$D=D_{105}$.\n\n')
 s=s.replace(r'\section{The full group and irreducibility}',r'\subsection{The full group and irreducibility}').replace(r'\section{Uniqueness inside the permutation module}',r'\subsection{Uniqueness inside the permutation module}').replace(r'\section{The other two twenty-dimensional modules}',r'\subsection{The other two twenty-dimensional modules}').replace(r'\section{Qualifications and attribution}',r'\subsection{The global and local representation claims}')
 s=replace(s,'A nonzero invariant subspace stable\nunder all these matrices is stable under every endomorphism, hence equals\n$D$. Independence persists over field extensions, so $D$ is absolutely\nirreducible.',r'The common matrix-algebra criterion \cite[Theorem~6.2]{U} therefore proves absolute irreducibility of $D$.')
 s=cut(s,'Refine vertex colours by old colour and neighbour-colour multiplicities,','Successively individualizing',r'Apply the common refinement bound \cite[Theorem~6.4]{U}. '+ '\n')
 s=replace(s,'All coordinate colours then differ. At each step a stabilizer orbit is\ncontained in the selected colour class; after the final step the\nstabilizer is trivial. Thus','All coordinate colours then differ, so the theorem gives')
 s=cut(s,'To avoid an\nunnecessarily large elimination', 'Here a recorded polynomial',r'For the $45$-dimensional factor use the rank-one alternative in that same theorem.'+'\n\n')
 s=s.replace(r'Lemma~\ref{lem:rankone}',r'the common rank-one test')
 s=cut(s,'For their remaining code parameters, we reuse the already proved','For $(n,k)=(105,20)$',r'For their remaining code parameters, apply the common transitive-distance and minimum-set theorems \cite[Theorems~8.1--8.2]{U} to the actual transitive group and row-reduced information columns.'+'\n')
 s=cut(s,'The common refinement and matrix-algebra arguments are the same as in','No whole-source admission,','The graph uniqueness input and all finite premises remain those stated above. Source comparisons to historical optimal-code tables are treated in the final section. Discovery used GRAPE and MeatAxe, but the final checks use literal generators, a full invariant filtration, matrix products and complete linear equations.\n')
 s=s[:s.index('No whole-source admission,')]+'\n'
 s=s.replace(r'\tag{1}',r'\tag{5}').replace('Consequently (1)','Consequently (5)').replace(r'\tag{2}',r'\tag{6}')
 save(p,'03-code105.tex',old,s,'Remove repeated graph setup and generic matrix/rank-one/refinement/averaging proofs; invoke the exact frozen U interfaces, retaining all local matrices, table transfers, uniqueness, socle and qualification arguments.')
 p=source('module120');old=section_part(p,r'\section{The incidence operator}',r'\paragraph{Limits.}');s=old
 s=s.replace(r'\section{The incidence operator}',r'\section{The socle on 120 Fano subplanes}')
 s=cut(s,r'\begin{lemma}\label{lem:square}','For the fixed family',r'The common square-zero incidence lemma \cite[Lemma~6.1]{U} will give self-orthogonality after the following integer table is checked.'+'\n\n')
 s=s.replace(r'Lemma~\ref{lem:square}',r'That common lemma')
 s=s.replace(r'\section{Recognizing the socle}',r'\subsection{Recognizing the socle}').replace(r'\section{Weights and full permutation automorphisms}',r'\subsection{Weights and full permutation automorphisms}')
 s=cut(s,'The following elementary criterion makes the\nremaining module calculation transparent.', 'Here $V=',r'We apply the common full-matrix-algebra and socle criteria \cite[Theorems~6.2--6.3]{U}; the whole filtration and all intertwiner spaces must be checked.'+'\n\n')
 s=s.replace(r'Lemma~\ref{lem:socle}',r'the common criterion')
 s=cut(s,'The dual distributions are obtained from the classical','In both\ncases the dual coefficients',r'The complete dual distributions follow from the common MacWilliams theorem \cite[Theorem~7.1]{U}. '+ '\n')
 s=s.replace('weight $4$8 word','weight-$48$ word')
 s=cut(s,'Here is a short upper-bound certificate','Successively individualize',r'The common refinement theorem \cite[Theorem~6.4]{U} bounds the full automorphism group of this structure. '+ '\n')
 s=cut(s,'After these choices all coordinate classes are singletons.','The explicit permutations',r'After these choices all coordinate classes are singletons. The theorem gives the upper bound $120\cdot21\cdot2\cdot4\cdot2\cdot2=80640$.'+'\n\n')
 save(p,'05-socle120.tex',old,s,'Remove generic square-zero/socle/matrix/refinement/MacWilliams repetitions and replace them by full-U references; retain all local construction, integer Gram data, filtration, Hom dimensions, counts and actual group hypotheses. Correct inherited typographic weight $4$8 to weight-48.')
 p=source('module176');old=section_part(p,r'\section{The common incidence calculation}',r'\end{document}');s=old
 s=cut(s,r'\section{The common incidence calculation}',r'\section{The exact module and group certificate}',r'''\section{The irreducible code on 176 residual blocks}
Here $H=H_1$, $C=C_{176}=H^{\mathsf T}(e^\perp)$ and $\dim C=21$ by (1).
The integral Gram matrix is $40I_{22}+16J_{22}$, reducing to $I_{22}+J_{22}$.
The common incidence theorem proves LCD and the two complement--dual
identities. The constant vector belongs to $C^\perp$, because its image
under $H$ is $56e$, which annihilates $e^\perp$. Thus the full orthogonal
decomposition in the source is established before any module classification.

''')
 s=s.replace(r'\section{The exact module and group certificate}',r'\subsection{The exact module and group certificate}').replace(r'\section{The precise source boundary}',r'\subsection{The precise representation boundary}')
 s=s.replace(r'Lemma~\ref{lem:support}',r'the common refinement theorem \cite[Theorem~6.4]{U}').replace(r'Lemma~\ref{lem:matrix}',r'the common matrix-algebra theorem \cite[Theorem~6.2]{U}')
 s=cut(s,'The complete retained weight distribution also determines the dual one','The certificate computes all coefficients',r'The complete retained weight distribution determines the dual by the common MacWilliams theorem \cite[Theorem~7.1]{U}.'+'\n')
 s=s.replace(r'\tag{3}',r'\tag{10}').replace('group in\n(3)','group in\n(10)').replace('consequence of (3)','consequence of (10)').replace('dimension. the common matrix-algebra','dimension. The common matrix-algebra')
 s=s[:s.index('The complete mandatory local files')]
 save(p,'06-code176.tex',old,s,'Move the full incidence, matrix-algebra, support-refinement and MacWilliams arguments to U; retain actual Gram coefficients, all local action/intertwining and support checks, full group and retained classification boundary.')
 p=source('module253');old=section_part(p,'Let $\\mathcal D$',r'\end{document}');s=old
 s=r'\section{The augmentation code on 253 heptads}'+'\n\n'+s
 s=cut(s,'There are $77$ heptads through each point','We next prove the irreducibility,',r'''The common residual-incidence theorem \cite[Theorem~2.2]{U} applies to the fixed system and gives $HH^{\mathsf T}=2I_{23}$,
$A=H^{\mathsf T}(J_{23}-I_{23})H$, $C=\im H^{\mathsf T}$ and the
orthogonal splitting $C=Fj\perp\!\oplus H^{\mathsf T}(e^\perp)$.
The two point-space summands are nondegenerate because $23\ne0$ in $F$.
Thus it proves both LCD statements and the displayed dimensions.

''')
 s=cut(s,'Any invariant subspace of $E$ is therefore stable','The existing enumeration records',r'The common full-matrix-algebra criterion \cite[Theorem~6.2]{U} proves absolute irreducibility of $E$ and its equivariant image $D$.'+'\n\n')
 s=cut(s,'The dual distributions follow from','All coefficients are evaluated',r'The dual distributions follow from the common MacWilliams theorem \cite[Theorem~7.1]{U}.'+'\n')
 s=cut(s,'It remains to prove that the displayed automorphism subgroup is full.','For an explicit upper bound,',r'''The $46$ words $h_i,-h_i$ are precisely the minimum words, by their weights and the complete count. The common Steiner recognition proposition \cite[Proposition~2.3]{U} therefore identifies $\Aut(C)$ with the block action of $\Aut(\mathcal D)$. This explicitly discharges its minimum-word hypothesis.

''')
 s=cut(s,'Each cell contains the orbit of its chosen point','Exact group computations',r'The common refinement theorem \cite[Theorem~6.4]{U} consequently bounds $|\Aut(\mathcal D)|$ by $23\cdot22\cdot21\cdot20\cdot16\cdot3=10200960$.'+'\n')
 s=s.replace(r'\begin{theorem}',r'\begin{theorem}\label{L050.253}')
 save(p,'07-code253.tex',old,s,'Retain exact augmentation representation matrices, complete distributions, group generators and classification qualifications; replace generic incidence, matrix-algebra, MacWilliams, recognition and refinement derivations by precise frozen U citations.')
 p=source('group120');old=section_part(p,r'\begin{theorem}\label{main}',r'\paragraph{Exact certificate');s=old
 s=r'\subsection{Full automorphism groups of the graph and difference codes}'+'\n\n'+s
 s=s.replace(r'\newpage','').replace(r'\F',r'\mathbb F')
 s=s.replace(' [3]', ' the retained degree-$120$ module certificate').replace('[3]', 'the retained degree-$120$ module certificate')
 for label in ['main','projection','support','fullness']:
  s=s.replace('{'+label+'}','{L050.120.'+label+'}')
 s=cut(s,'For the reverse inequality, color refinement','The following are the actual chosen vertices',r'For the reverse inequality, apply the common refinement theorem \cite[Theorem~6.4]{U}, using the deterministic choice of the first vertex in the smallest nonsingleton cell (lexicographic ties). '+'\n')
 s=cut(s,'After the last refinement all 120 cells are singletons,','This matches the subgroup lower bound.',r'After the last refinement all 120 cells are singletons. The common theorem gives $|\Aut(\Gamma)|\le120\cdot42\cdot8\cdot2=80640$.'+'\n')
 s=s.replace('The retained exact bases','The retained exact bases')
 s=s.replace('The complete minimum-word count is 112','The complete minimum-word count is 112')
 s=s.replace('The retained complete minimum-word count is 112','The complete distribution in (4) gives exactly 112 minimum words')
 s=s.replace('four coordinate generators retained in the retained','four coordinate generators of the retained')
 s=s.replace('Here $G$ is the group on the literal four coordinate generators retained in the retained degree-$120$ module certificate.', 'Here $G$ is the group on the literal four coordinate generators of the retained degree-$120$ module certificate.')
 s=s.replace('the abstract identification is retained from the retained degree-$120$ module certificate.', 'the abstract identification uses that earlier exact group certificate.')
 s=s.replace(r'\subsection{Full automorphism groups of the graph and difference codes}',r'\subsection{Full automorphism groups of the graph and difference codes}'+'\n\nLet $\\Gamma$ be the fixed length-$120$ graph, write $A=A_{120}$ and $C=C_{120}$, and let $G$ be the supplied group on its coordinates.')
 save(p,'04b-group120.tex',old,s,'Migrate the entire actual projector, minimum-support recovery, group lower bound and local refinement chain from the distinct-authored bridge; use U only for the generic refinement bound. Keep the retained complete112 count explicit.')
 (D/'migration.json').write_text(json.dumps({'status':'AUTHOR_ASSEMBLY_IN_PROGRESS','rows':rows,'frozen_common_manifest_sha256':'f7e364bda66b12e60a390e85aa45ed68336852d9f596bc93a631324138e0f1d1','common_root_adoption_sha256':'bd3cbb1d290568255d5dd693ec9f1550109c2e7d1f9896ea75b0a33b1ea6dc32','generic_statements_removed_only_with_exact_common_references':True},indent=2)+'\n')
if __name__=='__main__':main()
