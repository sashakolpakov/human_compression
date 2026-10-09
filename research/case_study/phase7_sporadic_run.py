#!/usr/bin/env python3
"""Source-bound restartable RWPRI panel enumeration; never reads a geometry list."""
import argparse, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
SCRIPT = HERE / 'phase7_sporadic_search.g'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj):
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2) + '\n'); tmp.replace(p)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('group', choices=['M22','M23','HS','J3'])
    ap.add_argument('--gap', default=os.environ.get('GAP') or shutil.which('gap'))
    ap.add_argument('--require-2t', action='store_true', default=True)
    ap.add_argument('--borels', nargs='+', type=int)
    ap.add_argument('--resume', action='store_true')
    a = ap.parse_args()
    if not a.gap: ap.error('Set GAP or pass --gap')
    query = f'LoadPackage("tomlib");;Print("COUNT=",Length(OrdersTom(TableOfMarks("{a.group}"))),"\\n");QUIT;'
    out = subprocess.check_output([a.gap,'-q','-c',query],text=True)
    total = int(re.search(r'COUNT=(\d+)',out)[1])
    ids = sorted(set(a.borels or range(1,total+1)))
    if any(i<1 or i>total for i in ids): ap.error('Borel index outside catalogue')
    tag = a.group + ('_2T' if a.require_2t else '')
    stem = f'phase7_sporadic_{tag}'
    progress_path = HERE / (stem + '_progress.json')
    checkpoints = HERE / (stem + '_checkpoints'); checkpoints.mkdir(exist_ok=True)
    digest = sha(SCRIPT)
    if a.resume:
        progress = json.loads(progress_path.read_text())
        assert progress['executed_script_sha256'] == digest, 'Script changed'
        for rec in progress['completed'].values(): assert sha(HERE/rec['checkpoint']) == rec['sha256']
    else:
        if progress_path.exists(): ap.error('Existing run: use --resume or choose a fresh output group/mode')
        progress = dict(group=a.group, require_2t=a.require_2t, total_borels=total,
                        executed_script_sha256=digest, completed={}, runs=[])
    remaining = [i for i in ids if str(i) not in progress['completed']]
    if not remaining: print('Requested anchors already complete'); return
    nr = len(progress['runs']) + 1
    log = HERE / f'{stem}_run{nr:03d}.log'
    cmd = (f'GROUP_NAME:="{a.group}";REQUIRE_2T:={str(a.require_2t).lower()};'
           f'OUTPUT_DIR:="{checkpoints.name}";BOREL_IDS:={remaining};Read("{SCRIPT.name}");QUIT;')
    record = dict(number=nr, borel_ids=remaining, completed_ids=[], executed_script_sha256=digest,
                  log=log.name, status='running', passed=False)
    progress['runs'].append(record); save(progress_path,progress)
    start=time.monotonic(); errors=[]
    with log.open('w') as f:
        proc=subprocess.Popen([a.gap,'-q','-c',cmd],cwd=HERE,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,text=True,bufsize=1)
        try:
            for line in proc.stdout:
                f.write(line); f.flush()
                if 'Error,' in line: errors.append(line.strip())
                m=re.match(r'BOREL_COMPLETE id=(\d+)\b',line)
                if m:
                    i=int(m[1]); p=checkpoints/f'b{i}_done.g'
                    assert p.exists()
                    progress['completed'][str(i)]=dict(checkpoint=str(p.relative_to(HERE)),sha256=sha(p),run=nr)
                    record['completed_ids'].append(i); save(progress_path,progress)
                    print(line.strip(),flush=True)
                elif line.startswith(('INPUT','BOREL_BEGIN','SEARCH_COMPLETE')): print(line.strip(),flush=True)
            code=proc.wait()
        except BaseException:
            proc.terminate(); proc.wait()
            record.update(status='interrupted',log_sha256=sha(log),seconds=time.monotonic()-start)
            save(progress_path,progress); raise
    passed=code==0 and sha(SCRIPT)==digest and not errors and record['completed_ids']==remaining and 'SEARCH_COMPLETE' in log.read_text()
    record.update(status='complete',exit_code=code,errors=errors,log_sha256=sha(log),seconds=time.monotonic()-start,passed=passed)
    progress['all_borels_complete']=len(progress['completed'])==total
    save(progress_path,progress)
    print('RUN_PASS' if passed else 'RUN_FAIL',round(record['seconds'],3),flush=True)
    if not passed: raise SystemExit(1)
if __name__=='__main__': main()
