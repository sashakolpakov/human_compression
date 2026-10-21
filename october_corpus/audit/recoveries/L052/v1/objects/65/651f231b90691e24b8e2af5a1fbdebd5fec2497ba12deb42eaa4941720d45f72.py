"""Replay the exact finite L052 component; no source classification search."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, ast, copy, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')

def run(argv, out, name, timeout=120, success=True, env=None):
    start = time.monotonic()
    clean = os.environ.copy()
    clean.pop('PYTHONOPTIMIZE', None)
    clean['PYTHONDONTWRITEBYTECODE'] = '1'
    if env:
        clean.update(env)
    try:
        r = subprocess.run([str(x) for x in argv], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, env=clean)
    except subprocess.TimeoutExpired as e:
        (out/(name+'.stdout')).write_bytes(e.stdout or b'')
        (out/(name+'.stderr')).write_bytes(e.stderr or b'')
        save(out/(name+'.receipt.json'), {'status':'TIMEOUT', 'seconds':timeout})
        raise
    (out/(name+'.stdout')).write_bytes(r.stdout)
    (out/(name+'.stderr')).write_bytes(r.stderr)
    save(out/(name+'.receipt.json'), {'argv':list(map(str, argv)), 'returncode':r.returncode,
         'seconds':time.monotonic()-start})
    if success:
        need(r.returncode == 0 and not r.stderr.strip(), name+' clean success')
    else:
        need(r.returncode != 0, name+' rejection')
    return r.stdout.decode(), r.stderr.decode()

def gapvalue(text, key):
    lines = [s[len(key)+1:] for s in text.splitlines() if s.startswith(key+' ')]
    need(len(lines)==1, 'unique GAP receipt '+key)
    return ast.literal_eval(lines[0])

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--study',type=Path,required=True)
    p.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'))
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--render',action='store_true')
    a=p.parse_args(); base=Path(__file__).resolve().parent
    need(a.out.is_absolute() and not a.out.exists(), 'fresh absolute output directory')
    a.out.mkdir(parents=True)
    manifest=json.loads((base/'manifest.json').read_text())
    for b in manifest['exports']:
        q=base/b['path']; need(q.stat().st_size==b['bytes'] and digest(q)==b['sha256'],'export '+b['path'])
    deps=json.loads((base/'dependencies.json').read_text())
    roots={'study':a.study,'public':a.public_root}
    for b in deps:
        q=roots[b['namespace']]/b['path']
        need(q.stat().st_size==b['bytes'] and digest(q)==b['sha256'],'dependency '+b['path'])
    data=json.loads((base/'literal_inputs.json').read_text())
    rows=data['tables']; findings=[]
    run([sys.executable,base/'input_links.py','--out',a.out/'input_links.json'],a.out,'input_links')
    for row in rows:
        d=a.out/row['id']; d.mkdir()
        engine=base/('table1_engine.g' if row['id'].startswith('T1.') else 'table2_engine.g')
        regular=row['status']=='regular'
        driver='L003Input:=rec(id:='+json.dumps(row['id'])+',p:='+str(row['p'])+',a:='+str(row['a'])+',b:='+str(row['b'])+',expected_rotation_order:='+str(row['rotation_order'])+',regular:='+str(regular).lower()+',coset_limit:=1000000);;\nRead('+json.dumps(str(engine))+');\nQUIT;\n'
        (d/'run.g').write_text(driver)
        stdout,_=run([a.gap,'-q','-T',d/'run.g'],d,'run',60)
        need(stdout.splitlines()[-1]=='PASS_L052_ROW '+row['id'],'complete row')
        need(gapvalue(stdout,'ROTATION_ORDER')==row['rotation_order'],'exact presented order')
        need(gapvalue(stdout,'FULL_ORDER')==row['printed_g'],'full automorphism order')
        need(gapvalue(stdout,'ICPLUS_SUBGROUP_ORDERS')==row['icplus_orders'],'literal subgroup correspondence')
        need(gapvalue(stdout,'ICPLUS_PAIRS')==256 and gapvalue(stdout,'RANK3_GENERATION')==4,'complete tests')
        flags=gapvalue(stdout,'ROTATION_FLAGS'); residues=gapvalue(stdout,'RANK2_RESIDUES')
        need(len(flags)==16 and all(x[2]==x[3] for x in flags),'actual flag counts')
        need(len(residues)==6 and all(x[2]==2*x[1] for x in residues),'actual connected residues')
        need(gapvalue(stdout,'INVERTED_RELATOR_FAILURES')==([] if regular else [7]),'all-relator inversion')
        if regular:
            need(gapvalue(stdout,'FULL_IP_PAIRS')==256 and len(gapvalue(stdout,'FULL_FLAGS'))==16,'regular completion')
        findings.append({'id':row['id'],'order':row['printed_g'],'status':row['status']})
    # These scripts contain the frozen literal groups, not paths to author runs.
    for script,marker in [('examples.g','PASS_EXAMPLES'),('structures.g','PASS_NAMED_MODELS'),('relationships.g','PASS_RELATIONSHIPS')]:
        stdout,_=run([a.gap,'-q','-T',base/script],a.out,script[:-2],120)
        need(stdout.splitlines()[-1]==marker,'complete '+script)
        if script=='relationships.g':
            need(stdout.count('ROTATION_HALVING ')==11,'all eleven marked halving maps')
            need(stdout.count('SPLIT_FULL_HALVING ')+stdout.count('SPLIT_CHIRAL_HALVING ')==11,'all eleven complements')
        if script=='structures.g':
            need('NOT_DIRECT_A5_S4 [ 60, 12, 24 ]' in stdout,'characteristic invariant')
    run([sys.executable,base/'literal.py','--input',base/'literal_inputs.json','--out',a.out/'literal.json'],a.out,'literal')
    literal=json.loads((a.out/'literal.json').read_text())
    need(literal['subset_pairs']==6464,'all independent literal intersections')
    controls=[]
    for label in ['missing_row','duplicate_row','bad_permutation','false_order','false_subgroup_order','bad_example']:
        bad=copy.deepcopy(data)
        if label=='missing_row': bad['tables'].pop()
        elif label=='duplicate_row': bad['tables'][1]=bad['tables'][0]
        elif label=='bad_permutation': bad['tables'][0]['rotation'][0][0]=0
        elif label=='false_order': bad['tables'][0]['rotation_order']+=1
        elif label=='false_subgroup_order': bad['tables'][0]['icplus_orders'][3]+=1
        else: bad['examples'][0]['order']+=1
        f=a.out/(label+'.json'); save(f,bad)
        run([sys.executable,base/'literal.py','--input',f,'--out',a.out/(label+'_unexpected.json')],a.out,label,success=False)
        controls.append(label)
    for script in ['check.py','literal.py','input_links.py']:
        for mode in ['argument','environment']:
            cmd=[sys.executable]+(['-O'] if mode=='argument' else [])+[base/script,'--help']
            run(cmd,a.out,script[:-3]+'_guard_'+mode,success=False,env={'PYTHONOPTIMIZE':'1'} if mode=='environment' else None)
    pages=None
    if a.render:
        native=a.out/'native';native.mkdir()
        for i in range(2):
            run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(native),base/'finite.tex'],a.out,'latex'+str(i))
        log=(native/'finite.log').read_text()
        need(not any(x in log for x in ['Overfull','Underfull','undefined references','undefined citations']),'clean final native output')
        from pypdf import PdfReader
        doc=PdfReader(native/'finite.pdf')
        (native/'finite.txt').write_text('\f'.join(page.extract_text() or '' for page in doc.pages))
        if (base/'native/finite.txt').exists():
            need((native/'finite.txt').read_bytes()==(base/'native/finite.txt').read_bytes(),'same frozen native text')
        run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r90','-sOutputFile='+str(native/'page-%02d.png'),native/'finite.pdf'],a.out,'native_raster')
        pages=len(list(native.glob('page-*.png')))
    report={'status':'PASS_L052_FINITE','exports':len(manifest['exports']),'bindings':len(deps),'tables':findings,'examples':3,'literal_subset_pairs':6464,'damaged_inputs':controls,'optimization_guards':6,'native_pages':pages,'whole_original_credit':0,'new_question_credit':0}
    save(a.out/'report.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='tables'}))

if __name__=='__main__':
    main()
