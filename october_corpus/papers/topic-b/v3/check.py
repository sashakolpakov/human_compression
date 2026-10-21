#!/usr/bin/env python3
"""Integrity, exact contract transfer and optional isolated rendering of unified B.
No inherited classification computation or Lean proof is altered or reproved here.
"""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess
from itertools import permutations
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','inductively-minimal-geometries','maximal-symmetric-markings','frattini-coordinate-geometries','disjoint-subset-geometries','high-rank-symmetric-markings','program-appendix']
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(r,base):
 p=base/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'binding '+r['path'])
def validate(s,study,public):
 need(s['original_sources']==['N001','N003','N008','L030','L040'] and s['original_count']==5,'five unchanged originals')
 for r in s['inherited_inputs']:binding(r,study if r['root']=='study' else public)
 for r in s['primary_editions']:binding(r,study)
 for r in s['prior_scientific_replays']:binding(r,public)
 old=json.loads((public/'papers/topic-b/v2/mapping_correction/source_contract_map.json').read_text())
 new=json.loads((study/'corpus161_L040_recovery/scope.json').read_text())
 need(len(s['source_rows'])==s['source_row_count']==65,'all 30+35 rows')
 for current,prior in zip(s['source_rows'][:30],old['rows']):
  need(current['inherited_record']==prior,'exact old source row')
  need(current['unchanged_disposition']==prior['verdict'] and current['target']==prior['source_contract'],'old contract unchanged')
 for current,prior in zip(s['source_rows'][30:],new['contracts']):
  need(current['inherited_record']==prior,'exact L040 source row')
  need(current['unchanged_disposition']==prior['status'] and current['target']==prior['target'],'L040 qualification unchanged')
 for id,r in s['proof_contexts'].items():
  t=(ROOT/r['path']).read_text();a=r['start_codepoint'];b=r['end_codepoint_exclusive']
  need(0<=a<b<=len(t) and hashlib.sha256(t[a:b].encode()).hexdigest()==r['sha256_utf8'],'complete proof context '+id)
 for row in s['source_rows']:
  need(row['current_proof_nodes'],'actual current route')
  need(all(n in s['proof_contexts'] for n in row['current_proof_nodes']+row['current_shared_interfaces']),'all current locators present')
 target=next(r for r in s['source_rows'] if r['source_reference']=='L040.T1.1')
 need(set(['A.Maximum','UB.Extremal','UB.Sign','UB.F','UB.Coset'])<=set(target['current_proof_nodes']),'actual shared rank n-1 route')
 need([r['role'] for r in s['programs']]==[r['role'] for r in new['program_inventory']],'four exact program roles')
 for r,p in zip(s['programs'],new['program_inventory']):
  binding(r,ROOT);need(r['sha256']==p['sha256'] and r['bytes']==p['bytes'],'whole old mathematical program')
 for name in s['unchanged_applications']:
  need((ROOT/name).read_bytes()==(study/'topic_B_volume'/name).read_bytes(),'unchanged application '+name)
 for row in s['formal_evidence']:
  oldpath=study/('topic_B_volume/formal/ResidualGeneration.lean' if row['declarations']==6 else 'corpus161_L040_recovery/formal/IrredundantNormalization.lean')
  need((ROOT/row['module']).read_bytes()==oldpath.read_bytes(),'unchanged actual formal source')
 need(sum(r['declarations'] for r in s['formal_evidence'])==s['reused_partial_declarations']==14,'exact partial formal count')
 need(s['new_formal_declarations']==s['new_source_credit']==s['new_question_credit']==0,'no extra credit')
 need(s['compression_factor'] is None and not s['complete_formalization_claim'] and not s['unpriced_application_imports'],'no unreviewed price or formal claim')
 for key in ['whole_common_charged_once','all_five_complete_applications','all_four_complete_programs_visible']:need(s['boundaries'][key],'complete topic boundary')
 for key in ['retained_external_proof_cost','source_graphics_cost','historical_software_cost','full_formalization_cost']:need(s['boundaries'][key] is None,'unknown not zero')
 for r in s['documents']:binding(r,ROOT)
 return True

