#!/usr/bin/env python3
"""Independent sparse integer/permutation check of the frozen phase66 proof data.

Reads JSON data and saved fresh replay evidence. Does not import author helpers,
rerun GAP, or use floating-point, finite-field, or Smith-normal-form arithmetic.
"""
import argparse
import ast
from collections import Counter, deque
import hashlib
import itertools
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "phase74_coprime_cover_recent_audit"


def bind(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists() or args.report.is_symlink():
        raise FileExistsError("Existing report refused")
    inputs = {}
    for name, expected_hash in [
        ("phase66_coprime_cover_manifest.json", "ff1082c12f183e27150bac0baa1ec25d648cb53152abe150a8f445ee0a4a1c50"),
        ("phase73_2primary_cover_recent_audit_manifest.json", "2b814f3464b0d49da03f03e5e6dfc5cf1923ff400f449a4c943b94ff61ec07e1")]:
        assert bind(ROOT / name)["sha256"] == expected_hash
        inputs[name] = bind(ROOT / name)
        manifest = json.loads((ROOT / name).read_text())
        for filename, expected in manifest["files"].items():
            assert bind(ROOT / filename) == expected, filename
            inputs[filename] = expected
    model = json.loads((ROOT / "phase66_coprime_cover_permutation_model.json").read_text())
    certificate = json.loads((ROOT / "phase66_coprime_cover_coefficients.json").read_text())["terms"]
    assert model["degree"] == 128 and model["distinguished_coset"] == 1
    gens = [tuple(permutation) for permutation in model["generators"]]
    identity = tuple(range(1, 129))
    assert len(gens) == 4 and all(sorted(g) == list(identity) for g in gens)

    def product(left, right):
        return tuple(right[i-1] for i in left)

    def inverse(p):
        result = [0] * 128
        for i, target in enumerate(p, 1):
            result[target-1] = i
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
        seen = {identity}
        queue = deque([identity])
        while queue:
            current = queue.popleft()
            for g in generators:
                new = product(current, g)
                if new not in seen:
                    seen.add(new)
                    queue.append(new)
        return seen

    def word(indices):
        current = identity
        for i in indices:
            assert type(i) is int and 1 <= i <= 4
            current = product(current, gens[i-1])
        return current

    assert all(product(g, g) == identity for g in gens)
    assert all(product(gens[i], gens[j]) == product(gens[j], gens[i])
               for i in range(4) for j in range(i+2, 4))
    group = closure(gens)
    medial = closure(gens[1:3])
    stabilizer = {g for g in group if g[0] == 1}
    assert len(group) == 1024 and len(medial) == 8 and stabilizer == medial
    assert {g[0] for g in group} == set(identity)
    a, b, c = [product(gens[i], gens[i+1]) for i in range(3)]
    assert power(a, 8) == power(b, 4) == power(c, 8) == identity
    w1 = product(product(b, power(a, 2)), inverse(product(power(a, 2), b)))
    w2 = product(product(power(c, 2), b), inverse(product(b, power(c, 2))))
    assert w1 == w2 and power(w1, 2) == identity
    assert all(product(w1, g) == product(g, w1) for g in (a, b, c))
    y_group = power(c, 2)
    z = product(product(product(inverse(y_group), inverse(b)), y_group), b)
    assert z == word(model["z_word_1based"])
    assert z not in medial and all(product(z, g) == product(g, z) for g in medial)
    intersection = closure(gens[:3]) & closure(gens[1:])
    assert intersection == closure(gens[1:3] + [z]) and len(intersection) == 16

    # Signed sparse sums; Counter subtraction is deliberately not used, since
    # it drops negative coefficients. Every update below is an integer update.
    def cleaned(vector):
        return {index: value for index, value in vector.items() if value}

    def difference(left, right):
        output = Counter(left)
        for index, value in right.items():
            output[index] -= value
        return cleaned(output)

    def act(vector, permutation):
        output = Counter()
        for index, value in vector.items():
            output[permutation[index-1]] += value
        return cleaned(output)

    unit = {1: 1}
    y = difference(unit, act(unit, gens[3]))
    y = difference(y, act(y, gens[0]))
    d = difference(act(unit, z), unit)
    assert d
    assert len(certificate) == 55
    embedded = ast.literal_eval((ROOT / "phase66_coprime_cover_check.g").read_text().split("terms:=", 1)[1].split(";;", 1)[0])
    assert certificate == embedded
    total = Counter()
    for coefficient, indices in certificate:
        assert type(coefficient) is int
        contribution = act(y, word(indices))
        for index, value in contribution.items():
            total[index] += coefficient * value
    assert cleaned(total) == {i: 2*n for i, n in d.items()}

    replay_file, log_file = PREFIX + "_replay.json", PREFIX + "_replay.log"
    replay = json.loads((ROOT / replay_file).read_text())
    log = (ROOT / log_file).read_text()
    assert replay["status"] == "PASS" and replay["GAP_version"] == "4.15.1"
    assert replay["runner_sha256"] == inputs["phase66_coprime_cover_check.py"]["sha256"]
    assert replay["log_sha256"] == bind(ROOT / log_file)["sha256"]
    assert (ROOT / log_file).read_bytes() == (ROOT / "phase66_coprime_cover_check.log").read_bytes()
    for filename, expected in replay["inputs_pre_post_sha256"].items():
        assert bind(ROOT / filename)["sha256"] == expected
        inputs[filename] = bind(ROOT / filename)
    flat = re.sub(r"\s+", " ", log.replace("\\\n", ""))
    rows = re.findall(r'INTEGRAL_PASS \[ (\d+), (-?\d+), (-?\d+) \] terms 55 full (\d+) quotient 1024', flat)
    assert [tuple(map(int, row[:3])) for row in rows] == list(itertools.product([5,6], [-1,1], [-1,1]))
    assert all(int(row[3]) == 256 * 2**int(row[0]) for row in rows)
    assert 'SMITH_PASS 0^7 1^120 2^1' in flat and 'PASS COPRIME_INTEGRAL_CERTIFICATE 8' in flat
    outputs = {n: bind(ROOT / n) for n in (replay_file, log_file)}
    refusal = subprocess.run(["/Users/sasha/.venvs/global/bin/python", str(ROOT / "phase66_coprime_cover_check.py"),
                              "--report", str(ROOT / replay_file), "--log", str(ROOT / log_file)],
                             capture_output=True, text=True, timeout=10)
    assert refusal.returncode != 0 and "fresh output paths required" in refusal.stderr
    assert all(bind(ROOT / n) == value for n, value in outputs.items())
    assert all(bind(ROOT / n) == value for n, value in inputs.items())
    result = {
        "schema": "phase74_independent_sparse_integral_certificate_v1", "status": "PASS",
        "checker": bind(Path(__file__)), "bound_inputs": inputs,
        "independent_implementation": "No author helper imports. One-based tuple permutations, closure by deque, signed sparse integer accumulation; no finite-field or floating-point tests.",
        "group_order": len(group), "permutation_degree": 128,
        "medial_order": len(medial), "medial_equals_full_point_stabilizer": True,
        "marked_small_quotient_relations_verified": True,
        "end_intersection_order": len(intersection), "defect_word_exact": True,
        "terms": 55, "literal_embedded_coefficient_identity": True, "multiplier": 2,
        "sparse_y": y, "sparse_d": d, "sparse_sum": cleaned(total),
        "fresh_author_runner_replay": outputs, "seconds_GAP": replay["seconds_GAP"],
        "eight_source_binding_cases_checked": True, "exact_original_log_match": True,
        "fresh_Smith_diagnostic_from_GAP": "1^120, 2^1, 0^7; auxiliary only",
        "reviewer_independent_Smith_reimplementation": False,
        "fresh_refusal_test": {"returncode": refusal.returncode, "stderr": refusal.stderr,
                               "two_existing_outputs_unchanged": True},
        "all_bound_inputs_unchanged": True,
        "phase58_dependency_independently_admitted_by_phase73": True,
        "uniform_mathematical_transport_is_separate_written_review": True,
    }
    with args.report.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "report": str(args.report), **bind(args.report),
                      "identity": cleaned(total)}, indent=2))


if __name__ == "__main__":
    main()
