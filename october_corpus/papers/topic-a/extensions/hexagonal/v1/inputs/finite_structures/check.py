#!/usr/bin/env python3
"""Bounded structural replay and exact predecessor-image conservation."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent
from shape_search import SHAPES

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError(m)
def validate(scope,rows):
 need(len(rows)==35 and len({r['id'] for r in rows})==35 and {r['id'] for r in rows}==set(SHAPES),'exact 35 distinct finite structures')
 need(scope['literal_source_shapes_verified']==34 and scope['corrected_row']=='T4.8','honest 34 plus correction')
 need(scope['T4.8_printed_split_claim']=='false_no_A5_subgroup','literal split claim not restored')
 need(scope['whole_original_credit']==scope['new_question_credit']==scope['new_Lean_credit']==0,'bounded new work')
 need(scope['seven_shared_rows']=='separate packet, not proved here','separate authorship')
 need(all(r['shape']==SHAPES[r['id']] for r in rows),'exact fully bracketed statements')
 need(all(r['status']==('corrected_nonsplit_shape' if r['id']=='T4.8' else 'printed_shape_under_explicit_brackets') for r in rows),'row correction boundary')
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--programs',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 if (HERE/'manifest.json').exists():
  for z in load(HERE/'manifest.json')['exports']:
   q=HERE/z['path'];need(q.stat().st_size==z['bytes'] and sha(q)==z['sha256'],'frozen '+z['path'])
 b=load(HERE/'bindings.json')
 for z in b['accepted_full_receipts']:
  q=HERE/z['path'];need(q.stat().st_size==z['bytes'] and sha(q)==z['sha256'],'whole accepted image receipt '+z['path'])
 scope=load(HERE/'scope.json');rows=load(HERE/'results.json')['rows'];validate(scope,rows);controls=[]
 for label,field,val in [('restore false split claim','T4.8_printed_split_claim','true'),('inflate original credit','whole_original_credit',1),('claim other author rows','seven_shared_rows','proved here')]:
  bad=copy.deepcopy(scope);bad[field]=val
  try:validate(bad,rows)
  except ValueError:controls.append(label)
  else:raise ValueError('accepted metadata corruption '+label)
 try:validate(scope,rows[:-1])
 except ValueError:controls.append('drop finite row')
 else:raise ValueError('accepted dropped row')
 for r in rows:
  q=HERE/'certificates'/(r['id']+'.log');need(sha(q)==r['witness_sha256'] and 'PASS_SHAPE '+r['id'] in q.read_text(),'complete positive witness '+r['id'])
 need('PASS_NO_A5_SUBGROUP' in (HERE/'obstruction_certificate.log').read_text(),'actual obstruction receipt')
 if a.programs:
  subprocess.run([sys.executable,'-B','-O',str(HERE/'shape_search.py'),'--out',str(a.out/'structures'),'--timeout','60'],check=True,timeout=2100)
  fresh=load(a.out/'structures/report.json');need(len(fresh)==35 and all(r['passed'] for r in fresh),'all fresh structural witnesses')
  subprocess.run([sys.executable,'-B','-O',str(HERE/'obstruction.py'),'--out',str(a.out/'obstruction')],check=True,timeout=50)
  q=a.out/'controls_input.g';q.write_text('Read('+json.dumps(str(HERE/'shape_engine.g'))+');;Read('+json.dumps(str(HERE/'controls.g'))+');;\n')
  with (a.out/'controls.stdout').open('w') as out:r=subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(q)],stdout=out,stderr=subprocess.STDOUT,timeout=20)
  text=(a.out/'controls.stdout').read_text();need(r.returncode==0 and 'PASS_NINE_STRUCTURAL_CONTROLS' in text,'nine actual group controls')
 rendered=[]
 if a.render:
  from pypdf import PdfReader
  d=a.out/'render';d.mkdir();shutil.copyfile(HERE/'structural_completion.tex',d/'structural_completion.tex')
  for turn in [1,2]:
   with (d/f'pass{turn}.stdout').open('w') as o:r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','structural_completion.tex'],cwd=d,stdout=o,stderr=subprocess.STDOUT,timeout=30)
   need(r.returncode==0,'TeX pass')
  log=(d/'structural_completion.log').read_text();need(not any(z in log for z in ['Overfull','Underfull','LaTeX Warning','Missing character']),'clean rendered paper')
  texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
  need(texts(d/'structural_completion.pdf')==texts(HERE/'structural_completion.pdf'),'exact rendered pages');rendered=[len(texts(d/'structural_completion.pdf'))]
 report={'status':'PASS_AUTHOR_STRUCTURAL_COMPLETION','finite_rows':35,'printed_shapes':34,'corrected_shapes':1,'exact_predecessor_receipts':35,'full_programs_replayed':a.programs,'new_structural_group_controls':9 if a.programs else 'retained receipt','metadata_controls':controls,'rendered_pages':rendered,'prior_presentation_geometry_Lean_repeated':False,'whole_original_credit':0,'seconds':round(time.monotonic()-start,6)}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
