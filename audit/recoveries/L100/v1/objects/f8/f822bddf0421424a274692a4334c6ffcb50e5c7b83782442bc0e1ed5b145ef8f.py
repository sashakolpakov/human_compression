"""Bounded negative controls for the independent oracle and draft input gate."""
import copy,hashlib,json,pathlib,subprocess,sys,tempfile
if not __debug__:raise SystemExit('optimized execution forbidden')
import literal_oracle as lo
import prepare_driver as prep
HERE=pathlib.Path(__file__).resolve().parent
def must_reject(label,f):
    try:f()
    except (AssertionError,ValueError,IndexError,KeyError,StopIteration):return label
    raise RuntimeError('accepted damaged input: '+label)
def main():
    out=HERE/'damage01';out.mkdir(exist_ok=False)
    model=json.loads((HERE/'rank3_models01/models.json').read_text())[0]
    changes=[]
    def trial(name,mutate):
        bad=copy.deepcopy(model);mutate(bad)
        changes.append(must_reject(name,lambda:lo.check_model('C2xC2xC2',bad)))
    trial('invalid multiplication',lambda m:m[1][0].__setitem__(0,1))
    trial('missing subgroup representative',lambda m:m[2].pop())
    trial('missing maximal inclusion',lambda m:m[3].pop())
    trial('missing Borel output',lambda m:m[4].pop())
    trial('duplicate actual panel',lambda m:m[4][0][1].append(m[4][0][1][0]))
    trial('missing accepted rank3 family',lambda m:m[4][0][2][2].pop())
    trial('duplicate accepted family',lambda m:m[4][0][2][1].append(m[4][0][2][1][0]))
    trial('missing terminal empty level',lambda m:m[4][0][2].pop())
    trial('missing full-group family',lambda m:m[4][0][3].pop())
    trial('out-of-range panel label',lambda m:m[4][0][2][0][0].__setitem__(0,999))
    with tempfile.TemporaryDirectory(dir=out) as td:
        td=pathlib.Path(td)
        inp=HERE/'input_catalogue01.g';src=prep.STUDY/'phase7_sporadic_search.g';fn=HERE/'legacy_functions.g'
        for label,original,which in [('catalogue mutation',inp,0),('legacy mutation',src,1),('function mutation',fn,2)]:
            bad=td/(str(which)+'.g');bad.write_bytes(original.read_bytes()+b'\n')
            args=[inp,src,fn];args[which]=bad
            changes.append(must_reject(label,lambda args=args:prep.validate(*args)))
    opt=[]
    for script in ['literal_oracle.py','prepare_driver.py','damage_controls.py','run_bounded.py']:
        cmd=[sys.executable,'-O',str(HERE/script)]
        p=subprocess.run(cmd,capture_output=True)
        assert p.returncode!=0 and b'optimized execution forbidden' in p.stderr
        opt.append(dict(script=script,returncode=p.returncode,stderr=p.stderr.decode()))
    report=dict(status='PASS_BOUNDED_DAMAGES_NO_TARGET',damages=changes,optimization_guards=opt,target_runs=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
