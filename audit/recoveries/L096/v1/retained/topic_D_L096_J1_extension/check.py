#!/usr/bin/env python3
import argparse,copy,hashlib,importlib.util,json,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE_PIN='957d80c66b71be187bf1fc162fbac1cf402a95e98de93097979456ea125fc58b'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(t,m):
 if not t:raise ValueError(m)
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--shadows',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args();o=a.out;need(not o.exists(),'fresh output');o.mkdir(parents=True)
 base=a.study_root/'topic_D_L096_extended_candidate';need(sha(base/'manifest.json')==BASE_PIN,'retained generic freeze')
 if (ROOT/'manifest.json').exists():
  for e in json.loads((ROOT/'manifest.json').read_text())['exports']:need(sha(ROOT/e['path'])==e['sha256'] and (ROOT/e['path']).stat().st_size==e['bytes'],'frozen export '+e['path'])
 for e in json.loads((ROOT/'bindings.json').read_text())['inputs']:
  f=a.study_root/e['path'];need(sha(f)==e['sha256'] and f.stat().st_size==e['bytes'],'retained binding '+e['path'])
 for f in ['shadow_residues.g','prepare_archive.py']:need((ROOT/f).read_bytes()==(base/f).read_bytes(),'unchanged accepted '+f)
 generic=module(base/'check.py','generic_quantifiers');rows=json.loads((ROOT/'results.json').read_text())['rows'];inputs=json.loads((ROOT/'data/selected_inputs.json').read_text())
 coverage=generic.validate_rows(rows,inputs);receipt=generic.parse_log(ROOT/'receipts/shadows_stdout.log','RESULT|');need(generic.signature(receipt)==generic.signature(rows),'actual retained computations')
 for e in json.loads((ROOT/'receipts/shadows_executed_bindings.json').read_text()):need(sha(ROOT/e['path'])==e['sha256'],'actually executed input')
 p=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'prepare_archive.py'),'--archive',str(a.study_root/'sources/L096_supplementary_archive.tar'),'--out',str(o/'data'),'--members','j1.rk3','j1.rk4'],capture_output=True,text=True,timeout=30);need(p.returncode==0,p.stderr)
 for f in ['selected_inputs.json','inputs.g','archive_inventory.json']:need((o/'data'/f).read_bytes()==(ROOT/'data'/f).read_bytes(),'literal active inputs')
 need([r['source_filter_pass'] for r in rows]==[True]*3,'all actual source filters')
 need([(r['IP'],r['WIP']) for r in rows]==[(False,False),(True,True),(False,False)],'full table')
 controls=[]
 def reject(name,fn):
  d=copy.deepcopy(rows);fn(d)
  try:generic.validate_rows(d,inputs)
  except (ValueError,KeyError,IndexError,TypeError):controls.append(name);return
  raise ValueError('accepted '+name)
 reject('drop_archive_row',lambda d:d.pop());reject('assume_historical_label',lambda d:d[0].update(published_label_verified=True));reject('omit_proper_residue',lambda d:d[1]['residues'].pop());reject('weaken_actual_FT',lambda d:d[1]['residues'][0].update(flag_transitive=False));reject('wrong_residue_multiplicity',lambda d:d[0]['residues'][0].update(flag_orbit_size=2));reject('confuse_global_and_residual_weak',lambda d:d[2].update(WIP=True))
 for f in ['shadow_residues.g','run.g','match_prior.g']:shutil.copyfile(ROOT/f,o/f)
 shutil.copyfile(a.study_root/'phase6_sporadic_J1_representatives.g',o/'prior_representatives.g')
 execution=[]
 for f,limit,marker in [('match_prior.g',120,'PASS_J1_PRIOR_MATCH')]+([('run.g',180,'PASS_J1_RESIDUES')] if a.shadows else []):
  t=time.monotonic();r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',f],cwd=o,capture_output=True,text=True,timeout=limit);(o/(f+'.stdout.log')).write_text(r.stdout);(o/(f+'.stderr.log')).write_text(r.stderr);need(r.returncode==0 and not r.stderr and marker in r.stdout and 'Error,' not in r.stdout,'clean '+f);execution.append({'script':f,'seconds':time.monotonic()-t})
 if a.shadows:need(generic.signature(generic.parse_log(o/'run.g.stdout.log','RESULT|'))==generic.signature(rows),'fresh exact mathematical decisions')
 raw=(o/'match_prior.g.stdout.log').read_text();need('COMPLETE_PRIOR_CLASSES|[ 27, 31, 32 ]|[ 27, 31, 32 ]' in raw,'exact previous census coverage')
 if a.render:
  from pypdf import PdfReader
  shutil.copyfile(ROOT/'janko_residues.tex',o/'janko_residues.tex')
  for i in [1,2]:
   r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','janko_residues.tex'],cwd=o,capture_output=True,text=True,timeout=30);(o/f'render{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'render')
  need(not any(s in r.stdout for s in ['Overfull','undefined','Missing character']),'render diagnostics')
  need([p.extract_text() for p in PdfReader(o/'janko_residues.pdf').pages]==[p.extract_text() for p in PdfReader(ROOT/'janko_residues.pdf').pages],'exact page text')
 report={'status':'PASS','scope':'Three literal J1 inputs, all source action filters and every rank>=2 residue; historical labels unverified.','coverage':coverage,'rank_ge_two_base_residues':sum(x['residue_rank']>=2 for r in rows for x in r['residues']),'prior_census_matches':[27,31,32],'controls':controls,'fresh_execution':execution,'fresh_all_shadows':a.shadows,'prior_complete_census_rerun':False,'full_source_credit':0};(o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
