#!/usr/bin/env python3
"""Replay the principal PSL maniplex application and its explicit retained inputs."""
import argparse, hashlib, json, os, pathlib, re, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent

def need(b,msg):
    if not b:raise RuntimeError('PHASE258_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(row):
    p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'relative binding')
    p=ROOT/p;need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'binding '+row['path'])
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['out','gap','lean','packages']:ap.add_argument('--'+name,type=pathlib.Path,required=True)
    ap.add_argument('--verify-primary',action='store_true');a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
    m=json.loads((ROOT/'phase258_manifest.json').read_bytes())
    for row in m['exports']:bound(row)
    for row in m['retained_bindings']:
        if a.verify_primary or not row['path'].startswith('sources/'):bound(row)
    ledger=json.loads((ROOT/'phase258_source_ledger.json').read_bytes())
    need(len(ledger['rows'])==32 and len(ledger['proof_spans'])==9,'source ledger scope')
    for name,row in ledger['proof_spans'].items():
        data=b''.join((ROOT/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'proof span '+name)
    need(all(all(x in ledger['proof_spans'] for x in r['proof_spans']) for r in ledger['rows']),'ledger span references')
    for manifest,name in [('phase238_manifest.json','phase238_topic_E_umbrella.md'),('phase230_manifest.json','phase230_finite_check.g'),('phase237_manifest.json','phase237_formal/ProjectiveDihedralMatrices.lean')]:
        old=json.loads((ROOT/manifest).read_bytes());entry=next(r for r in old['exports'] if r['path']==name);bound(entry)
    reports=[]
    def run(label,args,env=None,timeout=240):
        start=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=out,env=env,text=True,capture_output=True,timeout=timeout)
        stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
        reports.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-start,4),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
        return p
    def gap(label,path,marker):
        p=run(label,[a.gap,'-q','-T',path]);need(p.returncode==0 and marker in p.stdout and not re.search(r'Error|warning',p.stdout+p.stderr),label);return p
    p=gap('local_sggi',ROOT/'phase258_local_sggi.g','PHASE258_LOCAL_PASS');flat=' '.join(p.stdout.split())
    need('SGGI_LOCAL 24 TOTAL 72 BAD_IP 0' in flat and 'SGGI_LOCAL 60 TOTAL 360 BAD_IP 0' in flat,'IP tested after complete generation census')
    need(all(x in p.stdout for x in ['SOURCE_L33_COUNTEREXAMPLE','DIHEDRAL_NON_C_SGGI_CONTROL','RANK_BOUND_NO_STRING_FALSE_WEAKENING']),'local mathematical controls')
    p=gap('families',ROOT/'phase258_family_check.g','PHASE258_FAMILY_PASS')
    need(p.stdout.count('CONSTANT_FAMILY ')==3 and p.stdout.count('PROPER_END_FAMILY ')==3 and
        'OMITTED_S4 PSL23 ORDER6072 FACETS253 VERTICES1' in p.stdout and 'SELFDUAL_CLASS1 PSL13 ORDER1092' in p.stdout
        and 'SOURCE_CONJUGACY_PASS' in p.stdout and 'ALTERED_REJECTED' in p.stdout
        and 'RANK_BOUND_ALLOW_IDENTITY_FALSE_WEAKENING' in p.stdout,'eight exact marked models and source adapters')
    p=gap('shared_ten_table',ROOT/'phase230_finite_check.g','PHASE230_FINITE_PASS')
    need(len(re.findall(r'ROW\s+\d+\s+ORDER',p.stdout))==10 and 'RANK3 24 MARKINGS 72' in p.stdout and 'RANK3 60 MARKINGS 360' in p.stdout,'complete retained finite table')
    changed=(ROOT/'phase258_family_check.g').read_text().replace('[[1,-2],[2,-1]]','[[1,-2],[2,1]]')
    need(changed!=(ROOT/'phase258_family_check.g').read_text(),'matrix mutation applied')
    bad=out/'bad_matrix.g';bad.write_text(changed);p=run('control_matrix',[a.gap,'-q','-T',bad])
    need('Error' in p.stdout+p.stderr and 'PHASE258_FAMILY_PASS' not in p.stdout,'noninvolutory fourth matrix rejected')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_bytes());deps=[]
    for row in pins['packages']:
        path=a.packages/row['name'];rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
        need(rev==row['rev'],'dependency revision '+row['name'])
        need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'clean tracked dependency '+row['name']);deps.append(dict(name=row['name'],rev=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    axioms={}
    for label,name,count in [('new_bridge','phase258_formal/StringCentralizerBridge.lean',3),('retained_char2','formal/InvolutionCentralizers.lean',2)]:
        source=(ROOT/name).read_text();need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',source,re.M),'formal proof-hole scan '+name)
        target=out/pathlib.Path(name).name;target.write_text(source)
        p=run(label,[a.lean,'-o',target.with_suffix('.olean'),target],env=env)
        need(p.returncode==0 and not re.search(r'error:|warning:|sorryAx',p.stdout+p.stderr),'formal compile '+label)
        rows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout)
        need(len(rows)==count and all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in rows),'standard-only axiom reports '+label);axioms[label]=rows
    source=(ROOT/'phase258_formal/StringCentralizerBridge.lean').read_text()
    for label,old,new in [('no_string','i.val + 1 < j.val','False'),('allow_identity','(nonidentity : ∀ i, rho i ≠ 1)','(nonidentity : ∀ i, True)')]:
        changed=source.replace(old,new);need(changed!=source,'formal mutation applied '+label)
        target=out/(label+'.lean');target.write_text(changed);p=run('control_'+label,[a.lean,target],env=env)
        need(p.returncode!=0 and 'error:' in p.stdout+p.stderr,'false weakening rejected '+label)
    report=dict(status='PASS',exports_checked=len(m['exports']),retained_checked=sum(a.verify_primary or not x['path'].startswith('sources/') for x in m['retained_bindings']),
        primary_checked=a.verify_primary,source_rows=32,proof_spans=9,executions=reports,axioms=axioms,new_lean_declarations=3,reused_lean_declarations=2,
        lean_version=version,dependencies=deps,local_sggi_markings={'S4':72,'A5':360},retained_universal_rows=10,finite_marked_models=8,
        controls=['dihedral sggi withoutIP','A5 five-generator model without string condition','rankfive identity extension ofPSL13',
            'altered projective matrix rejected','altered reversal conjugator rejected','two false Lean weakenings rejected'],
        limits=['Uniform positive results require the full written proof.','Dickson/maximal-subgroup,tori,Dirichlet and Suzuki facts retained.',
            'GAP exact group/presentation algorithms trusted.','Three new general Lean interface declarations only; entire classification not formalized.',
            'New corrections have no question or priority credit.','FinalPGLquestion handled separately.','No measurement or sourcecount credit before independentreview.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',rows=32,local_markings=432,new_lean=3,report=str(out/'report.json'))))
if __name__=='__main__':main()
