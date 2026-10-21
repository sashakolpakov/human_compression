#!/usr/bin/env python3
"""Bounded exact-delta controls on private copies, not changes to frozen files."""
import argparse,json,shutil,tempfile
from pathlib import Path
import bibliography_check as b

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();b.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 original=b.ROOT;rows=[]
 changes=[('wrong_page_range','umbrella.tex',lambda s:s.replace('493--516','494--516')),('proof_text_change','chiral-projective-lines.tex',lambda s:s.replace('\\begin{proof}','\\begin{proof} Changed. ',1)),('source_scope_change','scope.json',lambda s:s.replace('L056','L055',1)),('required_data_edited','programs/psl2_square_witnesses.json',lambda s:s+' '),('formal_proof_edited','formal/ProjectiveTraceExtension.lean',lambda s:s+'\n-- mutation\n'),('bad_context_binding','proof_map.json',lambda s:s.replace('b19a4a8dbfaa44b223cc6fdd3d370dde54a45a3f1131025ff625d31ab29c0622','0'*64,1))]
 for name,file,fn in changes:
  with tempfile.TemporaryDirectory(prefix='E-bib-control-',dir=a.out)as td:
   copy=Path(td)/'copy';shutil.copytree(original,copy,ignore=shutil.ignore_patterns('manifest.json','__pycache__'))
   # Keep inherited manifest evidence: only omit the current top-level manifest.
   shutil.copy2(original/'provenance/original_manifest.json',copy/'provenance/original_manifest.json');shutil.copy2(original/'provenance/independent_manifest.json',copy/'provenance/independent_manifest.json')
   q=copy/file;old=q.read_text();new=fn(old);b.need(new!=old,'mutation actually changes '+name);q.write_text(new);b.ROOT=copy
   try:b.verify()
   except(ValueError,KeyError)as e:rows.append({'control':name,'rejected':True,'reason':str(e)})
   else:raise RuntimeError('accepted '+name)
   finally:b.ROOT=original
 b.dump(a.out/'controls.json',{'status':'PASS','controls':rows,'count':len(rows),'no_finite_or_formal_replay':True});print('PASS',len(rows))
if __name__=='__main__':main()
