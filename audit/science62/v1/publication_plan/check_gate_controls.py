"""Bounded root-gate controls; creates no root acceptance or public file."""
from pathlib import Path
import argparse,copy,importlib.util,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('science62_gate_subject',HERE/'check.py')
subject=importlib.util.module_from_spec(spec);spec.loader.exec_module(subject)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 required={r['path'] for r in subject.load(HERE/'wrapper_routes.json')['files']}|{r['public_path'] for r in subject.load(HERE/'copy_plan.json')['files'] if r['public_path'].startswith(subject.NATIVE+'/')}|{subject.AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
 # This in-memory shape tests metadata only; it is never persisted as acceptance.
 shape=dict(status='ROOT_ACCEPTED_SCIENCE62_PUBLICATION',source_ids=['L025'],measurements_added=0,new_question_credit=0,bindings=[dict(path=k) for k in sorted(required)])
 subject.root_gate(shape,required);passed=[]
 mutations=[('missing verifier binding',lambda d:d['bindings'].remove(next(x for x in d['bindings'] if x['path']=='scripts/verify_snapshot.py'))),('duplicate binding',lambda d:d['bindings'].append(d['bindings'][0])),('wrong status',lambda d:d.__setitem__('status','PENDING')),('unrelated source',lambda d:d.__setitem__('source_ids',['L025','F008'])),('new measurement',lambda d:d.__setitem__('measurements_added',1))]
 for name,mut in mutations:
  d=copy.deepcopy(shape);mut(d)
  try:subject.root_gate(d,required)
  except ValueError:passed.append(name)
  else:raise ValueError('accepted malformed gate '+name)
 if (a.repo/subject.AUDIT/'root_integration.json').exists():raise ValueError('Expected a private candidate without root gate')
 try:subject.verify(a.repo,require_root=True)
 except FileNotFoundError as e:
  if Path(e.filename)!=a.repo/subject.AUDIT/'root_integration.json':raise
  passed.append('absent actual root gate')
 else:raise ValueError('candidate accepted without root gate')
 report=dict(status='PASS_ROOT_GATE_NEGATIVE_CONTROLS',required_paths=sorted(required),controls=passed,root_acceptance_created=False,public_files_written=False)
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
