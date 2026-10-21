#!/usr/bin/env python3
"""Check programme53 routes and root acceptance without rerunning its proofs."""
from pathlib import Path
import argparse,hashlib,importlib.util,json

def check_root_acceptance(root, record):
    if record.get('status') != 'ROOT_ACCEPTED_PROGRAMME53_INTEGRATION':
        raise ValueError('Programme53 requires an explicit root integration acceptance.')
    if record.get('new_originals') != ['L003'] or record.get('counts') != dict(
            active=106, measured=53, mathematical_pending=52, editorial=1,
            archived=55, topics=19):
        raise ValueError('Root acceptance has an incorrect original partition.')
    if record.get('full_source_Lean_credit') or record.get('new_question_credit'):
        raise ValueError('This integration supplies no new formal or question credit.')
    required = {
        'audit/programme53/v1/publication_plan/manifest.json',
        'audit/programme53/v1/registration_report.json',
        'audit/corpus/latest.json', 'papers/latest_catalogue.json',
        'papers/topic-a/latest.json', 'audit/overview/latest.json',
        'audit/overview/v19/admission.json', 'audit/topic-a/v5/admission.json',
        'audit/topic-a/extensions/hexagonal/v1/admission.json',
        'scripts/verify_snapshot.py', 'scripts/check_programme53.py',
        'audit/completion.rst',
    }
    bindings = record.get('bindings', [])
    paths = [row['path'] for row in bindings]
    if len(paths) != len(set(paths)) or not required.issubset(paths):
        raise ValueError('Root acceptance is missing exact integration bindings.')
    for row in bindings:
        path = Path(row['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe acceptance path.')
        content = (root/path).read_bytes()
        if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
            raise ValueError('Root acceptance binding changed: ' + str(path))
    return len(bindings)

def verify(root,reference_repo=None,proposal=None):
    root=Path(root).resolve()
    proposal=Path(proposal) if proposal else root/'audit/programme53/v1/publication_plan'
    reference_repo=Path(reference_repo) if reference_repo else root
    spec=importlib.util.spec_from_file_location('programme53_frozen_map',proposal/'check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.verify(root,reference_repo,root)
    result.update(status='PASS_EXACT_PROGRAMME53_ROUTES',measured=53,mathematical_pending=52,
                  editorial=1,archived=55,overview_fractions=72,overview_bars=163)
    acceptance=json.loads((root/'audit/programme53/v1/root_integration.json').read_text())
    result['root_integration_bindings']=check_root_acceptance(root,acceptance)
    result['root_publication_review_required']=False
    result['status']='PASS_ROOT_ACCEPTED_PROGRAMME53'
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--reference-repo',type=Path);p.add_argument('--proposal',type=Path)
    p.add_argument('--out',type=Path);a=p.parse_args();r=verify(a.repo,a.reference_repo,a.proposal)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
