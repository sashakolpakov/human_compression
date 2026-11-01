"""UNRUN synthetic D38/prime19-word and fixed-space controls; no original input."""
import copy,sys
import runtime as rt
import field as f
import common,search,check19

def controls(b):
    checks=[]
    def yes(name,ok):rt.need(ok,name);checks.append(name)
    def no(name,call):
        try:call()
        except ValueError:checks.append(name);return
        raise AssertionError(name)
    def identity():return [[int(i==j)for j in range(7)]for i in range(7)]
    def flat(a):return bytes(x for row in a for x in f.vector(row,7,b))
    # Companion of x^3+x^2+2x+10 and its explicit inverse. This is synthetic
    # fixture data from the previously accepted generic prime19 controls.
    C=((0,1,0),(0,0,1),(1,9,10));U=((2,1,1),(1,0,0),(0,1,0))
    r=identity();s=identity()
    for i in range(6):
        for j in range(6):
            r[i][j]=C[i][j]if i<3 and j<3 else U[i-3][j-3]if i>=3 and j>=3 else 0
            s[i][j]=int(j==(i+3)%6)
    R,S=flat(r),flat(s);T=b.multiply(S,R)
    raw=[s,[[T[7*i+j]for j in range(7)]for i in range(7)],identity()]
    g=common.marks(raw,b);cert,cov=search.supply(g,128,b,{})
    yes('actual BFS finds a positive original-generator word',cert is not None and cert['word']==[0,1] and cov['nonidentity_words_tested']>=1)
    result=check19.consume(g,cert,b)
    yes('naive prime19 and complete fixed kernel',result['exact_prime_order']==19 and result['fixed_dimension']==1 and result['selected_seed']==[0,0,0,0,0,0,1])
    M=common.word(g,cert['word'],b);v=tuple(result['selected_seed'])
    yes('actual fixed seed image',b.image(v,M)==bytes(v))
    bad=copy.deepcopy(cert);bad['word']=[0]
    no('wrong prime power refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['word']=[2]
    no('identity word cannot certify19',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['word']=[]
    no('empty word refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['word']=[True]
    no('Boolean word letter refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['word']=[0]*256
    no('full word length cap',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['kernel']['rank']=True
    no('Boolean rank refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['kernel']['row_combinations'][0][0]=(bad['kernel']['row_combinations'][0][0]+1)%11
    no('actual R equals C times A required',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['kernel']['nullspace_basis'][0][0]=1
    no('every original fixed equation checked',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['kernel']['nullspace_basis']=[]
    no('complete nonzero nullspace required',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['seed']=[0]*7
    no('zero selected seed refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(cert);bad['seed'][6]=True
    no('Boolean seed refused',lambda:check19.consume(g,bad,b))
    bad=copy.deepcopy(raw);bad[2][0][0]=2
    no('all three involutions checked',lambda:common.marks(bad,b))
    no('Boolean search cap refused',lambda:search.supply(g,True,b,{}))
    miss,_=search.supply(common.marks([identity()]*3,b),128,b,{})
    yes('finite search miss is no certificate',miss is None)
    before=b.linear
    try:b.scalar(rt.CAPS['linear_units']-before+1)
    except rt.Limit:pass
    else:raise AssertionError('same field bank overflow')
    yes('same bank refuses before overflow',b.linear==before)
    return dict(status='PASS',count=len(checks),checks=checks,Root_authority=False,original_case_credit=0)

def main(argv):
    mp,msha,jp,jsha,out=rt.arguments(argv);b,job,pins=rt.startup(mp,msha,jp,jsha)
    rt.origins(pins,__file__,f,common,search,check19,search.solve,check19.verify)
    rt.need(job=={'schema':'F004_ORDER19_FIXED_SEED_CONTROLS_V1','context_refs':[]},'closed synthetic controls job')
    report=controls(b);rt.close_inputs(b);report.update(input_pins=pins,counts=b.snapshot())
    outputs=rt.emit(out,dict(status='PASS',count=report['count'],Root_authority=False),report,b)
    print(rt.encoded(dict(status='GENERIC_CONTROLS_ONLY',outputs=outputs)).decode(),end='')

if __name__=='__main__':main(sys.argv)
