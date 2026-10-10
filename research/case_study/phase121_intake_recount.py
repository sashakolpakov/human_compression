#!/usr/bin/env python3
"""Read-only recount of the published registry; no mathematical checks implied."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def binding(base, name):
    raw = (base/name).read_bytes()
    return dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not os.path.lexists(args.output), 'Refusing an existing output')
    root = args.repository.resolve()
    names = ['research/case_study/paper_registry.json',
             'research/case_study/manuscript_replacements.json']
    registry, replacements = [json.loads((root/n).read_text()) for n in names]
    entries = registry['entries']
    ids = [r['id'] for r in entries]
    require(len(ids) == len(set(ids)), 'Duplicate registry identifiers')
    assemblies = registry['assembled_replacements']
    by_id = {r['id']: r for r in replacements['replacements']}
    require(len(by_id) == len(replacements['replacements']), 'Duplicate replacement identifiers')
    for assembly in assemblies:
        require(assembly['intake'] == by_id[assembly['id']]['intake'], 'Intake cache disagreement')
    union = sorted(set().union(*(set(a['intake']) for a in assemblies)))
    counts = dict(indexed=len(entries), origins=dict(Counter(r['origin'] for r in entries)),
                  retrieved_full_text=sum(r['access_coverage']['retrieved_full_text'] for r in entries),
                  reading_categories=dict(Counter(r['access_coverage']['reading_category'] for r in entries)),
                  encoded=sum(r['encoded'] for r in entries),
                  rederived=sum(r['rederived'] for r in entries),
                  full_principal_results=sum(r['full_principal_results'] for r in entries),
                  statuses=dict(Counter(r['status'] for r in entries)),
                  reviewed_assembled_replacements=len(assemblies),
                  manuscripts_in_reviewed_assemblies=len(union),
                  assembly_membership_occurrences=sum(len(a['intake']) for a in assemblies))
    declared = registry['counts']
    for key in ['retrieved_full_text','reading_categories','encoded','rederived',
                'full_principal_results','statuses','reviewed_assembled_replacements',
                'manuscripts_in_reviewed_assemblies']:
        require(counts[key] == declared[key], 'Cached count disagreement: '+key)
    for origin, value in counts['origins'].items():
        require(declared[origin] == value, 'Origin count disagreement')
    nonprincipal = [r for r in entries if r['rederived'] and not r['full_principal_results']]
    complete_reading = [r for r in entries if r['access_coverage']['reading_category'] in
                        ['full_text_read','full_short_text_read']]
    primary_ids = sorted(r['id'] for r in entries if r['full_principal_results'])
    drift = []
    for a in assemblies:
        for field in ['length_factor','length_lower_bound']:
            if a.get(field) != by_id[a['id']].get(field):
                drift.append(dict(assembly=a['id'], field=field,
                                  registry_cached=a.get(field),
                                  replacements_authoritative=by_id[a['id']].get(field)))
    git = subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
    require(git.returncode == 0, 'Repository revision unavailable')
    report = dict(status='PASS_COUNTS_WITH_RECORDED_MEASUREMENT_CACHE_DRIFT',
                  repository_commit=git.stdout.strip(),inputs=[binding(root,n) for n in names],
                  counts=counts,admitted_union=union,
                  assemblies=[dict(id=a['id'],intake=a['intake']) for a in assemblies],
                  nonprincipal_rederived=len(nonprincipal),
                  nonprincipal_rederived_statuses=dict(Counter(r['status'] for r in nonprincipal)),
                  recorded_complete_reading=len(complete_reading),
                  principal_ids=primary_ids,principal_outside_assemblies=sorted(set(primary_ids)-set(union)),
                  measurement_cache_drift=drift,
                  latest_admitted_measurement=by_id['Compress_12']['length_lower_bound'],
                  boundary='Counts describe records and named assembly memberships, not a fresh review of the indexed mathematics or proof of corpus completeness.')
    with args.output.open('x') as stream:
        json.dump(report,stream,indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=report['status'],indexed=counts['indexed'],
                         retrieved_full_text=counts['retrieved_full_text'],
                         admitted_union=len(union),cache_drift_fields=len(drift))))


if __name__ == '__main__':
    main()
