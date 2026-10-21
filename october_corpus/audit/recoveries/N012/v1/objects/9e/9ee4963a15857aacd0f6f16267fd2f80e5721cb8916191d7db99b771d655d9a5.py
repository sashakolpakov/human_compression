"""Integrity and exact-algebra replay for the finite H component."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError("Validation requires Python assertions; optimized Python is unsupported.")

def read(path):
    return json.loads(path.read_text())

def binding_ok(path, binding):
    data=path.read_bytes()
    return len(data)==binding['bytes'] and hashlib.sha256(data).hexdigest()==binding['sha256']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--study-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    args.out.mkdir(parents=True,exist_ok=True)
    checks=0
    for b in read(here/'manifest.json')['exports']:
        assert binding_ok(here/b['path'],b), b['path']
        checks+=1
    acquired=0
    for b in read(here/'dependencies.json')['bindings']:
        p=args.study_root/b['path']
        assert binding_ok(p,b),b['path']
        checks+=1
        if p.name=='manifest.json':
            for x in read(p).get('exports',[]):
                assert binding_ok(p.parent/x['path'],x),x['path']
                acquired+=1
    probe=read(here/'manifest.json')['exports'][0]
    assert not binding_ok(here/probe['path'],dict(probe,bytes=probe['bytes']+1))
    assert not binding_ok(here/probe['path'],dict(probe,sha256='0'*64))
    work=args.out/'algebra';work.mkdir(exist_ok=True)
    for name in ['finite_H.tex','check_h6_prime_word.py','h6_3_word_letters_v2.g','check_finite_H_words.py']:
        shutil.copyfile(here/name,work/name)
    child_env=dict(os.environ)
    child_env.pop('PYTHONOPTIMIZE',None)
    prime=subprocess.run([sys.executable,'check_h6_prime_word.py'],cwd=work,capture_output=True,text=True,env=child_env)
    (args.out/'prime_stdout.txt').write_text(prime.stdout+prime.stderr)
    assert prime.returncode==0,prime.stderr
    word=json.loads(prime.stdout)
    assert word['status']=='PASS' and word['tex_literal_exact']
    symbolic=subprocess.run([sys.executable,'check_finite_H_words.py'],cwd=work,capture_output=True,text=True,env=child_env)
    (args.out/'symbolic_stdout.txt').write_text(symbolic.stdout+symbolic.stderr)
    assert symbolic.returncode==0,symbolic.stderr
    exact=read(work/'finite_H_words_report.json')
    assert exact==read(here/'finite_H_words_report.json')
    assert len(exact['identities'])==42
    scope=read(here/'scope.json')
    assert scope['whole_original_credit']==scope['new_question_credit']==scope['new_Lean_credit']==0
    assert scope['field_characteristic']=='odd' and scope['new_factor'] is None
    report={'status':'PASS','export_and_direct_bindings':checks,'acquired_exports':acquired,
            'exact_polynomial_identities':42,'prime_word':word,'damaged_binding_controls':2,
            'new_whole_original_credit':0,'new_Lean_credit':0,'long_search_repeated':False}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':
    main()
