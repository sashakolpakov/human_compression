from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L033_hyperbolic_names_distinct';A=S/'corpus106_L033_hyperbolic_names_v1';P=S/'corpus106_L033_hyperbolic_names_independent_review';AH='cf5c11147ecd166866bd4086694e4cead3cfeb25dc7c0a2628034df522de0a0f';STATUS='ACCEPTED_L033_HYPERBOLIC_NAMES_COMPONENT_V1'
def need(b,m):
 if not b:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p):
 p=p.resolve();return dict(namespace='study'if p.is_relative_to(S)else'absolute',path=str(p.relative_to(S))if p.is_relative_to(S)else str(p),bytes=p.stat().st_size,sha256=sha(p))
def resolve(r):
 p=Path(r['path'])
 if p.is_absolute():return p
 if r.get('namespace')=='absolute':return Path('/')/p
 need(r.get('namespace')=='study','namespace');return S/p
need(sha(A/'manifest.json')==AH,'exact author');need(not P.exists(),'immutable new destination')
fresh=json.loads((W/'fresh01/report.json').read_text());need(fresh['status']=='PASS_L033_TWENTY_TWO_GROUP_CERTIFICATES'and fresh['LINS_runs']==fresh['target_searches']==0,'complete bounded replay')
ind=json.loads((W/'independent02/receipt.json').read_text());need(ind['returncode']==0 and not(W/'independent02/stderr').read_bytes()and 'PASS_INDEPENDENT_GROUP_CERTIFICATES'in(W/'independent02/stdout').read_text(),'independent pass')
identity=[];old=S/'reboot_20261013/L033_work/hyperbolic_recovery_work/named_stage03'
for name in ['names.tex','source_map.json','selected_tuples.json','verify.g','check.py','direct.g','series.g','dot.g']:
 need((A/name).read_bytes()==(old/name).read_bytes(),'read edition exact');identity.append(dict(author=pin(A/name),read_stage=pin(old/name)))
dump(W/'read_edition_identity.json',identity)
shutil.copy2(S/'corpus106_L033_hyperbolic_core_independent_review/source14.png',W/'source14.png')
P.mkdir()
for p in sorted(W.rglob('*')):
 if p.is_file():dest=P/p.relative_to(W);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
deps={}
def add(p,r=None):
 p=p.resolve();x=pin(p)
 if r:need(all(x[k]==r[k]for k in ['bytes','sha256']),'exact input '+str(p))
 key=(x['namespace'],x['path']);need(key not in deps or deps[key]==x,'no rebinding');deps[key]=x
add(A/'manifest.json');m=json.loads((A/'manifest.json').read_text())
for r in m['exports']:add(A/r['path'],r)
for r in json.loads((A/'dependencies.json').read_text()):add(resolve(r),r)
for p in W.rglob('*'):
 if p.is_file():add(p)
for r in identity:add(resolve(r['read_stage']),r['read_stage'])
for rel in ['corpus106_L033_hyperbolic_core_v1/finite_core.tex','corpus106_L033_hyperbolic_core_independent_review/mathematical_read01.rst','corpus106_L033_hyperbolic_core_independent_review/stage02_read.rst','corpus106_L033_hyperbolic_core_independent_review/final_read.rst','corpus106_L033_hyperbolic_core_root_adoption/review.json','sources/catalogue_L033.pdf','sources/catalogue_L033.txt','reboot_20261013/L033_work/hyperbolic_recovery_work/named_handoff01.json']:
 add(S/rel)
dump(P/'dependencies.json',[deps[k]for k in sorted(deps)])
review=dict(status=STATUS,author_manifest=pin(A/'manifest.json'),author='publication_recovery',reviewer='l044_resume',roles='Root original quotient probe and reader earlier distinct core review acquired; no new proof or production contribution by this reviewer.',scope='Twenty-two actual positive named groups from the accepted core only; two earlier exclusions acquired, ninth diagram and whole source separate.',source_pages_directly_viewed=[13,14],native_pages_directly_viewed=[1,2,3],native_text_identical=True,fresh_session=16797,exports_checked=106,author_bindings_checked=752,positive_certificates=22,negative_certificates=5,source_join_damages=3,optimization_guards=2,independent_session=30873,independent=dict(binary_matrices=512,linear_permutations=168,kernel_elements=672,extraspecial_element_pairs=1024,actual_central_quotient_order=960,faithful_L16_rows=2),retained_software='Exact GAP constructor/homomorphism interfaces; no StructureDescription identification or new LINS run.',preserved_harness_failure='independent01 read-only Z and unbound-global warnings; exact minimal independent02 delta and complete clean success retained.',dependencies=len(deps),LINS_runs=0,census_runs=0,whole_original_credit=0,question_credit=0,measurement=None,new_Lean=0,root_adoption=False,public_writes=False,time_utc=datetime.now(timezone.utc).isoformat())
dump(P/'review.json',review)
exports=[dict(path=str(p.relative_to(P)),bytes=p.stat().st_size,sha256=sha(p))for p in sorted(P.rglob('*'))if p.is_file()]
dump(P/'manifest.json',dict(status=STATUS,exports=exports))
for r in exports:need(sha(P/r['path'])==r['sha256']and(P/r['path']).stat().st_size==r['bytes'],'final export')
for r in deps.values():need(pin(resolve(r))==r,'final dependency')
print(json.dumps(dict(status=STATUS,manifest=str(P/'manifest.json'),sha256=sha(P/'manifest.json'),exports=len(exports),dependencies=len(deps)),indent=2))
