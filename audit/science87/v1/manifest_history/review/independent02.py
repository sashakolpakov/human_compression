"""Bounded independent controls; no full snapshot and no public writes."""
from pathlib import Path
import ast, copy, hashlib, importlib.util, json, os, subprocess, sys, tempfile
sys.dont_write_bytecode=True
R=Path('/Users/sasha/medusa/math_compression')
W=Path(__file__).resolve().parent
E=W/'evidence01'
C=Path('/Users/sasha/medusa/research/leemans/reboot_20261013/combined_dispositions_publication_work')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):return json.loads(p.read_text())
def module(p):
 s=importlib.util.spec_from_file_location('bounded_'+p.stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module(R/'scripts/check_science87.py');old=module(E/'scripts/check_science87.py')
cor=get(C/'manifest_correction01/correction.json')
new=(R/'scripts/check_science87.py').read_text();previous=(E/'scripts/check_science87.py').read_text()
addition="  if r['path']=='provenance/publication_manifest.json':\n   archived=dict(r,path=AUD+'/manifest_history/predecessor_publication_manifest.json')\n   p=bind(root,archived);need(not (root/archived['path']).is_symlink() and bool(p.stat().st_mode&0o111)==(r['mode']=='100755'),'Predecessor manifest mode preserved');continue\n"
assert new.count(addition)==1 and new.replace(addition,'')==previous
assert m.HISTORY==old.HISTORY and len(m.HISTORY)==9
for p in ['scripts/verify_snapshot.py','scripts/check_science87_history.py','audit/science87/v1/history_routes.json','audit/science87/v1/predecessor_tree.json']:
 assert (R/p).read_bytes()==(E/p).read_bytes(),p
assert sha(R/'scripts/check_science87.py')==cor['new_checker']['sha256']=='8a3cf3cef317ba7f00f47de66378a992432bdcb2212496fd81d02cf3e4d90371'
for name,pin in cor['old_routes'].items():
 m.bind(R,pin);assert (R/pin['path']).read_bytes()==(E/name).read_bytes(),name
m.bind(R,cor['predecessor_manifest'])
assert (R/cor['predecessor_manifest']['path']).read_bytes()==(E/'predecessor_publication_manifest.json').read_bytes()
oldroutes=cor['old_routes'];shared='audit/science87/v1/root_integration.json';individuals=set(oldroutes)-{'scripts/check_science87.py',shared}
for name in [*sorted(individuals),shared]:
 a=get(E/name);b=get(R/name);expected=copy.deepcopy(a)
 for pin in expected['bindings']:
  if pin['path']=='scripts/check_science87.py':pin.update(cor['new_checker'])
  elif name==shared and pin['path'] in individuals:
   p=R/pin['path'];pin.update(bytes=p.stat().st_size,sha256=sha(p))
 extra=b['publication_manifest_correction']
 assert set(extra)=={'previous_gate','previous_checker','predecessor_manifest','scope'}
 assert extra['previous_gate']==oldroutes[name] and extra['previous_checker']==oldroutes['scripts/check_science87.py'] and extra['predecessor_manifest']==cor['predecessor_manifest']
 assert extra['scope']=='Only the regenerated publication manifest is checked at its immutable predecessor path in the old-tree audit. Current tracked-file integrity remains checked by publication_rows in verify_snapshot.py. Mathematical acceptance and credits are unchanged.'
 expected['publication_manifest_correction']=extra
 expected['bindings'] += [oldroutes[name],oldroutes['scripts/check_science87.py'],cor['predecessor_manifest']]
 assert b==expected,name
 for p in expected['bindings'][-3:]:m.bind(R,p)
# Execute the literal final tree-audit loop, isolated from unrelated source checks.
f=next(n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef) and n.name=='verify')
loop=next(n for n in f.body if isinstance(n,ast.For) and ast.unparse(n.iter)=="tree['files']")
code=compile(ast.fix_missing_locations(ast.Module(body=[loop],type_ignores=[])),'literal_tree_loop','exec')
row=next(r for r in get(R/'audit/science87/v1/predecessor_tree.json')['files'] if r['path']=='provenance/publication_manifest.json')
checks=[]
def expect_bad(label,fn):
 try:fn()
 except (ValueError,AssertionError):checks.append(label)
 else:raise AssertionError('Damaged input accepted: '+label)
