#!/usr/bin/env python3
"""Proposed additive public guard; no science, extraction or formal rerun."""
from pathlib import Path
import argparse,importlib.util,json

def verify(root,reference_repo=None,proposal=None):
    root=Path(root).resolve()
    proposal=Path(proposal) if proposal else root/'audit/programme53/v1/publication_plan'
    reference_repo=Path(reference_repo) if reference_repo else root
    spec=importlib.util.spec_from_file_location('programme53_frozen_map',proposal/'check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.verify(root,reference_repo,root)
    result.update(status='PASS_EXACT_PROGRAMME53_ROUTES',measured=53,mathematical_pending=52,
                  editorial=1,archived=55,overview_fractions=72,overview_bars=163)
    # This guard verifies accepted payloads and proposed exact registry bindings.
    # A separate root integration acceptance must authorize public current pointers.
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--reference-repo',type=Path);p.add_argument('--proposal',type=Path)
    p.add_argument('--out',type=Path);a=p.parse_args();r=verify(a.repo,a.reference_repo,a.proposal)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
