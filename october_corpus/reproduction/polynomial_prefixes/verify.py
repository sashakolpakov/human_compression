#!/usr/bin/env python3
"""Replay ten polynomial identities over F_11 using Python's standard library.

The model, original frame and exhaustive maximal cover are explicit imports.
There is no coefficient search, elimination, process launch or private input.
"""
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
    raise SystemExit('Run without -O.')
START = time.monotonic()
PRODUCTS = 0
DIAGONAL_ADDITIONS = 0
EXPECTED = [156,160,166,167,168,170,174,175,183,187]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def budget():
    require(time.monotonic()-START < 100, '100-second wall cap')
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        rss *= 1024
    require(rss < 128*2**20, '128-MiB RSS cap')

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def parse(raw):
    def unique(items):
        result = {}
        for key,value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def finite(text):
        value = float(text)
        require(math.isfinite(value), 'finite JSON number')
        return value
    def invalid(_):
        raise ValueError('nonfinite JSON constant')
    return json.loads(raw,object_pairs_hook=unique,parse_float=finite,parse_constant=invalid)

def matrix(value, n):
    require(type(n) is int and 1 <= n <= 7, 'matrix dimension')
    require(type(value) in (list,tuple) and len(value)==n, 'matrix rows')
    require(all(type(row) in (list,tuple) and len(row)==n for row in value), 'matrix columns')
    require(all(type(x) is int and 0 <= x < 11 for row in value for x in row), 'matrix entries')
    return tuple(tuple(row) for row in value)

def one(n):
    return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))

def product(left,right):
    global PRODUCTS
    n=len(left)
    require(1 <= n <= 7 and len(right)==n and all(len(row)==n for row in left+right), 'product shapes')
    PRODUCTS += 1
    require(PRODUCTS <= 400000, '400000 matrix-product cap')
    budget()
    rows=[]
    for i in range(n):
        row=[]
        for j in range(n):
            total=0
            for k in range(n):
                total += left[i][k]*right[k][j]
            row.append(total % 11)
        rows.append(tuple(row))
    return tuple(rows)

def repeated_power(value,exponent):
    require(type(exponent) is int and 0 <= exponent <= 55, 'literal exponent at most55')
    result=one(len(value))
    for _ in range(exponent):
        result=product(result,value)
    return result

def horner(value,coefficients):
    global DIAGONAL_ADDITIONS
    require(type(coefficients) is list and 1 <= len(coefficients) <= 7, 'one to seven coefficients')
    require(all(type(x) is int and 0 <= x < 11 for x in coefficients), 'literal field coefficients')
    n=len(value)
    result=tuple(tuple(coefficients[-1]*int(i==j) for j in range(n)) for i in range(n))
    for coefficient in reversed(coefficients[:-1]):
        result=product(result,value)
        DIAGONAL_ADDITIONS += n
        require(DIAGONAL_ADDITIONS <= 200000, '200000 separate scalar-addition cap')
        result=tuple(tuple((result[i][j]+coefficient*int(i==j))%11 for j in range(n)) for i in range(n))
    return result

def exact_order(value,order):
    require(type(order) is int and order in (33,55), 'exact33 or55')
    identity=one(len(value))
    require(repeated_power(value,order)==identity, 'annihilating power')
    divisors=(3,11) if order==33 else (5,11)
    witnesses=[]
    for prime in divisors:
        exponent=order//prime
        value_at_exponent=repeated_power(value,exponent)
        require(value_at_exponent!=identity, 'proper prime-divisor power nonidentity')
        witnesses.append(dict(prime=prime,exponent=exponent,value=value_at_exponent))
    return witnesses

