#!/usr/bin/env python3
"""Replay all complete affine-topic mathematical programs and scoped Lean components."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError('AFFINE_VOLUME_REJECT '+msg)
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
    ap.add_argument('--sources-root',type=pathlib.Path)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--xelatex',type=pathlib.Path,default=pathlib.Path('/opt/homebrew/bin/xelatex'))
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
    manifest=json.loads((ROOT/'manifest.json').read_bytes())
    for row in manifest['exports']:bound(row)
    scope=json.loads((ROOT/'scope.json').read_bytes())
    need(scope['ledger_rows']==33 and len(scope['source_rows'])==33,'complete fixed source rows')
    need(len({r['id'] for r in scope['source_rows']})==33 and all(r['id']==r['original_record']['id'] for r in scope['source_rows']),'distinct original source rows')
    need(scope['principal_contracts']==1 and scope['project_total_preserved']==27,'no new principal credit')
    for row in scope['source_rows']:
        need(all(k in scope['proof_regions'] for k in row['current_regions']),'source proof region '+row['id'])
    expected_programs={'phase250_affine_check.py','phase250_affine64_kernel.g','phase250_fixed_groups.g','phase250_base384_census.g','phase2_cubic_lattice_check.py','phase2_cubic_kernel_check.g'}
    need({pathlib.PurePosixPath(r['file']).name for r in scope['programs']}==expected_programs and len(scope['programs'])==6,'six complete required programs')
    for row in scope['programs']:
        bound(dict(path=row['file'],bytes=row['bytes'],sha256=row['sha256']))
    for row in scope['editions']:bound(row)
    # Check the full printed source, without treating line wrapping or page furniture
    # as program bytes. No code fragment or selected diagnostic is substituted.
    from pypdf import PdfReader
    appendix=[]
    for i,page in enumerate(PdfReader(ROOT/'required-programs.pdf').pages):
        lines=page.extract_text().splitlines()
        need(lines[-1]==str(i+1),'appendix footer')
        appendix.append('\n'.join(lines[:-1]))
    appendix='\n'.join(appendix).replace('↪','').replace('⌋','')
    names=re.findall(r'\{programs/([^}]+)\}',(ROOT/'required-programs.tex').read_text())
    need(set(names)==expected_programs and len(names)==6,'full program inclusion directives')
    positions=[re.search('^'+re.escape(n)+'$',appendix,re.M) for n in names]
    need(all(positions),'appendix headings')
    printed=[]
    for i,(name,m) in enumerate(zip(names,positions)):
        end=positions[i+1].start() if i+1<len(names) else len(appendix)
        actual=''.join(appendix[m.end():end].split());expected=''.join((ROOT/'programs'/name).read_text().split())
        need(actual==expected,'complete printed program '+name)
        printed.append(dict(file=name,nonspace_characters=len(expected),complete=True))
    for row in scope['proof_regions'].values():
        p=ROOT/row['path'];text=p.read_text();part=text[row['start']:row['end']]
        need(hashlib.sha256(part.encode()).hexdigest()==row['sha256'],'written proof span '+row['path'])
    if a.sources_root:
        for row in scope['source_bindings']:
            p=a.sources_root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'primary '+row['path'])
    reports=[]
    def run(label,args,cwd=out,env=None,timeout=240):
        start=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
        stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
        reports.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-start,4),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
        return p
    def gaprun(label,path,marker):
        p=run(label,[a.gap,'-q','-T',path]);need(p.returncode==0 and marker in p.stdout and not re.search(r'Error|warning',p.stdout+p.stderr),label);return p
    p=run('affine',[sys.executable,'-B','-O',ROOT/'programs/phase250_affine_check.py','--out',out/'affine.json'])
    need(p.returncode==0 and 'PHASE250_AFFINE_PASS' in p.stdout and 'SCHREIER_NORMALIZATION_CONTROL_PASS' in p.stdout,'exact normalized affine model')
    affine=json.loads((out/'affine.json').read_bytes())
    need(affine['point_group_order']==48 and affine['translation_index']==4 and affine['period_indices']==[2,4,8] and len(affine['overlaps'])==2,'uniform affine certificate')
    p=run('control_affine',[sys.executable,'-B','-O',ROOT/'programs/phase250_affine_check.py','--out',out/'bad_affine.json','--corrupt-translation'])
    need(p.returncode!=0 and 'PHASE250_REJECT translation lattice index4' in p.stderr and not (out/'bad_affine.json').exists(),'collapsed affine translation rejection')
    p=gaprun('kernel64',ROOT/'programs/phase250_affine64_kernel.g','AFFINE64_Z3_KERNEL_PASS')
    need('INDEX 48 RAW GENERATORS 3 RAW RELATORS 3' in p.stdout,'exact kernel presentation size')
    p=gaprun('fixed_groups',ROOT/'programs/phase250_fixed_groups.g','PHASE250_FIXED_GROUPS_PASS')
    need(p.stdout.count('IP64 RETRACTION PASS')==3 and 'CORRECTED45 n10 s4 ORDER3072 ROTATION16 IP64 PASS' in p.stdout
        and 'LITERAL45 n10 s4 ORDER1536 ROTATION8 REJECTED_TARGET' in p.stdout
        and 'PERIOD_COMMUTATION_FALSE_WEAKENING_REJECTED' in p.stdout,'fixed models and sign controls')
    p=gaprun('census384',ROOT/'programs/phase250_base384_census.g','PHASE250_CENSUS_PASS')
    flat=' '.join(p.stdout.split())
    need('SMALLGRP_VERSION 1.5.4 GROUP_COUNT 20169' in flat and
        'NO_CGROUP_6_16_ORDER384_PASS GROUPS 20169 ELIGIBLE 1178 PAIRS 4436 GENERATING 0' in flat
        and 'POSITIVE_CGROUP_6_4_CONTROL [ 27, 8, 8 ]' in flat,'complete bound384 census and positive search control')
    legacy=out/'legacy';(legacy/'research/leemans').mkdir(parents=True)
    for name in ['phase2_cubic_lattice_check.py','phase2_cubic_kernel_check.g']:shutil.copy2(ROOT/'programs'/name,legacy/name)
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
    env=dict(os.environ)
    env['LEAN_PATH']=os.pathsep.join([str(out)]+[str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir()])
    axioms=[]
    for name,count in [('QuotientIntersectionCriterion',4),('AffinePeriodIntersections',2),('PeriodSignObstruction',3)]:
        source=ROOT/'formal'/(name+'.lean');text=source.read_text()
        need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'formal proof-hole scan')
        target=out/source.name;target.write_text(text)
        p=run('formal_'+name,[a.lean,'-o',out/(name+'.olean'),target],env=env)
        need(p.returncode==0 and not re.search(r'error:|warning:|sorryAx',p.stdout+p.stderr),'formal compilation '+name)
        declarations=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout)
        need(len(declarations)==count and all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in declarations),'standard axiom reports '+name)
        axioms.extend(declarations)
    expected_declarations={d for m in scope['formal_scope']['modules'] for d in m['declarations']}
    need({n for n,_ in axioms}==expected_declarations and len(axioms)==9,'exact scoped formal inventory')
    p=run('finite_controls',[sys.executable,'-B','-O',ROOT/'controls.py','--out',out/'finite_controls.json'])
    need(p.returncode==0 and 'AFFINE_PERIOD_CONTROLS_PASS' in p.stdout,'period hypothesis controls')
    renders=[]
    if a.render:
        from pypdf import PdfReader
        temp=out/'render';shutil.copytree(ROOT,temp,ignore=shutil.ignore_patterns('author_replay','*.aux','*.log','*.out','manifest.json'))
        for stem in ['umbrella','mixed-prime-polyhedra','required-programs']:
            for i in range(2):
                p=run('render_'+stem+'_'+str(i),[a.xelatex,'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=temp)
                need(p.returncode==0,'render '+stem)
            need(not re.search(r'Overfull|Missing character|Warning:',p.stdout+p.stderr),'render diagnostics '+stem)
            old=[p.extract_text() for p in PdfReader(ROOT/(stem+'.pdf')).pages];new=[p.extract_text() for p in PdfReader(temp/(stem+'.pdf')).pages]
            need(old==new,'exact rendered page text '+stem);renders.append(dict(paper=stem,pages=len(new),exact_text=True))
    report=dict(status='PASS',scope='Complete corrected principal L012 application, independently reviewable; no admission from execution alone.',
        exports_checked=len(manifest['exports']),retained_bindings_checked=len(scope['source_bindings']) if a.sources_root else 0,
        printed_programs=printed,source_rows=33,proof_spans=len(scope['proof_regions']),primary_checked=bool(a.sources_root),renders=renders,executions=reports,axiom_reports=axioms,
        dependencies=deps,lean_version=version,smallgroups_version='1.5.4',census=dict(groups=20169,exponent_eligible=1178,adjacent_orbits=4436,generating_triples=0),
        affine64=dict(point_group=48,translation_index=4,period_indices=[2,4,8]),affine66=dict(point_group=48,translation_index=16,period_indices=[4,8,16]),
        controls=['Schreier raw-rank1/normalized-rank2 countermodel','collapsed affine translation rejected','literal sign presentation misses its advertised target',
            'period-commutation false weakening countermodel','same census finds known6,4 seed','legacy assertions enabled and changed determinant rejected','3787 valid elementary abelian smaller-period cases','countermodels to removing point-faithfulness or period containment'],
        limits=['Exact bounded GAP algorithms and SmallGroups catalogue retained.','Three old sign lemmas, four old quotient criteria and two new smaller-period statements; not the full positive theorem.',
            'Burnside and Lucchini retained with exact scope.','Source correction restricted to bound arXivv2.','No new conjecture or compression rate.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',rows=33,catalogue_groups=20169,lean_declarations=9,report=str(out/'report.json'))))
if __name__=='__main__':main()
