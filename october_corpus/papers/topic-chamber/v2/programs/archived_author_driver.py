"""Replay the exact finite source example using stock GAP, without RAMP."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,tempfile,time
root=Path(__file__).resolve().parent
script=root/'phase41_chiral_cover_check.g'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
h=sha(script);start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='phase41_chiral_') as tmp:
    r=subprocess.run([shutil.which('gap'),'-q',str(script)],cwd=tmp,capture_output=True,text=True,timeout=300)
assert sha(script)==h
assert r.returncode==0 and not r.stderr.strip(),(r.returncode,r.stderr,r.stdout)
assert not re.search(r'Error,|Syntax error|FAIL',r.stdout),r.stdout
assert len(re.findall(r'^ROW ',r.stdout,re.M))==6
assert 'DISTINGUISH (b*c^-1)^2*a*c^2*a^-1 ORDERS [1,3]' in r.stdout
assert 'CHIRALITY facet=vertex=<b^3> ORDER 3' in r.stdout
assert 'PASS GAP ' in r.stdout
log=root/'phase41_chiral_cover_check.log';log.write_text(r.stdout)
report={'status':'PASS','date':'2026-10-10','wall_seconds':time.monotonic()-start,
'script':script.name,'script_sha256':h,'runner_sha256':sha(Path(__file__)),
'log_sha256':sha(log),'source_unchanged':True,'gap':shutil.which('gap'),
'scope':'Exact source P,T,Tdual bare presentations; full finite orders; mixed groups R,Q,Qdual; string C+ intersection properties; mirror automorphisms; marked degree-three covers; duality; distinguishing word.',
'GAP_version':re.search(r'PASS GAP (\S+)',r.stdout).group(1),
'retained':'GAP exact finitely presented/permutation group algorithms and standard C+ group/polytope correspondence. No RAMP or SmallGroups. No Lean verification.',
'rotation_orders':{'P':324,'T':324,'Tdual':324,'R':972,'Q':2916,'Qdual':2916},
'R_end_intersection_order':27,'medial_order':9,'Q_Qdual_end_intersection_order':9,
'distinguishing_word':'(b c^-1)^2 a c^2 a^-1','distinguishing_orders':[1,3]}
(root/'phase41_chiral_cover_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
