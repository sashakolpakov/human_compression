"""A reachable ordered-pair certificate for a proposed involution centralizer.

Named ATLAS model, unique involution class and centralizer order are borrowed
premises. A returned tree proves only its stated finite orbit lower bound.
"""
import argparse
from array import array
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import struct
import sys
import time

D = Path(__file__).resolve().parent
SOURCE = D/'check_standard_pair.py'
SOURCE_SHA = 'acc28b910d81fe4c67b065f8da76cec5e62683d24a50729d70dab98b1546065c'
GOAL = 161280
RECORD = struct.Struct('<IB')
ROOT_PARENT, ROOT_LABEL = 2**32-1, 255
START = time.monotonic()


def need(ok, why):
    if not ok:
        raise ValueError(why)


def budget():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak = peak if sys.platform == 'darwin' else peak*1024
    if time.monotonic()-START >= 30 or peak >= 128*2**20:
        raise RuntimeError('pair-orbit certificate30s/128MiB budget')


def helper():
    need(SOURCE.is_file() and not SOURCE.is_symlink() and SOURCE.stat().st_size == 7808,
         'fixed ordinary literal permutation Source')
    need(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA,
         'whole unchanged literal permutation Source')
    spec = importlib.util.spec_from_file_location('retained_literal_permutations', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(seed, n, goal):
    need(type(n) is int and 1 <= n <= 245520 and type(goal) is int and 1 <= goal <= GOAL,
         'bounded pair degree and requested lower bound')
    need(type(seed) in (tuple,list) and len(seed) == 2
         and all(type(x) is int and 0 <= x < n for x in seed) and seed[0] != seed[1],
         'two distinct explicit full-degree points')


def produce(gens, seed, n, goal, tick=budget):
    validate(seed,n,goal)
    need(len(gens)==2 and all(len(g)==n for g in gens),'two full-degree generators')
    first,second = array('I',[seed[0]]),array('I',[seed[1]])
    seen = {seed[0]*n+seed[1]}
    raw = bytearray(RECORD.pack(ROOT_PARENT,ROOT_LABEL))
    index = 0
    while len(first) < goal and index < len(first):
        if index % 128 == 0:
            tick()
        for label,g in enumerate(gens):
            a,b = g[first[index]],g[second[index]]
            key = a*n+b
            if key not in seen:
                seen.add(key)
                first.append(a);second.append(b)
                raw.extend(RECORD.pack(index,label))
                if len(first)==goal:
                    break
        index += 1
    tick()
    return bytes(raw),len(first)==goal,len(first)


def verify(raw, gens, seed, n, goal, tick=budget):
    validate(seed,n,goal)
    need(len(gens)==2 and all(len(g)==n for g in gens),'same two full-degree generators')
    need(len(raw)==goal*RECORD.size,'whole exact requested tree')
    need(RECORD.unpack_from(raw,0)==(ROOT_PARENT,ROOT_LABEL),'unique specified root record')
    first,second=array('I',[seed[0]]),array('I',[seed[1]])
    seen={seed[0]*n+seed[1]}
    for i in range(1,goal):
        if i % 128 == 0:
            tick()
        parent,label=RECORD.unpack_from(raw,i*RECORD.size)
        need(parent < i and label < 2,'earlier parent and one of the exact two marks')
        g=gens[label];a,b=g[first[parent]],g[second[parent]]
        key=a*n+b
        need(key not in seen,'all reached ordered pairs distinct')
        seen.add(key);first.append(a);second.append(b)
    tick()
    return goal-1


def controls(m):
    x=m.parse('x := (1,2);',3)
    z=m.parse('z := (1,2,3);',3)
    gs=[x,z];seed=(0,1)
    raw,complete,count=produce(gs,seed,3,6)
    need(complete and count==6 and verify(raw,gs,seed,3,6)==5,
         'six distinct ordered pairs of three points')
    results=[dict(name='complete_S3_pair_tree',status='PASS')]
    def refuses(name,action,kind=ValueError):
        try:
            action()
        except kind:
            results.append(dict(name=name,status='PASS'))
        else:
            raise ValueError('missing intended refusal: '+name)
    refuses('root_parent',lambda:verify(RECORD.pack(0,255)+raw[5:],gs,seed,3,6))
    refuses('root_label',lambda:verify(RECORD.pack(ROOT_PARENT,0)+raw[5:],gs,seed,3,6))
    refuses('future_parent',lambda:verify(raw[:5]+RECORD.pack(1,0)+raw[10:],gs,seed,3,6))
    refuses('wrong_generator_label',lambda:verify(raw[:5]+RECORD.pack(0,2)+raw[10:],gs,seed,3,6))
    refuses('duplicate_reached_pair',lambda:verify(raw[:10]+raw[5:10]+raw[15:],gs,seed,3,6))
    refuses('truncated_tree',lambda:verify(raw[:-1],gs,seed,3,6))
    short,complete,count=produce(gs,seed,3,7)
    need(not complete and count==6 and len(short)==30,'short exhausted orbit remains unpaid')
    results.append(dict(name='short_orbit_unpaid',status='PASS'))
    refuses('coincident_seed_points',lambda:produce(gs,(0,0),3,6))
    refuses('outside_seed_point',lambda:produce(gs,(0,3),3,6))
    refuses('excessive_requested_size',lambda:produce(gs,seed,3,GOAL+1))
    def stopped():
        raise RuntimeError('synthetic resource interruption')
    refuses('producer_interruption',lambda:produce(gs,seed,3,6,stopped),RuntimeError)
    refuses('verifier_interruption',lambda:verify(raw,gs,seed,3,6,stopped),RuntimeError)
    return dict(status='PASS_FOCUSED_CENTRALIZER_PAIR_ORBIT_CONTROLS',controls=results,
                count=len(results),production_inputs_opened=False,scientific_credit=0)


def model(m):
    pins,gs=[],[]
    for path,expected in m.FILES:
        ref,raw=m.pin(path)
        need(ref['sha256']==expected,'exact retained ATLAS model')
        pins.append(ref);gs.append(m.parse(raw.decode('ascii'),m.N))
    c,d=gs
    need(m.exact_order(c,2,[2]) and m.exact_order(d,4,[2])
         and m.exact_order(m.mul(c,d),22,[2,11]),'retained outer standard orders')
    d2=m.power(d,2);w=m.power(m.mul(c,d2),2)
    a,b=m.mul(m.mul(m.inv(w),d2),w),d
    for text,order,primes in [('a',2,[2]),('b',4,[2]),('ab',11,[11]),
                              ('abb',19,[19]),('abababbabb',31,[31])]:
        need(m.exact_order(m.word(text,a,b),order,primes),'same inner standard pair')
    z=m.word('ababb',a,b)
    need(m.exact_order(z,20,[2,5]),'exact order20 centralizer word')
    t=m.power(z,10)
    comm=m.mul(m.mul(m.mul(m.inv(t),m.inv(b)),t),b)
    x=m.power(comm,14)
    need(m.exact_order(t,2,[2]),'nontrivial involution')
    need(m.mul(x,t)==m.mul(t,x) and m.mul(z,t)==m.mul(t,z),
         'both actual words centralize the same involution')
    return [x,z],pins


def put(path,raw):
    need(len(raw)<=1024**2,'bounded fresh whole output')
    with path.open('xb') as f:
        need(f.write(raw)==len(raw),'whole output');f.flush();os.fsync(f.fileno())
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--mode',choices=['controls','produce','check'],required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seed',nargs=2,type=int)
    ap.add_argument('--certificate',type=Path)
    ap.add_argument('--certificate-sha256')
    args=ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
         'ordinary assert-enabled -E -B')
    out=args.out
    need(out.is_absolute() and out.parent.resolve(strict=True)==out.parent and not out.exists(),
         'fresh ordinary declared output directory')
    m=helper()
    if args.mode=='controls':
        need(args.seed is None and args.certificate is None and args.certificate_sha256 is None,
             'controls do not take production inputs')
        report=controls(m)
        out.mkdir()
    else:
        validate(args.seed,m.N,GOAL)
        if args.mode=='check':
            need(args.certificate is not None and args.certificate_sha256 is not None,
                 'explicit real certificate and digest')
            cert,raw=m.pin(args.certificate)
            need(cert['sha256']==args.certificate_sha256 and cert['bytes']==GOAL*RECORD.size,
                 'whole received certificate before arithmetic')
        else:
            need(args.certificate is None and args.certificate_sha256 is None,'producer has no input tree')
        gs,pins=model(m)
        out.mkdir()
        if args.mode=='produce':
            raw,complete,count=produce(gs,args.seed,m.N,GOAL)
            if complete:
                edges=verify(raw,gs,args.seed,m.N,GOAL)
                cert=put(out/'pairs.bin',raw)
            else:
                cert=None;edges=0
            report=dict(status='COMPLETE_REACHABLE_CENTRALIZER_PAIR_TREE' if complete else 'SHORT_PAIR_ORBIT_UNPAID',
                        complete=complete,reached_pairs=count,verified_edges=edges,certificate=cert)
        else:
            edges=verify(raw,gs,args.seed,m.N,GOAL)
            need(m.pin(args.certificate)[0]==cert,'unchanged complete tree after verification')
            report=dict(status='VERIFIED_REACHABLE_CENTRALIZER_PAIR_TREE',complete=True,
                        reached_pairs=GOAL,verified_edges=edges,certificate=cert)
        for ref in pins:
            need(m.pin(ref['path'])[0]==ref,'unchanged entire retained model')
        report.update(degree=m.N,seed=args.seed,model_inputs=pins,requested_lower_bound=GOAL,
                      same_involution_centralized=True,generators=['[(ababb)^10,b]^14','ababb'],
                      named_model_reproved=False,centralizer_upper_bound_borrowed=161280,
                      census_credit=0,whole_original_credit=0)
    budget()
    report.update(program=m.pin(Path(__file__).resolve())[0],helper=m.pin(SOURCE)[0],
                  seconds=time.monotonic()-START,whole_original_credit=0)
    ref=put(out/'result.json',(json.dumps(report,sort_keys=True,indent=2)+'\n').encode())
    print(json.dumps(dict(status=report['status'],result=ref)))


if __name__=='__main__':
    main()
