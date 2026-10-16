"""F003 source assembly: exact imports, literal binary identities and scope.

This checks finite identities and document assembly. It does not certify
the general proofs or promote a prior principal correction to completion.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('optimization is not an admitted execution mode')

from binary import MATRIX, check as binary_check

P = Path(__file__).resolve().parent
R = Path('/Users/sasha/medusa/math_compression')
EXPECTED = {
    'Theorem 1.1': 'REFUTED_BY_ACCEPTED_PRINCIPAL_CONSTRUCTION',
    'Section 2 parameter and base-field equalities': 'TYPOGRAPHICAL_ERRORS_CORRECTED',
    'Section 2 product and Wilson characterization': 'EXPLICIT_CITED_PREMISE',
    'Section 3 reduction to simple rank four': 'EXPLICIT_CITED_PREMISE',
    'Section 3 normalization of the total product': 'PROVED_WITH_CITED_CONJUGACY',
    'Equation (1) endpoint membership in X': 'PROVED',
    'Symmetry preceding equation (2)': 'PROVED_AND_CONVERSE_ADDED',
    'Equations (3)–(12)': 'PROVED',
    'Product imposed on nonorthogonal pairs': 'REFUTED_AND_DOMAIN_CORRECTED',
    'Repeated basis pair before equations (7)–(20)': 'INDEX_TYPO_IDENTIFIED',
    'Equations (21)–(22)': 'PROVED',
    'Case 3.1': 'PROVED_FOR_STRONGER_SYSTEM',
    'Case 3.2': 'PROVED_FOR_STRONGER_SYSTEM',
    'Case 3.3': 'PROVED_FOR_STRONGER_SYSTEM',
    'Case 3.4': 'PROVED_FOR_STRONGER_SYSTEM',
    'Case 3.5': 'PROVED_FOR_STRONGER_SYSTEM',
    'Case 3.6': 'PROVED_FOR_STRONGER_SYSTEM',
    'Displayed classification X={J} union T': 'REFUTED_AND_STRONGER_SYSTEM_CLASSIFIED',
    'Section 3.7 generation contradiction': 'PROVED_WITH_ADDITIONAL_HYPOTHESIS',
}


def need(value, message):
    if not value:
        raise ValueError(message)


def binding(path, base=None):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path),
                bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def verify(row, base=None):
    path = Path(row['path']) if base is None else base / row['path']
    need(binding(path, base) == row, 'binding changed: ' + str(path))


def ledger_check(ledger):
    need(ledger['source_id'] == 'F003', 'wrong source')
    need(ledger['source_edition'] == 'arXiv:2010.04080v1, 8 October 2020', 'edition changed')
    rows = ledger['claims']
    need(len(rows) == len(EXPECTED), 'missing claim')
    need({r['label']: r['status'] for r in rows} == EXPECTED, 'claim disposition changed')
    for r in rows:
        need(1 <= r['physical_page'] == r['printed_page'] <= 4, 'wrong source page')
        need(all(r[k] for k in ['proof', 'qualification', 'attribution']), 'missing source scope')
    need(ledger['principal_disposition'] == 'principal_statement_refuted', 'principal disposition')
    for k in ['ordinary_recovery_credit', 'new_principal_refutation_credit',
              'new_original_credit', 'new_named_open_questions_solved',
              'new_Lean_declarations', 'new_measurements']:
        need(ledger[k] == 0, 'unearned credit: ' + k)
    need(ledger['public_registration_performed'] is False, 'private stage is not registration')
    need(ledger['principal_acquisition_repeated'] is False, 'no repeated acquisition')
    need(ledger['remaining_fixed_source_claims'] == [], 'assembly incomplete')
    need(len(ledger['borrowed_premises']) == 4, 'borrowed premises hidden')
    need(len(ledger['uncertified_extensions']) == 2, 'scope limits hidden')


def normalized(page):
    return ''.join(page.extract_text().split())


def compare_pdfs(first, second):
    from pypdf import PdfReader
    a, b = PdfReader(first), PdfReader(second)
    need(len(a.pages) == len(b.pages), 'rendered page count mismatch')
    for i, (x, y) in enumerate(zip(a.pages, b.pages)):
        need(normalized(x) == normalized(y), 'rendered page text mismatch: ' + str(i + 1))


def embedded_page_check(source, container):
    # pdfpages preserves literal page streams. Its shared ToUnicode font
    # maps can change extracted text (e.g. a mapsto component 7 to a bar).
    # Compare actual drawing commands and embedded glyph programs instead.
    forms = [x.get_object() for x in container['/Resources']['/XObject'].values()]
    need(len(forms) == 1, 'one imported page form required')
    form = forms[0]
    need(form.get_data() == source.get_contents().get_data(), 'imported page drawing stream changed')
    a, b = source['/Resources']['/Font'], form['/Resources']['/Font']
    need(set(a) == set(b), 'page font resources changed')
    for name in a:
        x, y = a[name].get_object(), b[name].get_object()
        need(x['/Subtype'] == y['/Subtype'], 'font type changed')
        dx, dy = x['/FontDescriptor'].get_object(), y['/FontDescriptor'].get_object()
        for key in ['/FontFile', '/FontFile2', '/FontFile3']:
            need((key in dx) == (key in dy), 'font program presence changed')
            if key in dx:
                need(dx[key].get_data() == dy[key].get_data(), 'glyph program changed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    out = Path(args.out).resolve()
    need(not out.exists() and not out.is_relative_to(P), 'fresh separate output required')
    need(shutil.disk_usage(P).free >= 4 * 1024**3, 'hold below 4GiB reserve')
    dependencies = json.loads((P / 'dependencies.json').read_text())
    for row in dependencies:
        verify(row)
    if (P / 'manifest.json').exists():
        for row in json.loads((P / 'manifest.json').read_text())['exports']:
            verify(row, P)
    ledger = json.loads((P / 'claims.json').read_text())
    ledger_check(ledger)
    verify(ledger['source_pdf'])
    verify(ledger['source_text'])
    scope = json.loads((P / 'quoted_premise_scope.json').read_text())
    need(scope['historical_entry']['id'] == 'L004', 'quoted premise identity')
    need(scope['L004_in_active_corpus'] is False and 'L004' not in scope['active_original_ids'],
         'unavailable chapter cannot acquire source credit')
    principal = R / 'corrections/suzuki-rank/v1/proof/rank4_counterexample'
    for ext in ['.tex', '.pdf']:
        need((P / 'proofs' / ('principal' + ext)).read_bytes() == principal.with_suffix(ext).read_bytes(),
             'accepted principal proof changed')
    gate = json.loads((R / 'audit/principal-refutations/F003/v1/root_integration.json').read_text())
    need(gate['status'] == 'ROOT_ACCEPTED_F003_PRINCIPAL_REFUTATION_PUBLICATION', 'principal acceptance')
    need(gate['principal_refutation_credit'] == 1 and gate['ordinary_recovery_credit'] == 0,
         'principal interface')
    binary = binary_check(MATRIX)
    need(binary == json.loads((P / 'binary_result.json').read_text()), 'literal output changed')
    controls = []
    for name, mutate in [
        ('false_recovery_credit', lambda x: x.update(ordinary_recovery_credit=1)),
        ('missing_source_case', lambda x: x['claims'].pop(11)),
        ('conditional_argument_promoted', lambda x: x['claims'][-1].update(status='PROVED')),
        ('borrowed_premise_hidden', lambda x: x.update(borrowed_premises=[])),
    ]:
        damaged = copy.deepcopy(ledger)
        mutate(damaged)
        try:
            ledger_check(damaged)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError('damaged scope accepted: ' + name)
    for name, bad in [
        ('broken_symmetry', [[0, 0, 0, 1], *copy.deepcopy(MATRIX[1:])]),
        ('identity_has_no_nonzero_defect', [[int(i == j) for j in range(4)] for i in range(4)]),
    ]:
        try:
            binary_check(bad)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError('damaged binary example accepted: ' + name)
    from pypdf import PdfReader
    whole = PdfReader(P / 'complete.pdf')
    pieces = [(P / 'symmetric.pdf', 6), (P / 'proofs/principal.pdf', 5)]
    need(len(whole.pages) == 12, 'whole-volume length')
    offset = 1
    for path, count in pieces:
        part = PdfReader(path)
        need(len(part.pages) == count, 'part length: ' + path.name)
        for i, page in enumerate(part.pages):
            embedded_page_check(page, whole.pages[offset + i])
        offset += count
    for flag in ['-O', '-OO']:
        run = subprocess.run([sys.executable, flag, str(P / 'check.py')],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        need(run.returncode != 0 and b'optimization is not an admitted execution mode' in run.stderr,
             'optimization guard failed')
        controls.append(flag + '_rejected')
    out.mkdir(parents=True)
    runs = []
    if args.render:
        work = out / 'native'
        (work / 'proofs').mkdir(parents=True)
        for rel in ['symmetric.tex', 'complete.tex', 'proofs/principal.pdf', 'proofs/principal.tex']:
            shutil.copyfile(P / rel, work / rel)
        for name in ['symmetric', 'complete']:
            for edition in [1, 2]:
                command = ['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode', '-halt-on-error', name + '.tex']
                start = time.monotonic()
                run = subprocess.run(command, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                (work / (name + '-pass' + str(edition) + '.stdout')).write_bytes(run.stdout)
                (work / (name + '-pass' + str(edition) + '.stderr')).write_bytes(run.stderr)
                need(run.returncode == 0, 'native TeX failed')
                runs.append(dict(command=command, cwd=str(work), returncode=run.returncode,
                                 seconds=time.monotonic() - start))
            log = (work / (name + '.log')).read_text()
            need('Overfull' not in log and 'undefined' not in log, 'native document warning: ' + name)
            compare_pdfs(P / (name + '.pdf'), work / (name + '.pdf'))
        command = ['/opt/homebrew/bin/gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE',
                   '-sDEVICE=png16m', '-r105', '-sOutputFile=' + str(out / 'complete-%02d.png'),
                   str(work / 'complete.pdf')]
        start = time.monotonic()
        run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        (out / 'render.stdout').write_bytes(run.stdout)
        (out / 'render.stderr').write_bytes(run.stderr)
        need(run.returncode == 0, 'native rendering failed')
        need(len(list(out.glob('complete-*.png'))) == 12, 'native pages missing')
        runs.append(dict(command=command, returncode=run.returncode, seconds=time.monotonic() - start))
    for row in dependencies:
        verify(row)
    report = dict(status='PASS_F003_SOURCE_ASSEMBLY', dependencies=len(dependencies),
                  source_claims=19, supplement_pages=6, imported_principal_pages=5,
                  volume_pages=12, complete_page_drawing_streams_and_glyph_programs_match=True,
                  binary_result=binary, controls=controls, runs=runs,
                  general_proofs='REQUIRE_DISTINCT_MATHEMATICAL_REVIEW',
                  principal_acquisition_repeated=False, new_group_searches=0,
                  public_mutations=0, new_Lean=0, measurements=None,
                  outputs=[binding(f, out) for f in sorted(out.rglob('*')) if f.is_file()])
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'dependencies', 'source_claims', 'volume_pages', 'controls']}))


if __name__ == '__main__':
    main()
