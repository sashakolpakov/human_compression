#!/usr/bin/env python3
"""Exact integer-action certificate. Standard library only; no group oracle."""
from pathlib import Path
import argparse,hashlib,json

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,default=Path(__file__).with_name('phase32_L003_voltage.json'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to replace an existing output file; choose a fresh path.')
    data=json.loads(args.data.read_text())
    n=data['degree']
    assert n==216
    permutations=[[j-1 for j in p] for p in data['permutations']]
    weights=data['weights']
    assert len(permutations)==len(weights)==3
    assert all(sorted(p)==list(range(n)) for p in permutations)
    assert all(len(w)==n and all(type(a) is int and a in (-1,0,1) for a in w) for w in weights)
    inverses=[[p.index(i) for i in range(n)] for p in permutations]
    def inverse(w):return tuple(-a for a in reversed(w))
    def power(w,k):return (w if k>=0 else inverse(w))*abs(k)
    x,y,z=(1,),(2,),(3,)
    # Direct transcription of the displayed p=6 source presentation:
    relators=[('x6',power(x,6)),('y3',power(y,3)),('z2',power(z,2)),
       ('(zx)3',power(z+x,3)),('(zy)6',power(z+y,6)),
       ('(x^-1 y)2',power(inverse(x)+y,2)),
       ('(y^-1 x^-2)3',power(inverse(y)+power(x,-2),3)),
       ('(z x3)2',power(z+power(x,3),2)),
       ('(x^-1 z (y^-1 z)2)(z x (zy)2)',
          inverse(x)+z+power(inverse(y)+z,2)+z+x+power(z+y,2)),
       ('(y (zy)2)6',power(y+power(z+y,2),6))]
    def act(word,state):
        height=0
        for letter in word:
            g=abs(letter)-1
            assert 0<=g<3
            if letter>0:
                height+=weights[g][state]
                state=permutations[g][state]
            else:
                state=inverses[g][state]
                height-=weights[g][state]
        return state,height
    results=[]
    for name,word in relators:
        assert all(act(word,i)==(i,0) for i in range(n)),name
        results.append(dict(name=name,word=list(word),states_checked=n))
    witness=power(x+y+x+z,2)
    shifts=[act(witness,i) for i in range(n)]
    assert all(state==i for i,(state,_) in enumerate(shifts))
    assert shifts[0]==(0,-1)
    assert all(act(witness*k,0)==(0,-k) for k in [1,2,3,7,23])
    local_word=y+power(z+y,2)
    assert all(act(power(local_word,6),i)==(i,0) for i in range(n))
    exact_order=next(k for k in range(1,7) if all(act(power(local_word,k),i)==(i,0) for i in range(n)))
    assert exact_order==6
    report=dict(result='PASS',degree=n,generators=3,relators=results,
       relator_state_checks=n*len(relators),
       witness_word=list(witness),witness_is_pure_translation=True,
       witness_translation_at_state_1=-1,
       witness_translation_vector=[h for _,h in shifts],
       last_parameter_word_exact_order=exact_order,
       theorem_scope='The displayed rotational presentation at s=6 has an infinite image; so does each presentation with positive s divisible by 6. No geometry or finite-quotient existence assertion.',
       data_sha256=hashlib.sha256(args.data.read_bytes()).hexdigest(),
       checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 2160 relator-state checks; (xyxz)^2 is a nonzero pure integer translation; parameter word has exact order 6.')

if __name__=='__main__':main()
