"""Complete finite point-orbit/Schreier stabilizer arithmetic over F11^7."""
import base64
I=bytes(int(i==j)for i in range(7)for j in range(7))
MAX_ORBIT=9240;MAX_K=2048;MAX_GENERATORS=16
class Incomplete(RuntimeError):pass

def need(ok,message):
    if not ok:raise ValueError(message)

def row(raw,b):
    b.scalar(7);need(type(raw)in(list,tuple)and len(raw)==7 and all(type(x)is int and 0<=x<11 for x in raw),'canonical row in F11^7')
    return bytes(raw)

def marks(raw,b):
    need(type(raw)in(list,tuple)and len(raw)==3,'three ordered end marks')
    out=[]
    for a in raw:
        need(type(a)in(list,tuple)and len(a)==7,'seven complete matrix rows')
        out.append(b''.join(row(r,b)for r in a))
    return tuple(out)

def seed(raw,b):
    v=row(raw,b);b.scalar(7);need(any(v),'nonzero seed vector');return v

def involutions(g,b):
    for a in g:need(b.multiply(a,a)==I,'all three complete involution equations')

def get2(raw,i):return raw[2*i]|raw[2*i+1]<<8

def put2(raw,x):raw.extend((x&255,x>>8))

def at(raw,i,width):return bytes(raw[width*i:width*(i+1)])

