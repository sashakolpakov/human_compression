#!/usr/bin/env python3
"""Distinct whole-file appendix/render review; no scientific execution."""
import argparse,copy,hashlib,json,re,shutil,subprocess,unicodedata
from pathlib import Path
from pypdf import PdfReader
PIN='8e9fa6a10c70c244c143df572643b305b4fad14912dd88111da7082189c9db05'
FILES={'check_examples.g':'topic_B_L020_positive_v2/check_examples.g','check_models.g':'topic_B_L020_positive_v2/check_models.g','check_case.py':'topic_B_L020_case_three_correction/check_case.py'}
def need(b,m):
 if not b:raise ValueError(m)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def valid_tex(tex):
 need(re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)==list(FILES),'exact three complete inputs')
 need(not re.search(r'firstline|lastline|firstnumber|lastnumber',tex),'no partial inclusion')
def full_print(pages,files):
 need(len(pages)==3,'all three pages');ss=[]
 for i,p in enumerate(pages,1):
  lines=p.splitlines();need(lines[-1]==str(i),'footer');ss.append('\n'.join(lines[:-1]))
 compact=lambda t:''.join(unicodedata.normalize('NFKC',t).split())
 t=compact('\n'.join(ss));ranges=[]
 for name,b in files.items():
  s=compact(b.decode());need(t.count(s)==1,'whole file printed exactly once '+name);ranges.append((t.index(s),t.index(s)+len(s)))
 need(ranges==sorted(ranges) and all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'whole files in order and disjoint')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 p=a.study_root/'topic_B_L020_complete_programs';need(h(p/'manifest.json')==PIN,'exact author manifest');m=json.loads((p/'manifest.json').read_text())
 for e in m['exports']:need((p/e['path']).stat().st_size==e['bytes'] and h(p/e['path'])==e['sha256'],'unchanged author export')
 files={}
 for name,src in FILES.items():
  b=(p/name).read_bytes();need(b==(a.study_root/src).read_bytes(),'whole program source bytes');files[name]=b;(a.out/name).write_bytes(b)
 tex=(p/'programs.tex').read_text();valid_tex(tex);(a.out/'programs.tex').write_text(tex)
 for i in range(2):
  q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','programs.tex'],cwd=a.out,capture_output=True);(a.out/f'render{i}.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'fresh XeLaTeX')
 log=(a.out/'programs.log').read_text();diag=[s for s in log.splitlines() if any(k in s for k in ['Overfull','Underfull','Missing character','LaTeX Warning','Font Warning'])];need(not diag,'empty diagnostics')
 pages=[x.extract_text() for x in PdfReader(a.out/'programs.pdf').pages];need(pages==[x.extract_text() for x in PdfReader(p/'programs.pdf').pages],'all three per-page text identities');full_print(pages,files)
 controls=[]
 def reject(name,fn):
  try:fn()
  except ValueError:controls.append(name);return
  raise ValueError('control accepted '+name)
 reject('omit counterexample file',lambda:valid_tex(tex.replace('{check_case.py}','{check_models.g}')))
 reject('slice a program',lambda:valid_tex(tex.replace('fontsize=','firstline=2,fontsize=',1)))
 reject('drop last page',lambda:full_print(pages[:-1],files))
 bad=copy.deepcopy(files);bad['check_case.py']=bad['check_case.py']+b'\nINVENTED_TOKEN\n';reject('alter source program',lambda:full_print(pages,bad))
 r=dict(status='ACCEPTED_COMPLETE_PRINTING_APPENDIX',author_manifest_sha256=PIN,source_files=3,whole_program_bytes=sum(map(len,files.values())),pages=3,exact_page_text=True,diagnostics=diag,negative_controls=controls,science_or_GAP_Lean_replayed=False,replaces_old_two_page_appendix=True)
 (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
