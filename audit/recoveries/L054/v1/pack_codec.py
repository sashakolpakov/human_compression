"""Exact content streams in bounded packs; never extracts arbitrary stored paths."""
import hashlib,zlib,shutil
from pathlib import Path,PurePosixPath
BLOCK=2**20
def need(ok,why):
 if not ok:raise ValueError(why)
def relative(name):
 need(isinstance(name,str),'string path');p=PurePosixPath(name);need(p.parts and str(p)==name and not p.is_absolute()and '..'not in p.parts and '.'not in p.parts,'literal safe relative path');return p
def resolve(name,roots):
 relative(name)
 for root in roots:
  root=Path(root).resolve();p=root/name
  if p.is_file():need(p.resolve().is_relative_to(root),'no escaping symlink');return p
 raise ValueError('missing stored path '+name)
def digest_file(p):
 h=hashlib.sha256();n=0
 with Path(p).open('rb')as f:
  for b in iter(lambda:f.read(BLOCK),b''):h.update(b);n+=len(b)
 return n,h.hexdigest()
class Writer:
 def __init__(self,root,prefix,limit=48*2**20,reserve=8*2**30):
  self.root=Path(root);self.prefix=str(relative(prefix));self.limit=limit;self.reserve=reserve;need(limit>0,'positive pack limit')
  (self.root/self.prefix).mkdir(parents=True,exist_ok=True);self.parts=[];self.file=None;self.used=0;self.number=0
 def close_part(self):
  if self.file is not None:
   self.file.close();self.parts.append(dict(path=self.name,bytes=self.used,sha256=self.hash.hexdigest()));self.file=None
 def write(self,data,segments):
  while data:
   if self.file is None:
    self.number+=1;self.name=self.prefix+'/part-%04d.bin'%self.number;p=self.root/self.name;need(not p.exists(),'fresh pack');self.file=p.open('xb');self.used=0;self.hash=hashlib.sha256()
   n=min(len(data),self.limit-self.used);need(shutil.disk_usage(self.root).free>=self.reserve+n,'8-GiB storage reserve')
   b=data[:n];self.file.write(b);self.hash.update(b)
   if segments and segments[-1]['path']==self.name and segments[-1]['offset']+segments[-1]['bytes']==self.used:segments[-1]['bytes']+=n
   else:segments.append(dict(path=self.name,offset=self.used,bytes=n))
   self.used+=n;data=data[n:]
   if self.used==self.limit:self.close_part()
 def add(self,path,expected,encoding):
  need(encoding in ['identity','gzip'],'exact encoding');h=hashlib.sha256();stored=hashlib.sha256();raw=encoded=0;segments=[];c=zlib.compressobj(level=6,wbits=31)if encoding=='gzip'else None
  def emit(b):
   nonlocal encoded
   stored.update(b);encoded+=len(b);self.write(b,segments)
  with Path(path).open('rb')as f:
   for b in iter(lambda:f.read(BLOCK),b''):
    h.update(b);raw+=len(b);emit(c.compress(b)if c else b)
  if c:emit(c.flush())
  need((raw,h.hexdigest())==(expected['bytes'],expected['sha256']),'unchanged exact input')
  return dict(bytes=raw,sha256=h.hexdigest(),encoding=encoding,stored_bytes=encoded,stored_sha256=stored.hexdigest(),segments=segments)
 def finish(self):self.close_part();return self.parts
def decoded(record,roots):
 """Yield bounded decoded blocks and validate the complete encoded stream."""
 need(record['encoding']in ['identity','gzip'],'known encoding');need(type(record['bytes'])is int and record['bytes']>=0 and type(record['stored_bytes'])is int and record['stored_bytes']>=0,'nonnegative exact lengths')
 total=raw=0;encoded_hash=hashlib.sha256();raw_hash=hashlib.sha256();dec=zlib.decompressobj(wbits=31)if record['encoding']=='gzip'else None
 for seg in record['segments']:
  need(type(seg['offset'])is int and seg['offset']>=0 and type(seg['bytes'])is int and seg['bytes']>0,'exact segment range')
  p=resolve(seg['path'],roots);need(seg['offset']+seg['bytes']<=p.stat().st_size,'segment within stored file')
  with p.open('rb')as f:
   f.seek(seg['offset']);left=seg['bytes']
   while left:
    b=f.read(min(BLOCK,left));need(b,'complete segment');left-=len(b);total+=len(b);encoded_hash.update(b)
    need(total<=record['stored_bytes'],'no extra stored bytes')
    if dec:
     while b:
      out=dec.decompress(b,BLOCK);b=dec.unconsumed_tail;need(not dec.unused_data,'single exact gzip stream')
      if out:raw+=len(out);need(raw<=record['bytes'],'bounded decoded length');raw_hash.update(out);yield out
    else:
     raw+=len(b);need(raw<=record['bytes'],'bounded decoded length');raw_hash.update(b);yield b
 if dec:
  need(dec.eof and not dec.unused_data and not dec.unconsumed_tail,'complete single gzip stream')
  out=dec.flush();raw+=len(out);need(raw<=record['bytes'],'bounded final length');raw_hash.update(out)
  if out:yield out
 need((total,encoded_hash.hexdigest())==(record['stored_bytes'],record['stored_sha256']),'complete stored identity')
 need((raw,raw_hash.hexdigest())==(record['bytes'],record['sha256']),'complete decoded identity')
def verify(record,roots):
 for _ in decoded(record,roots):pass
def materialize(record,roots,out):
 out=Path(out);need(not out.exists(),'fresh selected input');out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('xb')as f:
  for b in decoded(record,roots):f.write(b)
