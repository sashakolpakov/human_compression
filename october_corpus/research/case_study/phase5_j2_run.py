#!/usr/bin/env python3
"""Run/resume independent arbitrary-B J2 enumeration with per-Borel checkpoints."""
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
SCRIPT=HERE/'phase5_j2_search.g'
PROGRESS=HERE/'phase5_j2_progress.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));ap.add_argument('--borels',type=int,nargs='+');ap.add_argument('--resume',action='store_true');a=ap.parse_args()
    if not a.gap:ap.error('Set GAP or pass --gap; the executable was not found')
    ids=sorted(set(a.borels or range(1,147)))
    if not ids or any(i<1 or i>146 for i in ids):ap.error('Borel ids must be integers from1 through146')
    digest=sha(SCRIPT);(HERE/'phase5_j2_checkpoints').mkdir(exist_ok=True)
    if a.resume:
        progress=json.loads(PROGRESS.read_text());assert progress['executed_script_sha256']==digest,'Script changed: old checkpoints cannot be silently reused'
        for i,entry in progress['completed'].items():assert sha(HERE/entry['checkpoint'])==entry['sha256']
    else:
        progress={'executed_script_sha256':digest,'completed':{},'runs':[],'scope':'All subgroup classes of J2 as Borel anchors; original geometry lists are not read.'}
    remaining=[i for i in ids if str(i) not in progress['completed']]
    if not remaining:print('Requested Borel anchors already complete');return
    nr=len(progress['runs'])+1;log=HERE/f'phase5_j2_search_run{nr:03d}.log'
    command='BOREL_IDS:='+str(remaining)+';Read("research/leemans/phase5_j2_search.g");'
    start=time.monotonic();errors=[];finished=[]
    with log.open('w') as f:
        proc=subprocess.Popen([a.gap,'-q','-c',command],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in proc.stdout:
            f.write(line);f.flush()
            if 'Error,' in line:errors.append(line.strip())
            m=re.match(r'BOREL_COMPLETE id=(\d+)\b',line)
            if m:
                i=int(m[1]);checkpoint=HERE/f'phase5_j2_checkpoints/b{i}_done.g';assert checkpoint.exists()
                progress['completed'][str(i)]={'checkpoint':str(checkpoint.relative_to(HERE)),'sha256':sha(checkpoint),'run':nr}
                finished.append(i);save(PROGRESS,progress)
                print(line.strip(),flush=True)
            elif line.startswith(('INPUT','BOREL_BEGIN','SEARCH_COMPLETE')):print(line.strip(),flush=True)
        code=proc.wait()
    unchanged=sha(SCRIPT)==digest
    record={'number':nr,'borel_ids':remaining,'completed_ids':finished,'executed_script_sha256':digest,'log':log.name,'log_sha256':sha(log),'seconds':time.monotonic()-start,'exit_code':code,'errors':errors,'passed':code==0 and unchanged and not errors and finished==remaining and 'SEARCH_COMPLETE' in log.read_text()}
    progress['runs'].append(record);progress['all_146_borels_complete']=len(progress['completed'])==146;save(PROGRESS,progress)
    print('RUN_PASS' if record['passed'] else 'RUN_FAIL',round(record['seconds'],3),flush=True)
    if not record['passed']:raise SystemExit(1)
if __name__=='__main__':main()
