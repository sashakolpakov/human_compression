#!/usr/bin/env python3
"""Fresh-output exact checks of the uniform obstruction and one finite degree-2/4 census."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, tempfile, time
root = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--report', type=Path, required=True)
ap.add_argument('--log', type=Path, required=True)
a = ap.parse_args()
assert not a.report.exists() and not a.log.exists(), 'fresh output paths required'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
names = ['phase58_2primary_cover_check.g','phase58_2primary_cover_extension_check.g',
         'phase58_2primary_cover_theorem.md','phase58_2primary_cover_ledger.md',
         'phase58_2primary_cover_intake.json','phase49_cover_family_source_web.txt',
         'phase49_cover_family_presentation_web.txt']
before = {name:sha(root/name) for name in names}
# Frozen earlier packages are read only; no author checker that overwrites reports is invoked.
for manifest in ['phase49_cover_family_manifest.json','phase46_cover_manifest.json']:
    before[manifest] = sha(root/manifest)
    for name, md in json.loads((root/manifest).read_text())['files'].items():
        assert sha(root/name) == md['sha256'], name
        before[name] = md['sha256']
outputs=[]; timings={}
with tempfile.TemporaryDirectory(prefix='phase58_covers_') as td:
    for name in names[:2]:
        path=Path(td)/name;path.write_bytes((root/name).read_bytes());start=time.monotonic()
        r=subprocess.run([shutil.which('gap'),'-q',str(path)],cwd=td,text=True,capture_output=True,timeout=1200)
        timings[name]=time.monotonic()-start
        assert r.returncode==0 and not r.stderr.strip(),(name,r.returncode,r.stderr,r.stdout)
        assert not re.search(r'FAIL|Error,|Syntax error|SKIP_',r.stdout),(name,r.stdout)
        outputs.append(r.stdout)
flat=re.sub(r'\s+',' ',outputs[0].replace('\\\n',''))
rows=re.findall(r'PARAM \[ (\d+), (-?\d+), (-?\d+) \] orders P,R,T,Qraw,Q0,Q0d,H \[ ([\d, ]+) \]',flat)
params=[(b,e,f) for b in [5,6] for e in [-1,1] for f in [-1,1]]
assert [tuple(map(int,r[:3])) for r in rows]==params,rows
for r in rows:
    q=2**int(r[0]); assert list(map(int,r[3].replace(' ','').split(',')))==[64*q,128*q,32*q,512*q,256*q,256*q,256*q]
assert 'PASS UNIFORM_DIAGNOSTICS 8' in flat
flat2=re.sub(r'\s+',' ',outputs[1].replace('\\\n',''))
assert 'PASS COMPLETE_DEGREE_2_4 beta=5 eps=1,1' in flat2
c4=re.findall(r'C4_QUOTIENTS \[ ([\d, -]+) \] \[ (\d+), (\d+), (\d+) \]',flat2)
v4=re.findall(r'V4_QUOTIENTS \[ ([\d, ]+) \] \[ (\d+), (\d+), (\d+) \]',flat2)
assert len(c4)==16 and sum(int(r[2]) for r in c4)==16 and all(r[3]=='0' for r in c4),c4
assert len(v4)==15 and sum(int(r[2]) for r in v4)==11 and all(r[3]=='0' for r in v4),v4
assert 'DOUBLE_COVERS [ 15, 1 ]' in flat2
assert 'ALL_CENTRAL_QUOTIENTS [ 67, 4 ] max good kernel sizes [ 8 ] all good [ 2, 4, 4, 8 ]' in flat2
for name,digest in before.items():assert sha(root/name)==digest,name
log=''.join(f'FILE {names[i]}\n{out}' for i,out in enumerate(outputs))
a.log.write_text(log)
report={'date':'2026-10-10','status':'PASS','runner_sha256':sha(Path(__file__)),
 'sources_pre_post_sha256':before,'log_sha256':sha(a.log),'seconds':timings,
 'uniform_diagnostics':params,'finite_scope':{'beta':5,'eps1':1,'eps2':1,'full_R_order':8192},
 'polytopal_marked_covers':{'degree_2':1,'degree_4_cyclic':16,'degree_4_central_V4':2,'degree_4_noncentral_V4':11},
 'new_minimal_degree_4':0,'cyclic_character_rows':c4,'noncentral_V4_character_rows':v4,
 'scope':'All-parameter theorem is the separate written obstruction. Exhaustive finite degree-2/4 extension census is only for beta=5, eps1=eps2=+1; no higher-degree, odd-kernel, global uniqueness, Lean or priority claim.',
 'retained':['source Theorem 4.8 for the family','standard marked geometric recognition','stock GAP exact algorithms'],
 'earlier_bound_files_unchanged':True}
a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','seconds':timings,'log_sha256':sha(a.log)},indent=2))
