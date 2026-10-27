#!/usr/bin/env python3
"""Portable direct checks for the final62 indexed markings.

Adapted by /root/q11_batch_source_review from the independent matrix,
finite-parabolic, line-bound and Schreier checkers identified in provenance.
Only standard-library modules are imported. Original model/domain acquisition
and the stated classical classification and stabilizer facts remain premises.
"""
import time
START = time.monotonic()
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import struct
import sys

HERE = Path(__file__).resolve().parent
DATA = dict(file='delta.json', bytes=30656,
    sha256='e5b91d44aa906c480c96d07206db2fb8fcf79f8cfbc026497ca87e67cb5a2374')
BASE_CHECK = dict(file='../shared_obstructions/check.py', bytes=15399,
    sha256='863eb2f8134e46300e606e987c3455953ae1a50192d9bec00f555b550cd3a5f7')
I = bytes(int(i == j) for i in range(7) for j in range(7))
ORDER = 11**6*(11**6-1)*(11**2-1)
JOB_COUNTS = {12:685,15:3801,16:3779,17:7455,19:694}
POSITIVES = ((15,366),(15,515),(15,1055),(15,1253),(15,2252),(15,2285),
    (15,2303),(15,2988),(15,3009),(15,3101),(15,3126),(16,189),(16,423),(16,483))


def require(ok, why):
    if not ok:
        raise ValueError(why)


def integer(x, low, high):
    return type(x) is int and low <= x <= high


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),
                      ensure_ascii=True,allow_nan=False).encode('ascii')


