#!/usr/bin/env python3
"""Exact diagnostic of the printed thesis marking; not an existence test.

Standard library only. The matrix identity is over Z and therefore applies
in every odd characteristic. No source text or PDF is bundled.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
from math import gcd


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def diag(v):
    return [[v[i] if i == j else 0 for j in range(4)] for i in range(4)]


alpha = diag([-1, 1, -1, 1])
beta = [[0, -1, 0, 0], [1, 0, 0, 0],
        [0, 0, 0, 1], [0, 0, 1, 0]]
one = diag([1, 1, 1, 1])
beta2 = mul(beta, beta)
assert beta2 == diag([-1, -1, 1, 1])
assert mul(beta2, beta2) == one
assert beta2[2][2] - beta2[0][0] == 2
assert mul(alpha, alpha) == one
assert mul(alpha, beta) == [[-x for x in row] for row in mul(beta, alpha)]

# For a cyclic scalar group of order m=q-1, these are exact subgroup sizes.
# The written proof identifies the groups uniformly, without relying on this
# bounded integer sweep.
rows = []
for q in [3, 5, 7, 9, 13, 17, 25, 41]:
    m = q - 1
    center_sl = gcd(4, m)
    center_det_pm = gcd(8, m)
    scalar_kernel = center_det_pm // center_sl
    determinant_image_order = center_sl // gcd(center_sl, m // 2)
    if q % 8 == 1:
        assert (scalar_kernel, determinant_image_order) == (2, 1)
    else:
        assert (scalar_kernel, determinant_image_order) == (1, 2)
    rows.append(dict(q=q, center_sl_order=center_sl,
                     center_det_pm_order=center_det_pm,
                     kernel_to_projective_image=scalar_kernel,
                     projective_image_index_over_psl=determinant_image_order))

here = Path(__file__).resolve()
report = {
    "schema_version": 1,
    "executed_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS",
    "checker_sha256": sha256(here.read_bytes()).hexdigest(),
    "scope": "Exact integer square of the displayed beta on thesis p72; bounded scalar-group diagnostics supporting the separate uniform written quotient calculation.",
    "integer_identities_checked": 5,
    "beta_squared": beta2,
    "universal_odd_characteristic_obstruction": "Two diagonal entries differ by 2, hence beta squared is never scalar in odd characteristic. Its coset modulo Z(SL4(q)) has order 4.",
    "scalar_quotient_diagnostics": rows,
    "not_claimed": ["The thesis existence theorem is false", "The displayed marking can be repaired by a particular change", "Publication priority", "Full proof validation of the thesis"]
}
here.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
print("PASS: five integer identities and eight scalar-quotient diagnostics")
