"""24 fresh Original-free checks of the actual two-end-word verifier."""
import sys
import runtime as rt
import field,algebra,end_words
import verify_intersection as api
def tensor(a,c,b):
    b.scalar(98)
    return bytes(a[i//2][j//2]*c[i%2][j%2]%11 if i<4 and j<4 else int(i==j)
        for i in range(7)for j in range(7))
def fixtures(b):
    names=[]
    def yes(name,value):rt.need(value,name);names.append(name)
    def no(name,fn):
        try:fn()
        except ValueError:names.append(name);return
        raise ValueError(name)
    I=((1,0),(0,1));A=((1,0),(0,10));X=((0,1),(1,0))
    g=(tensor(A,I,b),tensor(X,I,b),tensor(I,A,b),tensor(I,X,b))
    marks=[algebra.rows(x)for x in g];left=[0,1,0,1];right=[2,3]
    def run(l=left,r=right,p=2,m=None):return end_words.verify(marks if m is None else m,l,r,p,b)
    v=run();yes('fresh_actual_both_end_words_positive',v['LEFT_member']is v['RIGHT_member']is v['outside_complete_middle']is True)
    yes('fresh_complete_middle_order4',v['middle_order']==4 and v['middle_rotation_order']==2)
    no('wrong_LEFT_word_refused',lambda:run(l=[0,0,1,1]))
    no('wrong_RIGHT_word_refused',lambda:run(r=[1,2]))
    no('equal_identity_words_not_obstruction',lambda:run(l=[0,0],r=[1,1],p=1))
    no('equal_middle_generator_not_obstruction',lambda:run(l=[1],r=[1],p=1))
    no('LEFT_label3_refused',lambda:run(l=[3]))
    no('RIGHT_label0_refused',lambda:run(r=[0]))
    no('bool_LEFT_label_refused',lambda:run(l=[True]))
    no('bool_RIGHT_label_refused',lambda:run(r=[True]))
    no('bool_positive_power_refused',lambda:run(p=True))
    no('unadmitted_positive_power4_refused',lambda:run(p=4))
    no('zero_power_refused',lambda:run(p=0))
    no('empty_LEFT_word_refused',lambda:run(l=[]))
    no('empty_RIGHT_word_refused',lambda:run(r=[]))
    r64=right+[1,1]*31
    yes('RIGHT_word64_boundary_positive',len(r64)==64 and run(r=r64)['outside_complete_middle'])
    no('RIGHT_word65_refused',lambda:run(r=r64+[1]))
    l60000=left+[0,0]*29998
    yes('LEFT_word60000_boundary_positive',len(l60000)==60000 and run(l=l60000)['outside_complete_middle'])
    no('LEFT_word60001_refused',lambda:run(l=l60000+[0]))
    bad=[[row[:]for row in mat]for mat in marks];bad[0][0][0]=True
    no('noncanonical_bool_mark_refused',lambda:run(m=bad))
    no('duplicate_Original_mark_refused',lambda:run(m=[marks[0],marks[0],marks[2],marks[3]]))
    bad2=[[row[:]for row in mat]for mat in marks];bad2[0][0][0]=2
    no('noninvolution_mark_refused',lambda:run(m=bad2))
    permutation=list(range(7));permutation[2],permutation[4]=permutation[4],permutation[2]
    swap=[[int(permutation[i]==j)for j in range(7)]for i in range(7)]
    no('failed_Original_string_commutation_refused',lambda:run(m=marks[:3]+[swap]))
    yes('no_HSGS_or_RIGHT_order_or_GEN_credit',v['whole_H_SGS_or_order_replayed']is v['complete_RIGHT_subgroup_or_order_claimed']is v['named_type_or_GEN_claimed']is v['Original_identity_transfer_verified']is False and v['new_case_or_census_credit']==0)
    rt.need(len(names)==len(set(names))==24,'all24 new word designs');return names
def main():
    b,a,pins=api.start(sys.argv,'arithmetic');api.origin(sys.modules[__name__],'intersection_controls.py')
    names=fixtures(b);api.close(b)
    outputs=api.emit(a.output,dict(status='PASS',arithmetic_count=24,names=names,Original_inputs_loaded=False),dict(Source=pins,counts=b.snapshot()),b)
    sys.stdout.buffer.write(rt.encoded(dict(status='PASS',count=24,outputs=outputs)))
if __name__=='__main__':main()