def parse(raw):
    def unique(pairs):
        result = {}
        for key,value in pairs:
            require(key not in result,'Unique JSON keys')
            result[key] = value
        return result
    return json.loads(raw,object_pairs_hook=unique,
        parse_float=lambda x: (_ for _ in ()).throw(ValueError(x)),
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def columns(matrix):
    return tuple(matrix[j::7] for j in range(7))


def matrix(value, size=7):
    require(type(value) is list and len(value) == size
        and all(type(row) is list and len(row) == size for row in value)
        and all(integer(x,0,10) for row in value for x in row),'Full canonical F11 matrix')
    return bytes(x for row in value for x in row)


def vector(value):
    require(type(value) is list and len(value) == 7
        and all(integer(x,0,10) for x in value) and any(value),'Nonzero canonical F11 row')
    return tuple(value)


def row_product(v, g):
    return tuple(sum(v[k]*g[7*k+j] for k in range(7)) % 11 for j in range(7))


def line_scalar(v, image):
    at = next(i for i,x in enumerate(v) if x)
    require(any(image),'Invertible image of nonzero row')
    scalar = image[at]*pow(v[at],-1,11) % 11
    require(scalar != 0 and image == tuple(scalar*x % 11 for x in v),'Exact projective line preservation')
    return scalar


class Check:
    def __init__(self):
        self.refs = {}
        self.read_bytes = 0
        self.products = 0
        self.peak = 0

    def tick(self):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        self.peak = max(self.peak,rss)
        require(rss <= 128*2**20 and time.monotonic()-START < 125,
                'Per-invocation125s / 128MiB sampled resource limits')

    def read(self, ref):
        self.tick()
        require(type(ref) is dict and set(ref) == {'file','bytes','sha256'}
            and type(ref['file']) is str and integer(ref['bytes'],0,16*2**20)
            and type(ref['sha256']) is str and len(ref['sha256']) == 64
            and set(ref['sha256']) <= set('0123456789abcdef'),'Full local file pin')
        name = ref['file']
        if name.startswith('../shared_obstructions/'):
            require(name.split('/') == ['..','shared_obstructions',name.rsplit('/',1)[1]]
                and name.rsplit('/',1)[1] in ('check.py','portabledata.json','cache.u8','verification.json'),
                'Only the frozen sibling baseline roles')
        else:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts
                and (name == 'delta.json' or name.startswith('trees/')),'Only adjacent certificate files')
        path = Path(os.path.abspath(HERE/name))
        a = path.lstat()
        require(path.resolve(strict=True) == path and stat.S_ISREG(a.st_mode)
            and a.st_nlink == 1 and a.st_size == ref['bytes'],'Ordinary canonical single-link input')
        require(self.refs.get(name,ref) == ref and self.read_bytes+ref['bytes'] <= 32*2**20
            and (name in self.refs or len(self.refs) < 48),'One identity;32MiB total reads;48files')
        with path.open('rb') as f:
            b = os.fstat(f.fileno());raw = f.read(ref['bytes']+1);c = os.fstat(f.fileno())
        sig = lambda s: (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        require(sig(a) == sig(b) == sig(c) == sig(path.lstat()) and len(raw) == ref['bytes']
            and hashlib.sha256(raw).hexdigest() == ref['sha256'],'Stable complete file SHA256')
        self.refs[name] = ref;self.read_bytes += len(raw);self.tick()
        return raw

    def recheck(self):
        for ref in list(self.refs.values()):
            self.read(ref)

    def product(self, left, right_columns):
        self.products += 1
        require(self.products <= 2500000,'Per-invocation2500000 matrix product bound')
        if self.products % 256 == 0:
            self.tick()
        result = bytearray(49)
        for i in range(7):
            a,b,c,d,e,f,g = left[7*i:7*i+7]
            for j,v in enumerate(right_columns):
                result[7*i+j] = (a*v[0]+b*v[1]+c*v[2]+d*v[3]+e*v[4]+f*v[5]+g*v[6]) % 11
        return bytes(result)

    def multiply(self, a, b):
        return self.product(a,columns(b))

    def power(self, value, exponent):
        require(integer(exponent,0,ORDER),'Bounded nonnegative exponent')
        result = I
        while exponent:
            if exponent & 1:
                result = self.multiply(result,value)
            exponent >>= 1
            if exponent:
                value = self.multiply(value,value)
        return result

    def word(self, marks, letters, mask=15):
        require(type(letters) is list and 1 <= len(letters) <= 64
            and all(integer(j,0,3) and mask & (1 << j) for j in letters),'Literal word in its required generator set')
        value = I
        for j in letters:
            value = self.multiply(value,marks[j])
        return value

    def small_group(self, marks, mask):
        alphabet = tuple(j for j in range(4) if mask & (1 << j))
        right = tuple(columns(g) for g in marks)
        group = {I};queue = [I]
        for value in queue:
            for j in alphabet:
                z = self.product(value,right[j])
                if z not in group:
                    require(len(group) < 4096,'Complete small subgroup cap4096')
                    group.add(z);queue.append(z)
        return group


def context(check, data):
    require(data['schema'] == 'PORTABLE_COMPLETE_FIVE_FAMILY_MARKED_CENSUS_V1'
        and data['field'] == 11 and data['dimension'] == 7 and data['group_order'] == ORDER
        and data['fixed_prefix_order'] == ['a','e','b']
        and data['mark_order'] == ['a','b','candidate_final','e'],'Exact portable delta and marking convention')
    require(data['baseline']['check.py'] == BASE_CHECK,'Frozen unchanged baseline checker')
    cache = check.read(data['baseline']['cache.u8'])
    require(len(cache) == 14763*49 and all(x < 11 for x in cache),'Whole canonical acquired catalogue cache')
    fixed = {r['prefix']:tuple(matrix(g) for g in r['matrices']) for r in data['fixed_prefixes']}
    require(set(fixed) == {15,16} and all(len(v) == 3 for v in fixed.values()),'Only two unresolved fixed prefixes')
    eligible = {tuple(p) for p in data['baseline_unresolved']}
    require(len(eligible) == 62 and len(data['baseline_unresolved']) == 62,'Exact62 distinct unresolved triples')
    def marks(position):
        require(type(position) is list and len(position) == 3
            and all(type(x) is int for x in position) and tuple(position) in eligible,'Exact included original position')
        p,index,representative = position;a,e,b = fixed[p]
        require(1 <= representative <= 14763 and 1 <= index <= JOB_COUNTS[p],'Original position bounds')
        c = cache[49*(representative-1):49*representative];result = (a,b,c,e)
        require(len(set(result)) == 4,'Four distinct marked matrices')
        for g in result:
            require(g != I and check.multiply(g,g) == I,'All marked matrices are nonidentity involutions')
        for i in range(4):
            for j in range(i+2,4):
                require(check.multiply(result[i],result[j]) == check.multiply(result[j],result[i]),
                        'Every distant pair commutes')
        return result
    Q = matrix(data['canonical_norm']['Q'],8)
    q = matrix(data['canonical_norm']['pure'])
    beta = matrix(data['canonical_norm']['beta'])
    require(data['canonical_norm']['kappa'] == 7 and Q[:8] == bytes((1,0,0,0,0,0,0,0))
        and all(Q[8*i] == 0 for i in range(1,8))
        and q == bytes(Q[8*i+j] for i in range(1,8) for j in range(1,8))
        and q == bytes(7*x % 11 for x in beta)
        and all(Q[8*i+j] == Q[8*j+i] for i in range(8) for j in range(8)),
        'Exact acquired canonical Q and pure q=7beta, not2Q or an arbitrary scale')
    return marks,Q


def typed_end(check, marks, Q, side, cert):
    require(side in (0,1) and cert['prime'] in (19,37),'End and recognition prime')
    mask = 7 if side == 0 else 14;end = (0,1,2) if side == 0 else (1,2,3)
    v = vector(cert['fixed_row']);signs = cert['end_signs']
    require(type(signs) is list and len(signs) == 3 and all(type(s) is int and s in (1,10) for s in signs),
            'Three involution line signs')
    for j,s in zip(end,signs):
        require(row_product(v,marks[j]) == tuple(s*x % 11 for x in v),'The whole end preserves its supplied pure line')
    full = (0,)+v;norm = sum(full[i]*Q[8*i+j]*full[j] for i in range(8) for j in range(8)) % 11
    kind = 'S' if cert['prime'] == 19 else 'U'
    require(type(cert['canonical_norm']) is int and 0 < norm == cert['canonical_norm'] < 11
        and cert['type'] == kind and pow(-norm % 11,5,11) == (1 if kind == 'S' else 10),
        'Nonzero canonical norm and squareclass of its negative')
    Y = check.power(check.word(marks,cert['word'],mask),cert['cofactor'])
    require(Y != I and check.power(Y,cert['prime']) == I and row_product(v,Y) == v,
            'Actual same-end prime-order word and fixed pure row')
    # Under the attributed natural Cayley and classical subgroup premises,
    # the distinct commuting outer involutions and this prime imply that
    # this three-generator end is its entire specified line stabilizer.
    order = 2*11**3*(11**3+(-1 if kind == 'S' else 1))*(11**2-1)
    return v,order


def common_checks(check, data, marks_for, Q):
    old = parse(check.read(data['baseline']['portabledata.json']))
    require(old['unresolved'] == data['baseline_unresolved'],'Literal62-row join to the baseline')
    original = {j['job'][0]:j for j in old['jobs']}
    require({p:len(j['orbits']) for p,j in original.items()} == JOB_COUNTS,'Original five domain sizes')
    for row in data['fixed_prefixes']:
        require(row['matrices'] == original[row['prefix']]['fixed_prefix'],'Exact compact fixed-prefix copy')
    for p,index,rep in data['baseline_unresolved']:
        require(original[p]['orbits'][index-1][0] == rep,'Every exact original representative')
    obstructions = data['obstructions'];covered = set()
    def add(position):
        key = tuple(position);require(key not in covered,'No repeated obstruction');covered.add(key)
    require(len(obstructions['two_ends']) == 39 and len(obstructions['common_words']) == 3
        and len(obstructions['one_end']) == 6,'Exact39+3+6 delta obstruction counts')
    for row in obstructions['two_ends']:
        position = row[:3];marks = marks_for(position);add(position)
        _,left_order = typed_end(check,marks,Q,0,row[3])
        _,right_order = typed_end(check,marks,Q,1,row[4])
        D = check.small_group(marks,6)
        require(left_order*right_order > ORDER*len(D),
                'Product-set lower bound forces the two full ends to intersect beyond the exact middle')
    for row in obstructions['common_words']:
        position = row[:3];marks = marks_for(position);add(position)
        h = check.word(marks,row[3],7)
        require(h == check.word(marks,row[4],14) and h not in check.small_group(marks,6),
                'Literal common word in the two ends lies outside the exact middle')
    for row in obstructions['one_end']:
        position = row[:3];marks = marks_for(position);add(position);side = row[3]
        v,_ = typed_end(check,marks,Q,side,row[4])
        h = check.word(marks,row[5],14 if side == 0 else 7)
        require(line_scalar(v,row_product(v,h)) in (1,10) and h not in check.small_group(marks,6),
                'Opposite-end word preserves the recognized full line stabilizer and is outside the middle')
    positive = [tuple(r['position']) for r in data['positive_markings']]
    require(len(positive) == len(set(positive)) == 14
        and tuple((p,i) for p,i,r in positive) == POSITIVES
        and not(covered & set(positive))
        and covered | set(positive) == {tuple(p) for p in data['baseline_unresolved']},
        'All62 exact remaining original positions split into48 obstructions and14 positive candidates')
    return dict(checked_delta_obstructions=48,two_recognized_ends=39,common_words=3,one_recognized_end=6,
                exact62_position_join_and_partition=True)


def generation(check, marks, facts):
    require(type(facts) is list and [w['prime'] for w in facts] == [19,37],'Two whole-marking generation witnesses')
    for fact in facts:
        require(fact['cofactor'] == ORDER//fact['prime'],'Literal whole-group prime cofactor')
        Y = check.power(check.word(marks,fact['word']),fact['cofactor'])
        require(Y != I and check.power(Y,fact['prime']) == I,'Exact supplied prime-order power in the whole marking')


def tree_group(check, marks, mask, tree):
    n = tree['count'];require(integer(n,1,200000),'Complete endpoint size at most200000')
    parents = check.read(tree['parents']);letters = check.read(tree['letters'])
    require(len(parents) == 4*n and len(letters) == n and letters[0] == 255
        and struct.unpack_from('<I',parents,0)[0] == 0,'Whole identity-rooted word-tree arrays')
    values = [I];right = tuple(columns(g) for g in marks)
    for k in range(1,n):
        parent = struct.unpack_from('<I',parents,4*k)[0];j = letters[k]
        require(parent < k and j in range(4) and mask & (1 << j),'Earlier parent and endpoint generator')
        values.append(check.product(values[parent],right[j]))
    digest = hashlib.sha256()
    for value in values:
        digest.update(value)
    require(digest.hexdigest() == tree['matrix_sha256'],'Regenerated full ordered matrix table equals its source hash')
    group = set(values);require(len(group) == n,'No duplicate table elements')
    for value in values:
        for j in range(4):
            if mask & (1 << j):
                require(check.product(value,right[j]) in group,'Every endpoint generator edge closes')
    return group


def finite_case(check, marks, case):
    require(set(case['trees']) == {'7','14'} and len(case['sizes']) == 15,'Both complete end trees and fifteen sizes')
    groups = {}
    for mask in range(15):
        groups[mask] = (tree_group(check,marks,mask,case['trees'][str(mask)])
            if mask in (7,14) else check.small_group(marks,mask))
        require(len(groups[mask]) == case['sizes'][mask],'Exact proper-parabolic order')
    for left in range(15):
        for right in range(left+1,15):
            require(groups[left] & groups[right] == groups[left & right],
                    'All105 distinct proper-mask intersections equal their required subgroup')
    return dict(method='finite',proper_parabolic_orders=case['sizes'],proper_mask_pairs_checked=105)


def line_case(check, marks, case):
    big = case['large_end'];require(big in (7,14),'Specified unenumerated endpoint')
    lines = [vector(v) for v in case['lines']];require(lines,'At least one supplied invariant line')
    for v in lines:
        for j in range(4):
            if big & (1 << j):
                require(line_scalar(v,row_product(v,marks[j])) in (1,10),'Large-end generators preserve every supplied line')
    finite = 14 if big == 7 else 7
    require(set(case['trees']) == {str(finite)},'Only the opposite finite endpoint tree')
    sizes = dict(case['sizes']);require(set(sizes) == set(range(15))-{big},'All fourteen finite proper masks')
    groups = {}
    for mask in sizes:
        groups[mask] = (tree_group(check,marks,mask,case['trees'][str(mask)])
            if mask == finite else check.small_group(marks,mask))
        require(len(groups[mask]) == sizes[mask],'Exact finite subgroup order')
    for left in range(15):
        for right in range(left+1,15):
            if big not in (left,right):
                require(groups[left] & groups[right] == groups[left & right],'Exact finite subgroup intersection')
            else:
                other = right if left == big else left
                if other & big == other:
                    continue
                meet = set()
                for g in groups[other]:
                    preserved = True
                    for v in lines:
                        image = row_product(v,g);at = next(i for i,x in enumerate(v) if x)
                        scalar = image[at]*pow(v[at],-1,11) % 11
                        if scalar == 0 or image != tuple(scalar*x % 11 for x in v):
                            preserved = False;break
                    if preserved:
                        meet.add(g)
                require(meet == groups[other & big],
                        'Stabilizer upper bound equals the word-generated lower bound')
    return dict(method='line',large_end_mask=big,proper_mask_pairs_checked=105,
                no_exact_large_end_order_or_line_search_completeness_assumed=True)


def schreier_case(check, marks, case):
    n = case['count'];require(n == 1320,'Exact finite conjugation orbit size')
    raw = case['seed'];require(type(raw) is list and len(raw) == 49
        and all(integer(x,0,10) for x in raw),'Canonical matrix conjugation point')
    X = bytes(raw)
    for j in (1,2,3):
        require(check.multiply(X,marks[j]) == check.multiply(marks[j],X),'The right endpoint fixes the conjugation point')
    parents = check.read(case['parents']);letters = check.read(case['letters'])
    require(len(parents) == 4*n and len(letters) == n and letters[0] == 255
        and struct.unpack_from('<I',parents,0)[0] == 0,'Complete conjugation word tree')
    trans = [I];inverse = [I];states = [X]
    for k in range(1,n):
        parent = struct.unpack_from('<I',parents,4*k)[0];j = letters[k]
        require(parent < k and j in (0,1,2),'Earlier left-end word parent')
        trans.append(check.multiply(trans[parent],marks[j]))
        inverse.append(check.multiply(marks[j],inverse[parent]))
        states.append(check.multiply(check.multiply(inverse[k],X),trans[k]))
    for values,key in ((states,'states_sha256'),(trans,'transversals_sha256'),(inverse,'inverses_sha256')):
        digest = hashlib.sha256()
        for value in values:
            digest.update(value)
        require(digest.hexdigest() == case[key],'Regenerated complete ordered orbit data equal their source hashes')
    by_state = {x:i for i,x in enumerate(states)};require(len(by_state) == n,'All1320 states distinct')
    D = check.small_group(marks,6);require(len(D) == 20,'Exact complete middle group')
    for k,x in enumerate(states):
        require(check.multiply(trans[k],inverse[k]) == I
            and check.multiply(inverse[k],trans[k]) == I,'Actual inverse transversals, without scalar normalization')
        for j in (0,1,2):
            target = check.multiply(check.multiply(marks[j],x),marks[j]);at = by_state.get(target)
            require(at is not None,'Entire conjugation orbit closes under every left generator')
            loop = check.multiply(check.multiply(trans[k],marks[j]),inverse[at])
            require(loop in D,'Each exact right-action Schreier loop lies in the middle subgroup')
    proper = {end:[m for m in range(16) if m != end and m & end == m] for end in (7,14)}
    groups = {m:check.small_group(marks,m) for m in sorted(set(proper[7]+proper[14]))}
    for end in (7,14):
        for k,left in enumerate(proper[end]):
            for right in proper[end][k+1:]:
                require(groups[left] & groups[right] == groups[left & right],
                        'Every proper-mask intersection in each rank-three endpoint')
    return dict(method='schreier',complete_orbit_states=1320,exact_Schreier_loops_checked=3960,
                rank_three_proper_mask_pairs_checked=42,conjugation_action_faithfulness_assumed=False)


def main():
    require(sys.dont_write_bytecode and (sys.flags.isolated or sys.flags.ignore_environment),
            'Use python3 -I -B -S')
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--case',required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('125 second checker limit')))
    signal.setitimer(signal.ITIMER_REAL,max(.001,125-(time.monotonic()-START)))
    check = Check();data = parse(check.read(DATA))
    if args.case == 'baseline':
        for ref in data['baseline'].values():
            check.read(ref)
        require(data['baseline']['check.py'] == BASE_CHECK,'Exact unchanged baseline Source')
        signal.setitimer(signal.ITIMER_REAL,0)
        os.execv(sys.executable,[sys.executable,'-I','-B','-S',str((HERE/BASE_CHECK['file']).resolve())])
    marks_for,Q = context(check,data)
    if args.case == 'obstructions':
        detail = common_checks(check,data,marks_for,Q)
    else:
        selected = [r for r in data['positive_markings'] if '%s_%s' % tuple(r['position'][:2]) == args.case]
        require(len(selected) == 1 and tuple(selected[0]['position'][:2]) in POSITIVES,'One declared original positive case')
        case = selected[0];marks = marks_for(case['position']);generation(check,marks,case['generation'])
        method = case['method']
        require(method in ('finite','line','schreier'),'Known direct IP method')
        detail = {'finite':finite_case,'line':line_case,'schreier':schreier_case}[method](check,marks,case)
        detail.update(position=case['position'],whole_marking_generation_verified=True,intersection_property_verified=True)
    check.recheck();check.tick()
    receipt = dict(status='PASS_PORTABLE_MARKED_CENSUS_CASE',case=args.case,details=detail,
        data=DATA,baseline_cache=data['baseline']['cache.u8'],
        resources=dict(seconds=time.monotonic()-START,sampled_peak_rss_bytes=check.peak,
            matrix_products=check.products,physical_input_bytes_read=check.read_bytes,
            wall_limit_seconds=125,sampled_rss_limit_bytes=128*2**20,product_limit=2500000),
        original_model_and_domains_reacquired=False,classifications_reproved=False,
        complete_package_claim_requires_all_driver_cases=True,whole_F004_or_manuscript_claim=False,
        new_open_conjecture_claim=False,Lean_claim=False,compression_measurement_claim=False)
    signal.setitimer(signal.ITIMER_REAL,0)
    print(encode(receipt).decode())


if __name__ == '__main__':
    main()
