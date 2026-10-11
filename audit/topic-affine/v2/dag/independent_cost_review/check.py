#!/usr/bin/env python3
"""Replay the independent affine cost review with its fixed primary inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import arithmetic_controls
import correction_check
import reader_check


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    correction_check.need(not a.out.exists(), 'fresh output directory')
    review=json.loads((root/'review.json').read_text())
    for name,pin in review['input_manifests'].items():
        correction_check.need(hashlib.sha256((a.study_root/name).read_bytes()).hexdigest()==pin,
                              'Exact accepted input '+name)
    packet=a.study_root/'topic_Affine_dag_costs_v2'
    correction=correction_check.check(a.study_root)
    arithmetic=arithmetic_controls.run(a.study_root,packet)
    reader=reader_check.check_with_controls(a.study_root,packet)
    a.out.mkdir(parents=True)
    for name,data in [('correction.json',correction),('arithmetic.json',arithmetic),('reader.json',reader)]:
        (a.out/name).write_text(json.dumps(data,indent=2)+'\n')
    report=dict(status='PASS_INDEPENDENT_AFFINE_COST_REVIEW_REPLAY',
                owner_metric_cells=arithmetic['baseline']['owner_metric_cells'],
                routes=arithmetic['baseline']['routes_checked'],
                arithmetic_controls=len(arithmetic['controls']),reader_controls=len(reader['controls']),
                semantic_reading='Frozen reviewer judgment; execution checks its exact119 interface assignments, not human reading anew.',
                new_source_credit=0,new_question_credit=0,new_formal_credit=0,
                primary_text_exported=False)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
