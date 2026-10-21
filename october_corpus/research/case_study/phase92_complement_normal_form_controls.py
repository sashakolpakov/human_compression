#!/usr/bin/env python3
"""Author negative controls for exact certificate regeneration and no-clobber."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
PROGRAM='phase92_complement_normal_form.py'
CERTIFICATE='phase92_complement_normal_form_certificate.json'

def require(ok,message):
    if not ok:raise ValueError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):return {str(p.relative_to(path)):digest(p) for p in sorted(path.rglob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--successful-replay-dir',type=Path,required=True)
    a=ap.parse_args()
    require(not a.output_dir.exists() and not a.output_dir.is_symlink(),'New control directory required')
    a.output_dir.mkdir(parents=True)
    original=json.loads((ROOT/CERTIFICATE).read_text());rows=[]
    for kind in ['forward_image','reverse_witness','automorphism','tree_endpoint','binary_kernel']:
        data=copy.deepcopy(original)
        if kind=='forward_image':data['original_generator_target_normal_forms']['40']=[]
        if kind=='reverse_witness':data['reverse_relation_witnesses']['176']['cyclic_core']=[]
        if kind=='automorphism':data['action_generator_images'][0]['16']=[16]
        if kind=='tree_endpoint':data['coset_square_complex']['spanning_tree'][0]['A_vertex']=7
        if kind=='binary_kernel':data['mod2_module']['kernel_basis']=[32768]
        path=a.output_dir/(kind+'.json');path.write_text(json.dumps(data,indent=2)+'\n')
        output=a.output_dir/(kind+'-out')
        proc=subprocess.run([sys.executable,'-O',str(ROOT/PROGRAM),'--expected-certificate',str(path),
                             '--output-dir',str(output)],capture_output=True,text=True)
        require(proc.returncode!=0 and not output.exists(),'Altered certificate admitted: '+kind)
        require('Distributed certificate differs' in proc.stderr,'Unexpected rejection')
        rows.append(dict(kind=kind,returncode=proc.returncode,output_absent=True))
    for kind,name in [('model','phase66_coprime_cover_permutation_model.json'),
                      ('trace','phase83_word_elimination.json')]:
        folder=a.output_dir/(kind+'-inputs');folder.mkdir()
        for f in [PROGRAM,'phase66_coprime_cover_permutation_model.json','phase83_word_elimination.json']:
            shutil.copyfile(ROOT/f,folder/f)
        with (folder/name).open('ab') as f:f.write(b'\n')
        output=folder/'out'
        proc=subprocess.run([sys.executable,'-O',str(folder/PROGRAM),'--output-dir',str(output)],
                            capture_output=True,text=True)
        require(proc.returncode!=0 and not output.exists() and 'Frozen input changed' in proc.stderr,
                'Changed frozen input admitted')
        rows.append(dict(kind=kind,returncode=proc.returncode,output_absent=True))
    before=inventory(a.successful_replay_dir)
    require(len(before)==2,'Unexpected successful-run output inventory')
    existing=a.output_dir/'existing-file';existing.write_text('preserve\n')
    dangling=a.output_dir/'dangling-link';dangling.symlink_to(a.output_dir/'absent')
    refused=[]
    for kind,path in [('directory',a.successful_replay_dir),('file',existing),('dangling_symlink',dangling)]:
        proc=subprocess.run([sys.executable,'-O',str(ROOT/PROGRAM),'--output-dir',str(path)],
                            capture_output=True,text=True)
        require(proc.returncode!=0 and 'Fresh output directory required' in proc.stderr,'Occupied output not refused')
        refused.append(dict(kind=kind,returncode=proc.returncode))
    require(inventory(a.successful_replay_dir)==before and existing.read_text()=='preserve\n' and dangling.is_symlink(),
            'Existing output altered')
    result=dict(status='PASS',date='2026-10-10',malformed_inputs_rejected=rows,
                no_clobber=refused,preserved_output_files=before,optimized_python=True,
                program_sha256=digest(ROOT/PROGRAM),certificate_sha256=digest(ROOT/CERTIFICATE),
                controls_sha256=digest(Path(__file__)),scope='Author interface controls; independent theorem review remains required.')
    (a.output_dir/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
