"""Find exact content in committed immutable public paths, including segmented packs."""
from pathlib import Path
import json,subprocess
import pack_codec as codec

def index(repo,wanted):
    names=set(subprocess.run(['git','-C',str(repo),'ls-tree','-rz','--name-only','HEAD'],capture_output=True,check=True).stdout.decode().split('\0'))
    result={};files={};sources=[]
    def add(digest,record,bindings):
        if digest not in wanted or digest in result:return
        if record['bytes']!=wanted[digest]['bytes']:raise ValueError('same raw hash, different length')
        if any(s['path']not in names for s in record['segments']):return
        for seg in record['segments']:
            if seg['path']not in bindings:return
        result[digest]=dict(record,kind='EXISTING_PUBLIC')
        for seg in record['segments']:files[seg['path']]=bindings[seg['path']]
    # Read only committed transport indexes; actual content is independently hashed later.
    for name in sorted(names):
        if not name.endswith('/transport.json'):continue
        path=repo/name
        if not path.is_file():continue
        try:t=json.loads(path.read_text())
        except (ValueError,UnicodeError):continue
        if not isinstance(t,dict):continue
        if isinstance(t.get('objects'),dict):
            bindings={r['path']:r for r in t.get('packs',[])+t.get('existing_public_files',[])}
            for h,r in t['objects'].items():
                if r.get('kind')in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']:add(h,r,bindings)
        if isinstance(t.get('files'),list):
            for r in t['files']:
                if not isinstance(r,dict)or not all(k in r for k in ['bytes','sha256','public_path','stored_bytes','stored_sha256']):continue
                n=r['public_path'];rec=dict(bytes=r['bytes'],sha256=r['sha256'],encoding=r.get('encoding','identity'),stored_bytes=r['stored_bytes'],stored_sha256=r['stored_sha256'],segments=[dict(path=n,offset=0,bytes=r['stored_bytes'])]if r['stored_bytes']else[])
                add(r['sha256'],rec,{n:dict(path=n,bytes=r['stored_bytes'],sha256=r['stored_sha256'])})
        sources.append(name)
    # Direct immutable historical inputs can also be reused byte-for-byte.
    for h,r in wanted.items():
        if h in result:continue
        p=Path(r['path'])
        if p.is_relative_to(repo):
            n=str(p.relative_to(repo))
            if n in names and n.startswith(('audit/','papers/')):
                add(h,dict(bytes=r['bytes'],sha256=h,encoding='identity',stored_bytes=r['bytes'],stored_sha256=h,segments=[dict(path=n,offset=0,bytes=r['bytes'])]if r['bytes']else[]),{n:dict(path=n,bytes=r['bytes'],sha256=h)})
    return result,files,sources
