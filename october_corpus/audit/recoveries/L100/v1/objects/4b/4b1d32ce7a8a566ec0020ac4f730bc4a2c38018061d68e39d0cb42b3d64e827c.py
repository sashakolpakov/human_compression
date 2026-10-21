"""Frozen preparation component only; no L100 extension or target caller."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,time
if not __debug__:raise SystemExit('optimized execution forbidden')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows_check(rows,study):
    for r in rows:
        p=study/r['path'] if r['namespace']=='study' else pathlib.Path(r['path'])
        assert p.is_file() and p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],p
def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
    here=pathlib.Path(__file__).resolve().parent
    if not a.out.is_absolute():raise SystemExit('absolute output directory required')
    manifest=json.loads((here/'manifest.json').read_text());deps=json.loads((here/'dependencies.json').read_text())
    for r in manifest['exports']:
        f=here/r['path'];assert f.stat().st_size==r['bytes'] and digest(f)==r['sha256'],f
    rows_check(deps,a.study)
    src=(a.study/'phase7_sporadic_search.g').read_bytes()
    assert (here/'legacy_functions.g').read_bytes()==src[src.index(b'IsMaxPair:=function'):src.index(b'if not IsBound(BOREL_IDS)')]
    assert (here/'legacy_initialization.g').read_bytes()==src[src.index(b'maxorders:=rec();;'):src.index(b'Print("INPUT')]
    assert (here/'accepted_verify.g').read_bytes()==(a.study/'phase4_geometry_checks.g').read_bytes()
    a.out.mkdir(parents=True,exist_ok=False)
    cmd=[sys.executable,str(here/'replay_small.py'),'--out',str(a.out/'small')]
    with (a.out/'replay.stdout').open('wb') as so,(a.out/'replay.stderr').open('wb') as se:
        r=subprocess.run(cmd,stdout=so,stderr=se,timeout=45)
    assert r.returncode==0 and not (a.out/'replay.stderr').read_bytes()
    report=json.loads((a.out/'small/report.json').read_text());assert report['status']=='PASS_FRESH_BROAD_APPLICABILITY_SMALL_CONTROLS'
    opts=[]
    for script in ['check.py','replay_small.py','literal_oracle.py','prepare_driver_v2.py']:
        r=subprocess.run([sys.executable,'-O',str(here/script)],capture_output=True)
        assert r.returncode!=0 and b'optimized execution forbidden' in r.stderr
        opts.append(script)
    native=[]
    if a.render:
        n=a.out/'native';n.mkdir()
        for i in range(2):
            r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(n),str(here/'applicability.tex')],capture_output=True,timeout=30)
            (n/f'build{i}.stdout').write_bytes(r.stdout);(n/f'build{i}.stderr').write_bytes(r.stderr);assert r.returncode==0
        log=(n/'applicability.log').read_text();assert not any(x in log for x in ['Overfull','Underfull','LaTeX Warning'])
        r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pngalpha','-r100','-sOutputFile='+str(n/'page-%02d.png'),str(n/'applicability.pdf')],capture_output=True,timeout=30)
        assert r.returncode==0 and not r.stderr
        for i in range(1,4):
            f=n/f'page-{i:02d}.png';assert f.read_bytes()==(here/f'page-{i:02d}.png').read_bytes();native.append(digest(f))
        assert len(list(n.glob('page-*.png')))==3
    rows_check(deps,a.study)
    for r in manifest['exports']:assert digest(here/r['path'])==r['sha256']
    final=dict(status='PASS_FROZEN_BROAD_PRIMITIVE_PREPARATION_COMPONENT',exports=len(manifest['exports']),bindings=len(deps),
      literal_models=7,borel_controls=46,panel_subsets=403,inner_type_classes=160,broad_witnesses=64,non_two_transitive_witnesses=8,
      damaged_controls=len(report['damages']),optimization_guards=opts,native_pages=native,target_runs=0)
    (a.out/'report.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps(final,indent=2))
if __name__=='__main__':main()
