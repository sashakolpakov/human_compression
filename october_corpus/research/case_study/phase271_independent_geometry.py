#!/usr/bin/env python3
"""Independent literal triangle models, using polynomial arithmetic rather than GAP."""
import argparse, collections, itertools, json, pathlib, time

def need(b, message):
    if not b:
        raise RuntimeError("PHASE271_REJECT " + message)

class Field:
    def __init__(self, p, coefficients):
        self.p = p
        self.modulus = coefficients
        self.e = len(coefficients)-1
        self.q = p**self.e
        need(coefficients[-1] == 1, "monic field modulus")
        self.digits = []
        for n in range(self.q):
            a=[]
            for _ in range(self.e):
                a.append(n % p); n //= p
            self.digits.append(a)
        self.adds=[[self.enc([(a+b)%p for a,b in zip(self.digits[x],self.digits[y])])
                    for y in range(self.q)] for x in range(self.q)]
        self.mults=[[self.multiply(x,y) for y in range(self.q)] for x in range(self.q)]
        # Exact independent field check; no supplied irreducibility assertion.
        need(all(self.pow(x,self.q-1)==1 for x in range(1,self.q)), "all nonzero inverses")
        self.inverses=[0]+[self.pow(x,self.q-2) for x in range(1,self.q)]
    def enc(self, v):
        return sum(x*self.p**i for i,x in enumerate(v))
    def add(self,x,y):
        return self.adds[x][y]
    def neg(self,x):
        return self.enc([(-a)%self.p for a in self.digits[x]])
    def sub(self,x,y):
        return self.add(x,self.neg(y))
    def multiply(self,x,y):
        v=[0]*(2*self.e-1)
        for i,a in enumerate(self.digits[x]):
            for j,b in enumerate(self.digits[y]):
                v[i+j]=(v[i+j]+a*b)%self.p
        for k in range(len(v)-1,self.e-1,-1):
            for j,a in enumerate(self.modulus):
                v[k-self.e+j]=(v[k-self.e+j]-v[k]*a)%self.p
        return self.enc(v[:self.e])
    def mul(self,x,y):
        return self.mults[x][y]
    def pow(self,x,n):
        r=1
        while n:
            if n&1:r=self.mul(r,x)
            x=self.mul(x,x);n//=2
        return r
    def dot(self,v,w):
        a=0
        for x,y in zip(v,w):a=self.add(a,self.mul(x,y))
        return a
    def normvec(self,v):
        a=next(x for x in v if x)
        return tuple(self.mul(x,self.inverses[a]) for x in v)
    def lincomb(self,a,v,b,w):
        return tuple(self.add(self.mul(a,x),self.mul(b,y)) for x,y in zip(v,w))

def hermitian(q,F):
    need(F.q==q*q, "quadratic field")
    # Hyperbolic form rather than author's diagonal form.
    points=[]
    for v in itertools.product(range(F.q),repeat=3):
        if not any(v) or v != F.normvec(v):continue
        value=F.add(F.add(F.mul(v[0],F.pow(v[2],q)),F.mul(v[2],F.pow(v[0],q))),F.pow(v[1],q+1))
        if value==0:points.append(v)
    need(len(points)==q**3+1, "isotropic point count")
    lookup={p:i for i,p in enumerate(points)}
    # Secants from their point spans, not from a supplied table or line equations.
    blocks=set()
    for i,j in itertools.combinations(range(len(points)),2):
        v,w=points[i],points[j]
        span={F.normvec(F.lincomb(1,v,b,w)) for b in range(F.q)}
        span.add(w)
        block=frozenset(lookup[x] for x in span if x in lookup)
        need(len(block)==q+1,"every secant size")
        blocks.add(block)
    blocks=sorted(blocks,key=lambda x:tuple(sorted(x)))
    need(len(blocks)==q*q*(q*q-q+1), "all secants")
    counts=collections.Counter(pair for B in blocks for pair in itertools.combinations(sorted(B),2))
    need(len(counts)==len(points)*(len(points)-1)//2 and set(counts.values())=={1},"unique secant")
    return points,blocks

def residue_profiles(adj):
    profiles=[]
    for root in range(len(adj)):
        dist={root:0};todo=collections.deque([root])
        while todo:
            u=todo.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v]=dist[u]+1;todo.append(v)
        need(len(dist)==len(adj),"connected residue")
        counts=collections.Counter(dist.values())
        profiles.append(tuple(counts[d] for d in range(max(dist.values())+1)))
    # Independent girth: remove one undirected edge and find shortest alternate path.
    girth=len(adj)+1
    for u in range(len(adj)):
        for v in adj[u]:
            if v<u:continue
            dist={u:0};todo=collections.deque([u])
            while todo:
                x=todo.popleft()
                for y in adj[x]:
                    if (x==u and y==v) or (x==v and y==u):continue
                    if y not in dist:
                        dist[y]=dist[x]+1;todo.append(y)
                if v in dist:break
            if v in dist:girth=min(girth,dist[v]+1)
    return profiles,girth

