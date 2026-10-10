#!/usr/bin/env python3
"""Independent source-contract and raw-triple review; no author helper imports."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

AUTHOR_MANIFEST = 'phase110_commuting_pairs_integration_manifest.json'
AUTHOR_SHA = 'ed62d34e741342ee2da07485a76bea4e3b172fb373a2cb5ad1319fad3cd54c9c'
P = 'phase110_commuting_pairs_integration_'
PREVIOUS = 'phase78_n009_integration_'
REVIEW = 'phase114_commuting_pairs_review_'
CORRECTION_MANIFEST = 'phase116_commuting_pairs_manifest.json'
CORRECTION_SHA = '4975931d45b53a8a388904dec6413b3b4c295dcb9d8e321f98a59e00531cc412'
CORRECTED_LEDGER = 'phase116_commuting_pairs_corrected_ledger.json'

# Independently transcribed from the fully read source and replacement. Section
# endpoints are obtained from global heading matches, not the author builder.
TARGETS = [
    ('Theorem 1.1', '25.2', '25.3', True),
    ('Theorem 1.2', '25.2', '25.3', True),
    ('Proposition 3.1', '25.1', '25.1', False),
    ('Lemma 3.2', '25.2', '25.2', False),
    ('Lemma 3.3', '25.2', '25.2', False),
    ('Remark 3.4', '25.2', '25.4', False),
    ('Definition 3.5', '25.3', '25.3', False),
    ('Theorem 3.6', '25.3', '25.3', True),
    ('Remark 3.7', '25.4', '25.4', False),
    ('Proposition 4.1', '25.1', '25.1', False),
    ('Lemma 4.2', '25.2', '25.2', False),
    ('Lemma 4.3', '25.3', '25.3', False),
    ('Theorem 4.4', '25.3', '25.4', True),
    ('Table 1', '25.4', '25.4', False),
    ('Equation (2)', '25.3', '25.3', False),
    ('Even/odd degree observation', '25.2', '25.2', False),
]


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def binding(base, name):
    data = (base / name).read_bytes()
    return dict(path=name, bytes=len(data), sha256=digest(data))


def load(base, name):
    return json.loads((base / name).read_text())


def check_rows(base, rows):
    if isinstance(rows, dict):
        rows = [dict(path=k, **v) for k, v in rows.items()]
    for row in rows:
        actual = binding(base, row['path'])
        require(actual['sha256'] == row['sha256'], 'Bound hash: ' + row['path'])
        if 'bytes' in row:
            require(actual['bytes'] == row['bytes'], 'Bound bytes: ' + row['path'])


def section_boundaries(text):
    headings = list(re.finditer(r'^#{2,3} (\d+(?:\.\d+)?)\.', text, re.M))
    result = {}
    for i, heading in enumerate(headings):
        key = heading.group(1)
        require(key not in result, 'Duplicate numbered heading')
        result[key] = (heading.start(), headings[i+1].start() if i+1 < len(headings) else len(text))
    return result


def audit_contract(text, prior_text, ledger, prior_ledger):
    old = {r['integration_id']: r for r in prior_ledger['contracts']}
    rows = {r['integration_id']: r for r in ledger['contracts']}
    require(len(old) == 120 and len(rows) == len(ledger['contracts']) == 136,
            'Contract inventory or duplicate identifiers')
    allowed = {'integrated_proof_span', 'previous_integration_proof_span',
               'previous_replacement_file', 'replacement_file'}
    for key, oldrow in old.items():
        row = rows[key]
        require({k: v for k, v in oldrow.items() if k not in allowed} ==
                {k: v for k, v in row.items() if k not in allowed},
                'Retained contract content changed: ' + key)
        p, q = oldrow['integrated_proof_span'], row['integrated_proof_span']
        oldspan = prior_text[p['start_codepoint']:p['end_codepoint_exclusive']]
        newspan = text[q['start_codepoint']:q['end_codepoint_exclusive']]
        require(oldspan == newspan and digest(newspan.encode()) == q['sha256_utf8'],
                'Retained proof changed: ' + key)
    boundaries = section_boundaries(text)
    report = []
    for i, (name, first, last, principal) in enumerate(TARGETS, 1):
        row = rows['L066.' + str(i)]
        require(row['source_reference'] == name and row['principal'] == principal,
                'Source inventory differs: ' + name)
        start, end = boundaries[first][0], boundaries[last][1]
        span = row['integrated_proof_span']
        expected = dict(start_codepoint=start, end_codepoint_exclusive=end,
                        sha256_utf8=digest(text[start:end].encode()))
        require(span == expected, 'Incomplete substantive proof span: ' + name)
        require(end-start > 1000, 'Suspiciously empty proof span')
        report.append(dict(id=row['integration_id'], source=name, **expected))
    require(ledger['manuscript']['sha256'] == digest(text.encode()), 'Ledger manuscript binding')
    return report


def audit_continuity(base, text, prior_text):
    preserved = []
    for n in [1] + list(range(3, 25)):
        pattern = r'^## ' + str(n) + r'\. .*?(?=^## |\Z)'
        old = re.search(pattern, prior_text, re.M | re.S)[0]
        new = re.search(pattern, text, re.M | re.S)[0]
        require(old == new, 'Whole old proof section changed: ' + str(n))
        preserved.append(dict(section=n, sha256=digest(new.encode())))
    code = re.findall(r'^```(gap|python)\n(.*?)^```', text, re.M | re.S)
    oldcode = re.findall(r'^```(gap|python)\n(.*?)^```', prior_text, re.M | re.S)
    require(len(code) == 11 and len(oldcode) == 8 and code[:8] == oldcode,
            'Retained executable continuity')
    for i, name in enumerate(['finite.g', 'formula.py', 'run.py'], 8):
        require(code[i][1] == (base / (P+name)).read_text(), 'Executable appendix content')
    return dict(whole_sections=preserved, unchanged_old_programs=8, total_programs=11)


def arithmetic():
    # Enumerate all ORDERED multiplicity vectors and fixed points of reversal.
    # This differs from the author's x<=y enumeration and series expansion.
    records = []
    coordinates = 0
    for n in range(41):
        ordered = fixed = even_ordered = even_fixed = 0
        for t in range(n//2 + 1):
            for x in range(n-2*t+1):
                for y in range(n-2*t-x+1):
                    for z in range(n-2*t-x-y+1):
                        if not (t or (x > 0)+(y > 0)+(z > 0) >= 2):
                            continue
                        ordered += 1
                        fixed += x == y
                        even = (x+z) % 2 == (y+z) % 2 == 0
                        even_ordered += even
                        even_fixed += even and x == y
                        k, l = y+z+2*t, z+2*t
                        require(1 <= k <= n and 0 <= l <= k and 0 <= t <= l//2
                                and 0 <= x <= n-k, 'Forward coordinate range')
                        require((k-l, l-2*t) == (y, z), 'Coordinate inverse')
                        coordinates += 1
        lam = lambda k: ((k+2)**2)//4
        def omitted(k):
            h = max(0, 2*k-n)
            return sum(j//2+1 for j in range(h))
        ordered_formula = sum(lam(k)*(n-k+1)-2 for k in range(1, n+1))
        fixed_formula = sum(lam(k)-omitted(k)-1 for k in range(1, n+1))
        even_formula = 0
        even_fixed_formula = 0
        for k in range(2, n+1, 2):
            gamma = Fraction(k*k, 8) + Fraction(3*k, 4) + 1
            delta = Fraction(k*k, 8) + Fraction(k, 4)
            even_formula += gamma*((n-k+2)//2) + delta*((n-k+1)//2)-2
            even_fixed_formula += lam(k)-omitted(k)-1
        require((ordered, fixed, even_ordered, even_fixed) ==
                (ordered_formula, fixed_formula, even_formula, even_fixed_formula),
                'Independent multiplicity/floor disagreement at ' + str(n))
        require((ordered+fixed) % 2 == (even_ordered+even_fixed) % 2 == 0,
                'Reversal orbit parity')
        records.append(dict(half_degree=n, ordered=ordered, fixed=fixed,
                            even_ordered=even_ordered, even_fixed=even_fixed,
                            unordered=(ordered+fixed)//2,
                            even_unordered=(even_ordered+even_fixed)//2))
    printed = [('1,2,3',0,0),('4,5',3,1),('6',5,1),('7',9,2),('8,9',21,7),
               ('10,11',39,10),('12,13',67,21),('14,15',105,28),('16,17',158,48),
               ('18,19',226,61),('20',315,93),('30',1169,315),('40',3105,855),('50',6774,1795)]
    for degrees, sym, alt in printed:
        for degree in map(int, degrees.split(',')):
            if degree == 6:
                continue  # proved by separate complete finite-group census
            require((records[degree//2]['unordered'], records[degree//2]['even_unordered']) ==
                    (sym, alt), 'Source table arithmetic')
    return dict(half_degrees=[0,40], records=records, coordinate_vectors=coordinates,
                table_rows=14, degree_six='Independent raw GAP census',
                scope='Bounded controls only; the written all-parameter proof is reviewed separately')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--primary-check', action='store_true')
    args = parser.parse_args()
    require(not os.path.lexists(args.output_dir), 'Refusing existing output directory')
    base = args.base.resolve()
    require(digest((base/AUTHOR_MANIFEST).read_bytes()) == AUTHOR_SHA, 'Author manifest hash')
    author = load(base, AUTHOR_MANIFEST)
    check_rows(base, author['files'])
    check_rows(base, author['retained_public_runtime_bindings'])
    require(CORRECTION_MANIFEST and CORRECTION_SHA and CORRECTED_LEDGER,
            'Review is not frozen until the independent correction review is complete')
    require(digest((base/CORRECTION_MANIFEST).read_bytes()) == CORRECTION_SHA,
            'Correction manifest hash')
    correction = load(base, CORRECTION_MANIFEST)
    check_rows(base, correction['files'])
    text = (base/(P+'manuscript.md')).read_text()
    oldtext = (base/(PREVIOUS+'manuscript.md')).read_text()
    ledger = load(base, CORRECTED_LEDGER)
    original_ledger = load(base, P+'ledger.json')
    for key in set(ledger) | set(original_ledger):
        if key not in {'schema', 'proof_span_correction', 'contracts'}:
            require(ledger.get(key) == original_ledger.get(key), 'Correction changed extra metadata')
    require(ledger['contracts'][:120] == original_ledger['contracts'][:120],
            'Correction changed a retained full contract row')
    for row, oldrow in zip(ledger['contracts'][120:], original_ledger['contracts'][120:]):
        require({k:v for k,v in row.items() if k != 'integrated_proof_span'} ==
                {k:v for k,v in oldrow.items() if k != 'integrated_proof_span'},
                'Correction changed a source claim')
    oldledger = load(base, PREVIOUS+'ledger.json')
    spans = audit_contract(text, oldtext, ledger, oldledger)
    continuity = audit_continuity(base, text, oldtext)
    try:
        audit_contract(text, oldtext, load(base, P+'ledger.json'), oldledger)
    except RuntimeError as exc:
        original_rejection = str(exc)
    else:
        raise RuntimeError('Known original ledger defect was accepted')
    private = []
    if args.primary_check:
        check_rows(base, author['private_source_bindings_not_exported'])
        private = author['private_source_bindings_not_exported']
    args.output_dir.mkdir(parents=True)
    started = time.monotonic()
    direct = Path(__file__).with_name(REVIEW+'direct.g')
    gap = shutil.which('gap')
    require(gap is not None, 'GAP is required')
    result = subprocess.run([gap, '-q', str(direct)], capture_output=True, text=True)
    (args.output_dir/'direct.log').write_text(result.stdout)
    (args.output_dir/'direct.stderr').write_text(result.stderr)
    require(result.returncode == 0 and not result.stderr.strip() and
            result.stdout.rstrip().endswith('PASS'), 'Independent raw census process failed')
    direct_rows = []
    for line in result.stdout.splitlines():
        if line.startswith('DIRECT|'):
            values = line.split('|')[1:]
            direct_rows.append([int(v) for v in values[:8]] +
                               [json.loads(v) for v in values[8:]])
    require(direct_rows == [[720,1440,75,495,37125,2160,138240,2,[720,1440],
                            [[[5,6],1440],[[6,6],720]]],
                            [360,1440,45,90,4050,0,0,0,[],[]]], 'Independent raw result')
    counts = arithmetic()
    report = dict(status='PASS',author_manifest_sha256=AUTHOR_SHA,
                  correction_manifest_sha256=CORRECTION_SHA,
                  manuscript=binding(base,P+'manuscript.md'),
                  corrected_ledger=binding(base,CORRECTED_LEDGER),
                  source_contracts=spans,prior_contracts_exact=120,
                  continuity=continuity,original_ledger_rejected=original_rejection,
                  direct_census=direct_rows,arithmetic=counts,
                  primary_assets_checked=private,private_primary_check_skipped=not args.primary_check,
                  gap_version=next(x.split('|')[1] for x in result.stdout.splitlines() if x.startswith('VERSION|')),
                  elapsed_seconds=round(time.monotonic()-started,6),
                  trusted_infrastructure='GAP exact group, subgroup, intersection, automorphism and orbit algorithms',
                  mathematical_review='See the independently written phase114 review; this executable is not a formal proof of every written theorem',
                  new_Lean_claim=False,compression_factor=None,historical_novelty_claim=False)
    (args.output_dir/'check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',raw_extension_candidates=41175,
                         raw_generating_triples=2160,actual_IP_meets=138240,
                         corrected_source_spans=16,prior_contracts_exact=120,
                         elapsed_seconds=report['elapsed_seconds'])))


if __name__ == '__main__':
    main()
