"""Declared arithmetic budgets and whole-file IO. No Root authority is created."""
import hashlib,json,os,resource,stat,sys,time
from pathlib import Path
CAPS=dict(matrix_products=400000,row_images=200000,linear_units=200000,
          read_bytes=8388608,paths=96,source_bytes=65536,
          rss_bytes=134217728,seconds=100,output_files=2,output_bytes_each=131072)
SOURCE_NAMES={'runtime.py','field.py','algebra.py','solve.py','schreier.py','request.py','propose.py','consume.py','controls.py'}
ENV4=('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')
EXTERNAL_RUNTIME={
 'supervise_validation.py':(4806,'c3b626b86791ac355c3503a654136f49ad76abbcdfadf0455efb32dd5cca25f4'),
 'supervise_transient.py':(18361,'5c7eed80537835e1a78c8489621d34741eeafc01f47fb394fec519e83f2c9b42')}
class Limit(RuntimeError):pass

def need(ok,message):
    if not ok:raise ValueError(message)

def duplicate_free(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out

def decode(data):
    def bad_number(_):raise ValueError('only integer JSON numbers')
    return json.loads(data,object_pairs_hook=duplicate_free,parse_float=bad_number,parse_constant=bad_number)

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')+b'\n'

def digest(data):return hashlib.sha256(data).hexdigest()

def ref(value):
    need(type(value)is dict and set(value)=={'path','bytes','sha256'},'whole-file descriptor')
    need(type(value['path'])is str and 0<len(value['path'])<=4096,'bounded file path')
    need(type(value['bytes'])is int and 0<=value['bytes']<=8388608,'bounded byte count')
    h=value['sha256'];need(type(h)is str and len(h)==64 and all(c in '0123456789abcdef'for c in h),'whole SHA256')
    return value

class Budget:
    Limit=Limit
    def __init__(self):
        self.started=time.monotonic();self.calls=0;self.products=0;self.rows=0;self.linear=0
        self.read_bytes=0;self.explicit_read_bytes=0;self.import_source_reserved_bytes=0
        self.paths=set();self.reads=[];self.peak_rss=0
    def tick(self):
        self.calls+=1
        if time.monotonic()-self.started>90:raise Limit('90 second cooperative deadline; outer role remains 100/150 seconds')
        if self.calls%256==1:
            rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys.platform!='darwin':rss*=1024
            self.peak_rss=max(self.peak_rss,rss)
            if rss>117440512:raise Limit('112 MiB cooperative RSS; outer role remains 128 MiB')
    def scalar(self,n):
        self.tick();need(type(n)is int and n>=0,'nonnegative linear debit')
        if self.linear+n>CAPS['linear_units']:raise Limit('shared 200000 linear-unit bank')
        self.linear+=n
    def multiply(self,a,b):
        self.tick()
        if self.products>=CAPS['matrix_products']:raise Limit('400000 complete matrix products')
        self.products+=1
        return bytes(sum(a[7*i+k]*b[7*k+j]for k in range(7))%11 for i in range(7)for j in range(7))
    def image(self,v,a):
        self.tick()
        if self.rows>=CAPS['row_images']:raise Limit('200000 complete row images')
        self.rows+=1
        return bytes(sum(v[k]*a[7*k+j]for k in range(7))%11 for j in range(7))
    def read(self,path,expected=None,cap=4194304):
        self.tick();p=Path(path)
        need(not p.is_symlink(),'no symlink input')
        p=p.resolve(strict=True);name=str(p)
        need(len(self.paths|{name})<=CAPS['paths'],'96 distinct whole input paths')
        flags=os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)
        fd=os.open(name,flags)
        try:
            before=os.fstat(fd);need(stat.S_ISREG(before.st_mode)and before.st_nlink==1 and before.st_size<=cap,'bounded regular single-link whole input')
            need(self.read_bytes+before.st_size<=CAPS['read_bytes'],'8 MiB cumulative physical input reads')
            with os.fdopen(fd,'rb',closefd=False)as f:data=f.read(before.st_size+1)
            after=os.fstat(fd)
            signature=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
            need(signature(before)==signature(after)==signature(p.lstat())
                 and len(data)==before.st_size,'stable whole read including EOF')
        finally:os.close(fd)
        self.read_bytes+=len(data);self.explicit_read_bytes+=len(data);self.paths.add(name)
        got=dict(path=name,bytes=len(data),sha256=digest(data))
        if expected is not None:
            ref(expected);need(got['bytes']==expected['bytes']and got['sha256']==expected['sha256'],'whole-file size and digest')
        self.reads.append(got);return data
    def snapshot(self):
        self.tick();return dict(matrix_products=self.products,row_images=self.rows,linear_units=self.linear,
            read_bytes=self.read_bytes,explicit_read_bytes=self.explicit_read_bytes,
            import_source_reserved_bytes=self.import_source_reserved_bytes,
            distinct_read_paths=len(self.paths),whole_read_events=len(self.reads),
            whole_read_sequence_sha256=digest(encoded(self.reads)),
            elapsed_microseconds=int((time.monotonic()-self.started)*1000000),peak_rss_bytes=self.peak_rss)

