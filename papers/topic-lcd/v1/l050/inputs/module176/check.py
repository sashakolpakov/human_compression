#!/usr/bin/env python3
"""Portable exact replay; retained enumeration is checked, never repeated."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
import certificate


def need(test,message):
    if not test:
        raise ValueError(message)


def run(command,cwd,log,marker=None):
    p=subprocess.run(list(map(str,command)),cwd=cwd,text=True,capture_output=True,timeout=120)
    text=p.stdout+p.stderr
    log.write_text(text)
    need(p.returncode==0 and 'Error,' not in text,'failed command: '+repr(command))
    need(marker is None or marker in text,'missing success marker')
    return text


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--render',action='store_true')
    p.add_argument('--pdflatex',default='pdflatex')
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    if (root/'manifest.json').exists():
        for row in json.loads((root/'manifest.json').read_text())['exports']:
            f=root/row['path']
            need(f.is_file() and f.stat().st_size==row['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],
                 'frozen export mismatch: '+row['path'])
    binding=json.loads((root/'bindings.json').read_text())
    if a.study_root:
        for row in binding['inputs']:
            f=a.study_root/row['path']
            need(f.is_file() and f.stat().st_size==row['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],
                 'external binding mismatch: '+row['path'])
    for name,sha in binding['retained_copies'].items():
        need(hashlib.sha256((root/'retained'/name).read_bytes()).hexdigest()==sha,'retained input mismatch: '+name)
    enumeration_manifest=json.loads((root/'retained/enumeration_manifest.json').read_text())
    exports={row['path']:row for row in enumeration_manifest['exports']}
    for original,copyname in [('176_adjacency.json','176_adjacency.json'),('bases/176_adjacency.txt','176_basis.txt'),('receipt.json','enumeration_receipt.json')]:
        f=root/'retained'/copyname
        need(exports[original]['sha256']==hashlib.sha256(f.read_bytes()).hexdigest(),'enumeration manifest interface')
    receipt=json.loads((root/'retained/enumeration_receipt.json').read_text())
    need(receipt['results']['176_adjacency']['enumeration_sha256']==exports['176_adjacency.json']['sha256'],'receipt interface')
    need(receipt['method_review_sha256']==hashlib.sha256((root/'retained/enumeration_method_review_manifest.json').read_bytes()).hexdigest(),'distinct method acceptance')
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    data=json.loads((root/'module_data.json').read_text())
    basis=root/'retained/176_basis.txt';enum=root/'retained/176_adjacency.json'
    result=certificate.inspect(data,basis,enum,out/'certificate')
    run([a.gap,'-q','-b','-T',out/'certificate/constructed.g',root/'identify.g'],out/'certificate',out/'identification.log','LCD176_IDENTIFICATION_PASS')
    controls=[]
    def rejected(name,changed,changed_enum,expected):
        try:
            certificate.inspect(changed,basis,changed_enum,out/('mutation_'+str(len(controls))))
        except (RuntimeError,ValueError) as e:
            need(expected in str(e),'wrong rejection: '+name+': '+str(e))
            controls.append({'name':name,'rejected_at':str(e)})
        else:
            raise ValueError('accepted corruption: '+name)
    changed=copy.deepcopy(data);changed['minimum_seed']=[0]*176
    rejected('zero minimum seed',changed,enum,'minimum seed weight')
    changed=copy.deepcopy(data)
    i=next(i for i,x in enumerate(changed['minimum_seed']) if x)
    changed['minimum_seed'][i]=3-changed['minimum_seed'][i]
    rejected('same-weight noncode seed',changed,enum,'seed membership')
    changed=copy.deepcopy(data);changed['coordinate_generators'][0][0]=changed['coordinate_generators'][0][1]
    rejected('nonpermutation generator',changed,enum,'literal permutations')
    changed=copy.deepcopy(data);changed['coordinate_generators'][1]=changed['coordinate_generators'][0][:]
    rejected('proper subgroup substituted',changed,enum,'two disjoint scalar orbits')
    record=json.loads(enum.read_text());record['weight_counts'][56]-=2
    bad=out/'incomplete_enumeration.json';bad.write_text(json.dumps(record))
    rejected('wrong complete minimum count',data,bad,'retained exact minimum-word count')
    record=json.loads(enum.read_text());record['weight_counts'][0]=2
    bad=out/'wrong_total.json';bad.write_text(json.dumps(record))
    rejected('wrong complete distribution',data,bad,'complete retained weight distribution')
    products,_=certificate.matrix_algebra([np.eye(21,dtype=np.int64)])
    need(len(products)==1 and len(products)!=441,'scalar representation falsely certified irreducible')
    controls.append({'name':'scalar matrices do not certify irreducibility','matrix_algebra_dimension':len(products)})
    # Deleting supports removes the informative upper bound, rather than silently
    # certifying the supplied subgroup as full. Small literal graph suffices.
    chain,upper=certificate.refinement_bound([],6)
    need(upper==720 and len(chain)==5,'empty incidence lost symmetric group bound')
    controls.append({'name':'unconstrained six-coordinate support structure','actual_upper_bound':upper})
    if a.render:
        render=out/'render';render.mkdir()
        for i in range(2):
            log=run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(render),root/'modules.tex'],root,out/f'render_{i}.log')
        need(not any(s in log for s in ['Overfull','Missing character','undefined references']),'render diagnostics')
    report={'status':'PASS','scope':'L050 Theorem1(c)/Proposition4 bounded module and group supplement',
            'certificate':result,'identification':json.loads((out/'certificate/identification.json').read_text()),
            'controls':controls,'external_bindings_checked':bool(a.study_root),'rendered':a.render,
            'retained_enumeration_recomputed':False,'full_source_admission':False}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','controls':len(controls),'group_order':result['explicit_group_order'],
                      'matrix_algebra_dimension':result['generated_matrix_algebra_dimension']},sort_keys=True))


if __name__=='__main__':
    main()
