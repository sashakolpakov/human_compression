#!/usr/bin/env python3
"""Bind completed exact J2 runs, their data sources, and their limited claims."""
import argparse,ast,hashlib,json,os,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('GAP not found: set GAP or pass --gap')
    runs=json.loads((HERE/'phase4_j2_runs.json').read_text())
    assert runs['passed'] and len(runs['runs'])==5
    for run in runs['runs']:
        assert run['passed'] and sha(HERE/run['script'])==run['executed_sha256'] and sha(HERE/run['log'])==run['log_sha256']
    source=json.loads((HERE/'phase4_j2_source_data.json').read_text())
    entries=[];text=(HERE/'phase4_verify_j2.log').read_text()
    for m in re.finditer(r'CHECK (\S+) (\d+) selected=(true|false) result=rec\((.*?)\) ms=(\d+)',text,re.S):
        flags={k:v=='true' for k,v in re.findall(r'(firm|rc|rwpri|twot|ip2|ft|join) := (true|false)',m[4])}
        assert len(flags)==7
        def field(name):return ast.literal_eval(re.search(r'\b'+name+r' := (\[[^\]]*\]|\d+)',m[4])[1])
        entries.append(dict(file=m[1],raw_index=int(m[2]),selected=m[3]=='true',borel=field('borel'),parabolic_orders=field('orders'),panel_orders=field('panels'),checks=flags,all_source_axioms=all(flags.values())))
    assert len(entries)==31
    rank3=[e for e in entries if e['file']=='j2.rk3'];rank4=[e for e in entries if e['file']=='j2.rk4']
    assert sum(e['selected'] for e in rank3)==24 and sum(e['all_source_axioms'] for e in rank3)==24
    assert all(e['all_source_axioms']==e['selected'] for e in rank3) and all(e['all_source_axioms'] for e in rank4)
    thinlog=(HERE/'phase4_thin_j2.log').read_text();assert 'EXHAUSTION_COMPLETE' in thinlog
    levels=[dict(rank=1,ambient_inner_and_type_classes=2,J2_classes=0)]
    for m in re.finditer(r'LEVEL_DONE rank=(\d+) classes=(\d+) J2=(\d+) orders=(.*?)(?=\nrank=|\nEXHAUSTION_COMPLETE)',thinlog,re.S):
        levels.append(dict(rank=int(m[1]),ambient_inner_and_type_classes=int(m[2]),J2_classes=int(m[3]),generated_group_orders_and_counts=ast.literal_eval(m[4])))
    assert [e['ambient_inner_and_type_classes'] for e in levels]==[2,17,62,63,21,0]
    assert [e['J2_classes'] for e in levels]==[0,0,0,4,0,0]
    tested={}
    for m in re.finditer(r'rank=(\d+) anchor=\d+/\d+ overgroups=\d+ checked=(\d+) accepted=\d+',thinlog):tested[m[1]]=int(m[2])
    fusions=[];fusionlog=(HERE/'phase4_fuse_j2.log').read_text()
    for m in re.finditer(r'FUSION name=(\S+) input=(\d+) classes=(\d+) aut_order=(\d+) orbits=(.*?)(?=\nSOURCE_INDICES|\nTHIN_CLASS_ORDERS)',fusionlog,re.S):
        fusions.append(dict(name=m[1],input=int(m[2]),classes=int(m[3]),automorphism_group_order=int(m[4]),orbits=ast.literal_eval(m[5])))
    assert [(e['input'],e['classes']) for e in fusions]==[(24,19),(1,1),(4,2)]
    data=re.search(r'INPUT\s+subgroup_classes=\s*(\d+)\s+maximal_inclusion_classes=\s*(\d+)\s+GAP=(\S+)\s+TomLib=(\S+)',thinlog)
    assert data and int(data[1])==146
    query='SizeScreen([100000,24]);LoadPackage("tomlib");Print("TOMDATA=",Filename(DirectoriesPackageLibrary("tomlib","data"),"tmjank.tom.gz"),"\\n");QUIT;'
    out=subprocess.run([a.gap,'-q','-c',query],check=True,capture_output=True,text=True).stdout
    path=Path(re.search(r'TOMDATA=(.+)',out)[1].strip());digest=sha(path)
    assert digest=='576834302b6da30248f34565d6559b857160fdbd67066d1e67c64f0191b8b143'
    artifacts=['phase4_old_classification.md','phase4_parse_j2.py','phase4_run_j2.py','phase4_build_certificate.py','phase4_thin_j2.g','phase4_verify_j2.g','phase4_fuse_j2.g','phase4_geometry_checks.g','phase4_identify_source.g','phase4_source_isomorphism.g','phase4_thin_j2_witnesses.g','phase4_verify_thin_witnesses.g','phase4_j2_runs.json']+[r['log'] for r in runs['runs']]
    report=dict(status='passed',scope={'uniform_theory':'Arbitrary finite-rank torsor/panel recognition and complete maximal-residue augmentation, with typed Helly retained.','independent_classification':'All thin firm FT RC RWPRI locally-two-transitive IP2 geometries of J2, conditional on the complete GAP TomLib subgroup/inclusion catalogue: precisely two rank4 Aut(J2)/type classes, no other ranks >=2.','source_data_validation':'All 30 raw rank3 source triples and the one thick rank4 source quadruple checked; 24 accepted rank3 entries fuse to19 classes.','not_claimed':'Independent exhaustion of the nonthin J2 geometries, or a new proof that the imported subgroup catalogue is complete.'},software={'GAP':data[3],'TomLib':data[4]},imported_subgroup_data={'package_file':'tomlib/data/tmjank.tom.gz','bytes':path.stat().st_size,'sha256':digest,'subgroup_classes':int(data[1]),'maximal_inclusion_classes':int(data[2]),'trust_boundary':'Catalogue subgroup-class completeness and GAP exact group operations are imported.'},primary_archive={'url':source['source_url'],'sha256':source['archive_sha256'],'member_sha256':{n:e['sha256'] for n,e in source['files'].items()},'redistribution':'Archive and original Magma files are not included; the parser requires an explicit --archive argument.'},group_identification={'method':'Explicit generator images define a checked bijective homomorphism from both primary-source groups onto TomLib J2.','witness':'phase4_source_isomorphism.g','check':'phase4_identify_source.log'},source_entries=entries,thin_levels=levels,maximal_augmentation_orbit_representatives_tested=tested,fusions=fusions,runs=runs['runs'],artifacts={n:{'bytes':(HERE/n).stat().st_size,'sha256':sha(HERE/n)} for n in artifacts},reproduction=['python3 research/leemans/phase4_run_j2.py --archive /path/to/S1461157000001133sup002.tar','python3 research/leemans/phase4_build_certificate.py'],provenance='Only the final five-stage pipeline is certified. Earlier stopped or changed development runs are excluded. No Lean claim is made for this enumeration.')
    (HERE/'phase4_j2_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'artifacts':len(artifacts),'thin_classes':2,'rank3_verified_classes':19,'thick_rank4_verified_classes':1,'total_run_seconds':sum(r['seconds'] for r in runs['runs'])},indent=2))
if __name__=='__main__':main()
