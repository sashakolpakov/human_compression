"""Check exact survey dispositions and proof joins, without repeating censuses."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode = True
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def validate(register, scope, source, retained, acquired, manuscripts):
    need(register['original'] == scope['original'] == 'N010', 'Exact original')
    for obj in [register, scope]:
        need(all(obj[k] == 0 for k in ['new_question_credit', 'new_Lean_declarations',
                                     'new_measurements', 'whole_original_credit']), 'No new credit')
        need(obj['compression_factor'] is None and not obj['all_classifications_reproved'],
             'No invented complete classification or measurement')
    need(not scope['global_aggregates_reproduced'] and not scope['present_open_status_claimed'],
         'Historical reports and present open status remain distinct')
    need(not register['source_questions_asserted_currently_open'], 'No present open-status assertion')
    need(register['source_only_aggregates'] == [17, 441]
         and register['corrected_family_count'] == 137
         and register['corrected_global_total'] is None, 'No inferred global correction')
    need(register['source_bibliography'] == source['source_bibliography']
         and len(register['source_bibliography']) == 66, 'All source bibliography entries')
    need(register['source_qualifications'] == source['review_qualifications'], 'Complete edition qualifications')
    need([r['id'] for r in register['contexts']] == [f'C{i:02}' for i in range(1, 17)],
         'All sixteen contexts')
    clauses = register['established_clauses']
    need([r['id'] for r in clauses] == [f'R{i:02}' for i in range(1, 53)], 'All52 clauses')
    need(scope['established_clauses'] == 52 and len(retained['rows']) == 51,
         'Revised assembly preserves the frozen 51-row source register')
    for old, row in zip(retained['rows'], clauses):
        for key, value in old.items():
            if key != 'disposition':
                need(row[key] == value, 'Exact retained source clause ' + row['id'])
        need(row['source_register_disposition'] == old['disposition'], 'Preserve frozen historical status')
        expected = ('COMPLETE_DISTINCTLY_REVIEWED_FINITE_COMPONENT' if row['id'] == 'R13'
                    else 'NEW_WRITTEN_PROOF_OF_ESTABLISHED_NECESSARY_CONDITION' if row['id'] == 'R46'
                    else old['disposition'])
        need(row['disposition'] == expected, 'No promoted retained classification')
    r52 = clauses[-1]
    need(r52['context'] == 'C07' and r52['physical_pages'] == [10]
         and r52['tex_line'] == 337
         and r52['source_anchor'] == 'In rank $4$ (but not in rank $5$)'
         and r52['claim'] == 'Every locally projective regular polytope of rank four is finite; the corresponding assertion fails in rank five.'
         and r52['source_citation_keys'] == ['halp', 'arp']
         and r52['disposition'] == 'SOURCE_ATTRIBUTED_CLASSIFICATION_NOT_INDEPENDENTLY_VERIFIED'
         and not r52['independently_inspected_primary_classification']
         and not r52['exact_acquired_join'] and r52['new_question_credit'] == 0,
         'Explicit historical rank distinction remains a retained input')
    need('R52' in register['contexts'][6]['rows'], 'Rank distinction routed to C07')
    need([r['number'] for r in register['questions']] == list(range(1, 35)), 'All34 numbered problems')
    for old, row in zip(source['numbered_problems'], register['questions']):
        need(all(row[k] == v for k,v in old.items()), 'Exact numbered source question')
        status = ('Already negative in the source.' if row['number'] == 8
                  else 'Affirmative existence by the acquired 2016 theorem.' if row['number'] == 31
                  else 'Regular ranks acquired; chiral rank-three existence only; other parts unsettled here.' if row['number'] == 32
                  else 'Restricted acquired results only; general question unsettled here.' if row['number'] == 30
                  else 'Unsettled here.')
        need(row['synthesis_status'] == status, 'Exact scope of question disposition')
    secondary = register['secondary_records']
    need(len(secondary) == 14 and len({r['id'] for r in secondary}) == 14, 'All14 secondary records')
    for old, row in zip(source['embedded_questions_and_conjectures'], secondary):
        need(all(row[k] == v for k,v in old.items()), 'Exact embedded question')
        need(row['synthesis_status'] == ('Only the exact positive families of the acquired simple-group theorem are supplied; the excluded families and regular-map question are not decided.' if row['id'] == 'P31-finite-simple' else 'No new solution supplied.'), 'No new embedded solution')
    need(len(acquired['private']) == 15 and len(acquired['published']) == 6,
         'All acquired private and published proof routes')
    need(acquired['no_new_census'] and acquired['no_new_Lean'], 'No expanded phase')
    need([r['pages'] for r in manuscripts['immediate_components']] == [4, 3, 2, 2]
         and all(r['complete'] for r in manuscripts['immediate_components']), 'All unabridged components')
    need(manuscripts['synthesis_pages'] == 11 and manuscripts['immediate_reading_volume_pages'] == 22
         and manuscripts['older_acquired_proofs_are_additional'], 'Honest reading volume boundary')
    return dict(contexts=16, established_clauses=52, numbered_questions=34,
                secondary_records=14, bibliography_entries=66)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    a = ap.parse_args()
    P = Path(__file__).resolve().parent
    S, R, O = a.study.resolve(), a.repo.resolve(), a.out.resolve()
    need(not O.exists() and not O.is_relative_to(P), 'Fresh external output')

    def verify(row):
        root = {'study': S, 'public': R, 'packet': P}[row['namespace']]
        p = (root / row['path']).resolve()
        need(p.is_relative_to(root) and p.is_file(), 'Safe exact input')
        b = p.read_bytes()
        need((len(b), hashlib.sha256(b).hexdigest()) == (row['bytes'], row['sha256']),
             'Changed input ' + row['path'])
        return p

    manifest = load(P / 'manifest.json')
    need(manifest['original'] == 'N010', 'Exact frozen author original')
    for row in manifest['exports']:
        verify(dict(namespace='packet', **row))
    dependencies = load(P / 'dependencies.json')
    for row in dependencies:
        verify(row)
    source = load(S / 'reboot_20261013/N010_work/source_contract02.json')
    retained = load(S / 'reboot_20261013/N010_retained_inputs/register01/retained_register.json')
    register, scope = load(P / 'claim_register.json'), load(P / 'scope.json')
    acquired, manuscripts = load(P / 'acquired_packets.json'), load(P / 'acquired_manuscripts.json')
    counts = validate(register, scope, source, retained, acquired, manuscripts)
    controls = []
    cases = ['omit_context', 'omit_clause', 'lose_question', 'lose_secondary',
             'lose_bibliography', 'promote_global_census', 'invent_corrected_total',
             'declare_currently_open', 'solve_general_twogroup', 'solve_all_chiral_ranks',
             'credit_old_sporadic', 'promote_retained_classification', 'abridge_component',
             'invent_formalization', 'promote_source_claim', 'promote_rank_distinction',
             'lose_rank_distinction_route']
    for case in cases:
        rr, ss, aa, mm = copy.deepcopy((register, scope, acquired, manuscripts))
        if case == 'omit_context': rr['contexts'].pop()
        elif case == 'omit_clause': rr['established_clauses'].pop()
        elif case == 'lose_question': rr['questions'].pop()
        elif case == 'lose_secondary': rr['secondary_records'].pop()
        elif case == 'lose_bibliography': rr['source_bibliography'].pop(next(iter(rr['source_bibliography'])))
        elif case == 'promote_global_census': ss['global_aggregates_reproduced'] = True
        elif case == 'invent_corrected_total': rr['corrected_global_total'] = 400
        elif case == 'declare_currently_open': rr['source_questions_asserted_currently_open'] = True
        elif case == 'solve_general_twogroup': rr['questions'][29]['synthesis_status'] = 'Solved completely'
        elif case == 'solve_all_chiral_ranks': rr['questions'][31]['synthesis_status'] = 'Solved completely'
        elif case == 'credit_old_sporadic': rr['questions'][30]['new_question_credit'] = 1
        elif case == 'promote_retained_classification': rr['established_clauses'][16]['disposition'] = 'REPROVED'
        elif case == 'abridge_component': mm['immediate_components'][0]['complete'] = False
        elif case == 'invent_formalization': rr['new_Lean_declarations'] = 1
        elif case == 'promote_source_claim': rr['established_clauses'][21]['claim'] = 'The corrected global total is441'
        elif case == 'promote_rank_distinction': rr['established_clauses'][-1]['disposition'] = 'REPROVED'
        else: rr['contexts'][6]['rows'] = 'R20--R23'
        try:
            validate(rr, ss, source, retained, aa, mm)
        except (ValueError, KeyError):
            controls.append(case)
        else:
            raise ValueError('Damaged scientific join accepted: ' + case)

    from pypdf import PdfReader
    def text(p):
        return [page.extract_text() for page in PdfReader(p).pages]
    expected = text(P / 'principal.pdf')
    need(len(expected) == 11 and '\n\f\n'.join(expected) == (P / 'principal_expected.txt').read_text(),
         'Exact complete synthesis text')
    full = expected[:]
    for row in manuscripts['immediate_components']:
        verify(row['tex'])
        part = text(verify(row['pdf']))
        need(len(part) == row['pages'], 'Complete acquired component pages')
        full.extend(part)
    need(len(full) == 22 and text(P / 'principal_and_components.pdf') == full, 'Exact22page reading volume')
    O.mkdir(parents=True)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    guards = []
    for mode in ['argument', 'environment']:
        e = env.copy()
        cmd = [sys.executable] + (['-O'] if mode == 'argument' else [])
        if mode == 'environment': e['PYTHONOPTIMIZE'] = '1'
        target = O / ('rejected_' + mode)
        p = subprocess.run(cmd + [str(P / 'check.py'), '--out', str(target)],
                           env=e, capture_output=True, timeout=15)
        (O / ('guard_' + mode + '.stderr')).write_bytes(p.stderr)
        need(p.returncode != 0 and b'Normal Python is required' in p.stderr and not target.exists(),
             'Pre-output optimization rejection')
        guards.append(mode)
    native = None
    if a.render:
        N = O / 'native'
        N.mkdir()
        for name in ['principal.tex', 'context_table.tex', 'question_table.tex', 'secondary_table.tex']:
            shutil.copyfile(P / name, N / name)
        for i in [1, 2]:
            p = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'principal.tex'],
                               cwd=N, env=env, capture_output=True, timeout=60)
            (N / f'pass{i}.stdout').write_bytes(p.stdout)
            (N / f'pass{i}.stderr').write_bytes(p.stderr)
            need(p.returncode == 0 and not p.stderr, 'Native TeX build')
        need(text(N / 'principal.pdf') == expected, 'Fresh native text and page identity')
        log = (N / 'principal.log').read_text()
        need(not any(s in log for s in ['Overfull', 'Underfull', 'LaTeX Warning:', 'undefined references']),
             'Clean native layout and references')
        p = subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m',
                            '-r90', '-sOutputFile=page-%02d.png', 'principal.pdf'],
                           cwd=N, capture_output=True, timeout=60)
        need(p.returncode == 0 and not p.stderr and len(list(N.glob('page-*.png'))) == 11, 'All native pages')
        native = dict(pages=11, text_identical=True, clean_log=True, direct_visual_review_required=True)
    report = dict(status='PASS_N010_COMPLETE_SURVEY_JOIN', exports=len(manifest['exports']),
                  direct_bindings=len(dependencies), counts=counts, damaged_controls=controls,
                  optimization_guards=guards, immediate_reading_pages=22, native=native,
                  mathematical_proof_checked_by_this_program=False, acquired_censuses_repeated=False,
                  whole_original_credit=0, new_question_credit=0, new_Lean_declarations=0, new_measurements=0)
    (O / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
