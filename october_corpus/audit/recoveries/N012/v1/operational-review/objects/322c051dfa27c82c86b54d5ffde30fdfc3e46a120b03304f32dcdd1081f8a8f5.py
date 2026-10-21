"""Private N012 transport inventory; no source admission or public edits."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError('No optimization')
S=Path(__file__).resolve().parents[1]
R=S.parents[1]/'math_compression'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main(a):
    need(not a.out.exists(),'Fresh inventory required')
    author=S/'corpus106_N012_principal_v1'
    d=json.loads((author/'dependencies.json').read_text())
    omissions=set(d['primary_files_hash_only'])|{
      'reboot_20261013/N012_central_quotients_distinct/source_pages/page-69.png',
      'reboot_20261013/N012_central_quotients_distinct/source_pages/page-72.png'}
    files={};packets={};missing=[]
    def add(p,expected=None,role='explicit bound evidence'):
        p=p.resolve();need(p.is_relative_to(S),'Outside study evidence');need(p.is_file(),'Missing '+str(p))
        rel=str(p.relative_to(S));v=dict(origin='study',path=rel,bytes=p.stat().st_size,sha256=sha(p),role=role)
        if expected:need(v['sha256']==expected['sha256'] and v['bytes']==expected.get('bytes',v['bytes']),'Changed '+rel)
        if rel in files:need(files[rel]['sha256']==v['sha256'],'Conflicting pin');return
        files[rel]=v
    def packet(name):
        p=S/name/'manifest.json';add(p,role='complete edition manifest');m=json.loads(p.read_text())
        packets[str(p.relative_to(S))]=dict(origin='study',path=str(p.relative_to(S)),sha256=sha(p),exports=len(m['exports']))
        for row in m['exports']:
            q=p.parent/row['path'];need(q.resolve().is_relative_to(p.parent),'Export escape');add(q,row,'complete edition export')
    packet('corpus106_N012_principal_v1')
    for row in d['bindings']:add(S/row['path'],row)
    for name in d['acquired_packets']:packet(str(Path(name).parent))
    for name in ['corpus106_N012_principal_root_review']:
        if not (S/name/'manifest.json').is_file():missing.append(name);continue
        packet(name)
        dp=S/name/'dependencies.json'
        if dp.is_file():
            for row in json.loads(dp.read_text()).get('bindings',[]):add(S/row['path'],row)
    needed={(x['bytes'],x['sha256']) for x in files.values() if x['path']not in omissions}
    existing={}
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
    # Prior transport files give exact raw identities even for compressed public logs.
    for rel in tracked:
        if not rel.endswith('/transport.json'):continue
        try:tr=json.loads((R/rel).read_text())
        except (ValueError,OSError):continue
        for row in tr.get('files',[]):
            if all(k in row for k in ['bytes','sha256','public_path','encoding','stored_bytes','stored_sha256']):
                key=(row['bytes'],row['sha256'])
                if key in needed:existing.setdefault(key,{k:row[k]for k in ['public_path','encoding','stored_bytes','stored_sha256']})
    sizes={n for n,h in needed}
    # This also finds the directly published N011 papers and review records.
    for rel in tracked:
        if not rel:continue
        p=R/rel
        if not p.is_file() or p.stat().st_size not in sizes:continue
        key=(p.stat().st_size,sha(p))
        if key in needed:existing.setdefault(key,dict(public_path=rel,encoding='identity',stored_bytes=key[0],stored_sha256=key[1]))
    rows=[]
    for row in sorted(files.values(),key=lambda x:x['path']):
        key=(row['bytes'],row['sha256'])
        if row['path'] in omissions:row['transport']='PRIVATE_PRIMARY_SOURCE_HASH_ONLY'
        elif key in existing:
            x=existing[key];p=(R/x['public_path']).resolve();need(p.is_relative_to(R.resolve()),'Public escape')
            need(p.stat().st_size==x['stored_bytes'] and sha(p)==x['stored_sha256'],'Public pin changed')
            row.update(transport='EXISTING_PUBLIC',**x)
        else:row['transport']='NEW_FROZEN_FILE'
        if row['path'].endswith('.md'):
            need(row['path']=='phase22_linear_priority_supplement.md','Unexpected working Markdown')
            row['public_suffix_override']='.txt'
            row['logical_markdown_provenance_only']=True
        rows.append(row)
    need(omissions<={r['path']for r in rows},'Every primary omission must have an exact record')
    report=dict(status='PRIVATE_TRANSPORT_PLAN_NOT_ADMISSION',files=rows,packets=list(packets.values()),
      logical_files=len(rows),missing_final_reviews=missing,primary_sources_hash_only=sorted(omissions),
      primary_omission_addendum='Two source-page screenshots are explicitly added to the frozen author list; all frozen bytes remain unchanged.',
      markdown_transport='One historical provenance .md is stored byte-exact with a .txt public suffix and restored only under its historical local name.',
      existing_public_logical_files=sum(x['transport']=='EXISTING_PUBLIC'for x in rows),
      new_logical_files=sum(x['transport']=='NEW_FROZEN_FILE'for x in rows),
      new_uncompressed_bytes=sum(x['bytes']for x in rows if x['transport']=='NEW_FROZEN_FILE'),
      source_assets_exported=False,private_runtime_fallback=False,whole_original_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ['files','packets','primary_sources_hash_only']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);main(p.parse_args())