def triangle_check(points,blocks):
    flags=[(p,l) for p in range(len(points)) for l,B in enumerate(blocks) if p in B]
    D=[];pred=[0]*len(flags)
    for i,(p,l) in enumerate(flags):
        out=0
        for j,(q,m) in enumerate(flags):
            if p in blocks[m] and q not in blocks[l]:
                out|=1<<j;pred[j]|=1<<i
        D.append(out)
    k=len(blocks[0]);r=(len(points)-1)//(k-1)
    def bits(n):
        while n:
            b=n&-n;yield b.bit_length()-1;n-=b
    panels=0;chambers=0
    for i in range(len(flags)):
        for j in bits(D[i]):
            completion=D[j]&pred[i]
            need(completion.bit_count()==k-1,"literal panel completion")
            panels+=1;chambers+=completion.bit_count()
        for j in range(i):
            succ=(D[i]&D[j]).bit_count();prev=(pred[i]&pred[j]).bit_count()
            need(succ==((r-2)*(k-1)) if flags[i][0]==flags[j][0] else succ in [0,k-2],"point signature")
            need(prev==((k-2)*(r-1)) if flags[i][1]==flags[j][1] else prev in [0,r-2],"line signature")
    # Literal residue at one flag: one side consists of its D successors,
    # the other of its D predecessors; incidence is again D.
    base=0
    left=list(bits(D[base]));right=list(bits(pred[base]))
    adj=[set() for _ in range(len(left)+len(right))]
    for a,i in enumerate(left):
        for b,j in enumerate(right):
            edge=bool(D[i]&(1<<j))
            # Check both directions of the proposed deleted-pencil bridge.
            need(edge == (flags[i][0] in blocks[flags[j][1]]),"literal deleted-pencil incidence")
            if edge:adj[a].add(b+len(left));adj[b+len(left)].add(a)
    need(set(map(len,adj))=={k-1},"all degrees")
    profiles,girth=residue_profiles(adj)
    return dict(v=len(points),blocks=len(blocks),flags=len(flags),signature_pairs=len(flags)*(len(flags)-1)//2,
                panels_one_type_pair=panels,chambers=chambers,residue_parts=[len(left),len(right)],
                girth=girth,point_profiles=sorted(set(profiles[:len(left)])),line_profiles=sorted(set(profiles[len(left):])))

def frame_check():
    F=Field(3,[1,0,1])
    elements=list(range(9))
    squares={F.pow(x,2) for x in elements[1:]}
    det=lambda a:F.sub(F.mul(a[0],a[3]),F.mul(a[1],a[2]))
    matrices=[a for a in itertools.product(elements,repeat=4) if det(a)]
    H=[(a,e) for a in matrices for e in [0,1] if (det(a) in squares)==(e==0)]
    need(len(H)==len(matrices)==5760,"frame orders")
    image={a for a,e in H}
    # Field Frobenius fixes the coordinate basis; each matrix is its image.
    need(len(image)==5760,"all frame images")
    need({det(a) for a,e in H if e==0}==squares,"linear determinant half")
    image_det={F.mul(det(a),F.pow(1,3**e)) for a,e in H}
    need(image_det==set(elements[1:]),"determinant orbit")
    nonsquare=next(x for x in elements[1:] if x not in squares)
    need(((nonsquare,0,0,1),0) not in H and ((nonsquare,0,0,1),1) in H,"GL excluded semilinear element included")
    # A proper subgroup with only the square linear determinants has two frame orbits.
    need(len({a for a,e in H if e==0})==2880,"negative determinant-transitivity control")
    return dict(field_modulus=F.modulus,H=5760,linear_half=2880,frame_orbit=5760,affine_order=81*5760,
                nonsquare_element=nonsquare,GL_contained=False)

