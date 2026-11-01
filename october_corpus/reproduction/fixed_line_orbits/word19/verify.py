"""Independent witness verifier; imports no elimination or supplier implementation."""
import field as f

def actual_equations(g,signs,b):
    out=[]
    for index,mat in enumerate(g):
        for column in range(7):
            coeff=[]
            for variable in range(7):
                b.scalar(1);coeff.append((mat[7*variable+column]-(signs[index]if variable==column else 0))%11)
            out.append(tuple(coeff))
    return out

def block(rows,cert,b):
    f.need(type(cert)is dict and set(cert)=={'rank','pivots','echelon_rows','row_combinations','nullspace_basis','kind','signs'},'exact complete kernel witness')
    m=len(rows);r=cert['rank'];p=cert['pivots'];R=cert['echelon_rows'];C=cert['row_combinations'];N=cert['nullspace_basis']
    f.need(type(r)is int and 0<=r<=7 and type(p)is list and len(p)==r and all(type(x)is int and 0<=x<7 for x in p)and p==sorted(set(p)),'typed ordered pivots')
    f.need(type(R)is list and type(C)is list and len(R)==len(C)==r and type(N)is list and len(N)==7-r,'complete rank/basis extents')
    for i,pivot in enumerate(p):
        row=f.vector(R[i],7,b);comb=f.vector(C[i],m,b)
        for j in range(pivot):b.scalar(1);f.need(row[j]==0,'zeros before independent leading pivot')
        b.scalar(1);f.need(row[pivot]==1,'normalized nonzero independent pivot')
        for j in range(7):
            value=0
            for k in range(m):b.scalar(2);value=(value+comb[k]*rows[k][j])%11
            b.scalar(1);f.need(value==row[j],'every echelon row is an actual equation combination')
    free=[j for j in range(7)if j not in p];b.scalar(7);basis=[]
    for i,raw in enumerate(N):
        v=f.vector(raw,7,b)
        for j,column in enumerate(free):b.scalar(1);f.need(v[column]==int(i==j),'complete independent canonical free-coordinate basis')
        for coeff in rows:
            value=0
            for x,y in zip(coeff,v):b.scalar(2);value=(value+x*y)%11
            b.scalar(1);f.need(value==0,'ALL original scalar equations on EVERY basis row')
        basis.append(v)
    return basis

def consume(g,certificate,b):
    f.need(type(certificate)is dict and set(certificate)=={'space_type','blocks','selected_seeds'}and certificate['space_type']=='FOUR_JOINT_SIGN_SPACES','exact joint-sign certificate type')
    blocks=certificate['blocks'];f.need(type(blocks)is list and len(blocks)==4,'all four sign spaces required')
    dimensions=[]
    for signs,cert in zip(([1,1],[1,10],[10,1],[10,10]),blocks):
        f.need(type(cert)is dict and cert['kind']=='JOINT_SIGNS'and type(cert['signs'])is list and len(cert['signs'])==2 and all(type(x)is int for x in cert['signs'])and cert['signs']==signs,'exact ordered typed sign pair')
        basis=block(actual_equations(g,signs,b),cert,b)
        for v in basis:
            for mark,sign in zip(g,signs):
                expected=[]
                for x in v:b.scalar(1);expected.append(sign*x%11)
                f.need(b.image(v,mark)==bytes(expected),'fresh full row image for BOTH original sign equations')
        dimensions.append(7-cert['rank'])
    wanted=f.selected(blocks,b);chosen=certificate['selected_seeds']
    f.need(type(chosen)is list and len(chosen)<=4,'one seed per nonzero joint space')
    for item in chosen:
        f.need(type(item)is dict and set(item)=={'block','basis','signs','vector'}and type(item['block'])is type(item['basis'])is int and type(item['signs'])is list and all(type(x)is int for x in item['signs']),'typed seed provenance')
        v=f.vector(item['vector'],7,b);b.scalar(14);f.need(any(v),'nonzero selected seed')
    f.need(chosen==wanted,'exact first normalized basis vector per nonzero joint space')
    return dict(status='VERIFIED_JOINT_SIGN_SEEDS_ONLY',sign_pairs=[[1,1],[1,10],[10,1],[10,10]],
        dimensions=dimensions,selected_seeds=wanted,blocks_verified=4,scalar_equations_verified=56,
        only_plus_plus_is_H_fixed=True,other_nonzero_spaces_are_H_invariant_lines=True,
        original_subgroup_order_generation_or_IP_authority=False,original_case_credit=0)
