"""Compare every predecessor Git object with the literal candidate tree."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
from pathlib import Path
import argparse, hashlib, json, os, subprocess

p=argparse.ArgumentParser()
p.add_argument('--git-repo',type=Path,required=True)
p.add_argument('--candidate',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
base='16fd924ec3fd058225d209d8232dd4473cbc5361'
root=a.candidate.resolve()
allowed={'README.rst','audit/completion.rst','audit/corpus/latest.json',
         'papers/latest_catalogue.json','papers/catalogue_principal_refutations.json',
         'scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf'}
raw=subprocess.check_output(['git','-C',str(a.git_repo),'ls-tree','-rz',base])
rows=[];changed=[];symlinks=[];total=0
for entry in raw.split(b'\0'):
    if not entry:continue
    header,name=entry.split(b'\t',1);mode,kind,digest=header.split()
    if kind!=b'blob':raise RuntimeError('Unexpected nonblob tree object')
    name=name.decode();path=root/name
    if mode==b'120000':
        if not path.is_symlink():raise RuntimeError('Lost symbolic link '+name)
        data=os.readlink(path).encode();symlinks.append(name)
    else:
        if path.is_symlink() or not path.is_file():raise RuntimeError('Lost regular file '+name)
        data=path.read_bytes()
        if bool(path.stat().st_mode&0o111)!=(mode==b'100755'):
            raise RuntimeError('Changed executable mode '+name)
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    total+=len(data)
    if actual!=digest.decode():
        if name not in allowed:raise RuntimeError('Unrelated predecessor bytes changed '+name)
        changed.append(name)
        oldpath=root/'audit/principal-refutations/suzuki-subfields/v1/previous'/name
        oldbytes=oldpath.read_bytes()
        oldhash=hashlib.sha1(b'blob '+str(len(oldbytes)).encode()+b'\0'+oldbytes).hexdigest()
        if oldhash!=digest.decode():raise RuntimeError('Historical predecessor is not exact '+name)
    rows.append(dict(path=name,mode=mode.decode(),git_blob=digest.decode(),
                     candidate_blob=actual,bytes=len(data)))
if set(changed)!=allowed:raise RuntimeError('Unexpected set of changed predecessor files '+repr(changed))
report=dict(status='PASS_COMPLETE_PREDECESSOR_TREE_AUDIT',baseline=base,
            files=len(rows),bytes=total,symlinks=symlinks,changed=changed,
            unchanged=len(rows)-len(changed),rows=rows)
a.out.parent.mkdir(parents=True,exist_ok=True)
a.out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
