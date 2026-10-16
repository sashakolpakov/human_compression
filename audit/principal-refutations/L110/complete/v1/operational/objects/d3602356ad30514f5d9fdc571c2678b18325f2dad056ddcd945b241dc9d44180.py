from pathlib import Path
import json,hashlib,subprocess,shutil,sys,importlib.util
from pypdf import PdfReader
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence';C=Y/'local_geometry_v1';O=Y/'local_geometry_root01'
assert hashlib.sha256((C/'manifest.json').read_bytes()).hexdigest()=='58f1f33fd2fbf93f2237d3378e11e76d7025e06e137f1debc01ff153d1fd4013'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/local_geometry_v1');O.mkdir();shutil.copyfile(C/'local_geometry.tex',O/'local_geometry.tex')
for i in (1,2):
 p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','local_geometry.tex'],cwd=O,capture_output=True);(O/f'build{i}.stdout').write_bytes(p.stdout);(O/f'build{i}.stderr').write_bytes(p.stderr);assert p.returncode==0
a,b=PdfReader(C/'local_geometry.pdf'),PdfReader(O/'local_geometry.pdf');assert len(a.pages)==len(b.pages)==2
assert [''.join(p.extract_text().split()) for p in a.pages]==[''.join(p.extract_text().split()) for p in b.pages]
p=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pnggray','-r90','-sOutputFile=page-%02d.png','local_geometry.pdf'],cwd=O,capture_output=True);assert p.returncode==0
(O/'report.json').write_text(json.dumps(dict(status='PASS_NATIVE_GEOMETRY_JOIN',pages=2,source_manifest_sha256='58f1f33fd2fbf93f2237d3378e11e76d7025e06e137f1debc01ff153d1fd4013',new_target_calls=0),indent=2)+'\n');print('PASS: exact package acquired and two native pages rebuilt.')