def startup(manifest_path,manifest_sha,job_path,job_sha):
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'require -E -B -S without -O')
    need(all(name not in os.environ for name in ENV4),'original matrix-role ENV4 variables absent')
    b=Budget();raw=b.read(manifest_path,cap=65536);need(digest(raw)==manifest_sha,'Root-selected manifest digest')
    need(len(raw)<=65536,'bounded manifest before JSON decoding')
    m=decode(raw);need(type(m)is dict and set(m)=={'schema','caps','sources','external_runtime'},'complete Source manifest')
    need(m['schema']=='F004_SMALL_STABILIZER_SCHREIER_ORDER_SOURCE_V1'and m['caps']==CAPS,'unchanged declared caps')
    files=m['sources'];need(type(files)is list and len(files)==9,'nine whole worker Source files')
    names=[x['path']for x in files];need(set(names)==SOURCE_NAMES and len(set(names))==9,'exact complete worker Source namespace')
    total=0;base=Path(manifest_path).resolve().parent
    for x in files:
        ref(x);need(Path(x['path']).name==x['path'],'same-directory Source only')
        data=b.read(base/x['path'],x);total+=len(data)
    external=m['external_runtime'];need(type(external)is list and len(external)==2,'two disclosed external guard Sources')
    used=set();external_total=0
    for x in external:
        ref(x);name=Path(x['path']).name
        need(name in EXTERNAL_RUNTIME and name not in used and (x['bytes'],x['sha256'])==EXTERNAL_RUNTIME[name],'exact acquired external runtime')
        used.add(name);external_total+=len(b.read(x['path'],x))
    need(total+external_total<=CAPS['source_bytes'],'worker plus disclosed external runtime union at most65536')
    # Nominal project bootstrap bodies are additional to explicit Source pins.
    # The supervisor reads the transient body twice then loads it once.
    reserved=total+4806+3*18361
    need(b.read_bytes+reserved<=CAPS['read_bytes'],'project bootstrap reservation in the same 8 MiB bank')
    b.read_bytes+=reserved;b.import_source_reserved_bytes=reserved
    body=b.read(job_path,cap=262144);need(digest(body)==job_sha,'Root-selected whole arithmetic job digest')
    need(len(body)<=262144,'256 KiB arithmetic job before JSON decoding')
    job=decode(body);need(type(job)is dict,'complete job object')
    need(Path(__file__).resolve()==base/'runtime.py','actual runtime origin is the manifest directory')
    return b,job,dict(manifest_sha256=manifest_sha,job_sha256=job_sha,manifest_directory=str(base),worker_Source_union_bytes=total,
        external_runtime_Source_bytes=external_total,combined_Source_union_bytes=total+external_total,
        source_names=sorted(names),Root_authority_created=False)

