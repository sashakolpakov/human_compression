"""Compile a new module while protecting cached companion objects."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lean', required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error('output must be new')
    runner = Path(__file__).resolve().parent / 'formal/verify_lean.py'
    spec = importlib.util.spec_from_file_location('public_lean_runner', runner)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with tempfile.TemporaryDirectory(prefix='math-compression-overlay-') as tmp:
        base = Path(tmp)
        checkout = base / 'mathlib'
        library = checkout / '.lake/build/lib/lean'
        cache = library / 'Mathlib'
        cache.mkdir(parents=True)
        source = checkout / 'Mathlib/CompanionBoundary.lean'
        source.parent.mkdir(parents=True)
        source.write_text('namespace CompanionBoundary\ndef value : Nat := 37\nend CompanionBoundary\n')
        sentinels = {}
        for suffix in ['.olean.private', '.olean.server', '.ilean', '.trace']:
            p = cache / ('CompanionBoundary' + suffix)
            p.write_text('cached companion must remain unchanged: ' + suffix)
            sentinels[p.name] = p.read_bytes()
        caller = base / 'formal'
        caller.mkdir()
        (caller / 'Caller.lean').write_text('import Mathlib.CompanionBoundary\n')
        mod.ROOT = caller
        output = base / 'out'
        env = dict(os.environ)
        env['LEAN_PATH'] = os.pathsep.join(map(str, [output, library]))
        mod.prepare_mathlib(['Caller'], args.lean, output, env, 60)
        for name, expected in sentinels.items():
            if (cache / name).read_bytes() != expected:
                raise RuntimeError('installed companion overwritten: ' + name)
            if (output / 'Mathlib' / name).is_symlink():
                raise RuntimeError('target companion still linked: ' + name)
        built = output / 'Mathlib/CompanionBoundary.olean'
        if not built.is_file() or built.is_symlink():
            raise RuntimeError('fresh target was not compiled privately')
        record = {
            'status': 'PASS', 'runner_sha256': hashlib.sha256(runner.read_bytes()).hexdigest(),
            'fresh_real_Lean_compilation': True, 'cached_companions_preserved': sorted(sentinels),
            'dependency_build': json.loads((output / 'dependency_builds.json').read_text()),
            'scope': 'Compiler-output cache boundary regression, not a mathematical theorem.'}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            json.dump(record, f, indent=2)
            f.write('\n')
    print('PASS: fresh private compilation preserves all cached companions.')


if __name__ == '__main__':
    main()
