#!/usr/bin/env python3
"""Bind the four literal Lean data arrays to the frozen authored JSON.

This checks transcription only, not the Lean proof or the group/geometry adapter.
"""
import argparse
import ast
import hashlib
import json
import re
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent
    parser.add_argument('--data', type=Path, default=root / 'phase30_affine_map_check.json')
    parser.add_argument('--source', type=Path, default=root / 'formal/Phase30AffineData.lean')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing report')
    data = json.loads(args.data.read_text())
    source = args.source.read_text()
    bindings = {'columns': 'columns_13bit', 'vertexBlocks': 'vertex_blocks',
                'faceBlocks': 'face_blocks', 'incidentPairs': 'incident_pairs'}
    checked = {}
    for name, field in bindings.items():
        match = re.search(r'^def ' + name + r' : [^\n]+ := (\[[^\n]*\])$', source, re.M)
        assert match, name
        literal = ast.literal_eval(match.group(1))
        if name == 'incidentPairs':
            literal = [list(pair) for pair in literal]
        assert literal == data[field], name
        checked[name] = {'json_field': field, 'literal_entries': len(literal), 'equal': True}
    report = {'status': 'PASS', 'scope': 'Literal data transcription only; no Lean execution or geometry theorem.',
              'checker_sha256': digest(Path(__file__)), 'data_sha256': digest(args.data),
              'lean_source_sha256': digest(args.source), 'bindings': checked}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('AFFINE_LEAN_DATA_PASS columns30 blocks24 pairs60')


if __name__ == '__main__':
    main()
