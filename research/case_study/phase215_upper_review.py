#!/usr/bin/env python3
"""Independent audit runs and controls for the literal coset-deduction verifier."""
import argparse,gzip,hashlib,json,subprocess,time
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def execute(cmd,out,name,expected):
    start=time.monotonic()
    r=subprocess.run(cmd,text=True,capture_output=True,timeout=120)
    (out/(name+'.stdout')).write_text(r.stdout);(out/(name+'.stderr')).write_text(r.stderr)
    require((r.returncode==0)==expected,name+' wrong outcome')
    return dict(name=name,command=cmd,exit_code=r.returncode,seconds=time.monotonic()-start,
        stdout_sha256=sha(out/(name+'.stdout')),stderr_sha256=sha(out/(name+'.stderr')),
        output_tail=(r.stdout+r.stderr).strip().splitlines()[-4:])
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    a=ap.parse_args();require(not a.output_dir.exists() and not a.output_dir.is_symlink(),'Fresh directory required');out=a.output_dir.resolve();require(not out.exists(),'Fresh directory required');out.mkdir()
    src=Path(__file__).with_name('phase214_table_deduction.cpp').resolve()
    frozen=out/'author_checker.cpp';frozen.write_bytes(src.read_bytes());exe=out/'checker'
    runs=[execute(['clang++','-std=c++17','-O2','-Wall','-Wextra',str(frozen),'-o',str(exe)],out,'compile',True)]
    metadata=json.loads(src.with_name('phase214_tables.json').read_text())
    tables=[]
    for item in metadata['tables']:
        d=item['rank'];packed=src.parent.joinpath(item['path']).read_bytes()
        require(hashlib.sha256(packed).hexdigest()==item['gzip_sha256'],'Packed certificate hash')
        raw=gzip.decompress(packed);p=out/f'table{d}.txt';p.write_bytes(raw)
        require(sha(p)==item['raw_sha256'] and len(raw)==item['raw_bytes'],'Raw certificate binding')
        tables.append(dict(rank=d,path=str(p),sha256=sha(p),bytes=p.stat().st_size))
        runs.append(execute([str(exe),str(p)],out,f'rank{d}',True))
        require('COMPLETE index_upper_bound=' in (out/f'rank{d}.stdout').read_text(),'Missing completion')
    # This is a genuine permutation action of the group satisfying every
    # relator and every subgroup loop, but it is not an upper-bound derivation.
    one=out/'one_coset_quotient.txt';one.write_text('1 3\n1 1 1\n')
    runs.append(execute([str(exe),str(one)],out,'one_coset_quotient_control',False))
    require('INCOMPLETE' in (out/'one_coset_quotient_control.stdout').read_text(),'Wrong one-coset rejection')
    # A valid table with its labels permuted must still permit the proof.
    raw=(out/'table3.txt').read_text().split()
    N,d=map(int,raw[:2]);rows=[list(map(int,raw[2+i*d:2+(i+1)*d])) for i in range(N)]
    perm=[0]+[1]+list(range(N,1,-1));renamed=[None]*N
    for u in range(1,N+1):renamed[perm[u]-1]=[perm[v] for v in rows[u-1]]
    good=out/'relabelled_rank3.txt';good.write_text(f'{N} {d}\n'+'\n'.join(' '.join(map(str,row)) for row in renamed)+'\n')
    runs.append(execute([str(exe),str(good)],out,'relabelled_rank3',True))
    # An in-range edge corruption is not silently installed from the oracle.
    badrows=[r[:] for r in rows];badrows[0][-1]=N if rows[0][-1]!=N else N-1
    bad=out/'corrupt_edge.txt';bad.write_text(f'{N} {d}\n'+'\n'.join(' '.join(map(str,row)) for row in badrows)+'\n')
    runs.append(execute([str(exe),str(bad)],out,'corrupt_edge_control',False))
    # A strictly weaker, infinite Coxeter presentation cannot be proved finite
    # by importing the supplied table's unknown transitions.
    weaker=out/'without_triple_relators.cpp'
    s=frozen.read_text();anchor='k=1;k<11;++k'
    require(s.count(anchor)==1,'Changed source anchor')
    weaker.write_text(s.replace(anchor,'k=1;k<1;++k'))
    weakexe=out/'weaker_checker'
    runs.append(execute(['clang++','-std=c++17','-O2',str(weaker),'-o',str(weakexe)],out,'compile_weaker',True))
    runs.append(execute([str(weakexe),str(out/'table3.txt')],out,'omitted_triple_relators_control',False))
    require('INCOMPLETE' in (out/'omitted_triple_relators_control.stdout').read_text(),'Wrong weakened-presentation rejection')
    report=dict(status='PASS',author_source_sha256=sha(frozen),tables=tables,runs=runs,
      checker_mathematical_invariant='Every known edge represents a proved equality of actual right H-cosets. Only tree definitions, inverse edges, original subgroup loops and one-gap literal relator deductions install edges.',
      assumptions_not_used=['distinctness of table labels','ACE correctness','unknown oracle transitions','unproved coincidences'],
      scope='Index upper-bound certificates only; matrix lower bounds and full conjecture obstruction are separate obligations.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',runs=len(runs))))
if __name__=='__main__':main()
