#!/usr/bin/env python3
"""Exercise early integrity checks, without repeating the mathematical programs."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
    manifest=json.loads((ROOT/'manifest.json').read_text());results=[]
    for name in ['changed_proof','missing_program','lost_source_row','omitted_program_print']:
        d=a.out/name;d.mkdir()
        for row in manifest['exports']:
            p=d/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/row['path'],p)
        m=json.loads(json.dumps(manifest));changed=[]
        if name=='changed_proof':
            p=d/'sections/04-periods.tex';p.write_text(p.read_text()+'\nChanged proof control.\n');expected='binding sections/04-periods.tex'
        elif name=='missing_program':
            p=d/'scope.json';x=json.loads(p.read_text());x['programs'].pop();p.write_text(json.dumps(x));changed=[p];expected='six complete required programs'
        elif name=='lost_source_row':
            p=d/'scope.json';x=json.loads(p.read_text());x['source_rows'].pop();p.write_text(json.dumps(x));changed=[p];expected='complete fixed source rows'
        else:
            p=d/'required-programs.tex';p.write_text(p.read_text().replace('programs/phase250_affine_check.py','programs/omitted.py'));changed=[p]
            q=d/'scope.json';x=json.loads(q.read_text())
            for row in x['editions']:
                if row['path']=='required-programs.tex':row.update(bytes=p.stat().st_size,sha256=sha(p))
            q.write_text(json.dumps(x));changed.append(q);expected='full program inclusion directives'
        for p in changed:
            for row in m['exports']:
                if row['path']==str(p.relative_to(d)):row.update(bytes=p.stat().st_size,sha256=sha(p))
        (d/'manifest.json').write_text(json.dumps(m))
        # These mutations must fail before any tool is invoked. Deliberately invalid
        # executable paths catch an accidental traversal into the mathematical stage.
        p=subprocess.run([sys.executable,'-B','-O',d/'check.py','--out',a.out/(name+'_output'),'--gap','/unused','--lean','/unused','--packages','/unused'],text=True,capture_output=True)
        need(p.returncode!=0 and expected in p.stderr,name+' did not fail as expected')
        results.append(dict(control=name,rejected=True,expected=expected,returncode=p.returncode))
    report=dict(status='PASS',checker_sha256=sha(ROOT/'check.py'),python_optimized=True,scope='Early packet integrity and completeness checks; not independent mathematical review.',controls=results)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