with tempfile.TemporaryDirectory(prefix='science87-manifest-review-') as d:
 root=Path(d).resolve();p=root/cor['predecessor_manifest']['path'];p.parent.mkdir(parents=True);raw=(E/'predecessor_publication_manifest.json').read_bytes();p.write_bytes(raw)
 live=root/row['path'];live.parent.mkdir(parents=True);live.write_text('{"files":[]}\n')
 scope=dict(m.__dict__,root=root,tree={'files':[row]},history={'routes':{}})
 def run():exec(code,scope)
 run();checks.append('literal archive branch accepts independently regenerated live manifest')
 p.write_bytes(raw+b'x');expect_bad('archive length damage',run);p.write_bytes(raw)
 p.write_bytes(bytes([raw[0]^1])+raw[1:]);expect_bad('archive same-length hash damage',run);p.write_bytes(raw)
 p.chmod(0o755);expect_bad('archive executable-mode damage',run);p.chmod(0o644)
 # The final branch tests the literal locator before following its safe target.
 target=root/'same_bytes';target.write_bytes(raw);p.unlink();p.symlink_to(target);expect_bad('archive internal symlink with exact bytes and mode',run);p.unlink();p.write_bytes(raw)
 target=root/'target';target.write_bytes(raw+b'x');p.unlink();p.symlink_to(target);expect_bad('archive symlink to wrong bytes',run);p.unlink();p.write_bytes(raw)
 # Invoke actual current-manifest generator and literal main equality in a tiny Git fixture.
 source=(R/'scripts/verify_snapshot.py').read_text();tree=ast.parse(source)
 funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'publication_rows','need','digest','load'}]
 main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
 equality=next(n for n in main.body if isinstance(n,ast.Expr) and 'Publication differs from manifest.' in ast.unparse(n))
 ns=dict(ROOT=root,MANIFEST=live,subprocess=subprocess,json=json,sha256=hashlib.sha256)
 exec(compile(ast.fix_missing_locations(ast.Module(body=funcs,type_ignores=[])),'literal_manifest_functions','exec'),ns)
 subprocess.run(['git','init','-q',str(root)],check=True)
 (root/'artifact.txt').write_text('fixed artifact\n')
 subprocess.run(['git','add','artifact.txt','provenance/publication_manifest.json'],cwd=root,check=True)
 eq=compile(ast.fix_missing_locations(ast.Module(body=[equality],type_ignores=[])),'literal_manifest_equality','exec')
 def current():
  ns['rows']=ns['publication_rows']();exec(eq,ns)
 live.write_text(json.dumps({'files':ns['publication_rows']()}));current();checks.append('literal current-manifest equality passes')
 live.write_text('{"files":[]}');expect_bad('live manifest damage remains rejected',current)
 live.write_text(json.dumps({'files':ns['publication_rows']()}));(root/'artifact.txt').write_text('changed artifact\n');expect_bad('tracked artifact damage remains rejected',current)
 live.write_text(json.dumps({'files':ns['publication_rows']()}));current();run();checks.append('regeneration and historical check coexist')
expect_bad('original unchanged checker rejects regenerated live manifest',lambda:old.bind(R,row))
report=dict(status='PASS_INDEPENDENT_MANIFEST_CORRECTION',exact_added_lines=3,old_routes_preserved=9,old_gate_bytes_preserved=7,gate_deltas_verified=7,unchanged_history_and_main_files=4,controls=checks,public_writes=False,full_snapshot_repeated=False)
(W/'independent_report02.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
