#!/usr/bin/env python3
"""Render the complete computed class and physical-source-row tables."""
import argparse,json
from pathlib import Path
R=Path(__file__).resolve().parent
PRE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,longtable,hyperref,fvextra}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\setmonofont{Menlo}
\setlength{\LTpre}{4pt}\setlength{\LTpost}{4pt}
'''
SHAPES={'1':'1','2':'2','3':'3','4':'4','22':'2^2','23':'2^3','24':'2^4','232':'2^3 2','322':'3^2 2','242':'2^4 2','2222':'2^2 2^2','2322':'2^3 2^2','324':'3^2 4','243':'2^4 3','22A4':'2^2 A_4','22D8':'2^2 D_8','2422':'2^4 2^2','24A4':'2^4 A_4','2× D8':'2\\times D_8','A5':'A_5','S3':'S_3','D8':'D_8','Q8':'Q_8','D10':'D_{10}','A4':'A_4','D12':'D_{12}','F21':'F_{21}','S4':'S_4'}
def texlabel(s):
 import re
 m=re.fullmatch(r'M(\d{3})\((.*)\)',s);parts=m[2].split(':');vals=[]
 for x in parts[0].split(','):
  x=x.strip();vals.append(x[0]+'_'+x[1] if len(x)==2 else x)
 return 'M_{'+m[1]+'}('+','.join(vals)+(':'+parts[1].strip() if len(parts)>1 else '')+')'
def candidate(row,k):
 ids=row['candidates'][k]
 if ids is None:return '?'
 if not ids:return '--'
 good=row['shape_compatible'][k]
 text=','.join(str(i)+('!'if i not in good else '') for i in ids)
 if k=='explicit_pair_objects' and row['provisional_literal_pair_labels']:text+='p'
 return text

def build(data,out):
 d=json.loads(data.read_text());out.mkdir(exist_ok=True)
 text=PRE+r'''\title{Complete class tables for the $M_{22}$ census}\author{}\date{}\begin{document}\maketitle
These are new witness identifiers, not the unavailable historical \texttt{geo[]} numbers. Type names and the exact equivalence convention are defined in the accompanying proof. Every Borel identifier $[n,k]$ means \texttt{SmallGroup(n,k)}, fixing the abstract group rather than only its order. Full literal permutation representatives are in the bound witness file. The tables contain all 81 pairs and all 431 triples; no representative is omitted because its source label is problematic.
\section*{Rank two}
The signature is $(t_1,t_2,|X_1\cap X_2|,|H_1\cap H_2|)$, minimized over the canonical orientations and type reorderings.\small
\begin{longtable}{r|rrrr|rr}\toprule
ID&$t_1$&$t_2$&$|X_1\cap X_2|$&$|H_{12}|$&$n$&$k$\\\midrule\endhead
'''
 # Use complete canonical pair data; the reconciliation also binds broad pairs.
 cp=json.loads((data.parent/'canonical_pairs.json').read_text())
 for w in cp['triples']:text+=' & '.join(map(str,[w['witness']]+min(w['signatures'])+w['borel_id']))+r'\\'+'\n'
 text+=r'''\bottomrule\end{longtable}\normalsize
\section*{Rank three}
Columns give the least canonical signature $(t_1,t_2,t_3,x_{12},x_{13},x_{23},h_{12},h_{13},h_{23})$ and exact Borel identifier $[n,k]$. Here $x_{ij}=|X_i\cap X_j|$ and $h_{ij}=|H_i\cap H_j|$.\small
\begin{longtable}{r|rrr|rrr|rrr|rr}\toprule
ID&$t_1$&$t_2$&$t_3$&$x_{12}$&$x_{13}$&$x_{23}$&$h_{12}$&$h_{13}$&$h_{23}$&$n$&$k$\\\midrule\endhead
'''
 for w in d['replacement_triples']:text+=' & '.join(map(str,[w['witness']]+min(w['signatures'])+w['borel_id']))+r'\\'+'\n'
 text+=r'\bottomrule\end{longtable}\end{document}'+'\n';(out/'class-tables.tex').write_text(text)
 text=PRE+r'''\title{All physical rows of the 2010 $M_{22}$ table}\author{}\date{}\begin{document}\maketitle
Row means the consecutive physical row, reading each line left then right; $N$ preserves the printed historical Number and $p$ the physical page. The source label and Borel column are transcribed literally, with mathematical subscripts restored. The three candidate columns use: K, canonical endecads and the predecessor's pair-order table; O, both endecad complements and that order table; L, both complements and literal predecessor objects. A colon in L uses its actual displayed triple.

A number identifies a computed class satisfying the label interpretation. An exclamation mark means that its actual Borel is incompatible with the printed shape. A dash means no class satisfies that interpretation; a question mark means a defining literal object is invalid. Suffix p marks the explicitly provisional fourth-displayed-endecad reading for the undefined name $e_4$. Juxtaposed Borel extensions are tested only for a normal elementary abelian kernel and named quotient, without inferring an unprinted action or splitting. No column is an asserted reconstruction of the intended \texttt{geo[]} numbering. The mathematical result is the complete separate 431-class table.
\small
\begin{longtable}{rrr|l|l|rrr}\toprule
row&$p$&$N$&source label&Borel&K&O&L\\\midrule\endhead
'''
 for row in d['source_rows']:
  vals=[str(row['row']),str(row['page']),str(row['source_number']),'$'+texlabel(row['label_text'])+'$','$'+SHAPES[row['Borel_text']]+'$']+[candidate(row,k) for k in ['canonical_pair_order','source_pair_order','explicit_pair_objects']]
  text+=' & '.join(vals)+r'\\'+'\n'
 text+=r'\bottomrule\end{longtable}\end{document}'+'\n';(out/'source-rows.tex').write_text(text)
 programs=['phase164_m22_census.g','phase164_m22_validate.g','orbit_coordinates.g','phase180_code_completions.py','phase180_mog_check.g','phase180_borel_check.g','reconcile.py']
 text=PRE+r'''\title{Complete mathematical programs for the $M_{22}$ census}\author{}\date{}\begin{document}\maketitle
Every required mathematical program is printed in full. The census and validator reuse the previously reviewed programs byte-for-byte. The coordinate program extends the earlier shadow proof to rank two and the source's independent endecad complements. The complete labelled-code, literal-configuration and Borel programs are reused; the reconciliation keeps all interpretations separate. The driver and table-formatting script are separately bound auxiliary files, not mathematical premises hidden by excerpts. Catalogue, exact-algorithm and classical group-identification trust remains as stated in the proof. No Lean claim is made.
'''
 for name in programs:
  text+='\\section*{\\texttt{'+name.replace('_',r'\_')+'}}\n'+r'\VerbatimInput[fontsize=\scriptsize,breaklines=true,breakanywhere=true,breaksymbolleft={},breaksymbolright={},breakanywheresymbolpre={},breakanywheresymbolpost={}]{programs/'+name+'}\n'
 text+=r'\end{document}'+'\n';(out/'required-programs.tex').write_text(text)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.evidence/'reconciliation.json',a.out)
