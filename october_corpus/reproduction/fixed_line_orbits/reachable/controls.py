"""UNRUN S3 parent-tree controls and a synthetic prime19 starting-vector check."""
import copy,sys
import runtime as rt
import field as f
import common,prime_seed,tree,search,check

def controls(b):
    checks=[]
    def yes(name,ok):rt.need(ok,name);checks.append(name)
    def no(name,call):
        try:call()
        except ValueError:checks.append(name);return
        raise AssertionError(name)
    def identity():return [[int(i==j)for j in range(7)]for i in range(7)]
    def swap(i,j):
        p=list(range(7));p[i],p[j]=p[j],p[i]
        return [[int(k==p[r])for k in range(7)]for r in range(7)]
    g=common.marks([swap(0,1),swap(1,2),swap(0,2)],b);v=bytes((1,0,0,0,0,0,0))
    cert=search.supply(g,v,3,b,{})
    expected=tree.encode(bytes((255,255,255,0,0,0,0,0,2)),3)
    yes('small target supplies only earlier parents',cert==expected)
    answer=check.consume(g,v,cert,3,b)
    yes('independent full-image distinctness',answer['reachable_distinct']==3 and answer['parent_images_verified']==2 and answer['orbit_closure_claimed']is False)
    missing=search.supply(g,v,4,b,{})
    yes('closed small orbit gives no threshold carrier',missing is None)
    bad=tree.encode(bytes((255,255,255,1,0,0,0,0,2)),3)
    no('parent must be earlier',lambda:check.consume(g,v,bad,3,b))
    bad=tree.encode(bytes((255,255,255,0,0,3,0,0,2)),3)
    no('label is an actual end mark',lambda:check.consume(g,v,bad,3,b))
    bad=tree.encode(bytes((255,255,255,0,0,0,0,0,0)),3)
    no('duplicate actual reached vector',lambda:check.consume(g,v,bad,3,b))
    bad=tree.encode(bytes((0,255,255,0,0,0,0,0,2)),3)
    no('single root sentinel required',lambda:check.consume(g,v,bad,3,b))
    bad=copy.deepcopy(cert);bad['parent_tree_b64']+='AAAA'
    no('whole packed EOF required',lambda:check.consume(g,v,bad,3,b))
    bad=copy.deepcopy(cert);bad['n']=True
    no('Boolean count refused',lambda:check.consume(g,v,bad,3,b))
    no('small certificate cannot pay strict9241',lambda:check.consume(g,v,cert,9241,b))
    no('zero start seed refused',lambda:prime_seed.begin(g,[0]*7,[0],b))
    no('identity word refused',lambda:prime_seed.begin(g,list(v),[0,0],b))
    no('wrong prime power refused',lambda:prime_seed.begin(g,list(v),[0],b))
    no('Boolean word refused',lambda:common.word(g,[True],b))
    C=((0,1,0),(0,0,1),(1,9,10));U=((2,1,1),(1,0,0),(0,1,0))
    r=identity();s=identity()
    for i in range(6):
        for j in range(6):
            r[i][j]=C[i][j]if i<3 and j<3 else U[i-3][j-3]if i>=3 and j>=3 else 0
            s[i][j]=int(j==(i+3)%6)
    R=bytes(x for row in r for x in f.vector(row,7,b));S=bytes(x for row in s for x in f.vector(row,7,b))
    T=b.multiply(S,R);dg=common.marks([s,[[T[7*i+j]for j in range(7)]for i in range(7)],identity()],b)
    seed=prime_seed.begin(dg,[0,0,0,0,0,0,1],[0,1],b)
    yes('fresh positive order19 word and fixed seed',seed==bytes((0,0,0,0,0,0,1)))
    no('actual seed image required',lambda:prime_seed.begin(dg,[1,0,0,0,0,0,0],[0,1],b))
    bad=[swap(0,1),swap(1,2),identity()];bad[2][0][0]=2
    no('every input involution checked',lambda:common.marks(bad,b))
    before=b.linear
    try:b.scalar(rt.CAPS['linear_units']-before+1)
    except rt.Limit:pass
    else:raise AssertionError('shared scalar bank overflow')
    yes('no bank reset or overflow',b.linear==before)
    return dict(status='PASS',count=len(checks),checks=checks,Root_authority=False,original_case_credit=0)

def main(argv):
    mp,msha,jp,jsha,out=rt.arguments(argv);b,job,pins=rt.startup(mp,msha,jp,jsha)
    rt.origins(pins,__file__,f,common,prime_seed,tree,search,check)
    rt.need(job=={'schema':'F004_ORDER19_REACHABILITY_CONTROLS_V1','context_refs':[]},'closed generic controls')
    report=controls(b);rt.close_inputs(b);report.update(input_pins=pins,counts=b.snapshot())
    outputs=rt.emit(out,dict(status='PASS',count=report['count'],Root_authority=False),report,b)
    print(rt.encoded(dict(status='GENERIC_CONTROLS_ONLY',outputs=outputs)).decode(),end='')

if __name__=='__main__':main(sys.argv)
