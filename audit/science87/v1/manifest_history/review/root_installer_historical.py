"""Preserve the predecessor integrity manifest while allowing its regeneration."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('/Users/sasha/medusa/math_compression')
HERE = Path(__file__).resolve().parent / 'manifest_correction01'
ARCHIVE = 'audit/science87/v1/manifest_history'
BASELINE = 'ade9feeb7f8feaffa8f773932d57a50e60cb64c2'
CHECKER = 'scripts/check_science87.py'

def pin(path, name=None):
    raw = path.read_bytes()
    return {'path': name or str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

if HERE.exists() or (ROOT / ARCHIVE).exists():
    raise RuntimeError('A fresh correction directory is required')
HERE.mkdir()
(ROOT / ARCHIVE).mkdir()
shared_path = 'audit/science87/v1/root_integration.json'
shared = json.loads((ROOT / shared_path).read_text())
individuals = [r['path'] for r in shared['bindings']
               if r['path'].endswith('/root_integration.json')]
if len(individuals) != 6:
    raise RuntimeError('Exactly six individual source gates are required')
old_paths = [CHECKER] + individuals + [shared_path]
routes = {}
for i, name in enumerate(old_paths):
    target = f'{ARCHIVE}/{i:02d}_{Path(name).name}'
    (ROOT / target).write_bytes((ROOT / name).read_bytes())
    routes[name] = pin(ROOT / target, target)
manifest_name = 'provenance/publication_manifest.json'
old_manifest = subprocess.check_output(
    ['git', 'show', BASELINE + ':' + manifest_name], cwd=ROOT)
manifest_path = f'{ARCHIVE}/predecessor_publication_manifest.json'
(ROOT / manifest_path).write_bytes(old_manifest)
tree = json.loads((ROOT / 'audit/science87/v1/predecessor_tree.json').read_text())
rows = [r for r in tree['files'] if r['path'] == manifest_name]
if len(rows) != 1:
    raise RuntimeError('Exact predecessor manifest row required')
old_pin = pin(ROOT / manifest_path, manifest_path)
if any(old_pin[k] != rows[0][k] for k in ['bytes', 'sha256']):
    raise RuntimeError('Git predecessor manifest differs from preserved tree')
current_pin = pin(ROOT / manifest_name, manifest_name)
if current_pin['sha256'] == old_pin['sha256']:
    raise RuntimeError('Expected regenerated current publication manifest')
old_checker = (ROOT / CHECKER).read_text()
anchor = " for r in tree['files']:\n  if r['path']in HISTORY:\n"
replacement = (
    " for r in tree['files']:\n"
    "  if r['path']=='provenance/publication_manifest.json':\n"
    "   archived=dict(r,path=AUD+'/manifest_history/predecessor_publication_manifest.json')\n"
    "   p=bind(root,archived);need(not p.is_symlink() and bool(p.stat().st_mode&0o111)==(r['mode']=='100755'),'Predecessor manifest mode preserved');continue\n"
    "  if r['path']in HISTORY:\n"
)
if old_checker.count(anchor) != 1:
    raise RuntimeError('Exact unique tree-loop insertion required')
(ROOT / CHECKER).write_text(old_checker.replace(anchor, replacement))
new_checker_pin = pin(ROOT / CHECKER, CHECKER)
changes = []
for name in individuals + [shared_path]:
    data = json.loads((ROOT / name).read_text())
    checker_rows = [r for r in data['bindings'] if r['path'] == CHECKER]
    if len(checker_rows) != 1 or checker_rows[0]['sha256'] != routes[CHECKER]['sha256']:
        raise RuntimeError('Exact previously accepted checker required')
    checker_rows[0].update(new_checker_pin)
    if name == shared_path:
        for row in data['bindings']:
            if row['path'] in individuals:
                row.update(pin(ROOT / row['path'], row['path']))
    data['publication_manifest_correction'] = {
        'previous_gate': routes[name],
        'previous_checker': routes[CHECKER],
        'predecessor_manifest': old_pin,
        'scope': 'Only the regenerated publication manifest is checked at its immutable predecessor path in the old-tree audit. Current tracked-file integrity remains checked by publication_rows in verify_snapshot.py. Mathematical acceptance and credits are unchanged.'
    }
    data['bindings'] += [routes[name], routes[CHECKER], old_pin]
    write_json(ROOT / name, data)
    changes.append(pin(ROOT / name, name))
record = {
    'status': 'ROOT_AUTHORED_MINIMAL_MANIFEST_CORRECTION_AWAITING_DISTINCT_REVIEW',
    'baseline': BASELINE,
    'old_routes': routes,
    'predecessor_manifest': old_pin,
    'regenerated_manifest_at_detection': current_pin,
    'new_checker': new_checker_pin,
    'changed_gates': changes,
    'history_routes_changed': False,
    'history_checker_changed': False,
    'mathematics_changed': False,
    'new_source_credit': 0,
    'new_measurements': 0
}
write_json(HERE / 'correction.json', record)
write_json(ROOT / ARCHIVE / 'correction.json', record)
print(json.dumps({'status': record['status'], 'checker': new_checker_pin,
                  'archived_files': len(routes) + 1, 'changed_gates': len(changes)}))
