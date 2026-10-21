#!/usr/bin/env python3
"""Fail-closed replay of the TeX-first chiral enumeration package."""
import argparse,hashlib,json,os,pathlib,re,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE282_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(row):
    p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative binding')
    p=ROOT/p;need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'binding '+row['path'])
def span(row):
    p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe span path')
    b=b''.join((ROOT/p).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
    need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'proof span '+str(p))
def semantic(x):
    if isinstance(x,dict):return {k:semantic(v) for k,v in x.items() if k!='seconds'}
    if isinstance(x,list):return [semantic(v) for v in x]
    return x

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=pathlib.Path,required=True)
    ap.add_argument('--verify-primary',action='store_true');ap.add_argument('--xelatex',type=pathlib.Path);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output directory')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output directory');out.mkdir(parents=True)
    manifest=json.loads((ROOT/'phase282_manifest.json').read_bytes())
    need(not any(r['path'].endswith('.md') for r in manifest['exports']+manifest['retained_bindings']),'no Markdown publication or proof dependency')
    for row in manifest['exports']:bound(row)
    for row in manifest['retained_bindings']:
        if a.verify_primary or not row['path'].startswith('sources/'):bound(row)
    ledger=json.loads((ROOT/'phase282_source_ledger.json').read_bytes())
    need(len(ledger['rows'])==32 and len(ledger['proof_spans'])==12,'exact source contract dimensions')
    for row in ledger['proof_spans'].values():span(row)
    need(all(all(s in ledger['proof_spans'] for s in row['proof_spans']) for row in ledger['rows']),'valid ledger edges')
    proof=json.loads((ROOT/'phase282_proof_map.json').read_bytes())
    need(len(proof['written_theorems'])==9 and len(proof['lean_theorems'])==7,'theorem proof map dimensions')
    for row in list(proof['written_theorems'].values())+list(proof['lean_theorems'].values()):span(row)
    for row in proof['lean_theorems'].values():
        actual=''.join((ROOT/row['path']).read_text().splitlines(keepends=True)[row['start_line']-1:row['end_line']]).split(':= by')[0].rstrip()
        need(actual==row['statement'],'literal Lean statement map')
    scope=json.loads((ROOT/'phase282_scope.json').read_bytes());need(scope['principal_credit']==scope['question_credit']==0 and scope['compression_ratio'] is None,'no premature credit')
    executions=[]
    def run(label,args,env=None,timeout=240):
        t=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=out,env=env,capture_output=True,text=True,timeout=timeout)
        stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
        executions.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,4),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
        return p
    p=run('enumeration',[sys.executable,'-B','-O',ROOT/'phase282_enumerate.py','--out',out/'enumeration.json']);need(p.returncode==0,'full finite enumeration')
    enumeration=json.loads((out/'enumeration.json').read_bytes());expected=json.loads((ROOT/'phase282_expected_enumeration.json').read_bytes())
    need(semantic(enumeration)==semantic(expected),'exact enumeration semantic baseline')
    need(len(enumeration['models'])==11 and sum(len(x['witnesses']) for x in enumeration['models'].values())==18,'eleven groups and eighteen complete marking checks')
    p=run('table',[sys.executable,'-B','-O',ROOT/'phase282_table_counts.py','--out',out/'table.json']);need(p.returncode==0,'32 exact mathematical table rows')
    table=json.loads((out/'table.json').read_bytes());need(table==json.loads((ROOT/'phase282_exact_table.json').read_bytes()),'exact mathematical table baseline')
    p=run('involutions',[a.gap,'-q','-T',ROOT/'phase282_involution_check.g']);need(p.returncode==0 and 'PHASE282_ALL_TWENTY_COUNTS_PASS' in p.stdout and not re.search(r'Error|warning',p.stdout+p.stderr),'independent GAP involution classes')
    bykey={(r['family'],r['q']):r for r in table['rows']};rows=0
    for family,q,order,invol in re.findall(r'PHASE282_CLASSICAL_PASS (PSL|PSU) (\d+) order (\d+) involutions (\d+)',p.stdout):
        r=bykey[family+'3',int(q)];need(r['order']==int(order) and r['involutions']==int(invol),'classical cross-check');rows+=1
    for family,q,invol in re.findall(r'PHASE282_PERMUTATION_PASS (Alt|Sym) (\d+) involutions (\d+)',p.stdout):
        need(bykey[family,int(q)]['involutions']==int(invol),'permutation cross-check');rows+=1
    need(rows==20,'twenty independent table rows')
    for label,old,new in [('mirror_edge','mirrored[v^1][i]','mirrored[v][i]'),('mirror_count',"result['AGL1_5']['oriented_chiral']==2","result['AGL1_5']['oriented_chiral']==1")]:
        source=(ROOT/'phase282_enumerate.py').read_text();changed=source.replace(old,new);need(changed!=source,'mutation applied '+label)
        target=out/(label+'.py');target.write_text(changed);p=run('control_'+label,[sys.executable,'-B','-O',target,'--out',out/(label+'.json')]);need(p.returncode!=0 and 'PHASE282_REJECT' in p.stderr,'finite mutation rejected '+label)
    source=(ROOT/'phase282_involution_check.g').read_text();changed=source.replace('q^2*(q^2-q+1)','q^2*(q^2+q+1)');need(changed!=source,'unitary mutation applied')
    target=out/'bad_unitary.g';target.write_text(changed);p=run('control_unitary',[a.gap,'-q','-T',target]);need('PHASE282_REJECT' in p.stdout+p.stderr and 'PHASE282_ALL_TWENTY_COUNTS_PASS' not in p.stdout,'wrong unitary count rejected')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_bytes());deps=[]
    for row in pins['packages']:
        path=a.packages/row['name'];rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip();need(rev==row['rev'],'pinned dependency '+row['name'])
        need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'clean tracked dependency '+row['name']);deps.append(dict(name=row['name'],rev=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'pinned Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    source=(ROOT/'phase282_formal/PrefixCoordinates.lean').read_text();need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',source,re.M),'proof-hole scan')
    target=out/'PrefixCoordinates.lean';target.write_text(source);p=run('formal',[a.lean,'-o',target.with_suffix('.olean'),target],env=env)
    need(p.returncode==0 and not re.search(r'error:|warning:|sorryAx',p.stdout+p.stderr),'seven general Lean proofs')
    axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout)
    need(len(axioms)==7 and all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in axioms),'seven standard-only axiom reports')
    need({n.rsplit('.',1)[-1] for n,_ in axioms}==set(proof['lean_theorems']),'axiom statement binding')
    for label,old,new in [('missing_inverse','segment s i n = (prefixWord s i)⁻¹ * prefixWord s (i + n)','segment s i n = (prefixWord s i) * prefixWord s (i + n)'),('false_square','∀ x : G, f (f x) = x := by','∀ x : G, f (f x) = 1 := by')]:
        changed=source.replace(old,new);need(changed!=source,'formal mutation applied '+label)
        target=out/(label+'.lean');target.write_text(changed);p=run('control_'+label,[a.lean,target],env=env);need(p.returncode!=0 and 'error:' in p.stdout+p.stderr,'false formal conclusion rejected '+label)
    rendered={}
    if a.xelatex:
        for name,pages in [('phase282_marked_coordinate_umbrella',4),('phase282_chiral_enumeration',9)]:
            directory=out/name;directory.mkdir()
            for k in [1,2]:
                p=run(name+str(k),[a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',directory,ROOT/(name+'.tex')]);need(p.returncode==0,'direct TeX render '+name)
            log=(directory/(name+'.log')).read_text();need('Missing character' not in log and not re.search(r'Overfull|Undefined control sequence',log),'render glyph and box checks '+name)
            need(re.search(r'Output written on .*?\('+str(pages)+r' pages?[),]',log,re.S),'render page count '+name);rendered[name]=dict(pages=pages,pdf_sha256=sha(directory/(name+'.pdf')))
    report=dict(status='PASS',exports_checked=len(manifest['exports']),primary_checked=a.verify_primary,source_rows=32,section_spans=12,written_theorem_spans=9,lean_declarations=7,
        finite_groups=11,complete_flag_markings=18,table_rows=32,independent_GAP_rows=20,executions=executions,axioms=axioms,lean_version=version,dependencies=deps,rendered=rendered,
        controls=['altered mirror edge rejected','false mirror count rejected','wrong unitary count rejected','missing coordinate inverse rejected','false automorphism-square conclusion rejected','outer tetrahedral inversion retained','nonorientable A5 60 versus120 flags'],
        limits=scope['formal']['exclusions']+scope['formal']['trusted']+['Written uniform proof is not replaced by finite models.','Schulte–Weiss and Liebeck–Shalev inputs retained.','No original timing, sourcecount, question or compression ratio claim.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',report=str(out/'report.json'),groups=11,table_rows=32,lean=7)))
if __name__=='__main__':main()
