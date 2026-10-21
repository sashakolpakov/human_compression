"""Run the exact prior science72 guards on preserved historical pointers."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile

AUD='audit/science74/v1'

def verify(root):
    root=Path(root).resolve()
    routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
    for row in routes.values():
        data=(root/row['path']).read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('Historical science72 binding changed: '+row['path'])
    with tempfile.TemporaryDirectory(prefix='F003-history-') as tmp:
        historical=Path(tmp)/'repo'
        # Real paths preserve science72's containment checks. No linked file is written.
        shutil.copytree(root,historical,copy_function=os.link,
                        ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
        if (root/'.git').exists():
            (historical/'.git').symlink_to((root/'.git').resolve(),
                                           target_is_directory=(root/'.git').is_dir())
        for name,row in routes.items():
            target=historical/name
            target.unlink()
            shutil.copyfile(root/row['path'],target)
        spec=importlib.util.spec_from_file_location('immutable_science72',historical/'scripts/verify_snapshot.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.ROOT=historical
        nested=module.check_previous_science73()
        science72=module.check_science73()
        if science72['counts']['corrected_recoveries']!=73 or science72['counts']['mathematical_pending']!=31:
            raise ValueError('Historical science72 partition changed')
        return dict(status='PASS_EXACT_HISTORICAL_SCIENCE73',science72=science72,
                    legacy=nested['legacy'],current=nested['current'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    print(json.dumps(verify(parser.parse_args().repo)))
