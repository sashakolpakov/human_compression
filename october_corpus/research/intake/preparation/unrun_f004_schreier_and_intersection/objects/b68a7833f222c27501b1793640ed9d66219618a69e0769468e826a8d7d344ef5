"""Complete finite orbit with a certified small Schreier stabilizer, no recognition."""
import struct
import runtime as rt
import field,solve
NMAX=10000
SMAX=128
KMAX=8
MAGIC=b'F004SSP1'
HEADER=19
MAX_BYTES=121315
class Inconclusive(RuntimeError):pass

def generators(g,b):
    rt.need(type(g)in(tuple,list)and len(g)==3,'three explicit generators')
    b.scalar(147)
    rt.need(all(type(a)is bytes and len(a)==49 and all(x<11 for x in a)for a in g)
        and len(set(g))==3 and all(a!=field.I for a in g),'distinct nonidentity whole F11 matrices')
    for a in g:rt.need(b.multiply(a,a)==field.I,'all three full involution equations')

def prime_value(g,word,cofactor,labels,b,prime=19):
    rt.need(type(prime)is int and prime in(3,19),'pure controls3 or production19')
    rt.need(type(word)is list and 1<=len(word)<=32 and all(type(x)is int and x in labels for x in word)
        and type(cofactor)is int and cofactor in(1,7),'bounded positive word in exact Original end labels and cofactor')
    b.scalar(len(word)+1);w=field.I
    for x in word:w=b.multiply(w,g[x])
    Y=field.I
    for _ in range(cofactor):Y=b.multiply(Y,w)
    rt.need(Y!=field.I,'fresh nonidentity prime value');p=field.I
    for _ in range(prime):p=b.multiply(p,Y)
    rt.need(p==field.I,'fresh complete prime power is identity');return Y

def fixed_basis(Y,b):
    b.scalar(49)
    return solve.nullspace([[(Y[7*i+j]-int(i==j))%11 for i in range(7)]for j in range(7)],7,b)

def decode(raw,b):
    rt.need(type(raw)is bytes and HEADER<=len(raw)<=MAX_BYTES and raw[:8]==MAGIC,'whole bounded stabilizer carrier header')
    n=raw[8]|raw[9]<<8;m=raw[10];k=raw[11];v=raw[12:19]
    rt.need(1<=n<=NMAX and 1<=m<=SMAX and 0<=k<=KMAX and(k or m==1)
        and len(raw)==HEADER+2*k+2*m+m*k+12*n,'exact complete carrier extent')
    rt.need(any(v)and all(x<11 for x in v),'canonical nonzero seven-coordinate seed')
    b.scalar(len(raw));o=HEADER
    ge=[raw[o+2*j]|raw[o+2*j+1]<<8 for j in range(k)];o+=2*k
    rt.need(len(set(ge))==k and all(e<3*n for e in ge),'distinct actual orbit edge identifiers for stabilizer generators')
    st=[tuple(raw[o+2*i:o+2*i+2])for i in range(m)];o+=2*m
    table=raw[o:o+m*k];o+=m*k
    rt.need(st[0]==(255,255)and all(p<i and j<k for i,(p,j)in enumerate(st[1:],1))
        and all(t<m for t in table),'whole earlier-parent stabilizer tree and multiplication targets')
    nodes=[]
    for i in range(n):
        p,j=struct.unpack_from('<HB',raw,o);o+=3;edges=[]
        for _ in range(3):
            target,s=struct.unpack_from('<HB',raw,o);o+=3
            rt.need(target<n and s<m,'typed actual orbit target and stabilizer element');edges.append((target,s))
        rt.need((p,j)==(65535,255)if i==0 else p<i and j<3,'unique root or strict earlier orbit parent')
        nodes.append((p,j,edges))
    rt.need(o==len(raw),'whole carrier EOF');return v,ge,st,table,nodes

def encode(v,ge,st,table,nodes,b):
    n=len(nodes);m=len(st);k=len(ge)
    rt.need(1<=n<=NMAX and 1<=m<=SMAX and 0<=k<=KMAX,'finite binary producer extents')
    raw=bytearray(MAGIC+struct.pack('<HBB',n,m,k)+v)
    for e in ge:raw.extend(struct.pack('<H',e))
    for p,j in st:raw.extend(bytes((p,j)))
    raw.extend(table)
    for p,j,edges in nodes:
        raw.extend(struct.pack('<HB',p,j))
        for target,s in edges:raw.extend(struct.pack('<HB',target,s))
    rt.need(len(raw)==HEADER+2*k+2*m+m*k+12*n<=MAX_BYTES,'prospective whole binary bound')
    b.scalar(len(raw));return bytes(raw)

def member(v,rows,lifts,S,omitted,b):
    w=b.image(v,omitted);indices={x:i for i,x in enumerate(rows)}
    if w not in indices:return False
    t=lifts[indices[w]]
    for s in S:
        if(t if s==field.I else b.multiply(s,t))==omitted:return True
    return False

