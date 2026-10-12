"""Author negative controls; they are optional validation, not independent review."""
from pathlib import Path
import copy,json
from certificate import verify,power,refine,model,need

def main():
    data=json.loads((Path(__file__).resolve().parent/'data.json').read_text())
    cases=[]
    def reject(name,change,expected):
        d=copy.deepcopy(data);change(d)
        try:verify(d)
        except ValueError as e:
            need(expected in str(e),name+' failed at an unintended check: '+str(e))
            cases.append(dict(name=name,rejected_at=str(e)))
        else:raise ValueError(name+' was not rejected')
    reject('one-generator T is incomplete',lambda d:d['T_generators'].pop(),'T order2448')
    reject('a cubed cannot replace a',lambda d:d.update(a=list(power(tuple(d['a']),3))),'actual marked elements')
    reject('identity is not the marked b',lambda d:d.update(b=list(range(18))),'actual marked elements')
    reject('identity cannot supply a type reflection',lambda d:d.update(reflection=list(range(1839))),'reflection is an involution')
    def change_image(d):d['reflection'][0],d['reflection'][1]=d['reflection'][1],d['reflection'][0]
    reject('corrupted full reflection permutation',change_image,'reflection')
    def fix_markers(d):d['reflection'][1836:]=[1836,1837,1838]
    reject('fixing the markers changes the claimed reflection',fix_markers,'reflection preserves entire augmented graph')
    reject('repeated base point does not kill the edge stabilizer',lambda d:d.update(refinement_base=[0,612,612]),'invariant three-cell')
    m=model(data)
    cells,_=refine(m['augmented'],[0,612],1836)
    need(len(cells)==633 and len(cells)!=1839,'two-point refinement is not a trivial stabilizer certificate')
    cases.append(dict(name='edge stabilizer cannot be silently set to1',rejected_at='633 color classes remain, including a three-cell'))
    need(all(power(m['sigma'],3)[x]//612==x//612 for x in range(1836)),'cube is type preserving')
    cases.append(dict(name='order-three power is not a triality',rejected_at='sigma cubed fixes all three types'))
    print(json.dumps(dict(status='PASS_AUTHOR_NEGATIVE_CONTROLS',controls=cases,count=len(cases),independent_review=False),indent=2))

if __name__=='__main__':main()
