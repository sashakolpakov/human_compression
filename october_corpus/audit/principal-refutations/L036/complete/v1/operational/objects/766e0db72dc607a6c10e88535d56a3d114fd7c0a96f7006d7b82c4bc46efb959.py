"""Replay the five exact integer calculations and the explicit L073 import."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
RAW_SHA='7ea5d09b6f4c0fc2c8d384b83e7e155bd944ee03c60ac57463066d316c506bb1'


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):return json.loads(path.read_text())


def main(a):
    need(a.out.is_absolute() and not a.out.exists(),'Fresh absolute output')
    deps=load(HERE/'dependencies.json')
    for row in deps:
        p=Path(row['path'])
        need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact input '+str(p))
    imports=load(HERE/'imports.json')
    need(imports['source_ids']==['L073'] and imports['target_source_ids']==['L036'] and imports['rank_two_count']==81,'Exact imported claim')
    adm=load(Path(imports['admission']['path']))
    need(adm['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and adm['source_ids']==['L073'] and adm['rank_two_classes']==81,'Existing accepted L073 result')
    request=load(HERE.parent/'character_request02/request.json')
    receipt=load(HERE.parent/'character_execution01/receipt.json')
    need(receipt['reason']=='completed' and receipt['returncode']==0 and receipt['seconds']<30,'Actual bounded successful export')
    need(receipt['request_sha256']==sha(HERE.parent/'character_request02/request.json'),'Actual exact request')
    need((HERE.parent/'character_execution01/stderr').read_bytes()==b'','Empty actual stderr')
    raw=HERE.parent/'character_execution01/stdout'
    need(sha(raw)==RAW_SHA,'Exact acquired raw output')
    a.out.mkdir()
    command=[sys.executable,str(HERE/'arithmetic.py'),'--input',str(raw),'--expected-sha',RAW_SHA,'--out',str(a.out/'arithmetic.json')]
    run=subprocess.run(command,capture_output=True,timeout=30)
    (a.out/'arithmetic.stdout').write_bytes(run.stdout);(a.out/'arithmetic.stderr').write_bytes(run.stderr)
    need(run.returncode==0 and not run.stderr,'Fresh independent arithmetic')
    actual=load(a.out/'arithmetic.json')
    need(actual==load(HERE/'arithmetic01.json'),'Exact repeat of all acquired values and structural controls')
    guards=[]
    for flag in ['-O','-OO']:
        r=subprocess.run([sys.executable,flag,str(HERE/'arithmetic.py')],capture_output=True,timeout=5)
        need(r.returncode!=0 and b'Ordinary Python required' in r.stderr,'Optimization rejected')
        guards.append(flag)
    native=[]
    if a.render:
        for stem,pages in [('theory',3),('totals',2)]:
            shutil.copyfile(HERE/(stem+'.tex'),a.out/(stem+'.tex'))
            for i in [1,2]:
                r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=a.out,capture_output=True,timeout=30)
                (a.out/f'{stem}-pass{i}.stdout').write_bytes(r.stdout);(a.out/f'{stem}-pass{i}.stderr').write_bytes(r.stderr)
                need(r.returncode==0 and not r.stderr,'Exact standalone TeX compilation')
            need('Overfull' not in (a.out/(stem+'.log')).read_text(),'Readable proof layout')
            need(len(PdfReader(a.out/(stem+'.pdf')).pages)==pages,'Exact proof page count')
            r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+stem+'-%02d.png',stem+'.pdf'],cwd=a.out,capture_output=True,timeout=30)
            need(r.returncode==0 and not r.stdout and not r.stderr,'Exact native proof rendering')
            for i in range(1,pages+1):
                name=f'{stem}-{i:02d}.png';native.append(dict(path=name,sha256=sha(a.out/name)))
        if (HERE/'native_review.json').is_file():
            need(native==load(HERE/'native_review.json')['pages'],'Exact fresh native mathematical pages')
    report=dict(status='PASS_L036_FIVE_CHARACTER_TOTALS_AND_L073_IMPORT',dependency_bindings=len(deps),
                counts={row['name']:row['unordered_pair_orbits'] for row in actual['groups']},imported_M22_count=81,
                damage_controls=actual['controls'],optimization_guards=guards,native_pages=native,
                new_group_searches=0,new_ordinary_recovery_credit=0,new_refutation_credit=0,
                whole_source_complete=False,retained_classification_premises=True)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true')
    main(p.parse_args())
