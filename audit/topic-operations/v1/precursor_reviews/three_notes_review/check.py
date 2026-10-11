"""Review binding replay, independent bounded models, and optional fresh TeX."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--study-root', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--render', action='store_true')
    p.add_argument('--xelatex', default='/opt/homebrew/bin/xelatex')
    args = p.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output required')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'manifest.json').read_text())
    for row in manifest['exports']:
        path = root/row['path']
        need(sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], 'review export '+row['path'])
    inputs = json.loads((root/'bindings.json').read_text())
    for row in inputs['artifacts']:
        need(sha(args.study_root/row['path']) == row['sha256'], 'reviewed input '+row['path'])
    args.out.mkdir(parents=True)
    run = subprocess.run([sys.executable, '-B', '-O', str(root/'models.py')], text=True, capture_output=True, check=True)
    (args.out/'models.stdout').write_text(run.stdout)
    actual = json.loads(run.stdout)
    need(actual == json.loads((root/'model_report.json').read_text()), 'bounded independent model equality')
    render = []
    if args.render:
        from pypdf import PdfReader
        src = args.study_root/'corpus161_N005_recovery'
        for name in inputs['papers']:
            dest = args.out/name
            dest.mkdir()
            for _ in range(2):
                build = subprocess.run([args.xelatex, '-interaction=nonstopmode', '-halt-on-error',
                    '-output-directory='+str(dest.resolve()), name+'.tex'], cwd=src,
                    capture_output=True, text=True, check=True)
            (dest/'build.stdout').write_text(build.stdout)
            log = (dest/(name+'.log')).read_text()
            bad = [line for line in log.splitlines() if any(term in line for term in
                   ['Overfull','Underfull','Missing character','undefined','LaTeX Warning'])]
            need(not bad, 'render diagnostics '+name+': '+str(bad))
            original = [page.extract_text() for page in PdfReader(src/(name+'.pdf')).pages]
            fresh = [page.extract_text() for page in PdfReader(dest/(name+'.pdf')).pages]
            need(original == fresh, 'per-page text '+name)
            render.append({'paper':name,'pages':len(fresh),'exact_page_text':True})
    report = {'status':'PASS','manifest_sha256':sha(root/'manifest.json'),
              'bindings':len(inputs['artifacts']),'models':actual,'render':render,
              'scope':'Independent review of three root-authored positive notes only; separate S4 author investigation excluded.'}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','bindings':len(inputs['artifacts']),
                      'controls':len(actual['rejected_controls']), 'rendered_pages':sum(x['pages'] for x in render)}))

if __name__ == '__main__':
    main()
