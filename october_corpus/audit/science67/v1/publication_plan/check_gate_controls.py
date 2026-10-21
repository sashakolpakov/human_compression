"""In-memory publication-gate controls; never create a root acceptance file."""
from pathlib import Path
import argparse,copy,json
import check
def main(a):
    r=check.verify(a.repo);required=set(r['required_root_gate_paths'])
    fixture=dict(status='ROOT_ACCEPTED_SCIENCE67_PUBLICATION',source_ids=['L031'],measurements_added=0,new_question_credit=0,bindings=[dict(path=n) for n in sorted(required)])
    check.root_gate(fixture,required);tests=[]
    changes=[('pending is not acceptance',lambda x:x.__setitem__('status','PENDING')),
             ('wrong original',lambda x:x.__setitem__('source_ids',['L015'])),
             ('new measurement',lambda x:x.__setitem__('measurements_added',1)),
             ('new question',lambda x:x.__setitem__('new_question_credit',1)),
             ('missing exact binding',lambda x:x['bindings'].pop()),
             ('duplicate binding',lambda x:x['bindings'].append(x['bindings'][0]))]
    for n,f in changes:
        x=copy.deepcopy(fixture);f(x)
        try:check.root_gate(x,required)
        except (ValueError,KeyError):tests.append(n)
        else:raise ValueError('control accepted '+n)
    out=dict(status='PASS_IN_MEMORY_ROOT_GATE_CONTROLS',controls=tests,required_root_gate_paths=sorted(required),root_acceptance_file_created=False)
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
