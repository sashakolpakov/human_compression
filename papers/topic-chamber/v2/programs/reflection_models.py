#!/usr/bin/env python3
"""Finite diagnostics of the actual two-copy formula, not its general proof."""
from itertools import permutations
import json

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def check_model(name, elements, mul, inv, one, marks, theta):
    chambers = [(g, side) for g in elements for side in (False, True)]
    def neighbor(a, x):
        g, side = x
        return (mul(g, a if side else inv(a)), not side)
    def reflect(x):
        return (theta(x[0]), not x[1])
    def translate(g, x):
        return (mul(g, x[0]), x[1])
    require(all(theta(mul(g,h)) == mul(theta(g),theta(h))
                for g in elements for h in elements), name + ' automorphism')
    require(len({theta(g) for g in elements}) == len(elements), name + ' bijective')
    require(all(theta(a) == inv(a) for a in marks), name + ' marking')
    counts = {'neighbor_involution': 0, 'reflection_involution': 0,
              'color_preservation': 0, 'conjugation': 0}
    for x in chambers:
        require(reflect(reflect(x)) == x, name + ' reflection involution')
        counts['reflection_involution'] += 1
        for a in marks:
            require(neighbor(a,neighbor(a,x)) == x, name + ' neighbor involution')
            require(reflect(neighbor(a,x)) == neighbor(a,reflect(x)), name + ' color')
            counts['neighbor_involution'] += 1
            counts['color_preservation'] += 1
        for g in elements:
            require(reflect(translate(g,x)) == translate(theta(g),reflect(x)), name + ' conjugation')
            counts['conjugation'] += 1
    return {'name':name,'order':len(elements),'checks':counts}

def main():
    reports=[]
    for n in (3,5,7):
        reports.append(check_model('cyclic_'+str(n),list(range(n)),
            lambda a,b,n=n:(a+b)%n,lambda a,n=n:(-a)%n,
            0,[0,1,2],lambda a,n=n:(-a)%n))
    elements=list(permutations(range(3)))
    def mul(a,b): return tuple(a[b[i]] for i in range(3))
    def inv(a): return tuple(a.index(i) for i in range(3))
    one=(0,1,2);a=(1,2,0);b=(1,0,2)
    reports.append(check_model('symmetric_3',elements,mul,inv,one,[one,a,b],
                               lambda g:mul(mul(b,g),b)))
    controls=[]
    def cyc_neighbor(n,a,x):
        g,side=x
        return ((g+(a if side else -a))%n,not side)
    def cyc_reflect(n,multiplier,x,swap=True):
        return ((multiplier*x[0])%n,not x[1] if swap else x[1])
    # Identity is an automorphism of C5 but does not invert its generator.
    x=(0,False)
    left=cyc_reflect(5,1,cyc_neighbor(5,1,x))
    right=cyc_neighbor(5,1,cyc_reflect(5,1,x))
    controls.append({'removed':'inversion_on_marks','modulus':5,
                     'left':left,'right':right,'detected':left!=right})
    # Inversion without the copy swap does not commute with color 1.
    left=cyc_reflect(5,-1,cyc_neighbor(5,1,x),swap=False)
    right=cyc_neighbor(5,1,cyc_reflect(5,-1,x,swap=False))
    controls.append({'removed':'swap_of_chamber_copies','modulus':5,
                     'left':left,'right':right,'detected':left!=right})
    # The mark 0 does not generate C7. Multiplication by 2 inverts that
    # mark but its square is not the identity automorphism.
    left=cyc_reflect(7,2,cyc_reflect(7,2,(1,False)))
    right=(1,False)
    controls.append({'removed':'generation','modulus':7,'marks':[0],
                     'automorphism_multiplier':2,'left':left,'right':right,
                     'detected':left!=right})
    require(all(c['detected'] for c in controls),'a hypothesis control failed')
    print(json.dumps({'status':'PASS','models':reports,'controls':controls},indent=2))

if __name__=='__main__':
    main()