def code_inclusion():
 names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{(programs/[^}]+)\}',(ROOT/'program-appendix.tex').read_text())
 need(len(names)==4,'four whole printed programs')
 chunks=[]
 for p in PdfReader(ROOT/'program-appendix.pdf').pages:
  def visitor(t,cm,tm,font,size):
   if font and 'Menlo' in str(font.get('/BaseFont','')):chunks.append(t)
  p.extract_text(visitor_text=visitor)
 norm=lambda t:''.join(c for c in t if not c.isspace())
 need(norm(''.join(chunks))==norm(''.join((ROOT/n).read_text() for n in names)),'literal complete code appendix')
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 s=json.loads((ROOT/'scope.json').read_text());validate(s,a.study_root,a.public_root)
 controls=[]
 mutations=[('drop source clause',lambda t:t['source_rows'].pop()),('admit false branching clause',lambda t:next(r for r in t['source_rows'] if r['source_reference']=='L040.C6.5.2').update(unchanged_disposition='recovered_complete')),('omit common extremal premise',lambda t:next(r for r in t['source_rows'] if r['source_reference']=='L040.T1.1')['current_proof_nodes'].remove('UB.Extremal')),('alter proof context',lambda t:t['proof_contexts']['UB.Laminar'].update(sha256_utf8='0'*64)),('demote required program',lambda t:t['programs'][0].update(role='finite_validation')),('claim full Lean coverage',lambda t:t.update(complete_formalization_claim=True)),('invent factor',lambda t:t.update(compression_factor=2)),('unknown classical proofs as zero',lambda t:t['boundaries'].update(retained_external_proof_cost=0))]
 for name,edit in mutations:
  t=copy.deepcopy(s);edit(t)
  try:validate(t,a.study_root,a.public_root)
  except ValueError:controls.append(name)
  else:raise ValueError('control accepted '+name)
 # The three concrete counterexamples protect the new interface's hypotheses.
 A=[{0,1},{0,2},{0,3}];X=[{0,1},{0,2},{1,2}]
 need(all(len(A[i]&A[j])==len(X[i]&X[j]) for i in range(3) for j in range(i)) and set.intersection(*A) and not set.intersection(*X),'nonlaminar pairwise data insufficient')
 need(not any(p[0]==2 and p[1]==2 for p in permutations(range(3))),'root image overlapping a target prevents extension')
 need(2*4-4<2*4-2 and 4+1<2*4-2,'binary endpoint m=4')
 need(any({p[0],p[1]}=={2,3} and set(p)==set(range(4)) for p in permutations(range(4))),'vacuous selected full set and empty root')
 renders=[]
 if a.render:
  stage=a.out/'render';stage.mkdir();shutil.copytree(ROOT/'sections',stage/'sections');shutil.copytree(ROOT/'programs',stage/'programs')
  for n in ['preamble']+DOCS:shutil.copyfile(ROOT/(n+'.tex'),stage/(n+'.tex'))
  for n in DOCS:
   for i in range(2):
    p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',n+'.tex'],cwd=stage,capture_output=True,text=True)
    (stage/(n+f'.run{i}.txt')).write_text(p.stdout+p.stderr);need(p.returncode==0,'render '+n)
   log=(stage/(n+'.log')).read_text();need(not re.search('Overfull|Missing character|LaTeX Warning|Package .* Warning',log),'clean final render '+n)
   current=[x.extract_text()or'' for x in PdfReader(stage/(n+'.pdf')).pages];bound=[x.extract_text()or'' for x in PdfReader(ROOT/(n+'.pdf')).pages]
   need(current==bound,'all exact rendered page texts '+n);renders.append(dict(document=n,pages=len(current)))
 if (ROOT/'manifest.json').exists():
  for r in json.loads((ROOT/'manifest.json').read_text())['exports']:binding(r,ROOT)
 r=dict(status='PASS',originals=5,unchanged_source_rows=65,proof_contexts=len(s['proof_contexts']),complete_programs=code_inclusion(),reused_partial_Lean_declarations=14,new_Lean_declarations=0,controls=controls,small_hypothesis_checks=4,rendered=renders,finite_programs_and_formal_sources_unchanged=True,full_uniform_proofs_verified_by_this_program=False)
 (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
