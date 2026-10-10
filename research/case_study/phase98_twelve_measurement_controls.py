#!/usr/bin/env python3
"""Author rejection controls for phase98. Private inputs required; no proof test."""
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def snapshot(d):
    return {str(p.relative_to(d)):sha(p.read_bytes()) for p in sorted(d.rglob('*')) if p.is_file() and not p.is_symlink()}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--existing-replay',type=Path,required=True)
    a=ap.parse_args();o=a.output_dir.absolute();require(not os.path.lexists(o),'Fresh controls directory required')
    proto=P/'phase98_twelve_measurement_protocol.json';raw=proto.read_bytes()
    require(sha(raw)=='f297f3509ba598b5fc375e101a21e7381049d38d6cb27717c5287cc77b89f0ee','Protocol changed');p=json.loads(raw)
    runner=P/'phase98_twelve_measurement.py';before=snapshot(a.existing_replay);o.mkdir();rows=[]
    cmd=[sys.executable,'-O',str(runner)]
    for name,target in [('directory',a.existing_replay),('file',o/'existing-file'),('dangling-symlink',o/'dangling-output')]:
        if name=='file':target.write_bytes(b'preserve this file\n')
        if name=='dangling-symlink':target.symlink_to(o/'nonexistent-link-target')
        r=subprocess.run(cmd+['--output-dir',str(target)],capture_output=True,text=True)
        require(r.returncode!=0 and 'Refusing existing output directory' in r.stderr,'Failed existing-path rejection '+name)
        if name=='file':require(target.read_bytes()==b'preserve this file\n','Existing file changed')
        if name=='dangling-symlink':require(target.is_symlink() and os.readlink(target)==str(o/'nonexistent-link-target') and not (o/'nonexistent-link-target').exists(),'Dangling link changed')
        rows.append(dict(control='existing_'+name,rejected=True,returncode=r.returncode,stderr=r.stderr))
    require(snapshot(a.existing_replay)==before,'Existing replay files changed')
    bindings=p['contract_bindings']+p['external_costs']+[p['measurement_helper'],p['render_helper']]
    files={b['path']:b['sha256'] for b in bindings}
    for key in p['source_keys']:
        s=p['documents'][key];files[s['pdf_path']]=s['pdf_sha256']
    for key in p['replacement_keys']:
        s=p['documents'][key];files[s['path']]=s['sha256']
    files[proto.name]=sha(raw)
    tree=o/'isolated-inputs';tree.mkdir()
    for name,digest in files.items():
        src=P/name;require(sha(src.read_bytes())==digest,'Input changed '+name)
        dst=tree/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    mutations=[('protocol',proto.name),('manuscript','phase78_n009_integration_manuscript.md'),
      ('code','phase78_n009_integration_census.g'),('data','phase78_n009_integration_data.g'),
      ('review','phase87_n009_integration_recent_audit.json'),('boundary','phase98_twelve_measurement_N009_spec.json'),
      ('metric-helper',p['measurement_helper']['path']),('primary-pdf',p['documents']['N009']['pdf_path'])]
    for label,name in mutations:
        target=tree/name;original=target.read_bytes();target.write_bytes(original+b'\nAUTHOR_MUTATION_REJECTION_CONTROL\n')
        out=o/('rejected-'+label)
        r=subprocess.run(cmd+['--input-root',str(tree),'--protocol',str(tree/proto.name),'--output-dir',str(out)],capture_output=True,text=True)
        require(r.returncode!=0 and 'Bound input changed:' in r.stderr,'Mutation did not fail at hash boundary '+label)
        require(not os.path.lexists(out),'Output created before input rejection '+label)
        target.write_bytes(original)
        rows.append(dict(control='changed_'+label,input=name,rejected=True,returncode=r.returncode,output_created=False,stderr=r.stderr))
    for name,digest in files.items():require(sha((P/name).read_bytes())==digest and sha((tree/name).read_bytes())==digest,'Input not preserved/restored '+name)
    require(snapshot(a.existing_replay)==before,'Existing replay changed during mutation controls')
    report=dict(status='PASS_author_rejection_controls_not_independent_review',runner_sha256=sha(runner.read_bytes()),protocol_sha256=sha(raw),controls_sha256=sha(Path(__file__).read_bytes()),
      no_clobber_cases=3,existing_replay_files_preserved=len(before),mutation_cases=8,all_private_originals_unchanged=True,rows=rows,
      scope='Controlled single-input changes in private copies; existing directory/file/dangling-link refusal. No mathematical or independent metric proof.',primary_assets_exported=False)
    with (o/'report.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:report[k] for k in ['status','no_clobber_cases','existing_replay_files_preserved','mutation_cases']}))
if __name__=='__main__':main()
