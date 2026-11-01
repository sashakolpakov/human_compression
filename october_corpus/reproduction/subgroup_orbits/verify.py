#!/usr/bin/env python3
"""Verify two original G2(11) end certificates through a shared matrix reader."""
import time
START = time.monotonic()
import argparse,base64,hashlib,itertools,json,math,os,resource,stat,struct,sys,types
from array import array
from pathlib import Path
ROOT = Path(__file__).resolve().parent
MANIFEST = {"file":"manifest.json","bytes":1638,"sha256":"4c680f870d93d2afaa94a66932e7a79ef716af1ead98a6a8d60a0fb761c9c184"}
VECTOR_UNIVERSE=11**7
ROOT_PARENT=65535
ROOT_LABEL=255

def need(value,message):
    if not value:
        raise ValueError(message)

def can(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def decode(raw):
    def unique(items):
        out={}
        for key,value in items:
            need(key not in out,'duplicate JSON key')
            out[key]=value
        return out
    def finite(text):
        value=float(text)
        need(math.isfinite(value),'nonfinite JSON number')
        return value
    return json.loads(raw,object_pairs_hook=unique,parse_float=finite,
                      parse_constant=lambda _:(_ for _ in()).throw(ValueError('nonfinite JSON')))

def signature(s):
    return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

class Budget:
    def __init__(self,bootstrap_bytes=0):
        self.reader=None
        self.read_bytes=bootstrap_bytes
        self.row_images=0
        self.peak=0
        self.refs={}
        self.raw={}
        self.signatures={}
    @property
    def products(self):
        return sum(self.reader.PRODUCTS.values()) if self.reader is not None else 0
    @property
    def linear(self):
        return self.reader.FIELD if self.reader is not None else 0
    def tick(self):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
        self.peak=max(self.peak,rss)
        need(time.monotonic()-START<100 and rss<128*2**20,'100s/128MiB verification limit')
        need(self.products<=400000 and self.row_images<=200000 and self.linear<=200000,'one cumulative arithmetic budget')
        need(self.read_bytes<=8*2**20 and len(self.refs)<=96,'8MiB/96-path verification limit')
    def read(self,path,pin=None,again=False):
        self.tick();path=Path(path)
        need(path.is_absolute()and path.resolve(strict=True)==path,'canonical local input')
        a=path.lstat()
        need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and 0<a.st_size<=2**21,'ordinary bounded input')
        key=str(path)
        if key in self.raw and not again:
            value=self.raw[key]
        else:
            need(self.read_bytes+a.st_size<=8*2**20 and (key in self.refs or len(self.refs)<96),'complete read bank')
            with path.open('rb')as f:
                opened=os.fstat(f.fileno());value=f.read(a.st_size+1);closed=os.fstat(f.fileno())
            need(signature(a)==signature(opened)==signature(closed)==signature(path.lstat())and len(value)==a.st_size,'whole stable input')
            need(key not in self.signatures or self.signatures[key]==signature(a),'input identity unchanged')
            self.signatures[key]=signature(a);self.read_bytes+=len(value)
        digest=hashlib.sha256(value).hexdigest()
        current=dict(bytes=len(value),sha256=digest)
        need(key not in self.refs or self.refs[key]==current,'one input version')
        if pin is not None:
            need(type(pin)is dict and set(pin)=={'file','bytes','sha256'}
                 and type(pin['bytes'])is int and pin['bytes']==len(value)
                 and type(pin['sha256'])is str and pin['sha256']==digest,'exact complete local input pin')
        self.refs[key]=current;self.raw[key]=value;return value
    def document(self,directory,pin):
        need(type(pin)is dict and type(pin.get('file'))is str,'local JSON pin')
        name=pin['file']
        need(name.isascii()and name.endswith('.json')and name.count('.')==1
             and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789_.'for c in name),'plain local JSON filename')
        return decode(self.read(directory/name,pin))
    def multiply(self,a,b):
        self.tick();value=self.reader.mul(a,b);self.tick();return value
    def image(self,v,a):
        self.row_images+=1;self.tick();return self.reader.image(v,a)
    def recheck(self):
        for name in list(self.refs):self.read(Path(name),again=True)
        self.tick()

def cp(b,reserve=0):
    b.tick()
    need(time.monotonic()-START<90 and b.peak<112*2**20 and b.products+reserve<=400000,
         'complete verification stopped at the inherited soft limit')

def arguments():
    p=argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--shared-directory',type=Path)
    p.add_argument('--output',type=Path,required=True)
    return p.parse_args()

def environment(args,controls=False):
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize,'run with -E -B -S, without -O')
    own=Path(__file__).resolve();control=ROOT/'controls.py'
    bootstrap=own.stat().st_size+(2*control.stat().st_size if controls else 0)
    b=Budget(bootstrap);ownraw=b.read(own);controlraw=b.read(control)
    manifest=b.document(ROOT/'data',MANIFEST)
    need(manifest['schema']=='G2_11_SUBGROUP_ORBIT_REPLAY_MANIFEST_V1'
         and manifest['original_job']==[24,4]and manifest['field']==11 and manifest['dimension']==7
         and manifest['positions']==[2570,3017],'two original job24 certificates')
    shared=(args.shared_directory if args.shared_directory is not None else ROOT.parent/'matrix_certificates').resolve(strict=True)
    need(shared.is_dir(),'shared matrix certificate directory')
    sp=manifest['shared_reader'];need(sp['relative']=='../matrix_certificates/verify.py','fixed shared reader relation')
    raw=b.read(shared/'verify.py',dict(file='verify.py',bytes=sp['bytes'],sha256=sp['sha256']))
    need(len(raw)+len(ownraw)+len(controlraw)<=65536,'complete activated project Source union')
    s=types.ModuleType('shared_matrix_certificate_reader');s.__file__=str(shared/'verify.py')
    exec(compile(raw,s.__file__,'exec'),s.__dict__)
    # Every shared arithmetic call uses the caller's single deadline and RSS bank.
    s.tick=b.tick;s.I7=s.identity(7);b.reader=s;b.tick()
    need(s.PRODUCTS=={}and s.FIELD==0,'fresh shared counters before any arithmetic')
    return b,s,manifest,shared

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

