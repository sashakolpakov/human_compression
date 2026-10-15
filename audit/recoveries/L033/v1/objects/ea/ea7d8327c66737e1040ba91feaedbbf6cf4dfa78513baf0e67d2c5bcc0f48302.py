import sys
if sys.flags.optimize:
    raise SystemExit('optimized execution unsupported')
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,json,os,pathlib,re,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parent
def need(v,m):
    if not v: raise ValueError(m)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_pin(row,base):
    p=base/row['path'];need(p.is_file(),'missing input '+str(p))
    need(p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'damaged input '+str(p))
def run(cmd,out,seconds=120):
    out.mkdir(parents=True,exist_ok=False);start=time.monotonic();env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with (out/'stdout').open('wb') as so,(out/'stderr').open('wb') as se:
        try:r=subprocess.run(cmd,stdout=so,stderr=se,env=env,timeout=seconds)
        except subprocess.TimeoutExpired:
            (out/'timeout.json').write_text(json.dumps({'seconds':time.monotonic()-start,'status':'TIMEOUT_NO_CERTIFICATE'}));raise
    need(r.returncode==0,'child failure '+str(out));text=(out/'stdout').read_text();err=(out/'stderr').read_text()
    need(not err.strip() and not any(w in text for w in ['Syntax warning','Error,','Error:']),'unclean child '+str(out))
    return text
def census_summary(text):
    m=re.search(r'INDEX_MULTIPLICITIES (.*?)\nACCEPTED ',text,re.S);need(m,'missing index inventory')
    return json.loads(m.group(1))
def execution_aliases():
    aliases=json.loads((ROOT/'execution_aliases.json').read_text()); checked=0
    for typ in json.loads((ROOT/'source_map.json').read_text())['types']:
        receipt=json.loads((ROOT/'censuses'/typ/'report.json').read_text())
        need(receipt['returncode']==0 and receipt['command'][-1]==receipt['inputs'][2]['path'],'wrong execution closure')
        for kind in ['inputs','outputs']:
            for row in receipt[kind]:
                key=typ+':'+kind+':'+row['path']
                need(key in aliases,'missing execution alias '+key)
                target=aliases[key]
                need(target['sha256']==row['sha256'] and target['bytes']==row['bytes'],'changed historical execution pin')
                verify_pin(target,ROOT);checked+=1
    need(checked==len(aliases),'extra execution alias');return checked

