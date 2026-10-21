#!/usr/bin/env python3
"""Independent literal affine reconstruction of the exceptional two-orbit mix."""
from itertools import product
from pathlib import Path
import argparse,json
def need(b,m):
    if not b:raise ValueError(m)
points=list(product(range(3),repeat=2));ix={p:i for i,p in enumerate(points)}
one=tuple(range(9))
def affine(f):return tuple(ix[tuple(v%3 for v in f(x,y))]for x,y in points)
def mul(g,h):return tuple(g[h[i]]for i in range(9))
def subgroup(marks):
    out=[one];seen={one}
    for g in out:
        for h in marks:
            z=mul(g,h)
            if z not in seen:seen.add(z);out.append(z)
    return out
def partitions(edges):
    out=[]
    for mask in range(16):
        row=[0]*len(edges)
        for q in range(len(edges)):
            if row[q]:continue
            stack=[q];seen={q}
            while stack:
                v=stack.pop()
                for i in range(4):
                    if mask>>i&1:
                        w=edges[v][i]
                        if w not in seen:seen.add(w);stack.append(w)
            bits=sum(1<<v for v in seen)
            for v in seen:row[v]=bits
        out.append(row)
    return out
def ip(parts):
    for a,b in product(range(16),repeat=2):
        for q in range(len(parts[0])):need(parts[a][q]&parts[b][q]==parts[a&b][q],'actual all-subset path intersection')
    return 256*len(parts[0])
def run():
    a=affine(lambda x,y:(-x,y));b=affine(lambda x,y:(x,1-y));d=affine(lambda x,y:(y,x));ap=mul(mul(d,a),d)
    H=subgroup([a,b,d]);need(len(H)==72,'literal affine group order')
    flags=[(h,e)for h in H for e in [0,1]];lookup={v:i for i,v in enumerate(flags)}
    def step(v,i):
        h,e=v
        return [(h,1-e),(mul(a if e==0 else ap,h),e),(mul(b,h),e),(mul(d,h),1-e)][i]
    edges=[[lookup[step(v,i)]for i in range(4)]for v in flags]
    need(all(len({q,*edges[q]})==5 and all(edges[edges[q][i]][i]==q for i in range(4))for q in range(144)),'simple colored involutions')
    need(all(edges[edges[q][i]][j]==edges[edges[q][j]][i]for q in range(144)for i in range(4)for j in range(i+2,4)),'all actual string squares')
    parts=partitions(edges);need(parts[15][0]==(1<<144)-1,'connected input');n1=ip(parts)
    need(all(parts[6][q].bit_count()==(4 if e==0 else 6)for q,(h,e)in enumerate(flags)),'middle size distinguishes the two sheets')
    # These72 right multiplications are all automorphisms: a colored automorphism
    # is determined by one image, and middle sizes exclude the other sheet.
    for k in H:
        action=[lookup[mul(h,k),e]for h,e in flags]
        need(len(set(action))==144 and all(action[edges[q][i]]==edges[action[q]][i]for q in range(144)for i in range(4)),'actual right multiplication automorphism')
    base=(lookup[one,0],lookup[one,1]);mix=[base];mi={base:0};medges=[]
    for x,y in mix:
        row=[]
        for i in range(4):
            z=(edges[x][i],edges[y][i])
            if z not in mi:mi[z]=len(mix);mix.append(z)
            row.append(mi[z])
        medges.append(row)
    need(len(mix)==2592,'actual rooted mix size');mp=partitions(medges);n2=ip(mp)
    # Construct a color-preserving map from the base to EVERY flag. Each
    # attempted image is propagated along every actual edge, so a successful
    # bijection proves regularity directly, without a monodromy package.
    automorphisms=0
    for target in range(len(mix)):
        image=[-1]*len(mix);image[0]=target;queue=[0]
        for q in queue:
            for i,z in enumerate(medges[q]):
                want=medges[image[q]][i]
                if image[z]<0:image[z]=want;queue.append(z)
                else:need(image[z]==want,'global colored automorphism consistency')
        need(len(set(image))==len(mix)and -1 not in image,'actual mix automorphism bijective');automorphisms+=1
    q0=0;q1=medges[0][0]
    def fiber(mask,q):
        first,second=mix[q];out=set()
        for z,(x,y)in enumerate(mix):
            if mp[mask][q]>>z&1 and x==first:
                need(flags[y][1]==flags[second][1],'automorphism preserves second sheet');out.add(flags[y][0])
        return out
    Ty={affine(lambda x,y,c=c:(x,y+c))for c in range(3)}
    A={affine(lambda x,y,e=e,c=c:(e*x,e*y+c))for e in [1,-1]for c in range(3)}
    B0={affine(lambda x,y,e=e,c=c:(e*x+(0 if e==1 else 1),e*y+c))for e in [1,-1]for c in range(3)}
    B1={affine(lambda x,y,e=e,c=c:(e*x+c,e*y+(0 if e==1 else 1)))for e in [1,-1]for c in range(3)}
    C1={one,affine(lambda x,y:(-x,1-y))}
    fibers=[]
    for q,expected in [(q0,[A,B0,Ty]),(q1,[A,B1,C1])]:
        actual=[fiber(mask,q)for mask in [7,14,6]];need(actual==expected,'all six actual embedded variance subgroups')
        need(actual[0]&actual[1]==actual[2],'correct rooted criterion');fibers.append(actual)
    need(Ty&C1=={one} and len(A&B0)==3 and len(A&B1)==2,'both literal simplified criteria fail')
    # A word in the middle yields the order-three element at the first root.
    q=q0
    for i in [1,2,1,2]:q=medges[q][i]
    x,y=mix[q];need(x==base[0] and flags[y][0]==affine(lambda x,y:(x,y+2)) and flags[y][0]in Ty-{one},'actual middle word in left side but not common right side')
    # The second root reverses the factor order, exactly as Corollary6.15(2).
    need(mix[q1]==tuple(reversed(base)),'printed regular-cover argument order')
    return dict(status='PASS_DISTINCT_EXCEPTIONAL_AFFINE_MODEL',author_modules_imported=False,input_flags=144,actual_input_automorphisms=72,flag_orbits=2,medial_orbits=2,medial_sizes=[4,6],input_IP_identities=n1,mix_flags=2592,mix_IP_identities=n2,actual_mix_automorphisms=automorphisms,regular_mix=True,all_six_embedded_fibers=True,correct_intersections=[3,2],printed_right_intersection=1,Cor610_literal_failure=True,Cor615_2_reversed_arguments_literal_failure=True,whole_source_or_question_credit=False)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');r=run();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
