"""Portable binding/render replay; no external census or mathematical search."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent

def need(value, message):
    if not value:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    args = parser.parse_args()
    need(not args.out.exists(), 'output directory must be fresh')
    args.out.mkdir(parents=True)
    manifest = json.loads((HERE/'manifest.json').read_text())
    for row in manifest['exports']:
        p = HERE/row['path']
        need(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'], 'export '+row['path'])
    dependencies = json.loads((HERE/'dependencies.json').read_text())
    checked_sources = 0
    if args.study_root:
        for row in dependencies['private_primary_sources']:
            p = args.study_root/row['path']
            need(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'], 'primary '+row['id'])
            checked_sources += 1
    run = subprocess.run([sys.executable, '-B', '-O', str(HERE/'check_optional.py')], check=True, capture_output=True, text=True)
    optional = json.loads(run.stdout)
    need(optional == json.loads((HERE/'optional_report.json').read_text()), 'optional diagnostic changed')
    need(optional['mathematical_premise'] is False, 'optional role')
    roles = json.loads((HERE/'program_roles.json').read_text())
    need(roles['required_new_mathematical_programs'] == [] and roles['source_census_reexecuted'] is False, 'software scope')
    rendered = 0
    if args.render:
        from pypdf import PdfReader
        work = args.out/'render'
        work.mkdir()
        shutil.copy2(HERE/'odd_cycle_bound.tex', work/'odd_cycle_bound.tex')
        for i in range(2):
            run = subprocess.run([args.pdflatex, '-halt-on-error', '-interaction=nonstopmode', 'odd_cycle_bound.tex'], cwd=work, capture_output=True, text=True)
            (work/f'run{i}.log').write_text(run.stdout+run.stderr)
            need(run.returncode == 0, 'native rendering')
        log = (work/'odd_cycle_bound.log').read_text()
        for bad in ['Overfull', 'Undefined control sequence', 'LaTeX Warning:']:
            need(bad not in log, 'render diagnostic '+bad)
        reference = PdfReader(HERE/'odd_cycle_bound.pdf')
        actual = PdfReader(work/'odd_cycle_bound.pdf')
        need(len(actual.pages) == len(reference.pages) == 3, 'three complete pages')
        for i,(a,b) in enumerate(zip(actual.pages,reference.pages)):
            need(a.extract_text() == b.extract_text(), 'page text '+str(i+1))
        rendered = len(actual.pages)
    report = dict(status='PASS_BOUNDED_AUTHOR_REPLAY', exports=len(manifest['exports']),
                  private_sources_checked=checked_sources, optional_odd_cycle_cases=len(optional['odd_cycle_cases']),
                  optional_controls=len(optional['controls']), rendered_pages=rendered,
                  source_census_reexecuted=False, new_mathematical_finite_premises=0,
                  retained_external_finite_premise='F012 Table 2, (4,6,18): lower bound 32',
                  distinct_review=False)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
