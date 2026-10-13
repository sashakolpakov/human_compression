from pathlib import Path
import os,importlib.util,json,hashlib,subprocess,sys,difflib
S=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;C=S/'reboot_20261013/L071_publication_work/checker01';T=S/'reboot_20261013/L071_publication_work/stage02/audit/recoveries/L071/v1/transport.json';REST=W/'run01/restored'
os.environ.update(L071_RESTORED_STUDY=str(REST/'study'),L071_CHECK_OUTPUT=str(W/'unused'),L071_TRANSPORT=str(T),PYTHONDONTWRITEBYTECODE='1')
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=load('l071portablepaths',C/'portable_paths.py');main=load('l071portablemain',C/'check.py');done=[]
def reject(name,fn):
 try:fn()
 except (ValueError,FileNotFoundError):done.append(name)
 else:raise AssertionError('bad input accepted: '+name)
for n in ['../escape','/absolute','foo/../escape','']:
 reject('unsafe path '+repr(n),lambda n=n:main.safe(n))
reject('external private path',lambda:p.resolve('/private/tmp/not-evidence'))
reject('restored root escape',lambda:p.resolve('../../escape'))
reject('missing restored evidence',lambda:p.resolve('missing-evidence'))
row=json.loads(T.read_text())['files'][0]
known=next(x for x in json.loads(T.read_text())['files'] if x['path']=='sources/catalogue_L071.pdf')
p.verify_pin({'path':'sources/catalogue_L071.pdf','sha256':known['sha256'],'bytes':known['bytes']})
reject('changed documentary hash',lambda:p.verify_pin({'path':'sources/catalogue_L071.pdf','sha256':'0'*64,'bytes':known['bytes']}))
reject('changed documentary size',lambda:p.verify_pin({'path':'sources/catalogue_L071.pdf','sha256':known['sha256'],'bytes':known['bytes']+1}))
f=REST/'study/corpus106_L071_Co3_v1/manifest.json';assert p.resolve('/Users/sasha/medusa/research/leemans/corpus106_L071_Co3_v1/manifest.json')==f
reject('changed restored pin',lambda:p.verify_pin({'path':str(f),'sha256':'0'*64}))
result=subprocess.run([sys.executable,'-O',str(C/'check.py'),'--repo',str(S.parents[1]/'math_compression'),'--payload',str(T.parents[4]),'--out',str(W/'optimized_should_not_exist')],capture_output=True)
assert result.returncode!=0 and b'run without Python optimization' in result.stderr and not (W/'optimized_should_not_exist').exists();done.append('optimized Python rejected before restoring')
meta=json.loads((C/'porting.json').read_text());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for e in meta['adaptations']:
 assert h(S/e['original'])==e['original_sha256'] and h(C/e['file'])==e['sha256']
 delta=''.join(difflib.unified_diff((S/e['original']).read_text().splitlines(keepends=True),(C/e['file']).read_text().splitlines(keepends=True),fromfile=e['original'],tofile=e['file']))
 assert delta==(C/(e['file']+'.diff')).read_text()
report={'status':'PASS_OPERATIONAL_NEGATIVE_CONTROLS','rejected':done,'legacy_private_path_remapped_to_public_restoration':True,'all_four_declared_diffs_exact':True,'code_sha256':{f.name:h(f) for f in sorted(C.glob('*.py'))},'transport_sha256':h(T)}
(W/'controls_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
