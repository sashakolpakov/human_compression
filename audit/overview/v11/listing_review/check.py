#!/usr/bin/env python3
"""Independent check of the listing audit and unchanged comparison statuses."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(audit, public, study=None):
    manifest = read(audit / 'manifest.json')
    need(sha((audit / 'manifest.json').read_bytes()) ==
         'eb605489814f8bc43f10445d34101159053a3da99f987925316fb0a6c7b9be5a',
         'exact listing audit')
    for row in manifest['exports']:
        data = (audit / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], row['path'])
    old = read(public / 'audit/overview/v10/packet/results.json')
    rows = read(audit / 'comparison_dispositions.json')['comparisons']
    expected = []
    for topic in old['topics']:
        expected.append(('whole_topic', topic['topic'], topic['source_ids'], topic['written']))
        for pair in topic['pairs']:
            expected.append(('conditional_application', topic['topic'], [pair['source']], pair['conditional']))
    need(len(expected) == len(rows) == 62, 'all earlier comparisons accounted for')
    retained = {'whole_topic': 0, 'conditional_application': 0}
    held_topics = {'Chamber', 'ChiralEnumeration', 'Operations'}
    held_sources = {'L008', 'L028', 'N006'}
    for row, (kind, topic, source_ids, value) in zip(rows, expected):
        need((row['kind'], row['topic'], row['source_ids'], row['historical_value']) ==
             (kind, topic, source_ids, value), 'unchanged historical value and owner')
        hold = topic in held_topics if kind == 'whole_topic' else source_ids[0] in held_sources
        need(row['current_status'] == ('WITHHOLD_PENDING_SYMMETRIC_REMEASUREMENT' if hold
                                      else 'RETAIN_UNCHANGED_MANUSCRIPT_COORDINATE'),
             'status applies only to affected comparison')
        retained[kind] += int(not hold)
    need(retained == {'whole_topic': 16, 'conditional_application': 40}, '56 retained values')

    documents = read(audit / 'documents.json')['documents']
    need(len(documents) == 109 and len({(d['topic'], d['side'], d['key']) for d in documents}) == 109,
         'unique complete document inventory')
    need(sum(d.get('actual_pages', 0) for d in documents) == 1003, 'all PDF pages')
    bindings = read(audit / 'bindings.json')
    bound_rows = [bindings['overview'], bindings['policy']] + bindings['measurement_specs']
    bound_rows += bindings['replacement_tex_closure'] + [d['file'] for d in documents]
    verified, skipped, seen = 0, 0, set()
    for row in bound_rows:
        identity = (row['root'], row['path'])
        if identity in seen:
            continue
        seen.add(identity)
        base = public if row['root'] == 'public' else study
        if base is None:
            skipped += 1
            continue
        data = (base / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'input ' + row['path'])
        verified += 1
    tex_files = bindings['replacement_tex_closure']
    need(len(tex_files) == 191, 'complete counted replacement input closure')
    checked_tex = 0
    for row in tex_files:
        base = public if row['root'] == 'public' else study
        if base is None:
            continue
        text = (base / row['path']).read_text()
        need(not re.search(r'\\(?:lstinputlisting|VerbatimInput|inputminted)\b|'
                           r'\\begin\{(?:verbatim|Verbatim|lstlisting|minted|CompleteProgram)\}', text),
             'unaccounted replacement executable input ' + row['path'])
        checked_tex += 1
    findings = read(audit / 'listing_findings.json')['findings']
    need({r['source'] for r in findings} == held_sources, 'three confirmed listing sources')
    actual_blocks = 0
    if study is not None:
        from pypdf import PdfReader
        for finding in findings:
            pdf = PdfReader(study / finding['source_file']['path'])
            for block in finding['block_locators']:
                first_page, first_line = block['start']
                last_page, last_line = block['end']
                start = pdf.pages[first_page - 1].extract_text().splitlines()[first_line - 1]
                end = pdf.pages[last_page - 1].extract_text().splitlines()[last_line - 1]
                need(start.startswith(('function ', 'procedure ', 'Invs :=')), 'actual code start')
                need(end.strip() in {'end function;', 'end procedure;', 'end for'}, 'actual code end')
                actual_blocks += 1
        need(actual_blocks == 7, 'seven actual implementation blocks')
    screen = read(audit / 'topic_screen.json')
    need(screen['positive_topics'] == 15 and screen['held_topics'] == 3, 'bounded other-topic screen')
    review = read(audit / 'review.json')
    need(review['scope']['fresh_visual_pages'] == 8 and review['scope']['new_full_scientific_reviews'] == 0,
         'honest review scope')
    need(review['findings']['old_costs_or_factors_modified'] is False, 'no silent recount')
    return {
        'status': 'PASS_INDEPENDENT_LISTING_POLICY_CHECK',
        'verified_bindings': verified, 'private_bindings_skipped': skipped,
        'replacement_tex_files_checked': checked_tex, 'source_blocks_checked': actual_blocks,
        'retained_whole': 16, 'retained_conditional': 40,
        'held_topics': sorted(held_topics), 'held_sources': sorted(held_sources),
        'fresh_full_source_rereading_claimed': False,
        'ratios_remeasured': False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--public', type=Path, required=True)
    parser.add_argument('--study', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output')
    result = verify(args.audit, args.public, args.study)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
