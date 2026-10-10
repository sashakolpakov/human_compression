#!/usr/bin/env python3
"""Compile the canonical TeX papers directly; no Markdown or Pandoc input."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True,
                    help='Fresh build directory, outside the canonical paper sources.')
    ap.add_argument('--jobs', type=int, default=2)
    args = ap.parse_args()
    if args.output_dir.exists() or args.output_dir.is_symlink():
        ap.error('Use a fresh output directory.')
    if args.jobs < 1:
        ap.error('--jobs must be positive')
    engine = shutil.which('xelatex')
    if not engine:
        ap.error('XeLaTeX is required, with the fonts specified in the TeX sources.')
    out = args.output_dir.resolve()
    out.mkdir(parents=True)
    papers = json.loads((ROOT/'papers/catalogue.json').read_text())['papers']
    papers = papers + [{'id':'audit/protocol','tex':'audit/protocol.tex'}]

    def build(row):
        source = ROOT/row['tex']
        data = source.read_bytes()
        target = out/row['id']
        target.mkdir(parents=True)
        (target/'paper.tex').write_bytes(data)
        for turn in (1, 2):
            proc = subprocess.run([engine, '-no-shell-escape', '-interaction=nonstopmode',
                                   '-halt-on-error', 'paper.tex'], cwd=target,
                                  text=True, capture_output=True, timeout=180)
            (target/f'run-{turn}.log').write_text(proc.stdout+proc.stderr)
            if proc.returncode:
                raise RuntimeError(f"{row['id']}: XeLaTeX failed; see {target}")
        log = (target/'paper.log').read_text(errors='replace')
        diagnostics = [s for s in log.splitlines()
                       if re.search(r'Warning:|Overfull|Missing character:|Missing glyph', s)]
        if any('Missing character:' in s or 'Missing glyph' in s for s in diagnostics):
            raise RuntimeError(f"{row['id']}: missing glyphs: {diagnostics}")
        if source.read_bytes() != data:
            raise RuntimeError(f"{source}: source changed during build")
        result = {'id':row['id'], 'tex_sha256':sha256(data).hexdigest(),
                  'pdf_sha256':sha256((target/'paper.pdf').read_bytes()).hexdigest(),
                  'diagnostics':diagnostics, 'status':'compiled'}
        print('Compiled '+row['id'], flush=True)
        return result

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(build, papers))
    (out/'report.json').write_text(json.dumps({
        'scope':'Direct TeX compilation only; no new mathematical review or compression measurement.',
        'papers':results},indent=2)+'\n')
    print(f'PASS: compiled {len(results)-1} proof manuscripts and the audit protocol.')


if __name__ == '__main__':
    main()
