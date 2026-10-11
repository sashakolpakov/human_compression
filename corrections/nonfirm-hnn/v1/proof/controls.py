"""Concrete incorrect-data controls for the literal S4 reconstruction."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

source = Path(__file__).with_name('literal_s4.py').read_text()
mutations = [
    ('wrong sixth named subgroup', 'subgroup([r])]', 'subgroup([a])]'),
    ('identity automorphism', 'phi=lambda x:mul(mul(b,x),b)', 'phi=lambda x:x'),
    ('unclosed sixth output base', 'K=subgroup([r,s]);', 'K=subgroup([r]);'),
    ('unshifted third output coset', 'F=[P[0],P[1],coset(a,K)]', 'F=[P[0],P[1],coset(one,K)]'),
]
results = []
with tempfile.TemporaryDirectory(prefix='N005-s4-controls-') as tmp:
    for number, (label, old, new) in enumerate(mutations):
        if source.count(old) != 1:
            raise ValueError('mutation anchor is not unique: '+label)
        path = Path(tmp)/f'case_{number}.py'
        path.write_text(source.replace(old, new))
        run = subprocess.run([sys.executable, '-B', '-O', str(path)], text=True, capture_output=True)
        if run.returncode == 0 or 'ValueError:' not in run.stderr:
            raise ValueError('incorrect model was not rejected: '+label)
        results.append({'label': label, 'rejected': True,
                        'reason': run.stderr.split('ValueError:')[-1].strip()})
print(json.dumps({'status': 'PASS', 'controls': results}, indent=2))
