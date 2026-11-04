"""Indexed prospective q11 Cayley frame and centralizer-domain certificate.

All arithmetic is behind main(). Source preparation must not import or call it.
Original prefix/export/model/A and permutation joins remain Root premises.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

HERE=Path(__file__).absolute().parent
D4=HERE.parent
THEORY=D4.parent/'theory'
P=11
I2=(1,0,0,1)
ZERO4=(0,0,0,0)
UNIT=(1,0,0,0,0,0,0,0)
STD_UNIT=(1,0,0,1,0,0,0,0)
INPUT_CAP=65536
DOC_CAP=2**21
OUTPUT_CAP=2**20
NORMALIZATION=dict(path=str(D4/'cayley_normalization_acquisition/root_acceptance.json'),bytes=112192,
    sha256='208431dc9dd0ec31b7688719e12def55682dd35a085f088ba2cd32d34fdde940')
NORMAL_RESULT=dict(path=str(D4/'cayley_normalization_acquisition/result.json'),bytes=10559,
    sha256='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1')
FORMS=dict(path=str(D4/'invariant_forms_acquisition/root_acceptance.json'),bytes=78082,
    sha256='0ab1b853480874ef685a807d5c72d5f98fba22894e7b5727e7cb6815d0cc1d36')
FRAME=dict(path=str(D4/'matrix_frame_root_acceptance.json'),bytes=3394,
    sha256='a8746058d9d1482ac9ed92157f31b765c0998d195efc312d734a8533ddc86498')
FRAME_RESULT=dict(path=str(D4/'matrix_frame_acquisition_result/result.json'),bytes=9384,
    sha256='b6259de58ace64a7bccf97db50e81e4686c5f6f501c3263c86186fadb09e8391')
CANDIDATES=dict(path=str(D4/'invariant_tensor_candidates/result.json'),bytes=7610,
    sha256='4d6f3c194b9208d5960443e7363207ec0d595a9e185528c5943269f285596fd7')
MODEL_PROOF=dict(path=str(THEORY/'acquired_cayley_full_group_bridge.rst'),bytes=9716,
    sha256='a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801')
CATALOGUE_PROOF=dict(path=str(THEORY/'cayley_centralizer_inventory_reduction.rst'),bytes=25604,
    sha256='665de95492ec34b949252c4c5955eba3c997b806f87363a4bc4262031a64a816')
CATALOGUE_PEER=dict(path=str(THEORY/'cayley_centralizer_inventory_distinct_review.rst'),bytes=9975,
    sha256='8c0a283f9da68061ed0465c5d7b2a8430ebb724859d6a750802b564d1a3b1784')


def need(value,message):
    if not value:raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def shape(q):
    need(type(q)is dict and set(q)=={'path','bytes','sha256'}and type(q['path'])is str
         and Path(q['path']).is_absolute()and type(q['bytes'])is int and q['bytes']>=0
         and type(q['sha256'])is str and len(q['sha256'])==64
         and all(c in'0123456789abcdef'for c in q['sha256']),'exact ordinary reference')
    return q


def exact(q,tick,cap=DOC_CAP,decode=False):
    shape(q);p=Path(q['path']);a=p.lstat()
    need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size==q['bytes']<=cap,'bounded ordinary whole input')
    with p.open('rb')as f:
        if sys.platform=='darwin':fcntl.fcntl(f.fileno(),48,1)
        b=os.fstat(f.fileno());raw=f.read(cap+1);z=os.fstat(f.fileno())
    sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(sig(a)==sig(b)==sig(z)==sig(p.lstat())and len(raw)==a.st_size
         and hashlib.sha256(raw).hexdigest()==q['sha256'],'whole stable exact input')
    tick()
    if not decode:return raw
    def pairs(values):
        d={}
        for k,v in values:need(k not in d,'unique JSON key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda s:(_ for _ in()).throw(ValueError('nonfinite '+s)))


def vec(v,n):
    need(type(v)is list and len(v)==n and all(type(x)is int and 0<=x<P for x in v),'canonical field vector')
    return tuple(v)


def mat(value,n):
    need(type(value)is list and len(value)==n,'canonical square matrix')
    return tuple(vec(row,n)for row in value)


def ident(n):return tuple(tuple(int(i==j)for j in range(n))for i in range(n))


def scale(c,x):return tuple(c*a%P for a in x)


def add(x,y):return tuple((a+b)%P for a,b in zip(x,y))


def row(x,m):
    out=[0]*len(m)
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(m[i]):out[j]=(out[j]+a*b)%P
    return tuple(out)


def mm(a,b):return tuple(row(x,b)for x in a)


def inverse(m):
    n=len(m);work=[list(x)+list(ident(n)[i])for i,x in enumerate(m)]
    for j in range(n):
        pivot=next((i for i in range(j,n)if work[i][j]),None);need(pivot is not None,'nonsingular matrix')
        work[j],work[pivot]=work[pivot],work[j];work[j]=[x*pow(work[j][j],-1,P)%P for x in work[j]]
        for i in range(n):
            if i!=j:
                c=work[i][j];work[i]=[(x-c*y)%P for x,y in zip(work[i],work[j])]
    return tuple(tuple(x[n:])for x in work)


def nullspace(equations,n):
    work=[list(x)for x in equations];pivots=[];r=0
    for j in range(n):
        k=next((k for k in range(r,len(work))if work[k][j]),None)
        if k is None:continue
        work[r],work[k]=work[k],work[r];c=pow(work[r][j],-1,P);work[r]=[c*x%P for x in work[r]]
        for k in range(len(work)):
            if k!=r:
                c=work[k][j];work[k]=[(x-c*y)%P for x,y in zip(work[k],work[r])]
        pivots.append(j);r+=1
    basis=[]
    for j in range(n):
        if j not in pivots:
            v=[0]*n;v[j]=1
            for k,p in enumerate(pivots):v[p]=-work[k][j]%P
            basis.append(tuple(v))
    return basis


def bilinear(x,q,y):return sum(a*b for a,b in zip(row(x,q),y))%P


def product(t,x,y):
    out=[0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:
                    for k,c in enumerate(t[i][j]):out[k]=(out[k]+a*b*c)%P
    return tuple(out)


def mul2(a,b):
    return((a[0]*b[0]+a[1]*b[2])%P,(a[0]*b[1]+a[1]*b[3])%P,
           (a[2]*b[0]+a[3]*b[2])%P,(a[2]*b[1]+a[3]*b[3])%P)


def bar2(a):return(a[3],-a[1]%P,-a[2]%P,a[0])


def det2(a):return(a[0]*a[3]-a[1]*a[2])%P


def inv2(a):return scale(pow(det2(a),-1,P),bar2(a))


def standard(x,y):
    a,b=x[:4],x[4:];c,d=y[:4],y[4:]
    return add(mul2(a,c),scale(-1,mul2(bar2(d),b)))+add(mul2(d,a),mul2(b,bar2(c)))


def norm0(x):return(det2(x[:4])+det2(x[4:]))%P


def frame(i,u,v,multiply,unit):
    iu=multiply(i,u)
    return(unit,i,u,iu,v,multiply(i,v),multiply(u,v),multiply(iu,v))


def operator(p,q):
    ip=inv2(p);out=[]
    for j in range(8):
        e=tuple(int(k==j%4)for k in range(4))
        out.append(mul2(mul2(p,e),ip)+ZERO4 if j<4 else ZERO4+mul2(mul2(q,e),ip))
    return tuple(out)


def normalize_pair(p,q):
    c=next(x for x in p if x);v=scale(pow(c,-1,P),p+q)
    return v[:4],v[4:]


def jpair(value):
    if value[0]==0:return I2,scale(-1,I2)
    _,x,y,z,a,b,c=value
    return(x,y,z,-x%P),(a,b,c,-a%P)


def jkey(delta,p,q):
    a=(delta,p[0],p[1],p[2],q[0],q[1],q[2])
    b=(delta,-p[0]%P,-p[1]%P,-p[2]%P,-q[0]%P,-q[1]%P,-q[2]%P)
    return min(a,b)


def catalogue(tick):
    values=[(0,0,0,0,0,0,0)];sizes=[]
    need(pow(2,(P-1)//2,P)==P-1,'fixed nonsquare2')
    for delta in(1,2):
        triples=[(x,y,z)for x in range(P)for y in range(P)for z in range(P)if(-x*x-y*z)%P==delta]
        epsilon=1 if pow(-delta%P,(P-1)//2,P)==1 else -1
        need(len(triples)==P*(P+epsilon),'all tracezero matrices at exact determinant')
        for p in triples:
            for q in triples:
                v=(delta,)+p+q
                if v==jkey(delta,(p[0],p[1],p[2],-p[0]%P),(q[0],q[1],q[2],-q[0]%P)):
                    values.append(v)
            tick()
        sizes.append(dict(delta=delta,epsilon=epsilon,tracezero_matrices=len(triples),class_size=len(triples)**2//2,
            class_centralizer_order=2*(P-epsilon)**2))
    need(len(values)==len(set(values))==14763,'complete duplicate-free equal-det quotient catalogue')
    return values,sizes


def common_group(delta,u,tick):
    i=(0,-delta%P,1,0)
    d=[add(scale(s,I2),scale(t,i))for s in range(P)for t in range(P)]
    units=sorted(x for x in d if det2(x)==1);h=len(units)
    need(h in(10,12),'complete quadratic norm-one group')
    lifts={}
    for alpha in units:
        lifts[alpha]=next((x for x in d if det2(x)and mul2(x,inv2(bar2(x)))==alpha),None)
        need(lifts[alpha]is not None,'full rational lift, no missing nonsquare class')
    by={}
    for alpha in units:
        p=lifts[alpha]
        for beta in units:
            q=mul2(beta,p)
            for bit in(0,1):
                pair=normalize_pair(mul2(p,u),mul2(q,u))if bit else normalize_pair(p,q)
                need(pair not in by,'distinct full endpoint-centralizer pair');by[pair]=True
        tick()
    pairs=sorted(by);need(len(pairs)==2*h*h,'complete endpoint centralizer')
    one=normalize_pair(I2,I2)
    involutions=[j+1 for j,(p,q)in enumerate(pairs)if(p,q)!=one
                 and normalize_pair(mul2(p,p),mul2(q,q))==one]
    need(len(involutions)==h*h+3,'entire common final involution domain')
    return pairs,involutions,h


def orbit_cover(values,domain,pairs,stabilizer,tick):
    index={v:j+1 for j,v in enumerate(values)};left=set(domain);orbits=[]
    while left:
        rep=min(left);p,q=jpair(values[rep-1]);transports={};fixed=[]
        for k in stabilizer:
            r,s=pairs[k-1]
            # For RIGHT_ROW matrices M(r,s), right conjugation M^-1 X M
            # represents functional rho(r,s) X rho(r,s)^-1, hence r p r^-1.
            image=1 if rep==1 else index[jkey(values[rep-1][0],mul2(mul2(r,p),inv2(r)),mul2(mul2(s,q),inv2(s)))]
            need(image in domain,'full stabilizer preserves selected domain')
            transports.setdefault(image,k)
            if image==rep:fixed.append(k)
        members=sorted(transports)
        need(fixed and len(members)*len(fixed)==len(stabilizer)and set(members)<=left,'complete disjoint full-stabilizer orbit')
        left.difference_update(members)
        # Compact complete orbit certificate. Exact S_rep is recoverable from
        # the retained whole S and pair operators; its order is checked here.
        orbits.append([rep,members,[transports[j]for j in members],len(fixed)])
        tick()
    need(sum(len(x[1])for x in orbits)==len(domain),'full literal orbit index cover')
    return orbits


def certify(data,normal,tick):
    need(type(data)is dict and data.get('schema')=='F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1'
         and data.get('field')==11 and data.get('dimension')==7 and data.get('convention')=='RIGHT_ROW'
         and data.get('matrix_frame_result')==FRAME_RESULT,'genuine exported prefix schema and paid coordinate frame')
    rank=data.get('rank');need(type(rank)is int and rank in(4,5),'one rank4 final or rank5 fourth prefix')
    need(data.get('selected_labels')==[1,rank,2]
         and data.get('end_order')==([1,4,2,3]if rank==4 else[1,5,2,4,3]),'complete original fixed label order')
    need(type(data.get('original_job'))is list and len(data['original_job'])==2
         and all(type(x)is int and x>0 for x in data['original_job'])and data['original_job'][1]==rank,'explicit original job identity')
    prefix_index=data.get('original_prefix_index')
    need(type(prefix_index)is int and prefix_index>0,'positive original source prefix index, never a new catalogue index')
    origin=data.get('origin');need(type(origin)is dict and set(origin)==
        {'literal_prefix','native_source','root_terminal','root_clearance','binding_source','prelift_map','root_source_authentication','original_prefix_index_proof'},'all original export/provenance roles and exact indexed native proof')
    for q in origin.values():shape(q)  # Root authenticates these complete origins externally; no payload replay.
    claims=data.get('external_premises');need(type(claims)is dict and set(claims)==
        {'root','model_bridge_source','model_source_join','original_A_equals_G'}and claims['root']=='/root'
        and claims['model_bridge_source']==MODEL_PROOF and type(claims['original_A_equals_G'])is bool,'explicit imported model/A premises')
    shape(claims['model_source_join'])
    need(normal['schema']=='F004_GF11_CAYLEY_NORMALIZATION_CERTIFICATE_V1'
         and normal['status']=='CERTIFIED_GF11_SPLIT_CAYLEY_COMPOSITION'and normal['certificate_verified']is True
         and normal['field']==11 and normal['kappa']==7 and normal['input']==CANDIDATES
         and normal['vector_identities_checked']==196 and normal['scalar_identities_checked']==1372,
         'same paid complete196 normalization, no new forms/model inference')
    q=mat(normal['quadratic_form_matrix'],8);inverse(q)
    need(type(normal['multiplication_tensor'])is list and len(normal['multiplication_tensor'])==8,'whole512 multiplication coefficients')
    t=tuple(mat(layer,8)for layer in normal['multiplication_tensor']);units=ident(8)
    need(all(q[i][j]==q[j][i]for i in range(8)for j in range(8))and q[0][0]==1,'canonical symmetric norm')
    marks=data.get('matrices');need(type(marks)is list and len(marks)==3,'three complete ordered prefix matrices')
    marks=[mat(x,7)for x in marks]
    extended=[((1,0,0,0,0,0,0,0),)+tuple((0,)+r for r in m)for m in marks]
    for m in extended:
        need(mm(m,m)==ident(8)and m!=ident(8),'nonidentity marked involutions')
        for i in range(8):
            for j in range(8):
                need(row(t[i][j],m)==product(t,m[i],m[j]),'all64 basis products on actual mark')
                need(bilinear(m[i],q,m[j])==q[i][j],'full norm coefficient preservation')
        tick()
    a,e,b=extended
    need(len(set(extended))==3 and mm(a,e)==mm(e,a)and mm(e,b)==mm(b,e)
         and mm(a,b)!=mm(b,a),'original distant/adjacent selected-prefix relations')
    def eigenspace(sa,se):
        equations=[]
        for m,sign in((marks[0],sa),(marks[1],se)):
            equations.extend(tuple((m[i][j]-sign*int(i==j))%P for i in range(7))for j in range(7))
        return[(0,)+x for x in nullspace(equations,7)]
    spaces={(sa,se):eigenspace(sa,se)for sa,se in((1,1),(1,-1),(-1,1),(-1,-1))}
    need([len(spaces[k])for k in((1,1),(1,-1),(-1,1),(-1,-1))]==[1,2,2,2],'complete pure common eigenspace dimensions')
    i0=spaces[1,1][0]
    choices=[(c,scale(c,i0))for c in range(1,P)if bilinear(scale(c,i0),q,scale(c,i0))in(1,2)]
    need(choices,'nondegenerate common fixed line');i=choices[0][1];delta=bilinear(i,q,i)
    def norm_one(key):
        x,y=spaces[key]
        for c in range(P):
            for d in range(P):
                z=add(scale(c,x),scale(d,y))
                if bilinear(z,q,z)==1:return z
        raise ValueError('complete121 coefficient search has no norm-one vector')
    u=norm_one((1,-1));v=norm_one((-1,1));multiply=lambda x,y:product(t,x,y)
    actual=frame(i,u,v,multiply,UNIT);inverse(actual)
    need(all(bilinear(actual[i],q,actual[j])==0 for i in range(8)for j in range(8)if i!=j),'whole Cayley-frame orthogonality')
    xy=next(((x,y)for x in range(P)for y in range(P)if(x*x+delta*y*y+1)%P==0),None)
    need(xy is not None,'complete standard binary norm equation');x,y=xy
    si=(0,-delta%P,1,0)+ZERO4;su=(x,delta*y%P,y,-x%P)+ZERO4;sv=ZERO4+I2
    standard_frame=frame(si,su,sv,standard,STD_UNIT)
    r=mm(inverse(standard_frame),actual);ir=inverse(r)
    need(row(STD_UNIT,r)==UNIT,'exact unital standard-to-actual row map')
    for x in units:
        for y in units:
            need(row(standard(x,y),r)==multiply(row(x,r),row(y,r)),'all64 multiplication basis joins')
            polar=(norm0(add(x,y))-norm0(x)-norm0(y))%P
            need(2*bilinear(row(x,r),q,row(y,r))%P==polar,'full canonical norm scale joins')
    standard_marks=[mm(mm(r,m),ir)for m in extended]
    a0=tuple(scale(1 if j<4 else -1,x)for j,x in enumerate(units))
    need(standard_marks[0]==a0 and standard_marks[1]==operator(si[:4],si[:4]),'whole ordered endpoint normalization')
    values,class_info=catalogue(tick);pairs,final_raw,h=common_group(delta,su[:4],tick)
    stabilizer=[j+1 for j,(p,q0)in enumerate(pairs)if mm(operator(p,q0),standard_marks[2])==mm(standard_marks[2],operator(p,q0))]
    need(stabilizer,'complete pointwise prefix stabilizer contains identity')
    domain=[]
    for j,value in enumerate(values,1):
        if rank==4:domain.append(j)
        else:
            p,q0=jpair(value);m=operator(p,q0)
            if mm(m,standard_marks[2])==mm(standard_marks[2],m):domain.append(j)
        if j%64==0:tick()
    orbits=orbit_cover(values,set(domain),pairs,stabilizer,tick)
    return dict(status='VERIFIED_CAYLEY_FRAME_AND_AUTOMORPHISM_DOMAIN',certificate_verified=True,
        rank=rank,original_job=data['original_job'],original_prefix_index=prefix_index,
        original_prefix_index_proof=origin['original_prefix_index_proof'],
        selected_labels=data['selected_labels'],origin=origin,external_premises=claims,
        common_eigenspace_dimensions=[1,2,2,2],frame=list(actual),frame_norms=[bilinear(z,q,z)for z in actual],
        delta=delta,standard_binary_solution=xy,standard_frame=list(standard_frame),standard_to_actual_row_map=r,
        actual_to_standard_row_map=ir,standard_ordered_prefix_matrices=standard_marks,
        algebra_basis_products_checked=64,canonical_polar_coefficients_checked=64,
        catalogue_schema='INDEX1_IS_A0_OTHER_ROWS_ARE_DELTA_PX_PY_PZ_QX_QY_QZ_SIMULTANEOUS_SIGN_QUOTIENT',
        catalogue=values,catalogue_sha256=hashlib.sha256(canonical(values)).hexdigest(),catalogue_size=len(values),class_info=class_info,
        endpoint_group_pair_coordinates=pairs,endpoint_group_order=len(pairs),quadratic_norm_one_order=h,
        prefix_stabilizer_indices=stabilizer,prefix_stabilizer_order=len(stabilizer),
        selected_raw_domain_indices=domain,selected_raw_domain_size=len(domain),orbits=orbits,
        orbit_schema='[representative_J_index,all_member_J_indices,matching_transporter_Q_indices,full_stabilizer_order]',
        common_final_raw_involution_indices=final_raw if rank==5 else None,
        common_final_raw_involution_size=len(final_raw)if rank==5 else None,
        orbit_action='RIGHT_ROW M_g^-1 M_x M_g; coefficient pairs r p r^-1 and s q s^-1',
        old_indices_reinterpreted=False,original_double_coset_weights_certified=False,
        terminal_predicates_executed=False,rank5_final_orbits_executed=False,original_prefix_origin_reproved=False,
        full_named_model_identity_reproved=False,original_A_equals_G_reproved=False,permutation_lifts_generated=False,
        scope='Complete explicit domain/orbits in Aut(C) for the supplied algebra-automorphism prefix. Saved-group/A/original-prefix/lifts/old-index/terminal jobs require separate Root joins.')


def main():
    started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--prefix-export',type=Path,required=True);ap.add_argument('--prefix-export-sha256',required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary -E -B invocation')
    def peak():
        n=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return n if sys.platform=='darwin'else n*1024
    def tick():need(time.monotonic()-started<100 and peak()<=128*2**20,'observed100s/128MiB; outer Root guard still required')
    need(args.prefix_export.is_absolute()and args.output.is_absolute()and not os.path.lexists(args.output)
         and args.output.parent.resolve(strict=True)==args.output.parent,'absolute input/fresh ordinary output parent')
    prefix_ref=dict(path=str(args.prefix_export),bytes=args.prefix_export.lstat().st_size,sha256=args.prefix_export_sha256)
    reads=[NORMALIZATION,NORMAL_RESULT,FORMS,FRAME,MODEL_PROOF,CATALOGUE_PROOF,CATALOGUE_PEER,prefix_ref]
    try:
        prefix=exact(prefix_ref,tick,INPUT_CAP,True)
        ng=exact(NORMALIZATION,tick,decode=True);normal=exact(NORMAL_RESULT,tick,decode=True)
        forms=exact(FORMS,tick,decode=True);fg=exact(FRAME,tick,decode=True)
        need(ng['root']=='/root'and ng['status']=='ROOT_ACCEPTED_F004_ACTUAL_SPLIT_CAYLEY_NORMALIZATION'
             and ng['actual_normalization_certified']is True and ng['input']==CANDIDATES and ng['result']==NORMAL_RESULT
             and ng['kappa']==7 and ng['invariant_forms_acceptance']==FORMS and ng['faithful_frame_acceptance']==FRAME,
             'exact acquired composition/forms/frame authority joins')
        need(forms['status']=='ROOT_ACCEPTED_F004_Q11_DIRECT_INVARIANT_FORMS'and forms['forms_verified']is True
             and forms['beta_equations_checked']==98 and forms['tau_equations_checked']==70
             and fg['status']=='ROOT_ACCEPTED_Q11_FAITHFUL_MATRIX_FRAME'and fg['result']==FRAME_RESULT
             and fg['inputs_unchanged']is True,'same independently acquired invariance/faithful frame')
        for q in(MODEL_PROOF,CATALOGUE_PROOF,CATALOGUE_PEER):exact(q,tick)
        result=certify(prefix,normal,tick)
        for q in reads:exact(q,tick,INPUT_CAP if q==prefix_ref else DOC_CAP)
        tick()
    except (ValueError,RuntimeError,OSError,KeyError,TypeError,StopIteration)as exc:
        result=dict(status='REFUSED_CAYLEY_FRAME_OR_DOMAIN',certificate_verified=False,error=type(exc).__name__+': '+str(exc)[:2048])
    result.update(schema='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1',field=11,convention='RIGHT_ROW',
        prefix_export=prefix_ref,normalization=NORMALIZATION,normalization_result=NORMAL_RESULT,forms_acceptance=FORMS,
        faithful_frame_acceptance=FRAME,model_bridge_source=MODEL_PROOF,catalogue_proof=CATALOGUE_PROOF,catalogue_peer=CATALOGUE_PEER,
        seconds=time.monotonic()-started,peak_self_bytes=peak(),census_credit=0,candidate_credit=0,whole_original_credit=0,
        qualification='Algebra/frame/domain certificate only. Exact saved model/full-group/A/original prefix/export/phi/mu/lift and old-index/weight joins, original guards/terminal generation/IP, native/strict/independent actual review and Root adoption remain external duties. Refusal or interruption is unpaid.')
    raw=canonical(result)+b'\n';need(len(raw)<=OUTPUT_CAP,'complete1MiB output, never truncate')
    with args.output.open('xb')as f:need(f.write(raw)==len(raw),'whole fresh certificate');f.flush();os.fsync(f.fileno())
    print(canonical(dict(status=result['status'],certificate_verified=result['certificate_verified'],
        output=dict(path=str(args.output),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),census_credit=0)).decode())
    if not result['certificate_verified']:raise SystemExit(2)


if __name__=='__main__':main()
