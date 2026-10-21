"""Literal permutation checks for the cached ATLAS outer-generator model.

No group enumeration, matrix identification, or census computation.
"""
import argparse
from array import array
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import stat
import sys
import time

START = time.monotonic()
S = Path('/Users/sasha/medusa/research/leemans')
N = 245520
FILES = [
    (S/'corpus161_N006_sporadic/private_data/ONd2G1-p245520B0.g1',
     '6f6c19692a8916ea66890461ce3fc12427b01baa23b0eaaf6a77da99cd2eb3a7'),
    (S/'corpus161_N006_sporadic/private_data/ONd2G1-p245520B0.g2',
     '0c50acddb7cd7dd0e78b36bf0317e2d71074a715d3699108b18704d987867d22')]


def need(ok, message):
    if not ok:
        raise ValueError(message)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak = peak if sys.platform == 'darwin' else peak*1024
    if time.monotonic()-START >= 30 or peak >= 128*2**20:
        raise RuntimeError('literal permutation30s/128MiB bound')


def parse(text, n):
    need(type(n) is int and 1 <= n <= N, 'bounded positive degree')
    match = re.fullmatch(r'\s*[A-Za-z][A-Za-z0-9_]*\s*:=\s*((?:\([\d,\s]+\)\s*)+);\s*', text)
    need(match is not None, 'whole literal cycle assignment')
    out = array('I', range(n))
    seen = bytearray(n)
    for cycle in re.finditer(r'\(([^()]*)\)', match.group(1)):
        values = [int(x)-1 for x in cycle.group(1).split(',')]
        need(len(values) >= 2, 'nontrivial cycle')
        for value in values:
            need(0 <= value < n and not seen[value], 'distinct in-range cycle entries')
            seen[value] = 1
        for i, value in enumerate(values):
            out[value] = values[(i+1) % len(values)]
    return out


def identity(n):
    return array('I', range(n))


def mul(a, b):
    need(len(a) == len(b), 'same permutation degree')
    return array('I', (b[x] for x in a))


def inv(a):
    out = identity(len(a))
    for i, value in enumerate(a):
        out[value] = i
    return out


def power(a, n):
    need(type(n) is int and n >= 0, 'nonnegative literal exponent')
    out = identity(len(a))
    while n:
        if n & 1:
            out = mul(out, a)
        n //= 2
        if n:
            a = mul(a, a)
    return out


def exact_order(a, order, prime_divisors):
    need(type(order) is int and order > 1 and prime_divisors,
         'declared positive order and complete prime divisors')
    e = identity(len(a))
    return power(a, order) == e and all(power(a, order//p) != e for p in prime_divisors)


def word(text, a, b):
    need(type(text) is str and 1 <= len(text) <= 32 and set(text) <= {'a','b'},
         'bounded positive standard word')
    out = identity(len(a))
    for letter in text:
        out = mul(out, a if letter == 'a' else b)
    return out


def pin(path):
    path = Path(path)
    before = path.lstat()
    signature = lambda s: (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    need(path.resolve(strict=True) == path and stat.S_ISREG(before.st_mode)
         and before.st_nlink == 1 and before.st_size <= 2*2**20,
         'ordinary bounded exact input')
    with path.open('rb') as stream:
        need(signature(before)==signature(os.fstat(stream.fileno())),
             'same ordinary input descriptor')
        raw = stream.read(before.st_size+1)
    need(len(raw)==before.st_size and signature(before)==signature(path.lstat()),
         'stable whole input identity')
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), raw


def controls():
    a = parse('a := (1,2)(3,4);', 4)
    b = parse('b := (1,2,3,4);', 4)
    checks = []
    def yes(name, ok):
        need(ok, name)
        checks.append(dict(name=name,status='PASS'))
    yes('literal_right_images', list(a)==[1,0,3,2] and list(b)==[1,2,3,0])
    yes('composition_right_action', list(mul(a,b))==[2,1,0,3])
    yes('inverse_both_sides', mul(b,inv(b))==identity(4)==mul(inv(b),b))
    yes('zero_and_positive_powers',power(b,0)==identity(4) and list(power(b,2))==[2,3,0,1] and power(b,4)==identity(4))
    yes('exact_not_merely_dividing_order',exact_order(b,4,[2]) and not exact_order(a,4,[2]))
    for name,text in [('overlapping_cycles','x := (1,2)(2,3);'),
                      ('repeated_cycle_entry','x := (1,2,1);'),
                      ('out_of_range','x := (1,5);'),
                      ('trailing_program','x := (1,2); Quit();')]:
        try:
            parse(text,4)
        except ValueError:
            checks.append(dict(name=name,status='PASS'))
        else:
            raise ValueError('missing intended refusal: '+name)
    return dict(status='PASS_FOCUSED_LITERAL_PERMUTATION_CONTROLS',controls=checks,
                count=len(checks),production_inputs_opened=False)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--mode',choices=['controls','check'],required=True)
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
         'ordinary assert-enabled -E -B')
    need(args.output.is_absolute() and args.output.parent.resolve(strict=True)==args.output.parent
         and not args.output.exists(),'fresh ordinary output')
    if args.mode == 'controls':
        report = controls()
    else:
        pins, gs = [], []
        for path, expected in FILES:
            ref, raw = pin(path)
            need(ref['sha256']==expected,'exact cached ATLAS model')
            pins.append(ref)
            gs.append(parse(raw.decode('ascii'),N))
        c, d = gs
        need(exact_order(c,2,[2]) and exact_order(d,4,[2])
             and exact_order(mul(c,d),22,[2,11]),'cached outer standard orders')
        d2 = power(d,2)
        w = power(mul(c,d2),2)
        a, b = mul(mul(inv(w),d2),w), d
        specifications=[('a',2,[2]),('b',4,[2]),('ab',11,[11]),
                        ('abb',19,[19]),('abababbabb',31,[31])]
        checks=[]
        for text,order,primes in specifications:
            need(exact_order(word(text,a,b),order,primes),'exact standard word order: '+text)
            checks.append(dict(word=text,exact_order=order,prime_divisors=primes))
        for ref in pins:
            need(pin(ref['path'])[0]==ref,'unchanged input after literal arithmetic')
        report=dict(status='VERIFIED_CACHED_ON_STANDARD_PAIR_WORD_ORDERS',degree=N,
            inputs=pins,convention='RIGHT_ACTION',standard_transport='w=(c*d^2)^2;a=w^-1*d^2*w;b=d',
            transport_source='https://brauer.maths.qmul.ac.uk/Atlas/v3/subgroup/ONd2G1-max1W1',
            outer_orders=[2,4,22],checks=checks,group_enumeration=False,
            named_group_identification_reproved=False,cover_matrix_homomorphism_proved=False,
            census_credit=0,whole_original_credit=0,
            qualification='Exact literal permutation word facts only. Named Aut(ON), its inner kernel, and maximal-subgroup classification are attributed external premises. These checks alone prove no isomorphism to the45D matrix group and no census.')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak = peak if sys.platform=='darwin' else peak*1024
    report.update(seconds=time.monotonic()-START,self_peak_bytes=peak,
                  self_limits=dict(seconds=30,rss_bytes=128*2**20))
    raw=(json.dumps(report,sort_keys=True,indent=2)+'\n').encode()
    need(len(raw)<=64*1024,'bounded whole verdict')
    with args.output.open('xb') as f:
        need(f.write(raw)==len(raw),'whole fresh output')
    print(json.dumps(dict(status=report['status'],output=dict(path=str(args.output),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))))


if __name__ == '__main__':
    main()
