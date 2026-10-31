"""Small synthetic controls; no accepted42 verification is executed here."""
import argparse,hashlib,json,os,stat,sys,tempfile,types
from pathlib import Path

ENV=('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')
def environment(environ):
 if any(k in environ for k in ENV):raise ValueError('four retained environment denials')
def signature(s):return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def bootstrap(path,cap,sha,declared=None):
 if type(sha)is not str or len(sha)!=64 or set(sha)-set('0123456789abcdef'):raise ValueError('exact SHA256')
 if declared is not None and(type(declared)is not int or not 0<=declared<=cap):raise ValueError('bounded declared size')
 before=path.lstat()
 if path.resolve(strict=True)!=path or not stat.S_ISREG(before.st_mode)or before.st_nlink!=1 or not 0<=before.st_size<=cap or(declared is not None and before.st_size!=declared):raise ValueError('ordinary bounded bootstrap file')
 with path.open('rb')as stream:
  opened=os.fstat(stream.fileno())
  if signature(opened)!=signature(before):raise ValueError('bootstrap opened identity')
  raw=stream.read(cap+1);after=os.fstat(stream.fileno())
 if signature(before)!=signature(after)or signature(after)!=signature(path.lstat())or len(raw)!=before.st_size or hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('whole stable bootstrap SHA')
 return raw

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
 if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):raise ValueError('EBS/no optimization')
 environment(os.environ)
 root=Path(__file__).resolve(strict=True).parent;raw=bootstrap(root/'manifest.json',16384,args.manifest_sha256)
 m=json.loads(raw);ref=m['files']['verifier']
 if type(ref)is not dict or set(ref)!={'file','bytes','sha256'}or ref['file']!='verify.py':raise ValueError('exact verifier role')
 source=bootstrap(root/'verify.py',32768,ref['sha256'],ref['bytes'])
 ns={'__name__':'synthetic_cubic133_verifier','__file__':str(root/'verify.py')};exec(compile(source,str(root/'verify.py'),'exec'),ns)
 h=types.SimpleNamespace(**ns);manifest,mref,inputs=h.bundle(args.manifest_sha256);checks=[]
 def check(name,ok):h.need(ok,name);checks.append(name)
 def rejects(name,fn):
  try:fn()
  except(ValueError,AssertionError,TypeError,IndexError):checks.append(name);return
  raise ValueError('accepted invalid '+name)
 for name in ENV:rejects('environment-'+name,lambda name=name:environment({name:'1'}))
 with tempfile.TemporaryDirectory(prefix='cubic133-bootstrap-')as temporary:
  q=Path(temporary).resolve(strict=True);one=q/'one';one.write_bytes(b'x');sha=hashlib.sha256(b'x').hexdigest()
  check('stable-bootstrap-file',bootstrap(one,1,sha,1)==b'x')
  rejects('bootstrap-wrong-SHA',lambda:bootstrap(one,1,'0'*64,1))
  for name,cap in(('manifest',16384),('verifier',32768)):
   oversized=q/name;oversized.write_bytes(b'x'*(cap+1))
   rejects(name+'-oversize-before-open',lambda p=oversized,cap=cap:bootstrap(p,cap,'0'*64))
  link=q/'symlink';link.symlink_to(one.name)
  rejects('bootstrap-symlink',lambda:bootstrap(link,1,sha,1))
  hard=q/'hardlink';os.link(one,hard)
  rejects('bootstrap-hardlink',lambda:bootstrap(hard,1,sha,1))
 I=h.identity(7)
 check('field-matrix',h.mat(I,7)==I)
 rejects('bool-field-matrix',lambda:h.mat([[True]*7 for _ in range(7)],7))
 rejects('foreign-field-matrix',lambda:h.mat([[11]*7 for _ in range(7)],7))
 rejects('identity-mark-refusal',lambda:h.check_marks((I,I,I,I)))
 f=[10,0,6,1];check('independent-companion133',h.primitive_cubic(f))
 rejects('cubic-root-refusal',lambda:h.primitive_cubic([10,0,0,1]))
 rejects('bool-cubic',lambda:h.field_cubic([True,0,6,1]))
 rejects('nonmonic-cubic',lambda:h.field_cubic([10,0,6,2]))
 C=((0,1,0),(0,0,1),(1,0,5))
 A=tuple(tuple(C[i][j]if i<3 and j<3 else int(i==j)if i>=3 and j>=3 else 0 for j in range(7))for i in range(7))
 check('direct-cubic-row',h.direct_row((A,I,I),f,[1,0,0,0,0,0,0])==(0,)*7)
 rejects('zero-row',lambda:h.direct_row((A,I,I),f,[0]*7))
 rejects('wrong-row',lambda:h.direct_row((A,I,I),f,[0,0,0,0,0,0,1]))
 rejects('wrong-word',lambda:h.direct_row((I,I,I),f,[1,0,0,0,0,0,0]))
 e0=(1,0,0,0,0,0,0);e1=(0,1,0,0,0,0,0)
 b=h.extend_basis((),(e0,e1));check('rank-two-independent',len(b)==2)
 check('dependent-row-rank',len(h.extend_basis(b,(e0,tuple((x+y)%11 for x,y in zip(e0,e1)))))==2)
 check('basis-not-mutated',b==h.extend_basis((),(e0,e1)))
 check('full-rank',len(h.extend_basis((),I))==7)
 rejects('bool-equation-row',lambda:h.extend_basis((),((True,)*7,)))
 U=[list(r)for r in I];U[0][1]=1;U[1][1]=10;U=tuple(map(tuple,U))
 check('nonsymmetric-involution',h.mul(U,U)==I)
 rows=h.sign_rows(U,1);v=(2,1,0,0,0,0,0)
 check('RIGHT-row-transpose-required',all(sum(x*y for x,y in zip(v,r))%11==0 for r in rows)
  and any(sum(x*y for x,y in zip(e0,r))%11 for r in rows))
 ranks=h.left_ranks(h.prefix_bases(I,I),I)
 check('common-line-not-missed',ranks[-1]==0 and any(x<7 for x in ranks))
 check('literal-zero-stratum-transport',h.from_pair([0]*7,h.identity(8),h.identity(8))==tuple(tuple((1 if i<3 else 10)if i==j else 0 for j in range(7))for i in range(7)))
 rejects('duplicate-JSON-key',lambda:h.strict(b'{"x":1,"x":2}'))
 rejects('relative-path-escape',lambda:h.read_ref(dict(file='../verify.py',bytes=1,sha256='0'*64)))
 for ref in manifest['files'].values():h.read_ref(ref)
 h.read_ref(mref);h.tick()
 print(json.dumps(dict(status='PASS_SYNTHETIC_CUBIC133_CONTROLS',checks=checks,count=len(checks),accepted_case_calls=0,
  rank_field_operations=ns['FIELD'],matrix_products=ns['PRODUCTS'],row_images=ns['ROW_IMAGES'],
  source_and_input_identity_rechecked=True,scope='Synthetic scalar/row/rank/transpose/transport/typing seams only; no namedG2/model claim.'),sort_keys=True))
if __name__=='__main__':main()
