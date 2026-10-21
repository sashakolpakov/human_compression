"""Independent binding, reverse-migration, source-scope and small-model review.
No import or execution of the author checker; no census or Lean replay.
"""
from pathlib import Path
import argparse,copy,hashlib,json,re,subprocess,sys
HERE=Path(__file__).resolve().parent
PIN='1e4f67f5a84b39177c666b55d7884ca8ab6281f6f4b2de803a1c36f9d56cb973'
def require(ok,why):
 if not ok:raise ValueError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def check_binding(root,e):
 p=root/e['path'];require(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'binding: '+e['path'])
def body(t):
 m=re.search(r'\\maketitle\s*\n(?P<body>[\s\S]*?)(?:\\begin\{thebibliography\}|\\end\{document\})',t)
 require(m is not None,'body delimiters');return m['body'].strip()
def reverse_migration(root,m,override=None):
 t=override if override is not None else (root/m['target']).read_text()
 prefix=m.get('prepend','');require(t.startswith(prefix),'prepend');t=t[len(prefix):]
 for e in reversed(m['edits']):
  require(e['new'] in t,'declared replacement present');t=t.replace(e['new'],e['old'])
 for label in m['labels']:
  t=re.sub(r'(\\(?:label|ref|eqref|pageref)\{)'+re.escape(m['label_prefix']+label)+r'\}',lambda z:z[1]+label+'}',t)
 require(t.strip()==body((root/m['source']).read_text()),'reverse mathematical migration: '+m['target'])
 return len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary|proof)\}',t))
