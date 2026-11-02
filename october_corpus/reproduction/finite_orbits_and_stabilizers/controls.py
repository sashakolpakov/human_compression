"""Original33 arithmetic controls literal; eight new portable admission fixtures."""
import sys,struct
import runtime as rt
import field,algebra,solve,schreier
import verify as api

def permutation(swaps,b):
    p=list(range(7))
    for i,j in swaps:p[i],p[j]=p[j],p[i]
    b.scalar(49);return bytes(int(p[i]==j)for i in range(7)for j in range(7))

def generic19(b):
    # Constant0 cubics have root0. For a0!=0, test only the other10 points.
    for a2 in range(11):
        for a1 in range(11):
            for a0 in range(1,11):
                irreducible=True
                for x in range(1,11):
                    b.scalar(5)
                    if(((x+a2)*x+a1)*x+a0)%11==0:irreducible=False;break
                if not irreducible:continue
                C=algebra.rows(field.I);C[0][:3]=[0,1,0];C[1][:3]=[0,0,1]
                b.scalar(3);C[2][:3]=[(-a0)%11,(-a1)%11,(-a2)%11];x=bytes(t for row in C for t in row)
                U=field.I;e=70
                while e:
                    if e&1:U=b.multiply(U,x)
                    e//=2
                    if e:x=b.multiply(x,x)
                if U!=field.I:return U
    raise ValueError('finite generic cubic fixture unavailable')

