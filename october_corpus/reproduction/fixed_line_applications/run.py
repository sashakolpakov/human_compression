"""Serial replay dispatcher; scientific validators and per-role banks are separate."""
from pathlib import Path
import argparse,hashlib,json,os,re,resource,stat,subprocess,sys,time

MAX_CASES=8
READ_CAP=64*2**20
META_CAP=16*2**20
READ=0
PINS={}
BATCH_ROOT=None

def need(ok,message):
    if not ok:raise ValueError(message)

def dispatcher_tick():
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    need(peak<=256*2**20,'direct dispatcher256MiB; separate child guards keep their own banks')

def whole(path,cap=2**21):
    global READ
    dispatcher_tick()
    p=Path(path).absolute();a=p.lstat()
    need(p.resolve()==p and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=cap,'ordinary bounded whole input')
    need(READ+a.st_size<=READ_CAP and len(PINS|{str(p):None})<=512,'dispatcher64MiB/512path bank')
    sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    with p.open('rb')as f:
        b=os.fstat(f.fileno());raw=f.read(a.st_size+1);c=os.fstat(f.fileno())
    need(sig(a)==sig(b)==sig(c)==sig(p.lstat())and len(raw)==a.st_size,'stable whole input')
    ref=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    need(str(p)not in PINS or PINS[str(p)]==ref,'one immutable input version')
    PINS[str(p)]=ref;READ+=len(raw);dispatcher_tick();return ref,raw

def doc(path,cap=131072):
    ref,raw=whole(path,cap);return ref,json.loads(raw)

def emit(value):
    dispatcher_tick()
    print(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False),flush=True)
    dispatcher_tick()

def write(path,value):
    raw=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    need(len(raw)<=131072 and not path.exists()and path.parent.resolve()==path.parent,'fresh small completion record')
    metadata_extent(BATCH_ROOT,extra_bytes=len(raw),extra_files=1)
    with path.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return whole(path,131072)[0]

def metadata_extent(root,extra_bytes=0,extra_files=0):
    total=0;count=0
    for p in root.rglob('*'):
        s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'no output symlinks')
        if stat.S_ISREG(s.st_mode):
            # Scientific proof/result pairs retain their own existing output banks.
            if p.name not in('proof.json','result.json'):total+=s.st_size
            count+=1
    need(total+extra_bytes<=META_CAP and count+extra_files<=512,'dispatcher metadata16MiB/512file bound')
    return total

