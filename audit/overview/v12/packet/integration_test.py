#!/usr/bin/env python3
"""Bounded private shadow integration; never writes through public symlinks."""
from pathlib import Path
import argparse,ast,importlib.util,json,os,shutil,subprocess,sys
from build import HERE,read,need,sha
from check import nonmain

def shadow(public,dst):
 dst.mkdir(parents=True)
 for base,dirs,files in os.walk(public):
  dirs[:]=[x for x in dirs if x not in ['.git','__pycache__']]
  target=dst/Path(base).relative_to(public);target.mkdir(parents=True,exist_ok=True)
  for f in files:(target/f).symlink_to(Path(base)/f)
def replace(dst,data):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.is_symlink()or dst.exists():dst.unlink()
 dst.write_bytes(data)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh shadow output');a.out.mkdir();root=a.out/'public';shadow(a.public_root,root)
 # Only private copies below are replaced; no shared file is opened for writing.
 packet=root/'audit/overview/v12/packet';packet.mkdir(parents=True,exist_ok=True)
 for p in HERE.rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:replace(packet/p.relative_to(HERE),p.read_bytes())
 replace(root/'README.rst',(HERE/'proposed/README.rst').read_bytes())
 pointer=read('proposed/latest.template.json');replace(root/'audit/overview/latest.json',json.dumps(pointer).encode())
 old=(HERE/'inputs/v11_verify_snapshot.py').read_text();snippet=(HERE/'proposed/verifier_additions.py').read_text();modified=old.replace('\ndef main():','\n'+snippet+'\n\ndef main():',1);call='    current_fractions, current_bars = check_listing_symmetry_overview()';need(modified.count(call)==1,'one old current call');modified=modified.replace(call,'    check_historical_listing_symmetry_overview()\n    current_fractions, current_bars = check_listing_restored_overview()');replace(root/'scripts/verify_snapshot.py',modified.encode())
 old_ast=nonmain(old);new_ast=nonmain(modified);need(all(new_ast.get(n)==h for n,h in old_ast.items()),'all prior non-main functions exact');need(set(new_ast)-set(old_ast)=={'check_historical_listing_symmetry_overview','check_listing_restored_overview'},'only two added functions')
 spec=importlib.util.spec_from_file_location('v12_shadow_snapshot',root/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 result=m.check_historical_listing_symmetry_overview();need(result==(56,128),'historical v11 still checks exact old scope despite new current README/pointer')
 controls=[]
 def fail(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError,OSError):controls.append(name);return
  raise ValueError('unrejected '+name)
 fail('direct unwrapped old check sees unresolved new admission',m.check_listing_symmetry_overview)
 from types import FunctionType
 f=m.check_listing_symmetry_overview
 gl=dict(f.__globals__,load=lambda path:m.load('audit/overview/v12/packet/inputs/v11_pointer.json'if str(path)=='audit/overview/latest.json'else path))
 incomplete=FunctionType(f.__code__,gl,f.__name__,f.__defaults__,f.__closure__)
 fail('pointer-only wrapper fails on new root README',incomplete)
 rp=packet/'inputs/v11_README.rst';good=rp.read_bytes();replace(rp,good+b'corruption');fail('altered historical README snapshot rejected',m.check_historical_listing_symmetry_overview);replace(rp,good)
 pp=packet/'inputs/v11_pointer.json';good=pp.read_bytes();replace(pp,good+b' ');fail('altered historical pointer snapshot rejected',m.check_historical_listing_symmetry_overview);replace(pp,good)
 rp=packet/'inputs/v11_README.rst';good=rp.read_bytes();replace(rp,b'new root README without old holds');fail('new README cannot stand in for old',m.check_historical_listing_symmetry_overview);replace(rp,good)
 report=dict(status='PASS',scope='Private shadow only; no root admission fabricated or claimed',prior_nonmain_ASTs_preserved=len(old_ast),new_functions=sorted(set(new_ast)-set(old_ast)),historical_wrapper_result=list(result),negative_controls=len(controls),rejected=controls,public_files_written=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
