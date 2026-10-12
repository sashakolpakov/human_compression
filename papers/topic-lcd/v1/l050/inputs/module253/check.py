#!/usr/bin/env python3
"""Replay the bounded certificate, with existing enumeration data retained."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
import certificate as c


def run(a):
    root = Path(__file__).resolve().parent
    binding = json.loads((root/'bindings.json').read_text())
    for row in binding['retained_files']:
        data = (root/row['path']).read_bytes()
        c.need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
               'whole retained file '+row['path'])
    c.need(hashlib.sha256((root/'steiner_construction.py').read_bytes()).hexdigest()
           == binding['shared_constructor_sha256'], 'unchanged common constructor')
    old = json.loads((root/'retained/manifest.json').read_text())
    by_path = {x['path']:x for x in old['exports']}
    for path in ['253_adjacency.json','253_differences.json','bases/253_adjacency.txt',
                 'bases/253_differences.txt','receipt.json']:
        c.need(hashlib.sha256((root/'retained'/path).read_bytes()).hexdigest()
               == by_path[path]['sha256'], 'accepted enumeration interface')
    receipt = json.loads((root/'retained/receipt.json').read_text())
    for key in ['253_adjacency','253_differences']:
        c.need(receipt['results'][key]['enumeration_sha256'] == by_path[key+'.json']['sha256'],
               'completed enumeration receipt')
    c.need(receipt['method_review_sha256'] == binding['retained_method_review_sha256']
           == hashlib.sha256((root/'retained/method_review_manifest.json').read_bytes()).hexdigest(),
           'distinct enumeration method review')
    if (root/'manifest.json').exists():
        for row in json.loads((root/'manifest.json').read_text())['exports']:
            data = (root/row['path']).read_bytes()
            c.need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                   'frozen packet '+row['path'])
    c.need(not a.out.exists(), 'fresh output')
    a.out.mkdir(parents=True)
    result = c.run(root, root/'retained', a.out/'certificate')
    proc = subprocess.run([a.gap,'-q','-b','-T',str(a.out/'certificate/constructed.g'),
                           str(root/'identify.g')], cwd=a.out/'certificate', capture_output=True,
                          text=True, timeout=120)
    (a.out/'GAP.stdout').write_text(proc.stdout+proc.stderr)
    c.need(proc.returncode == 0 and 'LCD253_IDENTIFICATION_PASS' in proc.stdout
           and 'Error,' not in proc.stdout+proc.stderr, 'exact group identification')
    controls = []
    for name, work in [
        ('scalar action cannot certify absolute irreducibility',
         lambda: c.algebra_words([np.eye(22,dtype=np.int64)])),
        ('incomplete enumeration cannot supply a dual distribution',
         lambda: c.macwilliams([1]+[0]*253,253,22)),
        ('negative weight count rejected',
         lambda: c.macwilliams([1,-1]+[0]*252,253,22))]:
        try:
            work()
        except RuntimeError as error:
            controls.append(dict(name=name,rejected_at=str(error)))
        else:
            raise RuntimeError('accepted corruption: '+name)
    if a.render:
        directory = a.out/'render'
        directory.mkdir()
        for i in range(2):
            proc = subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error',
                                   '-no-shell-escape','-output-directory='+str(directory),
                                   str(root/'modules.tex')],cwd=root,capture_output=True,text=True)
            (directory/f'pass{i+1}.stdout').write_text(proc.stdout+proc.stderr)
            c.need(proc.returncode == 0, 'proof render')
        log = (directory/'modules.log').read_text()
        c.need(not any(x in log for x in ['Warning','Overfull','Underfull','Missing character']),
               'proof render diagnostics')
    report = dict(status='PASS',certificate=result,
                  identification=json.loads((a.out/'certificate/identification.json').read_text()),
                  controls=controls,full_enumerations_repeated=False,
                  whole_source_recovered=False,rendered=a.render)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex')
    p.add_argument('--render',action='store_true')
    a = p.parse_args()
    a.out = a.out.resolve()
    r = run(a)
    print(json.dumps(dict(status=r['status'],controls=len(r['controls']),
                         group_order=r['identification']['order'],
                         matrix_algebra_dimension=484)))
