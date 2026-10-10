#!/usr/bin/env python3
"""Replay the reviewed two-primary construction, finite census and integer obstruction.

Uses only distributed original proofs, reviews, programs and data. The written
parameter reductions are not machine checked. The integer model check below
adapts the independently authored phase74 sparse checker; GAP programs are
executed byte for byte. Historical author wrappers are not invoked.
"""
import argparse
import ast
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

REVIEWS = {
    'phase73_2primary_cover_recent_audit_manifest.json': '2b814f3464b0d49da03f03e5e6dfc5cf1923ff400f449a4c943b94ff61ec07e1',
    'phase74_coprime_cover_recent_audit_manifest.json': '749d3f79c57f255b1e62bf9c702232658623e4fe58487255f606c31d9bd59a0a',
}
PROGRAMS = ['phase58_2primary_cover_check.g',
            'phase58_2primary_cover_extension_check.g',
            'phase66_coprime_cover_check.g']
EXPECTED_LOGS = {
    'construction.log': '1f3bba0c157b740812e7a6a3d429c70ec42282466e18893f7a332987d8b7bff2',
    'coprime.log': '4500327a51a025851187205c0176811666d72475f9c37277d452a5427cc924be',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def bind_inputs(root):
    bound = dict(REVIEWS)
    for name, expected in REVIEWS.items():
        raw = (root / name).read_bytes()
        require(digest(raw) == expected, 'Reviewed manifest changed: ' + name)
        for filename, info in json.loads(raw)['files'].items():
            require(Path(filename).name == filename, 'Unexpected nested input')
            if filename in bound:
                require(bound[filename] == info['sha256'], 'Conflicting binding')
            bound[filename] = info['sha256']
    for name, expected in bound.items():
        require(digest((root / name).read_bytes()) == expected,
                'Reviewed input changed: ' + name)
    return bound


def verify_integer_model(root):
    """Exact one-based permutation and signed integer check, adapted from phase74."""
    model = json.loads((root / 'phase66_coprime_cover_permutation_model.json').read_text())
    terms = json.loads((root / 'phase66_coprime_cover_coefficients.json').read_text())['terms']
    require(model['degree'] == 128 and model['distinguished_coset'] == 1, 'Coset model')
    identity = tuple(range(1, 129))
    gens = [tuple(g) for g in model['generators']]
    require(len(gens) == 4 and all(sorted(g) == list(identity) for g in gens), 'Permutations')

    def product(left, right):
        return tuple(right[i - 1] for i in left)

    def inverse(p):
        result = [0] * 128
        for i, target in enumerate(p, 1):
            result[target - 1] = i
        return tuple(result)

    def power(p, exponent):
        result = identity
        while exponent:
            if exponent & 1:
                result = product(result, p)
            p = product(p, p)
            exponent //= 2
        return result

    def closure(generators):
        seen, queue = {identity}, deque([identity])
        while queue:
            current = queue.popleft()
            for g in generators:
                new = product(current, g)
                if new not in seen:
                    seen.add(new)
                    queue.append(new)
        return seen

    def word(indices):
        result = identity
        for i in indices:
            require(type(i) is int and 1 <= i <= 4, 'Word index')
            result = product(result, gens[i - 1])
        return result

    require(all(product(g, g) == identity for g in gens), 'Involutions')
    require(all(product(gens[i], gens[j]) == product(gens[j], gens[i])
                for i in range(4) for j in range(i + 2, 4)), 'String commutations')
    group, medial = closure(gens), closure(gens[1:3])
    require(len(group) == 1024 and len(medial) == 8, 'Group orders')
    require({g for g in group if g[0] == 1} == medial, 'Exact stabilizer')
    require({g[0] for g in group} == set(identity), 'Transitivity')
    a, b, c = [product(gens[i], gens[i + 1]) for i in range(3)]
    require(power(a, 8) == power(b, 4) == power(c, 8) == identity, 'Rotation orders')
    w1 = product(product(b, power(a, 2)), inverse(product(power(a, 2), b)))
    w2 = product(product(power(c, 2), b), inverse(product(b, power(c, 2))))
    require(w1 == w2 and power(w1, 2) == identity, 'Small quotient relators')
    require(all(product(w1, g) == product(g, w1) for g in (a, b, c)), 'Central relator')
    z = product(product(product(inverse(power(c, 2)), inverse(b)), power(c, 2)), b)
    require(z == word(model['z_word_1based']), 'Exact defect word')
    require(z not in medial and all(product(z, g) == product(g, z) for g in medial),
            'Nontrivial central medial defect')
    intersection = closure(gens[:3]) & closure(gens[1:])
    require(intersection == closure(gens[1:3] + [z]) and len(intersection) == 16,
            'Exact end intersection')

    def cleaned(v):
        return {i: value for i, value in v.items() if value}

    def difference(left, right):
        result = Counter(left)
        for i, value in right.items():
            result[i] -= value
        return cleaned(result)

    def act(v, p):
        result = Counter()
        for i, value in v.items():
            result[p[i - 1]] += value
        return cleaned(result)

    unit = {1: 1}
    y = difference(unit, act(unit, gens[3]))
    y = difference(y, act(y, gens[0]))
    d = difference(act(unit, z), unit)
    require(bool(d) and len(terms) == 55, 'Nonzero defect and 55 terms')
    embedded = ast.literal_eval((root / PROGRAMS[2]).read_text().split('terms:=', 1)[1].split(';;', 1)[0])
    require(terms == embedded, 'Literal JSON/GAP coefficient identity')
    total = Counter()
    for coefficient, indices in terms:
        require(type(coefficient) is int, 'Integer coefficient')
        for i, value in act(y, word(indices)).items():
            total[i] += coefficient * value
    require(cleaned(total) == {i: 2 * value for i, value in d.items()}, 'Integral identity 2d')
    return dict(status='PASS', model_order=1024, degree=128, medial_order=8,
                medial_equals_stabilizer=True, terms=55, multiplier=2,
                sparse_y=y, sparse_d=d, sparse_sum=cleaned(total),
                method='Exact integer arithmetic; adapted from independent phase74 checker.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--timeout', type=float, default=1200)
    args = parser.parse_args()
    output = args.output_dir.absolute()
    if output.exists() or output.is_symlink():
        parser.error('output path exists; refusing to overwrite')
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    bound = bind_inputs(args.input_root)
    gap = shutil.which(args.gap)
    if gap is None:
        raise RuntimeError('Stock GAP executable unavailable')
    integer_model = verify_integer_model(args.input_root)
    output.mkdir(parents=True, exist_ok=False)
    runs, normalized = [], []
    for name in PROGRAMS:
        local = output / name
        local.write_bytes((args.input_root / name).read_bytes())
        command = [gap, '-q', name]
        started = time.monotonic()
        timed_out = False
        try:
            run = subprocess.run(command, cwd=output, capture_output=True, timeout=args.timeout)
            stdout, stderr, exit_code = run.stdout, run.stderr, run.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, exit_code = exc.stdout or b'', exc.stderr or b'', None
            timed_out = True
        elapsed = time.monotonic() - started
        (output / (name + '.stdout.log')).write_bytes(stdout)
        (output / (name + '.stderr.log')).write_bytes(stderr)
        canonical = stdout.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
        normalized.append(canonical)
        runs.append(dict(program=name, command=command, exit_code=exit_code,
                         timed_out=timed_out, elapsed_seconds=elapsed,
                         stdout_sha256=digest(stdout), stderr_sha256=digest(stderr),
                         passed=not timed_out and exit_code == 0 and not stderr
                         and not re.search(r'FAIL|Error,|Syntax error|SKIP_', canonical)))
        if not runs[-1]['passed']:
            break
    logs = {}
    if len(normalized) >= 2:
        logs['construction.log'] = ''.join('FILE ' + PROGRAMS[i] + '\n' + normalized[i] for i in range(2))
    if len(normalized) == 3:
        logs['coprime.log'] = 'PYTHON INTEGER MODEL PASS order1024 degree128 terms55 multiplier2\n' + normalized[2]
    for name, value in logs.items():
        (output / name).write_bytes(value.encode())
    log_matches = {name: name in logs and digest(logs[name].encode()) == expected
                   for name, expected in EXPECTED_LOGS.items()}
    unchanged = all(digest((args.input_root / name).read_bytes()) == expected
                    for name, expected in bound.items())
    unchanged = unchanged and all(digest((output / row['program']).read_bytes()) == bound[row['program']]
                                  for row in runs)
    version = re.search(r'GAP_VERSION (\S+)', normalized[2]) if len(normalized) == 3 else None
    passed = (len(runs) == 3 and all(row['passed'] for row in runs)
              and all(log_matches.values()) and unchanged
              and version is not None and version.group(1) == '4.15.1')
    report = dict(
        date='2026-10-10', status='PASS' if passed else 'FAIL',
        runner_sha256=digest(Path(__file__).read_bytes()), bound_inputs=bound,
        all_bound_inputs_and_executed_copies_unchanged=unchanged,
        GAP_version=version.group(1) if version else None, runs=runs,
        expected_log_sha256=EXPECTED_LOGS, exact_prior_log_matches=log_matches,
        canonicalization='UTF-8; only CRLF and bare CR converted to LF.',
        integer_model=integer_model,
        finite_census=dict(beta=5, eps1=1, eps2=1, degree_two=1,
                           degree_four_cyclic=16, degree_four_central_V4=2,
                           degree_four_noncentral_V4=11, new_minimal_degree_four=0),
        scope='Exact replay of eight construction diagnostics, complete degree-two/four census only at beta5 signs++, and the fixed integer obstruction with eight source cross-checks. All-parameter transport is a separate written proof.',
        mathematical_scope_machine_checked=False, primary_source_captures_required=False,
        trusted_computation='Stock GAP 4.15.1 exact algorithms and Python integer arithmetic.',
        new_Lean_build=False, global_uniqueness_claim=False, historical_priority_claim=False)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], report=str(output / 'report.json'),
                         exact_prior_log_matches=log_matches,
                         seconds=sum(row['elapsed_seconds'] for row in runs)), indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