def controls():
    spec=importlib.util.spec_from_file_location('literal_core',ROOT/'literal.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    rows=json.loads((ROOT/'positives.json').read_text());row=rows[0];M=json.loads((ROOT/'source_map.json').read_text())['types'][row['type']]['matrix'];total=0
    probes=[]
    q=copy.deepcopy(row);q['order']+=1;probes.append((q,M))
    q=copy.deepcopy(row);q['permutations'][0][0]=0;probes.append((q,M))
    q=copy.deepcopy(row);q['permutations'][1]=q['permutations'][0];probes.append((q,M))
    q=copy.deepcopy(row);q['permutations'].pop();probes.append((q,M))
    mm=copy.deepcopy(M);mm[0][1]=mm[1][0]=7;probes.append((row,mm))
    for q,m in probes:
        try:r=mod.validate(q,m)
        except (ValueError,IndexError):total+=1;continue
        need(r['intersection_failures'] or r['flag_failures'],'damaged positive accepted');total+=1
    need(total==5,'wrong control count');return total
def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--reuse-recorded-census',action='store_true');a=p.parse_args()
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for row in manifest['exports']:verify_pin(row,ROOT)
    deps=json.loads((ROOT/'dependencies.json').read_text())
    for row in deps:verify_pin(row,a.study if row.get('namespace')=='study' else pathlib.Path('/'))
    alias_count=execution_aliases()
    a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    source=json.loads((ROOT/'source_map.json').read_text());census_rows=[]
    for typ,data in source['types'].items():
        old=ROOT/'censuses'/typ;receipt=json.loads((old/'report.json').read_text())
        need(receipt['status']=='PASS' and receipt['bound']==data['bound'],'not a complete recorded census')
        text=(old/'stdout').read_text();need(f"COMPLETE_HYPERBOLIC_BOUND {data['bound']} " in text,'missing recorded completion')
        need(not (old/'stderr').read_text().strip(),'recorded stderr')
        need(sum(n for _,n in census_summary(text))==data['kernels'],'recorded kernel count')
        if not a.reuse_recorded_census:
            fresh=a.out/'censuses'/typ
            run([sys.executable,'-B',str(ROOT/'run_broad.py'),'--type',typ,'--out',str(fresh),'--seconds','120'],a.out/'census_wrappers'/typ,130)
            need(census_summary((fresh/'stdout').read_text())==census_summary(text),'new kernel index inventory differs')
            driver=a.out/('compare_'+typ+'.g')
            driver.write_text(f'Read({json.dumps(str(ROOT/"compare_markings.g"))});;\nCompareMarkedFiles({json.dumps(str(old/"records.g"))},{json.dumps(str(fresh/"records.g"))});;\nQUIT;\n')
            comparison=run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)],a.out/'comparisons'/typ,120)
            need(f"COMPLETE_MARKED_COMPARISON {data['positive_kernels']} 2 CONTROLS" in comparison,'incomplete marked comparison')
        census_rows.append({'type':typ,'bound':data['bound'],'kernels':data['kernels']})
    driver=a.out/'positive_driver.g';driver.write_text(f'Read({json.dumps(str(ROOT/"enumerate_broad.g"))});;\nRead({json.dumps(str(ROOT/"verify.g"))});;\nVerifyFiniteCore({json.dumps(str(ROOT))});;\nQUIT;\n')
    text=run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)],a.out/'fresh_gap',120);need('COMPLETE_FINITE_CORE 59' in text,'missing fresh positive closure')
    bridge=re.search(r'POSITIVE_RECORDS (.*?)\nCOMPLETE_FINITE_CORE',text,re.S);need(bridge,'missing literal input bridge')
    actual=json.loads(bridge.group(1));expected=[[r['type'],r['node'],r['order'],r['permutations']] for r in json.loads((ROOT/'positives.json').read_text())]
    need(sorted(actual)==sorted(expected),'literal input differs from GAP records')
    run([sys.executable,'-B',str(ROOT/'literal.py'),'--input',str(ROOT/'positives.json'),'--out',str(a.out/'literal_positive.json')],a.out/'literal_positive',120)
    run([sys.executable,'-B',str(ROOT/'literal.py'),'--input',str(ROOT/'negatives.json'),'--out',str(a.out/'literal_negative.json')],a.out/'literal_negative',30)
    damages=controls();guards=0
    for script in ['check.py','literal.py']:
        for envopt in [False,True]:
            target=a.out/(script+str(envopt));env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
            args=[sys.executable]
            if envopt:env['PYTHONOPTIMIZE']='1'
            else:args+=['-O']
            args += [str(ROOT/script),'--out',str(target)]
            r=subprocess.run(args,capture_output=True,text=True,env=env,timeout=10)
            need(r.returncode!=0 and 'optimized execution unsupported' in r.stderr and not target.exists(),'optimization guard');guards+=1
    pages=None
    if a.render:
        native=a.out/'native';native.mkdir();shutil.copyfile(ROOT/'finite_core.tex',native/'finite_core.tex')
        for i in [1,2]:
            cmd=['/Library/TeX/texbin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(native/'finite_core.tex')]
            run(cmd,a.out/('latex'+str(i)),60)
        log=(native/'finite_core.log').read_text();need('Overfull' not in log and 'undefined' not in log,'native warning')
        run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'finite_core.pdf')],a.out/'raster',60)
        pages=len(list(native.glob('page-*.png')))
    report={'status':'PASS','exports':len(manifest['exports']),'dependencies':len(deps),'execution_pins':alias_count,'censuses':census_rows,'fresh_census':not a.reuse_recorded_census,'positive_tuples':59,'negative_tuples':5,'damaged_controls':damages,'optimization_guards':guards,'native_pages':pages,'seconds':time.monotonic()-start,'whole_original_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if __name__=='__main__':main()
