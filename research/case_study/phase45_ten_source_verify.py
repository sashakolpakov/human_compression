#!/usr/bin/env python3
"""Verify the new manuscript's complete embedded programs and optional replay.

All output goes to a fresh directory. Frozen component files are read only.
Default is structural verification; --run executes all four exact programs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

P = Path(__file__).resolve().parent
PROGRAMS = [
    'phase37_compress_twogroups_census.g',
    'phase40_compress_operations_check.g',
    'phase40_compress_operations_exhaustive.g',
    'phase41_chiral_cover_check.g',
]
EXPECTED_HASHES = [
    '0a1e993362b263c9ef23e8fca5103c3a2b766a937a2f9af7608fbca8252d2752',
    'f1d49b61e210e0026468a2bcb2621399e5fda10778893fd1c20d364019f54810',
    'bfe4190665e751a3c65d00fd692ae0a6059d25f6345fd11f0efdc5a5a938c952',
    '59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e',
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--gap', default='/opt/homebrew/bin/gap')
    args = ap.parse_args()
    if args.output_dir.exists():
        ap.error('output directory already exists; refusing to overwrite any artifact')
    manuscript = P/'phase45_ten_source_manuscript.md'
    data = manuscript.read_bytes()
    text = data.decode()
    blocks = re.findall(r'```gap\n(.*?)\n```', text, re.S)
    assert len(blocks) == 4, 'expected exactly four complete GAP programs'
    code = [(x.rstrip()+'\n').encode() for x in blocks]
    for name, body, expected in zip(PROGRAMS, code, EXPECTED_HASHES):
        assert sha(body) == expected, f'embedded bytes differ: {name}'
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    assert len(tags) == len(set(tags)), 'duplicate equation labels'
    sections = re.findall(r'^## (\d+)\.', text, re.M)
    assert sections == [str(i) for i in range(1,25)], 'section sequence changed'
    assert 'PSL₂(11)' in text and 'PSL₂(O11)' not in text
    assert 'Targets: Theorem 3.1, Proposition 3.2' in text
    for prefix, n in [('O',14),('V',8)]:
        for i in range(1,n+1):
            assert prefix+str(i) in tags, f'missing equation {prefix}{i}'
    assert '**Theorem K (intersection transport and exact coset transport).**' in text
    assert text.count('**(0) Three-subgroup transport.**') == 1
    assert '**Kernel transport K.**' not in text, 'duplicate component proof'
    contract = json.loads((P/'phase45_ten_source_adapter_map.json').read_text())
    assert len(contract['contracts']) == 79
    expected_ids = {'N001','N003','N008','L032','L035','F013','F016','L088','N013','N016'}
    assert set(contract['candidate_source_ids']) == expected_ids
    for row in contract['contracts']:
        span = row['integrated_proof_span']
        snippet = text[span['start_codepoint']:span['end_codepoint_exclusive']]
        assert sha(snippet.encode()) == span['sha256_utf8'], row['integration_id']
    args.output_dir.mkdir(parents=True)
    report = {
        'status':'structural_pass', 'manuscript_sha256':sha(data),
        'equation_tags':len(tags), 'contract_rows_checked':79,
        'component_replay_claim':'Existing reviews bind these unchanged exact program bytes; no new execution is implied without --run.',
        'programs':[], 'source_count_admitted':False, 'ratio':None,
    }
    for i,(name,body) in enumerate(zip(PROGRAMS,code),1):
        folder=args.output_dir/f'appendix_{i}'
        folder.mkdir()
        script=folder/'certificate.g'
        script.write_bytes(body)
        row={'component_path':name,'sha256':sha(body),'bytes':len(body),'executed':False}
        if args.run:
            gap=shutil.which(args.gap)
            if not gap:
                raise RuntimeError(f'GAP executable not found: {args.gap}')
            begin=time.monotonic()
            with (folder/'replay.log').open('wb') as log:
                result=subprocess.run([gap,'-q','certificate.g'],cwd=folder,stdout=log,stderr=subprocess.STDOUT)
            row.update(executed=True,exit_code=result.returncode,seconds=time.monotonic()-begin,
                       log_sha256=sha((folder/'replay.log').read_bytes()))
            if result.returncode:
                report['status']='replay_failed'
                report['programs'].append(row)
                (args.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
                raise RuntimeError(f'Appendix {i} returned {result.returncode}')
            logtext=(folder/'replay.log').read_text()
            assert 'Error,' not in logtext and 'FAIL' not in logtext, f'GAP error in appendix {i}'
            print(f'Appendix {i} complete in {row["seconds"]:.2f}s',flush=True)
        report['programs'].append(row)
    if args.run: report['status']='structural_and_four_replays_pass'
    (args.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
