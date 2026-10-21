#!/usr/bin/env python3
"""Replay the complete L012 application and its explicitly retained finite inputs."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE250_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(row):
    p=pathlib.PurePosixPath(row['path'])
    need(not p.is_absolute() and '..' not in p.parts,'relative artifact')
    path=ROOT/p
    need(path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'binding '+str(p))
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--gap',type=pathlib.Path,required=True)
    ap.add_argument('--lean',type=pathlib.Path,required=True)
    ap.add_argument('--packages',type=pathlib.Path,required=True)
    ap.add_argument('--verify-primary',action='store_true')
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
    manifest=json.loads((ROOT/'phase250_manifest.json').read_bytes())
    for row in manifest['exports']:bound(row)
    for row in manifest['retained_bindings']:
        if a.verify_primary or not row['path'].startswith('sources/'):bound(row)
    ledger=json.loads((ROOT/'phase250_source_ledger.json').read_bytes())
    need(len(ledger['rows'])==33 and len(ledger['proof_spans'])==14,'ledger coverage')
    for name,row in ledger['proof_spans'].items():
        data=b''.join((ROOT/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'proof span '+name)
    need(all(all(x in ledger['proof_spans'] for x in row['proof_spans']) for row in ledger['rows']),'ledger references')
    old=json.loads((ROOT/'phase207_export.json').read_bytes())
    entry=next(x for x in old['exports'] if x['path']=='phase207_topic_A_umbrella.md');bound(entry)
    reports=[]
    def run(label,args,cwd=out,env=None,timeout=240):
        start=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
        stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
        reports.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-start,4),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
        return p
    def gaprun(label,path,marker):
        p=run(label,[a.gap,'-q','-T',path]);need(p.returncode==0 and marker in p.stdout and not re.search(r'Error|warning',p.stdout+p.stderr),label);return p
    p=run('affine',[sys.executable,'-B','-O',ROOT/'phase250_affine_check.py','--out',out/'affine.json'])
    need(p.returncode==0 and 'PHASE250_AFFINE_PASS' in p.stdout and 'SCHREIER_NORMALIZATION_CONTROL_PASS' in p.stdout,'exact normalized affine model')
    affine=json.loads((out/'affine.json').read_bytes())
    need(affine['point_group_order']==48 and affine['translation_index']==4 and affine['period_indices']==[2,4,8] and len(affine['overlaps'])==2,'uniform affine certificate')
    p=run('control_affine',[sys.executable,'-B','-O',ROOT/'phase250_affine_check.py','--out',out/'bad_affine.json','--corrupt-translation'])
    need(p.returncode!=0 and 'PHASE250_REJECT translation lattice index4' in p.stderr and not (out/'bad_affine.json').exists(),'collapsed affine translation rejection')
    p=gaprun('kernel64',ROOT/'phase250_affine64_kernel.g','AFFINE64_Z3_KERNEL_PASS')
    need('INDEX 48 RAW GENERATORS 3 RAW RELATORS 3' in p.stdout,'exact kernel presentation size')
    p=gaprun('fixed_groups',ROOT/'phase250_fixed_groups.g','PHASE250_FIXED_GROUPS_PASS')
    need(p.stdout.count('IP64 RETRACTION PASS')==3 and 'CORRECTED45 n10 s4 ORDER3072 ROTATION16 IP64 PASS' in p.stdout
        and 'LITERAL45 n10 s4 ORDER1536 ROTATION8 REJECTED_TARGET' in p.stdout
        and 'PERIOD_COMMUTATION_FALSE_WEAKENING_REJECTED' in p.stdout,'fixed models and sign controls')
    p=gaprun('census384',ROOT/'phase250_base384_census.g','PHASE250_CENSUS_PASS')
    flat=' '.join(p.stdout.split())
    need('SMALLGRP_VERSION 1.5.4 GROUP_COUNT 20169' in flat and
        'NO_CGROUP_6_16_ORDER384_PASS GROUPS 20169 ELIGIBLE 1178 PAIRS 4436 GENERATING 0' in flat
        and 'POSITIVE_CGROUP_6_4_CONTROL [ 27, 8, 8 ]' in flat,'complete bound384 census and positive search control')
    legacy=out/'legacy';(legacy/'research/leemans').mkdir(parents=True)
    for name in ['phase2_cubic_lattice_check.py','phase2_cubic_kernel_check.g']:shutil.copy2(ROOT/name,legacy/name)
    # The historical script contains assertions. Deliberately set an inherited
    # optimization variable and pass -E: every legacy assertion must remain active.
    legacyenv=dict(os.environ);legacyenv['PYTHONOPTIMIZE']='2'
    p=run('legacy_assert_guard',[sys.executable,'-E','-B','-c','import sys; assert sys.flags.optimize == 0; print("ASSERTIONS_ENABLED")'],env=legacyenv)
    need(p.returncode==0 and p.stdout.strip()=='ASSERTIONS_ENABLED','legacy assertions active')
    p=run('affine66',[sys.executable,'-E','-B',legacy/'phase2_cubic_lattice_check.py'],cwd=legacy,env=legacyenv)
    need(p.returncode==0 and p.stdout.count('PASS:')==3,'retained exact6,6 affine replay')
    olddata=json.loads((legacy/'phase2_cubic_lattice_check.json').read_bytes())
    need(olddata['point_group_order']==48 and olddata['translation_index_in_Z3']==16
        and olddata['orders_for_m_one']==[192,384,768],'retained6,6 semantic scope')
    # The old script uses raw differences. Its candidate2D3 is Q-invariant;
    # the supplementary written lemma and these integer checks bind that condition.
    need(all(all(t%2==0 for t in v) and sum(v)%4==0 for v in olddata['schreier_vectors']),'raw6,6 containment in invariant2D3')
    basis=[(-2,-2,0),(-2,0,-2),(0,-2,-2)]
    need(all(list(v) in olddata['schreier_vectors'] for v in basis),'raw6,6 generators span2D3')
    # Legacy LogTo is relative; run in the isolated tree, never the shared workspace.
    p=run('kernel66',[a.gap,'-q','-T',legacy/'phase2_cubic_kernel_check.g'],cwd=legacy)
    need(p.returncode==0 and 'KERNEL IS Z^3: exact Reidemeister-Schreier/Tietze presentation PASS' in p.stdout
        and not re.search(r'Error|warning',p.stdout+p.stderr),'retained kernel66')
    bad=legacy/'assertion_control.py';original=(legacy/'phase2_cubic_lattice_check.py').read_text()
    changed=original.replace('assert index == 16','assert index == 17');need(changed!=original,'legacy mutation applied');bad.write_text(changed)
    p=run('control_legacy_assert',[sys.executable,'-E','-B',bad],cwd=legacy,env=legacyenv)
    need(p.returncode!=0 and 'AssertionError' in p.stderr,'corrupted legacy lattice assertion rejected')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_bytes());deps=[]
    for row in pins['packages']:
        path=a.packages/row['name'];rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
        need(rev==row['rev'],'dependency revision '+row['name'])
        need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'clean dependency '+row['name']);deps.append(dict(name=row['name'],rev=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'Lean version')
    source=ROOT/'phase250_formal/PeriodSignObstruction.lean';text=source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'formal proof-hole scan')
    target=out/source.name;target.write_text(text);env=dict(os.environ)
    env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    p=run('formal',[a.lean,'-o',out/'PeriodSignObstruction.olean',target],env=env)
    need(p.returncode==0 and not re.search(r'error:|warning:|sorryAx',p.stdout+p.stderr),'formal compilation')
    axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout)
    need(len(axioms)==3 and all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in axioms),'three standard axiom reports')
    report=dict(status='PASS',scope='Complete corrected principal L012 application, independently reviewable; no admission from execution alone.',
        exports_checked=len(manifest['exports']),retained_bindings_checked=sum(a.verify_primary or not x['path'].startswith('sources/') for x in manifest['retained_bindings']),
        source_rows=33,proof_spans=14,primary_checked=a.verify_primary,executions=reports,axiom_reports=axioms,
        dependencies=deps,lean_version=version,smallgroups_version='1.5.4',census=dict(groups=20169,exponent_eligible=1178,adjacent_orbits=4436,generating_triples=0),
        affine64=dict(point_group=48,translation_index=4,period_indices=[2,4,8]),affine66=dict(point_group=48,translation_index=16,period_indices=[4,8,16]),
        controls=['Schreier raw-rank1/normalized-rank2 countermodel','collapsed affine translation rejected','literal sign presentation misses its advertised target',
            'period-commutation false weakening countermodel','same census finds known6,4 seed','legacy assertions enabled and changed determinant rejected'],
        limits=['Exact bounded GAP algorithms and SmallGroups catalogue retained.','Three Lean sign lemmas only, not the full positive theorem.',
            'Burnside and Lucchini retained with exact scope.','Source correction restricted to bound arXivv2.','No new conjecture or compression rate.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',rows=33,catalogue_groups=20169,lean_declarations=3,report=str(out/'report.json'))))
if __name__=='__main__':main()
