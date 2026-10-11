#!/usr/bin/env python3
"""Recheck exact reviewed bytes and finite evidence, not the written uniform proof."""
from pathlib import Path
import argparse
import hashlib
import json
from pypdf import PdfReader
from finite_checks import run, need

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists(), 'fresh output')
    review = json.loads((HERE / 'review.json').read_text())
    for row in review['bindings']:
        b = (a.study_root / row['path']).read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
             'exact reviewed input ' + row['path'])
    need(review['status'] == 'ACCEPTED_BOUNDED_MATHEMATICAL_REVIEW' and
         review['new_recovered_originals'] == review['new_question_credit'] ==
         review['formal_declarations'] == 0 and review['compression_factor'] is None,
         'bounded acceptance without full-source, question, formal or ratio credit')
    need(review['open_findings'] == [] and len(review['resolved_review_findings']) == 1,
         'explicit resolved supporting-edge repair')
    finite = run()
    need(finite == json.loads((HERE / 'finite_result.json').read_text()), 'fresh independent finite evidence')
    rendered = json.loads((HERE / 'render_review.json').read_text())
    need(rendered['all_five_pages_visually_read'] and not rendered['visual_review_pending'],
         'recorded distinct full five-page view')
    total_pages = 0
    for row in rendered['records']:
        pdf = HERE / 'render' / (row['name'] + '.pdf')
        b = pdf.read_bytes()
        need(hashlib.sha256(b).hexdigest() == row['pdf_sha256'], 'exact freshly rendered proof PDF')
        pages = [p.extract_text() or '' for p in PdfReader(pdf).pages]
        need(len(pages) == row['pages'] and
             [hashlib.sha256(p.encode()).hexdigest() for p in pages] == row['page_text_sha256'],
             'all reviewed proof page texts')
        need(row['diagnostics'] == [], 'clean render report')
        total_pages += len(pages)
    if (HERE / 'manifest.json').exists():
        for row in json.loads((HERE / 'manifest.json').read_text())['exports']:
            b = (HERE / row['path']).read_bytes()
            need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
                 'frozen review export ' + row['path'])
    result = dict(status='PASS', exact_reviewed_inputs=len(review['bindings']),
                  reviewed_results=len(review['accepted']), final_proof_pages=total_pages,
                  independent_finite_controls=len(finite['rejected_controls']),
                  written_uniform_proof_checked_by_program=False,
                  full_N005_contract_accepted=False)
    a.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
