from pathlib import Path
import subprocess,json,hashlib,re
C=Path(__file__).resolve().parent; S=C.parents[2]
header=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,hyperref,longtable,booktabs,array}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\emergencystretch=1em
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcommand{\pandocbounded}[1]{#1}
'''
rows=[
('descent','phase7_suzuki_descent.md','Field descent and compatible tori','## 1. Main statements','## 9. Executable and formal evidence'),
('torus_families','phase7_suzuki_torus_families.md','Subfield and torus geometries','## 1. Source parameters','## 6. Extra exact checks'),
('pure_mixed','phase8_suzuki_subfields.md','Pure subfield geometries and a scalar obstruction','## 1. Exact source scope','## 6. Scope and proposed correction')]
editions=[]
replacements={
'phase-six':'earlier','phase-seven':'descent','phase six':'earlier',
'The phase-six':'The earlier','The main note':'The companion descent paper','the main note':'the companion descent paper',
'conditional-on-admissible-parameters realization theorem':'realization theorem for every admissible parameter tuple',
'overlapping-prime cases':'cases in which a selected prime divides the base order',
'Source parameters, including the lower-field restriction':'Source parameters and the base field',
'Coset coordinates without a coprime-base assumption':'Cyclic coset coordinates',
'The new exact seed check':'The retained exact seed check','The new seed checker':'The retained seed checker','The new checker':'The retained checker',
"the main note's":"the companion descent paper's",'of the main note':'of the companion descent paper',
'phase-seven Theorem C':'Theorem C of the companion descent paper',
'phase-seven files':'earlier files',
'## 2. Cyclic descent and subfield-coset Helly':'## 2. Cyclic descent and intersections of subfield cosets',
'## 4. One binary algebra, compatible tori in every odd degree':'## 4. Compatible tori in every odd degree',
'**Theorem C: coprime subfield-coset Helly.**':'**Theorem C: intersections of subfield cosets.**',
'Lang–Helly':'descent and coset-intersection',
'The standard subfield types satisfy Theorem C of the companion descent paper.':'The standard subfield types satisfy Theorem C of the companion descent paper.'}
for name,source,title,start,end in rows:
 p=S/source;raw=p.read_text();a=raw.index(start);b=raw.index(end)
 body=raw[a:b]
 applied=[]
 for old,new in replacements.items():
  if old in body:body=body.replace(old,new);applied.append([old,new])
 if name=='descent':
  body=body.replace('The rank-four configuration in\n[phase6_suzuki_realization.md](phase6_suzuki_realization.md) is a','The previously acquired rank-four configuration, described by the explicit groups below, is a')
  body=body.replace('This closes the geometric gap left in that note: the argument\nbelow establishes','The argument below establishes')
  body=body.replace('This is a proof supplement to the immutable\nearlier finite record, whose “unproved” statements correctly describe what\nhad been established at that earlier stage.','This supplies the geometric proof for that exact previously acquired configuration.')
 body=body.replace('They prove connectedness of every residue','They prove connectedness of every residue')
 intro=('This manuscript reassembles previously checked arguments for the fixed higher-rank Suzuki source. '
 'The exact earlier notes, finite certificates and independent reviews remain retained. '
 'Editorial changes give descriptive references and remove operational instructions; the mathematical scope is unchanged. '
 'Classical group-theoretic inputs are stated explicitly.\n\n')
 intro={
 'descent':'Lang--Steinberg descent gives a common representative for pairwise incident cosets of subgroups fixed by independent field automorphisms. Cyclic coset coordinates then add a torus normalizer as another type. We prove the resulting Suzuki geometries are thick, residually connected and residually weakly primitive in every rank. The proof retains classical Suzuki structure and Lang--Steinberg, and includes the exact finite matrices used to choose compatible tori.\n\n',
 'torus_families':'We realize every admissible parameter tuple in Constructions 8 and 9 of the fixed Suzuki source. A valuation calculation gives all intersections, including the cases in which a selected prime divides the base torus order. Descent and cyclic coset coordinates prove flag transitivity; the same intersections give thickness, residual connectedness and residual weak primitivity.\n\n',
 'pure_mixed':'For standard simple subfield parabolics, the exact criterion for residual weak primitivity is that their common subfield remain simple. Descent proves that the resulting geometries are thick, residually connected and flag-transitive. In the mixed parabolic of Construction 10, maximality is instead equivalent to a scalar codimension of one; this disproves the source claim for every prescribed parameter.\n\n'}[name]
 proc=subprocess.run(['/opt/homebrew/bin/pandoc','--from=markdown+tex_math_single_backslash','--to=latex'],input=(intro+body).encode(),capture_output=True,check=True)
 tex=header+'\\title{'+title+'}\n\\author{Human Compression project}\\date{}\n\\begin{document}\\maketitle\n'+proc.stdout.decode()+'\n\\end{document}\n'
 tex=re.sub(r'\\subsection\{\d+\. ',r'\\section{',tex)
 tex=tex.replace(r'\subsubsection{',r'\subsection{')
 if name=='descent':
  anchor='The exact order-13 matrix'
  insert=r"""For reference, the acquired seed matrices are
\[
 M=\begin{pmatrix}1&1&1&0\\0&0&1&1\\0&1&1&1\\1&0&0&0\end{pmatrix},
 \qquad r=\begin{pmatrix}1&0&0&0\\1&1&0&0\\1&1&1&0\\1&0&1&1\end{pmatrix}.
\]
The order-thirteen seed, in
$\mathbb F_8=\mathbb F_2[z]/(z^3+z+1)$, is
\[
 a=\begin{pmatrix}
 z^2+z+1&0&1&z^2+1\\
 1&z&z^2&1\\
 z^2&z^2&z+1&z^2+1\\
 z^2&1&z^2&z+1
 \end{pmatrix}.
\]
These are the literal previously checked matrices. The retained checks
verify group membership, order, centralization, the exceptional
endomorphism identities, and both twenty-element binary centralizers;
no search is needed to verify these displayed identities.

"""
  if tex.count(anchor)!=1:raise ValueError('seed insertion anchor')
  tex=tex.replace(anchor,insert+anchor)
 # Literal references use manuscript names, while exact source paths remain in the editorial ledger.
 labels={'phase6_suzuki_realization.md':'Earlier finite torus construction','phase7_suzuki_descent.md':'Field descent and compatible tori','phase5_suzuki_higher.md':'Earlier subfield and scalar proofs','phase6_suzuki_torus_check.json':'Exact finite torus certificate'}
 for path,label in labels.items():
  tex=tex.replace('\\href{'+path+'}{'+path.replace('_','\\_')+'}',label).replace('\\url{'+path+'}',label)
 (C/(name+'.tex')).write_text(tex)
 editions.append(dict(output=name+'.tex',source=source,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),selected_start=start,selected_end=end,replacements=applied,policy='Exact mathematical proof reassembly; narrative provenance and references updated; no finite acquisition or theorem scope enlargement.'))
(C/'editorial_sources.json').write_text(json.dumps(editions,indent=2)+'\n')
