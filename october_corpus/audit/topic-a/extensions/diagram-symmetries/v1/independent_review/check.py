#!/usr/bin/env python3
"""Bounded independent L128 review replay. No primary is copied to output.
The written review is evidence of human proof reading, not machine-checked by
these integrity and finite-interface controls. The full Lean replay is retained
from the independently executed identical v1 source.
"""
from pathlib import Path,PurePosixPath
import argparse,copy,difflib,hashlib,importlib.util,json,re,shutil,subprocess,time
HERE=Path(__file__).resolve().parent
PIN='1711f58b9e3343ee52958d52b6dd81690dcca0112c61ceb7cf40b06d4c0958d2'
OLD='56d747fa2d7cc24b0e55148104db8fab411c0419d696922f9f11cf4d9816d540'
NAMES=['instGroupExtension','vertexProjection','edgeForm','supported','support_intersection','power_gap']
def need(p,m):
 if not p:raise ValueError('L128_REVIEW_REJECT '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def safe(root,name):
 p=PurePosixPath(name);need(bool(p.parts) and not p.is_absolute() and '..' not in p.parts and not any(ord(c)<32 for c in name),'safe binding path')
 q=root.joinpath(*p.parts);need(not any(t.is_symlink() for t in [q,*q.parents] if t!=root.parent),'no symlink binding')
 need(q.resolve().is_relative_to(root.resolve()),'binding containment');return q
def verify(root,rows):
 paths=[]
 for r in rows:
  p=safe(root,r['path']);b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'binding '+r['path']);paths.append(r['path'])
 need(len(paths)==len(set(paths)),'distinct bindings')
