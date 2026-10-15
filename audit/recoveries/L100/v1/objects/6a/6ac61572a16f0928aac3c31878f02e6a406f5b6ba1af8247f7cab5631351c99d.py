"""Ordered endpoint checks for literal numerical a/g/b diagram labels."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True

def compare_endpoints(source,actual,permutation):
    nodes=source['nodes'];position={n['position']:permutation[i]+1 for i,n in enumerate(nodes)}
    pairs={frozenset(p['types']):p for p in actual['pairs']};checks=[];mismatches=[]
    for edge in source['edges']:
        if '/' not in edge['printed_label']:continue
        left,g,right=map(int,edge['printed_label'].split('/'))
        types=[position[n] for n in edge['nodes']];p=pairs[frozenset(types)]
        expected=[left,right];got=[p['eccentricities'][p['types'].index(t)] for t in types]
        checks.append(dict(nodes=edge['nodes'],catalogue_types=types,expected_endpoints=expected,actual_eccentricities=got))
        for n,e,v in zip(edge['nodes'],expected,got):
            if v!=[e]:mismatches.append(dict(kind='ordered_endpoint_eccentricity',node=n,printed=e,actual=v))
    return checks,mismatches
