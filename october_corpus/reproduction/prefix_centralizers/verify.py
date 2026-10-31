#!/usr/bin/env python3
"""One portable prefix recheck; group/model/completeness premises are imported."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import stat
import sys
import time
if sys.flags.optimize:
    raise SystemExit("Run without -O.")
START=time.monotonic()
PRODUCTS={}
INVERSES=0
FIELD=0
ANNIHILATOR=6495720
PRIMES=(2,3,5,7,11,19,37)
BASE=Path(__file__).resolve().parent

def tick():
    if time.monotonic()-START>=100:
        raise RuntimeError("100-second internal cap")
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    if peak>=128*2**20:
        raise RuntimeError("128-MiB internal RSS cap")

def need(ok,why):
 if not ok:raise ValueError(why)

def can(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def decode(raw):
    def unique(items):
        out={}
        for k,v in items:
            need(k not in out,"duplicate JSON key")
            out[k]=v
        return out
    def finite(text):
        v=float(text)
        need(math.isfinite(v),"finite JSON number")
        return v
    return json.loads(raw,object_pairs_hook=unique,parse_float=finite,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))

def signature(s):
    return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

def mat(v,n):
 assert type(v)in(list,tuple)and len(v)==n and all(type(r)in(list,tuple)and len(r)==n and all(type(x)is int and 0<=x<11 for x in r)for r in v)
 return tuple(tuple(r)for r in v)

def identity(n):return tuple(tuple(int(i==j)for j in range(n))for i in range(n))

def mul(a,b):
 n=len(a);assert n==len(b)and all(len(r)==n for r in a+b)
 PRODUCTS[n]=PRODUCTS.get(n,0)+1;assert sum(PRODUCTS.values())<=400000;tick()
 return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(n))%11 for j in range(n))for i in range(n))

def linpow(a,k):
 assert type(k)is int and 0<=k<=37
 x=identity(len(a))
 for _ in range(k):x=mul(x,a)
 return x

def image(v,a):return tuple(sum(v[i]*a[i][j]for i in range(7))%11 for j in range(7))

def inv2(a):
 global INVERSES
 d=(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11;assert d
 x=pow(d,-1,11);INVERSES+=1
 return((a[1][1]*x%11,-a[0][1]*x%11),(-a[1][0]*x%11,a[0][0]*x%11))

def from_pair(row,IR,R):
 assert len(row)==7 and all(type(x)is int and 0<=x<11 for x in row)
 if row[0]==0:P=identity(2);Q=((10,0),(0,10))
 else:
  _,x,y,z,a,b,c=row;P=((x,y),(z,-x%11));Q=((a,b),(c,-a%11))
 det=lambda a:(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11
 assert det(P)==det(Q)!=0
 ip=inv2(P);rows=[]
 for k in range(8):
  E=tuple(tuple(int(2*i+j==k%4)for j in range(2))for i in range(2))
  E=mul(mul(P if k<4 else Q,E),ip);flat=tuple(x for r in E for x in r)
  rows.append(flat+(0,0,0,0)if k<4 else(0,0,0,0)+flat)
 x=mul(mul(IR,tuple(rows)),R)
 assert x[0]==(1,0,0,0,0,0,0,0)and all(x[i][0]==0 for i in range(1,8))
 return tuple(tuple(x[i][j]for j in range(1,8))for i in range(1,8))

def fixed_row(y):
 global FIELD,INVERSES
 a=[[(y[j][i]-int(i==j))%11 for j in range(7)]for i in range(7)];pivots=[];rank=0
 for j in range(7):
  p=next((p for p in range(rank,7)if a[p][j]),None)
  if p is None:continue
  a[rank],a[p]=a[p],a[rank];z=pow(a[rank][j],-1,11);INVERSES+=1
  a[rank]=[z*x%11 for x in a[rank]];FIELD+=7
  for i in range(7):
   if i!=rank and a[i][j]:
    z=a[i][j];a[i]=[(x-z*b)%11 for x,b in zip(a[i],a[rank])];FIELD+=14
  pivots.append(j);rank+=1
 assert FIELD<=200000 and rank==6
 j=next(j for j in range(7)if j not in pivots);v=[0]*7;v[j]=1
 for i,k in enumerate(pivots):v[k]=-a[i][j]%11
 v=tuple(v);assert any(v)and image(v,y)==v
 return v

def bounded_power(a,k):
    need(type(k)is int and 0<=k<=ANNIHILATOR,"bounded nonnegative exact exponent")
    value=identity(len(a));base=a
    while k:
        if k&1:value=mul(value,base)
        k//=2
        if k:base=mul(base,base)
    return value

def exact_order(a):
    # The constant is first TESTED, never assumed to be an annihilator.
    bound=bounded_power(a,ANNIHILATOR)
    need(bound==I7,"actual adjacent product annihilator equation")
    n=ANNIHILATOR;reductions=[]
    for p in PRIMES:
        while n%p==0:
            exponent=n//p;value=bounded_power(a,exponent);annihilates=value==I7
            reductions.append(dict(prime=p,exponent=exponent,is_identity=annihilates))
            if not annihilates:break
            n=exponent
    final=bounded_power(a,n);need(final==I7,"final exact-order identity equation")
    proper=[]
    for p in PRIMES:
        if n%p==0:
            value=bounded_power(a,n//p);need(value!=I7,"every proper prime-divisor equation")
            proper.append(dict(prime=p,exponent=n//p,value=value))
    need(type(n)is int and 1<=n<=ANNIHILATOR and ANNIHILATOR%n==0,
        "complete finite exact-order factorization")
    return n,dict(annihilator=ANNIHILATOR,annihilator_power=bound,
        reduction_tests=reductions,order=n,final_power=final,proper_prime_powers=proper)

def matrix_at(raw,index,count=14763):
    need(type(raw)is bytes and type(count)is int and 1<=count<=14763
        and len(raw)==49*count and type(index)is int and 1<=index<=count,"exact ordered raw matrix locator")
    start=49*(index-1);flat=raw[start:start+49]
    need(len(flat)==49 and all(x<11 for x in flat),"literal GF11 matrix octets")
    return tuple(tuple(flat[7*i+j]for j in range(7))for i in range(7))

def acquire(ctx,bank):
    ab=mul(ctx['a'],ctx['b']);order,certificate=exact_order(ab)
    need(order>2,"actual noncommuting original dihedral prefix")
    involutions=[];e_index=None
    for j in range(1,14764):
        tick();c=matrix_at(bank,j)
        if mul(c,ctx['b'])==mul(ctx['b'],c):involutions.append(j)
        if c==ctx['e']:
            need(e_index is None,"unique original e in the adopted distinct bank");e_index=j
    need(e_index in involutions and 1 not in involutions,
        "original e belongs to U and original a does not commute with b")
    return involutions,e_index,ab,order,certificate

def expect_refusal(fn,label,seen):
    try:fn()
    except (AssertionError,ValueError,TypeError,KeyError):seen.append(label);return
    raise ValueError("accepted malformed control: "+label)

# The following two inherited helpers are used only by generic controls.
def descriptor(r):
    need(type(r)is dict and set(r)=={'path','bytes','sha256'},"complete descriptor")
    need(type(r['path'])is str and Path(r['path']).is_absolute(),"absolute input path")
    need(type(r['bytes'])is int and 0<r['bytes']<=2**21,"bounded input extent")
    need(type(r['sha256'])is str and len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef'),"SHA256")
    return r

def check_review(review,gate,mode,own,pref,rref,pending):
    need(review.get('schema')=='ROOT_REVIEWED_Q11_PREFIX_INVOLUTION_SOURCE_V1'
        and review.get('root')=='/root'and review.get('status')=='SUPPORTED'
        and review.get('program')==own
        and review.get('whole_Source_and_eight_arithmetic_definitions_reviewed')is True
        and review.get('whole_original_context_function_reviewed')is True
        and review.get('adopted_bank_consumer_and_exact_order_reviewed')is True,"Root whole Source and mathematics review")
    need(gate.get('schema')=='ROOT_RELEASED_Q11_PREFIX_INVOLUTION_RUN_V1'
        and gate.get('root')=='/root'and gate.get('authorized')is True
        and gate.get('mode')==mode and gate.get('program')==own
        and gate.get('plan')==pref and gate.get('Root_review')==rref,"fresh exact Root release")
    if mode=='science':
        need(gate.get('generic_controls_actual_accepted')is True
            and review.get('current157_registered_pending')==pending
            and review.get('original_context_associations_reviewed_under_borrowed_premises')is True,
            "actual controls and current original prefix scope")
    else:need(gate.get('no_prefix_or_case_credit')is True,"synthetic controls no prefix authority")

def controls():
    seen=[]
    need(ANNIHILATOR==2**3*3*5*7*11*19*37,"complete tested-bound prime factorization")
    seen.append('annihilator_factorization')
    need(bounded_power(I7,0)==I7 and bounded_power(I7,1)==I7,"zero and one exponents")
    seen.append('zero_one_power')
    for x in [-1,True,ANNIHILATOR+1]:
        expect_refusal(lambda x=x:bounded_power(I7,x),'refused_exponent_'+repr(x),seen)
    one=bytes(x for row in I7 for x in row)
    need(matrix_at(one,1,1)==I7,"complete row-major reconstruction");seen.append('one_row_major_record')
    expect_refusal(lambda:matrix_at(one,0,1),'zero_J_index',seen)
    expect_refusal(lambda:matrix_at(one,2,1),'out_of_range_J_index',seen)
    expect_refusal(lambda:matrix_at(one[:-1],1,1),'short_record',seen)
    expect_refusal(lambda:matrix_at(bytes([11])+one[1:],1,1),'out_of_field_octet',seen)
    order,certificate=exact_order(I7)
    need(order==1 and certificate['proper_prime_powers']==[],"identity exact order")
    seen.append('identity_order1')
    minus=tuple(tuple(-x%11 for x in row)for row in I7)
    need(exact_order(minus)[0]==2,"central scalar involution exact order")
    seen.append('negative_identity_order2')
    for size in (3,4,5,7):
        c=tuple(tuple(int(j==((i+1)%size if i<size else i))for j in range(7))for i in range(7))
        need(exact_order(c)[0]==size,"permutation cycle exact order")
        seen.append('synthetic_cycle_order'+str(size))
    jordan=tuple(tuple((int(i==j)+int(i==0 and j==1))%11 for j in range(7))for i in range(7))
    need(exact_order(jordan)[0]==11,"synthetic unipotent exact order")
    seen.append('synthetic_unipotent_order11')
    six=tuple(tuple(int(j==((i+1)%6 if i<6 else i))for j in range(7))for i in range(7))
    need(exact_order(six)[0]==6,"composite order requires all proper-prime checks")
    seen.append('synthetic_composite_order6')
    # The scalar2 has order10 in GF(11); this is not a G2(11) membership claim.
    scalar=tuple(tuple(2*int(i==j)%11 for j in range(7))for i in range(7))
    need(exact_order(scalar)[0]==10,"synthetic scalar exact order10")
    seen.append('synthetic_scalar_order10')
    weighted=tuple(tuple((2 if i==4 else 1)*int(j==((i+1)%5 if i<5 else i))%11
        for j in range(7))for i in range(7))
    # The monomial five-cycle has fifth power2I on its five-space, hence
    # order50, which does not divide the proposed annihilator.
    expect_refusal(lambda:exact_order(weighted),'refused_nonannihilating_bound',seen)
    expect_refusal(lambda:decode(b'{"x":1,"x":2}'),'duplicate_JSON_keys',seen)
    expect_refusal(lambda:descriptor({'path':'relative','bytes':1,'sha256':'0'*64}),'relative_input',seen)
    expect_refusal(lambda:check_review({}, {}, 'controls',{}, {},{},None),'absent_Root_authority',seen)
    return seen

matrix=mat
I2=identity(2)
I7=identity(7)
I8=identity(8)

def relative_file(name):
    need(type(name)is str and 0<len(name)<=256,"relative filename")
    p=Path(name)
    need(not p.is_absolute()and p.parts and all(x not in('','.','..')for x in p.parts)
        and str(p)==name and len(p.parts)<=4,"local normalized relative path")
    q=BASE/p
    need(q.resolve(strict=True)==q,"no input path aliases")
    return q

class Inputs:
    def __init__(self):
        self.bytes=Path(__file__).stat().st_size
        self.refs={};self.cache={}
    def read(self,r,again=False):
        need(type(r)is dict and set(r)=={'path','bytes','sha256'},"whole relative descriptor")
        need(type(r['bytes'])is int and 0<r['bytes']<=2**20,"one MiB per input file")
        need(type(r['sha256'])is str and len(r['sha256'])==64
            and set(r['sha256'])<=set('0123456789abcdef'),"literal whole SHA256")
        p=relative_file(r['path']);need(self.refs.get(r['path'],r)==r,"one immutable input edition")
        if r['path']in self.cache and not again:return self.cache[r['path']]
        need(self.bytes+r['bytes']+1<=8*2**20 and(len(self.refs)<96 or r['path']in self.refs),"eight MiB and96paths")
        a=p.lstat();need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size==r['bytes'],"ordinary whole input")
        with p.open('rb')as f:
            b=os.fstat(f.fileno());raw=f.read(r['bytes']+1);c=os.fstat(f.fileno())
        need(signature(a)==signature(b)==signature(c)==signature(p.lstat())
            and len(raw)==r['bytes']and hashlib.sha256(raw).hexdigest()==r['sha256'],"whole stable input identity")
        self.bytes+=r['bytes']+1;self.refs[r['path']]=dict(r);self.cache[r['path']]=raw;tick()
        return raw
    def document(self,r):return decode(self.read(r))
    def manifest(self):
        p=relative_file('manifest.json');a=p.lstat()
        need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and 0<a.st_size<=131072,"bounded manifest before IO")
        need(self.bytes+a.st_size+1<=8*2**20,"manifest read budget")
        with p.open('rb')as f:
            b=os.fstat(f.fileno());raw=f.read(a.st_size+1);c=os.fstat(f.fileno())
        need(signature(a)==signature(b)==signature(c)==signature(p.lstat())and len(raw)==a.st_size,"whole stable manifest")
        self.bytes+=a.st_size+1
        r=dict(path='manifest.json',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        self.refs[r['path']]=r;self.cache[r['path']]=raw
        return decode(raw)
    def finish(self):
        for r in list(self.refs.values()):self.read(r,True)

def eligible(n,s,order):
    need(all(type(v)is int and v>0 for v in(n,s,order)),"positive integer lemma data")
    return n<5 and s%5!=0 and order%11!=0

def prefix_matrices(row):
    need(type(row['original_job'])is list and len(row['original_job'])==2
        and type(row['original_job'][0])is int and row['original_job'][1]==4,"original rank4 job")
    need(type(row['matrices'])is list and len(row['matrices'])==3,"three original marks a,e,b")
    a,e,b=[mat(v,7)for v in row['matrices']]
    need(len({a,e,b})==3 and all(g!=I7 and mul(g,g)==I7 for g in(a,e,b)),"distinct original involutions")
    need(mul(a,e)==mul(e,a)and mul(b,e)==mul(e,b)and mul(a,b)!=mul(b,a),"original string prefix equations")
    s=row['S_coordinate_indices']
    need(type(s)is list and s==sorted(set(s))and all(type(x)is int and x>0 for x in s)
        and type(row['S_order'])is int and row['S_order']==len(s)>0,"imported complete S coordinate roster")
    need(row['S_index_space']=='Original endpoint-group coordinate roster; not raw J indices.',"S and raw J use distinct indices")
    return dict(a=a,e=e,b=b)

def verify_prefix(files,manifest,job):
    jobs=manifest['original_jobs']
    need(type(jobs)is list and len(jobs)==157 and jobs==sorted(set(jobs))
        and all(type(x)is int and x>0 for x in jobs)and job in jobs,"one exact original job among157")
    which=manifest['bank_for_job'];need(set(which)==set(map(str,jobs)),"complete finite job lookup")
    name=which[str(job)];need(name in('pair1','pair2'),"one literal bank family")
    data=files.document(manifest['prefix_data'][name]);banks=files.document(manifest['bank_data'])
    table=files.document(manifest['lemma_table'])
    need(data['schema']=='PORTABLE_Q11_157_LITERAL_PREFIX_CERTIFICATES_V1'
        and data['field']==11 and data['dimension']==7,"literal prefix data role")
    rows=data['prefixes'];need(type(rows)is list and len(rows)==(51 if name=='pair1'else 106)
        and len({tuple(r['original_job'])for r in rows})==len(rows),"complete bank-family row table")
    selected=[r for r in rows if r['original_job']==[job,4]];need(len(selected)==1,"unique selected prefix")
    row=selected[0];need(row['bank']==name,"same literal bank family")
    need(all(type(row[k])is int and row[k]>0 for k in
        ('complete_InvU_count','original_e_J_index','ab_order','dihedral_D_order')),"typed original integer facts")
    need(banks['schema']=='PORTABLE_Q11_TWO_ACQUIRED_BANKS_V1'and len(banks['banks'])==2,"two exact bank descriptors")
    entries=[r for r in banks['banks']if r['name']==name];need(len(entries)==1,"unique bank descriptor")
    bank=entries[0]
    need(bank['matrix_count']==14763 and bank['dimension']==7 and bank['field']==11
        and bank['encoding']=='ROW_MAJOR49_GF11_BYTES'
        and bank['literal_tuple_sha256']==row['literal_tuple_sha256'],"exact acquired catalogue/frame/a tuple")
    raw=files.read(bank['raw_bank']);need(len(raw)==723387,"complete ordered bank bytes")
    need(len({raw[i:i+49]for i in range(0,len(raw),49)})==14763,"whole bank distinct byte records")
    ctx=prefix_matrices(row);need(matrix_at(raw,1)==ctx['a'],"first original raw mark is a")
    involutions,e_index,ab,order,certificate=acquire(ctx,raw)
    need(involutions==row['InvU_J_indices']and len(involutions)==row['complete_InvU_count']
        and e_index==row['original_e_J_index']and order==row['ab_order']
        and 2*order==row['dihedral_D_order'],"entire original InvU list and exact adjacent order")
    need(can(certificate)==can(row['exact_ab_order_certificate']),"whole acquired finite order certificate, not a label")
    use=eligible(len(involutions),row['S_order'],order)
    need(type(row['prime5_centralizer_criterion'])is bool and row['prime5_centralizer_criterion']==use,"exact lemma qualification")
    need(table['schema']=='PORTABLE_Q11_81_PRIME_CENTRALIZER_APPLICATIONS_V1'
        and table['ell']==5 and table['p']==11 and len(table['rows'])==81
        and len({tuple(r['original_job'])for r in table['rows']})==81,"finite81application table")
    matches=[r for r in table['rows']if r['original_job']==[job,4]]
    need(bool(matches)==use and len(matches)<=1,"lemma table agrees with freshly rechecked selected prefix")
    if use:
        need(matches[0]=={k:row[k]for k in('original_job','complete_InvU_count','S_order','ab_order','dihedral_D_order')},"literal81table fields")
    return dict(original_job=[job,4],bank=name,scanned_J_count=14763,
        complete_InvU_count=len(involutions),original_e_J_index=e_index,ab_order=order,
        dihedral_D_order=2*order,S_order_imported=row['S_order'],prime5_centralizer_criterion=use,
        both_parabolic_types_excluded_under_explicit_imports=(True if use else None),
        original_group_model_membership_and_bank_completeness_reproved=False,
        full_S_identification_reproved=False,full_original_context_rechecked=False,
        U_equals_S_claimed=False,quartet_generation_or_intersection_claimed=False,
        new_manuscript_conjecture_Lean_or_measurement_credit=0)

def main():
    p=argparse.ArgumentParser(description=__doc__);mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prefix',type=int);mode.add_argument('--controls',action='store_true');args=p.parse_args()
    files=Inputs();m=files.manifest()
    need(m['schema']=='PORTABLE_Q11_PREFIX_RECHECK_MANIFEST_V1'and m['Source']['path']=='verify.py'
        and relative_file(m['Source']['path'])==Path(__file__).resolve(),"fixed public manifest and executing Source role")
    files.read(m['Source'])
    if args.controls:
        checks=controls()
        need(eligible(3,4,6)and eligible(1,2,15)and not eligible(1,2,33)
            and not eligible(3,4,11)and not eligible(11,4,6)
            and not eligible(3,5,6),"prime5/characteristic qualification controls")
        checks.append('prime5_qualification')
        expect_refusal(lambda:eligible(True,4,6),'boolean_lemma_count',checks)
        expect_refusal(lambda:relative_file('../outside'),'outside_relative_path',checks)
        expect_refusal(lambda:relative_file('/absolute'),'absolute_runtime_input',checks)
        result=dict(status='PASS_PORTABLE_PREFIX_GENERIC_CONTROLS',checks=checks,original_prefixes_checked=0)
    else:
        result=verify_prefix(files,m,args.prefix);result['status']='VERIFIED_ONE_PREFIX_WITH_EXPLICIT_GROUP_IMPORTS'
    files.finish();result.update(matrix_products=PRODUCTS,input_charge_bytes=files.bytes,
        seconds=time.monotonic()-START,source_edition=m['Source']['sha256'],counter_resets=0)
    print(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False))

if __name__=='__main__':main()
