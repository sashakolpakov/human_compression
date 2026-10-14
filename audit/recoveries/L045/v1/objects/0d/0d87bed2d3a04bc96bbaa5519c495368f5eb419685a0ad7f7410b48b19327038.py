"""Exact arithmetic for the explicitly retained character-table inputs.

This verifies class arithmetic and the counting theorem's numerical premises.
It does not derive sporadic classifications or maximal-list completeness.
"""
from collections import Counter
from fractions import Fraction
import argparse
import copy
import json
from pathlib import Path

if not __debug__:
    raise SystemExit("Run without Python optimization.")

TARGETS = [
    ("J4", "J4", 41, 29), ("Fi23", "Fi23", 80, 23),
    ("Fi24'", "Fi24", 88, 29), ("M", "M", 169, 71),
    ("B", "B", 172, 47), ("Th", "Th", 42, 31),
    ("Ly", "Ly", 45, 37), ("Co1", "Co1", 78, 23),
    ("Co2", "Co2", 53, 23), ("Co3", "Co3", 38, 23),
    ("Ru", "Ru", 35, 29), ("Fi22", "Fi22.2", 49, 13),
    ("ON", "ON.2", 29, 31), ("HN", "HN.2", 37, 19),
]


def need(test, message):
    if not test:
        raise ValueError(message)


def class_table(raw):
    name, identity, order, orders, sizes, centralizers, inverse, maximal = raw
    n = len(orders)
    need(type(order) is int and order > 1 and n > 0, "finite group order")
    need(len(sizes) == len(centralizers) == len(inverse) == n, "full class arrays")
    need(all(type(x) is int and x > 0 for x in orders + sizes + centralizers),
         "positive integral class data")
    need(sum(sizes) == order, "class sizes partition group")
    need(all(s * c == order for s, c in zip(sizes, centralizers)),
         "class centralizer equation")
    need(all(order % d == 0 for d in orders), "element orders divide group order")
    need(orders.count(1) == 1 and sizes[orders.index(1)] == 1, "identity class")
    need(sorted(inverse) == list(range(1, n + 1)), "inverse permutes classes")
    for i, j in enumerate(inverse):
        need(inverse[j - 1] == i + 1 and orders[j - 1] == orders[i]
             and sizes[j - 1] == sizes[i], "inverse class data")
    counts = Counter()
    for d, s in zip(orders, sizes):
        counts[d] += s
    return dict(name=name, identity=identity, order=order, orders=orders,
                sizes=sizes, centralizers=centralizers, inverse=inverse,
                maximal=maximal, counts=counts)