def main(argv):
    b,parsed_options,pins=api.start(argv,True);api.origin(sys.modules[__name__],'controls.py');names=[]
    def yes(name,ok):rt.need(ok,name);names.append(name)
    def no(name,call,exception=ValueError,contains=None):
        try:call()
        except exception as e:
            rt.need(contains is None or contains in str(e),'expected exact refusal branch');names.append(name);return
        raise ValueError('unrefused '+name)
    def changed(raw,offset,value,width=1):
        a=bytearray(raw);a[offset:offset+width]=int(value).to_bytes(width,'little');return bytes(a)
    def node_base(raw):return 19+2*raw[11]+2*raw[10]+raw[10]*raw[11]
    a=permutation([(0,1),(2,3)],b);c=permutation([(0,1),(3,4)],b);d=permutation([(0,1),(2,4)],b)
    g=(a,c,d);v=bytes([1,0,0,0,0,0,0]);raw,claimed,tables=schreier.build(g,v,b)
    facts,seed=schreier.check(g,raw,b)
    yes('S3_complete_order6_with_stabilizer3',facts['exact_end_order']==6 and facts['orbit_size']==2 and facts['stabilizer_size']==3)
    nb=node_base(raw);h=b.multiply(c,a);h2=b.multiply(h,h)
    rt.need(b.multiply(a,h2)==c and b.multiply(h2,a)!=c,'noncentral S3 right-versus-left orientation witness')
    no('right_factor_orientation_refused',lambda:schreier.check(g,changed(raw,nb+8,2),b),contains='left-factor')
    vg=(permutation([(0,1)],b),permutation([(2,3)],b),permutation([(4,5)],b))
    vr,vc,vt=schreier.build(vg,v,b);vf,_=schreier.check(vg,vr,b)
    yes('noncyclic_V4_leaf_gives_group_order8',vf['exact_end_order']==8 and vf['stabilizer_size']==4 and vf['stabilizer_generators']==2)
    yes('omitted_actual_group_member_verified',schreier.member(v,*vt,vg[0],b))
    yes('orbit_preserving_nonmember_rejected_by_full_matrix_coset',not schreier.member(v,*vt,permutation([(5,6)],b),b))
    yes('omitted_outside_orbit_is_nonmember',not schreier.member(v,*vt,permutation([(0,6)],b),b))
    no('finite_orbit_cap_is_inconclusive',lambda:schreier.build(g,v,b,ncap=1),schreier.Inconclusive)
    no('finite_leaf_cap_is_inconclusive',lambda:schreier.build(g,v,b,scap=2),schreier.Inconclusive)
    no('wrong_magic_refused',lambda:schreier.decode(b'WRONG001'+raw[8:],b))
    no('truncated_carrier_refused',lambda:schreier.decode(raw[:-1],b))
    no('trailing_carrier_refused',lambda:schreier.decode(raw+b'\0',b))
    no('zero_seed_refused',lambda:schreier.decode(raw[:12]+bytes(7)+raw[19:],b))
    no('late_orbit_parent_refused',lambda:schreier.decode(changed(raw,nb+12,1,2),b))
    no('outside_orbit_tree_label_refused',lambda:schreier.decode(changed(raw,nb+14,3),b))
    r3,_,_=schreier.build(g,bytes([0,0,1,0,0,0,0]),b);nb3=node_base(r3)
    no('duplicate_full_orbit_row_refused',lambda:schreier.check(g,changed(r3,nb3+24+2,0),b),contains='distinct')
    no('orbit_edge_target_outside_extent_refused',lambda:schreier.decode(changed(raw,nb+3,2,2),b))
    no('orbit_edge_S_index_outside_extent_refused',lambda:schreier.decode(changed(raw,nb+5,3),b))
    no('wrong_full_Schreier_equation_refused',lambda:schreier.check(g,changed(raw,nb+8,0),b),contains='left-factor')
    no('S_generator_edge_outside_extent_refused',lambda:schreier.decode(changed(raw,19,6,2),b))
    no('duplicate_S_generator_edge_refused',lambda:schreier.decode(changed(vr,21,int.from_bytes(vr[19:21],'little'),2),b))
    st=19+2*raw[11]
    no('late_S_parent_refused',lambda:schreier.decode(changed(raw,st+2,1),b))
    no('outside_S_tree_label_refused',lambda:schreier.decode(changed(raw,st+3,raw[11]),b))
    table=st+2*raw[10]
    no('wrong_S_generator_closure_target_refused',lambda:schreier.check(g,changed(raw,table,0),b),contains='multiplication closed')
    badleaf=schreier.encode(v,[0],[(255,255),(0,0)],bytes([1,0]),
        [(65535,255,[(0,0)]*3),(0,0,[(0,0)]*3)],b)
    no('nonfixing_Schreier_leaf_refused',lambda:schreier.check(g,badleaf,b),contains='fixes seed')
    X=[[0]*7 for _ in range(7)]
    for offset in(0,3):
        X[offset][offset+1]=1;X[offset+1][offset+2]=1;X[offset+2][offset:offset+3]=[1,9,10]
    X[6][6]=1;flat=bytes(x for row in X for x in row);generic=(field.I,flat,field.I,field.I)
    Y=schreier.prime_value(generic,[1],7,[1,2,3],b)
    yes('fresh_generic_order19_and_rank6',Y!=field.I and len(schreier.fixed_basis(Y,b))==1)
    no('identity_prime_word_refused',lambda:schreier.prime_value(generic,[2],1,[1,2,3],b))
    marks=[algebra.rows(permutation([(i,i+1)],b))for i in range(4)];marks[0][0][0]=True
    no('Original_boolean_matrix_refused',lambda:algebra.marking(marks,b))
    limited=rt.Budget();limited.products=400000
    no('hard_complete_product_cap_before_arithmetic',lambda:limited.multiply(field.I,field.I),rt.Limit)
    root=struct.pack('<HBHBHBHB',65535,255,0,0,0,0,0,0)
    child=struct.pack('<HBHBHBHB',0,0,0,0,0,0,0,0)
    maximum=schreier.MAGIC+struct.pack('<HBB',10000,128,8)+v+b''.join(struct.pack('<H',i)for i in range(8))+bytes([255,255])+bytes(254)+bytes(1024)+root+9999*child
    yes('maximum121315_byte_codec_admitted_only_as_structure',len(maximum)==121315 and len(schreier.decode(maximum,b)[4])==10000)
    no('production10001_node_codec_refused',lambda:schreier.decode(changed(maximum,8,10001,2),b))
    no('noncanonical_seed_refused',lambda:schreier.decode(changed(raw,12,11),b))
    no('boolean_Original_word_letter_refused',lambda:schreier.prime_value(generic,[True],7,[1,2,3],b))
    U=generic19(b);Ui=U
    for _ in range(17):Ui=b.multiply(Ui,U)
    Z=[[0]*7 for _ in range(7)];Z[6][6]=1;b.scalar(49)
    for i in range(3):
        for j in range(3):Z[i][j]=U[7*i+j];Z[i+3][j+3]=Ui[7*i+j]
    Y=bytes(t for row in Z for t in row);A=permutation([(0,3),(1,4),(2,5)],b)
    B=b.multiply(A,Y);C=b.multiply(A,b.multiply(Y,Y));g19=(A,B,C)
    fresh=schreier.prime_value(g19,[0,1],1,[0,1,2],b)
    r19,_,_=schreier.build(g19,bytes([0,0,0,0,0,0,1]),b);f19,_=schreier.check(g19,r19,b)
    yes('generic_prime19_rank6_noncyclic_D38_leaf',fresh==Y and len(schreier.fixed_basis(Y,b))==1
        and f19['orbit_size']==1 and f19['stabilizer_size']==38 and f19['exact_end_order']==38)
    rt.need(len(names)==len(set(names))==33,'all33 new Original-free controls')
    portable=[]
    def refuse(name,call):
        try:call()
        except ValueError:portable.append(name);return
        raise ValueError('portable refusal expected')
    import copy
    fixture=dict(schema='F004_FINITE_ORBIT_CASE_V1',original_job=[20,4],position=1,original_row_id='generic',marks=[],word=[0],cofactor=1,end_labels=[0,1,2],carrier=dict(path='data/generic.bin',bytes=19,sha256='0'*64),expected=dict(orbit_size=1,stabilizer_size=1,exact_end_order=1,omitted_mark_in_certified_end=False,fixed_space_dimension=1),provenance={},external_premises='Generic header only; no model authority')
    rt.need(api.header(fixture)==fixture,'portable header');portable.append('portable_complete_header_only')
    x=copy.deepcopy(fixture);x['position']=True;refuse('portable_boolean_position_refused',lambda:api.header(x))
    x=copy.deepcopy(fixture);x['carrier']['path']='/absolute.bin';refuse('portable_absolute_carrier_refused',lambda:api.header(x))
    x=copy.deepcopy(fixture);x['carrier']['path']='../escape.bin';refuse('portable_parent_carrier_refused',lambda:api.header(x))
    x=copy.deepcopy(fixture);x['expected']['orbit_size']=True;refuse('portable_boolean_expectation_refused',lambda:api.header(x))
    x=copy.deepcopy(fixture);x['word']=[True];refuse('portable_boolean_word_refused',lambda:api.header(x))
    refuse('portable_duplicate_JSON_refused',lambda:rt.decode(b'{"a":1,"a":2}'))
    refuse('portable_float_JSON_refused',lambda:rt.decode(b'{"a":1.0}'))
    rt.need(len(portable)==8,'eight portable admission controls');api.close(b)
    proof=dict(schema='F004_FINITE_ORBIT_PORTABLE_CONTROLS_V1',status='PASS',arithmetic_count=33,arithmetic_names=names,portable_count=8,portable_names=portable,Source=pins,counts=b.snapshot(),Original_calls=0,no_case_or_classification_credit=True)
    outputs=api.emit(parsed_options.output,dict(status='PASS',arithmetic_count=33,portable_count=8,Original_calls=0),proof,b)
    sys.stdout.buffer.write(rt.encoded(dict(status='PASS',arithmetic_count=33,portable_count=8,outputs=outputs)))

if __name__=='__main__':main(sys.argv)
