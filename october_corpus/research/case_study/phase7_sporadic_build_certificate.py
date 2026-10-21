#!/usr/bin/env python3
"""Bind generic exhaustive sporadic classifications to exact inputs and outputs."""
import argparse, ast, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('group',choices=['M22','M23','HS','J3'])
    ap.add_argument('--require-2t',action='store_true',default=True)
    ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap')); a=ap.parse_args()
    if not a.gap: ap.error('Set GAP or pass --gap')
    stem='phase7_sporadic_'+a.group+('_2T' if a.require_2t else '')
    progress=json.loads((HERE/(stem+'_progress.json')).read_text())
    checks=json.loads((HERE/(stem+'_final_checks.json')).read_text())
    total=progress['total_borels']
    assert progress['all_borels_complete'] and checks['passed']
    assert set(progress['completed'])=={str(i) for i in range(1,total+1)}
    assert sha(HERE/'phase7_sporadic_search.g')==progress['executed_script_sha256']
    for e in progress['completed'].values(): assert sha(HERE/e['checkpoint'])==e['sha256']
    for run in progress['runs']:
        assert sha(HERE/run['log'])==run['log_sha256']
        assert run['executed_script_sha256']==progress['executed_script_sha256']
    for run in checks['runs']:
        assert run['passed'] and sha(HERE/run['script'])==run['executed_sha256'] and sha(HERE/run['log'])==run['log_sha256']
    for name,digest in checks['prerequisites'].items(): assert sha(HERE/name)==digest
    # Use only the recorded successful run for each terminal anchor. Interrupted
    # attempts remain provenance but cannot duplicate an anchor in the certificate.
    borels={}; inputs=[]; tested={}
    for run in progress['runs']:
        logs=(HERE/run['log']).read_text()
        m=re.search(r'INPUT group=(\S+) require_2T=(\S+) order=(\d+) subgroup_classes=(\d+) maximal_inclusion_classes=(\d+) locally_2T_inclusions=(\d+) GAP=(\S+) TomLib=(\S+)',logs)
        assert m and m[1]==a.group and int(m[4])==total
        inputs.append(m.groups())
        keep={int(i) for i,e in progress['completed'].items() if e['run']==run['number']}
        for m in re.finditer(r'BOREL_BEGIN id=(\d+) order=(\d+) normalizer=(\d+) panels=(\d+)',logs):
            i=int(m[1])
            if i in keep: borels[i]=dict(id=i,order=int(m[2]),normalizer_order=int(m[3]),admissible_panels=int(m[4]),levels=[])
        for m in re.finditer(r'BOREL_LEVEL id=(\d+) rank=(\d+) classes=(\d+) full_group=(\d+)',logs):
            i=int(m[1])
            if i in keep: borels[i]['levels'].append(dict(rank=int(m[2]),classes=int(m[3]),full_group_classes=int(m[4])))
        for m in re.finditer(r'BOREL_COMPLETE id=(\d+) rank_counts=(\[[^\]]*\]) full_group(?:_ranks)?=(\[[^\]]*\])',logs):
            i=int(m[1])
            if i not in keep: continue
            b=borels[i]; counts=ast.literal_eval(m[2]); ranks=ast.literal_eval(m[3])
            assert counts==[e['classes'] for e in b['levels']]
            assert (counts and counts[-1]==0) if b['admissible_panels'] else counts==[]
            assert collections.Counter(ranks)==collections.Counter({e['rank']:e['full_group_classes'] for e in b['levels'] if e['full_group_classes']})
            b.update(exhaustion_complete=True,full_group_ranks=ranks)
        for m in re.finditer(r'BOREL_PROGRESS id=(\d+) rank=(\d+) anchor=\d+/\d+ checked=(\d+)',logs):
            if int(m[1]) in keep: tested[(int(m[1]),int(m[2]))]=int(m[3])
    assert set(borels)==set(range(1,total+1)) and all(b.get('exhaustion_complete') for b in borels.values())
    assert all(x==inputs[0] for x in inputs)
    inp=inputs[0]; inner=collections.Counter(); generated=collections.Counter()
    for b in borels.values():
        for e in b['levels']: inner[e['rank']]+=e['full_group_classes']; generated[e['rank']]+=e['classes']
    fusion=(HERE/(stem+'_fuse.log')).read_text(); fusions=[]; twot=[]
    for m in re.finditer(r'FUSION rank=(\d+) inner_classes=(\d+) aut_type_classes=(\d+) orbits=(\[[^\n]*\])',fusion):
        r=int(m[1]); orbits=ast.literal_eval(m[4]); n=int(m[2])
        assert n==inner[r] and sorted(x for o in orbits for x in o)==list(range(1,n+1))
        assert len(orbits)==int(m[3])
        fusions.append(dict(rank=r,inner_classes=n,aut_type_classes=int(m[3]),orbits=orbits))
    for m in re.finditer(r'LOCAL_2T rank=(\d+) total=(\d+) nontruncations=(\d+)',fusion):
        twot.append(dict(rank=int(m[1]),total=int(m[2]),nontruncations=int(m[3])))
    assert fusions and fusions[-1]['aut_type_classes']==0 and len(twot)==len(fusions)
    witnesses=[]; verify=(HERE/(stem+'_verify.log')).read_text()
    for m in re.finditer(r'WITNESS id=(\d+) rank=(\d+) borel=(\d+) parabolic_orders=(\[[^\]]*\]) panel_orders=(\[[^\]]*\]) twot=(true|false) all_requested_axioms=true',verify):
        witnesses.append(dict(id=int(m[1]),rank=int(m[2]),borel_order=int(m[3]),parabolic_orders=ast.literal_eval(m[4]),panel_orders=ast.literal_eval(m[5]),twot=m[6]=='true',all_requested_axioms=True))
    assert len(witnesses)==sum(e['aut_type_classes'] for e in fusions)
    assert [w['id'] for w in witnesses]==list(range(1,len(witnesses)+1))
    for row in twot: assert sum(w['rank']==row['rank'] and w['twot'] for w in witnesses)==row['total']
    if a.require_2t: assert all(w['twot'] for w in witnesses)
    table_file={'M22':'tmmath.tom.gz','M23':'tmmath.tom.gz','J3':'tmjank.tom.gz','HS':'tmhsmcl.tom.gz'}[a.group]
    query=f'SizeScreen([100000,24]);LoadPackage("tomlib");Print("TOMDATA=",Filename(DirectoriesPackageLibrary("tomlib","data"),"{table_file}"),"\\n");QUIT;'
    out=subprocess.check_output([a.gap,'-q','-c',query],text=True)
    tompath=Path(re.search(r'TOMDATA=(.+)',out)[1].strip())
    expected={'M22':[1,20,12,9,0],'M23':[0,3,16,10,0],'HS':[4,20,41,8,1],'J3':[5,17,0,0,0]}[a.group]
    actual=[next((x['nontruncations'] for x in twot if x['rank']==r),0) for r in range(2,7)]
    comparison=dict(primary_source='Leemans, Australasian J. Combin.33(2005),231–236, Table1 p.232',url='https://ajc.maths.uq.edu.au/pdf/33/ajc_v33_p231.pdf',convention='Local (2T)1 imposed and truncations of higher-rank geometries removed',published=expected,computed=actual,matches=actual==expected)
    names=['phase7_sporadic_source_assets.json','phase7_sporadic_source_audit.md','phase7_sporadic_theory.md','phase7_sporadic_search.g','phase7_sporadic_run.py','phase7_sporadic_fuse.g','phase7_sporadic_verify.g','phase7_sporadic_finish.py','phase7_sporadic_build_certificate.py','phase4_geometry_checks.g',stem+'_representatives.g',stem+'_progress.json',stem+'_final_checks.json']
    names += [r['log'] for r in progress['runs']]+[r['log'] for r in checks['runs']]+[progress['completed'][str(i)]['checkpoint'] for i in range(1,total+1)]
    expected_totals={'M22':{3:25,4:16,5:9},'M23':{3:13,4:21,5:10},'HS':{3:30,4:41,5:8,6:1},'J3':{3:17}}[a.group]
    total_actual={r:next((x['aut_type_classes'] for x in fusions if x['rank']==r),0) for r in expected_totals}
    total_comparison=dict(primary_source='Jacobs and Leemans, LMS J. Comput. Math.7(2004), Table1 p.288',url='https://doi.org/10.1112/S1461157000001133',convention='All geometries in the locally two-transitive class; truncations retained.',published=expected_totals,computed=total_actual,matches=total_actual==expected_totals)
    supplementary={}
    apath=HERE/(stem+'_archive_compare.json')
    if a.group in ['M22','M23'] and apath.exists():
        ar=json.loads(apath.read_text())
        assert ar['passed'] and ar['group']==a.group
        assert sha(HERE/'phase7_sporadic_archive_compare.g')==ar['executed_source_sha256']
        assert sha(HERE/'phase7_sporadic_archive_compare.py')==ar['parser_sha256']
        assert sha(HERE/'phase4_parse_j2.py')==ar['permutation_parser_sha256']
        assert sha(HERE/ar['log'])==ar['log_sha256']
        for n,digest in ar['prerequisites'].items(): assert sha(HERE/n)==digest
        names += ['phase7_sporadic_archive_compare.g','phase7_sporadic_archive_compare.py','phase4_parse_j2.py',apath.name,ar['log']]
        supplementary['source_archive_comparison']=ar
    artifacts={n:dict(bytes=(HERE/n).stat().st_size,sha256=sha(HERE/n)) for n in names}
    report=dict(status='passed',group=a.group,supplementary=supplementary,scope='All firm, flag-transitive, residually connected, RWPRI, locally two-transitive coset geometries satisfying (IP)2, rank at least two.',requires_local_two_transitivity=a.require_2t,original_geometry_lists_read_during_enumeration=False,original_geometry_lists_read_during_posthoc_comparison='source_archive_comparison' in supplementary,software=dict(GAP=inp[6],TomLib=inp[7]),imported_group_data=dict(package_file='tomlib/data/'+table_file,bytes=tompath.stat().st_size,sha256=sha(tompath),order=int(inp[2]),subgroup_classes=total,maximal_inclusion_classes=int(inp[4]),locally_two_transitive_inclusions=int(inp[5])),trust_boundary=['Completeness of the imported subgroup catalogue.','GAP exact finite-group algorithms.','The uniform completeness/recognition argument is a written proof, not a Lean formalization.'],counts=dict(inner_and_type={str(r):inner[r] for r in sorted(inner)},automorphism_and_type={str(e['rank']):e['aut_type_classes'] for e in fusions},all_generated_subgroup_classes={str(r):generated[r] for r in sorted(generated)},tested_augmentation_orbit_representatives=sum(tested.values())),borel_anchors=[borels[i] for i in range(1,total+1)],fusions=fusions,local_two_transitivity_postprocessing=twot,verified_witnesses=witnesses,primary_table_comparison=comparison,primary_total_comparison=total_comparison,search_runs=progress['runs'],final_checks=checks['runs'],timing_seconds=dict(search=sum(r.get('seconds',0) for r in progress['runs']),fusion_and_validation=sum(r['seconds'] for r in checks['runs'])),artifacts=artifacts,source_scope_caution='See phase7_sporadic_source_audit.md. The exact class is primary-source verified, but original M22/M23 article bodies were not obtained. Principal census components are rederived; separate constructions and whole-paper equivalence are not claimed.',reproduction=[f'python3 research/leemans/phase7_sporadic_run.py {a.group}',f'python3 research/leemans/phase7_sporadic_finish.py {a.group}',f'python3 research/leemans/phase7_sporadic_build_certificate.py {a.group}'])
    (HERE/(stem+'_certificate.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(group=a.group,status='passed',counts=report['counts']['automorphism_and_type'],borels=total,witnesses=len(witnesses),primary_table_matches=comparison['matches'],timing_seconds=report['timing_seconds']),indent=2))
if __name__=='__main__': main()
