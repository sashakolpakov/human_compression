from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys
if sys.flags.optimize:
    raise RuntimeError('optimized Python unsupported')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--replay', type=Path, required=True)
    parser.add_argument('--gap', default='/opt/homebrew/bin/gap')
    a = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins = json.loads((here / 'inputs.json').read_text())
    for pin in pins:
        p = a.sources / pin['path']
        need(p.stat().st_size == pin['bytes'] and digest(p) == pin['sha256'],
             'input pin: ' + pin['path'])
    a.replay.mkdir(exist_ok=False)
    for name in ('subdivision_markings.g', 'subdivision_actual_actions.g'):
        shutil.copy2(here / name, a.replay / name)
    lines = ['Read("subdivision_actual_actions.g");;']
    names = ['CAT_1024_10', 'CAT_1080_1', 'CAT_1440_6']
    for name in names:
        witness = (a.sources / 'subdivision_markings' / (name + '.g')).resolve()
        # JSON escaping is correct for this GAP string literal; no shell is used.
        lines.extend(['Read(' + json.dumps(str(witness)) + ');;',
                      'rows:=L059SubdivisionRows(L059Subdivision.A_subdivision,L059Subdivision.edges_original,List(L059Subdivision.witnesses,r->r.H));;',
                      'Need(rows=L059Subdivision.witnesses);;',
                      'Print("PASS_ACTUAL_ACTIONS ' + name + ' ",Length(rows),"\\n");'])
    lines.append('QUIT_GAP(0);')
    script = a.replay / 'replay.g'
    script.write_text('\n'.join(lines)+'\n')
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    run = subprocess.run([a.gap, '-q', '-b', '-T', 'replay.g'],
                         cwd=a.replay, env=env, capture_output=True, text=True, timeout=180)
    (a.replay/'stdout.log').write_text(run.stdout)
    (a.replay/'stderr.log').write_text(run.stderr)
    expected = ['PASS_ACTUAL_ACTIONS ' + n + ' ' + str(c)
                for n, c in zip(names, [3,4,3])]
    need(run.returncode == 0 and not run.stderr and run.stdout.strip().splitlines() == expected,
         'actual-action row comparison failed')
    report = dict(status='PASS_TEN_COMPLETE_ROWS', compared_graphs=names,
                  row_counts=[3,4,3], input_pins=pins,
                  new_library_sha256=digest(here/'subdivision_actual_actions.g'),
                  old_library_sha256=digest(here/'subdivision_markings.g'),
                  stdout_sha256=digest(a.replay/'stdout.log'),
                  stderr_sha256=digest(a.replay/'stderr.log'))
    (a.replay/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS: ten complete rows in three retained graphs')


if __name__ == '__main__':
    main()
