"""Preserve stage01, add seven author installation aliases, reuse pack inodes.

No scientific bytes or premise boundary changes.  New metadata and readable
copies have fresh paths; the twelve immutable exact pack files are hard-linked.
"""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import json,os,shutil,time
import stage as b
P=Path(__file__).resolve().parent;old=P/'stage01';new=P/'stage02';prefix=b.PREFIX
def main():
 start=time.monotonic();b.need(not new.exists(),'fresh revision stage')
 d=old/prefix;m=b.load(d/'manifest.json');t=b.load(d/'transport.json')
 b.need(b.pin(d/'manifest.json')['sha256']=='8383a4342214b8f31e6e584178d41b6476e6a31c8a7420802efdf51d4bd53a5d','exact failed stage01')
 b.need(b.pin(d/'transport.json')['sha256']=='2189ec1524eac0d9c69a94235f71bf75b3aecf0ea213b18cfc01daf5f5ab7020','exact failed transport01')
 b.need(shutil.disk_usage(P).free>=b.RESERVE+100*2**20,'same reserve plus metadata allowance')
 for r in m['exports']:b.exact(old/r['path'],r)
 originals={r['original_path']:r for r in t['logical_files']};aliases=[]
 for r in b.load(b.H/'principal_synthesis_v1/dependencies.json'):
  if r['path'] in originals:continue
  canonical=str(Path(r['path']).resolve());q=originals[canonical]
  q={k:q[k] for k in ['bytes','sha256']};q['path']=canonical
  b.need((q['bytes'],q['sha256'])==(r['bytes'],r['sha256']),'same already bound canonical bytes')
  b.need(canonical.startswith('/opt/homebrew/Cellar/') and t['objects'][r['sha256']]['kind'] in ['INSTALLED_SOFTWARE_ENVIRONMENT_PREMISE','EXISTING_PUBLIC'],'already carried installation alias only')
  aliases.append(dict(alias=r,canonical=q))
  o,n=b.origin(r['path']);t['logical_files'].append(dict(origin=o,path=n,original_path=r['path'],bytes=r['bytes'],sha256=r['sha256']))
 b.need(len(aliases)==7,'exact seven missing author environment aliases');t['environment_aliases']=aliases
 new.mkdir();D=new/prefix;D.mkdir(parents=True)
 changed={prefix+'/'+n for n in ['transport.json','portable_check.py','portable_controls.py','roles.json']}
 packs={r['path'] for r in t['packs']}
 for r in m['exports']:
  n=r['path']
  if n in changed:continue
  dest=new/n;dest.parent.mkdir(parents=True,exist_ok=True)
  if n in packs:os.link(old/n,dest)
  else:b.copy_exact(old/n,dest)
 b.write_json(D/'transport.json',t,compact=True)
 for name in ['portable_check.py','portable_controls.py']:b.copy_exact(P/name,D/name)
 roles=b.load(d/'roles.json');roles['environment_alias_revision']='Seven literal author installation paths map to the identical canonical contents already in the accepted root closure. No new payload content or premise.'
 roles['stage01_preserved']=b.pin(d/'manifest.json');roles['packs']='The twelve immutable packs share exact read-only bytes with preserved stage01; no second codec run.'
 b.write_json(D/'roles.json',roles)
 exports=[]
 for f in sorted(new.rglob('*')):
  if f.is_file():r=b.pin(f);r['path']=str(f.relative_to(new));exports.append(r)
 b.write_json(D/'manifest.json',dict(status=m['status'],exports=exports,root_acceptance=t['root_acceptance'],new_scientific_targets=0))
 result=dict(status='STAGED_EXACT_L091_WITH_LITERAL_ENVIRONMENT_ALIASES',prior_stage=b.pin(d/'manifest.json'),manifest=b.pin(D/'manifest.json'),transport=b.pin(D/'transport.json'),
  logical_files=len(t['logical_files']),unique_objects=len(t['objects']),environment_aliases=aliases,new_pack_files=len(packs),new_pack_bytes=sum(r['bytes'] for r in t['packs']),
  new_stage_bytes=sum(r['bytes'] for r in exports)+(D/'manifest.json').stat().st_size,actual_pack_bytes_added=0,seconds=time.monotonic()-start)
 (P/'stage02_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
