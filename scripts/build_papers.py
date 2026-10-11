#!/usr/bin/env python3
"""Compile the canonical TeX papers directly; no Markdown or Pandoc input."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def relative_path(name):
    """Require a literal relative path, without aliases or traversal."""
    if (not isinstance(name, str) or not name or '\\' in name
            or any(ord(char) < 32 for char in name)):
        raise ValueError(f'Invalid relative path: {name!r}')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or str(path) != name or name == '.':
        raise ValueError(f'Invalid relative path: {name!r}')
    return path


def source_bundle(row, root=ROOT):
    """Read exactly the main source and its declared TeX inputs."""
    root = root.resolve()
    main = relative_path(row['tex'])
    inputs = row.get('tex_inputs', [])
    if not isinstance(inputs, list):
        raise ValueError('tex_inputs must be a list of repository-relative paths.')
    files = {}
    for name in [row['tex']] + inputs:
        path = relative_path(name)
        if path.suffix != '.tex' or not path.is_relative_to(main.parent):
            raise ValueError(f'TeX input must be within {main.parent}: {name}')
        if name in files:
            raise ValueError(f'Duplicate TeX source: {name}')
        source = root / path
        if source.resolve() != source or not source.is_file():
            raise ValueError(f'TeX source must be a regular file without symlink aliases: {name}')
        relative = path.relative_to(main.parent)
        if name != row['tex'] and relative == PurePosixPath('paper.tex'):
            raise ValueError('A TeX input conflicts with the isolated main filename paper.tex.')
        files[name] = source.read_bytes()
    return files


def select_papers(catalogue, requested=None):
    papers = catalogue['papers'] + catalogue.get('new_editions', [])
    papers = papers + [{'id': 'audit/protocol', 'tex': 'audit/protocol.tex'}]
    ids = [row['id'] for row in papers]
    for name in ids:
        relative_path(name)
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate paper IDs in the catalogue.')
    if requested:
        unknown = set(requested) - set(ids)
        if unknown:
            raise ValueError('Unknown paper IDs: ' + ', '.join(sorted(unknown)))
        return [row for row in papers if row['id'] in requested]
    return papers


def check_repository_reads(target, root=ROOT):
    """Reject TeX reads from the original checkout instead of the staged copy."""
    target, root = target.resolve(), root.resolve()
    for line in (target/'paper.fls').read_text(errors='strict').splitlines():
        if line.startswith('INPUT '):
            source = (target/line[6:]).resolve()
            if source.is_relative_to(root) and not source.is_relative_to(target):
                raise RuntimeError(f'TeX read an unstaged repository input: {source}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True,
                    help='Fresh build directory, outside the canonical paper sources.')
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--paper', action='append', metavar='ID',
                    help='Build only this exact catalogue ID; repeat to select several. Duplicate selections build once.')
    args = ap.parse_args()
    if args.output_dir.exists() or args.output_dir.is_symlink():
        ap.error('Use a fresh output directory.')
    if args.jobs < 1:
        ap.error('--jobs must be positive')
    engine = shutil.which('xelatex')
    if not engine:
        ap.error('XeLaTeX is required, with the fonts specified in the TeX sources.')
    catalogue = json.loads((ROOT/'papers/catalogue.json').read_text())
    try:
        papers = select_papers(catalogue, args.paper)
        bundles = {row['id']: source_bundle(row) for row in papers}
    except (ValueError, OSError) as exc:
        ap.error(str(exc))
    out = args.output_dir.resolve()
    out.mkdir(parents=True)

    def build(row):
        files = bundles[row['id']]
        data = files[row['tex']]
        target = out/row['id']
        target.mkdir(parents=True)
        (target/'paper.tex').write_bytes(data)
        parent = PurePosixPath(row['tex']).parent
        for name, content in files.items():
            if name != row['tex']:
                destination = target / PurePosixPath(name).relative_to(parent)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
        for turn in (1, 2):
            proc = subprocess.run([engine, '-no-shell-escape', '-recorder', '-interaction=nonstopmode',
                                   '-halt-on-error', 'paper.tex'], cwd=target,
                                  text=True, capture_output=True, timeout=180)
            (target/f'run-{turn}.log').write_text(proc.stdout+proc.stderr)
            if proc.returncode:
                raise RuntimeError(f"{row['id']}: XeLaTeX failed; see {target}")
            check_repository_reads(target)
        log = (target/'paper.log').read_text(errors='replace')
        diagnostics = [s for s in log.splitlines()
                       if re.search(r'Warning:|Overfull|Missing character:|Missing glyph', s)]
        if any('Missing character:' in s or 'Missing glyph' in s for s in diagnostics):
            raise RuntimeError(f"{row['id']}: missing glyphs: {diagnostics}")
        for name, content in files.items():
            if (ROOT/name).read_bytes() != content:
                raise RuntimeError(f"{name}: source changed during build")
        result = {'id':row['id'], 'tex_sha256':sha256(data).hexdigest(),
                  'tex_inputs':[{'path': name, 'bytes': len(content),
                                 'sha256': sha256(content).hexdigest()}
                                for name, content in files.items() if name != row['tex']],
                  'pdf_sha256':sha256((target/'paper.pdf').read_bytes()).hexdigest(),
                  'diagnostics':diagnostics, 'status':'compiled'}
        print('Compiled '+row['id'], flush=True)
        return result

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(build, papers))
    (out/'report.json').write_text(json.dumps({
        'scope':'Direct TeX compilation only; no new mathematical review or compression measurement.',
        'papers':results},indent=2)+'\n')
    print(f'PASS: compiled {len(results)} selected documents.')


if __name__ == '__main__':
    main()
