#!/usr/bin/env python3
"""Measure the complete six-source U+A PDF package, with all four programs.

Private primary PDFs are required. A new output directory is mandatory. No
mathematical program or Lean proof is executed. Primary captures stay private.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
PROTOCOL_SHA256 = "00bb0c5fe30f1e50d4e29d884501c5be2c7061f0e630db6ddb0a7a4a2b0f21a1"
sha = lambda b: hashlib.sha256(b).hexdigest()


def read_bound(root, binding):
    b = (root / binding['path']).read_bytes()
    if sha(b) != binding['sha256'] or ('bytes' in binding and len(b) != binding['bytes']):
        raise ValueError('Bound input changed: ' + binding['path'])
    return b


def load(root, binding, name):
    read_bound(root, binding)
    spec = importlib.util.spec_from_file_location(name, root / binding['path'])
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module


def write_json(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root', type=Path, default=ROOT)
    ap.add_argument('--protocol', type=Path, default=ROOT / 'phase144_measurement_protocol.json')
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--rasterize', action='store_true')
    ap.add_argument('--author-initial', action='store_true', help='Only before expected metrics are frozen')
    a = ap.parse_args()
    root = a.input_root.resolve()
    out = a.output_dir.expanduser().absolute()
    if os.path.lexists(out):
        raise FileExistsError('Refusing existing output directory: ' + str(out))
    pb = a.protocol.read_bytes()
    if PROTOCOL_SHA256 != 'AUTHOR_DRAFT' and sha(pb) != PROTOCOL_SHA256:
        raise ValueError('Protocol changed')
    p = json.loads(pb)
    if p['expected'] is None and not a.author_initial:
        raise ValueError('Unfrozen author protocol requires --author-initial')
    if p['expected'] is not None and a.author_initial:
        raise ValueError('Frozen protocol refuses --author-initial')
    m = load(root, p['measurement_helper'], 'phase144_metrics')
    h = load(root, p['render_helper'], 'phase144_render_tools')
    transform = load(root, p['presentation_helper'], 'phase144_transform')
    import pypdf
    programs = {k: h.program_info(k) for k in ['pandoc', 'xelatex'] + (['gs'] if a.rasterize else [])}
    if pypdf.__version__ != p['expected_toolchain']['pypdf']:
        raise ValueError('pypdf version changed; a new measurement is required')
    for name in ['pandoc', 'xelatex']:
        if programs[name]['first_line'] != p['expected_toolchain'][name + '_first_line']:
            raise ValueError(name + ' version changed; a new measurement is required')
    for b in p['contract_bindings'] + [p['plan']]:
        read_bound(root, b)
    inherited = json.loads(read_bound(root, p['inherited_source_protocol']))
    for key in p['inherited_source_keys']:
        if p['documents'][key] != inherited['documents'][key]:
            raise ValueError('Inherited source specification changed: ' + key)

    source_docs = {}
    private_bodies = {}
    for key in p['source_keys']:
        s = p['documents'][key]
        read_bound(root, {'path': s['pdf_path'], 'sha256': s['pdf_sha256'], 'bytes': s['pdf_bytes']})
        full, pages, warnings = h.extract_primary(root / s['pdf_path'], pypdf)
        if sha(full.encode()) != s['extraction_sha256'] or len(pages) != s['pages']:
            raise ValueError('Source extraction changed: ' + key)
        if warnings != s['expected_extraction_warnings']:
            raise ValueError('Source extraction warnings changed: ' + key)
        if len(pages) != len(s['page_spans']):
            raise ValueError('Source page bindings incomplete: ' + key)
        for page, binding in zip(pages, s['page_spans']):
            if sha(page.encode()) != binding['sha256_utf8']:
                raise ValueError('Source page extraction changed: ' + key)
        body, excluded = m.body_text(full, s)
        private_bodies[key] = body
        source_docs[key] = dict(pdf_path=s['pdf_path'], pdf_sha256=s['pdf_sha256'],
            version=p['source_versions'][key], pages=len(pages), body_pages=s['body_pages'],
            extraction_sha256=sha(full.encode()), warnings=warnings, body=s['body'], exclusions=excluded,
            cleaned_body_sha256=sha(body.encode()), metrics={f: m.metrics(body, f) for f in p['forms']},
            nonwhitespace_control_codepoints=sorted({ord(c) for c in body if ord(c) < 32 and not c.isspace()}))

    texts = [read_bound(root, b).decode() for b in p['replacement_manuscripts']]
    codes = [read_bound(root, b).decode() for b in p['certificate_programs']]
    if sum(len(t.encode()) for t in texts + codes) != p['inventory']['complete_required_raw_bytes']:
        raise ValueError('Complete raw input inventory changed')
    appendix = '# Complete computational proof appendix\n\n'
    appendix += ('The following four programs are reproduced in full and charged once. '
                 'Their exact source files accompany the manuscript. The runner executes the three GAP inputs; '
                 'GAP and its NQ package remain named computational dependencies.\n\n')
    for b, code in zip(p['certificate_programs'], codes):
        if '```' in code or not code.endswith('\n'):
            raise ValueError('Code fence or terminal-newline convention changed')
        lang = 'python' if b['path'].endswith('.py') else 'gap'
        appendix += '## ' + b['path'] + '\n\n```' + lang + '\n' + code + '```\n\n'
    body = '\n\n'.join(texts + [appendix])
    presented = transform.presentation_copy(body)
    # Fixed-width display wrapping avoids a TeX page-break defect in very long
    # verbatim blocks. It inserts only newlines, never removes a code character.
    # The per-original-line chunk counts make the transformation invertible.
    display_wrap = []
    def wrap_fence(match):
        opening, code, closing = match.group(1), match.group(2), match.group(3)
        lines = code.split('\n')
        chunks = [[line[i:i+64] for i in range(0, len(line), 64)] or [''] for line in lines]
        wrapped = '\n'.join(piece for row in chunks for piece in row)
        display_wrap.append(dict(original_sha256=sha(code.encode()), wrapped_sha256=sha(wrapped.encode()),
                                 original_line_chunk_counts=[len(row) for row in chunks]))
        return opening + wrapped + closing
    presented = re.sub(r'(?m)(^```[^\n]*\n)(.*?)(\n^```[ \t]*$)', wrap_fence, presented, flags=re.S)
    out.mkdir(parents=False)
    (out / 'replacement.md').write_text(body)
    (out / 'render.md').write_text(presented)
    (out / 'header.tex').write_text(p['render']['header'])
    private = out / 'private_source_bodies'
    private.mkdir()
    for key, text in private_bodies.items():
        (private / (key + '.txt')).write_text(text)
    commands = []

    def run(label, argv):
        result = subprocess.run(argv, cwd=out, capture_output=True, text=True)
        (out / (label + '.stdout.txt')).write_text(result.stdout)
        (out / (label + '.stderr.txt')).write_text(result.stderr)
        commands.append(dict(label=label, argv=argv, returncode=result.returncode))
        if result.returncode:
            raise RuntimeError(label + ' failed; inspect output directory')

    pandoc = programs['pandoc']['path']
    reader = '--from=' + p['render']['reader']
    for name in ['replacement', 'render']:
        run(name + '-ast', [pandoc, name + '.md', reader, '--to=json', '--output=' + name + '.json'])
    ast0 = json.loads((out / 'replacement.json').read_text())
    ast1 = json.loads((out / 'render.json').read_text())

    def nodes(tree, typ):
        found = []
        def visit(node):
            if isinstance(node, dict):
                if node.get('t') == typ:
                    found.append(node['c'])
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)
        visit(tree)
        return found

    for typ in ['Math', 'Table']:
        if nodes(ast0, typ) != nodes(ast1, typ):
            raise ValueError('Presentation changed ' + typ)
    original_code_nodes = nodes(ast0, 'CodeBlock')
    code_nodes = nodes(ast1, 'CodeBlock')
    if [c[1] for c in original_code_nodes[-4:]] != [c[:-1] for c in codes]:
        raise ValueError('Four complete program ASTs differ from original files')
    if len(original_code_nodes) != len(code_nodes) or len(code_nodes) != len(display_wrap):
        raise ValueError('Display wrapping omitted or introduced a code block')
    for original, wrapped, mapping in zip(original_code_nodes, code_nodes, display_wrap):
        pieces = wrapped[1].split('\n'); recovered = []; offset = 0
        for count in mapping['original_line_chunk_counts']:
            recovered.append(''.join(pieces[offset:offset+count])); offset += count
        if offset != len(pieces) or '\n'.join(recovered) != original[1] or original[0] != wrapped[0]:
            raise ValueError('Code display wrapping is not exactly reversible')
        if any(len(line) > 64 for line in pieces):
            raise ValueError('Display line exceeds the fixed column bound')
    write_json(out / 'code_display_wrap.json', display_wrap)
    opts = [reader, '--standalone', '--to=latex', '--include-in-header=header.tex',
            '--syntax-highlighting=' + p['render']['syntax_highlighting']]
    for v in p['render']['variables']:
        opts += ['--variable', v]
    run('latex', [pandoc, 'render.md', *opts, '--output=replacement.tex'])
    for n in [1, 2]:
        run('xelatex' + str(n), [programs['xelatex']['path'], '-interaction=nonstopmode', '-halt-on-error', 'replacement.tex'])
    log = (out / 'replacement.log').read_text()
    diagnostics = [line for line in log.splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph', line, re.I)]
    rendered, pages, warnings = h.extract_primary(out / 'replacement.pdf', pypdf)
    if warnings:
        raise ValueError('Replacement extraction warnings: ' + repr(warnings))
    (out / 'replacement_extraction.txt').write_text(rendered)
    rendered_metrics = {f: m.metrics(rendered, f) for f in p['forms']}
    measured = dict(assembled_markdown_sha256=sha(body.encode()), presentation_markdown_sha256=sha(presented.encode()),
        extraction_sha256=sha(rendered.encode()), pages=len(pages), metrics=rendered_metrics, diagnostics=diagnostics,
        AST_counts={typ: len(nodes(ast1, typ)) for typ in ['Math', 'Table', 'CodeBlock']},
        original_program_AST_sha256=[sha(c[1].encode()) for c in original_code_nodes[-4:]],
        displayed_program_AST_sha256=[sha(c[1].encode()) for c in code_nodes[-4:]],
        code_display_recovery_exact=True)
    if p['expected'] is not None and measured != p['expected']:
        write_json(out / 'changed_measurement.json', measured)
        raise ValueError('Frozen rendering/count result changed')
    raster = {}
    if a.rasterize:
        run('rasterize', [programs['gs']['path'], '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r110', '-sOutputFile=page-%02d.png', 'replacement.pdf'])
        raster = {f.name: sha(f.read_bytes()) for f in sorted(out.glob('page-*.png'))}
        if len(raster) != len(pages):
            raise ValueError('Incomplete rasterization')
    sums = {form: {key: sum(doc['metrics'][form][key] for doc in source_docs.values()) for key in p['metric_keys']} for form in p['forms']}
    comparisons = {form: {key: dict(numerator=sums[form][key], denominator=rendered_metrics[form][key],
        factor=sums[form][key] / rendered_metrics[form][key]) for key in p['metric_keys']} for form in p['forms']}
    for b in p['contract_bindings'] + p['replacement_manuscripts'] + p['certificate_programs']:
        read_bound(root, b)
    if a.protocol.read_bytes() != pb:
        raise ValueError('Protocol changed during execution')
    report = dict(schema='phase144_six_source_measurement_v1', status='author_measurement_pending_independent_review',
        protocol_sha256=sha(pb), runner_sha256=sha(Path(__file__).read_bytes()),
        environment=dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
            Unicode_database=unicodedata.unidata_version, pypdf=pypdf.__version__, programs=programs),
        source_documents=source_docs, source_body_sums=sums, replacement=measured, comparisons=comparisons,
        inventory=p['inventory'], rendering=dict(commands=commands, raster_sha256=raster, visual_review_automated=False),
        interpretation=dict(whole_source_bodies_not_minimal_target_proofs=True, full_U_counted_once=True,
            full_A_counted_once=True, all_four_programs_counted_once=True, all_required_corrections_integrated=True,
            primary_house_format_page_factor=None, layout_normalization_equivalence_claim=False,
            source_admission_or_mathematical_proof_checked_by_this_runner=False,
            primary_text_export_allowed=False, foundational_background_expansion_included=False,
            model_acquisition_or_historical_novelty_claim=False, optional_Lean_not_a_substitute_for_written_proofs=True))
    write_json(out / 'report.json', report)
    print(json.dumps(dict(status=report['status'], replacement=measured, comparisons=comparisons), indent=2))


if __name__ == '__main__':
    main()
