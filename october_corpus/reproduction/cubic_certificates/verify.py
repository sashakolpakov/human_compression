"""Portable replay of42accepted original cubic133 matrix certificates."""
import argparse,hashlib,itertools,json,math,os,resource,stat,sys,time
from pathlib import Path,PurePosixPath
START=time.monotonic();PRODUCTS={};FIELD=0;INVERSES=0;ROW_IMAGES=0;READ=0
ROOT=Path(__file__).resolve().parent
if sys.flags.optimize:raise SystemExit('Runwithout-O: literal helpers use assertions.')
def need(ok,why):
 if not ok:raise ValueError(why)
def tick():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(time.monotonic()-START<100 and peak<128*2**20,'100s128MiB finite replay')
def can(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def mat(v,n):
 assert type(v)in(list,tuple)and len(v)==n and all(type(r)in(list,tuple)and len(r)==n and all(type(x)is int and 0<=x<11 for x in r)for r in v)
 return tuple(tuple(r)for r in v)

def identity(n):return tuple(tuple(int(i==j)for j in range(n))for i in range(n))

def mul(a,b):
 n=len(a);assert n==len(b)and all(len(r)==n for r in a+b)
 PRODUCTS[n]=PRODUCTS.get(n,0)+1;assert sum(PRODUCTS.values())<=400000;tick()
 return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(n))%11 for j in range(n))for i in range(n))

def image(v,a):return tuple(sum(v[i]*a[i][j]for i in range(7))%11 for j in range(7))

