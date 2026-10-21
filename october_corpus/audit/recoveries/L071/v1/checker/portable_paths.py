"""Resolve historic pins only inside an explicitly restored public tree."""
from pathlib import Path
import os, json, hashlib
S = Path(os.environ['L071_RESTORED_STUDY']).resolve()
W = Path(os.environ['L071_CHECK_OUTPUT']).resolve()
R = S.parent / 'repo'
OLD_STUDY = Path('/Users/sasha/medusa/research/leemans')
OLD_REPO = Path('/Users/sasha/medusa/math_compression')
TRANSPORT = json.loads(Path(os.environ['L071_TRANSPORT']).read_text())
OMITTED = {r['path']:r for r in TRANSPORT['files'] if r['transport'].endswith('HASH_ONLY')}

def verify_pin(row, base=None):
    raw = Path(row['path'])
    if raw.is_absolute() and raw.is_relative_to(OLD_STUDY):
        key = str(raw.relative_to(OLD_STUDY))
    elif not raw.is_absolute() and (base is None or base == S):
        key = str(raw)
    else:
        key = str(raw)
    if key in OMITTED:
        expected = OMITTED[key]
        if row['sha256'] != expected['sha256'] or ('bytes' in row and row['bytes'] != expected['bytes']):
            raise ValueError('changed documentary metadata: ' + key)
        return  # Metadata agreement only; no fresh source-content verification.
    p = resolve(raw, base)
    if hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('changed restored pin: ' + str(p))
    if 'bytes' in row and p.stat().st_size != row['bytes']:
        raise ValueError('changed restored size: ' + str(p))

def resolve(name, base=None):
    p = Path(name)
    if p.is_absolute():
        if p.is_relative_to(OLD_STUDY):
            p = S / p.relative_to(OLD_STUDY)
        elif p.is_relative_to(OLD_REPO):
            p = R / p.relative_to(OLD_REPO)
        elif not (p.is_relative_to(S) or p.is_relative_to(R)):
            raise ValueError('undeclared external path: ' + str(p))
    else:
        p = (S if base is None else base) / p
    p = p.resolve()
    if not (p.is_relative_to(S) or p.is_relative_to(R)):
        raise ValueError('path escapes restored evidence tree: ' + str(p))
    if not p.is_file():
        raise ValueError('missing restored public evidence: ' + str(p))
    return p
