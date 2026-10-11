#!/usr/bin/env python3
"""Replay complete proof migration, data boundaries and current TeX; no census rerun."""
from pathlib import Path
import argparse,copy,hashlib,json,re,subprocess,shutil,unicodedata
from pypdf import PdfReader
H=Path(__file__).resolve().parent
PAT=re.compile(r'\\begin\{(lemma|theorem|proposition|proof)\}.*?\\end\{\1\}',re.S)
def need(x,m):
 if not x:raise ValueError('LOCALLY_PROJECTIVE_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def pin(base,r):
 p=Path(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative pin');b=(base/p).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'exact whole artifact '+r['path']);return b
def env(path,index):return list(PAT.finditer(path.read_text()))[index][0]
def manifests(h):
 found=[]
 for path in sorted((h/'accepted').rglob('manifest.json')):
  m=load(path)
  for r in m['exports']:pin(path.parent,r)
  found.append(dict(path=str(path.relative_to(h)),sha256=sha(path.read_bytes()),exports=len(m['exports'])))
 return found
def validate_scope(s,sw):
 need(s['originals']==['L084','L095'] and s['source_record_count']==52,'two distinct originals and all records')
 need(s['current_common_bundle']==['common.tex','complete-census.tex'] and s['tables_part_of_whole_common'],'whole common plus complete tables')
 need(s['current_applications']=={'L084':['erratum.tex'],'L095':['universal-polytope.tex']} and s['application_to_application_proof_edges']==[],'no free application cross-dependency')
 need(s['particular_target_universal_group_is_not_retained'] and s['historical_unavailable_g_txt_not_used'],'target group proved and no missing g.txt premise')
 need(s['formal_declarations']==0 and s['no_new_question_credit'] and s['no_new_formal_credit'] and s['no_ratio_calculated'],'exact no-new-credit/formal/cost scope')
 need(len(sw['programs'])==s['required_program_files']==6 and len({x['sha256'] for x in sw['programs']})==6,'six complete unique required files')
 need(all(x['whole_file'] and x['logical_role']=='required_finite_computation' for x in sw['programs']),'all whole programs required')
 need(len(sw['required_comparison_data'])==1 and sw['required_comparison_data'][0]['path']=='source_tables.json','complete historical comparison input')
 need(sw['unknown_classical_proof_cost'] is None and sw['unknown_full_runtime_cost'] is None and sw['formal_declarations']==0,'external costs unknown, no formal claim')
 need(len(sw['operational_drivers'])==2 and len(sw['complete_output_data'])==11,'whole separate drivers and all output evidence')
def source_map(h,m):
 need(len(m['rows'])==52 and m['source_ids']==['L084','L095'] and m['source_count']==2,'full source map')
 for k in ['L084','L095']:
  old=load(h/'accepted'/f'{k}_ledger.json')['rows'];new=[x for x in m['rows'] if x['inherited_ledger']==k]
  need([x['original_record'] for x in new]==old,'unchanged whole original records '+k)
  need(all(not x['disposition_changed'] for x in new),'literal qualifications retained')
 need(m['related_L095_edition_row_inside_L084_ledger_is_not_third_original'],'record/original distinction')
def migration(h,m):
 seen=set();counts={}
 for r in m['rows']:
  a,b=r['old'],r['current'];ot=env(h/a['path'],a['index']);nt=env(h/b['path'],b['index']);need(sha(ot.encode())==a['sha256'] and sha(nt.encode())==b['sha256'],'exact routed environment')
  k=(a['path'],a['index']);need(k not in seen,'old environment routed once');seen.add(k);mode=r['comparison'];counts[mode]=counts.get(mode,0)+1
  if mode=='byte_identical':need(ot==nt,'identical proof')
  elif mode=='one_placement_phrase':need(ot.replace('already printed and checked in the census packet','printed in full in the accompanying common program appendix')==nt,'only explicit placement phrase')
  else:need(mode=='explicit_source_application_restatement' and a['path']=='accepted/L095/universal-locally-projective.tex' and a['index'] in [8,9] and b['path']=='universal-polytope.tex','only final census corollary rewritten')
 expected={(p,i) for p in ['accepted/L095/census/semisparse-quotient-census.tex','accepted/L095/universal-locally-projective.tex'] for i in range(len(list(PAT.finditer((h/p).read_text()))))}
 need(seen==expected and len(seen)==18,'every old theorem/proof environment')
 need(counts=={'byte_identical':15,'one_placement_phrase':1,'explicit_source_application_restatement':2},'complete migration categories')
 need((h/'complete-census.tex').read_bytes()==(h/'accepted/L095/census/corrected-census.tex').read_bytes(),'all complete table TeX unchanged')
 need((h/'complete-census.pdf').read_bytes()==(h/'accepted/L095/census/corrected-census.pdf').read_bytes(),'all complete table PDF unchanged')
 return counts
def textpages(p):return [pg.extract_text() or '' for pg in PdfReader(p).pages]
def replay(h,out,render=False,xelatex='/opt/homebrew/bin/xelatex'):
 out=Path(out);need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True)
 if (h/'manifest.json').exists():
  for r in load(h/'manifest.json')['exports']:pin(h,r)
 old=manifests(h);s=load(h/'scope.json');sw=load(h/'software_boundary.json');validate_scope(s,sw);source_map(h,load(h/'source_map.json'));moves=migration(h,load(h/'migration.json'))
 for r in sw['programs']:
  need(pin(h,r)==(h/r['original']).read_bytes(),'byte-exact full required program')
 for r in sw['required_comparison_data']:
  need(pin(h,r)==(h/r['original']).read_bytes(),'whole comparison data')
 for r in sw['complete_output_data']+sw['operational_drivers']:pin(h,r)
 for x in sw['program_aliases']:
  need(len({sha((h/f).read_bytes()) for f in x})==1,'only byte-identical alias')
 common=(h/'common.tex').read_text();need(re.findall(r'\\input\{([^}]+)\}',common)==[f'sections/{x}.tex' for x in ['01-conjugacy','02-bounds','03-universal','04-geometry','05-census','06-data']],'complete common inputs')
 programtex=(h/'required-programs.tex').read_text();names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',programtex)
 need(set(names)=={x['path'] for x in sw['programs']} and len(names)==6,'all six full code inputs once');need(not re.search('firstline|lastline',programtex),'no pruned program range')
 pack=lambda text:''.join(unicodedata.normalize('NFKC',text).split())
 printed=''.join(re.sub(r'\n'+str(i)+r'\s*$','',t) for i,t in enumerate(textpages(h/'required-programs.pdf'),1))
 for n in names:need(pack((h/n).read_text()) in pack(printed),'full file actually present in appendix '+n)
 bindings=load(h/'current_documents.json');docs=[]
 for d in bindings['documents']:
  for r in d['inputs']:pin(h,r)
  pin(h,d['pdf']);pg=textpages(h/d['pdf']['path']);need(len(pg)==d['pages'],'whole document pages');need([sha(x.encode()) for x in pg]==d['page_text_hashes'],'complete page text');need(not any('\ufffd' in x for x in pg),'no replacement glyph')
  docs.append(dict(id=d['id'],pages=len(pg),pdf_sha256=d['pdf']['sha256']))
 renders=[]
 if render:
  dest=out/'render';dest.mkdir()
  for d in bindings['documents']:
   tex=d['tex'];stem=Path(tex).stem
   for i in [1,2]:
    q=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(dest),tex],cwd=h,capture_output=True);(dest/f'{stem}.pass{i}.txt').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'fresh TeX '+tex)
   bad=[x for x in (dest/(stem+'.log')).read_text(errors='replace').splitlines() if any(t in x for t in ['Overfull','Underfull','Missing character','Font Warning','LaTeX Warning'])];need(not bad,'clean typography '+tex+str(bad));need(textpages(dest/(stem+'.pdf'))==textpages(h/d['pdf']['path']),'complete freshly rendered page text '+tex);renders.append(dict(document=d['id'],pages=d['pages'],diagnostics=bad))
  aux=(dest/'common.aux').read_text()
  for lab,n in s['common_theorem_numbers'].items():need('\\newlabel{'+lab+'}{{'+str(n)+'}' in aux,'all application/common theorem numbers exact')
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):controls.append(name);return
  raise ValueError('accepted corrupt control '+name)
 for name,edit in [('omit full table acquisition',lambda z:z.update(current_common_bundle=['common.tex'])),('retain unproved target universal theorem',lambda z:z.update(particular_target_universal_group_is_not_retained=False)),('free application dependency',lambda z:z.update(application_to_application_proof_edges=[['L095','L084']])),('merge original with erratum',lambda z:z.update(originals=['L095'])),('claim new formal theorem',lambda z:z.update(formal_declarations=1)),('claim ratio',lambda z:z.update(no_ratio_calculated=False)),('missing g.txt premise',lambda z:z.update(historical_unavailable_g_txt_not_used=False))]:
  z=copy.deepcopy(s);edit(z);reject(name,lambda z=z:validate_scope(z,sw))
 for name,edit in [('omit complete marking file',lambda z:z['programs'].pop(0)),('demote required code',lambda z:z['programs'][0].update(logical_role='validation')),('drop historical raw tables',lambda z:z.update(required_comparison_data=[])),('external proof cost zero',lambda z:z.update(unknown_classical_proof_cost=0)),('drop witness output',lambda z:z['complete_output_data'].pop())]:
  z=copy.deepcopy(sw);edit(z);reject(name,lambda z=z:validate_scope(s,z))
 z=load(h/'source_map.json');z['rows'].pop();reject('omit source clause',lambda:source_map(h,z))
 z=load(h/'migration.json');z['rows'].pop();reject('omit old proof environment',lambda:migration(h,z))
 z=load(h/'migration.json');z['rows'][0]['current']['index']=1;reject('misroute old theorem to proof',lambda:migration(h,z))
 report=dict(status='AUTHOR_MIGRATION_SCOPE_RENDER_PASS',accepted_prior_packets=old,source_records=52,originals=2,migrated_environments=moves,complete_required_programs=6,required_comparison_files=1,complete_table_rows_each=137,documents=docs,renders=renders,controls=controls,finite_computation_repeated=False,new_mathematics_claimed=False,ratio=None)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','source_records','originals','migrated_environments','complete_required_programs','controls']}))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');q=a.parse_args();replay(H,q.out,q.render,q.xelatex)
