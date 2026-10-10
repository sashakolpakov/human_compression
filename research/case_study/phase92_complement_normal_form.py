#!/usr/bin/env python3
"""Exact bidirectional normal form for the marked universal complement group.

No GAP or imported author algebra code is used. The fixed trace is replayed;
all original relations are checked in the explicit free-product normal form.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
INPUTS={
 'phase66_coprime_cover_permutation_model.json':'0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338',
 'phase83_word_elimination.json':'d6cdcab4ea0bfd9a9a75255d5a1da0a1a589306c803d330b0a7a7b659ab86c17',
}
FREE_SOURCE=[1,2,4,5,6,8,9,10,12,14,16,19,21,25,32]
SURVIVORS=sorted(FREE_SOURCE+[3,7])
X,Y=16,17

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def inv(word):return [-x for x in word[::-1]]

def free(word):
    result=[]
    for x in word:
        require(type(x) is int and x!=0,'Invalid free letter')
        if result and result[-1]==-x:result.pop()
        else:result.append(x)
    return result

def replace(word,x,image):
    result=[]
    for y in word:result.extend(image if y==x else inv(image) if y==-x else [y])
    return free(result)

def evaluate(word,images,reducer=free):
    result=[]
    for x in word:
        image=images[abs(x)]
        result.extend(image if x>0 else inv(image))
    return reducer(result)

def normal(word):
    """F15 * V4: free letters +/-1..15; V4 syllables 16=X,17=Y,18=XY."""
    result=[]
    for x in word:
        require(type(x) is int and 1<=abs(x)<=18,'Invalid normal-form letter')
        if abs(x)<=15:
            if result and result[-1]==-x:result.pop()
            else:result.append(x)
        else:
            bits=abs(x)-15
            if result and result[-1]>=16:bits^=result.pop()-15
            if bits:result.append(bits+15)
    return result

def basis_images():
    forward={s:[i+1] for i,s in enumerate(FREE_SOURCE)}
    forward[7]=forward[6]+[X]
    forward[3]=forward[1]+[Y]+inv(forward[6])+forward[12]
    backward={i+1:[s] for i,s in enumerate(FREE_SOURCE)}
    backward[X]=[-6,7]
    backward[Y]=[-1,3,-12,6]
    return forward,backward

def group_closure(gens):
    identity=tuple(range(1,129)); pending=[identity]; seen={identity}
    for a in pending:
        for b in gens:
            c=tuple(b[i-1] for i in a)
            if c not in seen:seen.add(c);pending.append(c)
    return pending

def cyclic(word):
    word=free(word);prefix=[]
    while len(word)>1 and word[0]==-word[-1]:prefix.append(word.pop(0));word.pop()
    return prefix,word

def parity(word):
    v=0
    for x in word:
        a=abs(x)
        if a<=17:v^=1<<(a-1)
        else:v^=(1<<15)|(1<<16)
    return v

def linear(v,columns):
    result=0
    while v:
        bit=v&-v;result^=columns[bit.bit_length()-1];v^=bit
    return result

def binary_span(values):
    pivots={}
    for value in values:
        while value:
            p=value.bit_length()-1
            if p in pivots:value^=pivots[p]
            else:pivots[p]=value;break
    return [pivots[p] for p in sorted(pivots,reverse=True)]

def replay(model,trace):
    gens=[tuple(g) for g in model['generators']]
    require(model['degree']==128 and len(gens)==4,'Model dimensions')
    require(all(sorted(g)==list(range(1,129)) for g in gens),'Invalid permutation')
    group=group_closure(gens)
    medial=group_closure(gens[1:3])
    require(len(group)==1024 and len(medial)==8,'Group orders')
    require({g for g in group if g[0]==1}==set(medial),'Wrong coset stabilizer')
    require(len({g[0] for g in group})==128,'Nontransitive model')
    point=1
    for letter in model['z_word_1based']:point=gens[letter-1][point-1]
    require(point==40,'Wrong distinguished defect point')
    base=(1,gens[3][0],gens[0][0],gens[0][gens[3][0]-1])
    quads=sorted({tuple(g[x-1] for x in base) for g in group})
    require([list(q) for q in quads]==trace['quads'],'Wrong original orbit')
    # Bipartite coset graph, with each edge oriented from B\G to A\G.
    end_groups=[group_closure(gens[:3]),group_closure(gens[1:])]
    require([len(h) for h in end_groups]==[128,128],'Wrong end quotient orders')
    partitions=[];endpoints=[]
    for subgroup in end_groups:
        block={g[0] for g in subgroup}
        blocks=sorted({tuple(sorted(g[i-1] for i in block)) for g in group})
        require(len(blocks)==8 and all(len(b)==16 for b in blocks),'Wrong end coset partition')
        require(sorted(x for block in blocks for x in block)==list(range(1,129)),'End blocks do not partition edges')
        partitions.append(blocks)
        endpoints.append({x:j for j,block in enumerate(blocks) for x in block})
    parents=list(range(16))
    def root(v):
        while parents[v]!=v:v=parents[v]
        return v
    tree=[]
    for edge in FREE_SOURCE:
        av,bv=endpoints[0][edge],8+endpoints[1][edge]
        require(root(av)!=root(bv),'A free-source edge creates a cycle')
        parents[root(av)]=root(bv)
        tree.append(dict(edge=edge,A_vertex=av,B_vertex=bv))
    require(len({root(v) for v in range(16)})==1,'The fifteen free-source edges do not span')
    for a,b,c,d in quads:
        require(endpoints[0][a]==endpoints[0][c] and endpoints[1][a]==endpoints[1][b] and
                endpoints[0][b]==endpoints[0][d] and endpoints[1][c]==endpoints[1][d],
                'Original cell is not a closed d^-1 c a^-1 b boundary for B-to-A edges')
    original=[[-d,c,-a,b] for a,b,c,d in quads]
    require(original==trace['originals'],'Wrong original relators')
    current=dict(enumerate(original)); expansions={i:[i] for i in range(1,129)};gone=set()
    for step in trace['steps']:
        x,row=step['variable'],step['relation']
        require(x not in gone and row in current,'Repeated elimination or absent defining row')
        word=current[row]
        require(word==step['before'],'Wrong defining word')
        positions=[i for i,y in enumerate(word) if abs(y)==x]
        require(len(positions)==1,'Defining generator is not unique')
        at=positions[0];a,b=word[:at],word[at+1:];sign=1 if word[at]>0 else -1
        image=free(inv(a)+inv(b) if sign==1 else b+a)
        require(step['left']==a and step['right']==b and step['sign']==sign and step['replacement']==image,'Wrong solved equation')
        require(x not in map(abs,image) and replace(word,x,image)==[],'Invalid elimination')
        current={r:v for r,w in current.items() if r!=row and (v:=replace(w,x,image))}
        expansions={i:replace(w,x,image) for i,w in expansions.items()}
        gone.add(x)
    require(len(gone)==111 and sorted(set(range(1,129))-gone)==SURVIVORS,'Wrong surviving free generators')
    require({str(k):v for k,v in current.items()}==trace['remaining'],'Wrong full final relator inventory')
    require(len(current)==512,'Wrong number of nonempty final relators')
    require(free(inv(expansions[1])+expansions[40])==trace['delta']==[-6,7],
            'Wrong original defect under the reversible eliminations')
    fwd,bwd=basis_images()
    for i in SURVIVORS:require(evaluate(fwd[i],bwd)==[i],'Free-basis backward-forward failure')
    for i in range(1,18):require(evaluate(bwd[i],fwd)==[i],'Free-basis forward-backward failure')
    transformed={r:evaluate(w,fwd) for r,w in current.items()}
    require(all(normal(w)==[] for w in transformed.values()),'A final relation survives in F15*V4')
    witnesses={}
    for row,expected in [(30,[Y,Y]),(67,[X,X]),(176,[-Y,-X,Y,X])]:
        prefix,core=cyclic(transformed[row])
        require(core==expected,'Incorrect reverse relation witness')
        witnesses[str(row)]=dict(original_quad=quads[row],final_word=current[row],
                                 transformed_word=transformed[row],conjugating_prefix=prefix,
                                 cyclic_core=core)
    raw_images={i:evaluate(w,fwd) for i,w in expansions.items()}
    images={i:normal(w) for i,w in raw_images.items()}
    require(all(evaluate(w,images,normal)==[] for w in original),'An original relation survives in target normal form')
    require(normal(inv(images[1])+images[40])==[X],'Marked defect is not X')
    target_relations=[[X,X],[Y,Y],[-Y,-X,Y,X]]
    for i in range(1,18):require(evaluate(bwd[i],images,normal)==[i],'Target-generator composite differs')
    for i in SURVIVORS:
        require(evaluate(raw_images[i],bwd)==[i],'Surviving original-generator composite differs freely')

    def action_for(g):
        action={i+1:images[g[s-1]] for i,s in enumerate(FREE_SOURCE)}
        action[X]=normal(inv(images[g[6-1]])+images[g[7-1]])
        action[Y]=normal(inv(images[g[1-1]])+images[g[3-1]]+inv(images[g[12-1]])+images[g[6-1]])
        action[18]=normal(action[X]+action[Y])
        return action

    actions=[action_for(g) for g in gens]
    for number,action in enumerate(actions):
        require(all(evaluate(w,action,normal)==[] for w in target_relations),'Action fails V4 relations')
        require(all(evaluate(action[i],action,normal)==[i] for i in range(1,18)),'Action generator is not involutory')
        require(all(evaluate(images[i],action,normal)==images[gens[number][i-1]] for i in range(1,129)),
                'Transported action disagrees on an original generator')
    for i,j in [(0,2),(0,3),(1,3)]:
        require(all(evaluate(actions[i][k],actions[j],normal)==evaluate(actions[j][k],actions[i],normal)
                    for k in range(1,18)),'Nonadjacent actions fail to commute')
    action_keys={tuple(tuple(a[k]) for k in range(1,18)) for g in group for a in [action_for(g)]}
    require(len(action_keys)==1024,'Unexpected action kernel')
    # Verify the complete finite multiplication interface on each generating edge.
    for g in group:
        ag=action_for(g)
        for s,action in zip(gens,actions):
            gs=tuple(s[i-1] for i in g);ags=action_for(gs)
            require(all(evaluate(ag[k],action,normal)==ags[k] for k in range(1,18)),
                    'Finite G-action multiplication mismatch')

    columns=[[parity(action[i]) for i in range(1,18)] for action in actions]
    w=parity(images[1]);u=linear(w,columns[3])^w
    require(linear(w,columns[1])==w and linear(w,columns[2])==w,'Medial nonfixity in canonical mod-2 quotient')
    require(linear(u,columns[0])==u,'Outer relation fails in canonical mod-2 quotient')
    z_w=w
    for letter in model['z_word_1based']:z_w=linear(z_w,columns[letter-1])
    require(z_w^w==1<<15,'Wrong canonical mod-2 defect')
    def affine_kernel(matrices,shifts):
        # Each difference is inverse(chosen lift) times the new lift.
        # Its invariant span contains, and is generated by, the usual
        # conjugate Schreier generators. Invariance is explicitly checked.
        identity=tuple(range(1,129)); lifts={identity:0}; pending=[identity];loops=[]
        for g in pending:
            v=lifts[g]
            for s,m,shift in zip(gens,matrices,shifts):
                gs=tuple(s[i-1] for i in g); new_v=linear(v,m)^shift
                if gs not in lifts:lifts[gs]=new_v;pending.append(gs)
                else:loops.append(new_v^lifts[gs])
        require(len(lifts)==1024,'Affine projection is not onto')
        basis=binary_span(loops)
        require(all(len(binary_span(basis+[linear(v,m)]))==len(basis)
                    for v in basis for m in matrices),'Schreier kernel span is not invariant')
        return basis

    kernel_basis=affine_kernel(columns,[0,0,0,u])
    require(kernel_basis==[1<<16,1<<15],'Unexpected full affine kernel')
    require(all(m[16]==1<<16 for m in columns),'Y line is not pointwise fixed')
    require([m[15] for m in columns]==[3<<15,1<<15,1<<15,3<<15],'Wrong action on X')
    mask=(1<<16)-1
    quotient_columns=[[v&mask for v in m] for m in columns]
    quotient_kernel=affine_kernel(quotient_columns,[0,0,0,u&mask])
    require(quotient_kernel==[1<<15],'Unexpected double-cover kernel')
    invariant_lines=[v for v in [1<<15,1<<16,3<<15] if all(linear(v,m)==v for m in columns)]
    require(invariant_lines==[1<<16],'Wrong invariant kernel lines')
    return dict(format='phase92-complement-free-product-v1',
                free_source_generators=FREE_SOURCE,surviving_generators=SURVIVORS,
                target_encoding={'free_letters':'signed 1..15 in listed order','X':16,'Y':17,'XY':18},
                coset_square_complex={'A_blocks':partitions[0],'B_blocks':partitions[1],
                    'edge_orientation':'B coset vertex to A coset vertex',
                    'vertex_encoding':'A vertices 0..7, B vertices 8..15, using listed sorted blocks',
                    'spanning_tree':tree,'all_closed_cell_boundaries_checked':1024,
                    'tree_quotient_normal_form':'C2 x C2, since these tree edges are exactly f1,...,f15'},
                inverse_target_generators={str(i):bwd[i] for i in range(1,18)},
                forward_survivor_free_basis={str(i):fwd[i] for i in SURVIVORS},
                original_generator_survivor_expansions={str(i):expansions[i] for i in range(1,129)},
                original_generator_target_normal_forms={str(i):images[i] for i in range(1,129)},
                reverse_relation_witnesses=witnesses,
                original_relators_checked=1024,final_relators_checked=512,
                free_basis_composites_checked=34,target_generator_composites_checked=17,
                marked_defect_normal_form=[X],
                action_generator_images=[{str(i):a[i] for i in range(1,18)} for a in actions],
                faithful_action_order=len(action_keys),action_generator_edge_products_checked=4096,
                all_original_generator_action_checks=512,
                mod2_module={'dimension':17,'action_columns':columns,'w':w,'u':u,'defect':1<<15,
                             'affine_projection_order':1024,'kernel_basis':kernel_basis,
                             'kernel_dimension':len(kernel_basis),
                             'affine_group_order':1024*(1<<len(kernel_basis)),
                             'unique_invariant_kernel_line':1<<16,
                             'quotient_by_Y_kernel_basis':quotient_kernel,
                             'quotient_by_Y_group_order':2048},
                proved_structure='F_15 * (C2 x C2)',
                scope='Exact original presentation with marked defect and fixed group action. Written Tietze/free-basis argument supplies bidirectional interpretation; no GAP simplifier is an input.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--expected-certificate',type=Path)
    a=p.parse_args()
    require(not a.output_dir.exists() and not a.output_dir.is_symlink(),'Fresh output directory required')
    started=time.monotonic();raw={name:(ROOT/name).read_bytes() for name in INPUTS}
    require(all(sha(data)==INPUTS[name] for name,data in raw.items()),'Frozen input changed')
    result=replay(json.loads(raw['phase66_coprime_cover_permutation_model.json']),json.loads(raw['phase83_word_elimination.json']))
    require(all((ROOT/name).read_bytes()==data for name,data in raw.items()),'Input changed during replay')
    certificate=(json.dumps(result,indent=2)+'\n').encode()
    if a.expected_certificate:
        require(a.expected_certificate.read_bytes()==certificate,'Distributed certificate differs from exact regeneration')
    a.output_dir.mkdir(parents=True,exist_ok=False)
    (a.output_dir/'certificate.json').write_bytes(certificate)
    report=dict(status='PASS',date='2026-10-10',seconds=time.monotonic()-started,
                inputs=INPUTS,checker_sha256=sha(Path(__file__).read_bytes()),certificate_sha256=sha(certificate),
                structure=result['proved_structure'],original_relators=1024,eliminations=111,
                final_relators=512,marked_defect='X',faithful_action_order=result['faithful_action_order'],
                mod2_module=result['mod2_module'],no_GAP_or_imported_algebra_code=True,
                formal_Lean_normal_form_claim=False,priority_claim=False)
    (a.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
