"""Filter the twelve acquired primitive exceptions, without a group library."""
import argparse
import json
from pathlib import Path
import sys
import permutation_library as lib

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def character(marks):
    values = {tuple(range(len(marks[0]))): 0}
    todo = list(values); consistent = True
    while todo:
        p = todo.pop()
        for j, q in enumerate(marks):
            t = lib.multiply(p,q); value = values[p] ^ (j == 0)
            if t in values:
                if values[t] != value:
                    consistent = False
            else:
                values[t] = value; todo.append(t)
    return values, consistent

def run(data):
    rows = data["representatives"]
    lib.need(len(rows) == 12 and [r["source_index"] for r in rows] == list(range(12)), "incomplete primitive classification")
    tested = []; surviving = []
    for row in rows:
        n = row["n"]; marks = lib.parse_marks(row,n,len(row["permutations"]))
        for orientation, ss in enumerate((marks, marks[::-1])):
            chars, consistent = character(ss); tail = lib.closure(ss[1:])
            points = lib.anchors(ss); valid = []
            for a in points:
                x = next(x for x in range(n) if x != a)
                orbit = {p[x] for p in tail}
                if len(orbit) == n-1:
                    valid.append(a+1)
                    if consistent:
                        surviving.append({"source_index":row["source_index"], "orientation":orientation,
                            "anchor":a+1,"degree":n,"rank":len(ss),"group_order":len(chars),
                            "tail_order":len(tail),"permutations":[[x+1 for x in p] for p in ss]})
            tested.append({"source_index":row["source_index"],"orientation":orientation,
                "anchors":[a+1 for a in points],"transitive_complement_anchors":valid,
                "character_exists":consistent,"group_order":len(chars),"tail_order":len(tail)})
    lib.need([(r["source_index"],r["orientation"]) for r in surviving] == [(3,1),(4,1),(6,0),(8,0)], "wrong surviving cases")
    lib.need(all((r["degree"],r["rank"],r["anchor"],r["group_order"],r["tail_order"]) == (6,3,1,120,10) for r in surviving), "wrong boundary invariants")
    lib.need(surviving[0]["permutations"] == surviving[2]["permutations"], "wrong first duplicate")
    point_map = (1,2,4,5,6,3)
    lib.need(all(point_map[x-1] == target[point_map[i]-1]
        for source,target in zip(surviving[1]["permutations"],surviving[3]["permutations"])
        for i,x in enumerate(source)), "wrong second conjugacy")
    return {"status":"PASS","tested_orientations":tested,"surviving":surviving,
            "second_conjugacy":list(point_map)}

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path(__file__).with_name("primitive_inputs.json"));p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();report=run(json.loads(a.input.read_text()));a.output.write_text(json.dumps(report,indent=2)+"\n")
    print("PASS: twelve primitive representatives, both orientations, two anchored types")

if __name__ == "__main__":
    main()
