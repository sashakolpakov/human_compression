#!/usr/bin/env python3
"""Generate an eleven-source reader with the frozen shared annotation engine.

Only presentation labels differ from the old engine. Validation and exact
insertion are reused. All source and evidence files remain immutable.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys

ENGINE_HASH = '6c811ba65bf740cc7dca839bfc39101f6cbf0cdc6227386fbdcf78699a14606d'
FILTER_HASH = 'c4e342b9c5ee3d0cf82b970d7bc795c9629d241051fc32352c514bef278dfd42'
LEGEND_HASH = '27a576a7d958ee620a4afe736a28f49a0043e19df17a4b70d29aaf418610ae85'


def digest(data):
    return sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def collect_bindings(value):
    if isinstance(value, dict):
        if {'path', 'sha256', 'bytes'} <= value.keys():
            yield value
        for child in value.values():
            yield from collect_bindings(child)
    elif isinstance(value, list):
        for child in value:
            yield from collect_bindings(child)


def recover_written(path, prefix, suffix, original, notes, engine, pandoc):
    """Strip the actual written presentation and inspect each inserted note."""
    written = path.read_text()
    require(written.startswith(prefix) and written.endswith(suffix), 'presentation boundary mismatch')
    body = written[len(prefix):len(written)-len(suffix)]
    if pandoc:
        pattern = re.compile(r'\n\n::: \{\.audit-margin data-note="([A-Z0-9]+)" data-codes="[BIRCVLMO ]+"\}\n[^\n]*\n:::\n')
    else:
        pattern = re.compile(r'\n\n> \*\*\[[BIRCVLMO]\][^\n]*? — ([A-Z0-9]+)\.\*\* [^\n]*\n')
    matches = list(pattern.finditer(body))
    ordered = sorted(notes, key=lambda r: (r['insert_after_codepoint'], r['id']))
    require([m.group(1) for m in matches] == [r['id'] for r in ordered], 'actual note inventory/order mismatch')
    for match, row in zip(matches, ordered):
        if pandoc:
            expected = ('\n\n::: {.audit-margin data-note="' + row['id'] + '" data-codes="'
                        + ' '.join(row['markers']) + '"}\n' + engine.note_text(row) + '\n:::\n')
        else:
            expected = '\n\n> ' + engine.note_text(row) + '\n'
        require(match.group(0) == expected, 'actual note content mismatch: ' + row['id'])
    recovered = pattern.sub('', body).encode()
    require(recovered == original, 'stripping written notes did not recover manuscript bytes')
    return {'notes_removed': len(matches), 'recovered_sha256': digest(recovered), 'recovered_bytes': len(recovered)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--sidecar', type=Path)
    parser.add_argument('--generator', type=Path)
    parser.add_argument('--margin-filter', type=Path)
    parser.add_argument('--legend', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(), 'output directory exists; refusing overwrite')
    study = args.study_root.resolve()
    sidecar_path = args.sidecar or study/'phase79_eleven_attribution.json'
    if args.generator:
        generator = args.generator.resolve()
    else:
        candidates = [study/'phase79_eleven_attribution_engine.py',
                      study.parents[1]/'scripts/annotate_manuscript.py',
                      study.parents[1]/'math_compression/scripts/annotate_manuscript.py']
        generator = next((p for p in candidates if p.exists()), None)
        require(generator is not None, 'supply --generator for the frozen annotation engine')
    local_filter = study/'phase79_eleven_attribution_margins.lua'
    local_legend = study/'phase79_eleven_attribution_legend.md'
    margin_filter = args.margin_filter or (local_filter if local_filter.exists() else generator.parent/'attribution_margins.lua')
    legend = args.legend or (local_legend if local_legend.exists() else generator.parent.parent/'ATTRIBUTION.md')
    for path, expected in [(generator, ENGINE_HASH), (margin_filter, FILTER_HASH), (legend, LEGEND_HASH)]:
        require(digest(path.read_bytes()) == expected, 'shared annotation infrastructure changed: ' + str(path))
    spec = importlib.util.spec_from_file_location('frozen_annotation_engine', generator)
    engine = importlib.util.module_from_spec(spec)
    bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(engine)
    finally:
        sys.dont_write_bytecode = bytecode_setting
    engine.STUDY = study
    raw = sidecar_path.read_bytes()
    sidecar = json.loads(raw)
    require(sidecar['scope']['source_count'] == 11, 'wrong source count')
    require(sidecar['scope']['required_erratum_incorporated'], 'missing incorporated erratum declaration')
    require(all(not ({'M', 'O'} & set(r['markers'])) for r in sidecar['notes']), 'eleven measurement/priority not cleared')
    original, text = engine.validate(sidecar)
    bindings = {b['path']: b for b in collect_bindings(sidecar)}
    before = {p: digest(engine.bound_file(b)) for p, b in bindings.items()}
    ledger = engine.ledger_text(sidecar)
    replacements = {
        '# Attribution ledger for Compress_10': '# Attribution ledger for Compress_11',
        '**No ten-source measured factor or previously-open-conjecture claim is cleared.**':
        '**No eleven-source measured factor or previously-open-conjecture claim is cleared.**'
    }
    for old, new in replacements.items():
        require(ledger.count(old) == 1, 'unexpected frozen ledger template')
        ledger = ledger.replace(old, new)
    prefix = ('# Annotated reader: Compress_11\n\n'
              'The manuscript below is preserved byte for byte apart from inserted audit notes. '
              'Its pending-review heading is historical: the bound independent extension review passes relative to the declared retained inputs and corrected source contract. '
              'The earlier ten-source reference erratum is already incorporated in this manuscript. '
              '[Legend and attribution scope](../../ATTRIBUTION.md). '
              'These notes add no mathematical proof content. No eleven-source numerical factor, historical novelty or newly solved open conjecture is claimed.\n\n')
    suffix = '\n\n' + ledger
    markdown = prefix + engine.insert_notes(text, sidecar['notes']) + suffix
    pandoc = prefix + engine.insert_notes(text, sidecar['notes'], pandoc=True) + suffix
    args.output_dir.mkdir(parents=True, exist_ok=False)
    for name, content in [('reader.md', markdown), ('reader.pandoc.md', pandoc), ('ledger.md', ledger)]:
        (args.output_dir/name).write_text(content)
    recovered = {
        name: recover_written(args.output_dir/name, prefix, suffix, original, sidecar['notes'], engine, flag)
        for name, flag in [('reader.md', False), ('reader.pandoc.md', True)]
    }
    after = {p: digest(engine.bound_file(b)) for p, b in bindings.items()}
    require(after == before, 'input changed during generation')
    require(sidecar_path.read_bytes() == raw, 'sidecar changed during generation')
    report = {
        'schema':'eleven_attribution_integrity.v1', 'status':'PASS_annotation_integrity',
        'semantic_review':'pending_separate_independent_review',
        'manuscript_sha256':digest(original), 'sidecar_sha256':digest(raw),
        'generator_sha256':ENGINE_HASH, 'margin_filter_sha256':FILTER_HASH, 'legend_sha256':LEGEND_HASH,
        'generator_reused':['validate','bound_file','insert_notes','note_text','ledger_text'],
        'presentation_changes_only':['Compress_11 labels','eleven scope prefix','incorporated erratum status'],
        'notes':len(sidecar['notes']),
        'marker_counts':dict(sorted(Counter(c for r in sidecar['notes'] for c in r['markers']).items())),
        'written_reader_recovery':recovered, 'all_input_hashes_unchanged':True, 'bound_input_count':len(bindings),
        'original_bytes':len(original), 'annotated_reader_bytes':len(markdown.encode()),
        'added_presentation_bytes':len(markdown.encode())-len(original),
        'reader_sha256':digest(markdown.encode()), 'pandoc_reader_sha256':digest(pandoc.encode()),
        'ledger_sha256':digest(ledger.encode()), 'annotated_edition_length_ratio':None,
        'new_Lean_build':False, 'new_finite_mathematical_replay':False,
        'mathematical_proof_checker':False, 'historical_priority_checker':False,
        'PDF_layout_review':False, 'frozen_manuscript_modified':False
    }
    (args.output_dir/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
