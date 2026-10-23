"""Byte-exact selected project definitions; see provenance/source_derivation.json.
No original host paths or project runtime are imported.
"""

def need(value,reason):
    if not value:raise ValueError(reason)

class Arithmetic:
    """The ADOPTED GF8 exponent tables; never an invented polynomial codec."""
    def __init__(self,codec,charge):
        need(callable(charge),'one actual shared budget callback')
        need(type(codec)is dict and codec['schema']=='F004_GF8_EXPONENT_CODEC_V1'
             and type(codec['zero'])is int and codec['zero']==0
             and type(codec['one'])is int and codec['one']==1,'accepted codec roles')
        for key in('addition','multiplication'):
            x=codec[key]
            need(type(x)is list and len(x)==8 and all(type(r)is list and len(r)==8
                 and all(type(v)is int and 0<=v<8 for v in r)for r in x),'whole typed8x8 field table')
        self.add=codec['addition'];self.multiply=codec['multiplication'];self.charge=charge
        self.identity=tuple(int(i==j)for i in range(6)for j in range(6))
        self.j=tuple(int(i+j==5)for i in range(6)for j in range(6))
        charge(0)

    def flat(self,matrix):
        need(type(matrix)is list and len(matrix)==6 and all(type(r)is list and len(r)==6
             and all(type(v)is int and 0<=v<8 for v in r)for r in matrix),'whole typed6x6 matrix')
        return tuple(x for row in matrix for x in row)

    def literal(self,matrix):
        need(type(matrix)is list and len(matrix)==36 and all(type(v)is int and 0<=v<8 for v in matrix),'whole36-code row')
        return tuple(matrix)

    def product(self,left,right):
        out=[]
        for i in range(6):
            self.charge(1) # One bounded six-coordinate row action, in the shared budget.
            for j in range(6):
                x=0
                for k in range(6):x=self.add[x][self.multiply[left[6*i+k]][right[6*k+j]]]
                out.append(x)
        self.charge(0)
        return tuple(out)

    def symplectic(self,matrix):
        transpose=tuple(matrix[6*j+i]for i in range(6)for j in range(6))
        need(self.product(self.product(matrix,self.j),transpose)==self.j,'actual determinant-one symplectic image')

def basis(arithmetic,matrices,label):
    need(label in('K','H')and type(matrices)is list and len(matrices)==9,'exact acquired621 K9/H9 order')
    values=[arithmetic.flat(m)for m in matrices]
    for m in values:arithmetic.symplectic(m)
    return values

def check_table(arithmetic,table,matrices,label):
    """Verify ANY topologically word-rooted closed table, without BFS search."""
    need(type(table)is dict and set(table)=={'schema','group','basis_matrices','rows','nonidentity_involution_rows',
         'complete_under_every_basis_generator','max_elements'},'whole table fields')
    gens=basis(arithmetic,matrices,label)
    supplied_basis=table['basis_matrices']
    need(type(supplied_basis)is list and len(supplied_basis)==9
         and [arithmetic.literal(m)for m in supplied_basis]==gens,'entire typed supplied basis')
    need(table['schema']=='F004_Q8_621_COMPLETE_MATRIX_WORD_TABLE_V1'and table['group']==label
         and table['complete_under_every_basis_generator']is True,'exact acquired ordered group basis')
    cap=table['max_elements'];rows=table['rows']
    need(type(cap)is int and 1<=cap<=4096 and type(rows)is list and 1<=len(rows)<=cap,'entire finite supplied table')
    elements=[]
    for i,row in enumerate(rows):
        need(type(row)is dict and set(row)=={'matrix','parent','generator'},'whole word-tree row')
        m=arithmetic.literal(row['matrix'])
        if i==0:
            need(m==arithmetic.identity and row['parent']is None and row['generator']is None,'literal identity root')
        else:
            p,k=row['parent'],row['generator']
            need(type(p)is int and 0<=p<i and type(k)is int and 1<=k<=9,'strictly earlier parent and exact basis index')
            need(m==arithmetic.product(elements[p],gens[k-1]),'actual positive original-basis word product')
        elements.append(m)
    lookup={m:i for i,m in enumerate(elements)}
    need(len(lookup)==len(elements),'all supplied group matrices distinct')
    for m in elements:
        for g in gens:need(arithmetic.product(m,g)in lookup,'EVERY full basis closure edge retained')
    inv=[i for i,m in enumerate(elements)if i and arithmetic.product(m,m)==arithmetic.identity]
    supplied=table['nonidentity_involution_rows']
    need(type(supplied)is list and all(type(x)is int for x in supplied)and supplied==inv,'ALL and ONLY literal nonidentity involutions')
    arithmetic.charge(0)
    return elements,lookup,inv

def check_prefix(arithmetic,fixed,K_generators,H_generators,K,H):
    """Fixed input order [a,e,b]; the full old prefix-IP authority is borrowed."""
    need(type(fixed)is list and len(fixed)==3,'exact original acquired fixed3')
    a,e,b=[arithmetic.flat(m)for m in fixed]
    need(len({a,e,b})==3 and all(m!=arithmetic.identity and arithmetic.product(m,m)==arithmetic.identity for m in(a,e,b)),
         'three distinct nonidentity original involution images')
    commute=lambda x,y:arithmetic.product(x,y)==arithmetic.product(y,x)
    need(commute(a,e)and commute(b,e)and not commute(a,b),'exact original fixed string relations')
    for g in basis(arithmetic,K_generators,'K'):need(commute(g,a)and commute(g,e),'all K generators centralize a,e')
    for g in basis(arithmetic,H_generators,'H'):need(commute(g,a)and commute(g,b),'all H generators centralize a,b')
    need(a in K[1]and e in K[1]and e in H[1],'expected actual fixed memberships in full acquired centralizers')
    arithmetic.charge(0)
    return a,b,e
