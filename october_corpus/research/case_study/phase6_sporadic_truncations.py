#!/usr/bin/env python3
"""Certify both truncation conventions for an already independently verified census."""
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('group',choices=['J1','M11','M12'])
    ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('Set GAP or pass --gap')
    source=HERE/'phase6_sporadic_truncations.g';witness=HERE/f'phase6_sporadic_{a.group}_representatives.g';log=HERE/f'phase6_sporadic_{a.group}_truncations.log'
    digest=sha(source);wdigest=sha(witness);start=time.monotonic()
    cmd=f'GROUP_NAME:="{a.group}";WITNESS_FILE:="{witness.name}";Read("{source.name}");QUIT;'
    with log.open('w') as f:r=subprocess.run([a.gap,'-q','-c',cmd],cwd=HERE,stdout=f,stderr=subprocess.STDOUT)
    out=log.read_text();passed=r.returncode==0 and 'TRUNCATION_CONVENTIONS_COMPLETE' in out and 'Error,' not in out and sha(source)==digest and sha(witness)==wdigest
    counts=[dict(rank=int(m[1]),restricted_nontruncations=int(m[2]),broader_nontruncations=int(m[3])) for m in re.finditer(r'TRUNCATION_COUNTS rank=(\d+) restricted_nontruncations=(\d+) broad_nontruncations=(\d+)',out)]
    report=dict(passed=passed,group=a.group,script=source.name,executed_sha256=digest,runner_sha256=sha(Path(__file__)),witness_file=witness.name,witness_sha256=wdigest,log=log.name,log_sha256=sha(log),exit_code=r.returncode,seconds=time.monotonic()-start,counts=counts,conventions=dict(restricted='Truncations of locally 2T RWPRI geometries only',broader='Truncations of any RWPRI geometry satisfying the other axioms'),scope='Post-processing of the independently exhausted Aut(G)/type census; both conventions are reported without fitting to a published count.')
    (HERE/f'phase6_sporadic_{a.group}_truncations.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=passed,group=a.group,counts=counts,seconds=report['seconds']),indent=2))
    if not passed:raise SystemExit(1)
if __name__=='__main__':main()