def inv2(a):
 global INVERSES
 d=(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11;assert d
 x=pow(d,-1,11);INVERSES+=1
 return((a[1][1]*x%11,-a[0][1]*x%11),(-a[1][0]*x%11,a[0][0]*x%11))

def from_pair(row,IR,R):
 assert len(row)==7 and all(type(x)is int and 0<=x<11 for x in row)
 if row[0]==0:P=identity(2);Q=((10,0),(0,10))
 else:
  _,x,y,z,a,b,c=row;P=((x,y),(z,-x%11));Q=((a,b),(c,-a%11))
 det=lambda a:(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11
 assert det(P)==det(Q)!=0
 ip=inv2(P);rows=[]
 for k in range(8):
  E=tuple(tuple(int(2*i+j==k%4)for j in range(2))for i in range(2))
  E=mul(mul(P if k<4 else Q,E),ip);flat=tuple(x for r in E for x in r)
  rows.append(flat+(0,0,0,0)if k<4 else(0,0,0,0)+flat)
 x=mul(mul(IR,tuple(rows)),R)
 assert x[0]==(1,0,0,0,0,0,0,0)and all(x[i][0]==0 for i in range(1,8))
 return tuple(tuple(x[i][j]for j in range(1,8))for i in range(1,8))

def strict(raw):
 def unique(items):
  out={}
  for k,v in items:need(k not in out,'unique JSON fields');out[k]=v
  return out
 def finite(text):
  v=float(text);need(math.isfinite(v),'finite metadata');return v
 return json.loads(raw,object_pairs_hook=unique,parse_float=finite,
  parse_constant=lambda value:(_ for _ in()).throw(ValueError('finite JSON')))
def sig(s):return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def read_ref(ref):
 global READ
 tick();need(type(ref)is dict and set(ref)=={'file','bytes','sha256'},'whole relative descriptor')
 name=ref['file'];need(type(name)is str and len(name)<=160 and '\\'not in name,'bounded relative file')
 p=PurePosixPath(name);need(not p.is_absolute()and str(p)==name and all(x not in('','.','..')for x in p.parts),'literal relative path')
 need(type(ref['bytes'])is int and 0<=ref['bytes']<=1048576 and type(ref['sha256'])is str and len(ref['sha256'])==64 and set(ref['sha256'])<=set('0123456789abcdef'),'bounded exact descriptor')
 path=ROOT.joinpath(*p.parts);s=path.lstat();need(path.resolve(strict=True)==path and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size==ref['bytes'],'ordinary relative input')
 need(READ+ref['bytes']<=2097152,'2MiB total actual artifact reads')
 with path.open('rb')as f:a=os.fstat(f.fileno());raw=f.read(ref['bytes']+1);b=os.fstat(f.fileno())
 need(sig(s)==sig(a)==sig(b)==sig(path.lstat())and len(raw)==ref['bytes']and hashlib.sha256(raw).hexdigest()==ref['sha256'],'whole stable input SHA')
 READ+=len(raw);return raw
def bundle(sha):
 m=ROOT/'manifest.json';need(m.stat().st_size<=16384,'manifest16KiB')
 mr=dict(file='manifest.json',bytes=m.stat().st_size,sha256=sha);manifest=strict(read_ref(mr))
 need(manifest['schema']=='F004_CUBIC133_PORTABLE_REPLAY_MANIFEST_V1'and manifest['field']==11 and manifest['dimension']==7,'portable mathematical role')
 refs=manifest['files'];need(type(refs)is dict and set(refs)=={'verifier','controls','cases','domain','proof','provenance','supervisor','runtime_base','requirements'},'complete relative release roles')
 need(refs['verifier']['file']==Path(__file__).name and len({r['file']for r in refs.values()})==len(refs),'one exact role per file')
 need(sum(refs[k]['bytes']for k in('verifier','controls','supervisor','runtime_base'))<=65536,'Source namespace65KiB')
 raw={k:read_ref(r)for k,r in refs.items()}
 return manifest,mr,raw
def field_cubic(f):
 need(type(f)is list and len(f)==4 and f[3]==1 and all(type(x)is int and 0<=x<11 for x in f),'monic exact field cubic')
 return f
def primitive_cubic(f):
 field_cubic(f)
 need(all((((x+f[2])*x+f[1])*x+f[0])%11!=0 for x in range(11)),'irreducible cubic: no F11 root')
 C=((0,1,0),(0,0,1),tuple(-x%11 for x in f[:3]))
 def naive(n):
  value=identity(3)
  for _ in range(n):value=mul(value,C)
  return value
 need(naive(133)==identity(3)and naive(7)!=identity(3)and naive(19)!=identity(3),'independent companion exact133')
 return True
def direct_row(marks,f,v):
 global ROW_IMAGES
 need(type(v)is list and len(v)==7 and all(type(x)is int and 0<=x<11 for x in v)and any(v),'nonzero field row')
 need(len(marks)==3,'same LEFT three marks');powers=[tuple(v)]
 for _ in range(3):
  w=powers[-1]
  for A in marks:
   tick();ROW_IMAGES+=1;need(ROW_IMAGES<=200000,'bounded row images');w=image(w,A)
  powers.append(w)
 result=tuple((powers[3][j]+f[2]*powers[2][j]+f[1]*powers[1][j]+f[0]*powers[0][j])%11 for j in range(7))
 need(result==(0,)*7,'direct nine-image cubic relation');return result
def field(n):
 global FIELD
 FIELD+=n;need(FIELD<=200000,'200000 rank field operations');tick()
def sign_rows(A,sign):
 need(type(sign)is int and sign in(-1,1),'literal involution sign')
 field(49)
 return tuple(tuple((A[j][i]-sign if i==j else A[j][i])%11 for j in range(7))for i in range(7))
def extend_basis(basis,rows):
 """Exact forward Gaussian row span; supplied basis is never mutated."""
 basis=list(basis)
 for row in rows:
  need(type(row)is tuple and len(row)==7 and all(type(x)is int and 0<=x<11 for x in row),'whole field equation row')
  if len(basis)==7:break
  w=list(row)
  for p,old in basis:
   if w[p]:
    q=w[p];field(2*(7-p))
    for j in range(p,7):w[j]=(w[j]-q*old[j])%11
  p=next((j for j,x in enumerate(w)if x),None)
  if p is not None:
   inverse=pow(w[p],9,11);field(4+7-p)
   for j in range(p,7):w[j]=w[j]*inverse%11
   basis.append((p,tuple(w)));basis.sort(key=lambda pair:pair[0])
 return tuple(basis)
def prefix_bases(a,b):
 return {(x,y):extend_basis((),sign_rows(a,x)+sign_rows(b,y))for x in(-1,1)for y in(-1,1)}
def left_ranks(prefix,c):
 rows={z:sign_rows(c,z)for z in(-1,1)}
 return [len(extend_basis(prefix[(x,y)],rows[z]))for x in(-1,1)for y in(-1,1)for z in(-1,1)]
def check_marks(marks):
 need(len(marks)==4 and len(set(marks))==4,'four distinct ORIGINAL marks')
 I=identity(7)
 need(all(A!=I and mul(A,A)==I for A in marks),'nonidentity involutions')
 need(all(mul(marks[i],marks[j])==mul(marks[j],marks[i])for i in range(4)for j in range(i+2,4)),'all distant string commutations')
def verify_case(case,domain,R,IR,prefix):
 p=case['position'];j=case['representative_J_index']
 need(type(p)is int and 1<=p<=3779 and type(j)is int and 1<=j<=14763,'original position and rawJ')
 orbit=domain['orbits'][p-1]
 need(can(case['original_orbit_row'])==can(orbit)and orbit[0]==j and j in orbit[1],'literal original orbit association import')
 need(type(orbit)is list and len(orbit)==4 and type(orbit[0])is int
  and type(orbit[1])is list and orbit[1]==sorted(set(orbit[1]))and all(type(x)is int and 1<=x<=14763 for x in orbit[1])
  and type(orbit[2])is list and all(type(x)is int and x in domain['prefix_stabilizer_indices']for x in orbit[2])
  and type(orbit[3])is int and orbit[3]>0 and len(orbit[1])==len(orbit[2])
  and len(orbit[1])*orbit[3]==len(domain['prefix_stabilizer_indices']),'typed original member/transporter roles; action proof imported')
 need(case['word']==[0,1,2]and all(type(x)is int for x in case['word'])and case['end']=='left','same original LEFT word')
 marks=tuple(mat(A,7)for A in case['actual_marks']);check_marks(marks)
 need(hashlib.sha256(can(marks)).hexdigest()==case['actual_marks_canonical_SHA256'],'all original carried matrix bytes')
 raw=domain['catalogue'][j-1];need(type(raw)is list and len(raw)==7 and all(type(x)is int and 0<=x<11 for x in raw),'exact original catalogue coordinates')
 need(raw==[0]*7 if raw[0]==0 else raw[0]in(1,2),'literal catalogue strata')
 need(from_pair(raw,IR,R)==marks[2],'finite original catalogue/frame transport')
 f=field_cubic(case['cubic']);primitive_cubic(f);direct_row(marks[:3],f,case['nonzero_row'])
 ranks=left_ranks(prefix,marks[2]);need(ranks==[7]*8,'all eight common LEFT sign systems have trivial kernel')
 return dict(position=p,representative_J_index=j,common_LEFT_sign_ranks=ranks)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary EBS/no optimization')
 need(all(k not in os.environ for k in('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')),'four environment denials')
 manifest,mref,raw=bundle(args.manifest_sha256);data=strict(raw['cases']);domain=strict(raw['domain'])
 need(data['schema']=='F004_CUBIC133_PORTABLE_ACCEPTED42_V1'and data['field']==11 and data['dimension']==7 and data['original_job']==[24,4]and data['convention']=='RIGHT_ROW','exact42 finite certificate role')
 need(domain['field']==11 and domain['rank']==4 and domain['original_job']==[24,4]and domain['convention']=='RIGHT_ROW'and len(domain['catalogue'])==14763 and len(domain['orbits'])==3779,'retained original domain shape')
 need(hashlib.sha256(raw['domain']).hexdigest()==data['original_domain_sha256']and hashlib.sha256(can(domain['catalogue'])).hexdigest()==data['full_catalogue_sha256']and hashlib.sha256(can(domain['orbits'])).hexdigest()==data['full_orbit_array_sha256'],'whole original literal catalogue/orbit array hashes')
 cases=data['cases'];need(type(cases)is list and len(cases)==42 and data['positions']==sorted(set(data['positions']))and [c['position']for c in cases]==data['positions'],'complete fixed42 distinct accepted positions')
 R=mat(domain['standard_to_actual_row_map'],8);IR=mat(domain['actual_to_standard_row_map'],8)
 need(mul(R,IR)==mul(IR,R)==identity(8),'literal frame inverses')
 first=tuple(mat(A,7)for A in cases[0]['actual_marks']);a,b,_,e=first
 need(len(domain['standard_ordered_prefix_matrices'])==3,'three complete original prefix transports')
 for A,standard in zip((a,e,b),domain['standard_ordered_prefix_matrices']):
  ext=((1,0,0,0,0,0,0,0),)+tuple((0,)+r for r in A)
  need(mul(mul(IR,mat(standard,8)),R)==ext,'whole actual prefix/frame transport')
 prefix=prefix_bases(a,b);verified=[]
 for case in cases:
  carried=tuple(mat(A,7)for A in case['actual_marks']);need((carried[0],carried[1],carried[3])==(a,b,e),'same exact prefix permits invocation-local Gaussian cache')
  verified.append(verify_case(case,domain,R,IR,prefix))
 for ref in manifest['files'].values():read_ref(ref)
 read_ref(mref);tick()
 print(json.dumps(dict(status='VERIFIED42_CUBIC133_FINITE_REPLAYS',positions=data['positions'],cases=len(verified),
  all_eight_LEFT_sign_ranks_checked=True,matrix_products=PRODUCTS,rank_field_operations=FIELD,row_images=ROW_IMAGES,
  artifact_read_bytes=READ,source_and_inputs_rechecked=True,
  imported_premises='Original full naturalG2/model/member/faithfulness/orbittransport and complete maximalclassification/J1spectrum; supplied matrices do not reprove them.',
  whole_original_credit=0,Lean_credit=0,conjecture_credit=0,new_compression_credit=0),sort_keys=True))
if __name__=='__main__':main()
