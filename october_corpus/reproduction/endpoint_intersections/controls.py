"""Original-free arithmetic and refusal controls; no G2(11) case is admitted."""
import argparse
import base64
import copy
import sys
import verify as v

def run(b,sc):
    b.scalar(4096);names=[]
    def yes(name,condition):v.need(condition,name);names.append(name)
    def no(name,call):
        try:call()
        except(ValueError,KeyError):names.append(name);return
        raise AssertionError(name)
    I=[[int(i==j)for j in range(7)]for i in range(7)]
    def diagonal(indices):
        return [[(10 if i in indices else 1)if i==j else 0 for j in range(7)]for i in range(7)]
    def swap(i,j):
        p=list(range(7));p[i],p[j]=p[j],p[i]
        return [[int(k==p[r])for k in range(7)]for r in range(7)]
    raw=[swap(0,1),diagonal({0}),diagonal({2}),diagonal({3})]
    marks=v.original_marks(raw,b,sc)
    yes('four_actual_involutions_and_string_Klein_four',len(set(marks))==4)
    bad=copy.deepcopy(raw);bad[0]=diagonal({0})
    no('duplicate_original_mark_refused',lambda:v.original_marks(bad,b,sc))
    bad=copy.deepcopy(raw);bad[2]=swap(1,2)
    no('noncommuting_original_AC_refused',lambda:v.original_marks(bad,b,sc))
    bad=copy.deepcopy(raw);bad[0][0][0]=True
    no('Boolean_field_coordinate_refused',lambda:v.original_marks(bad,b,sc))
    a=v.matrix(diagonal({3,4,5,6}),b,sc);c=v.matrix(diagonal({1,2,5,6}),b,sc)
    blocks=[dict(signs=list(signs),basis=[I[i]for i in indices])
        for signs,indices in(((1,1),(0,)),((1,10),(1,2)),((10,1),(3,4)),((10,10),(5,6)))]
    yes('four_complete_rational_sign_spaces',len(v.complete_AC(blocks,a,c,b,sc))==4)
    bad=copy.deepcopy(blocks);bad[1]['basis'][1]=bad[1]['basis'][0]
    no('proportional_two_dimensional_basis_refused',lambda:v.complete_AC(bad,a,c,b,sc))
    bad=copy.deepcopy(blocks);bad[1]['basis'][0]=I[5]
    no('wrong_actual_sign_basis_refused',lambda:v.complete_AC(bad,a,c,b,sc))
    yes('projective_normalization_identifies_scalar_multiples',
        v.normalized(bytes((2,4,0,0,0,0,0)),b)==v.normalized(bytes((1,2,0,0,0,0,0)),b))
    mixed=bytes((1,0,0,0,0,1,0))
    no('mixed_joint_sign_root_refused',lambda:v.joint_sign(mixed,a,c,b))
    permutation=lambda f:[[int(j==f(i))for j in range(7)]for i in range(7)]
    left=sc.marks([permutation(lambda i:-i%7),permutation(lambda i:(1-i)%7),I],b)
    A=[I[i]for i in(0,1,6,2,5,3,4)]
    cert=dict(kind='FULL_CYCLIC_SPAN_MATRIX_ALGEBRA_ONLY',dimension=7,basis=A,
        right_inverse=list(map(list,zip(*A))),parent_edges=[[i,1-i%2]for i in range(6)],
        nongeneration_claim=False,ambient_generation_claim=False,IP_claim=False)
    yes('D14_seven_actual_word_rows_span',v.cyclic_basis(cert,left,b,sc)==bytes(I[0]))
    bad=copy.deepcopy(cert);bad['right_inverse'][0][0]=0
    no('wrong_full_rank_inverse_refused',lambda:v.cyclic_basis(bad,left,b,sc))
    bad=copy.deepcopy(cert);bad['parent_edges'][0][0]=1
    no('future_cyclic_parent_refused',lambda:v.cyclic_basis(bad,left,b,sc))
    bad=copy.deepcopy(cert);bad['parent_edges'][0][1]=True
    no('Boolean_cyclic_label_refused',lambda:v.cyclic_basis(bad,left,b,sc))
    no('incomplete37_line_domain_refused',lambda:v.left_irreducible(blocks,[],(a,a,c),b,sc))
    point_marks=sc.marks([diagonal({4}),swap(0,1),diagonal({5})],b)
    tree=dict(n=2,parent_tree_b64=base64.b64encode(bytes((255,255,255,0,0,1))).decode('ascii'))
    fact=v.point_prefix(I[0],tree,point_marks,b,sc,2)
    yes('C2_cubed_small_point_prefix_lower_bound8',fact['group_order_lower_bound']==8)
    bad=dict(n=2,parent_tree_b64=base64.b64encode(bytes((255,255,255,1,0,1))).decode('ascii'))
    no('future_point_parent_refused',lambda:v.point_prefix(I[0],bad,point_marks,b,sc,2))
    duplicate=dict(n=3,parent_tree_b64=base64.b64encode(bytes((255,255,255,0,0,1,0,0,1))).decode('ascii'))
    no('duplicate_full_point_refused',lambda:v.point_prefix(I[0],duplicate,point_marks,b,sc,3))
    no('seed_not_fixed_by_AC_refused',lambda:v.point_prefix(I[4],tree,point_marks,b,sc,2))
    no('trailing_tree_payload_refused',lambda:v.point_prefix(I[0],dict(tree,parent_tree_b64=tree['parent_tree_b64']+'AAAA'),point_marks,b,sc,2))
    rotation=sc.marks([I,diagonal({0}),swap(0,1)],b)
    yes('D8_actual_bc_cubed_order4_and_middle_bound24',
        v.middle_order_four([1,2,1,2,1,2],rotation,b,sc)['exact_word_order']==4)
    no('wrong_word_shape_refused',lambda:v.middle_order_four([1,2],rotation,b,sc))
    no('Boolean_word_label_refused',lambda:v.middle_order_four([True,2,1,2,1,2],rotation,b,sc))
    commuting=sc.marks([I,diagonal({0}),diagonal({1})],b)
    no('order2_word_refused',lambda:v.middle_order_four([1,2,1,2,1,2],commuting,b,sc))
    right=sc.marks([swap(0,1),swap(1,2),swap(0,2)],b);seed=sc.seed(I[0],b)
    orbit,_=sc.produce(right,seed,b,{});fact=sc.consume(right,seed,orbit,b,{})
    yes('S3_complete_Schreier_order6',fact['orbit_size']==3 and fact['stabilizer_order']==2
        and fact['full_Schreier_loops']==9 and fact['subgroup_order']==6)
    bad=copy.deepcopy(orbit);bad['K_generator_edges']=[]
    no('unpaid_Schreier_loop_refused',lambda:sc.consume(right,seed,bad,b,{}))
    no('duplicate_JSON_key_refused',lambda:v.decode(b'{"n":1,"n":2}'))
    no('noninteger_JSON_number_refused',lambda:v.decode(b'{"n":1e999}'))
    no('JSON_trailing_bytes_refused',lambda:v.decode(b'{}{}'))
    before=(b.linear,b.products,b.rows)
    try:b.scalar(200000-b.linear+1)
    except v.Limit:pass
    else:raise AssertionError('scalar limit must refuse before overflow')
    yes('one_live_scalar_bank_refuses_before_overflow',before==(b.linear,b.products,b.rows))
    return names

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-sha256',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args(argv);b=v.Budget();sc,sources=v.load_sources(args.source_sha256,b)
    names=run(b,sc);b.close_inputs()
    result=dict(status='PASS_GENERIC_INTERSECTION_COMPONENT_CONTROLS_ONLY',count=len(names),counts=b.snapshot(),original_case_credit=0)
    proof=dict(checks=names,Sources=sources,original_inputs_opened=False,original_case_credit=0)
    print(v.encoded(dict(status='PASS',outputs=v.emit(args.out,result,proof,b))).decode())

if __name__=='__main__':
    try:main()
    except Exception as error:
        print(v.encoded(dict(status='FAIL_CLOSED_UNPAID',error=str(error))).decode(),file=sys.stderr);raise SystemExit(1)
