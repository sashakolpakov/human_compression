#!/usr/bin/env python3
"""Independent exact passage and dependency audit for the detached L073 papers."""
import argparse,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
PIN='50f4c08a990f3d6e43f4544fe5daa8e819649a62f5fbe47f7f89b9b8aa3b463d'
SCIENCE='13aa42fa08b4a6517945c91c08c51ee3eaec87f572662dad991fe9b519cd6676'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(root,r):
 p=Path(r['path']);need(not p.is_absolute()and'..'not in p.parts,'safe relative path');p=root/p
 need(p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'whole file '+str(p));return p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();s=a.study_root;h=s/'corpus161_L073_modular';old=s/'corpus161_L073_recovery'
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 need(sha(h/'manifest.json')==PIN and sha(s/'corpus161_L073_root_review/manifest.json')==SCIENCE,'exact author/science editions')
 exports=read(h/'manifest.json')['exports']
 for r in exports:bound(h,r)
 source=(old/'primitive-mathieu-geometries.tex').read_text();common=(h/'common.tex').read_text();app=(h/'mathieu-census.tex').read_text()
 start=source.index('\\section{Coset recognition');cut=source.index('\\section{The complete Mathieu census}');bib=source.index('\\begin{thebibliography}');end=source.index('\\end{document}')
 need(source[start:cut]in common,'whole definitions and all three generic proofs moved literally')
 body=source[cut:bib]
 refs=[('Proposition~\\ref{prop:orbits}','Common Proposition~3'),('Lemma~\\ref{lem:realize}','Common Lemma~1'),('Theorem~\\ref{thm:test}','Common Theorem~2')]
 for oldref,newref in refs:need(body.count(oldref)==1,'unique imported reference');body=body.replace(oldref,newref)
 need(body in app and source[bib:end]in app,'every group-specific proof and whole bibliography retained')
 abstract=source[source.index('\\begin{abstract}'):source.index('\\end{abstract}')+len('\\end{abstract}')]
 need(abstract in app,'complete scientific abstract retained')
 need('Throughout this common paper, $G$ is a finite group.'in common,'required finite scope correction')
 need('\\setcounter{theorem}{3}'in app and '\\setcounter{section}{1}'in app,'old theorem and section numbering')
 for label,n in [('lem:realize',1),('thm:test',2),('prop:orbits',3)]:
  need('\\label{'+label+'}'in common,'common labelled theorem '+label)
 a0=read(h/'arrangement.json');rows=[a0['source'],a0['retained_notation_source'],a0['common'],*a0['application'],a0['printed_programs'],*a0['scientific_bindings'],*a0['raw_programs'],*a0['required_raw_data'],*a0['auxiliary_scripts'],*a0['generated_outputs']]
 for r in rows:
  p=bound(s,r)
  if 'tex'in r:bound(s,r['tex'])
  if p.name=='manifest.json':
   for q in read(p)['exports']:bound(p.parent,q)
 need(a0['source']['pages']==9 and a0['retained_notation_source']['pages']==48,'source editions distinct')
 need([x['pages']for x in [a0['common'],*a0['application'],a0['printed_programs']]]==[2,5,10,9,11],'whole common/applications/programs')
 for x in [a0['common'],*a0['application'],a0['printed_programs']]:need(len(PdfReader(s/x['path']).pages)==x['pages'],'actual physical extent')
 need([len(a0[k])for k in ['raw_programs','required_raw_data','auxiliary_scripts','generated_outputs']]==[7,2,3,10],'whole dependency inventory')
 need(sum(x['bytes']for x in a0['required_raw_data'])==83965,'both entire required JSON inputs')
 for cat in ['raw_programs','required_raw_data','auxiliary_scripts','generated_outputs']:
  need(all(x['whole_file']for x in a0[cat]),'whole files required')
 need(a0['whole_common_required']and a0['no_old_umbrella_premise']and a0['no_L095_special_theorem_premise'],'no free external umbrella')
 need(a0['printed_and_raw_programs_are_alternatives']and a0['required_raw_data_has_no_complete_printed_alternative'],'complete computational alternatives')
 need(not a0['historical_geo_numbering_recovered']and not a0['predecessor_full_recovery']and a0['formal_declarations']==0 and a0['factor']is None,'retained limitations')
 report=dict(status='PASS_DISTINCT_ROOT_MODULAR_L073',author_manifest_sha256=PIN,prior_science_manifest_sha256=SCIENCE,author_exports=len(exports),author_program_imports=False,all_generic_and_application_proof_passages_preserved=True,imported_cross_reference_changes=3,finite_scope_correction=True,whole_common_pages=2,whole_application_pages=24,whole_program_pages=11,required_raw_input_bytes=83965,scientific_programs_rerun=False,formal_declarations=0,new_original_credit=0,compression_factor=None)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
