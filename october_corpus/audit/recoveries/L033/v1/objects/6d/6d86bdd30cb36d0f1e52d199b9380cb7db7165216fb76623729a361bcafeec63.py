"""Reproduce a divisor-restricted normal quotient census and its literal obstruction."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode = True
import argparse, copy, hashlib, importlib.util, json, subprocess, time
from pathlib import Path

P = Path(__file__).resolve().parent
S = P.parents[2]
METHOD = S/'corpus106_L033_coxeter_lins_methods_v1'
CORE = S/'corpus106_L033_hyperbolic_core_v1'
GAP = ['/opt/homebrew/bin/gap', '-q', '-b']
M = [[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]]

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    return json.loads(Path(path).read_text())

def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2)+'\n')

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return dict(path=str(path),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def exact(row):
    need(pin(row['path']) == row, 'unchanged binding '+row['path'])

def frozen():
    if not (P/'manifest.json').exists():
        return None
    manifest = read(P/'manifest.json')
    for row in manifest['exports']:
        actual = pin(P/row['path'])
        need(all(actual[k] == row[k] for k in ['bytes','sha256']), 'frozen export '+row['path'])
    return manifest

def call(out, name, command, inputs, cap=60, expected_error=None, census=False):
    directory = out/name
    directory.mkdir()
    rows = [pin(p) for p in sorted(set(map(str,inputs)))]
    save(directory/'inputs.json',rows)
    start = time.monotonic()
    with (directory/'stdout').open('wb') as so, (directory/'stderr').open('wb') as se:
        try:
            run = subprocess.run(command,stdin=subprocess.DEVNULL,stdout=so,stderr=se,timeout=cap)
        except subprocess.TimeoutExpired:
            save(directory/'receipt.json',dict(status='TIMEOUT_NO_CREDIT',cap_seconds=cap,seconds=time.monotonic()-start,command=command,target_census=census))
            raise
    for row in rows:
        exact(row)
    stderr = (directory/'stderr').read_text()
    stdout = (directory/'stdout').read_text()
    passed = run.returncode == 0 and not stderr
    if expected_error is not None:
        passed = expected_error in stderr and 'INVALID_ACCEPTED' not in stdout
    receipt = dict(status='PASS' if passed else 'FAILED_NO_CREDIT',command=command,returncode=run.returncode,
                   cap_seconds=cap,seconds=time.monotonic()-start,inputs_unchanged=True,
                   target_census=census,scope='Exact target9720 divisor census' if census else 'Finite validation',
                   expected_error=expected_error,whole_original_credit=0)
    save(directory/'receipt.json',receipt)
    need(passed,'finite command '+name)
    return stdout

def gap_driver(out, name, text):
    path = out/(name+'.g')
    path.write_text('SizeScreen([1000000,24]);;\n'+text+'\nQUIT_GAP(0);\n')
    return path

def load(path):
    return 'Read('+json.dumps(str(path))+');;\n'

def central_words(row):
    """Direct word evaluation; no group closure or acquired checker used."""
    gs = [[x-1 for x in g] for g in row['permutations']]
    d = len(gs[0])
    identity = list(range(d))
    def multiply(a,b):
        return [b[a[i]] for i in range(d)]
    def word(generators):
        x = identity[:]
        for g in generators:
            x = multiply(x,g)
        return x
    words = []
    for omitted in range(4):
        w = word([gs[i] for i in range(4) if i != omitted])
        words.append(word([w]*5))
    z = words[0]
    need(all(w == z for w in words),'four equal parabolic words')
    need(z != identity and multiply(z,z) == identity,'nonidentity involution')
    need(all(multiply(z,g) == multiply(g,z) for g in gs),'central involution')
    return dict(all_four_equal=True,order=2,central=True,literal=[x+1 for x in z])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--render',action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    need(not out.exists(),'fresh output')
    before = frozen()
    dependencies = read(P/'dependencies.json')
    for row in dependencies:
        exact(row)
    out.mkdir()
    runtime = [Path('/opt/homebrew/bin/gap'),Path('/opt/homebrew/Cellar/gap/4.15.1/bin/gap')]
    methods = [METHOD/'coxeter_seeds.g',METHOD/'composed_pmodules.g']
    common = methods+[P/'divisor_options.g']+runtime
    controls = call(out,'controls',GAP+[str(P/'controls.g')],common+[P/'controls.g'])
    need('COMPLETE_DIVISOR_CONTROLS 26 132' in controls,'all26 actual-kernel controls')
    prefix = 'LoadPackage("LINS");;\n'+''.join(load(p) for p in methods+[P/'divisor_options.g'])
    M3 = '[[1,2,2],[2,1,2],[2,2,1]]'
    errors = []
    for label,body,fragment in [
        ('zero_target','CoxeterDivisorOptions('+M3+',0);;','admitted positive target index'),
        ('negative_target','CoxeterDivisorOptions('+M3+',-1);;','admitted positive target index'),
        ('beyond_table','CoxeterDivisorOptions('+M3+',LINS_MaxIndex+1);;','admitted positive target index'),
        ('wrong_bound','F:=FreeGroup(3);;x:=GeneratorsOfGroup(F);;W:=F/Concatenation(List(x,g->g^2),[(x[1]*x[2])^2,(x[1]*x[3])^2,(x[2]*x[3])^2]);;LowIndexNormalSubgroupsSearch(W,1,CoxeterDivisorOptions('+M3+',2));;','fixed divisor bound identity')]:
        path = gap_driver(out,label,prefix+body+'\nPrint("INVALID_ACCEPTED\\n");;')
        call(out,label,GAP+[str(path)],common+[path],expected_error=fragment)
        errors.append(label)
    path = gap_driver(out,'ancestor_control',prefix+'''
F:=FreeGroup(3);;x:=GeneratorsOfGroup(F);;
W:=F/Concatenation(List(x,g->g^2),[(x[1]*x[2])^2,(x[1]*x[3])^2,(x[2]*x[3])^2]);;
good:=List(LowIndexNormalSubgroupsSearch(W,8,CoxeterDivisorOptions('''+M3+''',8)));;
opt:=CoxeterDivisorOptions('''+M3+''',8);;opt.DoCut:=function(gr,H)return Index(H)<>8;end;;
bad:=List(LowIndexNormalSubgroupsSearch(W,8,opt));;
if Number(good,H->Index(H)=8)<>1 or Number(bad,H->Index(H)=8)<>0 then Error("incorrect equality cut must lose target kernel");fi;
Print("ANCESTOR_CONTROL 1 0\\n");;
''')
    need('ANCESTOR_CONTROL 1 0' in call(out,'ancestor_control',GAP+[str(path)],common+[path]),'ancestor necessity')
    target_path = gap_driver(out,'target','OUTPUT_DIR:='+json.dumps(str(out/'target'))+';;\n'+load(P/'target.g'))
    target = call(out,'target',GAP+[str(target_path)],common+[target_path,P/'target.g',METHOD/'enumerate_changed.g'],census=True)
    need('DIVISOR_INDEX_MULTIPLICITIES [ [ 1, 1 ], [ 2, 1 ], [ 60, 1 ], [ 120, 1 ], [ 4860, 1 ], [ 9720, 1 ] ]' in target,'complete divisor node roster')
    need('COMPLETE_DIVISOR_TARGET 9720 NODES 6 EXACT 1' in target,'complete exact-target enumeration')
    comparison = gap_driver(out,'comparison',load(METHOD/'compare_markings.g')+load(out/'target/records.g')+'fresh:=divisor_records;;\n'+load(P/'records.g')+'''
old:=divisor_records;;
if OrderedMarkingBijection(fresh,old)=fail then Error("actual ordered quotient isomorphism");fi;
if OrderedMarkingBijection(fresh,Concatenation(old,old))<>fail then Error("wrong multiplicity accepted");fi;
bad:=StructuralCopy(old[1]);;bad.permutations[1]:=bad.permutations[2];;
if SameOrderedMarking(old[1],bad) then Error("wrong marking accepted");fi;
Print("LITERAL_TARGET ",List(fresh,r->[r.node,r.order,r.permutations]),"\\n");;
Print("COMPLETE_MARKED_COMPARISON 1 2\\n");;
''')
    bridge = call(out,'comparison',GAP+[str(comparison)],runtime+[comparison,METHOD/'compare_markings.g',out/'target/records.g',P/'records.g'])
    need('COMPLETE_MARKED_COMPARISON 1 2' in bridge,'marked comparison')
    lines = [line.removeprefix('LITERAL_TARGET ') for line in bridge.splitlines() if line.startswith('LITERAL_TARGET ')]
    need(len(lines)==1,'one complete literal bridge')
    values = json.loads(lines[0])
    need(len(values)==1,'one exact quotient')
    rows = [dict(type='3535',node=n,order=o,permutations=perms,matrix=M,expected_reject=True) for n,o,perms in values]
    save(out/'negative.json',rows)
    spec = importlib.util.spec_from_file_location('literal',CORE/'literal.py')
    literal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(literal)
    row = rows[0]
    result = literal.validate(row,M)
    need(result['local_orders']==[120]*4 and len(result['intersection_failures'])==12,'literal obstruction and exact locals')
    need([7,11,12,6] in result['intersection_failures'],'displayed intersection obstruction')
    central = central_words(row)
    recorded = read(P/'negative.json')
    need(len(recorded)==1 and literal.validate(recorded[0],M)==result,'recorded complete literal report')
    need(central_words(recorded[0])==read(P/'central.json'),'recorded central word')
    damages = []
    for label,change,fragment in [
        ('bad_order',lambda r:r.update(order=4860),'group order'),
        ('bad_permutation',lambda r:r['permutations'][0].__setitem__(0,r['permutations'][0][1]),'malformed permutations'),
        ('bad_mark',lambda r:r['permutations'].__setitem__(0,r['permutations'][1]),'pair matrix')]:
        bad = copy.deepcopy(row)
        change(bad)
        try:
            literal.validate(bad,M)
        except ValueError as error:
            need(fragment in str(error),'specific literal guard')
            damages.append(label)
        else:
            raise ValueError('literal damage accepted '+label)
    bad = copy.deepcopy(row)
    bad['permutations'][0] = list(range(1,28))
    try:
        central_words(bad)
    except ValueError:
        damages.append('wrong_central_word')
    else:
        raise ValueError('central word damage accepted')
    save(out/'literal.json',result)
    save(out/'central.json',central)
    pages = None
    if args.render:
        native = out/'native'
        native.mkdir()
        for i in [1,2]:
            call(out,'tex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(native),str(P/'quotients.tex')],[P/'quotients.tex'],30)
        need(not any(x in (native/'quotients.log').read_text() for x in ['Warning','Overfull','Underfull']),'clean native layout')
        from pypdf import PdfReader
        pdf = PdfReader(native/'quotients.pdf')
        pages = len(pdf.pages)
        if (P/'quotients.pdf').exists():
            need([p.extract_text() for p in pdf.pages]==[p.extract_text() for p in PdfReader(P/'quotients.pdf').pages],'same native proof text')
        call(out,'raster',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'quotients.pdf')],[native/'quotients.pdf'],30)
    for binding in dependencies:
        exact(binding)
    need(frozen()==before,'unchanged frozen component')
    report = dict(status='PASS_DIVISOR_TARGET9720',control_targets=26,actual_kernel_comparisons=132,
                  exact_target=9720,retained_normal_kernels=6,exact_target_kernels=1,intersection_failures=12,
                  central_obstruction=central,input_guards=errors,literal_damages=damages,marked_damages=2,
                  necessary_ancestor_control=[1,0],native_pages=pages,whole_original_credit=0,
                  new_question_credit=0,new_Lean=0,measurement=None,classification_premises_retained=True)
    save(out/'report.json',report)
    print(json.dumps(report))

if __name__=='__main__':
    main()
