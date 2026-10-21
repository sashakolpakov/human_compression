from pathlib import Path
import hashlib,json,shutil,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/psl2_rank_two';W=P/'overgroup_work';A=P/'overgroups'
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
if A.exists():raise ValueError('Fresh author edition required')
A.mkdir();(A/'native').mkdir()
for name in ['overgroups.tex','overgroups.pdf','finite_bounds.py','finite_bounds.json','reference.json']:
    shutil.copyfile(W/name,A/name)
for p in W.iterdir():
    if p.name.startswith('page-') or p.name in ['overgroups.tex','overgroups.pdf','overgroups.aux','overgroups.log','overgroups.fls','overgroups.out','compile04.stdout']:
        shutil.copyfile(p,A/'native'/p.name)
reader=(P/'cyclic_three/check.py').read_text()
reader=reader.replace("'pairs.tex'","'overgroups.tex'").replace("'pairs.pdf'","'overgroups.pdf'")
reader=reader.replace("'pairs.tex'","'overgroups.tex'").replace("len(actual) != 4","len(actual) != 6").replace("len(images) != 4","len(images) != 6")
reader=reader.replace("'-r105'","'-r100'").replace("native_pages=4","native_pages=6").replace("source_claim_groups=7","source_claim_groups=9")
reader=reader.replace('PASS_CYCLIC_THREE_EXACT_NATIVE_REPLAY','PASS_OVERGROUP_EXACT_NATIVE_REPLAY')
needle="    out.mkdir(parents=True)\n"
addition="""    out.mkdir(parents=True)
    arithmetic = subprocess.run([sys.executable, '-B', str(A/'finite_bounds.py'), '--out', str(out/'finite_bounds.json')], capture_output=True, timeout=10)
    if arithmetic.returncode or arithmetic.stderr or (out/'finite_bounds.json').read_bytes() != (A/'finite_bounds.json').read_bytes():
        raise ValueError('Finite order arithmetic differs')
"""
reader=reader.replace(needle,addition)
(A/'check.py').write_text(reader)
deps=set()
for line in (W/'overgroups.fls').read_text().splitlines():
    if line.startswith('INPUT '):
        p=Path(line[6:])
        if p.is_absolute() and p.is_file():deps.add(p.resolve())
for p in [W/'cameron_omidi_tayfeh_rezaie_2006.pdf',S/'sources/catalogue_L063.pdf',S/'sources/catalogue_L063.txt',S/'sources/catalogue_L064.pdf',S/'sources/catalogue_L064.txt',Path('/opt/homebrew/bin/pdflatex').resolve(),Path('/opt/homebrew/bin/gs').resolve(),Path(sys.executable).resolve(),Path(__file__)]:deps.add(p)
save(A/'dependencies.json',[dict(path=str(p),**pin(p))for p in sorted(deps)])
save(A/'scope.json',dict(status='AUTHOR_PROOF_REQUIRES_DISTINCT_REVIEW',author='root',sources=['L063','L064'],proof_pages=6,
 claims=['PSL2 two-transitive coset actions from the classical maximal subgroup list','PGL2 two-transitive coset actions from its simple normal subgroup','Elementary cyclic, dihedral and scalar affine quotient arguments','Small-intersection overgroups in nine stated parameter scopes'],
 borrowed=['Dickson, Moore and Suzuki subgroup types, field restrictions, normalizers and indicated class fusion','Classical exceptional isomorphisms and simplicity','Modern subgroup tables of Cameron, Omidi and Tayfeh-Rezaie, 2006'],
 whole_source_credit=0,conjecture_credit=0,lean_credit=0,compression_factor=None))
save(A/'manifest.json',dict(status='AUTHOR_L063_L064_COMMON_OVERGROUP_PROOF_PENDING_DISTINCT_REVIEW',exports=[dict(path=str(p.relative_to(A)),**pin(p))for p in sorted(A.rglob('*'))if p.is_file()]))
print(json.dumps(dict(path=str(A/'manifest.json'),**pin(A/'manifest.json'))))