def origins(pins,script_file,modules):
    base=Path(pins['manifest_directory']);script=Path(script_file).resolve()
    need(script.parent==base and script.name in {'propose.py','consume.py','controls.py'},'actual reviewed caller origin')
    need(Path(__file__).resolve()==base/'runtime.py','actual reviewed runtime origin')
    for module in modules:
        name=module.__name__+'.py'
        need(name in SOURCE_NAMES and Path(module.__file__).resolve()==base/name,'all actually loaded scientific module origins')
        for value in vars(module).values():
            if type(value).__name__=='function'and value.__module__==module.__name__:
                need(value.__globals__ is vars(module)and Path(value.__code__.co_filename).resolve()==base/name,'whole actual function body/globals origin')
        for cls in vars(module).values():
            if isinstance(cls,type)and cls.__module__==module.__name__:
                for method in cls.__dict__.values():
                    if type(method).__name__=='function':
                        need(method.__globals__ is vars(module)and Path(method.__code__.co_filename).resolve()==base/name,'actual helper class method origins')
    current=sys.modules[__name__]
    for value in vars(current).values():
        if type(value).__name__=='function'and value.__module__==__name__:
            need(value.__globals__ is vars(current)and Path(value.__code__.co_filename).resolve()==base/'runtime.py','actual runtime function origin')
    for value in Budget.__dict__.values():
        if type(value).__name__=='function':
            need(value.__globals__ is vars(current)and Path(value.__code__.co_filename).resolve()==base/'runtime.py','actual arithmetic Budget method origin')
    caller=sys._getframe(1).f_globals
    for value in caller.values():
        if type(value).__name__=='function'and value.__module__==caller['__name__']:
            need(value.__globals__ is caller and Path(value.__code__.co_filename).resolve()==script,'whole actual caller function origin')


def close_inputs(b):
    for r in list(b.reads):b.read(r['path'],r)

def provenance(job,b):
    """Pin supplied context files without interpreting their scientific authority."""
    refs=job['context_refs'];need(type(refs)is list and len(refs)<=80,'finite explicit context bank')
    seen=set()
    for x in refs:
        ref(x);name=str(Path(x['path']).resolve(strict=True));need(name not in seen,'no duplicate context role')
        seen.add(name);b.read(x['path'],x)
    return dict(pinned_context_files=len(refs),local_pins_issue_Root_authority=False,
        original_marking_frame_and_current_scope_joins='EXTERNAL_ROOT_DUTIES_NOT_INFERRED_FROM_HASHES')

def emit(outdir,result,proof,b):
    p=Path(outdir);need(p.is_absolute()and p.is_relative_to('/private/tmp')and p.parent.resolve(strict=True)==p.parent and not p.exists(),'fresh canonical private output directory')
    need(p.parent.is_dir()and not p.parent.is_symlink(),'existing regular output parent')
    bodies=[encoded(result),encoded(proof)]
    need(all(len(x)<=CAPS['output_bytes_each']for x in bodies),'two outputs at most 128 KiB each')
    need(len(b.paths|{str(p.resolve()/'result.json'),str(p.resolve()/'proof.json')})<=CAPS['paths'],'96 paths including outputs')
    b.tick();p.mkdir()
    for name,data in zip(('result.json','proof.json'),bodies):
        with open(p/name,'xb')as f:f.write(data)
    return [dict(path=str((p/name).resolve()),bytes=len(data),sha256=digest(data))for name,data in zip(('result.json','proof.json'),bodies)]

def arguments(argv):
    need(len(argv)==6,'manifest manifestSHA job jobSHA fresh-output-dir')
    return argv[1:]

def emit_carrier(outdir,carrier,proposal,b):
    p=Path(outdir);values=[('certificate.bin',carrier),('proposal.json',encoded(proposal))]
    need(p.is_absolute()and p.is_relative_to('/private/tmp')and p.parent.resolve(strict=True)==p.parent
         and not os.path.lexists(p),'fresh private carrier output directory')
    need(type(carrier)is bytes and 19<=len(carrier)<=121315 and len(values[1][1])<=32768
         and len(b.paths|{str(p/name)for name,body in values})<=96,'prospective two128KiB carrier/proposal outputs')
    b.tick();p.mkdir();refs=[]
    for name,body in values:
        with(p/name).open('xb')as stream:
            need(stream.write(body)==len(body),'whole exclusive write');stream.flush();os.fsync(stream.fileno())
        refs.append(dict(path=str(p/name),bytes=len(body),sha256=digest(body)))
    b.tick();return refs