def main():
    global BATCH_ROOT
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'require-E-B-S/no-O')
    p=argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('root',type=Path);p.add_argument('out',type=Path)
    p.add_argument('start',type=int);p.add_argument('stop',type=int)
    p.add_argument('--python',default=sys.executable)
    p.add_argument('--end',choices=('left','right'),default='right')
    a=p.parse_args();root=a.root.resolve(strict=True);common=root.parent/'fixed_line_orbits';out=a.out.absolute()
    need(root.is_dir()and common.resolve(strict=True)==common,'actual application/common roots')
    cases=sorted(x for x in(root/'cases').iterdir()if x.is_dir()and re.fullmatch(r'position[0-9]{4}_'+a.end,x.name))
    need(0<=a.start<a.stop<=len(cases)and a.stop-a.start<=MAX_CASES,'explicit nonempty case window of at most8')
    need(out.parent.resolve(strict=True)==out.parent and not os.path.lexists(out),'fresh batch output; preserve earlier partials')
    py=Path(a.python).absolute();need(py.is_file(),'existing literal Python interpreter path');guard=common/'runtime/supervise_validation.py'
    BATCH_ROOT=out
    source_files=[Path(__file__).resolve(),root/'acquisition/acquire.py',root/'close_replay.py',guard,
        common/'runtime/supervise_transient.py',common/'word19/consume.py',common/'reachable/consume.py']
    source_pins=[whole(x,65536)[0]for x in source_files]
    wm=common/'word19/source_manifest.json';rm=common/'reachable/source_manifest.json'
    wref,_=whole(wm,16384);rref,_=whole(rm,16384)
    out.mkdir();(out/'guards').mkdir();completed=[];began=time.monotonic()
    try:
        for directory in cases[a.start:a.stop]:
            cref,case=doc(directory/'case.json',16384)
            need(case['schema']=='F004_FIXED_LINE_PORTABLE_CASE_V1'and case['end']==a.end and case['end_id']==directory.name,'exact selected case metadata')
            files={name:whole(directory/name,131072)[0]for name in ['acquisition.json','word_job.json','reachable_job.json']}
            caseout=out/directory.name;caseout.mkdir();scope_inputs=[cref]+list(files.values())
            roles=[('original',[str(root/'acquisition/acquire.py'),files['acquisition.json']['path'],files['acquisition.json']['sha256'],str(caseout/'original')]),
                ('word',[str(common/'word19/consume.py'),str(wm),wref['sha256'],files['word_job.json']['path'],files['word_job.json']['sha256'],str(caseout/'word')]),
                ('reachable',[str(common/'reachable/consume.py'),str(rm),rref['sha256'],files['reachable_job.json']['path'],files['reachable_job.json']['sha256'],str(caseout/'reachable')]),
                ('join',[str(root/'close_replay.py'),str(caseout/'original/proof.json'),str(caseout/'word'),str(caseout/'reachable'),str(directory),str(common),str(caseout/'join')])]
            records=[]
            for role,args in roles:
                command=[str(py),'-E','-B','-S']+args;gdir=out/'guards'/(directory.name+'_'+role)
                cwd=common/'word19'if role=='word'else common/'reachable'if role=='reachable'else root
                argv=[str(py),'-E','-B',str(guard),'--volume',str(out),'--output',str(gdir),'--rss-cap-mib','128','--timeout','150','--']+command
                emit(dict(event='role_command',case=directory.name,role=role,cwd=str(cwd),argv=argv))
                dispatch_out=caseout/(role+'_guard_stdout.log');dispatch_err=caseout/(role+'_guard_stderr.log')
                with dispatch_out.open('xb')as stdout,dispatch_err.open('xb')as stderr:
                    dispatcher_tick()
                    result=subprocess.run(argv,cwd=cwd,stdout=stdout,stderr=stderr,check=False)
                    dispatcher_tick()
                metadata_extent(out)
                _,derr=whole(dispatch_err,262144);_,draw=whole(dispatch_out,262144)
                need(result.returncode==0 and derr==b'','guard refused or failed; preserve partials and use a fresh retry output')
                summary=json.loads(draw);gref,g=doc(gdir/'receipt.json')
                need(summary==dict(status='PASS',stop='RETURNED',receipt=str(gdir/'receipt.json'))
                    and g['status']=='PASS'and g['stop']=='RETURNED'and g['returncode']==0 and g['error']is None
                    and g['command']==command and g['limits']['total_rss']==128*2**20 and g['limits']['wall_seconds']==150
                    and g['cleanup']['remaining']==g['cleanup']['errors']==[],'exact actual successful role guard')
                sref,sout=doc(gdir/'stdout.log');eref,serr=whole(gdir/'stderr.log',262144);need(serr==b'','scientific role stderr')
                expected={'original':'ORIGINAL_QUARTET_RECONSTRUCTED_ONLY','word':'VERIFIED_END_WORD_ORDER19_AND_FIXED_SEED_ONLY',
                    'reachable':'VERIFIED_9241_REACHABLE_AND_ORDER19_STABILIZER_ONLY'}
                if role!='join':need(sout['status']==expected[role],'inconclusive or wrong scientific role result')
                else:need(sout['position']==case['position']and sout['representative_J_index']==case['representative_J_index']
                    and sout['end']==a.end.upper()and sout['conditional_conclusion']==a.end.upper()+'_EQUALS_G2_11_AND_ORIGINAL_MARKING_FAILS_IP','complete matching final join')
                artifacts=[whole(caseout/role/name,131072)[0]for name in(['result.json']if role=='join'else['proof.json','result.json'])]
                records.append(dict(role=role,command=command,cwd=str(cwd),guard=gref,stdout=sref,stderr=eref,artifacts=artifacts))
                emit(dict(event='role_complete',case=directory.name,role=role,guard=gref))
            for ref in scope_inputs+source_pins+[wref,rref]:need(whole(ref['path'],max(ref['bytes'],1))[0]==ref,'closing current inputs unchanged')
            completion=write(caseout/'completion.json',dict(schema='F004_FIXED_LINE_PUBLIC_CASE_REPLAY_V1',case=case,
                status='PASS_FOUR_SEPARATE_GUARDED_ROLES',inputs=scope_inputs,sources=source_pins,manifests=[wref,rref],roles=records,
                Root_authority=False,new_original_conjecture_Lean_measurement_credit=0))
            completed.append(completion);emit(dict(event='case_complete',case=directory.name,completion=completion))
        batch=write(out/'batch_complete.json',dict(status='PASS_SELECTED_CASE_WINDOW',start=a.start,stop=a.stop,
            total_available_cases=len(cases),selected_end=a.end,completed=completed,dispatcher_read_bytes=READ,dispatcher_metadata_bytes=metadata_extent(out),
            seconds=time.monotonic()-began,separate_scientific_role_banks=True,Root_authority=False,new_credit=0))
        emit(dict(event='batch_complete',record=batch,cases=len(completed)))
    except BaseException as exc:
        failed=dict(event='FAILED_STOPPED',completed_cases=len(completed),error_type=type(exc).__name__,error=str(exc),partials_preserved=str(out))
        try:write(out/'batch_failed.json',failed)
        except Exception:pass
        emit(failed)
        raise

if __name__=='__main__':main()
