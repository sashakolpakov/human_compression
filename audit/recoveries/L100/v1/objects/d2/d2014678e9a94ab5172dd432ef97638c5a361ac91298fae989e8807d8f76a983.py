from pathlib import Path
import hashlib,json,subprocess
S=Path('/Users/sasha/medusa/research/leemans');D=S/'reboot_20261013/L091_rank_two_distinct';Q=S/'reboot_20261013/L091_work';A=S/'corpus106_L091_rank_two_v1';O=D/'final_author01'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(p,r):
 if p.stat().st_size!=r['bytes']or h(p)!=r['sha256']:raise ValueError(str(p))
(O/'first_attempt.json').write_text(json.dumps(dict(status='REVIEWER_NATIVE_TEXT_HELPER_UNAVAILABLE_AFTER_SUCCESSFUL_BUILD',session_id=44819,exit_code=1,missing='/opt/homebrew/bin/pdftotext',script_sha256=h(D/'check_final_author.py'),scientific_checks_unchanged=True,native_builds_completed=2,author_files_changed=False),indent=2)+'\n')
m=json.loads((A/'manifest.json').read_text())
if h(A/'manifest.json')!='cd5d88b1948e753830dad6e5b19714fdc7531c0b826b27d936901380776b8e12':raise ValueError('Author pin')
for r in m['exports']:ck(A/r['path'],r)
d=json.loads((A/'dependencies.json').read_text())
for r in d:ck(Path(r['path']),r)
lib=json.loads((Q/'retained_library_inputs.json').read_text())
for r in lib['files']:ck(Path(r['path']),r)
for r in json.loads((D/'working_report.json').read_text())['inputs']:ck(S/r['path']if r['namespace']=='study'else Path(r['path']),r)
for p,name in [(Q/'rank_two.pdf','author'),(O/'native/rank_two.pdf','review')]:
 cmd=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=txtwrite','-sOutputFile='+str(O/(name+'.txt')),str(p)]
 r=subprocess.run(cmd,capture_output=True,timeout=30)
 if r.returncode or r.stderr:raise ValueError('Text extraction')
if (O/'author.txt').read_bytes()!=(O/'review.txt').read_bytes():raise ValueError('Native text differs')
r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(O/'page-%02d.png'),str(O/'native/rank_two.pdf')],capture_output=True,timeout=30)
if r.returncode or r.stderr:raise ValueError('Raster failure')
report=dict(status='PASS_EXACT_FINAL_AUTHOR_AND_NATIVE',author_manifest_sha256=h(A/'manifest.json'),author_exports=len(m['exports']),author_dependencies=len(d),library_inventory_files=len(lib['files']),working_math_inputs_identical=True,native_text_identical=True,native_pages=len(list(O.glob('page-*.png'))),no_geometry_census_repeated=True,preserved_initial_attempt='first_attempt.json')
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
