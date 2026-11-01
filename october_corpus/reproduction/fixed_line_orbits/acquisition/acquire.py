"""Reconstruct one original quartet using the unchanged public matrix reader."""
import hashlib,json,os,resource,stat,sys,time,types
from pathlib import Path
START=time.monotonic()
ROOT=Path(__file__).resolve().parent
s=None
READ=0
SEEN={}
def need(ok,message):
    if not ok:raise ValueError(message)
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')
def unique(rows):
    out={}
    for k,v in rows:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def decode(raw):
    def bad(x):raise ValueError('integer JSON only')
    return json.loads(raw,object_pairs_hook=unique,parse_float=bad,parse_constant=bad)
def sig(x):return(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
def tick():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    need(time.monotonic()-START<90 and rss<112*2**20,'soft90s/112MiB; outer100s/128MiB')
    need(READ+(s.READ if s else 0)<=8*2**20 and len(SEEN)<=94,'one8MiB/96path bank')
    if s:need(sum(s.PRODUCTS.values())<=400000 and s.FIELD<=200000,'one arithmetic bank')
def whole(path,pin=None):
    global READ
    path=Path(path).absolute();need(path.resolve(strict=True)==path,'ordinary canonical path')
    a=path.lstat();need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and 0<a.st_size<=2**21,'bounded ordinary file')
    need(READ+(s.READ if s else 0)+a.st_size<=8*2**20,'pre-read8MiB bank')
    with path.open('rb')as f:
        q=os.fstat(f.fileno());raw=f.read(a.st_size+1);z=os.fstat(f.fileno())
    need(sig(a)==sig(q)==sig(z)==sig(path.lstat())and len(raw)==a.st_size,'whole stable bytes')
    got=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    need(pin is None or all(pin[k]==got[k]for k in got),'whole supplied pin')
    need(str(path)not in SEEN or SEEN[str(path)]==got,'one input version')
    READ+=len(raw);SEEN[str(path)]=got;tick();return raw
class Context:
    def document(self,directory,pin):
        s.DATA=directory
        value=s.document(pin);whole(directory/pin['file'],pin);return value
    def multiply(self,a,b):return s.mul(a,b)

def original_context(b,s,m,shared):
    need(set(m['shared_data'])=={'domain','prefix','ambient_frame'},'exact shared context domain')
    domain,prefix,frame=[b.document(shared/'data',m['shared_data'][k])for k in('domain','prefix','ambient_frame')]
    need(domain['schema']=='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
         and domain['certificate_verified']is True and domain['original_job']==prefix['original_job']==[24,4]
         and domain['rank']==prefix['rank']==4 and domain['field']==prefix['field']==frame['field']==11
         and prefix['dimension']==frame['dimension']==7,'acquired natural frame and original rank')
    need(domain['convention']==prefix['convention']=='RIGHT_ROW'
         and domain['selected_labels']==prefix['selected_labels']==[1,4,2]
         and prefix['end_order']==[1,4,2,3]
         and domain['external_premises']==prefix['external_premises']
         and domain['external_premises']['original_A_equals_G']is True,'original ordered member interpretation')
    for original,local in [(domain['prefix_export'],m['shared_data']['prefix']),
                           (prefix['matrix_frame_result'],m['shared_data']['ambient_frame'])]:
        need(original['bytes']==local['bytes']and original['sha256']==local['sha256'],'complete original-to-public context join')
    need(len(domain['catalogue'])==domain['catalogue_size']==14763
         and hashlib.sha256(can(domain['catalogue'])).hexdigest()==domain['catalogue_sha256']
         and len(domain['orbits'])==3779
         and hashlib.sha256(can(domain['orbits'])).hexdigest()==m['original_orbit_array_sha256'],'complete original catalogue and orbit array')
    need(frame['full_generator_point_checks']==354312 and frame['six_inverse_checks']==6
         and frame['ordered_generators']==len(frame['source_matrices'])==2,'borrowed exact frame certificate identity')
    R=s.mat(domain['standard_to_actual_row_map'],8);IR=s.mat(domain['actual_to_standard_row_map'],8)
    need(b.multiply(R,IR)==b.multiply(IR,R)==s.identity(8),'fresh inverse row-frame maps')
    a,e,prefix_b=[s.mat(g,7)for g in prefix['matrices']]
    need(len(domain['standard_ordered_prefix_matrices'])==3,'three original prefix matrices')
    for g,standard in zip((a,e,prefix_b),domain['standard_ordered_prefix_matrices']):
        extended=((1,0,0,0,0,0,0,0),)+tuple((0,)+r for r in g)
        need(b.multiply(b.multiply(IR,s.mat(standard,8)),R)==extended,'fresh exact prefix transport')
    return domain,a,prefix_b,e,R,IR