def blob(text,size):
    need(type(text)is str and len(text)==4*((size+2)//3)and text.isascii(),'exact canonical base64 extent')
    raw=base64.b64decode(text,validate=True)
    need(len(raw)==size and base64.b64encode(raw).decode('ascii')==text,'whole canonical base64 with exact EOF')
    return raw

def parse(cert):
    need(type(cert)is dict and set(cert)=={'n','parent_tree_b64','closure_edges_b64','K_generator_edges'},'exact finite orbit certificate')
    n=cert['n'];need(type(n)is int and 1<=n<=MAX_ORBIT,'bounded complete orbit size')
    tree=blob(cert['parent_tree_b64'],3*n);edges=blob(cert['closure_edges_b64'],6*n)
    need(tree[:3]==b'\xff\xff\xff','exact single tree root')
    selected=cert['K_generator_edges']
    need(type(selected)is list and len(selected)<=MAX_GENERATORS and all(type(e)is int and 0<=e<3*n for e in selected)and len(set(selected))==len(selected),'at most sixteen distinct actual edge indices')
    return n,tree,edges,selected

def encode(tree,edges,selected):
    need(len(tree)%3==0 and len(edges)==2*len(tree),'complete packed certificate extents')
    return dict(n=len(tree)//3,parent_tree_b64=base64.b64encode(tree).decode('ascii'),
        closure_edges_b64=base64.b64encode(edges).decode('ascii'),K_generator_edges=selected)

def reconstruct(g,v,cert,b,c):
    n,tree,edges,selected=parse(cert);c.update(orbit_declared=n,tree_vertices_verified=1,closure_edges_verified=0)
    points=bytearray(v);lookup={v:0};t=bytearray(I);u=bytearray(I);cache=[-1]*(3*n)
    for j in range(1,n):
        b.tick();p=tree[3*j]|tree[3*j+1]<<8;label=tree[3*j+2]
        need(p<j and label<3,'each tree parent is earlier with one original mark')
        image=b.image(at(points,p,7),g[label]);need(image not in lookup,'full distinct reached vectors')
        need(cache[3*p+label]==-1,'one fresh image per parent edge')
        lookup[image]=j;points.extend(image);cache[3*p+label]=j
        t.extend(b.multiply(at(t,p,49),g[label]));u.extend(b.multiply(g[label],at(u,p,49)))
        c['tree_vertices_verified']+=1
    for x in range(n):
        for label in range(3):
            b.tick();e=3*x+label;y=get2(edges,e);need(y<n,'all closure targets in the complete orbit')
            if cache[e]>=0:need(y==cache[e],'freshly evaluated parent image is the claimed closure edge')
            else:
                image=b.image(at(points,x,7),g[label]);need(image in lookup and lookup[image]==y,'every full original generator image closes at its claimed vector')
            c['closure_edges_verified']+=1
    need(len(lookup)==n and c['closure_edges_verified']==3*n,'whole distinct reachable orbit and complete closure')
    return dict(n=n,tree=tree,edges=edges,selected=selected,points=points,t=t,u=u)

def discover(g,v,b,c):
    points=bytearray(v);lookup={v:0};t=bytearray(I);u=bytearray(I)
    tree=bytearray(b'\xff\xff\xff');edges=bytearray();head=0
    c.update(tree_vertices_verified=1,closure_edges_verified=0)
    while head<len(lookup):
        for label in range(3):
            b.tick();image=b.image(at(points,head,7),g[label]);y=lookup.get(image)
            if y is None:
                if len(lookup)==MAX_ORBIT:raise Incomplete('point orbit exceeds9240: no finite-end certificate')
                y=len(lookup);lookup[image]=y;points.extend(image);put2(tree,head);tree.append(label)
                t.extend(b.multiply(at(t,head,49),g[label]));u.extend(b.multiply(g[label],at(u,head,49)))
                c['tree_vertices_verified']+=1
            put2(edges,y);c['closure_edges_verified']+=1
        head+=1
    n=len(lookup);need(len(edges)==6*n,'all discovered point orbit edges complete')
    return dict(n=n,tree=tree,edges=edges,points=points,t=t,u=u,selected=[])

def edge_loop(g,data,e,b):
    x,label=divmod(e,3);y=get2(data['edges'],e)
    need(0<=x<data['n']and y<data['n'],'literal complete orbit edge')
    return b.multiply(b.multiply(at(data['t'],x,49),g[label]),at(data['u'],y,49))

def close_K(generators,v,b,c):
    """Exact finite monoid closure; derived invertible generators make a group."""
    c.update(K_closure_complete=False,K_current_pass_edges=0,K_distinct_prefix=1)
    for a in generators:need(b.image(v,a)==v,'every chosen actual Schreier loop fixes the exact seed')
    matrices=[I];index={I:0};head=0;work=0
    while head<len(matrices):
        for a in generators:
            image=b.multiply(matrices[head],a);work+=1;c['K_current_pass_edges']=work
            if image not in index:
                if len(matrices)==MAX_K:
                    c.update(K_distinct_prefix=MAX_K,K_current_pass_edges=work)
                    raise Incomplete('stabilizer subgroup closure exceeds2048: no order')
                index[image]=len(matrices);matrices.append(image);c['K_distinct_prefix']=len(matrices)
        head+=1
    c.update(K_distinct_prefix=len(matrices),K_current_pass_edges=work,K_closure_complete=True)
    return index

def consume(g,v,cert,b,c):
    involutions(g,b);data=reconstruct(g,v,cert,b,c)
    generators=[edge_loop(g,data,e,b)for e in data['selected']]
    K=close_K(generators,v,b,c);c.update(Schreier_loops_verified=0,K_generator_count=len(generators))
    for e in range(3*data['n']):
        loop=edge_loop(g,data,e,b)
        need(loop in K,'EVERY original generator Schreier loop is in the closed actual K')
        c['Schreier_loops_verified']+=1
    n=data['n'];need(c['Schreier_loops_verified']==3*n,'complete all-edge stabilizer membership coverage')
    return dict(status='VERIFIED_FINITE_MATRIX_SUBGROUP_ORDER_ONLY',orbit_size=n,stabilizer_order=len(K),
        subgroup_order=n*len(K),K_generator_count=len(generators),full_Schreier_loops=3*n,
        original_group_or_IP_authority=False,original_case_credit=0)

def produce(g,v,b,c):
    involutions(g,b);data=discover(g,v,b,c);K={I:0};generators=[];selected=[]
    c.update(Schreier_loops_verified=0,K_generator_count=0,K_closure_complete=True,K_distinct_prefix=1,K_current_pass_edges=0)
    for e in range(3*data['n']):
        loop=edge_loop(g,data,e,b)
        if loop not in K:
            if len(selected)==MAX_GENERATORS:raise Incomplete('sixteen stabilizer generators exhausted: no certificate')
            selected.append(e);generators.append(loop);c['K_generator_count']=len(generators);K=close_K(generators,v,b,c)
        c['Schreier_loops_verified']+=1
    cert=encode(data['tree'],data['edges'],selected)
    return cert,dict(status='SUPPLIED_COMPLETE_SCHREIER_CERTIFICATE_UNADOPTED',orbit_size=data['n'],
        stabilizer_order_proposal=len(K),subgroup_order_proposal=data['n']*len(K),
        original_group_or_IP_authority=False,original_case_credit=0)

# Positive central-involution certificates; no new subgroup-order conclusion.
def central_data(g,v,cert,b,c):
    involutions(g,b);data=reconstruct(g,v,cert,b,c)
    generators=[edge_loop(g,data,e,b)for e in data['selected']]
    K=close_K(generators,v,b,c)
    c.update(K_generator_count=len(generators),all_Schreier_loops_rechecked=False,
        subgroup_order_issued=False)
    return data,list(K)

def signed_targets(data,v,b):
    b.scalar(7);minus=bytes((-x)%11 for x in v)
    targets=[0]
    for index in range(data['n']):
        b.tick()
        if at(data['points'],index,7)==minus:
            need(index!=0,'nonzero seed differs from its negative');targets.append(index);break
    return targets

def central_involution(g,z,b):
    if z==I or b.multiply(z,z)!=I:return False
    for mark in g:
        if b.multiply(z,mark)!=b.multiply(mark,z):return False
    return True

def central_witness(g,v,data,members,certificate,b):
    need(type(certificate)is dict and set(certificate)=={'K_index','target_point_index'},
        'exact positive central-involution witness')
    index=certificate['K_index'];target=certificate['target_point_index']
    need(type(index)is int and 0<=index<len(members),'actual reconstructed K member index')
    need(type(target)is int and 0<=target<data['n'],'actual reached target point index')
    need(target in signed_targets(data,v,b),'target is the seed or its reached negative')
    z=b.multiply(members[index],at(data['t'],target,49))
    need(central_involution(g,z,b),'nonidentity involution commuting with ALL three marks')
    need(b.image(v,z)==at(data['points'],target,7),'fresh right-coset signed seed image')
    return z

def supply_central(g,v,orbit_certificate,b,c):
    data,members=central_data(g,v,orbit_certificate,b,c)
    targets=signed_targets(data,v,b);c.update(signed_target_count=len(targets),
        candidates_tested=0,positive_witness_verified=False)
    for target in targets:
        for index,member in enumerate(members):
            b.tick();z=b.multiply(member,at(data['t'],target,49));c['candidates_tested']+=1
            if central_involution(g,z,b):
                need(b.image(v,z)==at(data['points'],target,7),'fresh positive right-coset image')
                c['positive_witness_verified']=True
                return dict(K_index=index,target_point_index=target)
    return None

def consume_central(g,v,orbit_certificate,certificate,b,c):
    data,members=central_data(g,v,orbit_certificate,b,c)
    z=central_witness(g,v,data,members,certificate,b)
    c.update(positive_witness_verified=True,K_member_index=certificate['K_index'],
        target_point_index=certificate['target_point_index'])
    return z
