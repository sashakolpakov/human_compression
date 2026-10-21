"""Historical edition helper; build.py is the directory-local replay."""
from pathlib import Path
import hashlib,json,shutil,difflib,sys
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;s=w.parents[2];old=s/'topic_B_L019_orbit_budgets_v1';dest=s/'topic_B_L019_orbit_budgets_v2'
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if dest.exists():raise ValueError('Immutable destination exists')
a=(old/'orbit_budgets.tex').read_text();b=(w/'orbit_budgets.tex').read_text()
expected=a.replace('$a,b$ respectively. Every $\\rho_j$ with $|j-i|>1$ fixes\n$a,b$.','$a,b$ respectively. Under the string relations, every\n$\\rho_j$ with $|j-i|>1$ fixes $a,b$.')
if b!=expected or b==a:raise ValueError('Unexpected edition change')
shutil.copytree(old,dest)
(dest/'manifest.json').unlink()
for name in ['orbit_budgets.tex','orbit_budgets.pdf','build_receipts.json']+[f'build{i}.{ext}' for i in range(3) for ext in ['stdout','stderr']]:shutil.copy2(w/name,dest/name)
visual={'pages':3,'all_pages_directly_viewed':True,'result':'All three rebuilt pages are readable, with the sole hypothesis clarification visible in the introduction and no unresolved references.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]}
(dest/'visual_review.json').write_text(json.dumps(visual,indent=2)+'\n')
(dest/'edition_delta.json').write_text(json.dumps({'previous_manifest':pin(old/'manifest.json'),'requested_by':'/root/publication_recovery','sole_mathematical_text_change':'Qualify the introductory endpoint-fixing statement by Under the string relations.','unified_tex_diff':''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='v1/orbit_budgets.tex',tofile='v2/orbit_budgets.tex')),'unchanged':'All theorem statements and proofs, original dependencies, source attribution and scope; no mathematical computation exists to rerun.','rebuilt':'PDF, native receipts/stdout and direct visual review.','helper_notice':'freeze.py is retained unchanged as historical v1 helper. freeze_v2.py records this minimal immutable edition and is not a standalone replay interface.'},indent=2)+'\n')
shutil.copy2(w/'freeze_v2.py',dest/'freeze_v2.py')
exports=[]
for p in sorted(dest.iterdir()):
 d=pin(p);d['path']=p.name;exports.append(d)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_ORBIT_BUDGETS_V2','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n')
print(json.dumps(pin(dest/'manifest.json')))
