#!/usr/bin/env python3
"""Independent character-mask allocation on the fixed extraction boundary.

Uses the adopted extraction/calibration helper, but no code from the author's
atomic allocator, partition checker, or factor calculation. Writes no source
text. This is an accounting cross-check, not a mathematical proof checker.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import unicodedata

ROOT = Path('/Users/sasha/medusa/research/leemans')
HERE = Path(__file__).resolve().parent
METRICS = ('whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
           'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace')
FORMS = ('NFC','NFKC')

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    return json.loads((ROOT/path).read_text())

def binding(path):
    data = (ROOT/path).read_bytes()
    return dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def allocate(text, spans, form):
    mask, chunks = [], []
    next_position = 0
    for span in spans:
        need(span['start']==next_position and span['end']>span['start'], 'Partition gap or overlap')
        part = text[span['start']:span['end']]
        need(hashlib.sha256(part.encode()).hexdigest()==span['sha256'], 'Wrong owned string')
        normalized = unicodedata.normalize(form,part)
        mask += [span['node']]*len(normalized)
        chunks.append(normalized)
        next_position = span['end']
    need(next_position==len(text), 'Unowned suffix')
    t = unicodedata.normalize(form,text)
    need(''.join(chunks)==t and len(mask)==len(t), 'Boundary-changing normalization')
    result = {owner:dict.fromkeys(METRICS,0) for owner in set(mask)}
    first = next((i for i,c in enumerate(t) if not c.isspace()), len(t))
    last = next((i for i in range(len(t)-1,-1,-1) if not t[i].isspace()), -1)
    for i,c in enumerate(t):
        row=result[mask[i]]
        if not c.isspace():
            row['characters_without_whitespace'] += 1
            row['characters_with_collapsed_whitespace'] += 1
            row['utf8_bytes_with_collapsed_whitespace'] += len(c.encode())
            if i==0 or t[i-1].isspace():
                row['whitespace_tokens'] += 1
        elif first<i<last and not t[i-1].isspace():
            row['characters_with_collapsed_whitespace'] += 1
            row['utf8_bytes_with_collapsed_whitespace'] += 1
        if c.isalnum() and (i==0 or not t[i-1].isalnum()):
            row['alphanumeric_units'] += 1
    return result

def main():
    spec = read('topic_A_measurement/source_input_spec.json')['sources'] | read('topic_A_numerical_audit/final_replacement_input_spec_private.json')['ours']
    part = read('topic_A_weighted_dag/partition.json')
    recorded = read('topic_A_weighted_dag/weights.json')
    module_spec = importlib.util.spec_from_file_location('accepted_extract', ROOT/'topic_A_measurement/extract_inputs.py')
    helper = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper)
    owner_checks = doc_checks = 0
    totals = {}
    for key,row in spec.items():
        text = helper.document(ROOT,key,row)[2]
        totals[key] = {}
        for form in FORMS:
            own = allocate(text,part['documents'][key]['spans'],form)
            for owner,counts in own.items():
                need(counts==recorded['owner_weights'][owner][form], 'Atomic allocation mismatch '+owner+' '+form)
                owner_checks += len(METRICS)
            totals[key][form] = {m:sum(x[m] for x in own.values()) for m in METRICS}
            need(totals[key][form]==recorded['document_totals'][key][form], 'Document conservation '+key+' '+form)
            doc_checks += len(METRICS)
    report = dict(status='PASS_INDEPENDENT_ATOMIC_OWNERSHIP_RECOUNT',
                  algorithm='Explicit normalized-character owner mask and character-state counters; no bisect, regular-expression token counting, or author accounting helper.',
                  extraction='The exact previously adopted PDF extraction/calibration helper is shared; this is independent allocation, not a second font-calibration policy.',
                  metric_owner_cells=owner_checks,document_cells=doc_checks,
                  documents=len(spec),owners=len(recorded['owner_weights']),
                  spans=sum(len(d['spans']) for d in part['documents'].values()),
                  inputs=[binding(p) for p in ['topic_A_weighted_dag/manifest.json','topic_A_weighted_dag/partition.json','topic_A_weighted_dag/weights.json','topic_A_measurement/source_input_spec.json','topic_A_numerical_audit/final_replacement_input_spec_private.json','topic_A_measurement/extract_inputs.py']],
                  document_totals=totals,ratio=None,new_credit=0,primary_text_exported=False)
    (HERE/'independent_allocation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','metric_owner_cells','document_cells','documents','owners','spans']}))

if __name__ == '__main__':
    main()