def main():
    global s,READ
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'require-E-B-S/no-O')
    need(len(sys.argv)==4,'manifest manifestSHA fresh-output')
    mp=Path(sys.argv[1]).resolve(strict=True)
    need(0<mp.lstat().st_size<=16384,'manifest extent before whole read');raw=whole(mp)
    need(len(raw)<=16384 and hashlib.sha256(raw).hexdigest()==sys.argv[2],'bounded exact manifest')
    m=decode(raw);need(m['schema']=='F004_FIXED_LINE_ACQUISITION_V1'and m['original_job']==[24,4]and m['position']==59 and m['representative_J_index']==136,'exact original scope')
    shared=(ROOT/m['shared_directory']).resolve(strict=True);raws=[]
    for r in m['sources']:raws.append(whole((ROOT/r['relative']).resolve(strict=True),r))
    need(len(raws)==4 and len(raws[0])+len(raws[1])<=65536,'worker Source cap; both external guard bodies disclosed separately')
    need([r['relative']for r in m['sources']]==['acquire.py','../../matrix_certificates/verify.py','../runtime/supervise_validation.py','../runtime/supervise_transient.py'],'complete actual caller, shared and guard origins')
    need(m['shared_directory']=='../../matrix_certificates'and m['sources'][1]['sha256']=='8d0f424953bc5f8ca29fe29037790f0baba4f029d735dfc6e87e3e84329afd09','unchanged public shared reader')
    need([(len(x),hashlib.sha256(x).hexdigest())for x in raws[2:]]==[(4806,'c3b626b86791ac355c3503a654136f49ad76abbcdfadf0455efb32dd5cca25f4'),(18361,'5c7eed80537835e1a78c8489621d34741eeafc01f47fb394fec519e83f2c9b42')],'exact disclosed guard bodies')
    raw=raws[1];s=types.ModuleType('fixed_line_shared_reader');s.__file__=str(shared/'verify.py')
    exec(compile(raw,s.__file__,'exec'),s.__dict__);s.tick=tick
    need(s.PRODUCTS=={}and s.FIELD==0,'fresh shared counters');s.I7=s.identity(7)
    READ+=sum(len(x)for x in raws)+4806+3*18361;tick()
    domain,a,b,e,R,IR=original_context(Context(),s,m,shared)
    ms=s.check_marks(59,136,domain,a,b,e,R,IR)
    proof=dict(schema='F004_FIXED_LINE_ORIGINAL_REPLAY_V1',position=59,representative_J_index=136,original_job=[24,4],marks=ms,marks_sha256=hashlib.sha256(can(ms)).hexdigest(),status='ORIGINAL_QUARTET_RECONSTRUCTED_ONLY',Root_authority=False)
    for name,pin in list(SEEN.items()):whole(name,pin)
    result=dict(status='ORIGINAL_QUARTET_RECONSTRUCTED_ONLY',matrix_products=s.PRODUCTS,linear_units=s.FIELD,read_bytes=READ+s.READ,paths=len(SEEN),Root_authority=False)
    out=Path(sys.argv[3]).absolute();need(out.parent.resolve(strict=True)==out.parent and not out.exists(),'fresh output')
    bodies=[can(proof)+b'\n',can(result)+b'\n'];need(all(len(x)<=131072 for x in bodies),'two128KiB outputs')
    out.mkdir()
    for name,body in zip(('proof.json','result.json'),bodies):
        with(out/name).open('xb')as f:f.write(body)
    tick();print(can(result).decode())
if __name__=='__main__':main()
