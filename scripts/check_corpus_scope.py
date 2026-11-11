#!/usr/bin/env python3
"""Check current corpus accounting and links without replaying mathematics."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'october_corpus'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    need(path.stat().st_size <= 8 * 1024**2, 'Oversized metadata: ' + str(path))
    return json.loads(path.read_text())


def bind(record):
    path = (CORPUS / record['path']).resolve()
    need(path.is_relative_to(CORPUS), 'Metadata reference outside corpus')
    need(path.stat().st_size == record['bytes'], 'Byte count: ' + str(path))
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    need(digest.hexdigest() == record['sha256'], 'Digest: ' + str(path))


def verify():
    register = load(CORPUS / 'audit/corpus/latest.json')
    catalogue = load(CORPUS / register['active_catalogue']['path'])
    identities = load(CORPUS / register['manuscript_identity']['path'])
    intake = load(CORPUS / 'INTAKE_STATUS.json')
    overview = load(CORPUS / 'audit/overview/latest.json')
    papers = load(CORPUS / 'papers/latest_catalogue.json')
    current = load(CORPUS / 'audit/corpus/current.json')
    completion = load(CORPUS / 'audit/completion.json')
    intake_audit = load(CORPUS / 'audit/intake.json')
    queue = load(CORPUS / 'audit/work_queue.json')
    corpora = load(ROOT / 'corpora.json')
    october = next(c for c in corpora['corpora'] if c['id'] == 'october')

    components = [entry['original_id'] for entry in catalogue['entries']]
    grouped = [sid for group in identities['groups'] for sid in group['source_ids']]
    manuscript_ids = [group['manuscript_id'] for group in identities['groups']]
    need(len(components) == len(set(components)), 'Duplicate source component')
    need(sorted(grouped) == sorted(components), 'Manuscript groups partition components')
    need(len(manuscript_ids) == len(set(manuscript_ids)), 'Duplicate manuscript')
    need(set(manuscript_ids) == set(register['active_original_ids']), 'Active manuscripts')
    need(set(components) == set(register['active_source_ids']), 'Active source components')
    need(catalogue['active_original_ids'] == register['active_original_ids'], 'Catalogue membership')
    need(catalogue['active_source_ids'] == register['active_source_ids'], 'Catalogue components')
    counts = {entry['original_id']: entry['original_count'] for entry in catalogue['entries']}
    for group in identities['groups']:
        need(group['manuscript_id'] in group['source_ids'], 'Canonical manuscript component')
        need(sum(counts[sid] for sid in group['source_ids']) == 1, 'Count each manuscript once')

    recovered = set(register['admitted_original_ids'])
    refuted = set(register['refuted_principal_original_ids'])
    editorial = set(register['editorial_original_ids'])
    measured = set(register['measured_original_ids'])
    pending_measurement = set(register['measurement_pending_original_ids'])
    need(not (recovered & refuted or recovered & editorial or refuted & editorial), 'Disjoint treatments')
    need(recovered | refuted | editorial == set(manuscript_ids), 'All manuscripts accounted for')
    need(not measured & pending_measurement, 'Measured and pending sets are disjoint')
    need(measured | pending_measurement == recovered, 'All recoveries have measurement status')
    need(set(completion['completed_manuscript_ids']) == recovered | refuted, 'Completion membership')
    need(set(register['fully_treated_original_ids']) == recovered | refuted, 'Completed register')
    need(set(queue['order'][0]['original_ids']) == pending_measurement, 'Measurement queue')
    need(not queue['pending_mathematical_manuscripts'], 'No intake work remains')
    need(not intake['pending_manuscripts'], 'Empty intake obligations')
    need(intake['status'] == 'INTAKE_COMPLETE', 'Intake complete')
    need(intake['census_execution_enabled'] is False, 'Census execution disabled')
    need(queue['census_execution_enabled'] is False, 'Census queue disabled')

    table = (CORPUS / 'audit/overview/README.md').read_text()
    rows = re.findall(r'^\| \[[^\n]+\]\([^\n]+\) \| ([A-Z0-9, ]+) \| ([0-9.]+) \|$', table, re.M)
    topic_ids = [sid.strip() for ids, _ in rows for sid in ids.split(',')]
    need(len(topic_ids) == len(set(topic_ids)), 'A measured original occurs once')
    need(set(topic_ids) == measured, 'Overview covers the measured set exactly')
    rst = (CORPUS / 'README.rst').read_text()
    rst_rows = re.findall(r'   \* - `[^\n]+ <[^>]+>`_\n     - ([^\n]+)\n     - ([0-9.]+)', rst)
    need(rows == rst_rows, 'Programme and overview have identical factors and source sets')

    expected = dict(original_manuscripts=len(manuscript_ids),
        mathematical_manuscripts=len(recovered | refuted), editorials=len(editorial),
        source_components=len(components), complete_reviewed_mathematical_treatments=len(recovered | refuted),
        principal_result_recoveries=len(recovered), treatments_following_principal_refutations=len(refuted),
        pending_mathematical_manuscripts=0, measured_applications=len(measured),
        measurement_pending_recoveries=len(pending_measurement), measured_topics=len(rows))
    for doc in (register, catalogue, intake, current, completion, intake_audit, overview, october['statistics']):
        for key, value in expected.items():
            need(doc[key] == value, 'Consistent count: ' + key)
    need(overview['active_catalogue_originals'] == expected['original_manuscripts'], 'Overview denominator')
    need(overview['current_conditional_factors'] == len(measured), 'Conditional factors')
    need(overview['current_whole_factors'] == len(rows), 'Whole-topic factors')
    need(overview['unmeasured_accessible_originals'] == len(pending_measurement | refuted | editorial),
         'Unmeasured manuscript count')
    need(papers['active_originals'] == len(manuscript_ids), 'Paper catalogue denominator')
    need(papers['active_source_components'] == len(components), 'Paper catalogue source components')
    for paper in papers['entries']:
        need(set(paper.get('source_contracts', [])) <= set(components), 'Paper contracts are in corpus')

    records = [register['active_catalogue'], register['manuscript_identity'],
               catalogue['manuscript_identity'], current['register'], intake['source_register'],
               intake['manuscript_catalogue'], completion['source_register'], intake_audit['source_register'],
               papers['active_source_catalogue'], overview['counts_source']]
    for record in records:
        bind(record)

    docs = [ROOT/'README.md', CORPUS/'README.md', CORPUS/'README.rst',
            CORPUS/'REPRODUCING.md', CORPUS/'docs/REPRODUCING.rst',
            CORPUS/'audit/overview/README.md', CORPUS/'audit/completion.rst']
    required = set()
    for document in docs:
        text = document.read_text()
        targets = re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)
        targets += re.findall(r'<([^<>\n]+)>`_', text)
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (document.parent / unquote(parsed.path)).resolve()
            need(path.is_relative_to(ROOT), 'Documentation link outside repository')
            if not path.exists():
                required.add(path.relative_to(ROOT).as_posix())
    # Sparse checkouts can resolve links from Git trees without fetching blobs.
    if required:
        env = dict(os.environ, GIT_NO_LAZY_FETCH='1')
        process = subprocess.Popen(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=ROOT,
                                   stdout=subprocess.PIPE, text=True, env=env)
        for line in process.stdout:
            name = line.rstrip('\n')
            required.discard(name)
            for directory in tuple(required):
                if name.startswith(directory.rstrip('/') + '/'):
                    required.remove(directory)
        need(process.wait(timeout=30) == 0, 'Git tree listing')
    need(not required, 'Missing documentation targets: ' + ', '.join(sorted(required)))

    archive_status = load(CORPUS / 'research/intake/census/status.json')
    need(archive_status['status'] == 'ARCHIVED' and archive_status['execution_enabled'] is False,
         'Census is an inactive archive')
    need((ROOT / archive_status['checkpoint_manifest']).is_file(), 'Retained checkpoint')
    return dict(status='PASS_CORPUS_SCOPE', **expected, metadata_bindings_checked=len(records),
                documentation_files_checked=len(docs), scientific_jobs_started=0)


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