def check(g,raw,b,omitted=None):
    generators(g,b);v,ge,st,table,nodes=decode(raw,b);n=len(nodes);m=len(st);k=len(ge)
    rows=[v];lifts=[field.I];inverse=[field.I];seen={v}
    for p,j,edges in nodes[1:]:
        w=b.image(rows[p],g[j]);rt.need(w not in seen,'all full orbit vectors distinct');seen.add(w);rows.append(w)
        lifts.append(b.multiply(lifts[p],g[j]));inverse.append(b.multiply(g[j],inverse[p]))
    gs=[]
    for e in ge:
        i,j=divmod(e,3);target=nodes[i][2][j][0]
        gs.append(b.multiply(b.multiply(lifts[i],g[j]),inverse[target]))
    S=[field.I];matrices={field.I}
    for p,j in st[1:]:
        s=b.multiply(S[p],gs[j]);rt.need(s not in matrices,'all full stabilizer matrices distinct');S.append(s);matrices.add(s)
    for i,s in enumerate(S):
        rt.need(b.image(v,s)==v,'every whole stabilizer matrix fixes seed')
        for j,h in enumerate(gs):rt.need(b.multiply(s,h)==S[table[i*k+j]],'every small stabilizer generator multiplication closed')
    for i,(p,j,edges)in enumerate(nodes):
        for label,(target,si)in enumerate(edges):
            rhs=lifts[target]if si==0 else b.multiply(S[si],lifts[target])
            rt.need(b.multiply(lifts[i],g[label])==rhs,'EVERY full left-factor Schreier edge equation')
    facts=dict(status='VERIFIED_EXACT_END_ORDER_BY_SMALL_STABILIZER_SCHREIER',orbit_size=n,stabilizer_size=m,
        stabilizer_generators=k,exact_end_order=n*m,all_generator_edges=3*n,
        complete_stabilizer_closure=True,all_stabilizer_generators_actual_H_words=True,
        all_stabilizer_elements_fix_seed=True,all_left_factor_edge_equations_verified=True,
        endpoint_type_recognized=False,generation_proved=False,intersection_property_proved=False,new_case_credit=0)
    if omitted is not None:facts['omitted_mark_in_certified_end']=member(v,rows,lifts,S,omitted,b)
    return facts,v

def small_closure(gs,b,cap):
    S=[field.I];positions={field.I:0};tree=[(255,255)];table=bytearray();i=0
    while i<len(S):
        for j,h in enumerate(gs):
            w=b.multiply(S[i],h)
            if w not in positions:
                if len(S)>=cap:raise Inconclusive('small stabilizer closure cap; no order or absence conclusion')
                positions[w]=len(S);S.append(w);tree.append((i,j))
            table.append(positions[w])
        i+=1
    return S,positions,tree,bytes(table)

def build(g,v,b,ncap=NMAX,scap=SMAX):
    generators(g,b);rt.need(type(ncap)is int and 1<=ncap<=NMAX and type(scap)is int and 1<=scap<=SMAX,'controls lower finite caps only')
    rt.need(type(v)is bytes and len(v)==7 and any(v)and all(x<11 for x in v),'one nonzero canonical supplied seed')
    rows=[v];indices={v:0};lifts=[field.I];inverse=[field.I];parents=[(65535,255)];targets=[];i=0
    while i<len(rows):
        for j in range(3):
            w=b.image(rows[i],g[j])
            if w not in indices:
                if len(rows)>=ncap:raise Inconclusive('vector orbit cap; no absence or order conclusion')
                indices[w]=len(rows);rows.append(w);parents.append((i,j))
                lifts.append(b.multiply(lifts[i],g[j]));inverse.append(b.multiply(g[j],inverse[i]))
            targets.append(indices[w])
        i+=1
    gs=[];ge=[];S=[field.I];positions={field.I:0};st=[(255,255)];table=b'';sch=bytearray()
    for e,target in enumerate(targets):
        i,j=divmod(e,3);h=b.multiply(b.multiply(lifts[i],g[j]),inverse[target]);sch.extend(h)
        if h not in positions:
            if len(gs)>=KMAX:raise Inconclusive('eight Schreier generators cap; no order conclusion')
            gs.append(h);ge.append(e);S,positions,st,table=small_closure(gs,b,scap)
    for s in S:rt.need(b.image(v,s)==v,'fresh whole generated stabilizer fixes seed')
    nodes=[]
    for i,(p,j)in enumerate(parents):
        edges=[(targets[3*i+a],positions[bytes(sch[49*(3*i+a):49*(3*i+a+1)])])for a in range(3)]
        nodes.append((p,j,edges))
    raw=encode(v,ge,st,table,nodes,b)
    facts=dict(status='SUPPLIED_COMPLETE_SMALL_STABILIZER_ORDER_CARRIER',orbit_size=len(rows),stabilizer_size=len(S),
        stabilizer_generators=len(gs),claimed_end_order=len(rows)*len(S),independent_consumer_required=True)
    return raw,facts,(rows,lifts,S)
