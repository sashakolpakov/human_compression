import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'doubling_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable destination');P.mkdir()
    for n in ['literal_joins.py','literal_joins_v2.py','literal_joins_v3.py','fusion_join.py','replay.py','small_controls.py','controls.py','check.py','joins.tex','README.rst','approach01.rst','unpaid_truncation_delta.diff','source_link_successor_delta.diff','freeze.py']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native02/joins.pdf',P/'joins.pdf');shutil.copytree(W/'native02',P/'native_author');H=P/'history';H.mkdir();E=P/'expected';E.mkdir()
    for n in ['doubling01','truncation01','truncation02','fusion01','small01','replay01','controls01','native01']:shutil.copytree(W/n,H/n)
    for n in ['run_bound.py','run_bound_v2.py','run_bound_v3.py','doubling01_terminal.stdout','doubling01_terminal.stderr','truncation01_terminal.stdout','truncation01_terminal.stderr','truncation02_terminal.stdout','truncation02_terminal.stderr']:shutil.copyfile(W/n,H/n)
    aliases=[]
    for name,src in [('doubling.json',W/'doubling01/result/report.json'),('truncation.json',W/'truncation02/result/report.json'),('fusion.json',W/'fusion01/report.json')]:
        shutil.copyfile(src,E/name);r=row(src);aliases.append(dict(original=str(src),copy='expected/'+name,bytes=r['bytes'],sha256=r['sha256']))
    N=P/'native_source';N.mkdir()
    for i in range(1,8):shutil.copyfile(G/f'source_join_component_v2/native/high-{i:02d}.png',N/f'page-{i+6:02d}.png')
    shutil.copyfile(G/'remaining_audit_work/source-06.png',N/'page-06.png')
    roots={
      'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
      'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
      'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86',
      'palette_serialization_v1':'5399e45468b83a49e0d2750a2087cb8e6006919b08548d0434b5195ed550eff3',
      'palette_serialization_review_v1':'6a09697960e322a8d10bcabc9354504f8e0b1e6c17a9ed485ab36c25aa6ab96a',
      'source_join_component_v2':'2e69c5d047fa7d15fb8d101090a78c18a69f3100db2aeb111abc107878639ffb',
      'source_join_review_v2':'1cbc91ca8ba73e421cf2e6412b20654a5057f7545ffc232d29566d169f41fd00'}
    deps={};rootrows=[]
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'acquired binding '+str(p))
        if str(p)in deps:need(deps[str(p)]==r,'binding conflict')
        deps[str(p)]=r
    for name,h in roots.items():
        R=G/name;M=R/'manifest.json';need(row(M)['sha256']==h,'exact root');add(M);rootrows.append(row(M,S))
        for r in read(M)['exports']:add(R/r['path'],r)
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute() else S/p,r)
    for n in ['doubling01','truncation01','truncation02']:
        r=read(W/n/'receipt.json')
        for q in r['inputs']:add(Path(q['path']),q)
        for k in ['stdout','stderr','report']:
            if k in r:add(Path(r[k]['path']),r[k])
    for r in read(W/'fusion01/report.json')['inputs']:add(Path(r['path']),r)
    for p in W.rglob('*'):
        if p.is_file() and '__pycache__'not in p.parts:add(p)
    for p in [G/'remaining_audit_work/source-06.png',S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',Path(sys.executable),Path('/opt/homebrew/bin/pdflatex'),Path('/opt/homebrew/bin/gs')]:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    save(P/'acquired_roots.json',rootrows);save(P/'input_aliases.json',aliases)
    double=read(E/'doubling.json');trunc=read(E/'truncation.json');fusion=read(E/'fusion.json')
    save(P/'source_routes.json',dict(source='corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf',source_sha256='13f207232f40ca0e00674b9e9de02a91e98226b325ddd428320c661e6131ff84',source_edition='Halle22-page preprint; journal uncollated',doublings=[{k:r[k]for k in ['source_label','target_label','source_index','target_index','point_type','pair_type','checks']}for r in double['routes']],printed_doubling_pages=[8,11,13],rank_two_qualification='p8 applies a quoted rank>=3 corollary; direct elementary bipartite-double argument supplies rank2.',printed_valid_truncation_links=23,corrected_truncation_links=trunc['source_corrections'],acquired_prior_maps=8,new_truncation_maps=16,source_fusion_multiplicities=[{k:r[k]for k in ['label','printed','actual','match']}for r in fusion['rows']],full_source_credit=0,principal_classification_refuted=False,pending=['Abstract structural group names','Ordered butterflies and remaining direct recipes','Whole source synthesis']))
    save(P/'roles.json',dict(author='publication_recovery',source_attribution='Gottschalk--Leemans concrete links; general sourceCor2.1 is attributed there to[40]. Here a sufficient elementary argument proves the actual links.',root_input='Scope/retained-input requests and accepted prior component reviews; no new doubling argument or map-code contribution.',distinct_review='pending',priority_claim=False))
    save(P/'development.json',dict(doubling='One1.56s complete four-map pass.',truncation01='Ten complete maps followed by exact2.54s failure at printed5.3->3.6; original failure fully retained.',truncation02='Changed successor reuses10 prefix maps and searches6 outstanding positive maps, including5.2->3.6 repair.',native='First3-page build had2 overfull lines; exact oldTeX/log/PDF retained. Equivalent prose shortening gives clean native02; all3final pages directly viewed.',earlier_progress_wording='Before checking the native log, a progress message called the first build clean; the two layout warnings were subsequently found and corrected, with both editions retained.',all_owned_handles_terminal=True))
    final=[]
    for p,r in sorted(deps.items()):
        p=Path(p);final.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',final)
    exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()];save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_DOUBLING_TRUNCATION_FUSION_COMPONENT_V1',exports=exports,dependencies=len(final)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(final)),indent=2))
if __name__=='__main__':main()