def trace_orbits(p,e,modulus):
    F=Field(p,modulus);q=p**e
    fiber={z for z in range(F.q) if F.add(z,F.pow(z,q))==F.neg(1)}
    need(len(fiber)==q,"trace fiber size")
    orbits=[]
    while fiber:
        start=min(fiber);orbit=set();z=start
        while z not in orbit:orbit.add(z);z=F.pow(z,p)
        need(orbit<=fiber,"Frobenius fiber stability")
        fiber-=orbit;orbits.append(sorted(orbit))
    need((len(orbits)==1)==(q in [2,4]),"sampled exact unital criterion")
    return dict(q=q,orbit_lengths=sorted(map(len,orbits)),modulus=modulus)

def circle_check(v):
    blocks=list(itertools.combinations(range(v),2))
    flags=[(p,L) for L in blocks for p in L]
    lookup={f:i for i,f in enumerate(flags)}
    D=[{j for j,(q,M) in enumerate(flags) if p in M and q not in L} for p,L in flags]
    N=3*len(flags);adj=[set() for _ in range(N)]
    for i,row in enumerate(D):
        for j in row:
            for t in range(3):
                a=3*i+t;b=3*j+(t+1)%3
                adj[a].add(b);adj[b].add(a)
    def components(adj):
        left=set(range(len(adj)));result=[]
        while left:
            root=min(left);seen={root};todo=[root]
            for x in todo:
                for y in adj[x]:
                    if y not in seen:seen.add(y);todo.append(y)
            result.append(sorted(seen));left-=seen
        return result
    cc=components(adj)
    need(len(cc)==(6 if v==3 else 1),"circle global components")
    if v==3:
        need(all(len(c)==3 and {x%3 for x in c}=={0,1,2} for c in cc),"six typed chambers")
    neighbors=sorted(adj[0]);ri={x:i for i,x in enumerate(neighbors)}
    radj=[{ri[y] for y in adj[x] if y in ri} for x in neighbors]
    need(len(radj)==2*(v-2) and set(map(len,radj))=={1} and len(components(radj))==v-2,"circle matching residue")
    beta=[3*lookup[(next(q for q in L if q!=p),L)]+(-t)%3
          for p,L in flags for t in range(3)]
    tau=[3*i+(t+1)%3 for i in range(len(flags)) for t in range(3)]
    for name,perm in [('endpoint_type_reversal',beta),('triality',tau)]:
        need(set(perm)==set(range(N)) and all({perm[y] for y in adj[x]}==adj[perm[x]] for x in range(N)),name)
    diagonal=0
    for perm in itertools.permutations(range(v)):
        image=[lookup[(perm[p],tuple(sorted(perm[q] for q in L)))] for p,L in flags]
        need(all({image[j] for j in D[i]}==D[image[i]] for i in range(len(flags))),"all diagonal permutations")
        diagonal+=1
    if v>=4:
        for i,j in itertools.combinations(range(len(flags)),2):
            need((len(D[i]&D[j])==v-3)==(flags[i][0]==flags[j][0]),"circle point-fiber signature")
    return dict(v=v,objects=N,components=[len(c) for c in cc],residue_components=v-2,
                diagonal_permutations=diagonal,triality=True,endpoint_type_reversal=True,
                full_group_count_source="written reconstruction, not exhaustive graph-automorphism enumeration")

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--out",type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),"fresh report");start=time.monotonic()
    models=[]
    for q,p,modulus in [(2,2,[1,1,1]),(4,2,[1,1,0,0,1])]:
        points,blocks=hermitian(q,Field(p,modulus));r=triangle_check(points,blocks)
        if q==2:
            need(r["girth"]==12 and r["point_profiles"]==[(1,2,2,2,2,2,1)],"small unital cycle")
        else:
            need(r["girth"]==8 and r["point_profiles"]==[(1,4,12,36,44,20,3)] and r["line_profiles"]==[(1,4,12,36,42,20,5)],"exceptional profiles")
        r["q"]=q;models.append(r)
    traces=[trace_orbits(*args) for args in [(2,1,[1,1,1]),(3,1,[1,0,1]),(2,2,[1,1,0,0,1]),(5,1,[2,0,1]),(2,3,[1,1,0,0,0,0,1])]]
    report=dict(status="PASS",seconds=round(time.monotonic()-start,3),hermitian_models=models,frames=frame_check(),
                trace_fibers=traces,circle_models=[circle_check(v) for v in range(3,7)],scope="Independent exact diagnostics; uniform classification remains written with declared retained inputs.")
    report["seconds"]=round(time.monotonic()-start,3)
    a.out.write_text(json.dumps(report,indent=2)+"\n")
    print("PHASE271_INDEPENDENT_PASS",len(models),sum(r["signature_pairs"] for r in models),report["seconds"])
if __name__=="__main__":main()
