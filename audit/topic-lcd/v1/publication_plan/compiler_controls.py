#!/usr/bin/env python3
"""Bounded tests for the optional compiler field; no scientific execution."""
import argparse,ast,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists(),'fresh report path')
 old=a.public_root/'scripts/build_papers.py';baseline=json.loads((HERE/'public_baseline.json').read_text());expected=next(x for x in baseline['files']if x['path']=='scripts/build_papers.py');need(sha(old)==expected['sha256'],'bound prior builder')
 new=HERE/'build_papers.py';spec=importlib.util.spec_from_file_location('lcd_proposed_builder',new);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 seen=[]
 def finder(name):seen.append(name);return '/verified/'+name
 names,commands=m.compiler_commands([{'id':'old'},{'id':'new','compiler':'pdflatex'},{'id':'xe','compiler':'xelatex'}],finder)
 need(names=={'old':'xelatex','new':'pdflatex','xe':'xelatex'}and commands=={'pdflatex':'/verified/pdflatex','xelatex':'/verified/xelatex'}and seen==['pdflatex','xelatex'],'complete explicit/default dispatch')
 need(m.compiler_commands([{'id':'only-old'}],lambda n:'/xe'if n=='xelatex'else None)==({'only-old':'xelatex'},{'xelatex':'/xe'}),'legacy xelatex requires no pdflatex')
 rejected=[]
 for name in ['lualatex','/tmp/pdflatex','pdflatex -shell-escape','xelatex;echo',None,[],42]:
  try:m.compiler_commands([{'id':'bad','compiler':name}],finder)
  except ValueError:rejected.append(repr(name))
  else:raise ValueError('invalid compiler accepted')
 try:m.compiler_commands([{'id':'missing','compiler':'pdflatex'}],lambda n:None)
 except ValueError:rejected.append('missing declared compiler')
 else:raise ValueError('missing compiler accepted')
 def funcs(p):return{n.name:ast.dump(n,include_attributes=False)for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)and n.name!='main'}
 o,n=funcs(old),funcs(new);need(all(n[k]==v for k,v in o.items()),'all existing nonmain build functions unchanged');need(set(n)-set(o)=={'compiler_commands'},'single bounded new helper')
 report=dict(status='PASS_COMPILER_FIELD_CONTROLS',old_builder_sha256=sha(old),proposed_builder_sha256=sha(new),unchanged_existing_nonmain_functions=sorted(o),default='xelatex',explicit_alternative='pdflatex',positive_cases=2,rejected_cases=rejected,no_program_or_Lean_replay=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
