"""UNRUN relative proof-packet integrity verifier; no scientific Source import.
Original absolute paths are opaque keys. Every active read stays in corpus.
Author /root/compact_proof_author.
"""
import argparse,base64,gzip,hashlib,json,math,os,resource,stat,sys,time
from pathlib import Path,PurePosixPath
START=time.monotonic();TOTAL=0;MIB=2**20

def need(ok,why):
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 if not ok:raise ValueError(why)
 if rss>=256*MIB or time.monotonic()-START>=240:raise RuntimeError('256MiB240s integrity bound')

def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()

def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'unique JSON keys');out[k]=v
  return out
 def finite(s):
  x=float(s);need(math.isfinite(x),'finite JSON');return x
 return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:(_ for _ in()).throw(ValueError('finite JSON')))

def relative(text):
 need(type(text)is str and text and text.isascii(),'literal relative ASCII reference')
 p=PurePosixPath(text);need(not p.is_absolute()and str(p)==text and not set(p.parts)&{'.','..','.git','__pycache__','.lake'},
  'relative declared corpus path only; no private fallback')
 return Path(*p.parts)

def shape(r):
 need(type(r)is dict and set(r)=={'path','bytes','sha256'}and type(r['path'])is str
  and type(r['bytes'])is int and 0<=r['bytes']<=32*MIB and type(r['sha256'])is str
  and len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef'),'complete bounded content descriptor')

def read(root,r,body=False):
 global TOTAL
 shape(r);p=root/relative(r['path']);a=p.lstat()
 need(p.resolve(strict=True)==p and p.is_relative_to(root)and stat.S_ISREG(a.st_mode)and a.st_nlink==1
  and a.st_size==r['bytes'],'canonical ordinary relative payload')
 need(not body or r['bytes']<=8*MIB,'bounded JSON/bank input before allocation')
 need(TOTAL+r['bytes']<=64*MIB,'64MiB cumulative integrity read budget')
 h=hashlib.sha256();parts=[]if body else None;count=0
 sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 with p.open('rb')as f:
  b=os.fstat(f.fileno())
  while True:
   chunk=f.read(MIB)
   if not chunk:break
   count+=len(chunk);need(count<=r['bytes'],'whole declared extent');h.update(chunk)
   if parts is not None:parts.append(chunk)
  c=os.fstat(f.fileno())
 need(sig(a)==sig(b)==sig(c)==sig(p.lstat())and count==r['bytes']and h.hexdigest()==r['sha256'],
  'fresh entire relative file and stable identity')
 TOTAL+=count;return b''.join(parts)if body else None

def main():
 global TOTAL
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--corpus-root',required=True)
 ap.add_argument('--manifest',required=True);ap.add_argument('--manifest-sha256',required=True)
 ap.add_argument('--self-sha256',required=True);a=ap.parse_args()
 root=Path(a.corpus_root);need(root.is_absolute()and root.resolve(strict=True)==root,'explicit canonical corpus root')
 own=Path(__file__).resolve(strict=True);need(own.is_relative_to(root),'relative verifier Source')
 ownref=dict(path=str(own.relative_to(root)),bytes=own.stat().st_size,sha256=a.self_sha256)
 need(ownref['bytes']<=16384,'bounded verifier Source')
 TOTAL+=ownref['bytes'];read(root,ownref)
 mp=root/relative(a.manifest);mr=dict(path=a.manifest,bytes=mp.stat().st_size,sha256=a.manifest_sha256)
 manifest=decode(read(root,mr,True));need(manifest['schema']=='CURATED_PORTABLE_PROOF_PACKET_MANIFEST_V1',
  'one exact modern proof packet, not a historical caller verdict')
 files=manifest['files'];need(type(files)is list and len(files)<=4096,'finite complete file manifest')
 by={};total=0
 for row in files:
  r={k:row[k]for k in('path','bytes','sha256')};need(r['path']not in by,'one relative payload identity');by[r['path']]=r
  total+=r['bytes']
 need(total<=512*MIB,'512MiB finite packet payload')
 original={}
 for row in manifest['original_to_relative']:
  r=row['original'];shape(r);relpath=row['relative'];need(relpath in by,'every original maps to included content')
  key=(r['path'],r['bytes'],r['sha256'])
  need(by[relpath]['bytes']==r['bytes']and by[relpath]['sha256']==r['sha256'],
   'whole original identity, never a path-only alias')
  original[key]=r
 packed={};banks_checked=0
 for bank in manifest['proof_banks']:
  need(bank['path']in by and bank['maximum_expanded_bytes']<=8*MIB,'explicit bounded preserved evidence bank')
  packedraw=read(root,by[bank['path']],True)
  import io
  with gzip.GzipFile(fileobj=io.BytesIO(packedraw))as stream:
   raw=stream.read(bank['maximum_expanded_bytes']+1)
   need(len(raw)<=bank['maximum_expanded_bytes']and stream.read(1)==b'','whole bounded gzip evidence')
  value=decode(raw);need(value['schema']==bank['schema'],'exact archived bank kind')
  docs=value[bank['documents_field']];need(len(docs)==bank['documents'],'whole declared bank membership')
  for index,row in enumerate(docs):
   r=row[bank['reference_field']];shape(r);need(r['bytes']<=2*MIB,'bounded one whole archived body')
   data=base64.b64decode(row[bank['base64_field']],validate=True)
   need(len(data)==r['bytes']and hashlib.sha256(data).hexdigest()==r['sha256'],'entire archived mathematical/source/guard body')
   key=(bank['path'],index);need(key not in packed,'one exact packed location');packed[key]=r
  banks_checked+=1
  del value,docs,raw,packedraw
 selected=set()
 for row in manifest['packed_members']:
  r=row['original'];shape(r)
  key=(row['bank'],row['index']);need(key not in selected,'unique explicit packed mapping');selected.add(key)
  need(packed.get(key)==r,
   'explicit original-to-relative packed location, no missing private path duty')
  original[(r['path'],r['bytes'],r['sha256'])]=r
 need(selected==set(packed),'all archived bodies mapped without clipping')
 # Full current non-bank files are whole-hashed once here; each bank was
 # additionally authenticated before its complete bounded body validation.
 for r in by.values():read(root,r)
 read(root,mr);read(root,ownref)
 print(json.dumps(dict(schema='PORTABLE_PACKET_INTEGRITY_RESULT_V1',status='PASS_FILE_AND_ARCHIVED_BODY_INTEGRITY',packet=manifest['packet'],
  manifest=mr,files=len(by),payload_bytes=total,original_identities=len(original),proof_banks=banks_checked,packed_bodies=len(packed),
  physical_read_bytes=TOTAL,private_original_paths_opened=0,scientific_or_Source_calls=0,
  scientific_replay_status=manifest['scientific_replay_status'],whole_original_credit=0,conjecture_credit=0,Lean_credit=0,compression_credit=0,
  qualification='Whole file/body identity and complete relative mapping only. This is not matrix/point/action/group/Reader or theorem verification; use the separately reviewed mathematical replay boundary.'),sort_keys=True))

if __name__=='__main__':main()
