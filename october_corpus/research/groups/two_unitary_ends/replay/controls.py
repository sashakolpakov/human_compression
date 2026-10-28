"""UNRUN controls for the NEW relative two-end replay Source.
Generic GL7 arithmetic is not a G2 marking. Temporary ordinary fixture files
exercise only the explicit relative IO mapper, with no original model calls.
Author /root/compact_proof_author.
"""
import time
START=time.monotonic()
import argparse,hashlib,itertools,json,os,resource,sys,tempfile
from pathlib import Path
def need(ok,why):
 if not ok:raise ValueError(why)

class ArithmeticBudget:
 def __init__(self):self.products=0
 def tick(self,soft=False):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(rss<128*2**20 and time.monotonic()-START<100,'synthetic128MiB100s')
 def multiply(self,A,B):
  self.tick();self.products+=1;need(self.products<=50000,'synthetic50000products')
  return tuple(tuple(sum(A[i][k]*B[k][j]for k in range(len(B)))%11 for j in range(len(B[0])))for i in range(len(A)))

def quotient_fixture(kernel,budget):
 # Only +/* in F11[X]/(X^6+aX+b). No irreducibility assertion is needed:
 # the final literal GL7 matrices must themselves pass exact order37.
 one=(1,0,0,0,0,0);x=(0,1,0,0,0,0)
 for a in range(11):
  for b in range(1,11):
   def mul(u,v):
    budget.tick(True);out=[0]*11
    for i in range(6):
     for j in range(6):out[i+j]=(out[i+j]+u[i]*v[j])%11
    for k in range(10,5,-1):
     c=out[k];out[k-6]=(out[k-6]-b*c)%11;out[k-5]=(out[k-5]-a*c)%11
    return tuple(out[:6])
   z=one
   for bit in bin(47880)[2:]:
    z=mul(z,z)
    if bit=='1':z=mul(z,x)
   M=[mul(tuple(int(i==j)for i in range(6)),z)for j in range(6)]
   Y=((1,0,0,0,0,0,0),)+tuple((0,)+row for row in M)
   I=tuple(tuple(int(i==j)for j in range(7))for i in range(7))
   if Y!=I and kernel['power'](Y,37,budget)==I:return Y
 raise ValueError('bounded arithmetic fixture construction found no exact37 matrix')

def refused(call,why):
 try:call()
 except (ValueError,KeyError,TypeError,IndexError):return
 raise ValueError('negative synthetic control accepted: '+why)

def main():
 parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--consumer',nargs=2,required=True)
 parser.add_argument('--self-sha256',required=True);args=parser.parse_args();budget=ArithmeticBudget()
 own=Path(__file__).resolve(strict=True);ownraw=own.read_bytes()
 need(len(ownraw)<=16384 and hashlib.sha256(ownraw).hexdigest()==args.self_sha256,'exact bounded controls')
 path=Path(args.consumer[0]);raw=path.read_bytes()
 need(path.resolve(strict=True)==path and len(raw)<=65536 and hashlib.sha256(raw).hexdigest()==args.consumer[1],
      'complete new consumer Source before declaration activation')
 ns={'__name__':'portable_q11_control_subject','__file__':str(path)}
 exec(compile(raw,str(path),'exec'),ns)
 I=ns['I7'];Y=quotient_fixture(ns,budget);names=[]
 words=[''.join('1'+('0','2','02')[d]for d in digits)
        for size in range(1,5)for digits in itertools.product(range(3),repeat=size)]
 need(len(words)==120 and [ns['word_from_index'](i)for i in range(1,121)]==words,'independent dictionary enumeration')
 for bad in(0,121,-1,True,'1'):refused(lambda bad=bad:ns['word_from_index'](bad),'bad dictionary index')
 names.append('all120_literal_words_and_invalid_types')
 marks=(I,Y,I,Y)
 ns['direct_order37'](marks,(0,1,2),1,budget);ns['direct_order37'](marks,(1,2,3),1,budget)
 refused(lambda:ns['direct_order37']((I,I,I,I),(0,1,2),1,budget),'identity witness')
 refused(lambda:ns['direct_order37'](marks,(0,1,3),1,budget),'foreign end')
 minus=tuple(tuple(10*int(i==j)for j in range(7))for i in range(7))
 refused(lambda:ns['direct_order37']((I,minus,I,I),(0,1,2),1,budget),'wrong exact order')
 names.append('both_end_maps_exact37_and_three_invalid_witnesses')
 ctx=dict(orbits=[[1,[1],[1],1]],IR=(),R=(),catalogue=[])
 refused(lambda:ns['verify_records']([[1,1,'0'*64,1,1]],[1],ctx,budget),'foreign orbit body')
 names.append('full_original_orbit_digest_required')
 # IO fixtures are scalar strings, not original matrices or Source programs.
 with tempfile.TemporaryDirectory(prefix='portable_q11_controls_')as temp:
  root=Path(temp).resolve(strict=True);(root/'first.json').write_bytes(b'{"fixture":1}\n')
  (root/'second.json').write_bytes(b'{"fixture":2}\n')
  def original(n):
   data=(root/n).read_bytes()
   return dict(path='/nonexistent/original_history.json',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  first=original('first.json');second=original('second.json');b=ns['Budget'](root)
  b.bind([dict(original=first,relative='first.json'),dict(original=second,relative='second.json')])
  need(b.doc(first)=={'fixture':1}and b.doc(second)=={'fixture':2},'whole identity distinguishes historical versions')
  b.recheck();names.append('relative_only_reads_and_distinct_same_original_path_versions')
  for bad in('../outside','/private/tmp/outside','x/../outside','./first.json'):
   refused(lambda bad=bad:ns['Budget'](root).bind([dict(original=first,relative=bad)]),'relative escape')
  names.append('absolute_and_parent_relative_paths_refused_before_IO')
  refused(lambda:ns['Budget'](root).bind([dict(original=first,relative='first.json')]*2),'ambiguous original identity')
  refused(lambda:ns['Budget'](root).read(first),'undeclared original key')
  wrong=dict(first);wrong['sha256']='0'*64;b=ns['Budget'](root);b.bind([dict(original=wrong,relative='first.json')])
  refused(lambda:b.read(wrong),'whole-content mismatch')
  names.append('mapping_ambiguity_absent_mapping_and_hash_mismatch_refused')
  (root/'alias.json').symlink_to(root/'first.json');b=ns['Budget'](root)
  b.bind([dict(original=first,relative='alias.json')]);refused(lambda:b.read(first),'symlink alias')
  names.append('noncanonical_symlink_payload_refused')
 print(json.dumps(dict(schema='PORTABLE_Q11_TWO_END37_CONTROLS_V1',status='PASS',controls=len(names),names=names,
  program=dict(path=str(own),bytes=len(ownraw),sha256=args.self_sha256),
  consumer=dict(path=str(path),bytes=len(raw),sha256=args.consumer[1]),matrix_products=budget.products,
  original_case_model_or_group_calls=0,prior_Source_or_caller_identity_claim=False,
  qualification='Generic GL7 arithmetic and isolated scalar IO fixtures only; no original G2 marking or fresh scientific replay is established.'),sort_keys=True))

if __name__=='__main__':main()
