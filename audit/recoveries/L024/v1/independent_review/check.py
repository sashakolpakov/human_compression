"""Bounded distinct L024 replay; no author mathematical helper imports."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,subprocess,copy,ast
R=Path(__file__).resolve().parent

def need(t,m):
 if not t:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,e):need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'binding '+str(p))
def check_claims(review,scope,dep):
 need(review['status']=='ACCEPTED_CORRECTED_PRINCIPAL_RECOVERY','verdict boundary')
 need(not review['prior_authorship_in_this_L024_packet'],'distinct role')
 need(review['new_original_credit']==review['new_question_credit']==review['new_Lean']==0 and review['measurement'] is None,'no credit/metrics')
 need(scope['historical_run_not_reproduced'] and not scope['full_original_acceptance'],'historical and registration boundary')
 need(scope['finite_claims']['group_order']==258190571520 and scope['finite_claims']['IP_subset_pairs']==64,'finite record')
 need('no computational IP premise' in scope['finite_claims']['IP_role'],'written IP role')
 need(scope['finite_claims']['negative_FS_degrees']==[60,3660,7320,10980,14580],'FS record')
 need(dep['required_finite_programs']==['verify_schur_example.g'],'whole required file')
 need(dep['permutation_verification']['option']=='DefaultStabChainOptions.random=1000','guaranteed verification')
 need(any('Nuzhin' in x and 'n>=8' in x for x in dep['retained_theorems']),'Nuzhin range')
 need(any('PSU3' in x and 'PSU6' in x for x in dep['retained_theorems']),'small dimension borrowed input')
 need(len(review['limits'])>=6,'explicit limits')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--replay-author',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args();a.author=a.author.resolve();a.out.mkdir(parents=True,exist_ok=False)
 manifest=R/'manifest.json';n=0
 if manifest.exists():
  for e in load(manifest)['exports']:pin(R/e['path'],e);n+=1
 b=load(R/'bindings.json');pin(a.author/'manifest.json',b['author_manifest'])
 for e in b['author_exports']:pin(a.author/e['path'],e)
 if a.study_root:
  for k in ['source','borrowed_classification']:pin(a.study_root/'sources'/Path(b[k]['path']).name,b[k])
 pin(Path(b['table']['path']),b['table']);pin(Path(b['local_official_manual']['path']),b['local_official_manual'])
 review=load(R/'review.json');scope=load(a.author/'scope.json');dep=load(a.author/'dependencies.json');check_claims(review,scope,dep)
 controls=[]
 cases=[('IP validation promoted to premise',lambda x:x[1]['finite_claims'].__setitem__('IP_role','required finite IP premise')),('premature registration',lambda x:x[0].__setitem__('new_original_credit',1)),('new question credit',lambda x:x[0].__setitem__('new_question_credit',1)),('new Lean claim',lambda x:x[0].__setitem__('new_Lean',1)),('ratio inserted',lambda x:x[0].__setitem__('measurement',1)),('review role changed',lambda x:x[0].__setitem__('prior_authorship_in_this_L024_packet',True)),('historical run promoted',lambda x:x[1].__setitem__('historical_run_not_reproduced',False)),('finite group order changed',lambda x:x[1]['finite_claims'].__setitem__('group_order',120)),('indicator omitted',lambda x:x[1]['finite_claims']['negative_FS_degrees'].pop()),('required program omitted',lambda x:x[2].__setitem__('required_finite_programs',[])),('probabilistic-only verification',lambda x:x[2]['permutation_verification'].__setitem__('option','random=900')),('Nuzhin range omitted',lambda x:x[2].__setitem__('retained_theorems',[t for t in x[2]['retained_theorems'] if 'Nuzhin' not in t])),('small dimensions borrowed input omitted',lambda x:x[2].__setitem__('retained_theorems',[t for t in x[2]['retained_theorems'] if 'PSU3' not in t]))]
 for label,mut in cases:
  q=copy.deepcopy([review,scope,dep]);mut(q)
  try:check_claims(*q)
  except ValueError:controls.append(label)
  else:raise ValueError('control accepted '+label)
 run=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(R/'independent_coordinates.py'),'--out',str(a.out/'coordinates.json')],capture_output=True,text=True);need(run.returncode==0,run.stdout+run.stderr);coord=load(a.out/'coordinates.json');need(coord==load(R/'coordinate_report.json'),'independent coordinate reproducibility')
 run=subprocess.run([a.gap,'-q','--quitonbreak',str(R/'independent_character.g')],capture_output=True,text=True);(a.out/'character_stdout.txt').write_text(run.stdout);need(run.returncode==0 and 'Error' not in run.stderr,'independent character run');chars=json.loads(run.stdout);need(chars==load(R/'character_report.json'),'independent table induction')
 tex=(a.author/'schur_characters.tex').read_text();block=tex.split('\\midrule',1)[1].split('\\bottomrule',1)[0];rows=[]
 for match in re.finditer(r'(\d+)\s*&\s*(-?\d+)\s*&\s*(-?\d+)\s*&\s*(-?\d+)\s*&\s*(-?\d+)',block):
  z=list(map(int,match.groups()));rows.extend([z[1:]]*z[0])
 need(len(rows)==24 and Counter(map(tuple,rows))==Counter(map(tuple,chars['low_rows'])),'all displayed low character rows')
 need(762**2>580608 and 9**2>80 and 5*762+4*9==3846 and (4270-3846)>420,'exact column bound')
 saved=(R/'author_replay.txt').read_text();author_mult=ast.literal_eval(saved.split('all_multiplicities=',1)[1].split('gap_version=',1)[0].strip());need(author_mult==chars['multiplicities'],'all150 author/independent multiplicities')
 need('STATUS=PASS' in saved and 'IP_pairs=64' in saved,'whole author replay receipt')
 need(chars['negative_FS']==[[60,8],[3660,376],[7320,752],[10980,1072],[14580,1440]],'five negative indicators/multiplicities')
 for j in range(100):
  dimension=(8*j+5)*(8*j+6)//2;need(dimension==32*j*j+44*j+15 and dimension%4==3,'infinite sequence diagnostic')
 extra={}
 if a.replay_author:
  run=subprocess.run([a.gap,'-q','--quitonbreak','verify_schur_example.g'],cwd=a.author,capture_output=True,text=True);(a.out/'author_stdout.txt').write_text(run.stdout);(a.out/'author_stderr.txt').write_text(run.stderr);need(run.returncode==0 and 'STATUS=PASS' in run.stdout and not run.stderr.strip(),'fresh whole author certificate');need(run.stdout.strip()==saved.strip(),'fresh exact certificate output');extra['author_replay']='PASS'
 if a.render:
  from pypdf import PdfReader
  d=a.out/'render';d.mkdir()
  for i in range(2):
   run=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(d),'schur_characters.tex'],cwd=a.author,capture_output=True,text=True);(d/f'pass{i+1}.txt').write_text(run.stdout+run.stderr);need(run.returncode==0,'TeX render')
  log=(d/'schur_characters.log').read_text();need(all(k not in log for k in ['Overfull','undefined','Missing character']),'clean TeX')
  pp=lambda p:[x.extract_text() for x in PdfReader(p).pages]
  need(pp(d/'schur_characters.pdf')==pp(a.author/'schur_characters.pdf'),'five exact page texts');extra['render_pages']=len(pp(d/'schur_characters.pdf'))
 report={'status':'PASS','review_exports':n,'author_exports':len(b['author_exports']),'author_manifest':b['author_manifest']['sha256'],'independent_coordinate_checks':coord,'independent_multiplicities':150,'displayed_character_rows':24,'negative_FS':chars['negative_FS'],'scope_controls':controls,'source_science_no_new_credit':True,**extra};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