def no_left_line(marks,b):
    need(len(marks)>=3,'three LEFT marks')
    ranks=[]
    for signs in itertools.product((1,10),repeat=3):
        cp(b)
        rows=tuple(tuple((g[j][i]-sign*int(i==j))%11 for j in range(7))
                   for g,sign in zip(marks[:3],signs)for i in range(7))
        rank=b.reader.rank_seven(rows)
        need(rank==7,'LEFT has no common rational invariant line')
        ranks.append(dict(signs=list(signs),rank=rank))
    return ranks

def publish(b,path,proof,result):
    path=path.absolute()
    need(path.parent.resolve(strict=True)==path.parent and not os.path.lexists(path),'fresh output directory')
    raws=[can(proof)+b'\n',can(result)+b'\n']
    need(all(len(raw)<=131072 for raw in raws),'two128KiB output bounds')
    path.mkdir(mode=0o700);pins={}
    for name,raw in zip(('proof.json','result.json'),raws):
        target=path/name
        with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
        need(b.read(target)==raw,'whole exact output readback')
        pins[name]=dict(file=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    b.tick()
    out=dict(status=result['status'],outputs=pins,charged_project_read_bytes=b.read_bytes,
             paths=len(b.refs),seconds=time.monotonic()-START,peak_RSS_bytes=b.peak)
    line=can(out)+b'\n';need(len(line)<=131072,'bounded stdout');sys.stdout.buffer.write(line)


def word19(s,b,ms):
 W=s.I7
 for j in(0,1,0,1,2):W=b.multiply(W,ms[j])
 Z=s.I7
 for _ in range(7):Z=b.multiply(Z,W)
 Y=s.I7
 for _ in range(19):Y=b.multiply(Y,Z)
 need(Z!=s.I7 and Y==s.I7,'P036')
 return W,Z

def pid(v):
    need(len(v)==7 and all(type(x)is int and 0<=x<11 for x in v),'P040')
    return sum(x*11**i for i,x in enumerate(v))

def pv(n):
    need(type(n)is int and 0<n<VECTOR_UNIVERSE,'P041')
    v=[]
    for unused in range(7):v.append(n%11);n//=11
    return tuple(v)

def seed_vector(v):
 need(type(v)is list and len(v)==7 and all(type(x)is int and 0<=x<11 for x in v)and any(v),'typed nonzero seed')
 need(next(x for x in v if x)==1,'canonical supplied seed scale')
 return tuple(v)

def seed_fixed(v,Z,b):
 need(b.image(v,Z)==v,'fresh same-order19 fixed seed')

def replay_tree(t,v,ms,b,count):
 need(type(count)is int and 1<count<=9241 and type(t)is dict
  and set(t)=={'kind','count','seed_id','parents_labels_base64','ordered_vector_ids_SHA256'}
  and t['kind']=='REACHABLE_BOUND'and type(t['count'])is int and t['count']==count,'exact finite parent tree')
 seed=pid(v);need(type(t['seed_id'])is int and t['seed_id']==seed and seed>0,'tree root equals actual fixed seed')
 enc=t['parents_labels_base64'];need(type(enc)is str and len(enc)<=36964,'bounded parent encoding')
 packed=base64.b64decode(enc,validate=True)
 need(len(packed)==3*count and base64.b64encode(packed).decode('ascii')==enc,'exact canonical parent encoding')
 ids=array('I',[seed]);seen={seed};need(ids.itemsize==4 and len(ms)==3,'fixed vector encoding')
 for i,(p,k)in enumerate(struct.iter_unpack('<HB',packed)):
  cp(b)
  if i==0:need(p==ROOT_PARENT and k==ROOT_LABEL,'literal parent root');continue
  need(p<i and k<3,'earlier parent and actual LEFT label')
  n=pid(b.image(pv(ids[p]),ms[k]));need(n>0 and n not in seen,'fresh distinct nonzero child')
  seen.add(n);ids.append(n)
 need(len(ids)==len(seen)==count,'all distinct reachable children')
 digest=hashlib.sha256(b''.join(struct.pack('<I',n)for n in ids)).hexdigest()
 need(type(t['ordered_vector_ids_SHA256'])is str and t['ordered_vector_ids_SHA256']==digest,'post-replay ordered ID comparison')
 return dict(count=count,ordered_vector_ids_SHA256=digest,parents_labels_SHA256=hashlib.sha256(packed).hexdigest(),all_parent_images_fresh=True,all_vectors_distinct=True)

def main():
    args=arguments();b,s,m,shared=environment(args)
    domain,a,prefix_b,e,R,IR=original_context(b,s,m,shared)
    packet=b.document(ROOT/'data',m['files']['cases']);adoption=b.document(ROOT/'data',m['files']['adoption'])
    need(packet['schema']=='G2_11_TWO_REACHABLE_LEFT_CERTIFICATES_V1'
         and packet['original_job']==[24,4]and packet['field']==11 and packet['dimension']==7,'literal certificate field and original job')
    need(adoption['schema']=='ROOT_ACCEPTED_Q11_REACHABLE_LEFT_IP_FAILURES_V1'
         and adoption['root']=='/root'and adoption['Root_authority']is True and adoption['adopted']is True
         and adoption['original_job']==[24,4]and adoption['new_IP_failure_positions']==[2570,3017]
         and adoption['new_nongeneration_positions']==[]and adoption['whole_original_credit']==adoption['whole_job_credit']==0,
         'exact accepted two-case attribution; no whole-paper claim')
    need([c['position']for c in packet['cases']]==[2570,3017],'exact two supplied certificates')
    verified=[]
    for case in packet['cases']:
        cp(b);p=case['position'];J=case['representative_J_index']
        marks=s.check_marks(p,J,domain,a,prefix_b,e,R,IR)
        need(hashlib.sha256(can(marks)).hexdigest()==case['marks_sha256'],'fresh original mark comparison')
        # check_marks freshly proves involutions, nonidentity, distinctness and [a,c]=1.
        ranks=no_left_line(marks,b)
        w=case['word19'];need(w['word']==[0,1,0,1,2]and type(w['cofactor'])is int and w['cofactor']==7,'literal LEFT word')
        W,Z=word19(s,b,marks)
        need(hashlib.sha256(can(W)).hexdigest()==w['word_matrix_SHA256']
             and hashlib.sha256(can(Z)).hexdigest()==w['prime_element_SHA256'],'fresh word and exact-order19 comparison')
        v=seed_vector(case['seed']);seed_fixed(v,Z,b)
        replay=replay_tree(case['parent_tree'],v,marks[:3],b,9241)
        verified.append(dict(position=p,representative_J_index=J,marks_sha256=case['marks_sha256'],LEFT_sign_systems=ranks,
            word19=w,seed=list(v),parent_certificate=replay,proper_J1_orbit_bound=9240,
            omitted_mark_nonidentity=True,IP_failure_subsets=[[0,1,2],[3]]))
    b.recheck()
    proof=dict(schema='G2_11_TWO_SUBGROUP_ORBIT_PROOFS_V1',original_job=[24,4],verified=verified,
               borrowed_premises=m['borrowed_premises'],no_search=True,new_case_credit=0)
    result=dict(schema='G2_11_SUBGROUP_ORBIT_REPLAY_RESULT_V1',status='PASS',original_job=[24,4],
                verified_positions=[r['position']for r in verified],verified_cases=len(verified),
                matrix_products=s.PRODUCTS,row_images=b.row_images,linear_field_operations=s.FIELD,
                field_inverses=s.INVERSES,input_read_bytes_after_recheck=b.read_bytes,input_paths=len(b.refs),
                fresh_LEFT_sign_systems=16,no_orbit_search=True,new_whole_original_or_Lean_or_conjecture_or_compression_credit=0)
    publish(b,args.output,proof,result)
if __name__=='__main__':main()
