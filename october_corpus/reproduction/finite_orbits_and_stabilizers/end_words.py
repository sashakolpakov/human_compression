"""Two actual endpoint words and complete middle nonmembership; no SGS import."""
import runtime as rt
import field,algebra
LEFT_MAX=60000
RIGHT_MAX=64
POWERS=(1,2,3,5,11)
def verify(marks,left,right,power,b):
    g=algebra.marking(marks,b)
    rt.need(type(left)is list and 1<=len(left)<=LEFT_MAX and all(type(j)is int and j in(0,1,2)for j in left),'bounded actual LEFT word only')
    rt.need(type(right)is list and 1<=len(right)<=RIGHT_MAX and all(type(j)is int and j in(1,2,3)for j in right),'bounded actual RIGHT word only')
    rt.need(type(power)is int and power in POWERS,'finite declared positive RIGHT power')
    b.scalar(len(left)+len(right)+1);x=y=field.I
    for j in left:x=b.multiply(x,g[j])
    for j in right:y=b.multiply(y,g[j])
    z=field.I
    for _ in range(power):z=b.multiply(z,y)
    rt.need(x==z,'fresh full LEFT word equals actual RIGHT word power')
    middle=algebra.dihedral(g[1],g[2],b,cap=256)
    rt.need(middle is not None,'complete bounded middle required; no partial nonmembership')
    rt.need(x!=field.I and x not in middle[1],'common matrix outside COMPLETE middle')
    return dict(status='VERIFIED_MATRIX_INTERSECTION_PROPERTY_FAILURE_BY_TWO_END_WORDS',LEFT_member=True,RIGHT_member=True,outside_complete_middle=True,concrete_matrix_group_intersection_property=False,LEFT_word_length=len(left),RIGHT_word_length=len(right),RIGHT_positive_power=power,middle_order=len(middle[1]),middle_rotation_order=middle[0],whole_H_SGS_or_order_replayed=False,complete_RIGHT_subgroup_or_order_claimed=False,named_type_or_GEN_claimed=False,Original_identity_transfer_verified=False,new_case_or_census_credit=0)
