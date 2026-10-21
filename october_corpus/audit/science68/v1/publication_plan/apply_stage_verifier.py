"""Exercise the proposed verifier edit only in a marked private stage."""
from pathlib import Path
import argparse,ast,hashlib,json
HERE=Path(__file__).resolve().parent
def hashes(s):return {n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
def main(a):
 stage=a.stage.resolve()
 if stage==Path('/Users/sasha/medusa/math_compression') or not(stage/'science68_stage_report.json').is_file():raise ValueError('private marked stage required')
 p=stage/'scripts/verify_snapshot.py';s=p.read_text();base=json.loads((HERE/'baseline.json').read_text())['old_nonmain_ASTs']
 if hashes(s)!=base:raise ValueError('exact old function baseline required')
 before,mark,tail=s.partition('def main():')
 if not mark:raise ValueError('main boundary')
 t=before+(HERE/'snapshot_additions.py').read_text()+'\n'+mark+tail.replace('science67','science68')
 now=hashes(t)
 if any(now.get(k)!=v for k,v in base.items()) or set(now)-set(base)!={'check_previous_science68','check_science68'}:raise ValueError('nonmain preservation')
 if p.is_symlink():p.unlink()
 p.write_text(t)
 report=dict(status='PASS_PRIVATE_ADDITIVE_VERIFIER_AST_EDIT',old_nonmain_preserved=len(base),new_nonmain=len(now),added=['check_previous_science68','check_science68'],main_current_route=68,public_repo_written=False)
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',required=True,type=Path);p.add_argument('--out',required=True,type=Path);main(p.parse_args())