def verify(data):
    schema, gap_version, library_version, raw_tables, rows = data
    need(schema == "sporadic-counting-inputs-v1" and gap_version == "4.15.1"
         and library_version == "1.3.11", "recorded input edition")
    tables = {}
    for raw in raw_tables:
        t = class_table(raw)
        need(t["name"] not in tables, "unique query names")
        tables[t["name"]] = t
    need([tuple(r[:4]) for r in rows] == TARGETS, "fourteen specified classes")
    results = []
    for row in rows:
        gn, an, cl, p, lower, fusion, inner, omitted, details, claimed_b, claimed_mu, claimed_r, claimed_i2, claimed_real = row
        g, a = tables[gn], tables[an]
        need(p > 2 and all(p % d for d in range(2, int(p ** 0.5) + 1))
             and g["orders"][cl - 1] == p, "selected odd prime class")
        need(g["maximal"] and a["maximal"], "complete maximal lists supplied")
        need(len(fusion) == len(g["orders"]) and
             all(type(j) is int and 1 <= j <= len(a["orders"]) for j in fusion),
             "complete inclusion fusion")
        for i, j in enumerate(fusion):
            need(g["orders"][i] == a["orders"][j - 1], "fusion preserves orders")
            need(a["centralizers"][j - 1] % g["centralizers"][i] == 0,
                 "inclusion of class centralizers")
            need(fusion[g["inverse"][i] - 1] == a["inverse"][j - 1],
                 "fusion commutes with inversion")
        inv_rows = []
        if gn == an:
            need(fusion == list(range(1, len(fusion) + 1)), "identity fusion")
        else:
            need(a["order"] == 2 * g["order"], "index two automorphism extension")
            for i, d in enumerate(g["orders"]):
                if d == 2:
                    gc, ac = g["centralizers"][i], a["centralizers"][fusion[i] - 1]
                    need(ac == 2 * gc, "outer centralizer for every inner involution")
                    inv_rows.append([i + 1, fusion[i], gc, ac])
        need(inner == inv_rows, "complete involution interface ledger")
        b, computed_details = Fraction(0), []
        for name in g["maximal"]:  # Do not deduplicate subgroup classes.
            need(name in tables, "every maximal table supplied")
            m = tables[name]
            need(m["order"] < g["order"] and g["order"] % m["order"] == 0,
                 "proper G maximal order")
            over = Fraction(g["centralizers"][cl - 1] * m["counts"][p], m["order"])
            b += over * m["counts"][2]
            computed_details.append([name, m["counts"][p], m["counts"][2],
                                     over.numerator, over.denominator])
        need(details == computed_details, "every maximal class retained in ledger")
        mu, socle = 0, []
        for name in a["maximal"]:
            need(name in tables, "every maximal table supplied")
            m = tables[name]
            need(m["order"] < a["order"] and a["order"] % m["order"] == 0,
                 "proper A maximal order")
            if gn != an and m["identity"] == g["identity"]:
                need(m["order"] == g["order"], "identified socle order")
                socle.append(name)
            else:
                mu = max(mu, m["counts"][2])
        need(socle == omitted and len(socle) == (gn != an), "unique identified socle omission")
        j = fusion[cl - 1]
        real = a["inverse"][j - 1] == j
        r = a["centralizers"][j - 1] * mu if real else 0
        i2 = g["counts"][2]
        need([b.numerator, b.denominator] == claimed_b and mu == claimed_mu
             and r == claimed_r and i2 == claimed_i2 and real == claimed_real,
             "independently recomputed bounds agree")
        need(type(lower) is int and lower <= i2, "valid displayed lower bound")
        need(b + r < lower, "strict counting inequality")
        results.append(dict(group=gn, aut=an, prime=p, class_index=cl,
                            involutions=i2, displayed_lower=lower,
                            generation_bound=[b.numerator, b.denominator],
                            mu=mu, reversal_bound=r, real_in_aut=real,
                            maximal_classes=len(g["maximal"]),
                            involution_interfaces=inv_rows))
    return dict(status="PASS", cases=results, bound_tables=len(tables),
                whole_original_credit=0, new_conjecture_credit=0,
                new_lean_credit=0, new_measurement_credit=0)


def controls(data):
    outcomes = []
    def reject(name, mutate, reason):
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            verify(changed)
        except ValueError as error:
            need(str(error) == reason, "wrong control rejection: " + name + ": " + str(error))
            outcomes.append(dict(control=name, rejection=str(error)))
        else:
            raise ValueError("control incorrectly accepted: " + name)
    reject("wrong_prime_class", lambda d: d[3][0][3].__setitem__(40, 1),
           "identity class")
    reject("damaged_class_size", lambda d: d[3][0][4].__setitem__(0, 2),
           "class sizes partition group")
    reject("missing_maximal_table", lambda d: d[3].pop(next(i for i, t in enumerate(d[3]) if t[0] == d[3][0][7][0])),
           "every maximal table supplied")
    reject("missing_involution_interface", lambda d: d[4][2][6].pop(),
           "complete involution interface ledger")
    reject("dropped_maximal_class", lambda d: d[3][0][7].pop(),
           "every maximal class retained in ledger")
    reject("equality_instead_of_strictness", lambda d: d[4][0].__setitem__(4, d[4][0][9][0] + d[4][0][11]),
           "strict counting inequality")
    return outcomes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = json.loads(args.data.read_text())
    report = verify(data)
    report["negative_controls"] = controls(data)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: 14 exact counting cases and 6 mathematical controls")


if __name__ == "__main__":
    main()
