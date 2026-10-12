#!/usr/bin/env python3
"""Exact bounded replay; no study source, GAP catalogue or prior outputs needed."""
from pathlib import Path
import argparse,copy,hashlib,json,os,re,subprocess,sys,time
sys.dont_write_bytecode=True
import countermodel as C
from finite_models import audit,ensure
HERE=Path(__file__).resolve().parent
DECLS=['base_relations','modified_power_two','modified_power_four','bd_square_ne_one',
       'not_universal_power_two_consequence','not_universal_power_four_consequence']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_gap(s):
    ensure('GAP_VERSION 4.15.1' in s and 'PASS_EXACT_SOURCE_SECTION5' in s,'GAP completion/version')
    rows=re.findall(r'CASE (\d+) original=(\d+) modified=(\d+) parabolics=\[([^]]+)\] marked_toroids=PASS IP=256 localHelly=4 globalHelly=4 coverdegree=3',s)
    ensure(len(rows)==2,'two complete GAP cases')
    for row,n in zip(rows,[3,6]):
        t=n//3
        ensure([int(x) for x in row[:3]]==[n,720*t**6,720*t**6],'actual fp group orders')
        ensure([int(x) for x in row[3].split(',')]==[36*t*t,48,36,48],'ordered fp parabolics')
    return {'exact_abstract_cases':2,'all_marked_torus_isomorphisms':8,'marked_source_coverings':2}
def run(argv,cwd,out,stem,timeout=120,env=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,text=True,capture_output=True,timeout=timeout,env=env)
    (out/(stem+'.stdout')).write_text(p.stdout);(out/(stem+'.stderr')).write_text(p.stderr)
    return p
def formal(ns,out):
    dep=json.loads((HERE/'formal/dependency_manifest.json').read_text()); env=dict(os.environ)
    pins=[]
    for x in dep['packages']:
        p=ns.package_root/x['name']
        rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True).strip()
        ensure(rev==x['rev'],'package revision '+x['name'])
        dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=p,text=True)
        ensure(not dirty.strip(),'dirty package source '+x['name']);pins.append({'name':x['name'],'revision':rev})
    env['LEAN_PATH']=os.pathsep.join(str(ns.package_root/x['name']/'.lake/build/lib/lean') for x in dep['packages'])
    env['ELAN_TOOLCHAIN']=dep['lean']
    version=subprocess.check_output([ns.lean,'--version'],env=env,text=True);ensure('4.32.2' in version,'Lean version')
    src=(HERE/'formal/SectionFive.lean').read_text()
    body=re.sub(r'/\-.*?\-/','',src,flags=re.S)
    ensure(not re.search(r'\b(sorry|axiom|native_decide|admit)\b',body),'forbidden proof shortcut')
    p=run([ns.lean,'-o',out/'SectionFive.olean',HERE/'formal/SectionFive.lean'],HERE,out,'lean',env=env)
    ensure(p.returncode==0 and not p.stderr.strip(),'fresh scoped Lean compile')
    reports=re.findall(r"'L121SectionFive\.([^']+)' depends on axioms: \[([^]]*)\]",p.stdout)
    ensure([x[0] for x in reports]==DECLS,'all six actual declarations')
    ensure(all(set(x.strip() for x in row.split(','))<={'propext','Classical.choice','Quot.sound'} for _,row in reports),'Lean axiom scope')
    bad=out/'FalseConsequence.lean';bad.write_text(src+'\nexample : (L121SectionFive.b*L121SectionFive.d)^2 = 1 := by decide\n')
    q=run([ns.lean,bad],HERE,out,'lean_negative',env=env)
    ensure(q.returncode!=0 and 'decide' in q.stdout,'false printed consequence rejected by Lean')
    return {'declarations':DECLS,'axioms':reports,'packages':pins,'compiled_libraries_trusted':True,'negative_control':'false_bd_square_identity_rejected'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--formal',action='store_true')
    ap.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    ap.add_argument('--package-root',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    ns=ap.parse_args();ns.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    if (HERE/'manifest.json').exists():
        for row in json.loads((HERE/'manifest.json').read_text())['exports']:
            p=HERE/row['path'];ensure(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen export '+row['path'])
    if ns.study_root:
        for row in json.loads((HERE/'scope.json').read_text())['retained_bindings']:
            p=ns.study_root/row['path'];ensure(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'exact source '+row['path'])
    data=json.loads((HERE/'model_data.json').read_text());counter=C.audit();finite=audit(data)
    p=run([ns.gap,'-q','-T',HERE/'exact_groups.g'],HERE,ns.out,'gap')
    ensure(p.returncode==0 and not p.stderr.strip(),'exact GAP replay diagnostics')
    exact=validate_gap(p.stdout);controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,IndexError,KeyError,TypeError):controls.append(name);return
        raise ValueError('bad control accepted: '+name)
    reject('printed_order240_rejected',lambda:validate_gap(p.stdout.replace('original=720','original=240')))
    reject('unmarked_residue_permutation_rejected',lambda:validate_gap(p.stdout.replace('[ 36, 48, 36, 48 ]','[ 48, 36, 36, 48 ]')))
    reject('missing_larger_case_rejected',lambda:validate_gap(p.stdout.split('CASE 6')[0]+'GAP_VERSION 4.15.1\nPASS_EXACT_SOURCE_SECTION5'))
    x=copy.deepcopy(data);x['models'].pop();reject('omitted_case_data_rejected',lambda:audit(x))
    x=copy.deepcopy(data);x['models'][0]['generators'][3]=x['models'][0]['generators'][2];reject('collapsed_marking_rejected',lambda:audit(x))
    old=C.MOD
    try:
        C.MOD=C.ORIG;reject('restored_final_d_not_literal_replacement',C.audit)
    finally:C.MOD=old
    old=C.G[3]
    try:
        C.G[3]=C.I;reject('lost_countermodel_generator',C.audit)
    finally:C.G[3]=old
    report={'status':'PASS','countermodel':counter,'finite_images':finite,'abstract_presentation':exact,
            'controls':controls,'source_bindings_checked':bool(ns.study_root),'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    if ns.formal:report['formal']=formal(ns,ns.out)
    if ns.render:
        from pypdf import PdfReader
        work=ns.out/'render';work.mkdir()
        for i in [1,2]:
            p=run([ns.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(work),HERE/'section5.tex'],HERE,work,f'pass{i}')
            ensure(p.returncode==0,'TeX compilation')
        log=(work/'section5.log').read_text();bad=[x for x in log.splitlines() if 'Overfull' in x or 'LaTeX Warning:' in x]
        ensure(not bad,'TeX diagnostics '+str(bad))
        a=[p.extract_text() for p in PdfReader(work/'section5.pdf').pages];b=[p.extract_text() for p in PdfReader(HERE/'section5.pdf').pages]
        ensure(a==b,'all PDF page texts reproduced');report['render']={'pages':len(a),'all_page_texts_equal':True,'diagnostics':bad}
    report['seconds']=round(time.monotonic()-start,3);(ns.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':report['seconds'],'controls':len(controls),'formal':bool(ns.formal)}))
if __name__=='__main__':main()
