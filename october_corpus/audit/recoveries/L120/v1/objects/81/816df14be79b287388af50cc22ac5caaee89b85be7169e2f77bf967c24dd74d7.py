"""Small controls, not premises for the uniform proofs in elementary.tex."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import itertools,json,math

def need(ok,msg):
    if not ok: raise ValueError(msg)
def pmul(a,b):return tuple(b[a[i]] for i in range(len(a)))
def trans(n,i,j):
    p=list(range(n));p[i],p[j]=p[j],p[i];return tuple(p)
def mmul(a,b,q):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3))%q for i in range(3) for j in range(3))
def matrix(p,q):
    a=[]
    for i in range(3):
        row=[0]*4;row[p[i]]+=1;row[p[3]]-=1;a.extend(x%q for x in row[:3])
    return tuple(a)
def closure(gens,mul,one):
    seen={one};todo=[one]
    while todo:
        x=todo.pop()
        for g in gens:
            y=mul(x,g)
            if y not in seen:seen.add(y);todo.append(y)
    return seen
def rank(rows,q):
    a=[list(x) for x in rows];r=0
    for c in range(len(a[0])):
        j=next((j for j in range(r,len(a)) if a[j][c]),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r];u=pow(a[r][c],-1,q);a[r]=[x*u%q for x in a[r]]
        for j in range(len(a)):
            if j!=r:
                u=a[j][c];a[j]=[(x-u*y)%q for x,y in zip(a[j],a[r])]
        r+=1
    return r
def order(p):
    seen=set();out=1
    for i in range(len(p)):
        if i in seen:continue
        x=i;k=0
        while x not in seen:seen.add(x);k+=1;x=p[x]
        out=math.lcm(out,k)
    return out
def action(q):
    ps=list(itertools.permutations(range(4)));images={p:matrix(p,q) for p in ps};need(len(set(images.values()))==24,'faithfulness')
    for a in ps:
        for b in ps:need(images[pmul(a,b)]==mmul(images[a],images[b],q),'representation multiplication')
    marks=[images[trans(4,i,i+1)] for i in range(3)];one=tuple(int(i==j) for i in range(3) for j in range(3));subs=[]
    for mask in range(8):subs.append(closure([marks[i] for i in range(3) if mask>>i&1],lambda a,b:mmul(a,b,q),one))
    need(len(subs[-1])==24,'group order')
    for i in range(8):
        for j in range(8):need(subs[i]&subs[j]==subs[i&j],'full IP')
    need(mmul(marks[0],marks[2],q)==mmul(marks[2],marks[0],q),'string')
    out={'q':q,'matrices':[list(x) for x in marks],'order':24,'multiplication_pairs':576,'IP_pairs':64,'subgroup_orders':[len(x) for x in subs]}
    if q==5:
        need(rank(list(images.values()),q)==9,'full matrix algebra');out['matrix_algebra_dimension']=9;out['orthogonal_derived_order']=5*(5**2-1)//2
        need(out['orthogonal_derived_order']>24,'order obstruction')
    return out

def paths():
    rows=[]
    for n in range(4,25):
        marks=[trans(n,i,i+1) for i in range(n-1)]
        for s in range(n-3):
            r=n-1-s;expected=list(range(r)) if s==0 else [((s+2-j)%2) for j in range(s+2)]+list(range(2,r))
            actual=[]
            for j in range(n-1):
                labels=[i for i,p in enumerate(marks) if p[j]==j+1]
                need(len(labels)==1,'one label per path edge');actual.extend(labels)
            need(actual==expected,'path pattern')
            for p in marks:
                need(all(abs(p[j]-j)<=1 for j in range(n)),'nonpath edge')
            typ=[order(pmul(marks[i],marks[i+1])) for i in range(r-1)]
            target=[3]*(r-1) if s==0 else [n-r+2,6]+[3]*(r-3)
            need(typ==target,'Schlafli type');rows.append({'n':n,'r':r,'labels':actual,'type':typ})
            if r>3:marks=[marks[1],pmul(marks[0],marks[2])]+marks[3:]
    return rows

def run():
    need(max(order(p) for p in itertools.permutations(range(4)))==4,'S4 maximum element order')
    return {'status':'PASS','actions':[action(2),action(5)],'paths':paths(),'uniform_proof_premise':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
