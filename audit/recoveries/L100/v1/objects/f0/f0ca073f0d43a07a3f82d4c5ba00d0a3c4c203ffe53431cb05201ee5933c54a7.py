"""Focused separate-request tests only; never execute the fixed-group search."""
import argparse,ast,copy,json,os,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
import run_target as w
import previous_boundary as b
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();out=args.out
    w.require(out.is_absolute(),'absolute output required');out.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,ok):w.require(ok,name);checks.append(name)
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,OSError):checks.append(name);return
        raise AssertionError('accepted damage '+name)
    old=w.G34/'exhaustion_suffix_interface_v1'
    def funcs(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
    x,y=funcs(old/'run_target.py'),funcs(HERE/'run_target.py')
    names=[n for n in x if n not in {'preflight','main'}]
    check('same function inventory',set(x)==set(y));check('all other inherited functions unchanged',all(x[n]==y[n] for n in names))
    check('literal audit unchanged',(old/'audit_returned.g').read_bytes()==(HERE/'audit_returned.g').read_bytes())
    check('fixed actual and audit caps',w.TARGET_CAP==300 and w.AUDIT_CAP==20)
    prior=json.loads((w.G34/'exhaustion_target02/receipt.json').read_text())
    for anchor in (2,1):b.validate_boundary(prior,[anchor]);checks.append('actual unpaid anchor '+str(anchor))
    for req in [[2,1],[3],[95],[],[1,1]]:reject('invalid request '+str(req),lambda req=req:b.validate_boundary(prior,req))
    for name,change in [
        ('false suffix completion',lambda r:r.update(status='COMPLETE_REQUEST')),
        ('missing paid anchor',lambda r:r['completed_anchors'].pop()),
        ('paid prefix overlaps suffix',lambda r:r['previously_completed_anchors'].append(11)),
        ('unpaid set changed',lambda r:r.update(unpaid_anchors=[1])),
        ('unclosed prior process',lambda r:r['execution'].update(returncode=None)),
        ('failed prior audit',lambda r:r['audit'].update(returncode=1)),
        ('changed prior cap',lambda r:r.update(target_cap_seconds=300)),
    ]:
        r=copy.deepcopy(prior);change(r);reject(name,lambda:b.validate_boundary(r,[2]))
    preps=[]
    for anchor in (2,1):
        dest=out/('anchor'+str(anchor));process=out/('cli'+str(anchor))
        r=w.phase([sys.executable,str(HERE/'run_target.py'),'--anchor',str(anchor),'--prepare-only','--out',str(dest)],process,30,False)
        check('actual prepare CLI '+str(anchor),w.clean_phase(r,process))
        receipt=json.loads((dest/'receipt.json').read_text());req=json.loads((dest/'prepared/request.json').read_text())
        check('only requested anchor '+str(anchor),receipt['requested_anchors']==[anchor] and req['borels']==[anchor])
        check('no target '+str(anchor),receipt['status']=='PREPARED_ONLY_NO_TARGET' and receipt['target_census'] is False and not (dest/'target').exists())
        check('actual cap and other unpaid '+str(anchor),receipt['target_cap_seconds']==300 and receipt['preparer_proposed_cap_seconds']==60 and receipt['other_unpaid_anchor']==3-anchor)
        check('restart distinction '+str(anchor),receipt['unfinished_anchor_restart']==(2 if anchor==2 else None))
        check('all preparation pins '+str(anchor),w.unchanged(receipt['inputs']))
        expected=(w.G34/'exhaustion_target02/prepared/driver.g').read_text().replace(str(w.G34/'exhaustion_target02/prepared/checkpoints'),str(dest/'prepared/checkpoints'))
        expected=expected.replace('BOREL_IDS:='+str(list(range(11,0,-1)))+';;','BOREL_IDS:='+str([anchor])+';;')
        check('literal driver delta '+str(anchor),expected==(dest/'prepared/driver.g').read_text())
        preps.append(w.pin(dest/'receipt.json'))
    for label,extra in [('missing',[]),('paid',['--anchor','3']),('outside',['--anchor','96'])]:
        dest=out/('forbidden_'+label)
        r=subprocess.run([sys.executable,str(HERE/'run_target.py'),'--prepare-only','--out',str(dest)]+extra,capture_output=True,timeout=5)
        check('CLI reject '+label,r.returncode!=0 and not dest.exists())
    dest=out/'forbidden_prior'
    code=('import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'+repr(str(HERE))+');'
          'import run_target as w,previous_boundary as b;b.RECEIPT_SHA="0"*64;'
          'sys.argv=["w","--anchor","2","--prepare-only","--out",'+repr(str(dest))+'];w.main()')
    r=subprocess.run([sys.executable,'-c',code],capture_output=True,timeout=20)
    (out/'damaged_prior.stdout').write_bytes(r.stdout);(out/'damaged_prior.stderr').write_bytes(r.stderr)
    check('actual prior gate before output',r.returncode!=0 and not dest.exists())
    for script in ['run_target.py','previous_boundary.py','controls.py']:
        for mode in ['argument','environment']:
            dest=out/('optimized_'+script+'_'+mode);cmd=[sys.executable]+(['-O'] if mode=='argument' else [])+[str(HERE/script),'--out',str(dest)]
            env=os.environ.copy()
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            r=subprocess.run(cmd,env=env,capture_output=True,timeout=5)
            check('optimization '+script+' '+mode,r.returncode!=0 and not dest.exists() and b'optimized execution forbidden' in r.stderr)
    report=dict(status='PASS_L100_SEPARATE_ANCHOR_CONTROLS_NO_TARGET',checks=checks,target_runs=0,unchanged_functions=names,
                sources=[w.pin(HERE/n) for n in ['run_target.py','previous_boundary.py','audit_returned.g','controls.py']],preparation_receipts=preps)
    w.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],checks=len(checks),target_runs=0)))
if __name__=='__main__':main()
