"""Portable assembly binding/migration/render check; no scientific census rerun."""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parent

def need(t,m):
 if not t:raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def proof_environments(t):return re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}(.*?)\\end\{\1\}',t,re.S)
def native_body(t):
 return t.split('\\maketitle',1)[1].split('\\begin{thebibliography}',1)[0].split('\\end{document}',1)[0].strip()+'\n'
def migrated(r,base=ROOT):
 b=native_body((base/r['source']).read_text())
 need(hashlib.sha256(b.encode()).hexdigest()==r['original_body_sha256'],'original body hash')
 for lab in r['labels']:
  for cmd in ['label','ref','eqref','pageref']:b=b.replace('\\'+cmd+'{'+lab+'}','\\'+cmd+'{'+r['label_prefix']+lab+'}')
 for x in r['edits']:
  need(x['old'] in b,'declared migration edit missing');b=b.replace(x['old'],x['new'])
 return r.get('prepend','')+b

def semantic(scope,sm,programs,formal,migration):
 need(scope['original_id']=='N014' and scope['source_pages']==25,'whole fixed primary')
 need(len(scope['native_manuscripts'])==3,'all common/application manuscripts')
 need(scope['claims']['new_original_credit']==0 and not scope['claims']['whole_source_admitted'],'no admission by author')
 need(not scope['claims']['new_measurement'] and scope['claims']['new_Lean_declarations']==0,'no measurement/formal enlargement')
 need(all(v is None for v in scope['unknown_costs'].values()),'unknown costs are not zero')
 rows=sm['rows'];need(len(rows)==52 and sm['named_count']==43 and sm['additional_count']==9,'complete source inventory')
 need(len({r['id'] for r in rows})==52,'unique clause ids')
 need(not sm['unresolved_principal'],'no hidden unpaid principal slot')
 by={r['source_label']:r for r in rows}
 need(by['Theorem A']['status']=='CLAUSEWISE_CORRECTED' and 'sections/40-transitivity-converse.tex' in by['Theorem A']['proof_files'],'introductory converse correction')
 need(by['Theorem B']['status']==by['Theorem 4.4']['status']=='RECOVERED_LITERAL_COSET_IDENTIFICATION','literal coset identification retained')
 need(by['Proposition 3.13']['status']=='REFUTED_AND_REPAIRED','unrestricted RC false')
 need(by['Proposition 3.17']['status']=='CORRECTED','at-least-one endpoint correction')
 need(by['Lemma 4.6']['status']=='VACUOUS_LITERAL_SUFFICIENCY_WITH_EXACT_REPLACEMENT','vacuity distinguished from false implication')
 need(by['Theorem 4.1']['status']=='BORROWED_WITH_EXPLICIT_LIMIT','borrowed nonthin splitting boundary')
 need(by['Proposition 5.8']['status']=='CORRECTED_EXACT_PRESENTATION_WEAK_QUOTIENT_TRUE','presentation/quotient distinction')
 need(all('Figure'+str(i) in by for i in range(5,9)),'all four diagram families')
 for r in rows:need(r['proof_files'] and all((ROOT/p).is_file() for p in r['proof_files']),'proof route exists')
 required={x['path'] for x in programs['current_files'] if x['required_for_N014']}
 need(required=={'inputs/phase30_affine_map_check.py','inputs/phase30_affine_map_check.json'},'complete regular-counterexample finite premise')
 need(not any(x['required_for_N014'] for x in programs['current_files'] if x['role']=='optional_validation'),'optional validation not premise')
 need(formal['total_scoped_declarations']==22 and formal['new_declarations']==0 and not formal['full_source_formalization'],'exact partial formal scope')
 need(len(migration['phase30_transfer'])==7,'all seven phase30 sections')
 need(len(migration['native_tex'])==5,'all five new native proof packets')
 return True