def semantic(a,expected):
 scope,sm,programs,formal,connector,overlay=a
 actual={r['source_label']:(r['status'],r['physical_page'],r['proof_files']) for r in sm['rows']}
 wanted={r['source_label']:(r['disposition'],r['physical_page'],r['proof_files']) for r in expected['rows']}
 require(len(sm['rows'])==52 and len(actual)==52 and actual==wanted,'reviewed 52 source routes/dispositions')
 require(scope['source_pages']==25 and [r['pages'] for r in scope['native_manuscripts']]==[10,8,17],'whole source/common/application acquisition')
 require(scope['claims']['new_original_credit']==0 and scope['claims']['new_conjecture_credit']==0 and not scope['claims']['new_measurement'],'no admission or numerical claim')
 require('residually connected incidence geometry' in connector,'original RC premise')
 require('PC' in connector,'all-flag parity premise')
 require(all(x is None for x in scope['unknown_costs'].values()),'unknown external/software/graphics costs')
 req={r['path']:r['role'] for r in programs['current_files'] if r['required_for_N014']}
 require(req=={'inputs/phase30_affine_map_check.py':'required_mathematical_program','inputs/phase30_affine_map_check.json':'required_mathematical_data'},'complete exact finite proof premise')
 require(sum(r['role']=='optional_validation' for r in programs['current_files'])==6,'six optional diagnostics')
 require(formal['new_declarations']==0 and formal['total_scoped_declarations']==22 and formal['additional_declarations']==6 and formal['reused_old_scoped_declarations']==16 and not formal['full_source_formalization'],'partial reused Lean boundary')
 require(overlay['role']=='operational_assembly_binding_and_render_driver' and not overlay['mathematical_premise'] and overlay['whole_file_disclosed'],'current driver scope')
 require('arbitrary nonthin' in ' '.join(sm['borrowed_excluded']),'borrowed nonthin theorem boundary')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);args=ap.parse_args();P=args.packet;O=args.out;O.mkdir(parents=True,exist_ok=False)
 require(sha(P/'manifest.json')==PIN,'exact author freeze')
 entries=read(P/'manifest.json')['exports']
 require(len(entries)==183 and len({e['path'] for e in entries})==183,'183 exact exports')
 for e in entries:check_binding(P,e)
 self_manifest=HERE/'manifest.json'
 if self_manifest.exists():
  for e in read(self_manifest)['exports']:check_binding(HERE,e)
 copies=read(P/'copy_bindings.json');require(len(copies)==152,'152 inherited files')
 for e in copies:check_binding(P,dict(e,path=e['destination']))
 mi=read(P/'migration.json');require(len(mi['native_tex'])==5,'five native migrations')
 env=sum(reverse_migration(P,m) for m in mi['native_tex']);require(env==32,'32 whole environments')
 require(len(mi['phase30_transfer'])==7,'seven phase30 sections')
 phase=(P/'sections/10-regular-counterexample.tex').read_text()
 require(all(r['destination_section'] in ' '.join(phase.split()) for r in mi['phase30_transfer']),'seven phase30 section routes')
 scope=read(P/'scope.json');sm=read(P/'source_map.json');programs=read(P/'program_inventory.json');formal=read(P/'formal_scope.json');connector=(P/'sections/01-residues.tex').read_text();b=read(HERE/'binding.json');expected=read(HERE/'source_review.json')
 require(sm['source']==scope['source']==b['source']==expected['source'],'same exact source')
 if args.study_root:check_binding(args.study_root,b['source'])
 a=[scope,sm,programs,formal,connector,b['current_operational_overlay']];semantic(a,expected)
 for r in expected['rows']:
  for f in r['proof_files']:require((P/f).is_file(),'every source proof route')
 for r in programs['current_files']:check_binding(P,r)
 raw=read(P/'raw_occurrences.json')
 for r in raw['occurrences']:check_binding(P,r)
 require(len(raw['occurrences'])==114 and len({r['sha256'] for r in raw['occurrences']})==113,'114/113 inherited raw boundary')
 check_binding(P,b['current_operational_overlay'])
 tests=[]
 def reject(label,mut):
  x=copy.deepcopy(a);mut(x)
  try:semantic(x,expected)
  except ValueError:tests.append(label)
  else:raise ValueError('control escaped: '+label)
 reject('original RC removed',lambda x:x.__setitem__(4,x[4].replace('residually connected incidence geometry','incidence geometry')))
 reject('whole inherited common omitted',lambda x:x[0]['native_manuscripts'].pop(0))
 reject('source page omitted',lambda x:x[0].__setitem__('source_pages',24))
 reject('author grants original credit',lambda x:x[0]['claims'].__setitem__('new_original_credit',1))
 reject('software unknown zeroed',lambda x:x[0]['unknown_costs'].__setitem__('historical_source_software',0))
 for label,new in [('Theorem A','RECOVERED'),('Theorem B','REFUTED'),('Proposition 3.13','RECOVERED'),('Proposition 3.17','RECOVERED'),('Lemma 4.6','REFUTED'),('Theorem 4.1','RECOVERED'),('Proposition 5.8','RECOVERED'),('Proposition 5.12','RECOVERED')]:
  reject('wrong literal scope: '+label,lambda x,label=label,new=new:next(r for r in x[1]['rows'] if r['source_label']==label).__setitem__('status',new))
 reject('source proof route removed',lambda x:x[1]['rows'][0]['proof_files'].pop())
 reject('required finite data removed',lambda x:x[2]['current_files'][1].__setitem__('required_for_N014',False))
 reject('optional diagnostic becomes premise',lambda x:x[2]['current_files'][2].__setitem__('required_for_N014',True))
 reject('full-source formalization asserted',lambda x:x[3].__setitem__('full_source_formalization',True))
 reject('borrowed nonthin boundary suppressed',lambda x:x[1].__setitem__('borrowed_excluded',[]))
 reject('top-level driver hidden',lambda x:x[5].__setitem__('whole_file_disclosed',False))
 reject('top-level driver promoted to mathematical premise',lambda x:x[5].__setitem__('mathematical_premise',True))
 m=mi['native_tex'][0]
 try:reverse_migration(P,m,(P/m['target']).read_text()+'\nUnrecorded premise.\n')
 except ValueError:tests.append('unrecorded migration mutation')
 else:raise ValueError('migration control escaped')
 subprocess.run([sys.executable,'-B','-O',str(HERE/'check_models.py'),'--out',str(O/'models.json')],check=True,capture_output=True,text=True)
 model=read(O/'models.json');require(model==read(HERE/'models.json'),'fresh independent model results')
 report={'status':'PASS','author_manifest_sha256':PIN,'export_bindings':len(entries),'exact_inherited_copies':len(copies),'source_rows':52,'native_migrations':5,'mathematical_environments':env,'phase30_sections':7,'inherited_current_file_roles':12,'inherited_raw_occurrences':114,'inherited_unique_raw_contents':113,'additional_current_operational_driver':b['current_operational_overlay'],'controls_rejected':tests,'independent_models':model,'author_code_imported':False,'scientific_census_rerun':False,'Lean_rerun':False,'source_binding_checked':bool(args.study_root)}
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
