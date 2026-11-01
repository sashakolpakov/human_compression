"""Mechanical joining/file controls; imports no matrix reader."""
import copy,hashlib,json,os,stat,sys,tempfile,types
from pathlib import Path
ROOT=Path(__file__).resolve().parent
READ=0
def bounded(path,cap,pin=None):
    global READ
    a=path.lstat();assert path.resolve(strict=True)==path and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and 0<a.st_size<=cap
    sig=lambda z:(z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
    with path.open('rb')as f:q=os.fstat(f.fileno());raw=f.read(cap+1);z=os.fstat(f.fileno())
    assert sig(a)==sig(q)==sig(z)==sig(path.lstat())and len(raw)==a.st_size
    if pin is not None:assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256']
    READ+=len(raw);assert READ<=8388608;return raw
def load(name,path,pin):
    raw=bounded(path,16384,pin);m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(raw,str(path),'exec'),m.__dict__);return m
def main():
    assert sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
    assert len(sys.argv)==2
    raw=bounded(ROOT/'data/control_manifest.json',16384);assert hashlib.sha256(raw).hexdigest()==sys.argv[1]
    manifest=json.loads(raw);pins=manifest['sources']
    assert set(pins)=={'controls.py','close_replay.py','acquisition/acquire.py','runtime/supervise_validation.py','runtime/supervise_transient.py'}and sum(p['bytes']for p in pins.values())<=65536
    for name,pin in pins.items():bounded(ROOT/name,32768,pin)
    j=load('join_controls',ROOT/'close_replay.py',pins['close_replay.py']);a=load('acquire_controls',ROOT/'acquisition/acquire.py',pins['acquisition/acquire.py'])
    passed=[]
    def check(name,fn):
        assert fn();passed.append(name)
    def refuse(name,fn):
        try:fn()
        except(ValueError,KeyError,TypeError,IndexError):passed.append(name);return
        raise AssertionError(name)
    marks=[['A'],['B'],['C'],['E']]
    acquired=dict(schema='F004_FIXED_LINE_ORIGINAL_REPLAY_V1',position=59,representative_J_index=136,
        status='ORIGINAL_QUARTET_RECONSTRUCTED_ONLY',marks=marks,marks_sha256=hashlib.sha256(j.can(marks)).hexdigest())
    cert=dict(word=[0,1],seed=[1,0,0,0,0,0,0],kernel={'synthetic':'opaque'})
    wjob=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_V1',end_id='position0059_right',end_marks=marks[1:],certificate=cert)
    rjob=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_V1',end_id='position0059_right',end_marks=marks[1:],word=cert['word'],seed=cert['seed'],certificate={'n':9241,'synthetic':'opaque'})
    wp=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_PROOF_V1',end_id=wjob['end_id'],certificate=cert,supplier_or_solver_imported=False)
    rp=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_PROOF_V1',end_id=rjob['end_id'],certificate=rjob['certificate'],supplier_discovery_or_solver_imported=False)
    wr=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_RESULT_V1',answer=dict(status='VERIFIED_END_WORD_ORDER19_AND_FIXED_SEED_ONLY',word=cert['word'],selected_seed=cert['seed'],fixed_dimension=1,exact_prime_order=19))
    rr=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_RESULT_V1',answer=dict(status='VERIFIED_9241_REACHABLE_AND_ORDER19_STABILIZER_ONLY',reachable_distinct=9241,parent_images_verified=9240,concrete_end_order_lower_bound=175579))
    base=[acquired,wjob,wp,wr,rjob,rp,rr]
    check('complete same-payload mechanical join',lambda:j.joined(*base)['end_order_lower_bound']==175579)
    for key,value in [('fixed_dimension',True),('fixed_dimension',2),('exact_prime_order',True)]:
        bad=copy.deepcopy(base);bad[3]['answer'][key]=value
        refuse('wrong or Boolean '+key,lambda bad=bad:j.joined(*bad))
    for key,value in [('reachable_distinct',9240),('parent_images_verified',True),('status','INCONCLUSIVE_UNPAID')]:
        bad=copy.deepcopy(base);bad[6]['answer'][key]=value
        refuse('wrong reachable '+key,lambda bad=bad:j.joined(*bad))
    bad=copy.deepcopy(base);bad[4]['end_marks'].reverse();refuse('different actual end',lambda:j.joined(*bad))
    bad=copy.deepcopy(base);bad[4]['word']=[1,0];refuse('different word',lambda:j.joined(*bad))
    bad=copy.deepcopy(base);bad[5]['certificate']={'n':9240};refuse('different parent certificate',lambda:j.joined(*bad))
    bad=copy.deepcopy(base);bad[2]['supplier_or_solver_imported']=True;refuse('supplier cannot impersonate independent consumer',lambda:j.joined(*bad))
    refuse('duplicate JSON fields',lambda:j.decode(b'{"x":1,"x":2}'))
    refuse('nonfinite JSON',lambda:j.decode(b'{"x":NaN}'))
    check('finite elapsed timing metadata',lambda:j.decode(b'{"counts":{"elapsed_seconds":0.125}}')['counts']['elapsed_seconds']==0.125)
    refuse('floating scientific value',lambda:j.decode(b'{"answer":{"fixed_dimension":1.0}}'))
    refuse('overflowed elapsed timing',lambda:j.decode(b'{"counts":{"elapsed_seconds":1e999}}'))
    with tempfile.TemporaryDirectory()as d:
        p=Path(d).resolve()/'body';p.write_bytes(b'good');h=hashlib.sha256(b'good').hexdigest()
        check('stable ordinary whole read',lambda:a.whole(p,dict(bytes=4,sha256=h))==b'good')
        refuse('wrong digest',lambda:a.whole(p,dict(bytes=4,sha256='0'*64)))
        q=p.with_name('alias');os.link(p,q);refuse('hardlinked input',lambda:a.whole(p,dict(bytes=4,sha256=h)));q.unlink()
        p.write_bytes(b'x'*262145);refuse('join pre-read size bound',lambda:j.Inputs().read(p))
    assert len(passed)==20
    for name,pin in pins.items():bounded(ROOT/name,32768,pin)
    print(json.dumps(dict(schema='F004_FIXED_LINE_PORTABLE_MECHANICAL_CONTROLS_V1',checks=passed,
        checked=20,project_read_bytes=READ,scientific_matrix_reader_or_cases_imported=False,Root_authority=False),sort_keys=True))
if __name__=='__main__':main()
