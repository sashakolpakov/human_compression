"""Complete tree-conjugation equations for reusable Original D maps."""
import struct
import common as C
MAGIC=b'L026DFM1'
HEADER=14
WIDTH=16
def frame(K,raw,work,n=3510,root=2961):
    ctx=K.decode_operands(raw,work,n,root);nodes=[]
    for i in range(n):
        vertex,parent,label=struct.unpack_from('<HHb',raw,8+10*n+5*i)
        if i:
            work.charge(3,'whole actual bridge edge')
            C.need(action(ctx,label)[nodes[parent][0]]==vertex,'actual original bridge parent-point image')
        nodes.append((vertex,parent,label))
    material=b'L026DFK1'+struct.pack('<HH',n,root)+raw[8:8+2*n]+raw[8+6*n:8+10*n]+raw[8+10*n:];work.charge(len(material),'whole globally keyed original frame hash');key=C.digest(material)
    return ctx,nodes,key
def action(ctx,label):return ctx['ambient'][label-1 if label>0 else 1-label]
def vector(raw,n,work):
    C.need(type(raw)is bytes and len(raw)==2*n,'whole native-u16 map');a=struct.unpack('<'+'H'*n,raw);seen=bytearray(n)
    for x in a:
        work.charge(4,'complete selected map range/bijection');C.need(x<n and not seen[x],'whole actual bijection');seen[x]=1
    return a
def header(raw,n,nodes):
    C.need(type(raw)is bytes and len(raw)>=14 and raw[:8]==MAGIC,'complete cache header')
    degree,begin,count=struct.unpack_from('<HHH',raw,8)
    C.need(degree==n and begin%16==0 and 0<=begin<n and count==min(16,n-begin)and len(raw)==14+count*(2+2*n),'exact complete native chunk extent')
    for j in range(count):C.need(struct.unpack_from('<H',raw,14+j*(2+2*n))[0]==nodes[begin+j][0],'original vertex in exact bridge order')
    return begin,count
def selected(raw,ordinal,n,nodes,work):
    begin,count=header(raw,n,nodes);C.need(begin<=ordinal<begin+count,'actual parent map in declared chunk')
    offset=14+(ordinal-begin)*(2+2*n)+2;return vector(raw[offset:offset+2*n],n,work)
def encode(n,begin,nodes,maps,work):
    out=bytearray(MAGIC+struct.pack('<HHH',n,begin,len(maps)))
    for j,a in enumerate(maps):out.extend(struct.pack('<H',nodes[begin+j][0]));out.extend(struct.pack('<'+'H'*n,*a))
    work.charge(len(out),'whole native carrier encode');C.need(len(out)<=131072,'single128KiB native output');return bytes(out)
def compute(ctx,nodes,begin,parent_files,work,saved=None):
    n=ctx['n'];C.need(type(begin)is int and 0<=begin<n and begin%16==0,'sixteen aligned bridge-ordinal interval');end=min(begin+16,n)
    needed=sorted({(nodes[i][1]//16)*16 for i in range(begin,end)if i and nodes[i][1]<begin})
    C.need(type(parent_files)is dict and sorted(parent_files)==needed and len(needed)<=16,'all and only earlier parent chunks')
    for first,raw in parent_files.items():C.need(header(raw,n,nodes)[0]==first and first<begin,'honest earlier parent chunk')
    if saved is not None:C.need(header(saved,n,nodes)==(begin,end-begin),'strict exact proposed interval')
    cache={};maps=[];rows=[]
    for i in range(begin,end):
        vertex,parent,label=nodes[i]
        if i==0:expected=ctx['d0']
        else:
            if parent>=begin:pmap=maps[parent-begin]
            else:
                if parent not in cache:cache[parent]=selected(parent_files[(parent//16)*16],parent,n,nodes,work)
                pmap=cache[parent]
            forward,back=action(ctx,label),action(ctx,-label);expected=[]
            for x in range(n):work.charge(6,'entire child inverse-parent-forward conjugation');expected.append(forward[pmap[back[x]]])
            expected=tuple(expected)
        work.charge(4*n,'whole individual native map pack and digest');native=struct.pack('<'+'H'*n,*expected);a=vector(native,n,work)
        moved=False
        for x,y in enumerate(a):work.charge(4,'fresh whole involution/nonidentity');C.need(a[y]==x,'whole D involution');moved=moved or y!=x
        C.need(moved,'nonidentity D map')
        if saved is not None:C.need(selected(saved,i,n,nodes,work)==a,'EVERY saved full map equals original parent conjugate')
        maps.append(a);rows.append(dict(ordinal=i,vertex=vertex,parent_ordinal=None if i==0 else parent,label=label,map_sha256=C.digest(native)))
    raw=encode(n,begin,nodes,maps,work)
    if saved is not None:C.need(raw==saved,'whole strict native carrier byte equality')
    return raw,rows,needed
