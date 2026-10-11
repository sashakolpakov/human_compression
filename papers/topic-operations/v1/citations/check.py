#!/usr/bin/env python3
"""Verify exact citation-only overlays; optionally rebuild both documents."""
from pathlib import Path
import argparse,json,hashlib,re,subprocess,shutil
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
S=Path('/Users/sasha/medusa/research/leemans');P=Path('/Users/sasha/medusa/math_compression')
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def envs(t):return [m.group(0) for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',t,re.S)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 def remap(s):
  p=Path(s)
  if p.is_relative_to(P):return a.public_root/p.relative_to(P)
  if p.is_relative_to(S):return a.study_root/p.relative_to(S)
  return p
 def bound(row):
  p=remap(row['path']);b=p.read_bytes();need(sha(b)==row['sha256'] and len(b)==row['bytes'],'exact bound file '+str(p));return p
 if (HERE/'manifest.json').exists():
  for r in json.loads((HERE/'manifest.json').read_text())['exports']:
   b=(HERE/r['path']).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'frozen export')
 edition=json.loads((HERE/'edition.json').read_text());bound(edition['proposal_manifest']);bound(edition['integrated_review']);proposal_path=remap(edition['proposal_manifest']['path']).parent/'citation_proposals.json';proposals=json.loads(proposal_path.read_text());reports=[]
 for row in edition['documents']:
  key=row['original'];base=bound(row['base']);prop=next(e for e in proposals['editions'] if e['original']==key);before=base.read_text();after=before
  for e in prop['edits']:need(after.count(e['old'])==1,'unique old anchor');after=after.replace(e['old'],e['new'],1)
  new=HERE/key/base.name;pdf=new.with_suffix('.pdf');need(new.read_text()==after and sha(new.read_bytes())==row['new_tex']['sha256']==prop['proposed_tex_sha256'],'exact proposed text');need(sha(pdf.read_bytes())==row['pdf']['sha256'],'final PDF');need(envs(before)==envs(after) and len(envs(after))==row['identical_environments'],'complete environments unchanged');need((HERE/key/'preamble.tex').read_bytes()==(base.parent/'preamble.tex').read_bytes(),'unchanged preamble');need(len(PdfReader(pdf).pages)==row['pages'],'whole PDF page extent')
  # Actual theorem/proof substitution is rejected, independently of the complete file hash.
  bad=after.replace(r'\begin{proof}',r'\begin{proof} False extra premise.',1);need(envs(before)!=envs(bad),'proof-change control')
  r=dict(original=key,statements_and_proofs_unchanged=len(envs(after)),pages=row['pages'],rendered=False,proof_change_control_rejected=True)
  if a.render:
   d=a.out/key;d.mkdir();shutil.copyfile(new,d/new.name);shutil.copyfile(HERE/key/'preamble.tex',d/'preamble.tex')
   for i in range(2):
    result=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-file-line-error',new.name],cwd=d,capture_output=True,text=True);(d/f'build{i+1}.stdout').write_text(result.stdout);(d/f'build{i+1}.stderr').write_text(result.stderr);need(result.returncode==0,'fresh build')
   lines=(d/new.with_suffix('.log').name).read_text(errors='replace').splitlines();diag=[x for x in lines if any(s in x for s in ['Overfull','Underfull','Missing character','undefined','LaTeX Warning'])];need(diag==row['diagnostics'],'exact declared typography diagnostics')
   pages=[p.extract_text() or '' for p in PdfReader(d/pdf.name).pages];need(pages==[p.extract_text() or '' for p in PdfReader(pdf).pages],'fresh every-page text equality');r.update(rendered=True,per_page_text_identical=True,diagnostics=diag)
  reports.append(r)
 report=dict(status='PASS',scope='Exact citation/interface overlay, not a new mathematical review',documents=reports,scientific_programs_run=False,new_mathematical_results=0,ratios=None);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',pages=sum(r['pages'] for r in reports),unchanged_environments=sum(r['statements_and_proofs_unchanged'] for r in reports),rendered=a.render)))
if __name__=='__main__':main()
