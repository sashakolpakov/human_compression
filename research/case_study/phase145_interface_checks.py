#!/usr/bin/env python3
"""Independent isolated public-layout and refusal checks for frozen U3/A2.
No source PDFs, primary-source full texts, saved census outputs or private
rasters are copied. Exact mathematical predecessor inputs are copied. The author verifier is exercised, not trusted as a math review.
"""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
MANIFEST='3bca6b7691eb7683d4ab8a10521abc916ba280a5bb41f82d9144e26dd068f544'
ERRATA={'phase138_detailed_locator_erratum.md':'8717af197517e013c37270f22e42b9f6facd847b0762b37a31479f54ddcb627d','phase138_detailed_locator_erratum.json':'95a6caae6d4227a5974dc99526b1c6b000f9b86590debdaad23f7a890521041e'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study-root',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();root=a.study_root
 if a.output.exists() or a.output.is_symlink():raise SystemExit('Refusing existing output')
 mp=root/'phase138_manifest.json';require(digest(mp)==MANIFEST,'wrong author freeze');m=json.loads(mp.read_text())
 bindings={x['path']:x['sha256'] for x in m['files']+m['required_shared_inputs']}
 bindings.update({'phase138_manifest.json':MANIFEST,**ERRATA})
 for n,h in bindings.items():require(digest(root/n)==h,'wrong input '+n)
 ledger=json.loads((root/'phase138_module_A_v2_ledger.json').read_text());err=json.loads((root/'phase138_detailed_locator_erratum.json').read_text())
 require(digest(root/err['bound_ledger']['path'])==err['bound_ledger']['sha256'],'erratum bound to wrong ledger')
 for x in err['replacements']:
  rows=[r for r in ledger['detailed_multiclauses'] if r.get('id')==x['id']]
  require(len(rows)==1 and rows[0]['proof']==x['old_proof'],'locator old value not exact')
 checks=[]
 with tempfile.TemporaryDirectory(prefix='phase145-isolated-') as tmp:
  tree=Path(tmp);public=tree/'math_compression/research/case_study';public.mkdir(parents=True)
  for n in bindings:
   p=public/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/n,p)
  require(not (public/'sources').exists(),'private sources copied')
  def run(out,*flags):return subprocess.run([sys.executable,'-B','-O',str(public/'phase138_verify.py'),'--output',str(out),*flags],capture_output=True,text=True)
  r=run(tree/'portable.json','--rebuild');require(r.returncode==0,r.stderr)
  portable=json.loads((tree/'portable.json').read_text())
  require(portable['private_primary_files_checked']==0 and portable['exact_builder_and_checkpoint_replay'],'portable scope')
  mutations=['phase138_umbrella_v3.md','phase138_module_A_v2.md','phase138_module_A_v2_ledger.json','phase138_umbrella_v3_contracts.json','phase130_geometry_erratum.md','phase138_N009_decomposition_erratum.md','phase78_n009_integration_census.g','phase78_n009_integration_finite.g','phase78_n009_integration_data.g','phase78_n009_integration_run.py']
  for i,n in enumerate(mutations):
   p=public/n;old=p.read_bytes();p.write_bytes(old+b'\nindependent mutation control\n');out=tree/f'bad-{i}.json';r=run(out)
   require(r.returncode!=0 and not out.exists(),'mutation accepted '+n);p.write_bytes(old)
   checks.append({'case':'mutated_bound_input','path':n,'status':'PASS_rejected_before_output','error_tail':r.stderr.strip().splitlines()[-1:]})
  occupied=tree/'occupied.json';occupied.write_text('sentinel file\n');directory=tree/'directory';directory.mkdir();(directory/'keep').write_text('sentinel directory\n');target=tree/'target';target.write_text('sentinel target\n');link=tree/'link';link.symlink_to(target);dangling=tree/'dangling';dangling.symlink_to(tree/'missing')
  for label,p in [('regular',occupied),('directory',directory),('symlink',link),('dangling_symlink',dangling)]:
   r=run(p);require(r.returncode!=0 and 'Refusing existing output' in r.stderr,'occupied output accepted '+label)
   checks.append({'case':'no_clobber_'+label,'status':'PASS'})
  require(occupied.read_text()=='sentinel file\n' and target.read_text()=='sentinel target\n' and (directory/'keep').read_text()=='sentinel directory\n','sentinel changed')
  require(link.readlink()==target and dangling.readlink()==tree/'missing','symlink overwritten')
  for name in ['phase138_build.py','phase138_checkpoint.py','phase138_render.py']:
   argv=[sys.executable,'-B','-O',str(public/name),'--output-dir',str(directory)]
   if name.endswith('render.py'):argv+=['--module','A']
   r=subprocess.run(argv,capture_output=True,text=True);require(r.returncode!=0 and 'Refusing existing output' in r.stderr,'generator overwrite '+name)
   checks.append({'case':'generator_no_clobber','path':name,'status':'PASS'})
  for n,h in bindings.items():require(digest(public/n)==h and digest(root/n)==h,'bound input changed '+n)
 report={'script_sha256':digest(Path(__file__)),'status':'PASS_independent_interfaces_not_mathematical_proof','manifest_sha256':MANIFEST,'copied_file_count':len(bindings),'bindings':[{'path':n,'sha256':h} for n,h in sorted(bindings.items())],'private_sources_or_rasters_copied':False,'portable_replay':portable,'exact_locator_replacements_checked':len(err['replacements']),'controls':checks,'original_and_isolated_inputs_unchanged':True,'fresh_GAP_or_Lean_replay':False}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps({'status':report['status'],'copied_files':len(bindings),'controls':len(checks)}))
if __name__=='__main__':main()