def identity_certificate(export,record):
    require(export.get('schema')=='F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1', 'original export schema')
    job=export['original_job']
    require(type(job) is list and len(job)==2 and type(job[0]) is int and job[0] in EXPECTED
        and type(job[1]) is int and job[1]==4, 'fixed original job')
    require(export.get('original_prefix_index')==job[0] and export.get('field')==11
        and export.get('dimension')==7 and export.get('convention')=='RIGHT_ROW'
        and export.get('matrix_roles')==['a','e','b'] and export.get('selected_labels')==[1,4,2], 'literal matrix roles')
    require(export.get('external_premises',{}).get('original_A_equals_G') is True, 'explicit imported original model')
    require(record.get('original_job')==job and record.get('polynomial_membership_verified') is True
        and record.get('outcome')=='POLYNOMIAL_IDENTITY_VERIFIED', 'positive carrier association')
    require(type(export.get('matrices')) is list and len(export['matrices'])==3, 'three original matrices')
    a,e,b=[matrix(value,7) for value in export['matrices']]
    identity=one(7)
    require(all(x!=identity and product(x,x)==identity for x in (a,e,b)), 'nonidentity prefix involutions')
    require(product(a,e)==product(e,a) and product(b,e)==product(e,b), 'distant commutations')
    r=product(a,b)
    coefficients=record['coefficients']
    require(type(coefficients) is list and len(coefficients)==7, 'seven original coefficients')
    require(horner(r,coefficients)==e, 'independent full49-entry Horner equality')
    order=record['recorded_and_checked_ab_order']
    expected_order=33 if job[0] in (168,170) else 55
    require(type(order) is int and order==expected_order, 'fixed recorded order')
    witnesses=exact_order(r,order)
    return dict(original_job=job,coefficients=coefficients,exact_ab_order=order,
        proper_prime_divisor_witnesses=witnesses,full49_entry_Horner_equality=True,
        disposition='NO_TARGET_G_STRING_C_GROUP_DISJUNCTION_ONLY',
        classification='NONGENERATION_OR_INTERSECTION_PROPERTY_FAILURE_UNSEPARATED')

def rejected(call,label,labels):
    try:
        call()
    except (ValueError,TypeError,KeyError,IndexError):
        labels.append(label)
        return
    raise ValueError('malformed fixture accepted: '+label)

def signature(value):
    return (value.st_dev,value.st_ino,value.st_mode,value.st_nlink,value.st_size,value.st_mtime_ns,value.st_ctime_ns)

def controls():
    labels=[]
    r=matrix([[1,1],[0,1]],2)
    require(horner(r,[3,2])==((5,2),(0,5)), 'literal Jordan Horner');labels.append('Jordan_Horner')
    require(horner(matrix([[1,0],[0,2]],2),[1,3,2])==((6,0),(0,4)), 'literal diagonal Horner');labels.append('diagonal_Horner')
    require(horner(r,[0])==((0,0),(0,0)), 'zero polynomial');labels.append('zero_polynomial')
    require(horner(r,[10])==((10,0),(0,10)), 'constant polynomial');labels.append('constant_polynomial')
    require(horner(r,[3,1])!=((5,2),(0,5)), 'wrong coefficient inequality');labels.append('wrong_coefficient_not_identity')
    require(repeated_power(r,0)==one(2) and repeated_power(r,1)==r, 'literal repeated-power bounds');labels.append('powers_zero_and_one')
    require(repeated_power(r,11)==one(2), 'literal unipotent order11');labels.append('unipotent_eleven')
    r33=matrix([[int(j==((i+1)%3 if i<3 else i))+int(i==3 and j==4) for j in range(7)] for i in range(7)],7)
    r55=matrix([[(3*int(i==j)+3*int(i==0 and j==1))%11 if i<2 and j<2 else int(i==j) for j in range(7)] for i in range(7)],7)
    exact_order(r33,33);labels.append('independent_repeated_exact33')
    exact_order(r55,55);labels.append('independent_repeated_exact55')
    rejected(lambda:exact_order(r33,55),'wrong_annihilator',labels)
    rejected(lambda:exact_order(one(7),33),'proper_prime_divisor_refusal',labels)
    rejected(lambda:exact_order(r55,True),'Boolean_order',labels)
    rejected(lambda:repeated_power(r,-1),'negative_exponent',labels)
    rejected(lambda:repeated_power(r,56),'exponent56',labels)
    rejected(lambda:repeated_power(r,True),'Boolean_exponent',labels)
    rejected(lambda:horner(r,[]),'empty_coefficients',labels)
    rejected(lambda:horner(r,[0]*8),'eight_coefficients',labels)
    rejected(lambda:horner(r,[True]),'Boolean_coefficient',labels)
    rejected(lambda:horner(r,[11]),'coefficient11',labels)
    rejected(lambda:matrix([[True]],1),'Boolean_matrix',labels)
    rejected(lambda:matrix([[11]],1),'matrix_entry11',labels)
    rejected(lambda:matrix([[1,0]],2),'matrix_shape',labels)
    rejected(lambda:parse(b'{"x":1,"x":2}'),'duplicate_JSON_key',labels)
    rejected(lambda:parse(b'{"x":NaN}'),'nonfinite_JSON',labels)
    return labels

