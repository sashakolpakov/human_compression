#!/usr/bin/env python3
"""Literal modular migration; no mathematical program executes here."""
from pathlib import Path
import argparse, hashlib, json
ROOT=Path(__file__).resolve().parent
SHA='fe996e58524d05efdf16f7e5c1222d15141697319f4121b6763e785e0aa771dd'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(x,msg):
 if not x:raise ValueError(msg)
def make(src):
 raw=src.read_bytes();require(sha(raw)==SHA,'exact frozen scientific predecessor');text=raw.decode()
 pre=text[:text.index('\\title')]
 a=text.index('\\section{Coset recognition');b=text.index('\\section{The complete Mathieu census}')
 c=text.index('\\begin{thebibliography}');d=text.index('\\end{thebibliography}')+len('\\end{thebibliography}')
 abstract=text[text.index('\\begin{abstract}'):text.index('\\end{abstract}')+len('\\end{abstract}')]
 generic=text[a:b];specific=text[b:c];refs=text[c:d]
 replacements=[('Proposition~\\ref{prop:orbits}','Common Proposition~3'),('Lemma~\\ref{lem:realize}','Common Lemma~1'),('Theorem~\\ref{thm:test}','Common Theorem~2')]
 edits=[]
 for old,new in replacements:
  count=specific.count(old);require(count==1,'exact imported reference count '+old)
  offset=text.index(old,b);edits.append(dict(start=offset,end=offset+len(old),old=old,new=new,reason='Explicit reference to the complete detached common paper; theorem numbers preserved.'))
  specific=specific.replace(old,new)
 common=pre+r'''\title{Coset recognition and exhaustive maximal-subgroup enumeration}
\author{Common proof for finite-group census applications}
\date{}
\begin{document}\maketitle
\begin{abstract}
Flag-transitive rank-three geometries with distinct maximal object stabilizers can be recognized by three subgroup-generation equations and one exact completion-orbit count. Stabilizer-orbit augmentation then exhausts the admissible unordered triples. We give the full elementary reductions used in the accompanying Mathieu census. The complete finite-group catalogue and exact algorithms remain separate application premises.
\end{abstract}
Throughout this common paper, $G$ is a finite group. This finiteness assumption is required when equality of cardinalities identifies the completion set with a single orbit.

'''+generic+r'''
\section*{Attribution and scope}
Coset realization, connectedness by subgroup generation and stabilizer-orbit augmentation are classical. The three complete proofs above are reproduced from the preceding corrected Mathieu proof edition, without using its group-specific census, geometric coordinates or software outputs. Their source application is the classification of Leemans and Rowley cited below. This paper does not establish catalogue completeness or a named-group identification. A complete application must supply those inputs and its full required computation.
\begin{thebibliography}{9}
\bibitem{LR} D. Leemans and P. Rowley, \emph{Rank three residually connected geometries for $M_{22}$, revisited}, Electronic Journal of Combinatorics 17 (2010), N4, 9 pp.
\end{thebibliography}
\end{document}
'''
 application=pre+r'''\title{The complete primitive Mathieu census and its source-table corrections}
\author{Complete corrected application}
\date{}
\begin{document}\maketitle
'''+abstract+r'''
This application uses the whole common paper \emph{Coset recognition and exhaustive maximal-subgroup enumeration}. Its definitions, distinguished-group equivalence and Common Lemma~1, Theorem~2 and Proposition~3 are imported together. All group-specific arguments, source qualifications and complete tables remain in this application and its two table supplements. We preserve the predecessor's theorem numbering.
\setcounter{theorem}{3}
\setcounter{section}{1}
'''+specific+refs+'\n\\end{document}\n'
 outputs={'common.tex':common,'mathieu-census.tex':application}
 spans=[]
 for name,start,end,newname,newtext in [('complete generic definitions and proofs',a,b,'common.tex',generic),('original abstract',text.index('\\begin{abstract}'),text.index('\\end{abstract}')+len('\\end{abstract}'),'mathieu-census.tex',abstract),('complete Mathieu proof and qualifications',b,c,'mathieu-census.tex',specific),('complete original bibliography',c,d,'mathieu-census.tex',refs)]:
  at=outputs[newname].index(newtext)
  spans.append(dict(name=name,old_start=start,old_end=end,old_sha256=sha(text[start:end].encode()),new_path=newname,new_start=at,new_end=at+len(newtext),new_sha256=sha(newtext.encode()),literal_except_imported_cross_references=name=='complete Mathieu proof and qualifications'))
 require(generic in common and specific in application and refs in application,'whole body preservation')
 require(not any(x in application for x,y in replacements),'no unresolved cross-paper references')
 return outputs,dict(status='LITERAL_MIGRATION_PENDING_DISTINCT_REVIEW',predecessor=dict(path='corpus161_L073_recovery/primitive-mathieu-geometries.tex',bytes=len(raw),sha256=SHA),offset_unit='Python Unicode code points',spans=spans,reference_changes=edits,added_scope='G is finite throughout the detached common paper; actual Mathieu application unchanged.',added_wrapper_text_only=True,all_scientific_body_preserved=True,new_proof_argument=False,scope_correction='The detached common paper explicitly requires finite G; this is a hypothesis correction, not literal mathematical identity.',source_contract_unchanged=True,factors=None)
def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);x=p.parse_args();require(not x.out.exists(),'fresh output');x.out.mkdir(parents=True)
 outputs,report=make(x.study_root/'corpus161_L073_recovery/primitive-mathieu-geometries.tex')
 for n,s in outputs.items():(x.out/n).write_text(s)
 (x.out/'migration.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(status='PASS',complete_generic_proofs=3,complete_application_statements=4,edited_cross_references=len(report['reference_changes']),no_counts_or_factors=True)))
if __name__=='__main__':main()
