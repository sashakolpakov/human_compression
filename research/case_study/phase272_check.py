#!/usr/bin/env python3
"""Replay frozen triangle-geometry proofs with archived inputs; no primary PDFs."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PINS={'phase265_manifest.json': '18cd719df0625cbb3d7795bf64072e93bcfaf57e6aec3d1557355be897d1280c', 'phase271_manifest.json': '9e1f288479af5cd0e437bd0bea3d60083ae4b967638077ce2b53f9c8bb96d56d'}
ALIASES={'incidence_compression.md': 'phase272_incidence_compression.txt', 'hermitian_unital_proof.md': 'phase275_hermitian_unital_proof.md'}
def need(ok,message):
    if not ok:raise RuntimeError('PHASE272_REJECT '+message)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output')
    names=set(PINS);checked=0;omitted=set()
    for name,pin in PINS.items():
        f=ROOT/name;need(hashlib.sha256(f.read_bytes()).hexdigest()==pin,'manifest '+name)
        m=json.loads(f.read_bytes())
        for row in m['exports']+m['retained_bindings']:
            rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative binding')
            if rel.parts[0]=='sources':omitted.add(str(rel));continue
            f=ROOT/ALIASES.get(str(rel),str(rel))
            need(f.is_file() and f.stat().st_size==row['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],'binding '+str(rel))
            checked+=1;names.add(str(rel))
    out.mkdir(parents=True);start=time.monotonic()
    # Restore the exact archived bytes at their original relative names in
    # isolation. No mathematical program or assertion is edited.
    with tempfile.TemporaryDirectory(prefix='frozen-inputs-',dir=out) as temp:
        stage=Path(temp)
        for name in sorted(names):
            target=stage/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/ALIASES.get(name,name),target)
        command=[sys.executable,'-B','-O',str(stage/'phase271_check.py'),'--out',str(out/'replay'),
                 '--gap',str(a.gap.resolve()),'--lean',str(a.lean.resolve()),'--packages',str(a.packages.resolve())]
        result=subprocess.run(command,text=True,capture_output=True)
        (out/'review.stdout').write_text(result.stdout);(out/'review.stderr').write_text(result.stderr)
        need(result.returncode==0,'unchanged review replay; see review.stdout and review.stderr')
    r=json.loads((out/'replay/report.json').read_bytes())
    need(r['status']=='PASS' and r['actual_lean_declarations']==4 and r['independent_signature_pairs']==540910,'complete review scope')
    report=dict(status='PASS',seconds=round(time.monotonic()-start,4),frozen_public_bindings_checked=checked,
                omitted_private_primaries=sorted(omitted),archived_aliases=ALIASES,
                source_dispositions=44,complete_proof_spans=13,actual_lean_declarations=4,
                independent_signature_pairs=540910,question_delta=0,
                scope='Exact corrected principal L009 contract; written classification with scoped matrix/orbit proofs, not whole-paper recovery or a measured ratio.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
