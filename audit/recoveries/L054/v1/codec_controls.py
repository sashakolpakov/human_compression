"""Tiny exact pack-stream controls; no scientific input or repository copy."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,copy,gzip,zlib
import pack_codec as c
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();c.need(not a.out.exists(),'fresh controls');a.out.mkdir(parents=True)
 w=c.Writer(a.out,'packs',limit=73,reserve=0);records=[]
 data=[b'',b'a',b'a'*10000,bytes(range(256))*11,b'x'*73,b'z'*74,b'one\n'*500]
 for i,b in enumerate(data):
  p=a.out/('input%d'%i);p.write_bytes(b);expected=dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  for encoding in ['identity','gzip']:records.append(w.add(p,expected,encoding))
 parts=w.finish()
 for r in parts:c.need(c.digest_file(a.out/r['path'])==(r['bytes'],r['sha256']),'exact whole pack hash');c.need(r['bytes']<=73,'bounded pack')
 for i,r in enumerate(records):c.verify(r,[a.out]);c.need(b''.join(c.decoded(r,[a.out]))==data[i//2],'exact original stream')
 base=copy.deepcopy(records[6]);c.need(len(base['segments'])>1,'actual crossing fixture');bad=[]
 for key,val in [('sha256','0'*64),('bytes',base['bytes']-1),('stored_sha256','0'*64),('stored_bytes',base['stored_bytes']+1),('encoding','deflate')]:
  z=copy.deepcopy(base);z[key]=val;bad.append(z)
 for change in ['missing','repeat','offset','range','order','escape']:
  z=copy.deepcopy(base)
  if change=='missing':z['segments'].pop()
  if change=='repeat':z['segments'].append(copy.deepcopy(z['segments'][0]))
  if change=='offset':z['segments'][0]['offset']+=1
  if change=='range':z['segments'][0]['bytes']+=100000
  if change=='order':z['segments'].reverse()
  if change=='escape':z['segments'][0]['path']='../escape'
  bad.append(z)
 for z in bad:
  try:c.verify(z,[a.out])
  except (ValueError,zlib.error):pass
  else:raise ValueError('damaged pack record accepted')
 # Actual concatenated gzip, valid individual member hashes, is still outside
 # the one-stream interface. The exact stored digest alone cannot admit it.
 b=gzip.compress(b'one',mtime=0)+gzip.compress(b'two',mtime=0);p=a.out/'concatenated.gz';p.write_bytes(b)
 z=dict(encoding='gzip',bytes=6,sha256=hashlib.sha256(b'onetwo').hexdigest(),stored_bytes=len(b),stored_sha256=hashlib.sha256(b).hexdigest(),segments=[dict(path=p.name,offset=0,bytes=len(b))])
 try:c.verify(z,[a.out])
 except ValueError:pass
 else:raise ValueError('concatenated stream accepted')
 # Physical stored corruption is caught even though all descriptor lengths
 # and paths remain valid; restore the fixture after this single check.
 part=a.out/base['segments'][0]['path'];raw=part.read_bytes();mut=bytearray(raw);mut[base['segments'][0]['offset']]^=1;part.write_bytes(mut)
 try:c.verify(base,[a.out])
 except ValueError:pass
 else:raise ValueError('physical corruption accepted')
 part.write_bytes(raw)
 for name in ['', '.', '..', '/absolute', 'a/../b','a//b','a/./b']:
  try:c.relative(name)
  except ValueError:pass
  else:raise ValueError('unsafe path accepted')
 c.materialize(records[5],[a.out],a.out/'selected/exact.bin');c.need((a.out/'selected/exact.bin').read_bytes()==data[2],'small selective extraction')
 # A highly compressed stream spanning more than three decoded blocks tests
 # the actual bounded zlib output loop, without creating thousands of tiny packs.
 big=b'q'*(3*c.BLOCK+7);bigpath=a.out/'large_input';bigpath.write_bytes(big)
 large=c.Writer(a.out,'large_packs',limit=c.BLOCK,reserve=0);lr=large.add(bigpath,dict(bytes=len(big),sha256=hashlib.sha256(big).hexdigest()),'gzip');large.finish()
 chunks=list(c.decoded(lr,[a.out]));c.need(b''.join(chunks)==big and max(map(len,chunks))<=c.BLOCK,'bounded high-expansion stream')
 (a.out/'outside_link').symlink_to('/etc/hosts')
 try:c.resolve('outside_link',[a.out])
 except ValueError:pass
 else:raise ValueError('escaping physical symlink accepted')
 report=dict(status='PASS_EXACT_SEGMENTED_GZIP_STORAGE_CONTROLS',positive_streams=len(records),small_pack_files=len(parts),record_damages=len(bad),physical_corruptions=1,concatenated_stream_rejections=1,path_rejections=7,physical_symlink_rejections=1,large_decoded_bytes=len(big),bounded_decoded_chunks=len(chunks),scientific_calls=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