def controls(scope,sm,pr,fo,mi):
 cases=[]
 def add(name,fn):
  args=copy.deepcopy([scope,sm,pr,fo,mi]);fn(args)
  try:semantic(*args)
  except ValueError:cases.append(name)
  else:raise ValueError('negative control accepted '+name)
 add('source page dropped',lambda a:a[0].__setitem__('source_pages',24))
 add('common omitted',lambda a:a[0]['native_manuscripts'].pop(0))
 add('author source credit',lambda a:a[0]['claims'].__setitem__('new_original_credit',1))
 add('premature admission',lambda a:a[0]['claims'].__setitem__('whole_source_admitted',True))
 add('measurement inserted',lambda a:a[0]['claims'].__setitem__('new_measurement',True))
 add('unknown set zero',lambda a:a[0]['unknown_costs'].__setitem__('historical_source_software',0))
 add('source clause dropped',lambda a:a[1]['rows'].pop())
 add('duplicate clause id',lambda a:a[1]['rows'][1].__setitem__('id',a[1]['rows'][0]['id']))
 add('unpaid principal suppressed',lambda a:a[1]['unresolved_principal'].append('unproved'))
 for label,status in [('Theorem A','RECOVERED'),('Theorem B','REFUTED'),('Proposition 3.13','RECOVERED'),('Proposition 3.17','RECOVERED'),('Lemma 4.6','REFUTED'),('Theorem 4.1','NEW_THEOREM'),('Proposition 5.8','RECOVERED')]:
  add('wrong disposition '+label,lambda a,label=label,status=status:next(r for r in a[1]['rows'] if r['source_label']==label).__setitem__('status',status))
 add('required data omitted',lambda a:a[2]['current_files'][1].__setitem__('required_for_N014',False))
 add('optional code promoted',lambda a:next(r for r in a[2]['current_files'] if r['role']=='optional_validation').__setitem__('required_for_N014',True))
 add('full formal claim',lambda a:a[3].__setitem__('full_source_formalization',True))
 add('phase30 proof section omitted',lambda a:a[4]['phase30_transfer'].pop())
 add('native proof packet omitted',lambda a:a[4]['native_tex'].pop())
 return cases

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 manifest=ROOT/'manifest.json';self_n=0
 if manifest.exists():
  for e in read(manifest)['exports']:
   p=ROOT/e['path'];need(p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],'frozen export '+e['path']);self_n+=1
 bindings=read(ROOT/'copy_bindings.json')
 for e in bindings:
  p=ROOT/e['destination'];need(p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],'exact inherited copy '+e['destination'])
  q=None
  if e['source'].startswith('/Users/sasha/medusa/math_compression/') and a.public_root:q=a.public_root/e['source'].split('/math_compression/',1)[1]
  elif not e['source'].startswith('/') and a.study_root:q=a.study_root/e['source']
  if q is not None:need(q.stat().st_size==e['bytes'] and digest(q)==e['sha256'],'external predecessor binding')
 scope=read(ROOT/'scope.json');sm=read(ROOT/'source_map.json');pr=read(ROOT/'program_inventory.json');fo=read(ROOT/'formal_scope.json');mi=read(ROOT/'migration.json');semantic(scope,sm,pr,fo,mi)
 if a.study_root:
  e=scope['source'];p=a.study_root/e['path'];need(p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],'primary source pin')
 env=0
 for r in mi['native_tex']:
  expected=migrated(r);actual=(ROOT/r['target']).read_text();need(actual==expected,'exact native transfer '+r['target']);env+=len(proof_environments(actual))
 for r in pr['current_files']:
  p=ROOT/r['path'];need(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'whole program boundary')
 raw=read(ROOT/'raw_occurrences.json')
 for r in raw['occurrences']:
  p=ROOT/r['path'];need(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'raw occurrence pin')
 need(raw['content_count']==len({r['sha256'] for r in raw['occurrences']}),'unique whole content count')
 tests=controls(scope,sm,pr,fo,mi)
 # Isolated transfer corruption must be detected independently of the outer manifest.
 need(migrated(mi['native_tex'][0])!=(ROOT/mi['native_tex'][0]['target']).read_text().replace('None of these assertions requires','All of these assertions require'),'coset hypothesis mutation')
 tests.append('coset output-RC premise inserted')
 phase=read(ROOT/'inputs/phase30_affine_map_check.json');need(phase['status']=='PASS' and phase['code_dimension']==17 and phase['column_membership_tests']==720,'accepted finite receipt')
 report={'status':'PASS','self_exports':self_n,'exact_inherited_copies':len(bindings),'source_dispositions':52,'named_items':43,'native_mathematical_environments':env,'phase30_sections':7,'whole_program_inventory':len(pr['current_files']),'raw_occurrences':raw['occurrence_count'],'unique_raw_contents':raw['content_count'],'controls_rejected':tests,'scientific_programs_rerun':False,'Lean_rerun':False,'render':[]}
 if a.render:
  from pypdf import PdfReader
  for item in scope['native_manuscripts']:
   src=ROOT/item['tex'];d=a.out/src.stem;d.mkdir();args=[a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(d),src.name]
   for n in range(2):
    r=subprocess.run(args,cwd=src.parent,capture_output=True,text=True);(d/f'pass{n+1}.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'render '+str(src))
   log=(d/(src.stem+'.log')).read_text();need(all(s not in log for s in ['Overfull','undefined','Missing character']),'clean render '+src.stem)
   current=[p.extract_text() for p in PdfReader(d/(src.stem+'.pdf')).pages];frozen=[p.extract_text() for p in PdfReader(ROOT/item['path']).pages];need(current==frozen,'exact page texts '+src.stem);report['render'].append({'document':item['path'],'pages':len(current),'text_equal':True,'diagnostics':[]})
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
