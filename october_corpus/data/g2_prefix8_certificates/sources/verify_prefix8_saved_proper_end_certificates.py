"""Independent Saved verification of the actual230 proper-end witnesses.

New plain F11 arithmetic and word decoding; no ancestor function is loaded.
Only current split/split and split/unitary certificates are accepted.
No search, FULL/order4 inference, weights, original lift or automatic adoption.
Source only until independent review, focused guards and Root admission.
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
THEORY=HERE.parent.parent/'theory'
SEARCH=dict(path=str(HERE/'search_prefix8_end_rejections.py'),bytes=18889,sha256='e63ef0bce9015003047b427ac87782e932bb83728293e29147b49c0191919233')
HELPERS=dict(path=str(HERE/'verify_indexed_frame_catalogue.py'),bytes=22496,sha256='1cebbda5fcda823b43713f03dd17893480c34d040f27501a0651ab69d8f496d3')
DOMAIN=dict(path=str(HERE/'cases/original_prefix8/output/result.json'),bytes=513255,sha256='e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8')
EXPORT=dict(path=str(HERE.parent/'original_prefix8_matrix_export/indexed_prefix8_coordinates.json'),bytes=4345,sha256='6494e0d434e5b62a68d6966227e361bd3118c8afe936bc9900bd776924c2b8d6')
NORMAL=dict(path=str(HERE.parent/'cayley_normalization_acquisition/result.json'),bytes=10559,sha256='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1')
OLD_RESULT=dict(path=str(HERE/'cases/prefix8_end_rejections/output/result.json'),bytes=4886,sha256='d9d5dc7171a3659d278b4df05e63686125242ba2da17f98d84a3b5dad518d713')
OLD_JOURNAL=dict(path=str(HERE/'cases/prefix8_end_rejections/output/witnesses.jsonl'),bytes=191639,sha256='58a0c96fdbaec4fd3f0827f88b31ea5a985fd381c9ee5290b9c2918177cfedf8')
PARTIAL=dict(path=str(HERE/'cases/prefix8_end_rejections/root_partial_rejection_acceptance.json'),bytes=9314,sha256='bb7fab3d15834fac1ab12e8c41a966a48e16e5f1f6d24283315e4ab6d4479440')
GENERATION_ATTACHMENT=dict(path=str(HERE/'cases/prefix8_end_rejections/root_generation_source_attachment.json'),bytes=8398,sha256='3eb33961c12933b016e950b16c58175032b0f4b2c4e2b9bc3813de160a44bbf1')
PROOF=dict(path=str(THEORY/'double_unitary_end_intersection_obstruction.rst'),bytes=14424,sha256='d7e540f9ad61fbacf1f18ca1a184a0638581e6693a972a7705febd44e21c7126')
PROOF_REVIEW=dict(path=str(THEORY/'double_unitary_end_intersection_independent_review.rst'),bytes=4341,sha256='591ca8e3a02c9213789f926c8a4fd1f67b5672c0fdeb12f4e33a10f4009047f7')
GENERATION=dict(path=str(THEORY/'g2_11_generation_by_prime_witnesses.tex'),bytes=26437,sha256='f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b')
MODEL=dict(path=str(THEORY/'acquired_cayley_full_group_bridge.rst'),bytes=9716,sha256='a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801')
SCHEDULE_SOURCE=dict(path=str(HERE.parent/'matrix_end_certificate.g'),bytes=3831,sha256='d07cdbcaf1c25826e8917770adedec9b2ef4b159e13fe29c27181c88e17f137a')
PRIOR_PROGRAM=dict(path=str(HERE/'verify_prefix8_double_proper_ends.py'),bytes=18457,sha256='2481375f2203fda2920289ce9b15c02c2a3f081bd58ea625da267b4607d2f0d7')
PRIOR_GATE=dict(path=str(HERE/'cases/prefix8_double_proper_ends/root_double_proper_acceptance.json'),bytes=10008,sha256='cc7bedda717a6bb757185fdf22f73c4efaa0871e540e21f5ba890ef253ae9b94')
PRIOR_RESULT=dict(path=str(HERE/'cases/prefix8_double_proper_ends/output/result.json'),bytes=9816,sha256='ec933e426cffddaca7d44b4cc76dee7f3ed3426334f18ce2e6bb39d1f68c1a20')
PRIOR_JOURNAL=dict(path=str(HERE/'cases/prefix8_double_proper_ends/output/witnesses.jsonl'),bytes=25935,sha256='7222493162a76defebcfafd0cdd82c377155153d86a501d5e747f57291864320')
PRIOR_AUTHORITY=dict(path=str(HERE/'cases/prefix8_double_proper_ends/root_adoption_source_authentication.json'),bytes=717911,sha256='80706683a676867f7ea8be15de26c4241978171e8b1d6cc8a36ff74f6869512f')
SPLIT_PROOF=dict(path=str(THEORY/'split_and_unitary_end_intersection_obstruction.rst'),bytes=14302,sha256='c8d38efd6049367e7caad1e07f5fe93275108b6e2ef112e9d436dc578177a9db')
SPLIT_ROOT_REVIEW=dict(path=str(THEORY/'split_and_unitary_end_intersection_root_review.rst'),bytes=3432,sha256='0cfae243663fc710b5581ece4ab02366c831a067fa6121dbf8ca95523c85b113')
SPLIT_UNIT_REVIEW=dict(path=str(THEORY/'split_and_unitary_end_intersection_independent_review.rst'),bytes=6801,sha256='9feeff10defddf990b76114f90e78e4191f55d3ee9c34851ca6f86fdb8a85ce6')
NORMALIZER_SOURCE=dict(path=str(HERE.parent/'verify_cayley_normalization.py'),bytes=10508,sha256='ad8030d47175e58bd22fee6030f7b12a804076b42deaa707774c3eabd2957a67')
PRIOR_PROPER19_PROGRAM={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/search_prefix8_proper19_ends.py', 'bytes': 27417, 'sha256': 'ceac7edc8184584a76d11ef5901673c812567d95b2d61ec5483a391a780b8496'}
MOVED19_ORDER4_THEORY={'path': '/Users/sasha/medusa/research/leemans/computation/f004/theory/g2_11_generation_moved19_order4.rst', 'bytes': 11978, 'sha256': '1d82837bf00b85ed580d87fb59afb8e072c23da572676ff90d3c0fd74cc98f7f'}
MOVED19_ORDER4_REVIEW={'path': '/Users/sasha/medusa/research/leemans/computation/f004/theory/g2_11_generation_moved19_order4_root_review.rst', 'bytes': 3691, 'sha256': '45096e2926da7dacea8e31648c15bf87ffbd53b1524f97a903af047a33f578f3'}
SAVED_WORKER={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/search_prefix8_moved19_order4_ends.py', 'bytes': 33413, 'sha256': 'bf862fa619bc7f9dbde21b7024cbc7b958cad308381c4fe109f0ddae87e91392'}
SAVED_RESULT={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/output/result.json', 'bytes': 13561, 'sha256': '6c7862cb99a7cc3f7a48a3a3bc88c1b163ecb15df91755fb329a8c0a6906b14b'}
SAVED_JOURNAL={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/output/witnesses.jsonl', 'bytes': 235625, 'sha256': 'fdd9a6d5a8a0dcdd9930e120647070e62915e36b192375cad8ee1d6045b37e15'}
SAVED_TERMINAL={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/root_terminal.json', 'bytes': 2400, 'sha256': '962447988a7b3e9fd88b53b3b90d3d173b74183813ce34c49c106996f8d69217'}
SAVED_CLEARANCE={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/root_handle_clearance.json', 'bytes': 1033, 'sha256': '4de30fc655d9f48127bd101312c3b3baca77283ae3a8c0eec8f0b84b53116e26'}
SAVED_RELEASE={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/root_release.json', 'bytes': 4817, 'sha256': '617049dbe51ebe9a2a02fddef17a8ac1649f18f98f23129f5650ac784ad07c71'}
SAVED_WORKFLOW={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/cases/prefix8_moved19_order4_ends/root_workflow_execution.json', 'bytes': 15312, 'sha256': '764d3fddf89b7f7f4d4c3537b3aa0ca40e0d51508a74718305330ad2733fded6'}
MODEL_JOIN={'bytes': 8118, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/native_admission/root_model_source_join.json', 'sha256': '38d27708ce1b4be9d10fe24ffae68705d1a63d8f9796c2fd4b7d3fd366b8f6b3'}
FRAME_GATE={'bytes': 3394, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/matrix_frame_root_acceptance.json', 'sha256': 'a8746058d9d1482ac9ed92157f31b765c0998d195efc312d734a8533ddc86498'}
FORMS_GATE={'bytes': 78082, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/invariant_forms_acquisition/root_acceptance.json', 'sha256': '0ab1b853480874ef685a807d5c72d5f98fba22894e7b5727e7cb6815d0cc1d36'}
NORMAL_GATE={'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_normalization_acquisition/root_acceptance.json', 'bytes': 112192, 'sha256': '208431dc9dd0ec31b7688719e12def55682dd35a085f088ba2cd32d34fdde940'}
CATALOGUE_PROOF={'bytes': 25604, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/theory/cayley_centralizer_inventory_reduction.rst', 'sha256': '665de95492ec34b949252c4c5955eba3c997b806f87363a4bc4262031a64a816'}
CATALOGUE_PEER={'bytes': 9975, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/theory/cayley_centralizer_inventory_distinct_review.rst', 'sha256': '8c0a283f9da68061ed0465c5d7b2a8430ebb724859d6a750802b564d1a3b1784'}
ORIGIN_INPUTS=[{'bytes': 1855, 'path': '/Users/sasha/medusa/research/leemans/reboot_20261013/F004_recovery_work/batch_branches_v1.g', 'sha256': '8c47be758f55d1f4e398ac329f1cdbc58dd8f494bd6adec2c27c7300f2e8f6b7'}, {'bytes': 3314, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/original_prefix_binding.json', 'sha256': '2197b2a814fa0f26d830d3654aa390010e9420c4fa8b7bb5dbc7f1148f0deaf7'}, {'bytes': 3696, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/export_prefix8_matrices.g', 'sha256': '041cb3b596433636b9c29cd003b2cf93837d57022dd17eaa2a29b45f70514fa5'}, {'bytes': 3172, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/original_prefix_index_proof.rst', 'sha256': 'cc3bbc5859a6a73a650cf66563f054d629930f11a32993560edd4199eb5d2c84'}, {'bytes': 2737, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/frame_inverse.g', 'sha256': '16f56367e4546c68cf7db726d7646e7a7e1d8e660ee4841c9401ab52655c27d9'}, {'bytes': 1462, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/native_admission/root_handle_clearance.json', 'sha256': 'ac5ba4e289e7948afd21de6114b6b391b54be9bd28b010b779625b4feae90498'}, {'bytes': 680571, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/native_admission/root_retained_export_validation.json', 'sha256': '2737245dec4958fcc1c763c0eca6eeeb26022cabec43006ce2ead9f2188658a6'}, {'bytes': 3308, 'path': '/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/native_admission/root_terminal.json', 'sha256': '9beaf18448faa6cb25d0b8a5adcfee3230de03edb92d72c229facbf3a0c497a8'}]
ANCESTOR_INPUTS=[SEARCH,HELPERS,DOMAIN,EXPORT,NORMAL,OLD_RESULT,OLD_JOURNAL,PARTIAL,GENERATION_ATTACHMENT,PROOF,PROOF_REVIEW,GENERATION,MODEL,SCHEDULE_SOURCE,PRIOR_PROGRAM,PRIOR_GATE,PRIOR_RESULT,PRIOR_JOURNAL,PRIOR_AUTHORITY,SPLIT_PROOF,SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW,NORMALIZER_SOURCE,PRIOR_PROPER19_PROGRAM,MOVED19_ORDER4_THEORY,MOVED19_ORDER4_REVIEW]
INPUTS=ANCESTOR_INPUTS+[SAVED_WORKER,SAVED_RESULT,SAVED_JOURNAL,SAVED_TERMINAL,SAVED_CLEARANCE,SAVED_RELEASE,SAVED_WORKFLOW,MODEL_JOIN,FRAME_GATE,FORMS_GATE,NORMAL_GATE,CATALOGUE_PROOF,CATALOGUE_PEER]+ORIGIN_INPUTS

TOTAL_SECONDS,WORK_SECONDS,RSS_CAP=100,90,128*2**20
DOCUMENT_CAP,UNIQUE_INPUT_CAP,INPUT_COUNT_CAP=2**21,8*2**20,96
OUTPUT_CAP,RECORD_CAP=256*2**10,16384


def need(condition,message):
    if not condition:raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def decode(raw):
    def unique(pairs):
        out={}
        for key,value in pairs:
            need(key not in out,'duplicate JSON key');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=unique,
        parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite JSON '+x)))


def peak_bytes():
    value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform=='darwin'else value*1024


class Budget:
    def __init__(self):self.start=time.monotonic()
    def check(self,work=True):
        need(time.monotonic()-self.start<(WORK_SECONDS if work else TOTAL_SECONDS)
            and peak_bytes()<RSS_CAP,'shared90s work/100s total/128MiB observed self RSS')


def refcheck(ref):
    need(type(ref)is dict and set(ref)=={'path','bytes','sha256'}
        and type(ref['path'])is str and Path(ref['path']).is_absolute()
        and str(Path(ref['path']))==ref['path'] and '..'not in Path(ref['path']).parts
        and type(ref['bytes'])is int and 0<=ref['bytes']<=DOCUMENT_CAP
        and type(ref['sha256'])is str and len(ref['sha256'])==64
        and all(x in'0123456789abcdef'for x in ref['sha256']),'exact bounded whole-file pin')
    return ref


def current_inputs():
    by_path={}
    for ref in INPUTS:
        refcheck(ref);p=ref['path']
        need(p not in by_path or by_path[p]==ref,'no conflicting direct Source/data role')
        by_path[p]=ref
    rows=[by_path[p]for p in sorted(by_path)]
    need(len(rows)<=INPUT_COUNT_CAP and sum(q['bytes']for q in rows)<=UNIQUE_INPUT_CAP,
        'at most96 unique direct documents/8MiB, no historical expansion')
    return rows


def read_exact(ref,budget,work=True):
    refcheck(ref);budget.check(work);p=Path(ref['path']);a=p.lstat()
    need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size==ref['bytes']
        and p.resolve(strict=True)==p,'ordinary exact pinned document and parents')
    signature=lambda q:(q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
    with p.open('rb')as f:
        if sys.platform=='darwin':fcntl.fcntl(f.fileno(),48,1)
        b=os.fstat(f.fileno());raw=f.read(ref['bytes']+1);z=os.fstat(f.fileno())
    need(signature(a)==signature(b)==signature(z)==signature(p.lstat())and len(raw)==a.st_size
        and hashlib.sha256(raw).hexdigest()==ref['sha256'],'stable complete exact document bytes')
    budget.check(work);return raw


def file_pin(path,raw):
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def framed(raw,count):
    lines=raw.splitlines(keepends=True)
    need(len(lines)==count and all(x.endswith(b'\n')and len(x)<=RECORD_CAP for x in lines),
        'whole expected LF records, no partial/overlong tail')
    values=[decode(x)for x in lines]
    need(all(canonical(v)+b'\n'==line for v,line in zip(values,lines)),'canonical entire LF journal')
    return values


def vector(value,n):
    need(type(value)is list and len(value)==n
        and all(type(x)is int and 0<=x<11 for x in value),'canonical full F11 vector')
    return tuple(value)


def matrix(value,n):
    need(type(value)is list and len(value)==n,'full square F11 matrix')
    return tuple(vector(v,n)for v in value)


def unit(n):
    return tuple(tuple(1 if i==j else 0 for j in range(n))for i in range(n))


def product(a,b,budget):
    budget.check();n=len(a)
    need(n==len(b)and all(len(x)==n for x in a+b),'internal square product dimensions')
    out=tuple(tuple(sum(a[i][k]*b[k][j]for k in range(n))%11
        for j in range(n))for i in range(n))
    budget.check();return out


def right_row(v,a):
    return tuple(sum(v[i]*a[i][j]for i in range(len(v)))%11 for j in range(len(v)))


def power(a,exponent,budget):
    need(type(exponent)is int and exponent>=0,'nonnegative exact word power')
    answer=unit(len(a))
    for bit in bin(exponent)[2:]:
        answer=product(answer,answer,budget)
        if bit=='1':answer=product(answer,a,budget)
    return answer


def rank(a,budget):
    work=[list(v)for v in a];pivots=0
    for col in range(len(work[0])):
        budget.check();chosen=next((i for i in range(pivots,len(work))if work[i][col]),None)
        if chosen is None:continue
        work[pivots],work[chosen]=work[chosen],work[pivots]
        inverse=pow(work[pivots][col],9,11)
        work[pivots]=[(x*inverse)%11 for x in work[pivots]]
        for i in range(pivots+1,len(work)):
            factor=work[i][col]
            work[i]=[(x-factor*y)%11 for x,y in zip(work[i],work[pivots])]
        pivots+=1
        if pivots==len(work):break
    return pivots


def catalogue_operator(entry,index,budget):
    value=vector(entry,7)
    if index==1:
        need(value==(0,)*7,'literal first catalogue A0 identity')
        p=unit(2);q=tuple(tuple(-x%11 for x in row)for row in p)
    else:
        delta,x,y,z,a,b,c=value
        need(delta in(1,2),'acquired trace-zero pair class')
        p=((x,y),(z,-x%11));q=((a,b),(c,-a%11))
        need((p[0][0]*p[1][1]-p[0][1]*p[1][0])%11==delta
            and(q[0][0]*q[1][1]-q[0][1]*q[1][0])%11==delta,'exact paired determinants')
    determinant=(p[0][0]*p[1][1]-p[0][1]*p[1][0])%11
    need(determinant!=0,'invertible paired coordinate')
    inv=pow(determinant,9,11)
    ip=((p[1][1]*inv%11,-p[0][1]*inv%11),(-p[1][0]*inv%11,p[0][0]*inv%11))
    need(product(p,ip,budget)==product(ip,p,budget)==unit(2),'explicit2x2 inverse')
    rows=[]
    for j in range(8):
        basis=tuple(tuple(int(2*i+k==j%4)for k in range(2))for i in range(2))
        block=product(product(p if j<4 else q,basis,budget),ip,budget)
        flat=tuple(x for row in block for x in row)
        rows.append(flat+(0,)*4 if j<4 else(0,)*4+flat)
    return tuple(rows)


def pure_actual(standard,r,ir,q,budget):
    actual=product(product(ir,standard,budget),r,budget)
    need(actual[0]==(1,0,0,0,0,0,0,0)and all(actual[i][0]==0 for i in range(1,8)),
        'scalar-fixed exact actual pure7 block')
    transpose=tuple(tuple(actual[j][i]for j in range(8))for i in range(8))
    need(product(product(actual,q,budget),transpose,budget)==q,'same canonical full8 norm isometry')
    return tuple(tuple(row[1:])for row in actual[1:])


def actual_marks(prefix,c,budget):
    a,e,b=prefix;identity=unit(7)
    need(all(h!=identity and product(h,h,budget)==identity for h in(a,b,c,e))
        and a!=c and b!=e,'all four actual nonidentity involutions/distinct commuting end pairs')
    need(all(product(x,y,budget)==product(y,x,budget)for x,y in((a,c),(a,e),(b,e))),
        'all three required actual distant commutations')
    return(a,b,c),(b,c,e)


def word_value(end,text,budget):
    need(type(text)is str and 1<=len(text)<=160 and all(x in'1234'for x in text),
        'complete bounded right-row end word')
    h1,h2,h3=end
    letters=(product(h1,h2,budget),product(h2,h1,budget),product(h2,h3,budget),product(h3,h2,budget))
    answer=unit(7)
    for x in text:answer=product(answer,letters[int(x)-1],budget)
    return answer


def verify_side(end,saved,old_fact,words,q,budget):
    need(type(saved)is dict and saved.get('kind')in('PROPER19','PROPER37'),
        'only a recorded positive proper-line certificate, no moved/FULL/miss inference')
    number=saved['checkpoint'];text=saved['word'];kind=saved['kind']
    need(type(number)is int and 1<=number<=40 and text==words[number-1],'whole acquired checkpoint word')
    prime,exponent=(19,7)if kind=='PROPER19'else(37,3)
    need(type(saved['prime'])is int and saved['prime']==prime and type(saved['power'])is int
        and saved['power']==exponent,'literal prime and word exponent')
    fact=saved['fact']
    need(type(fact)is list and len(fact)==(3 if prime==19 else 1),'entire proper witness structure')
    v=vector(fact[0],7)
    need(any(v)and next(x for x in v if x)==1,'nonzero normalized actual pure fixed-line witness')
    if prime==19:need(old_fact is None,'new19 on an old side without a proper37 witness')
    else:
        need(type(old_fact)is list and len(old_fact)==3 and old_fact[0]==number
            and old_fact[1]=='PROPER'and old_fact[2]==list(v),'exact previously recorded37 side, freshly re-evaluated')
    y=power(word_value(end,text,budget),exponent,budget)
    need(y!=unit(7)and power(y,prime,budget)==unit(7),'independent exact prime-order end word')
    difference=tuple(tuple((y[i][j]-int(i==j))%11 for j in range(7))for i in range(7))
    need(rank(difference,budget)==6 and right_row(v,y)==v,'rank-six and the actual unique pure fixed line')
    for h in end:
        image=right_row(v,h)
        need(all((v[i]*image[j]-v[j]*image[i])%11==0 for i in range(7)for j in range(i+1,7)),
            'each actual end generator preserves the whole line, sign allowed')
    v8=(0,*v);norm=sum(x*y for x,y in zip(right_row(v8,q),v8))%11
    need(norm!=0,'nonisotropic canonical kappa7 line norm')
    roots=[x for x in range(1,11)if x*x%11==(-norm)%11]
    if prime==19:
        need(type(fact[1])is int and fact[1]==norm and type(fact[2])is int
            and fact[2]in roots,'split line from exact N(v8)=v8 Q v8^T and explicit sqrt(-norm)')
    else:need(roots==[],'nonsplit unitary line in the same canonical norm')
    return dict(kind=kind,checkpoint=number,word=text,prime=prime,power=exponent,
        actual_fixed_line=list(v),canonical_norm=norm,line_type='SPLIT'if roots else'NONSPLIT',
        rank_Y_minus_I=6,generators_preserve_line=True,exact_prime_order=True)


def verify_partition(domain,old,partial,oldrows,prior,gate,priorrows,saved,rows):
    values=domain['catalogue'];orbits=domain['orbits']
    need(type(values)is list and len(values)==domain['catalogue_size']==domain['selected_raw_domain_size']==14763
        and hashlib.sha256(canonical(values)).hexdigest()==domain['catalogue_sha256']
        and domain['selected_raw_domain_indices']==list(range(1,14764))and len(orbits)==3779
        and domain['endpoint_group_order']==288 and domain['prefix_stabilizer_order']==4,
        'same entire acquired catalogue and orbit metadata, not a new orbit enumeration')
    seen=set();reps=[]
    for orbit in orbits:
        need(type(orbit)is list and len(orbit)==4,'whole acquired original orbit row')
        rep,indices,transporters,stabilizer=orbit
        need(type(rep)is int and type(indices)is list and indices and indices==sorted(set(indices))
            and rep==min(indices)and not seen.intersection(indices)
            and all(type(j)is int and 1<=j<=14763 for j in indices)
            and type(transporters)is list and len(indices)==len(transporters)
            and type(stabilizer)is int and stabilizer>0 and len(indices)*stabilizer==4,'exact once-only original orbit identities')
        seen.update(indices);reps.append(rep)
    need(seen==set(range(1,14764))and reps==sorted(reps)and len(oldrows)==len(reps),'entire original14763/3779 cover')
    unpaid=[];paid=[];both=[]
    for rep,row in zip(reps,oldrows):
        need(type(row)is list and len(row)>=2 and type(row[0])is int and row[0]==rep,'original complete ordered old record')
        if row[1]=='UNPAID':
            need(len(row)==4,'whole old unpaid row')
            for f in row[2:]:
                if f is not None:
                    need(type(f)is list and len(f)==3 and type(f[0])is int and 1<=f[0]<=40 and f[1]=='PROPER','old proper37 encoding')
                    vector(f[2],7)
            unpaid.append(row)
            if all(f is not None for f in row[2:]):both.append(row)
        else:
            need(row[1]in('PREFIX_MEMBER','ADJACENT_LE2','END37'),'only an accepted old rejection tag')
            paid.append(rep)
    need([x[0]for x in unpaid]==old['unresolved_visited_orbits']==partial['unpaid_orbits']
        and len(unpaid)==535 and len(paid)==old['rejected_orbits']==partial['rejected_orbits']==3244,
        'exact old accepted3244/535 partition')
    selected=[x[0]for x in both]
    need(len(selected)==len(priorrows)==39 and selected==prior['newly_verified_representatives']==gate['newly_rejected_orbits'],
        'all actually accepted39, not an arbitrary handpicked subset')
    for before,after in zip(both,priorrows):
        need(after['representative']==before[0]and after['rejection']=='DOUBLE_PROPER_UNITARY_END_INTERSECTION'
            and after['all_mark_hypotheses_checked']is True,'exact prior accepted journal row')
        for f,oldf in zip((after['left'],after['right']),before[2:]):
            need(f['checkpoint']==oldf[0]and f['verified_fact']==oldf[1:],'same acquired proper37 fact')
    selected_set=set(selected);targets=[x for x in unpaid if x[0]not in selected_set]
    need([x[0]for x in targets]==prior['remaining_unpaid_orbits']==gate['unpaid_orbits']
        and len(targets)==496 and len(rows)==496,'exact remaining496 after old3283')
    rejected=[];remaining=[]
    for oldrow,row in zip(targets,rows):
        need(type(row)is dict and type(row.get('representative'))is int and row['representative']==oldrow[0]
            and row.get('status')in('UNPAID','REJECTED_END_INTERSECTION'),'one complete current row; FULL/interrupted unsupported')
        (rejected if row['status']=='REJECTED_END_INTERSECTION'else remaining).append(row['representative'])
    need(rejected==saved['newly_rejected_representatives']and len(rejected)==saved['new_rejected_orbits']==230
        and remaining==saved['unresolved_visited_orbits']and len(remaining)==266
        and not(set(rejected)&set(remaining)),'whole actual230/266 complement, never infer a miss')
    return values,targets,rejected,remaining


def main():
    budget=Budget()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated Python -E -B, assertions not optimized')
    ap=argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--journal',type=Path,required=True)
    args=ap.parse_args();paths=(args.output,args.journal)
    need(len(set(paths))==2 and all(p.is_absolute()and str(p)==str(p.absolute())and not os.path.lexists(p)
        and p.parent.resolve(strict=True)==p.parent and stat.S_ISDIR(p.parent.lstat().st_mode)for p in paths),
        'two fresh distinct absolute output files in ordinary existing parents')
    source_path=Path(__file__).absolute();self_stat=source_path.lstat()
    need(self_stat.st_size<=65536,'bounded current verifier Source')
    with source_path.open('rb')as f:self_raw=f.read(65537)
    self_ref=file_pin(source_path,self_raw);read_exact(self_ref,budget)
    inputs=current_inputs();documents={}
    for ref in inputs:documents[ref['path']]=read_exact(ref,budget)
    get=lambda ref:decode(documents[ref['path']])
    domain,export,normal,old,partial,prior,gate,saved=[get(x)for x in(DOMAIN,EXPORT,NORMAL,OLD_RESULT,PARTIAL,PRIOR_RESULT,PRIOR_GATE,SAVED_RESULT)]
    terminal,clearance,release,join,framegate,formgate,normalgate=[get(x)for x in(SAVED_TERMINAL,SAVED_CLEARANCE,SAVED_RELEASE,MODEL_JOIN,FRAME_GATE,FORMS_GATE,NORMAL_GATE)]
    need(domain['schema']=='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
        and domain['status']=='VERIFIED_CAYLEY_FRAME_AND_AUTOMORPHISM_DOMAIN'and domain['certificate_verified']is True
        and domain['field']==11 and domain['convention']=='RIGHT_ROW'and domain['rank']==4
        and domain['original_job']==[8,4]and domain['original_prefix_index']==8 and domain['selected_labels']==[1,4,2]
        and domain['prefix_export']==EXPORT and domain['normalization_result']==NORMAL and domain['model_bridge_source']==MODEL
        and domain['faithful_frame_acceptance']==FRAME_GATE and domain['forms_acceptance']==FORMS_GATE
        and domain['catalogue_proof']==CATALOGUE_PROOF and domain['catalogue_peer']==CATALOGUE_PEER
        and list(domain['origin'].values())==ORIGIN_INPUTS,'exact actual original natural Cayley domain and transport roles')
    need(export['schema']=='F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1'and export['original_job']==[8,4]
        and export['original_prefix_index']==8 and export['rank']==4 and export['selected_labels']==[1,4,2]
        and export['end_order']==[1,4,2,3]and export['convention']=='RIGHT_ROW'
        and export['origin']==domain['origin']and export['external_premises']==domain['external_premises'],
        'exact old original prefix, row action and faithful transport premises')
    need(domain['external_premises']==dict(root='/root',model_bridge_source=MODEL,model_source_join=MODEL_JOIN,original_A_equals_G=True)
        and join['root']=='/root'and join['schema']=='F004_PREFIX8_MODEL_SOURCE_JOIN_V1'
        and join['original_job']==[8,4]and join['original_prefix_index']==8 and join['original_A_equals_G']is True
        and join['model_bridge_source']==MODEL,'borrowed full natural model/A=G authority, not forms alone')
    model_gates=join['accepted_full_model_equality_premises']
    need(model_gates['cayley_normalization_gate']==NORMAL_GATE and model_gates['direct_forms_gate']==FORMS_GATE
        and model_gates['faithful_frame_gate']==FRAME_GATE and model_gates['theorem']==MODEL
        and model_gates['no_fresh_actual_model_equality_claim']is True,'same accepted model premises, no new group identification')
    need(framegate['status']=='ROOT_ACCEPTED_Q11_FAITHFUL_MATRIX_FRAME'and framegate['field']==11 and framegate['dimension']==7
        and formgate['root']=='/root'and formgate['status']=='ROOT_ACCEPTED_F004_Q11_DIRECT_INVARIANT_FORMS'
        and normalgate['root']=='/root'and normalgate['status']=='ROOT_ACCEPTED_F004_ACTUAL_SPLIT_CAYLEY_NORMALIZATION'
        and normalgate['result']==NORMAL and normalgate['faithful_frame_acceptance']==FRAME_GATE
        and normalgate['invariant_forms_acceptance']==FORMS_GATE,'borrowed actual frame/forms/kappa7 Root gates')
    need(normal['certificate_verified']is True and normal['kappa']==7
        and normal['coordinates']=='[scalar,v0,v1,v2,v3,v4,v5,v6]; right row coordinates'
        and normal['quadratic_matrix_convention']=='N(x)=x*Q*transpose(x); full polar matrix=2*Q',
        'canonical actual norm convention, never beta or polar2Q')
    need(old['schema']=='F004_PREFIX8_MATRIX_REJECTION_PASS_V1'and old['program']==SEARCH and old['domain']==DOMAIN
        and old['journal']==OLD_JOURNAL and old['status']=='INCOMPLETE_WITH_EXPLICIT_UNPAID_ORBITS'
        and old['started_orbits']==old['completed_orbits']==old['total_orbits']==3779
        and old['total_raw_domain']==14763 and old['unvisited_orbits']==[]and old['stop']is None,'complete old3779 journal')
    need(partial['root']=='/root'and partial['status']=='ROOT_ACCEPTED_QUALIFIED_PARTIAL_PREFIX8_MATRIX_REJECTIONS'
        and partial['domain']==DOMAIN and partial['result']==OLD_RESULT and partial['journal']==OLD_JOURNAL
        and partial['generation_source_attachment']==GENERATION_ATTACHMENT and partial['prefix_complete']is False
        and partial['original_root_roster_omission_preserved']is True and partial['retroactive_root_roster_freshness_claimed']is False,
        'old GEN-source omission remains qualified, no retroactive freshness')
    need(gate['schema']=='ROOT_F004_PREFIX8_DOUBLE_PROPER_ACCEPTANCE_V1'and gate['root']=='/root'
        and gate['status']=='ROOT_ACCEPTED_PREFIX8_DOUBLE_PROPER_END_REJECTIONS'and gate['domain']==DOMAIN
        and gate['result']==PRIOR_RESULT and gate['journal']==PRIOR_JOURNAL and gate['source_authentication']==PRIOR_AUTHORITY
        and gate['prior_partial_acceptance']==PARTIAL and gate['proof']==PROOF and gate['proof_review']==PROOF_REVIEW
        and gate['new_rejected_orbits']==39 and gate['old_rejected_orbits']==3244 and gate['total_rejected_orbits']==3283
        and gate['prefix_complete']is False and gate['unvisited_orbits']==[],'genuine old3283 adoption, no full-prefix claim')
    need(prior['schema']=='F004_PREFIX8_DOUBLE_PROPER_CERTIFICATE_V1'and prior['status']=='VERIFIED_ALL39_DOUBLE_PROPER_END_REJECTIONS'
        and prior['program']==PRIOR_PROGRAM and prior['domain']==DOMAIN and prior['original_export']==EXPORT
        and prior['old_result']==OLD_RESULT and prior['old_journal']==OLD_JOURNAL and prior['journal']==PRIOR_JOURNAL
        and prior['partial_acceptance']==PARTIAL and prior['new_rejected_orbits']==39
        and prior['old_rejected_orbits_preserved']==3244 and prior['remaining_unpaid_count']==496,'same actual accepted39 result')
    need(saved['schema']=='F004_PREFIX8_MOVED19_ORDER4_SEARCH_RESULT_V1'
        and saved['status']=='BOUNDED_MOVED19_ORDER4_END_CERTIFICATES_WITH_EXPLICIT_UNPAID'
        and saved['program']==SAVED_WORKER and saved['domain']==DOMAIN and saved['original_export']==EXPORT
        and saved['prior_gate']==PRIOR_GATE and saved['prior_result']==PRIOR_RESULT and saved['journal']==SAVED_JOURNAL
        and saved['original_job']==[8,4]and saved['original_prefix_index']==8 and saved['prior_accepted_orbits']==3283
        and saved['started_orbits']==saved['completed_orbits']==saved['target_orbits']==496
        and saved['unvisited_orbits']==[]and saved['stop']is None and saved['prefix_complete']is False
        and saved['root_adoption']is None and saved['moved19_alone_is_not_FULL_G2']is True
        and saved['full19_requires_same_end_exact4']is True and saved['original_weights_reproved']is False,
        'whole returned496 search input, no search status taken as proof')
    tool=terminal['actual_tool']
    need(type(tool)is dict and set(tool)=={'handle','initial_chunk','terminal_chunk','exit_code','synchronous'}
        and type(tool['exit_code'])is int and tool['exit_code']==0 and type(tool['synchronous'])is bool,
        'genuine typed successful prior scientific tool')
    need(terminal['root']=='/root'and terminal['purpose']=='moved19_order4'
        and terminal['status']=='ROOT_RETURNED_BOUNDED_PREFIX8_PASS'and terminal['passed']is True
        and terminal['result']==SAVED_RESULT and terminal['release']==SAVED_RELEASE
        and clearance['root']=='/root'and clearance['terminal']==SAVED_TERMINAL and clearance['actual_tool']==tool
        and clearance['known_scope_drained']is True and release['root']=='/root'and release['program']==SAVED_WORKER,
        'actual previous result and genuine Root closure; no new lifetime observation')
    old_records=framed(documents[OLD_JOURNAL['path']],3780)
    prior_records=framed(documents[PRIOR_JOURNAL['path']],40)
    records=framed(documents[SAVED_JOURNAL['path']],497)
    h0,h1,h2=old_records[0],prior_records[0],records[0];words=h0['word_schedule']
    need(type(words)is list and len(words)==40
        and all(type(s)is str and len(s)==4*(i+1)and all(c in'1234'for c in s)for i,s in enumerate(words))
        and all(words[i+1].startswith(words[i])for i in range(39)),'exact bounded inherited checkpoint strings')
    need(h0['program']==SEARCH and h0['domain']==DOMAIN and h0['original_export']==EXPORT
        and h0['word_schedule_source']==SCHEDULE_SOURCE and h0['word_power']==3 and h0['prime']==37
        and GENERATION in h0['direct_inputs']and h1['program']==PRIOR_PROGRAM and h1['domain']==DOMAIN
        and h1['old_journal']==OLD_JOURNAL and h1['partial_acceptance']==PARTIAL,'old complete journal Source/word identities')
    expected_proofs=[SPLIT_PROOF,SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW,PROOF,PROOF_REVIEW,MOVED19_ORDER4_THEORY,MOVED19_ORDER4_REVIEW]
    need(h2['schema']=='F004_PREFIX8_MOVED19_ORDER4_WITNESS_JOURNAL_V1'and h2['program']==SAVED_WORKER
        and h2['domain']==DOMAIN and h2['original_export']==EXPORT and h2['prior_gate']==PRIOR_GATE
        and h2['prior_result']==PRIOR_RESULT and h2['old_journal']==OLD_JOURNAL
        and h2['original_job']==[8,4]and h2['original_prefix_index']==8 and h2['proofs']==saved['proofs']==expected_proofs
        and h2['word_schedule_source']==SCHEDULE_SOURCE and h2['word_checkpoint_count']==40 and h2['word_max_length']==160
        and h2['new_word_power']==7 and h2['new_prime']==19 and h2['cached37_word_power']==3
        and h2['canonical_norm']==NORMAL and h2['normalization_source']==NORMALIZER_SOURCE
        and h2['direct_inputs']==saved['scientific_direct_inputs']==ANCESTOR_INPUTS,
        'whole actual current header and its exact scientific readset/proof roles')
    values,targets,rejected,remaining=verify_partition(domain,old,partial,old_records[1:],prior,gate,prior_records[1:],saved,records[1:])
    need(h2['target_representatives']==[x[0]for x in targets],'all496 actual targets, no cherry picking')
    r=matrix(domain['standard_to_actual_row_map'],8);ir=matrix(domain['actual_to_standard_row_map'],8)
    q=matrix(normal['quadratic_form_matrix'],8)
    need(q==tuple(zip(*q))and rank(q,budget)==8 and q[0]==(1,0,0,0,0,0,0,0)
        and all(q[i][0]==0 for i in range(1,8))and [list(v[1:])for v in q[1:]]==normal['pure_quadratic_form_matrix'],
        'nonsingular actual scalar/pure canonical quadratic matrix')
    need(product(r,ir,budget)==product(ir,r,budget)==unit(8),'full inverse actual/standard frame maps')
    prefix=[pure_actual(matrix(m,8),r,ir,q,budget)for m in domain['standard_ordered_prefix_matrices']]
    need(len(prefix)==3 and prefix==[matrix(m,7)for m in export['matrices']]and len(set(prefix))==3,
        'full ordered actual prefix7 equals original faithful exported matrices')
    verified=[];counts={'SPLIT_SPLIT':0,'SPLIT_UNITARY':0};journal_bytes=0
    with args.journal.open('xb')as out:
        def append(value):
            nonlocal journal_bytes
            raw=canonical(value)+b'\n'
            need(len(raw)<=RECORD_CAP and journal_bytes+len(raw)<=OUTPUT_CAP-32768,'complete bounded evidence records plus report reserve')
            need(out.write(raw)==len(raw),'whole fresh witness write');out.flush();journal_bytes+=len(raw)
        append(dict(schema='F004_PREFIX8_SAVED230_INDEPENDENT_WITNESSES_V1',program=self_ref,source_worker=SAVED_WORKER,
            saved_result=SAVED_RESULT,saved_journal=SAVED_JOURNAL,domain=DOMAIN,original_export=EXPORT,canonical_norm=NORMAL,
            proper_end_theorem=SPLIT_PROOF,theorem_reviews=[SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW],prior_gate=PRIOR_GATE,
            original_job=[8,4],original_prefix_index=8,derived_targets=[x[0]for x in targets],required_rejections=rejected,
            independent_plain_F11=True,ancestor_functions_loaded=False,full_end_or_order4_certificate_verified=False,
            original_weights_reproved=False,candidate_credit=0,census_credit=0))
        for oldrow,row in zip(targets,records[1:]):
            if row['status']=='UNPAID':continue
            rep=row['representative'];standard=catalogue_operator(values[rep-1],rep,budget)
            c=pure_actual(standard,r,ir,q,budget);ends=actual_marks(prefix,c,budget)
            facts=[verify_side(end,fact,oldfact,words,q,budget)
                for end,fact,oldfact in zip(ends,(row['left'],row['right']),oldrow[2:])]
            kinds=[f['kind']for f in facts]
            case='SPLIT_SPLIT'if kinds==['PROPER19','PROPER19']else'SPLIT_UNITARY'
            need(kinds==['PROPER19','PROPER19']or sorted(kinds)==['PROPER19','PROPER37'],
                'actual two positive proper ends include a split end; no duplicate old U/U')
            need(row['case']==case and row['theorem']==SPLIT_PROOF and row['middle']=='<b,c>'
                and row['middle_order_upper_bound']==(266 if case=='SPLIT_SPLIT'else 264)
                and row['intersection_lower_comparison']==('>479'if case=='SPLIT_SPLIT'else'>=480'),
                'exact witnessed hypotheses for the reviewed proper-end IP obstruction')
            append(dict(representative=rep,rejection='INDEPENDENT_PROPER_END_INTERSECTION',case=case,
                source_record_sha256=hashlib.sha256(canonical(row)+b'\n').hexdigest(),left=facts[0],right=facts[1],
                actual_marks_and_commutations_verified=True,middle_order_upper_bound=266 if case=='SPLIT_SPLIT'else 264))
            verified.append(rep);counts[case]+=1;budget.check()
        need(verified==rejected and len(verified)==230 and sum(counts.values())==230,'every actual rejection independently verified')
        out.flush();os.fsync(out.fileno())
    for ref in inputs:read_exact(ref,budget,False)
    need(read_exact(self_ref,budget,False)==self_raw,'whole new Source unchanged through verification')
    with args.journal.open('rb')as f:journal_raw=f.read(OUTPUT_CAP+1)
    need(len(journal_raw)==journal_bytes<=OUTPUT_CAP,'bounded entire freshly written witness file')
    result=dict(schema='F004_PREFIX8_SAVED230_INDEPENDENT_CERTIFICATE_V1',status='VERIFIED_ALL230_ACTUAL_PROPER_END_INTERSECTIONS',
        program=self_ref,source_worker=SAVED_WORKER,saved_result=SAVED_RESULT,saved_journal=SAVED_JOURNAL,
        saved_terminal=SAVED_TERMINAL,saved_clearance=SAVED_CLEARANCE,saved_workflow=SAVED_WORKFLOW,
        domain=DOMAIN,original_export=EXPORT,canonical_norm=NORMAL,model_source_join=MODEL_JOIN,prior_gate=PRIOR_GATE,
        journal=file_pin(args.journal,journal_raw),original_job=[8,4],original_prefix_index=8,
        newly_verified_representatives=verified,new_rejected_orbits=len(verified),rejection_type_counts=counts,
        prior_accepted_orbits_preserved=3283,prior_acceptance_and_weights_borrowed=True,
        remaining_unpaid_orbits=remaining,remaining_unpaid_count=len(remaining),unvisited_orbits=[],prefix_complete=False,
        proper_end_theorem=SPLIT_PROOF,theorem_reviews=[SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW],
        scientific_direct_inputs=inputs,scientific_direct_inputs_reauthenticated=True,
        independent_plain_F11=True,ancestor_functions_loaded=False,word_search_executed=False,
        full_end_or_order4_certificate_verified=False,subgroup_closure_executed=False,exact_end_order_engine_executed=False,
        original_weights_reproved=False,original_permutation_lifts_executed=False,root_adoption=None,
        candidate_credit=0,census_credit=0,whole_original_credit=0,
        worker_limits=dict(verification_seconds=WORK_SECONDS,total_seconds=TOTAL_SECONDS,rss_bytes=RSS_CAP,
            direct_document_bytes=DOCUMENT_CAP,unique_direct_input_bytes=UNIQUE_INPUT_CAP,combined_output_bytes=OUTPUT_CAP),
        outer_profile_required=dict(rss_mib=256,seconds=150),seconds=time.monotonic()-budget.start,peak_self_bytes=peak_bytes(),
        qualification='Only the complete actual230 positive S/S or S/U certificates are re-evaluated. Old3283, '
        'natural full-model/A=G/original transport and orbit weights are separately borrowed exact premises. '
        'All266 misses remain unpaid. No order4/FULL certificate is asserted; no automatic adoption or prefix/census credit.')
    raw=canonical(result)+b'\n'
    need(len(raw)<=32768 and journal_bytes+len(raw)<=OUTPUT_CAP,'bounded complete report, no clipping')
    budget.check(False)
    with args.output.open('xb')as f:need(f.write(raw)==len(raw),'whole fresh final certificate');f.flush();os.fsync(f.fileno())
    print(canonical(dict(status=result['status'],verified230=len(verified),remaining_unpaid=len(remaining),
        output=file_pin(args.output,raw),journal=result['journal'],candidate_credit=0,census_credit=0)).decode())


if __name__=='__main__':main()
