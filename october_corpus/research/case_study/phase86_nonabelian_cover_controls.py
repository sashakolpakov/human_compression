#!/usr/bin/env python3
"""Negative controls for this review's independent exact-word checkers."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def inventory(path):
    return {str(p.relative_to(path)):sha(p.read_bytes()) for p in sorted(path.rglob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--successful-replay-dir',type=Path,required=True)
    args=ap.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(), 'New control directory required')
    model=ROOT/'phase66_coprime_cover_permutation_model.json'
    certificate=ROOT/'phase83_word_elimination.json'
    lean=ROOT/'formal/OddKernelWord.lean'
    cert=json.loads(certificate.read_text())
    text=lean.read_text()
    args.output_dir.mkdir(parents=True)
    mutations=[]
    for kind in ['quad','replacement','sign','before','final_row','defect']:
        altered=copy.deepcopy(cert)
        if kind=='quad': altered['quads'][0][0]=128
        if kind=='replacement': altered['steps'][0]['replacement'].append(1)
        if kind=='sign': altered['steps'][0]['sign']=-altered['steps'][0]['sign']
        if kind=='before': altered['steps'][0]['before'].append(1)
        if kind=='final_row': altered['remaining']['239'].append(1)
        if kind=='defect': altered['delta']=list(reversed(altered['delta']))
        mutations.append((kind,'trace',altered,None))
    mutations += [
        ('literal_cell','cells',None,text.replace('(9, 102, 128, 37)','(9, 102, 127, 37)',1)),
        ('hypothesis_use','cells',None,text.replace('hcells 9 102 128 37','hcells 9 102 127 37',1)),
        ('elimination_row','cells',None,text.replace('Original orbit row 69;','Original orbit row 68;',1)),
        ('missing_cell','cells',None,text.replace('  (9, 102, 128, 37),\n','',1)),
    ]
    rows=[]
    for label,checker,cdata,ltext in mutations:
        folder=args.output_dir/label
        folder.mkdir()
        cp=certificate; lp=lean
        if cdata is not None:
            cp=folder/'certificate.json';cp.write_text(json.dumps(cdata))
        if ltext is not None:
            lp=folder/'OddKernelWord.lean';lp.write_text(ltext)
        report=folder/'report.json'
        command=[sys.executable,'-O',str(ROOT/f'phase86_nonabelian_cover_{checker}_check.py'),
                 '--model',str(model),'--certificate',str(cp),'--report',str(report)]
        if checker=='cells':command+=['--lean',str(lp)]
        result=subprocess.run(command,text=True,capture_output=True)
        require(result.returncode!=0 and not report.exists(), 'Mutation admitted: '+label)
        rows.append(dict(mutation=label,checker=checker,returncode=result.returncode,
                         report_absent=True,error=result.stderr.strip().splitlines()[-1]))
    fixed_model=json.loads(model.read_text()); fixed_model['generators'][0][0]=128
    bad_model=args.output_dir/'mutated_model.json';bad_model.write_text(json.dumps(fixed_model))
    rp=args.output_dir/'bad_model_report.json'
    result=subprocess.run([sys.executable,'-O',str(ROOT/'phase86_nonabelian_cover_trace_check.py'),
                           '--model',str(bad_model),'--certificate',str(certificate),'--report',str(rp)],
                          capture_output=True,text=True)
    require(result.returncode!=0 and not rp.exists(),'Mutated model admitted')
    rows.append(dict(mutation='model',checker='trace',returncode=result.returncode,
                     report_absent=True,error=result.stderr.strip().splitlines()[-1]))
    old=args.successful_replay_dir
    before=inventory(old)
    require(len(before)==7,'Unexpected successful output inventory')
    occupied_file=args.output_dir/'occupied-file';occupied_file.write_text('preserve\n')
    dangling=args.output_dir/'occupied-link';dangling.symlink_to(args.output_dir/'absent-target')
    no_clobber=[]
    for label,target in [('successful_directory',old),('regular_file',occupied_file),('dangling_symlink',dangling)]:
        result=subprocess.run([sys.executable,'-O',str(ROOT/'phase83_nonabelian_cover_check.py'),
                               '--packages','/deliberately-unused','--lean','/deliberately-unused',
                               '--output-dir',str(target)],capture_output=True,text=True)
        require(result.returncode!=0 and 'New output directory required' in result.stderr,
                'Occupied output was not refused before package/compiler access')
        no_clobber.append(dict(kind=label,returncode=result.returncode,error=result.stderr.strip().splitlines()[-1]))
    require(inventory(old)==before and occupied_file.read_text()=='preserve\n' and dangling.is_symlink(),
            'Existing output changed')
    report=dict(status='PASS',date='2026-10-10',mutation_controls=rows,
                no_clobber_controls=no_clobber,preserved_successful_output_files=before,
                optimized_parent=True,checker_sha256=sha(Path(__file__).read_bytes()),
                scope='11 malformed model/trace/cell cases rejected by independent checkers; 3 occupied-output kinds rejected by the author replay runner before dependency access. This is not a claim that the author runner embeds the outer proof-manifest hashes.')
    (args.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
