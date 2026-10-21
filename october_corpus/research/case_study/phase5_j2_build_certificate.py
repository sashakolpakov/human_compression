#!/usr/bin/env python3
"""Bind the independently exhaustive J2 census to code, inputs, and outputs."""
import argparse,ast,collections,hashlib,json,os,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('GAP unavailable: set GAP or pass --gap')
    progress=json.loads((HERE/'phase5_j2_progress.json').read_text());checks=json.loads((HERE/'phase5_j2_final_checks.json').read_text())
    assert progress['all_146_borels_complete'] and set(progress['completed'])=={str(i) for i in range(1,147)} and checks['passed']
    assert sha(HERE/'phase5_j2_search.g')==progress['executed_script_sha256']
    for item in progress['completed'].values():assert sha(HERE/item['checkpoint'])==item['sha256']
    for run in progress['runs']:
        assert run['passed'] and sha(HERE/run['log'])==run['log_sha256'] and run['executed_script_sha256']==progress['executed_script_sha256']
    for run in checks['runs']:
        assert run['passed'] and sha(HERE/run['script'])==run['executed_sha256'] and sha(HERE/run['log'])==run['log_sha256']
    for name,digest in checks['prerequisites'].items():assert sha(HERE/name)==digest
    logs='\n'.join((HERE/r['log']).read_text() for r in progress['runs'])
    inp=re.search(r'INPUT subgroup_classes=(\d+) maximal_inclusion_classes=(\d+) locally_2T_inclusions=(\d+) GAP=(\S+) TomLib=(\S+)',logs)
    assert inp and tuple(map(int,inp.group(1,2,3)))==(146,568,417)
    borels={}
    for m in re.finditer(r'BOREL_BEGIN id=(\d+) order=(\d+) normalizer=(\d+) panels=(\d+)',logs):
        i=int(m[1]);assert i not in borels
        borels[i]=dict(id=i,order=int(m[2]),normalizer_order=int(m[3]),admissible_panels=int(m[4]),levels=[])
    assert set(borels)==set(range(1,147))
    for m in re.finditer(r'BOREL_LEVEL id=(\d+) rank=(\d+) classes=(\d+) J2=(\d+)',logs):
        borels[int(m[1])]['levels'].append(dict(rank=int(m[2]),classes=int(m[3]),J2_classes=int(m[4])))
    for m in re.finditer(r'BOREL_COMPLETE id=(\d+) rank_counts=(\[[^\]]*\]) J2(?:_ranks)?=(\[[^\]]*\])',logs):
        b=borels[int(m[1])];counts=ast.literal_eval(m[2]);jranks=ast.literal_eval(m[3])
        assert counts==[e['classes'] for e in b['levels']]
        if b['admissible_panels']:assert counts and counts[-1]==0
        else:assert counts==[]
        assert collections.Counter(jranks)==collections.Counter({e['rank']:e['J2_classes'] for e in b['levels'] if e['J2_classes']})
        b['exhaustion_complete']=True;b['J2_ranks']=jranks
    assert all(b.get('exhaustion_complete') for b in borels.values())
    totals=collections.Counter();inner=collections.Counter();tested={}
    for b in borels.values():
        for e in b['levels']:totals[e['rank']]+=e['classes'];inner[e['rank']]+=e['J2_classes']
    assert [inner[r] for r in [2,3,4]]==[8,24,5] and not any(inner[r] for r in inner if r>=5)
    for m in re.finditer(r'BOREL_PROGRESS id=(\d+) rank=(\d+) anchor=\d+/\d+ checked=(\d+)',logs):tested[(int(m[1]),int(m[2]))]=int(m[3])
    fusions=[]
    for m in re.finditer(r'FUSION rank=(\d+) inner_classes=(\d+) aut_type_classes=(\d+) orbits=(\[[^\n]*\])',(HERE/'phase5_j2_fuse.log').read_text()):
        fusions.append(dict(rank=int(m[1]),inner_classes=int(m[2]),aut_type_classes=int(m[3]),orbits=ast.literal_eval(m[4])))
    assert len(fusions)==13 and [e['aut_type_classes'] for e in fusions[:3]]==[8,19,3] and all(e['aut_type_classes']==0 for e in fusions[3:])
    witnesses=[]
    for m in re.finditer(r'WITNESS id=(\d+) rank=(\d+) borel=(\d+) parabolic_orders=(\[[^\]]*\]) panel_orders=(\[[^\]]*\]) all_axioms=true',(HERE/'phase5_j2_verify.log').read_text()):
        witnesses.append(dict(id=int(m[1]),rank=int(m[2]),borel_order=int(m[3]),parabolic_orders=ast.literal_eval(m[4]),panel_orders=ast.literal_eval(m[5]),all_axioms=True))
    assert len(witnesses)==30
    query='SizeScreen([100000,24]);LoadPackage("tomlib");Print("TOMDATA=",Filename(DirectoriesPackageLibrary("tomlib","data"),"tmjank.tom.gz"),"\\n");QUIT;'
    output=subprocess.run([a.gap,'-q','-c',query],capture_output=True,text=True,check=True).stdout
    path=Path(re.search(r'TOMDATA=(.+)',output)[1].strip());digest=sha(path)
    assert digest=='576834302b6da30248f34565d6559b857160fdbd67066d1e67c64f0191b8b143'
    names=['phase5_j2_theory.md','phase5_j2_search.g','phase5_j2_run.py','phase5_j2_finish.py','phase5_j2_build_certificate.py','phase5_j2_fuse.g','phase5_j2_verify.g','phase5_j2_representatives.g','phase5_j2_progress.json','phase5_j2_final_checks.json','phase4_geometry_checks.g']+[r['log'] for r in progress['runs']]+[r['log'] for r in checks['runs']]+[progress['completed'][str(i)]['checkpoint'] for i in range(1,147)]
    artifacts={n:dict(bytes=(HERE/n).stat().st_size,sha256=sha(HERE/n)) for n in names}
    report=dict(status='passed',principal_result='Full L104 census independently reproduced: 8 rank-two, 19 rank-three, 3 rank-four geometries, none of higher rank, under the paper\'s stated axioms and Aut(J2)/type equivalence.',classification_scope='All firm, flag-transitive, residually connected, residually weakly primitive J2 coset geometries satisfying (2T)1 and (IP)2.',original_geometry_lists_read=False,software=dict(GAP=inp[4],TomLib=inp[5]),imported_group_data=dict(package_file='tomlib/data/tmjank.tom.gz',bytes=path.stat().st_size,sha256=digest,subgroup_classes=146,maximal_inclusion_classes=568,locally_two_transitive_inclusion_classes=417),trust_boundary=['Completeness of the imported J2 subgroup catalogue.','GAP exact finite-group algorithms, including maximal subgroups, normalizers, transporters, intersections, cosets, and automorphism actions.','The stated arbitrary-rank completeness and recognition proof is a human-readable mathematical argument; no complete Lean formalization is claimed.'],not_rederived=['The subgroup classification underlying TomLib.','Every secondary annotation in the original supplement, such as full correlation groups or doubling relations.'],counts=dict(inner_and_type={str(r):inner[r] for r in sorted(inner)},automorphism_and_type={str(e['rank']):e['aut_type_classes'] for e in fusions},all_generated_subgroup_classes={str(r):totals[r] for r in sorted(totals)},tested_maximal_augmentation_orbit_representatives=sum(tested.values()),tested_by_rank={str(r):sum(n for (b,k),n in tested.items() if k==r) for r in sorted(set(k for b,k in tested))}),borel_anchors=[borels[i] for i in range(1,147)],fusions=fusions,verified_witnesses=witnesses,search_runs=progress['runs'],final_checks=checks['runs'],timing_seconds=dict(search=sum(r['seconds'] for r in progress['runs']),fusion_and_validation=sum(r['seconds'] for r in checks['runs'])),artifacts=artifacts,primary_source=dict(catalogue_id='L104',title='The residually weakly primitive geometries of J2',author='Dimitri Leemans',year=2002,locator='Section3, pages79–80; axioms in Section1, page78.',url='https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585'),reproduction=['python3 research/leemans/phase5_j2_run.py','python3 research/leemans/phase5_j2_finish.py','python3 research/leemans/phase5_j2_build_certificate.py'],provenance='The recorded fresh full search and final checks bind exact executed source hashes. Development B=1 cross-check output is not used as exhaustion evidence.')
    (HERE/'phase5_j2_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='passed',counts=[8,19,3,0],borel_anchors=146,tested_orbit_representatives=sum(tested.values()),artifacts=len(artifacts),timing_seconds=report['timing_seconds']),indent=2))
if __name__=='__main__':main()