class Inputs:
    def __init__(self):
        self.base=Path(__file__).resolve().parent
        self.bytes=Path(__file__).stat().st_size
        self.files={}
        self.signatures={}
    def read(self,name,ref=None):
        require(type(name) is str and 0<len(name)<=128 and name not in ('.','..')
            and '/' not in name and '\\' not in name and not name.startswith('.'), 'flat local input name')
        path=self.base/name
        require(path.resolve(strict=True)==path, 'local input without aliases')
        s=path.lstat()
        require(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and 0<s.st_size<=2**20, 'regular one-MiB local file')
        if ref is not None:
            require(type(ref) is dict and set(ref)=={'path','bytes','sha256'}
                and ref['path']==name and type(ref['bytes']) is int and ref['bytes']==s.st_size
                and type(ref['sha256']) is str and len(ref['sha256'])==64
                and set(ref['sha256'])<=set('0123456789abcdef'), 'exact local descriptor')
        require(self.bytes+s.st_size+1<=8*2**20, 'eight-MiB cumulative read cap')
        with path.open('rb') as stream:
            require(signature(os.fstat(stream.fileno()))==signature(s), 'same opened local input')
            raw=stream.read(s.st_size+1)
            require(signature(os.fstat(stream.fileno()))==signature(s), 'same final opened local input')
        self.bytes+=len(raw)
        require(len(raw)==s.st_size and signature(path.lstat())==signature(s), 'whole stable local input')
        actual=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        require(ref is None or actual==ref, 'whole local SHA256')
        require(self.files.get(name,actual)==actual and self.signatures.get(name,signature(s))==signature(s), 'one immutable local edition')
        self.files[name]=actual;self.signatures[name]=signature(s)
        require(len(self.files)+1<=96, '96 paths including package directory')
        budget()
        return raw
    def obj(self,name,ref=None):
        return parse(self.read(name,ref))
    def close(self):
        for name,ref in list(self.files.items()):
            self.read(name,ref)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--controls',action='store_true')
    mode.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    inputs=Inputs()
    manifest=inputs.obj('manifest.json')
    require(manifest.get('schema')=='PORTABLE_POLYNOMIAL_TEN_MANIFEST_V1'
        and manifest.get('jobs')==EXPECTED, 'exact ten-job manifest')
    own=manifest['Source']
    require(own['path']==Path(__file__).name=='verify.py', 'actual local Source')
    inputs.read('verify.py',own)
    prefix=inputs.obj('prefixes.json',manifest['prefixes'])
    carriers=inputs.obj('certificates.json',manifest['certificates'])
    require(prefix.get('schema')=='PORTABLE_POLYNOMIAL_TEN_ORIGINAL_PREFIX_EXPORTS_V1'
        and prefix.get('field')==11 and prefix.get('dimension')==7
        and prefix.get('convention')=='RIGHT_ROW', 'prefix data schema')
    require(carriers.get('schema')=='PORTABLE_POLYNOMIAL_TEN_COEFFICIENT_CERTIFICATES_V1'
        and carriers.get('classification')=='NONGENERATION_OR_INTERSECTION_PROPERTY_FAILURE_UNSEPARATED', 'coefficient data schema')
    exports=prefix['records'];records=carriers['records']
    require(type(exports) is list and type(records) is list and len(exports)==len(records)==10
        and [r.get('original_job') for r in exports]==[[j,4]for j in EXPECTED]
        and [r.get('original_job') for r in records]==[[j,4]for j in EXPECTED], 'ordered original prefixes and carriers')
    if args.controls:
        labels=controls()
        proof=[]
        result=dict(status='PASS',mode='controls',checks=len(labels),labels=labels)
    else:
        proof=[identity_certificate(export,record)for export,record in zip(exports,records)]
        result=dict(status='PASS',mode='replay',prefixes=10,verified_jobs=[[j,4]for j in EXPECTED])
    inputs.close()
    result.update(matrix_products=PRODUCTS,separate_diagonal_additions=DIAGONAL_ADDITIONS,
        read_bytes=inputs.bytes,paths=len(inputs.files)+1,Source=own,certificates=proof,
        disposition='NO_TARGET_G_STRING_C_GROUP_DISJUNCTION_ONLY',
        classification='NONGENERATION_OR_INTERSECTION_PROPERTY_FAILURE_UNSEPARATED',
        imported_model_original_frame_membership_and_complete_maximal_cover=True,
        whole_original_conjecture_Lean_or_compression_credit=0)
    raw=canonical(result)+b'\n'
    require(len(raw)<=128*2**10, '128-KiB stdout cap')
    sys.stdout.buffer.write(raw)

if __name__=='__main__':
    main()
