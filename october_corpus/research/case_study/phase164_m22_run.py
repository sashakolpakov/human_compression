#!/usr/bin/env python3
"""Reproduce the new M22 census in an isolated, non-overwriting directory.

The source table is not read. This replay proves only the explicitly stated
census/shadow contract; it does not resolve the historical refined table labels.
"""
import argparse, hashlib, json, shutil, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROGRAMS=[('phase164_m22_census.g','census','M22_EXHAUSTIVE_FINISHED'),('phase164_m22_validate.g','validate','M22_WITNESSES_VALIDATED'),('phase164_m22_shadows.g','shadows','SHADOW_DECODING_COMPLETE 431')]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--gap',default=shutil.which('gap'))
    a=p.parse_args();out=a.output_dir
    if out.exists() or out.is_symlink():p.error('Refusing existing output path')
    if not a.gap:p.error('GAP unavailable')
    inputs={n:sha(ROOT/n) for n,_,_ in PROGRAMS}
    out.mkdir(parents=True)
    for name,_,_ in PROGRAMS:shutil.copyfile(ROOT/name,out/name)
    (out/'environment.g').write_text('LoadPackage("tomlib");;Print("GAP ",GAPInfo.Version," TOMLIB ",PackageInfo("tomlib")[1].Version,"\\n");QUIT;\n')
    records=[]
    for name,label,footer in [('environment.g','environment','TOMLIB')]+PROGRAMS:
        start=time.monotonic()
        with (out/(label+'.log')).open('w') as f:
            run=subprocess.run([a.gap,'-q','-b',name],cwd=out,stdout=f,stderr=subprocess.STDOUT,text=True)
        text=(out/(label+'.log')).read_text()
        record=dict(program=name,exit_code=run.returncode,seconds=time.monotonic()-start,log_sha256=sha(out/(label+'.log')),footer=footer)
        record['passed']=run.returncode==0 and footer in text and 'Error,' not in text
        records.append(record)
        (out/'replay.json').write_text(json.dumps(dict(status='running',inputs=inputs,records=records),indent=2)+'\n')
        if not record['passed']:raise SystemExit('Failed '+label+'; inspect isolated log')
        print(label+' PASS',flush=True)
    if any(sha(ROOT/n)!=digest for n,digest in inputs.items()):raise SystemExit('Source program changed during replay')
    witness=out/'phase164_m22_witnesses.g';shadow=out/'phase164_m22_shadow_data.json'
    decoded=json.loads(shadow.read_text())
    if len(decoded['triples'])!=431:raise SystemExit('Incomplete geometric decoding')
    report=dict(status='PASS_author_replay_not_independent_review',inputs=inputs,records=records,witnesses_sha256=sha(witness),shadow_data_sha256=sha(shadow),source_geometry_inputs=False,full_source_table_contract_complete=False)
    (out/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print('M22 census and shadow replay PASS; refined source table comparison remains separate')
if __name__=='__main__':main()
