"""Freeze small metadata only; never copy a payload or write to the public repository."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util
import json

I=Path(__file__).resolve().parent
P=I.parent
R=Path('/Users/sasha/medusa/math_compression')
C=P/'registration_candidate02'
ST=P/'stage01'
spec=importlib.util.spec_from_file_location('guard',I/'check_L036_completion.py')
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def write(name,value):
    p=I/name
    g.need(not p.exists(),'Fresh metadata plan')
    p.write_text(json.dumps(value,indent=2)+'\n')


def main():
    g.need(g.git(R,'rev-parse','HEAD').decode().strip()==g.BASELINE,'Exact predecessor')
    g.need(not g.git(R,'status','--porcelain').strip(),'Clean predecessor')
    g.need(g.sha(C/'manifest.json')==g.CANDIDATE_SHA,'Reviewed candidate')
    rows=[]
    def add(source,target):
        p=g.pin(source,source.parent)
        rows.append(dict(path=target,bytes=p['bytes'],sha256=p['sha256'],source_path=str(source)))
    baseline=g.load(C/'baseline.json')
    history=[]
    for name in baseline['history_paths']+['provenance/publication_manifest.json']:
        target=g.AUD+'/previous/'+name
        add(R/name,target)
        history.append({k:v for k,v in rows[-1].items() if k!='source_path'})
    stage=g.load(ST/g.AUD/'manifest.json')
    for row in stage['exports']+[g.pin(ST/g.AUD/'manifest.json',ST)]:
        g.bind(ST,row)
        add(ST/row['path'],row['path'])
    candidate=g.load(C/'manifest.json')
    for row in candidate['exports']+[g.pin(C/'manifest.json',C)]:
        g.bind(C,row)
        target=row['path'][9:] if row['path'].startswith('proposed/') else g.AUD+'/registration/'+row['path']
        add(C/row['path'],target)
    for name in ['check_registration_candidate.py','prepare_registration.py','check_registration_candidate02.py','prepare_registration02.py']:
        add(P/name,g.AUD+'/registration/'+name)
    old=(R/'scripts/verify_snapshot.py').read_text()
    (I/'verify_snapshot.py').write_text(g.verifier_delta(old))
    add(I/'verify_snapshot.py','scripts/verify_snapshot.py')
    add(I/'check_L036_completion.py','scripts/check_L036_completion.py')
    for name in ['install_L036_completion.py','finalize_L036_completion.py','prepare_plan.py']:
        add(I/name,g.AUD+'/integration/'+name)
    names=[r['path'] for r in rows]
    g.need(len(names)==len(set(names)),'No colliding installation targets')
    preserved_names=['audit/science91/v1/root_integration.json','audit/recoveries/L091/v1/root_integration.json',
                     'audit/science91/v1/registration_review/manifest.json','scripts/check_science91.py',
                     'papers/catalogue_corrected_unmeasured.json',baseline['active_catalogue']['path'],
                     'audit/corpus/updates/accessible106-science91-L091.json',
                     'audit/principal-refutations/L036/v1/admission.json',
                     'audit/principal-refutations/F003/complete/v1/root_integration.json',
                     'audit/principal-refutations/F003/complete/v1/source_completion_registration.json',
                     'scripts/check_F003_completion.py',
                     'audit/principal-refutations/L029/complete/v1/root_integration.json',
                     'audit/principal-refutations/L029/complete/v1/source_completion_registration.json',
                     'scripts/check_L029_completion.py']
    # An older principal admission may be routed at one of these two paths only.
    preserved_names=[name for name in preserved_names if (R/name).is_file()]
    params=dict(baseline=g.BASELINE,source_ids=['L036'],replaced_paths=baseline['history_paths'],
                preserved=[g.pin(R/name,R) for name in preserved_names],history=history,
                old_mutable={name:g.pin(R/name,R) for name in baseline['history_paths']},
                previous_publication_manifest=history[-1],integration_files=[],
                root_gate_status='ROOT_ACCEPTED_L036_COMPLETE_SOURCE_PUBLICATION',
                required_registration_review_status='ACCEPTED_L036_SOURCE_COMPLETION_REGISTRATION')
    write('parameters.json',params)
    write('install_files.json',dict(baseline=g.BASELINE,files=rows))
    write('payload_manifest.json',dict(baseline=g.BASELINE,files=[{k:v for k,v in r.items() if k!='source_path'} for r in rows]))
    print(json.dumps(dict(status='SMALL_L036_INSTALLATION_PLAN_FROZEN',files=len(rows),bytes=sum(r['bytes'] for r in rows),public_writes=0,payloads_copied=0)))


if __name__=='__main__':
    main()
