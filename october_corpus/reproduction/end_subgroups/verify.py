"""Finite supplied end-subgroup certificates over F11; no search or recognition."""
import argparse,copy,hashlib,json,os,resource,signal,stat,sys,time,types
from pathlib import Path
START=time.monotonic()
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('100 seconds')))
signal.alarm(100)
import runtime as rt
import field,algebra,arithmetic,prime_kernel,line_kernel

SOURCE=('verify.py','runtime.py','field.py','algebra.py','arithmetic.py','prime_kernel.py','line_kernel.py')
POSITIONS=(248,399,490,910,1082,1273,1812,2015,2200,3379,3417)
LINES=(490,3417)
LEFT=(1812,2015)
THEOREM='f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b'
REVIEW='8de6c659c024cd16d90bde4f8a8d548735b201b5a5892c747f63d9a8e08ae053'
IMPORT_KEYS=('named_inner_G2_11','faithful_natural_Cayley_7_module_over_F11',
 'four_marks_are_members_in_that_common_frame','complete_maximal_cover',
 'proper_37_containers_stabilize_a_rational_line','original_row_identification')

def need(ok,why):
    if not ok:raise ValueError(why)

def encoded(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def strict(raw):
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'duplicate JSON key');result[key]=value
        return result
    def bad(_):raise ValueError('integer JSON only')
    return json.loads(raw,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

def extent(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

class Inputs:
    def __init__(self,base,b):
        self.base=base;self.b=b;self.saved={};self.read=131072;self.paths={str(base)}
    def whole(self,name,cap):
        self.b.tick();p=self.base/name
        need(type(name)is str and not Path(name).is_absolute() and '..' not in Path(name).parts,'fixed relative input')
        s=p.lstat();sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        need(p.resolve(strict=True)==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=cap,
             'canonical bounded single-link regular file before read')
        self.paths.add(str(p));need(len(self.paths)<=96 and self.read+s.st_size+1<=8*2**20,'8 MiB/96 path bank')
        with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
            a=os.fstat(f.fileno());raw=f.read(s.st_size+1);z=os.fstat(f.fileno())
        need(sig(s)==sig(a)==sig(z)==sig(p.lstat()) and len(raw)==s.st_size,'whole same-FD input and exact EOF')
        self.read+=len(raw);self.b.tick();return raw
    def load(self,name,cap):
        need(name not in self.saved,'one initial input observation')
        raw=self.whole(name,cap);self.saved[name]=(raw,cap);return raw
    def close(self):
        for name,(raw,cap) in self.saved.items():need(self.whole(name,cap)==raw,'all consumed inputs close whole')

def origin(module,path):
    need(Path(module.__file__).absolute()==path,'literal module origin')
    for value in vars(module).values():
        if isinstance(value,types.FunctionType) and value.__module__==module.__name__:
            need(value.__globals__ is vars(module) and Path(value.__code__.co_filename).absolute()==path,'function origin')
        if isinstance(value,type) and value.__module__==module.__name__:
            for method in vars(value).values():
                if isinstance(method,types.FunctionType):
                    need(method.__globals__ is vars(module) and Path(method.__code__.co_filename).absolute()==path,'method origin')

def both_primes(g,cert,side,b):
    need(type(cert)is dict and set(cert)=={'prime19','prime37'},'two positive facts, no partial/miss inference')
    b.scalar(1024)
    for prime,key in ((19,'prime19'),(37,'prime37')):
        prime_kernel.checked_prime(cert[key],prime,arithmetic.internal(g),side,
            arithmetic.I7,arithmetic,arithmetic.Adapter(b))

def subject(data,expected):
    need(type(data)is dict and set(data)=={'schema','original_job','position','original_row_id','kind','side','marks','certificate'},'whole case schema')
    p=data['position'];need(type(p)is int and p in POSITIONS and data['original_job']==[20,4],'fixed job20 position')
    need(data['schema']=='END_SUBGROUP_CERTIFICATE_V1' and data['original_row_id']==expected['original_row_id'],'recorded original row')
    side=0 if p in LEFT else 1;kind='MOVED37_LINE' if p in LINES else 'TWO_PRIMES'
    need(type(data['side'])is int and data['side']==side and data['kind']==kind,'fixed method and actual end')
    need(hashlib.sha256(encoded(data['marks'])).hexdigest()==expected['marks_sha256'],'exact recorded four-mark tuple')
    return p,side,kind

def case(data,expected,b):
    p,side,kind=subject(data,expected);g=algebra.marking(data['marks'],b)
    if kind=='TWO_PRIMES':both_primes(g,data['certificate'],side,b)
    else:line_kernel.check(g,data['certificate'],b)
    return dict(position=p,original_row_id=data['original_row_id'],method=kind,end_labels=list(arithmetic.ENDS[side]),
        omitted_nonidentity_singleton_label=3 if side==0 else 0,finite_matrix_checks='PASS',
        full_end_and_IP_failure_conditional_on_attributed_imports=True,original_execution_credit=0,new_canonical_credit=0)

def companion(coefficients,b):
    b.scalar(256);degree=len(coefficients)-1
    rows=[[int(i==j)for j in range(7)]for i in range(7)]
    for i in range(degree):
        rows[i]=[0]*7
        if i+1<degree:rows[i][i+1]=1
        else:rows[i][:degree]=[-x%11 for x in coefficients[:-1]]
    return tuple(tuple(row)for row in rows)

def permutation(p):return bytes(int(p[i]==j)for i in range(7)for j in range(7))

def controls(b):
    names=[];b.scalar(20000)
    def yes(name,value):need(value,name);names.append(name)
    def no(name,call,exception=ValueError):
        try:call()
        except exception:names.append(name)
        else:raise ValueError('expected refusal: '+name)
    x=companion([10,2,1,1],b);y=companion([1,1,3,5,3,1,1],b)
    X=bytes(z for row in x for z in row);Y=bytes(z for row in y for z in row)
    right=(field.I,X,Y,field.I);left=(X,Y,field.I,field.I)
    def fact(side,label,rows):return dict(side=side,word=[label],cofactor=1,prime_value=[list(r)for r in rows])
    cert=dict(prime19=fact(1,1,x),prime37=fact(1,2,y))
    both_primes(right,cert,1,b);yes('generic_GL_same_RIGHT_two_primes',True)
    both_primes(left,dict(prime19=fact(0,0,x),prime37=fact(0,1,y)),0,b);yes('generic_GL_same_LEFT_two_primes',True)
    s=permutation([1,0,2,3,4,5,6]);t=permutation([0,2,1,3,4,5,6]);st=b.multiply(s,t)
    yes('noncommutative_product_and_order_three',st!=b.multiply(t,s) and
        arithmetic.power(arithmetic.internal((st,))[0],3,arithmetic.I7,arithmetic.Adapter(b))==arithmetic.I7)
    no('wrong_end_side',lambda:both_primes(right,cert,0,b))
    no('partial_prime_fact_not_full_end',lambda:both_primes(right,dict(prime19=cert['prime19']),1,b))
    def changed(key,value):
        out=copy.deepcopy(cert);out['prime19'][key]=value;return out
    no('identity_prime_matrix',lambda:both_primes(right,changed('word',[3]),1,b))
    no('wrong_actual_word',lambda:both_primes(right,changed('word',[2]),1,b))
    no('wrong_prime_cofactor',lambda:both_primes(right,changed('cofactor',3),1,b))
    no('boolean_side',lambda:both_primes(right,changed('side',True),1,b))
    bad=algebra.rows(X);bad[0][0]=True
    no('boolean_field_entry',lambda:arithmetic.field_matrix(bad))
    no('outside_end_word',lambda:both_primes(right,changed('word',[0]),1,b))
    no('overlong_word',lambda:both_primes(right,changed('word',[1]*33),1,b))
    no('generic_GL_fixture_not_Original_involutions',lambda:algebra.marking([algebra.rows(z)for z in (X,Y,s,t)],b))
    no('identity_original_marks',lambda:algebra.marking([algebra.rows(field.I)]*4,b))
    no('duplicate_JSON',lambda:strict(b'{"x":1,"x":2}'))
    no('floating_JSON',lambda:strict(b'{"x":1e999}'))
    limited=rt.Budget();limited.products=400000
    no('hard_matrix_product_refusal',lambda:limited.multiply(field.I,field.I),rt.Limit)
    mover=permutation([6,1,2,3,4,5,0]);negative=bytes(10 if i==j==6 else int(i==j)for i in range(7)for j in range(7))
    g=(field.I,Y,mover,negative);line=dict(prime37=fact(1,1,y),vector=[0]*6+[1],moving_label=2)
    yes('generic37_fixed_vector_and_moved_line',line_kernel.check(g,line,b)['moved_line_minor_verified'])
    yes('nonzero_vector_scaling',line_kernel.check(g,dict(line,vector=[0]*6+[2]),b)['moved_line_minor_verified'])
    no('negative_vector_is_same_line',lambda:line_kernel.check(g,dict(line,moving_label=3),b))
    no('zero_fixed_vector',lambda:line_kernel.check(g,dict(line,vector=[0]*7),b))
    no('wrong_fixed_vector',lambda:line_kernel.check(g,dict(line,vector=[1]+[0]*6),b))
    no('boolean_moving_label',lambda:line_kernel.check(g,dict(line,moving_label=True),b))
    no('omitted_mark_not_RIGHT_mover',lambda:line_kernel.check(g,dict(line,moving_label=0),b))
    no('extra_line_certificate_field',lambda:line_kernel.check(g,dict(line,extra=0),b))
    no('malformed_case_schema',lambda:subject({},{}))
    need(len(names)==len(set(names))==26,'all26 original-free controls');return names

def main():
    need(sys.platform in ('darwin','linux') and sys.dont_write_bytecode and not sys.flags.optimize,'POSIX Darwin/Linux, -B, no -O')
    parser=argparse.ArgumentParser(allow_abbrev=False);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--controls',action='store_true');mode.add_argument('--all',action='store_true');mode.add_argument('--case',type=int,choices=POSITIONS)
    args=parser.parse_args();b=rt.Budget();b.started=START
    given=Path(os.path.abspath(__file__));need(given.resolve(strict=True)==given,'canonical entry Source')
    base=given.parent;inputs=Inputs(base,b);sources={}
    for name in SOURCE:sources[name]=extent(inputs.load(name,32768))
    need(sum(r['bytes']for r in sources.values())+23167<=65536,'complete seven-module plus unchanged guards Source bank')
    for module in (sys.modules[__name__],rt,field,algebra,arithmetic,prime_kernel,line_kernel):origin(module,base/(module.__name__+'.py' if module is not sys.modules[__name__] else 'verify.py'))
    if args.controls:
        result=dict(status='PASS',controls=controls(b),generic_GL_fixtures_only=True,Original_cases=0)
    else:
        manifest=strict(inputs.load('manifest.json',65536));imports=strict(inputs.load('IMPORTS.json',65536))
        need(type(manifest)is dict and set(manifest)=={'schema','sources','cases','validation_record','validation_not_consumed'} and
             manifest['schema']=='END_SUBGROUP_PUBLIC_MANIFEST_V1' and manifest['sources']==sources and
             manifest['validation_record']=='VALIDATION.json' and manifest['validation_not_consumed'] is True,'whole public Source manifest')
        need(type(imports)is dict and set(imports)=={'schema','theorem_sha256','independent_review_sha256','assumptions','provenance'} and
             imports['schema']=='END_SUBGROUP_ATTRIBUTED_IMPORTS_V1' and imports['theorem_sha256']==THEOREM and
             imports['independent_review_sha256']==REVIEW and type(imports['assumptions'])is dict and
             set(imports['assumptions'])==set(IMPORT_KEYS) and all(imports['assumptions'][k]is True for k in IMPORT_KEYS),
             'attributed classification/frame/membership/row imports, not fresh recognition')
        roster=manifest['cases'];need(type(roster)is list and len(roster)==11 and
            [r['position']for r in roster]==list(POSITIONS),'exact ordered eleven-case roster')
        checked=[]
        for expected in roster:
            need(type(expected)is dict and set(expected)=={'position','original_row_id','marks_sha256','file','extent'},'case manifest entry')
            p=expected['position'];name='data/case_%04d.json'%p;need(expected['file']==name,'fixed relative certificate name')
            if args.case is not None and p!=args.case:continue
            raw=inputs.load(name,16384);need(extent(raw)==expected['extent'],'whole exact certificate extent')
            checked.append(case(strict(raw),expected,b))
        result=dict(status='PASS',cases=checked,conditional_IP_exclusions=len(checked),
            attributed_group_and_maximal_cover_imports=True,Original_execution_credit=0,new_canonical_credit=0)
    inputs.close();b.tick();result.update(matrix_products=b.products,row_images=b.rows,linear_units=b.linear,
        charged_read_bytes=inputs.read,distinct_paths=len(inputs.paths),all_consumed_files_closed=True)
    raw=encoded(result);need(len(raw)<=131072,'bounded terminal JSON');sys.stdout.buffer.write(raw)

if __name__=='__main__':main()
