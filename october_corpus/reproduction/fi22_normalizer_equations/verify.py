#!/usr/bin/env python3
"""Verify finite supplied normalizer equations from local portable data."""
from pathlib import Path
from array import array
import argparse,hashlib,json,os,resource,stat,struct,sys,time,types
START=time.monotonic();BASE=Path(__file__).resolve().parent
READ_CAP=8388608;PATH_CAP=32;SOURCE_CAP=50000;GUARD_SOURCE_BYTES=23167
DEGREE=3510;MAGIC=b'L026NMS1';BINARY_BYTES=12+39*2*DEGREE

def need(ok,why):
    if not ok:raise ValueError(why)

def tick():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    need(sys.platform in('darwin','linux')and rss<=134217728 and time.monotonic()-START<140,'128MiB140s process bound')

def parse(raw,work=None):
    if work is not None:work.charge(6*len(raw),'whole_finite_JSON_scan_reserve')
    def pairs(rows):
        out={}
        for k,v in rows:need(k not in out,'duplicate JSON key');out[k]=v
        return out
    def bad(_):raise ValueError('integer-only finite JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

class Inputs:
    def __init__(self):self.bytes=Path(__file__).stat().st_size;self.refs={};self.work=None
    def read(self,name,expected=None,cap=2097152):
        need(type(name)is str and name in {'verify.py','operations.py','equations.py','manifest.json','maps.bin','words.json'},'flat declared local input')
        p=BASE/name;s=p.lstat();sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        need(p.resolve(strict=True)==p and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and 0<s.st_size<=cap,'whole regular canonical input')
        need(self.bytes+s.st_size<=READ_CAP and len(set(self.refs)|{name})+1<=PATH_CAP,'8MiB32path bank')
        with p.open('rb')as f:a=os.fstat(f.fileno());raw=f.read(s.st_size+1);z=os.fstat(f.fileno())
        need(sig(s)==sig(a)==sig(z)==sig(p.lstat())and len(raw)==s.st_size,'stable whole input and EOF')
        r=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        need(expected is None or r==expected,'exact whole input size/SHA');need(self.refs.get(name,r)==r,'one input edition')
        self.bytes+=len(raw);self.refs[name]=r
        if self.work is not None:self.work.charge(4*len(raw),'whole_input_read_hash_buffer_reserve')
        tick();return raw
    def close(self):
        for name,r in list(self.refs.items()):self.read(name,r)

def load(raw,name):
    m=types.ModuleType(name);m.__file__=str(BASE/(name+'.py'));exec(compile(raw,m.__file__,'exec',dont_inherit=True),vars(m))
    for v in vars(m).values():
        if type(v).__name__=='function'and v.__module__==name:need(v.__globals__ is vars(m)and v.__code__.co_filename==m.__file__,'literal loaded function origin')
        if isinstance(v,type)and v.__module__==name:
            for f in v.__dict__.values():
                if type(f).__name__=='function':need(f.__globals__ is vars(m)and f.__code__.co_filename==m.__file__,'literal loaded method origin')
    return vars(m)

def vector(raw,at,n,w):
    w.charge(2*n,'explicit_little_endian_u16_decode');v=array('H',struct.unpack_from('<'+'H'*n,raw,at));seen=bytearray(n);w.charge(n,'bijection_seen_initialization')
    for x in v:w.charge(3,'bijection_field_range_unique');need(x<n and not seen[x],'entire bijection');seen[x]=1
    return v

def endpoint(K,V,a,c,n,w):
    I=K['identity'](n,w)
    need(not V['equal'](a,I,w)and not V['equal'](c,I,w)and not V['equal'](a,c,w),'distinct nonidentity endpoints')
    need(V['equal'](K['compose'](a,a,w),I,w)and V['equal'](K['compose'](c,c,w),I,w),'both complete involution equations')
    need(V['equal'](K['compose'](a,c,w),K['compose'](c,a,w),w),'actual commuting endpoints; genuine Klein four')

def check(K,V,raw,cert,w,n=DEGREE,count=36):
    need(type(raw)is bytes and len(raw)==12+(count+3)*2*n and raw[:8]==MAGIC,'exact full binary frame')
    need(struct.unpack_from('<HH',raw,8)==(n,count),'explicit degree/mapcount')
    maps=[vector(raw,12+2*n*i,n,w)for i in range(count+3)];a,c,g=maps[:3];cp={i+1:x for i,x in enumerate(maps[3:])}
    endpoint(K,V,a,c,n,w)
    for h in cp.values():need(V['equal'](K['compose'](a,h,w),K['compose'](h,a,w),w),'every CP map freshly centralizes a')
    gi=K['inverse'](g,w);need(V['equal'](K['compose'](K['compose'](gi,a,w),g,w),c,w),'whole a^g=c')
    need(type(cert)is dict and type(cert.get('r_word'))is list and type(cert.get('q_word'))is list,'two supplied words')
    w.charge(6*(len(cert['r_word'])+len(cert['q_word']))+64,'complete word-shape reserve')
    facts=V['verify'](K,dict(n=n,a=a,c=c),cp,g,cert,w)
    return dict(status='PASS',degree=n,CP_maps=count,equations=['a^g=c','a^r=a','c^r=ac','a^t=c','c^t=a'],
        all_maps_whole_bijections=True,all_CP_maps_centralize_a=True,t_expression='CP36(q_word) * g',
        r_letters=len(cert['r_word']),q_letters=len(cert['q_word']),
        normalizer_action_quotient='S3_CONDITIONAL_ON_IMPORTED_A_MEMBERSHIPS',
        normalizer_order_IF_imported_C_A_K_equals_H_of_order1024=6144,
        centralizer_or_normalizer_order_freshly_counted=False,original_group_frame_or_memberships_recognized=False,
        new_bank_rows_or_class_or_Lean_credit=0)

def controls(K,V,w):
    names=[]
    def yes(n,x):need(x,n);names.append(n)
    def no(n,f):
        try:f()
        except(ValueError,TypeError):names.append(n)
        else:raise ValueError('expected refusal:'+n)
    a=array('H',[1,0,3,2]);c=array('H',[2,3,0,1]);g=array('H',[0,2,1,3]);r=array('H',[0,1,3,2]);n=4
    cp=[r,c];cert=dict(schema='L026_TWO_NORMALIZER_WORD_CANDIDATE_V1',r_word=[2,1,2],q_word=[2,2],prefix_acceptance=dict(bytes=1,sha256='0'*64))
    def pack(maps):return MAGIC+struct.pack('<HH',4,2)+b''.join(struct.pack('<4H',*m)for m in maps)
    raw=pack([a,c,g]+cp);f=check(K,V,raw,cert,w,4,2)
    yes('S4_V4_all_five_equations',f['status']=='PASS')
    yes('actual_noncommuting_CP_maps',K['compose'](r,c,w)!=K['compose'](c,r,w))
    ri=K['inverse'](K['compose'](r,c,w),w);yes('whole_signed_inverse_orientation',list(ri)==list(K['compose'](c,r,w)))
    x=dict(cert,r_word=[-2,-1,-2]);yes('negative_CP_word',check(K,V,raw,x,w,4,2)['status']=='PASS')
    no('wrong_r_word',lambda:check(K,V,raw,dict(cert,r_word=[]),w,4,2))
    no('wrong_q_word',lambda:check(K,V,raw,dict(cert,q_word=[1]),w,4,2))
    no('wrong_g_map',lambda:check(K,V,pack([a,c,a]+cp),cert,w,4,2))
    no('noncentralizing_CP_map',lambda:check(K,V,pack([a,c,g]+[g,c]),cert,w,4,2))
    no('nonbijection',lambda:check(K,V,pack([a,c,g]+[[0,0,2,3],c]),cert,w,4,2))
    no('out_of_range_image',lambda:check(K,V,pack([a,c,g]+[[0,1,2,4],c]),cert,w,4,2))
    no('identity_endpoint',lambda:check(K,V,pack([range(4),c,g]+cp),cert,w,4,2))
    no('equal_endpoints',lambda:check(K,V,pack([a,a,g]+cp),cert,w,4,2))
    no('Boolean_word_label',lambda:check(K,V,raw,dict(cert,r_word=[True]),w,4,2))
    no('zero_word_label',lambda:check(K,V,raw,dict(cert,r_word=[0]),w,4,2))
    no('missing_CP_word_map',lambda:check(K,V,raw,dict(cert,r_word=[3]),w,4,2))
    no('word_over128',lambda:check(K,V,raw,dict(cert,r_word=[1]*129),w,4,2))
    no('truncated_binary',lambda:check(K,V,raw[:-1],cert,w,4,2))
    no('wrong_degree_header',lambda:check(K,V,raw[:8]+struct.pack('<HH',5,2)+raw[12:],cert,w,4,2))
    no('extra_certificate_field',lambda:check(K,V,raw,dict(cert,extra=0),w,4,2))
    no('wrong_certificate_schema',lambda:check(K,V,raw,dict(cert,schema='wrong'),w,4,2))
    no('duplicate_JSON',lambda:parse(b'{"x":1,"x":2}',w))
    no('noninteger_JSON',lambda:parse(b'{"x":1.5}',w))
    need(len(names)==22,'all22 original-free controls')
    return dict(status='PASS',mode='controls',controls=len(names),names=names,new_bank_rows_or_class_or_Lean_credit=0)

def main():
    need(not sys.flags.optimize,'run without-O');need(Path(__file__).name=='verify.py','selected entry')
    ap=argparse.ArgumentParser(allow_abbrev=False);g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--controls',action='store_true');g.add_argument('--check',action='store_true');args=ap.parse_args()
    inputs=Inputs();manifest_raw=inputs.read('manifest.json',cap=16384);manifest=parse(manifest_raw)
    need(manifest['schema']=='L026_PORTABLE_NORMALIZER_EQUATIONS_MANIFEST_V1'and manifest['degree']==3510 and manifest['CP_maps']==36,'fixed original finite subject')
    need(set(manifest['Source'])=={'verify.py','operations.py','equations.py'},'entire3body Source')
    bodies={n:inputs.read(n,r,cap=65536)for n,r in manifest['Source'].items()};size=sum(len(x)for x in bodies.values());need(size+GUARD_SOURCE_BYTES<=SOURCE_CAP,'whole Source plus original guards50000')
    K=load(bodies['operations.py'],'operations');V=load(bodies['equations.py'],'equations');w=K['Meter'](tick);w.start=START;inputs.work=w;w.charge(4*inputs.bytes+6*len(manifest_raw)+4*size,'initial_full_reads_JSON_and_Source_compilation_reserve')
    if args.controls:result=controls(K,V,w)
    else:
        raw=inputs.read('maps.bin',manifest['maps']);cert=parse(inputs.read('words.json',manifest['words'],cap=16384),w)
        need(cert['prefix_acceptance']==manifest['imported_prefix_acceptance'],'same imported accepted g expression')
        result=check(K,V,raw,cert,w)
    w.charge(262144,'full16KiB_stdout_serialization_reserve');inputs.close();w.charge(0,'final_work_guard')
    result.update(Source_bytes=size,Source_with_original_guards_bytes=size+GUARD_SOURCE_BYTES,physical_read_bytes=inputs.bytes,input_paths=len(inputs.refs)+1,shared_work_units=w.units,shared_work_cap=w.cap)
    output=(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();need(len(output)<=16384,'bounded16KiB stdout');sys.stdout.buffer.write(output)

if __name__=='__main__':main()
