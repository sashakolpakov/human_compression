from pathlib import Path
import tempfile,shutil,json,subprocess,hashlib,importlib.util
PUBLIC=Path('/Users/sasha/medusa/math_compression');PRIVATE=Path('/Users/sasha/medusa/research/leemans');ROOT=Path(tempfile.mkdtemp(prefix='actual-tex-builder-',dir='/private/tmp'));REPO=ROOT/'repo';(REPO/'scripts').mkdir(parents=True);(REPO/'papers/topic-a/v2').mkdir(parents=True);(REPO/'papers/legacy').mkdir(parents=True)
source=PUBLIC/'scripts/build_papers.py';shutil.copy2(source,REPO/'scripts/build_papers.py')
base=REPO/'papers/topic-a/v2';volume=PRIVATE/'topic_A_volume'
for name in ['umbrella.tex','preamble.tex','high-type-two-groups.tex','order-1024-markings.tex']:shutil.copy2(volume/name,base/name)
shutil.copytree(volume/'umbrella-sections',base/'umbrella-sections')
legacy='papers/legacy/pgl.tex';shutil.copy2(PUBLIC/'papers/topic-e/v2/pgl-polytopes.tex',REPO/legacy)
pre='papers/topic-a/v2/preamble.tex';sections=['papers/topic-a/v2/'+str(p.relative_to(base)) for p in sorted((base/'umbrella-sections').glob('*.tex'))]
rows=[{'id':'legacy','tex':legacy},*({'id':'topic-a/v2/'+n,'tex':'papers/topic-a/v2/'+n+'.tex','tex_inputs':[pre]+(sections if n=='umbrella' else [])} for n in ['umbrella','high-type-two-groups','order-1024-markings'])]
cat={'papers':[rows[0]],'new_editions':rows[1:]};(REPO/'papers/catalogue.json').write_text(json.dumps(cat))
spec=importlib.util.spec_from_file_location('actual_candidate',REPO/'scripts/build_papers.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
tests=[]
def test(name,fn,raises=False):
 try:fn();ok=not raises
 except (ValueError,OSError):ok=raises
 tests.append({'case':name,'passed':ok});
 if not ok:raise RuntimeError(name)
def eq(x,y):
 if x!=y:raise ValueError((x,y))
for bad in ['bad\x00path','bad\tpath','bad\rpath','bad\npath']:
 test('control_'+repr(bad),lambda bad=bad:mod.relative_path(bad),True)
test('legacy_omitted_list',lambda:eq(len(mod.source_bundle(rows[0])),1))
test('umbrella_declared_closure',lambda:eq(len(mod.source_bundle(rows[1])),len(sections)+2))
test('catalogue_order_not_request_order',lambda:eq(mod.select_papers(cat,[rows[2]['id'],'legacy']),[rows[0],rows[2]]))
test('unknown_ID',lambda:mod.select_papers(cat,['missing']),True)
test('duplicate_global_ID',lambda:mod.select_papers({'papers':[rows[0],rows[0]]},[rows[0]['id']]),True)
test('repeated_selection_idempotent',lambda:eq(mod.select_papers(cat,['legacy','legacy']),[rows[0]]))
for name,inputs in [('duplicate',[pre,pre]),('self',[rows[1]['tex']]),('traversal',['papers/topic-a/v2/../x.tex']),('absolute',['/etc/passwd']),('wrong_type','x'),('wrong_suffix',['papers/topic-a/v2/x.pdf']),('missing',['papers/topic-a/v2/missing.tex']),('outside_main',[legacy])]:
 test(name,lambda inputs=inputs:mod.source_bundle({**rows[1],'tex_inputs':inputs}),True)
(base/'linked.tex').symlink_to(base/'preamble.tex');test('file_symlink',lambda:mod.source_bundle({**rows[1],'tex_inputs':['papers/topic-a/v2/linked.tex']}),True)
(base/'linked').symlink_to(base/'umbrella-sections',target_is_directory=True);test('ancestor_symlink',lambda:mod.source_bundle({**rows[1],'tex_inputs':['papers/topic-a/v2/linked/01-markings.tex']}),True)
(base/'paper.tex').write_text('collision');test('paper_tex_collision',lambda:mod.source_bundle({**rows[1],'tex_inputs':['papers/topic-a/v2/paper.tex']}),True)
argv=['python3','-B','-O',str(REPO/'scripts/build_papers.py'),'--output-dir',str(ROOT/'good'),'--jobs','2']
for row in rows:argv.extend(['--paper',row['id']])
p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(ROOT/'good.stdout').write_text(p.stdout)
if p.returncode:raise RuntimeError(p.stdout[-3000:])
report=json.loads((ROOT/'good/report.json').read_text());test('all4_actual_compiles',lambda:eq(len(report['papers']),4))
# Verify isolated staged inputs and source hash fields, not PDF byte identity.
for row,built in zip(rows,report['papers']):
 files=mod.source_bundle(row);record={r['path']:r for r in built['tex_inputs']}
 test('hashes_'+row['id'],lambda files=files,record=record,row=row:eq(record,{n:{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in files.items() if n!=row['tex']}))
# Leave the undeclared real section present in the private repository: it must
# still be absent from staging and cause the umbrella compile to fail.
broken=json.loads(json.dumps(cat));broken['new_editions'][0]['tex_inputs'].remove(sections[0]);(REPO/'papers/catalogue.json').write_text(json.dumps(broken))
p=subprocess.run(['python3','-B','-O',str(REPO/'scripts/build_papers.py'),'--output-dir',str(ROOT/'omitted'),'--paper',rows[1]['id']],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(ROOT/'omitted.stdout').write_text(p.stdout)
test('undeclared_nested_input_fails_real_U',lambda:eq(p.returncode!=0,True))
test('undeclared_input_not_copied',lambda:eq((ROOT/'omitted'/rows[1]['id']/'umbrella-sections/01-markings.tex').exists(),False))
# A literal absolute input can be read by TeX, but the final candidate must
# reject that original-repository read via its actual recorder interface.
secret=REPO/'unreviewed.tex';secret.write_text('UNDECLARED.\n')
(REPO/legacy).write_text('\\documentclass{article}\\begin{document}\\input{'+str(secret)+'}\\end{document}\n')
(REPO/'papers/catalogue.json').write_text(json.dumps(cat))
p=subprocess.run(['python3','-B','-O',str(REPO/'scripts/build_papers.py'),'--output-dir',str(ROOT/'absolute-rejected'),'--paper','legacy'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(ROOT/'absolute.stdout').write_text(p.stdout)
test('absolute_original_repository_input_rejected',lambda:eq(p.returncode!=0 and 'unstaged repository input' in p.stdout,True))
# A complete valid recorder is accepted; system TeX and fonts remain external.
mod.check_repository_reads(ROOT/'good'/rows[1]['id'],root=REPO)
test('declared_real_umbrella_recorder_accepted',lambda:eq(True,True))
out={'status':'PASS','candidate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'tested_copy_sha256':hashlib.sha256((REPO/'scripts/build_papers.py').read_bytes()).hexdigest(),'temporary_root':str(ROOT),'tests':tests,'compiled_report':report,'scope':'Actual candidate functions and fresh isolated real U/A5/A6 plus one legacy one-file TeX; no public or frozen changes.'}
(PRIVATE/'tex_inputs_candidate_final_test.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'tests':len(tests),'temporary_root':str(ROOT),'sha256':out['tested_copy_sha256']}))
