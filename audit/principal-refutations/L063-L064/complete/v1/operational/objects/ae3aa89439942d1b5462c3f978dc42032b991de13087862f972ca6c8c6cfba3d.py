"""Exact-input and native-build replay; mathematical claims require proof review."""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
from pypdf import PdfReader

A = Path(__file__).resolve().parent

def pin(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

def verify(path, row):
    if pin(path) != {k: row[k] for k in ['bytes', 'sha256']}:
        raise ValueError('changed input: ' + str(path))

def main(out):
    if out.exists():
        raise ValueError('fresh replay directory required')
    manifest = json.loads((A/'manifest.json').read_text())
    for row in manifest['exports']:
        verify(A/row['path'], row)
    deps = json.loads((A/'dependencies.json').read_text())
    for row in deps:
        verify(Path(row['path']), row)
    out.mkdir(parents=True)
    shutil.copyfile(A/'s4_pairs.tex', out/'s4_pairs.tex')
    runs = []
    for i in [1, 2]:
        r = subprocess.run(['/opt/homebrew/bin/pdflatex', '-recorder',
                            '-interaction=nonstopmode', '-halt-on-error', 's4_pairs.tex'],
                           cwd=out, capture_output=True, timeout=30)
        (out/f'pass{i}.stdout').write_bytes(r.stdout)
        (out/f'pass{i}.stderr').write_bytes(r.stderr)
        if r.returncode:
            raise ValueError('TeX build failed')
        runs.append(r.returncode)
    actual = [p.extract_text() for p in PdfReader(out/'s4_pairs.pdf').pages]
    expected = [p.extract_text() for p in PdfReader(A/'s4_pairs.pdf').pages]
    if actual != expected or len(actual) != 4:
        raise ValueError('different mathematical page text')
    r = subprocess.run(['/opt/homebrew/bin/gs', '-q', '-dSAFER', '-dBATCH',
                        '-dNOPAUSE', '-sDEVICE=png16m', '-r105',
                        '-sOutputFile='+str(out/'page-%02d.png'), str(out/'s4_pairs.pdf')],
                       capture_output=True, timeout=30)
    (out/'render.stdout').write_bytes(r.stdout)
    (out/'render.stderr').write_bytes(r.stderr)
    if r.returncode:
        raise ValueError('native render failed')
    images = sorted(out.glob('page-*.png'))
    if len(images) != 4 or any(p.read_bytes() != (A/'native'/p.name).read_bytes() for p in images):
        raise ValueError('different native proof page')
    for row in deps:
        verify(Path(row['path']), row)
    report = dict(status='PASS_S4_AUTOMORPHISMS_EXACT_NATIVE_REPLAY',
                  dependencies=len(deps), native_pages=4,
                  source_claim_groups=3, mathematical_review_required=True,
                  new_group_searches=0, whole_source_credit=0)
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    main(p.parse_args().out.resolve())
