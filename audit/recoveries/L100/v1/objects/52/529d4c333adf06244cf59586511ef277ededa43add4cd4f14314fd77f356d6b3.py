"""Check saved group-structure witnesses directly, without restriction lookup."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('names',P/'automorphism_names.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
need=N.need;mul=N.mul;inv=N.inv;read=N.read

def validate(C,index,record,m=None,groups=None):
    m=read(N.D/f'model{index}.json')if m is None else m
    groups=read(N.D/f'groups{index}.json')if groups is None else groups
    need(record['catalogue_index']==index,'literal model index')
    n=m['n']+m['rank'];one=tuple(range(n))
    acts=[tuple(x-1 for x in g)+tuple(range(m['n'],n))for g in m['group_action']]
    need(len(acts)==2,'exact two generators')
    cache={C.identity:one}
    def action(k):
        need(type(k)is int and 0<=k<len(C.A.elements),'element index domain')
        if k not in cache:
            p=one
            for j in C.word(k):p=mul(p,acts[j])
            cache[k]=p
        return cache[k]
    def perm(v):
        q=tuple(v);need(len(q)==n and sorted(q)==list(range(n)),'literal complete permutation');return q
    total=0
    for profile in ['typed','correlations']:
        r=record['profiles'][profile]
        generators=[tuple(x-1 for x in g)for g in groups[profile+'_generators']]
        data=r['generator_decompositions'];need(len(data)==len(generators),'every actual complete-group generator')
        for q,d in zip(generators,data):
            perm(q);e=d['outer'];h=d['inner_element'];need(type(e)is int and 0<=e<12,'outer domain');a=C.auts[e][1]
            hi=inv(C.A.elements[h]);need(len(d['image_elements'])==2,'two literal generator images')
            for g,ga,k in zip(C.A.generators,acts,d['image_elements']):
                need(C.A.elements[k]==mul(mul(hi,a[g]),C.A.elements[h]),'exact coordinate-inner images')
                need(mul(mul(inv(q),ga),q)==action(k),'all-vertex conjugation equality');total+=n
        outer=N.subgroup(C.table,[d['outer']for d in data]);need(outer==r['outer_indices'],'exact generated outer subgroup and traversal')
        need(r['outer_names']==[C.names[e]for e in outer],'literal outer names')
        order=groups[profile+'_order'];need(r['acquired_order']==order,'acquired complete palette order')
        need(r['image_order']==20160*len(outer),'exact conjugation image order')
        kernel=r['kernel_order'];need(kernel in [1,2]and order==kernel*r['image_order'],'exact kernel order')
        if kernel==1:need(r['central_involution']is None,'no invented central factor');z=one
        else:
            z=perm(r['central_involution']);need(z!=one and mul(z,z)==one,'actual nontrivial kernel involution')
            need(all(mul(z,q)==mul(q,z)for q in generators+acts),'central kernel element')
        normalized={};section={}
        need(len(r['section_bits'])==len(outer)and all(b in [0,1]for b in r['section_bits']),'section binary vector')
        need(set(r['lift_words'])==set(r['normalization_elements'])==set(r['section_permutations'])=={str(e)for e in outer},'complete exact section domain')
        for i,e in enumerate(outer):
            q=one
            for j in r['lift_words'][str(e)]:
                need(type(j)is int and 0<=j<len(generators),'actual generator-word letter');q=mul(q,generators[j])
            h=r['normalization_elements'][str(e)];q=mul(q,inv(action(h)));normalized[e]=q
            for g,ga in zip(C.A.generators,acts):
                need(mul(mul(inv(q),ga),q)==action(C.A.index[C.auts[e][1][g]]),'normalized coordinate action')
            s=perm(r['section_permutations'][str(e)]);need(s==(mul(q,z)if r['section_bits'][i]else q),'literal normalized and adjusted lift')
            section[e]=s
        need(section[0]==one,'identity section')
        need(all(mul(section[e],section[f])==section[C.table[e][f]]for e in outer for f in outer),'complete section multiplication')
        # The lifts actually generate the given complete group with G and z.
        for q,d in zip(generators,data):
            error=mul(mul(q,inv(action(d['inner_element']))),inv(section[d['outer']]))
            need(error in [one,z],'original generators lie in asserted split product')
    return total

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir()
    C=N.Context();total=0
    records={i:read(a.results/f'model{i}.json')for i in range(1,30)}
    for i,r in records.items():total+=validate(C,i,r)
    involutions=[]
    for name,aut in C.auts:
        if name not in ['duality','diagonal0_field1','diagonal0_field1_duality']:continue
        involutions.append(dict(name=name,fixed_elements=sum(aut[g]==g for g in C.A.elements),outer_involutions=sum(mul(g,aut[g])==C.one for g in C.A.elements)))
    inner=sum(g!=C.one and mul(g,g)==C.one for g in C.A.elements)
    need(inner==315,'literal inner involutions')
    need({r['name']:r['outer_involutions']for r in involutions}=={'duality':336,'diagonal0_field1':120,'diagonal0_field1_duality':280},'three exact distinguishable outer cosets')
    damages=[];base=records[13]
    def reject(name,edit,model=None,groups=None):
        r=copy.deepcopy(base);edit(r)
        try:validate(C,13,r,model,groups)
        except (ValueError,IndexError,KeyError,TypeError):damages.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    reject('wrong-model',lambda r:r.update(catalogue_index=12))
    reject('wrong-acquired-order',lambda r:r['profiles']['typed'].update(acquired_order=1))
    reject('wrong-kernel',lambda r:r['profiles']['correlations'].update(kernel_order=1))
    reject('wrong-image-order',lambda r:r['profiles']['typed'].update(image_order=1))
    reject('missing-generator',lambda r:r['profiles']['typed']['generator_decompositions'].pop())
    reject('missing-outer',lambda r:r['profiles']['typed']['outer_indices'].pop())
    reject('wrong-outer-name',lambda r:r['profiles']['typed']['outer_names'].__setitem__(0,'field'))
    reject('wrong-inner-image',lambda r:r['profiles']['typed']['generator_decompositions'][0].update(inner_element=(r['profiles']['typed']['generator_decompositions'][0]['inner_element']+1)%20160))
    reject('wrong-literal-image',lambda r:r['profiles']['typed']['generator_decompositions'][0]['image_elements'].__setitem__(0,C.identity))
    reject('identity-central-involution',lambda r:r['profiles']['correlations'].update(central_involution=list(range(len(r['profiles']['correlations']['central_involution'])))))
    reject('bad-central-permutation',lambda r:r['profiles']['correlations']['central_involution'].__setitem__(0,r['profiles']['correlations']['central_involution'][1]))
    e=str(base['profiles']['correlations']['outer_indices'][1])
    reject('missing-section',lambda r:r['profiles']['correlations']['section_permutations'].pop(e))
    reject('wrong-section-identity',lambda r:r['profiles']['correlations']['section_permutations'].__setitem__('0',r['profiles']['correlations']['central_involution']))
    reject('wrong-section-bit',lambda r:r['profiles']['correlations']['section_bits'].__setitem__(0,1-r['profiles']['correlations']['section_bits'][0]))
    reject('bad-lift-letter',lambda r:r['profiles']['correlations']['lift_words'][e].append(999))
    reject('deleted-lift',lambda r:r['profiles']['correlations']['lift_words'].__setitem__(e,[]))
    # A nontrivial inconsistent cocycle must not be declared split.
    need(N.solve_bits([(0,1)],1)is None,'inconsistent binary relation rejects')
    need(N.solve_bits([(1,0),(1,1)],1)is None,'conflicting section bits reject')
    report=dict(status='PASS_LITERAL_AUT_COR_WITNESS_VALIDATION',models=29,groups=58,all_vertex_checks=total,
        inner_involutions=inner,outer_involutions=involutions,damaged_certificates=damages,
        inconsistent_section_controls=2,target_censuses=0,source_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],total,len(damages),flush=True)
if __name__=='__main__':main()
