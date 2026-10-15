"""Only changed suffix boundary/preparation/cap controls; no target or old-control replay."""
import argparse
import ast
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
if not __debug__:
    raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
import run_target as w
import previous_boundary as b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    out = args.out
    w.require(out.is_absolute(), 'absolute output required')
    out.mkdir(parents=True, exist_ok=False)
    checks = []
    def check(name, ok):
        w.require(ok, name);checks.append(name)
    def reject(name, fn):
        try:fn()
        except (ValueError, KeyError, OSError):checks.append(name);return
        raise AssertionError('accepted damage ' + name)
    old = w.G34 / 'exhaustion_target_interface_v1'
    def funcs(p):
        return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
    a,c=funcs(old/'run_target.py'),funcs(HERE/'run_target.py')
    check('identical function inventory',set(a)==set(c))
    preserved=[k for k in a if k not in {'preflight','validate_preparation','main'}]
    check('all other function ASTs unchanged',all(a[k]==c[k] for k in preserved))
    check('literal audit helper unchanged',(old/'audit_returned.g').read_bytes()==(HERE/'audit_returned.g').read_bytes())
    check('exact disjoint suffix',w.IDS==b.SUFFIX and not set(w.IDS)&set(b.PREFIX))
    check('exact actual cap and unchanged audit cap',w.TARGET_CAP==180 and w.AUDIT_CAP==20)
    prior=json.loads((w.G34/'exhaustion_target01/receipt.json').read_text())
    b.validate_boundary(prior);checks.append('actual previous boundary')
    for name,mutation in [
        ('prior falsely complete',lambda r:r.update(status='COMPLETE_REQUEST')),
        ('prior missing completed anchor',lambda r:r['completed_anchors'].pop()),
        ('prior unpaid overlap',lambda r:r['unpaid_anchors'].insert(0,12)),
        ('prior unclosed target',lambda r:r['execution'].update(returncode=None)),
        ('prior changed cap',lambda r:r.update(target_cap_seconds=180)),
        ('prior failed audit',lambda r:r['audit'].update(returncode=1)),
        ('prior changed row',lambda r:r['audited_returned_rows'].pop()),
    ]:
        r=copy.deepcopy(prior);mutation(r);reject(name,lambda:b.validate_boundary(r))
    prepout=out/'prepared_suffix'
    r=w.phase([sys.executable,str(HERE/'run_target.py'),'--prepare-only','--out',str(prepout)],out/'prepare_cli',25,False)
    check('actual suffix preparation CLI',w.clean_phase(r,out/'prepare_cli'))
    receipt=json.loads((prepout/'receipt.json').read_text())
    req=json.loads((prepout/'prepared/request.json').read_text())
    check('no target execution',receipt['status']=='PREPARED_ONLY_NO_TARGET' and receipt['target_census'] is False and not (prepout/'target').exists())
    check('actual suffix and documented cap override',req['borels']==w.IDS and req['proposed_external_cap_seconds']==60 and receipt['target_cap_seconds']==180 and receipt['preparer_proposed_cap_seconds']==60)
    check('previous exact receipt retained',receipt['previous_receipt']['sha256']==b.RECEIPT_SHA)
    check('new pins exact',w.unchanged(receipt['inputs']))
    old_driver=(w.G34/'exhaustion_target01/prepared/driver.g').read_text()
    expected=old_driver.replace(str(w.G34/'exhaustion_target01/prepared/checkpoints'),str(prepout/'prepared/checkpoints'))
    expected=expected.replace('BOREL_IDS:='+str(list(range(95,0,-1)))+';;','BOREL_IDS:='+str(w.IDS)+';;')
    check('literal driver only output path and requested IDs differ',expected==(prepout/'prepared/driver.g').read_text())
    check('partial old checkpoints never loaded','exhaustion_target01' not in expected)
    # Actual main rejects the exact prior receipt hash damage before creating output.
    forbidden=out/'forbidden_prior'
    code=('import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'+repr(str(HERE))+');'
          'import run_target as w,previous_boundary as b;b.RECEIPT_SHA="0"*64;'
          'sys.argv=["w","--prepare-only","--out",'+repr(str(forbidden))+'];w.main()')
    r=subprocess.run([sys.executable,'-c',code],capture_output=True,timeout=15)
    (out/'damaged_prior.stdout').write_bytes(r.stdout);(out/'damaged_prior.stderr').write_bytes(r.stderr)
    check('actual prior gate before output',r.returncode!=0 and not forbidden.exists())
    for script in ['run_target.py','controls.py','previous_boundary.py']:
        for mode in ['argument','environment']:
            forbidden=out/('optimized_'+script+'_'+mode)
            cmd=[sys.executable]+(['-O'] if mode=='argument' else [])+[str(HERE/script),'--out',str(forbidden)]
            env=os.environ.copy()
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            r=subprocess.run(cmd,capture_output=True,env=env,timeout=5)
            check('optimization '+script+' '+mode,r.returncode!=0 and not forbidden.exists() and b'optimized execution forbidden' in r.stderr)
    report=dict(status='PASS_L100_SUFFIX_BOUNDARY_CONTROLS_NO_TARGET',target_runs=0,checks=checks,
                unchanged_functions=preserved,prior_receipt=w.pin(w.G34/'exhaustion_target01/receipt.json'),
                sources=[w.pin(HERE/n) for n in ['run_target.py','audit_returned.g','previous_boundary.py','controls.py']],
                preparation_receipt=w.pin(prepout/'receipt.json'))
    w.save(out/'report.json',report)
    print(json.dumps(dict(status=report['status'],checks=len(checks),target_runs=0)))
if __name__=='__main__':main()
