#!/usr/bin/env python3
"""Reject changed project proof bytes through the portable source-dir interface."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args()
    packet=args.packet.resolve()
    with tempfile.TemporaryDirectory(prefix='topic_A_product_control_',dir='/private/tmp') as tmp:
        base=Path(tmp)
        source=base/'source';source.mkdir()
        for name in ('NormalKernelRecognition.lean','NormalKernelProduct.lean'):
            content=(packet/name).read_bytes()
            if name=='NormalKernelProduct.lean':
                content+=b'\n-- Independent changed-source control.\n'
            (source/name).write_bytes(content)
        proc=subprocess.run([sys.executable,'-B','-O',str(packet/'check.py'),
            '--source-dir',str(source),'--out',str(base/'replay')],
            text=True,capture_output=True,timeout=180)
        expected='Changed proof source: NormalKernelProduct.lean'
        if proc.returncode==0 or expected not in proc.stderr:
            raise RuntimeError('Changed source was not rejected at its expected binding.')
        if (base/'replay'/'NormalKernelProduct.olean').exists():
            raise RuntimeError('A changed product module unexpectedly compiled.')
        report={'status':'PASS','control':'changed NormalKernelProduct source bytes',
            'returncode':proc.returncode,'expected_rejection':expected,
            'rejected_before_changed_module_compilation':True,
            'source_dir_interface_used':True,
            'checker_sha256':hashlib.sha256((packet/'check.py').read_bytes()).hexdigest(),
            'stdout':proc.stdout,'stderr':proc.stderr,
            'limit':'Tests byte binding of the frozen source, not proof completeness. Mathematical scope is assessed separately by reading every statement and proof.'}
        args.report.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'status':'PASS','report':str(args.report)}))

if __name__=='__main__':main()
