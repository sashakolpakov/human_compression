from pathlib import Path
import hashlib,json,shutil,subprocess,os
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L027_odd_three_work';old=S/'corpus106_L027_odd_three_v1';out=S/'corpus106_L027_odd_three_v2'
if out.exists():raise SystemExit('immutable v2 exists')
shutil.copytree(old,out)
p=out/'odd_three.tex';s=p.read_text();a='When $q$ is even the block embedding of $\\operatorname{SL}_2(q)$\ngives the same normalizers.';b='When $q>2$ is even the block embedding of $\\operatorname{SL}_2(q)$\ngives the same normalizers. For $q=2$ the nonsplit construction gives\n$D_6$; the trivial split torus gives no rank-two marking.'
if a not in s:raise ValueError('literal first delta')
s=s.replace(a,b);a2='Their dihedral subgroups realize the corresponding smaller orders.';b2='Their dihedral subgroups with rotation order at least two realize the\ncorresponding smaller orders.'
if a2 not in s:raise ValueError('literal second delta')
p.write_text(s.replace(a2,b2))
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
native=W/'native_v2';native.mkdir();shutil.copy2(p,native/p.name)
for i in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','odd_three.tex'],cwd=native,env=env,capture_output=True);(native/('build'+str(i)+'.stdout')).write_bytes(r.stdout);(native/('build'+str(i)+'.stderr')).write_bytes(r.stderr)
 if r.returncode:raise ValueError('native')
log=(native/'odd_three.log').read_text()
if any(x in log for x in ['Warning','Overfull','Underfull']):raise ValueError('native warnings')
shutil.copy2(native/'odd_three.pdf',out/'odd_three.pdf')
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
deps=json.loads((out/'dependencies.json').read_text());deps.extend(pin(old/n)for n in ['manifest.json','odd_three.tex','odd_three.pdf'])
write(out/'dependencies.json',deps)
write(out/'edition_delta.json',dict(predecessor=pin(old/'manifest.json'),changes=[dict(before=a,after=b),dict(before=a2,after=b2)],review_correction='f003 independently identified the trivial q2 split torus normalizer boundary; publication_recovery relayed and reviewed it',unchanged=['All theorem statements','Odd rank-three proof','literal.py','finite.g','check.py','literal_expected.json','finite_expected.json']))
with (out/'development.rst').open('a')as f:f.write('\nV2 narrows the split-normalizer construction at q=2 and excludes rotation\norder one from rank-two realizations. This independent reviewer correction\nchanges only the two displayed manuscript sentences and native output. The\ncomplete v1 finite replay remains exact; no group enumeration is repeated.\n')
shutil.copy2(W/'prepare_v2.py',out/'prepare_v2.py')
exports=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name!='manifest.json':x=pin(p);x['path']=str(p.relative_to(out));exports.append(x)
write(out/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports));print(pin(out/'manifest.json'))