def semantic(contract,ledger,scope):
 need(contract['source_id']=='L128' and contract['authors']==['Dimitri Leemans','Pablo Spiga','Philippe Tranchida'],'source identity')
 need(contract['current_original_credit']==contract['new_question_answers']==0 and contract['comparison_factor'] is None,'no self-admission')
 need(contract['required_programs']==['minimal_rank_three.g'] and contract['validation_programs']==[],'required finite premise')
 need(len(contract['common_manuscripts'])==1 and len(contract['common_manuscripts'][0]['files'])==14 and contract['common_manuscripts'][0]['scope']=='whole common paper, charged once within Topic A','whole common input')
 need(contract['common_manuscripts'][0]['used_results']==['UA.SK.Helly','UA.Geometry'],'actual common interface')
 need(contract['source_qualifications'][0]=='Closing proper-quotient assertion requires preservation of the complete all-four diagram; Boolean marked quotient is a hypertope with an empty diagram.','quotient qualification')
 need([r['id'] for r in ledger['rows']]==['L128.%02d'%i for i in range(1,15)],'all fourteen rows')
 need(ledger['rows'][12]['status']=='recovered_with_same_diagram_qualification','corrected source row')
 need(len(ledger['proof_spans'])==7 and all(set(r['new_spans'])<=set(ledger['proof_spans']) for r in ledger['rows']),'all spans')
 need(scope['names']==NAMES and len(scope['not_formalized'])==6 and 'generation of supported subgroups by the markers' in scope['not_formalized'] and 'SmallGroups enumeration' in scope['not_formalized'],'formal boundary')
 need(scope['axioms_allowed']==['propext','Classical.choice','Quot.sound'],'standard axioms')
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',default='gap');p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);out=a.out.resolve();start=time.monotonic()
 A=a.author.resolve();need(sha((A/'manifest.json').read_bytes())==PIN,'author pin');m=load(A/'manifest.json');verify(A,m['exports']);need(len(m['exports'])==27,'author export count')
 need(sha((A/'previous_manifest.json').read_bytes())==OLD and m['previous_manifest_sha256']==OLD,'preserved v1')
 prior=load(A/'previous_manifest.json');oldrows={x['path']:x for x in prior['exports']};newrows={x['path']:x for x in m['exports']}
 binding=load(HERE/'bindings.json')
 for n in binding['unchanged_executed_files']:need(oldrows[n]==newrows[n],'unchanged executed '+n)
 contract=load(A/'contract.json');ledger=load(A/'source_clause_map.json');scope=load(A/'formal_scope.json');semantic(contract,ledger,scope)
 common=contract['common_manuscripts'][0]['files'];verify(a.public_root,common)
 if a.study_root:verify(a.study_root,[contract['source_binding'],contract['source_text_binding']])
 for row in ledger['proof_spans'].values():
  text=b''.join((A/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']]);need(len(text)==row['bytes'] and sha(text)==row['sha256'],'complete proof span')
 tex=(A/'graph_symmetries.tex').read_text();need('under the stabilizer $G_y$ of $y$' in tex and 'in the action kernel fixes a full original chamber' in tex and 'regular under its chamber stabilizer' not in tex,'corrected residue group')
 oldphrase='to the residue at $y$. This residue is regular under its chamber stabilizer,\na subgroup of the original two-group. Every type size in the whole regular\n'
 newphrase='to the residue at $y$. This residue is regular under the stabilizer $G_y$ of $y$ in the original\nchamber group. Indeed, $G_y$ is transitive on its chambers, and an element\nin the action kernel fixes a full original chamber and is therefore trivial.\nThus its chamber group is a subgroup of the original two-group. Every type size in the whole regular\n'
 need(tex.count(newphrase)==1 and sha(tex.replace(newphrase,oldphrase).encode())==oldrows['graph_symmetries.tex']['sha256'],'only accepted proof delta')
 formal=(A/'GraphCentralExtension.lean').read_text();need(not re.search(r'\b(?:sorry|admit|native_decide)\b|^\s*axiom\s',formal,re.M),'no holes')
 fresh=load(HERE/'fresh_author_replay/report.json');need(fresh['status']=='PASS' and fresh['source_clauses']==14 and fresh['proof_spans']==7 and [r[0] for r in fresh['formal_axiom_reports']]==NAMES,'fresh inherited exact-source replay')
 for n,s in fresh['formal_axiom_reports']:need(set(x.strip() for x in s.split(','))<=set(scope['axioms_allowed']),'reported axiom boundary')
 for run in fresh['executions']:
  for stream in ['stdout','stderr']:
   q=HERE/'fresh_author_replay'/(run['label']+'.'+stream)
   need(q.is_file() and sha(q.read_bytes())==run[stream+'_sha256'],'fresh exact stream '+q.name)
 controls=[]
 def reject(label,c,l,s):
  try:semantic(c,l,s)
  except ValueError:controls.append(label);return
  raise ValueError('control survived '+label)
 c=copy.deepcopy(contract);c['required_programs']=[];reject('omit finite premise',c,ledger,scope)
 c=copy.deepcopy(contract);c['common_manuscripts'][0]['files'].pop();reject('prune common paper',c,ledger,scope)
 c=copy.deepcopy(contract);c['source_qualifications'][0]='Every proper quotient fails.';reject('erase diagram qualification',c,ledger,scope)
 c=copy.deepcopy(contract);c['current_original_credit']=1;reject('assign source credit',c,ledger,scope)
 l=copy.deepcopy(ledger);l['rows'].pop();reject('omit source row',contract,l,scope)
 l=copy.deepcopy(ledger);l['rows'][12]['status']='fully_recovered';reject('erase corrected row status',contract,l,scope)
 s=copy.deepcopy(scope);s['not_formalized'].remove('generation of supported subgroups by the markers');reject('claim formal generation',contract,ledger,s)
 s=copy.deepcopy(scope);s['names'].append('full_hypertope');reject('inflate formal count',contract,ledger,s)
 spec=importlib.util.spec_from_file_location('independent_coordinates',HERE/'coordinate_models.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);models=module.run();need(models['models_checked']==13 and len(models['controls_rejected'])==1,'coordinate model controls');dump(out/'coordinate_report.json',models)
 def gap(label,code,positive):
  path=out/(label+'.g');path.write_text(code);r=subprocess.run([a.gap,'-q','-T',str(path)],capture_output=True,text=True,timeout=120)
  (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
  if positive:need(r.returncode==0 and 'L128_INDEPENDENT_ORBIT_SEARCH_PASS' in r.stdout and not re.search('Error|warning',r.stdout+r.stderr,re.I),'independent GAP complete')
  else:need('L128_INDEPENDENT_ORBIT_SEARCH_PASS' not in r.stdout and 'Error' in r.stdout+r.stderr,'GAP altered orbit count rejected')
  return r
 r=gap('independent_orbits',(HERE/'independent_search.g').read_text(),True)
 import ast
 raw=r.stdout.split('L128_INDEPENDENT_ORBITS ',1)[1].split('L128_INDEPENDENT_ORBIT_SEARCH_PASS',1)[0].strip();rows=ast.literal_eval(raw)
 need(rows==[[40,14,0,0,[],0],[48,52,52,528,[16],0],[56,13,0,0,[],0]],'independent orbit interpretation')
 gap('wrong_orbit_total',(HERE/'independent_search.g').read_text().replace('[0,528,0]','[0,527,0]'),False);controls.append('alter orbit total');controls.append('erase bilinear term')
 render={}
 if a.render:
  from pypdf import PdfReader
  for name,extras in [('graph_symmetries',[]),('programs',['minimal_rank_three.g'])]:
   d=out/name;d.mkdir()
   for f in [name+'.tex',*extras]:shutil.copyfile(A/f,d/f)
   for k in range(2):
    rr=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=d,capture_output=True,text=True,timeout=60);need(rr.returncode==0,'render '+name)
   log=(d/(name+'.log')).read_text();need(not re.search('Overfull|Missing character|Missing glyph|LaTeX Warning|Package .* Warning',log),'render diagnostics')
   pages=[p.extract_text() or '' for p in PdfReader(d/(name+'.pdf')).pages];expected=[p.extract_text() or '' for p in PdfReader(A/(name+'.pdf')).pages];need(pages==expected,'current exact page text');render[name]={'pages':len(pages),'page_text_sha256':sha('\n'.join(pages).encode()),'equal_current':True}
 if (HERE/'manifest.json').exists():verify(HERE,load(HERE/'manifest.json')['exports'])
 report={'status':'PASS','author_manifest_sha256':PIN,'author_exports':len(m['exports']),'common_files':len(common),'source_checked':bool(a.study_root),'source_rows':14,'proof_spans':7,'fresh_formal_reports':6,'formal_replay_scope':'Reuses independently compiled v1 exact source, dependency pins and controls, verified unchanged in v2. No full geometry formalization.','independent_gap_rows':rows,'coordinate_models':13,'controls_rejected':controls,'prior_full_replay_controls':fresh['controls_rejected'],'render':render,'scientific_credit_assigned':0,'question_credit_assigned':0,'ratio':None,'seconds':round(time.monotonic()-start,4)};dump(out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
