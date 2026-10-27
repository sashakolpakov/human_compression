"""Check the complete catalogue patch and the grouping of registered source IDs."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


def same(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same(x, y) for x, y in zip(left, right))
    return left == right


def check():
    directory = Path(__file__).resolve().parent
    corpus = directory.parents[3]
    patch = json.loads((directory / "patch.json").read_bytes())
    original = (corpus / patch["base"]["path"]).read_bytes()
    assert len(original) == patch["base"]["bytes"]
    assert sha256(original).hexdigest() == patch["base"]["sha256"]
    original = json.loads(original)
    transformed = deepcopy(original)
    for change in patch["changes"]:
        target = transformed
        for key in change["path"][:-1]:
            target = target[key]
        key = change["path"][-1]
        present = key in target if isinstance(target, dict) else 0 <= key < len(target)
        assert present is change["existed"]
        if present:
            assert same(target[key], change["before"])
        target[key] = deepcopy(change["after"])
    raw = (directory / "catalogue.json").read_bytes()
    assert len(raw) == patch["successor"]["bytes"]
    assert sha256(raw).hexdigest() == patch["successor"]["sha256"]
    assert same(transformed, json.loads(raw))
    for change in reversed(patch["changes"]):
        target = transformed
        for key in change["path"][:-1]:
            target = target[key]
        if change["existed"]:
            target[change["path"][-1]] = change["before"]
        else:
            del target[change["path"][-1]]
    assert same(transformed, original)
    identity = json.loads((directory / "manuscript_identity.json").read_bytes())
    groups = identity["groups"]
    ids = [item for group in groups for item in group["source_ids"]]
    assert len(groups) == 160 and len(ids) == len(set(ids)) == 161
    assert next(g for g in groups if g["manuscript_id"] == "L063")["source_ids"] == ["L063", "L064"]
    assert all(g["source_ids"] == [g["manuscript_id"]] for g in groups if g["manuscript_id"] != "L063")
    return {"status": "PASS", "typed_changes": len(patch["changes"]),
            "registered_source_ids": len(ids), "registered_manuscripts": len(groups),
            "count_qualification": identity["other_identity_checks"]["limits"],
            "proof_or_measurement_credit": 0}


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
