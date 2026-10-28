"""UNRUN corpus-relative checker of adopted integer-word two-end37 batches.
New adapter author /root/prime_theory_audit; relative resolver and all original
mathematical routines are borrowed literally from the fixed27 public wrapper
by /root/compact_proof_author and its old9f arithmetic/context parent.
Every active read uses the explicit corpus mapping; there is no private path
fallback, historical caller identity transfer, new adoption or search.
"""
import time
START=time.monotonic()
import argparse,hashlib,json,math,os,resource,signal,stat,sys,zlib
from pathlib import Path,PurePosixPath
I2=((1,0),(0,1))
I7=tuple(tuple(int(i==j)for j in range(7))for i in range(7))
I8=tuple(tuple(int(i==j)for j in range(8))for i in range(8))
ENV4=('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')
def need(ok,why):
 if not ok:raise ValueError(why)

def can(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def digest(v):return hashlib.sha256(can(v)).hexdigest()

def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'unique JSON keys');out[k]=v
  return out
 def floating(text):
  value=float(text);need(math.isfinite(value),'finite JSON float');return value
 return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def relative(text):
 need(type(text)is str and text and text.isascii(),'literal relative path')
 path=PurePosixPath(text)
 need(not path.is_absolute()and str(path)==text and not set(path.parts)&{'.','..','.git','__pycache__','.lake'},
      'relative corpus artifact only, no private fallback')
 return Path(*path.parts)

def reference_key(reference):
 need(type(reference)is dict and set(reference)=={'path','bytes','sha256'}
      and type(reference['path'])is str and type(reference['bytes'])is int
      and 0<=reference['bytes']<=2**21 and type(reference['sha256'])is str
      and len(reference['sha256'])==64 and set(reference['sha256'])<=set('0123456789abcdef'),
      'complete bounded original identity')
 return(reference['path'],reference['bytes'],reference['sha256'])

class Budget:
 def __init__(self,root):
  need(type(root)is Path or isinstance(root,Path),'explicit Path root')
  need(root.is_absolute()and root.resolve(strict=True)==root,'canonical explicit corpus root')
  self.root=root;self.maps={};self.refs={};self.raw={};self.bytes=0
  self.products=0;self.row_images=0;self.peak=0
 def tick(self):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  self.peak=max(self.peak,rss)
  need(rss<128*2**20 and time.monotonic()-START<125,'128MiB125s portable direct replay envelope')
 def physical(self,reference,again=False):
  self.tick();reference_key(reference);name=str(relative(reference['path']))
  need(self.refs.get(name,reference)==reference,'one exact physical identity')
  if name in self.raw and not again:return self.raw[name]
  need(self.bytes+reference['bytes']<=8*2**20 and(name in self.refs or len(self.refs)<96),
       '8MiB96paths includes every physical reread')
  path=self.root/relative(name);before=path.lstat()
  need(path.resolve(strict=True)==path and path.is_relative_to(self.root)
       and stat.S_ISREG(before.st_mode)and before.st_nlink==1 and before.st_size==reference['bytes'],
       'canonical single-link relative ordinary input')
  with path.open('rb')as stream:
   opened=os.fstat(stream.fileno());raw=stream.read(reference['bytes']+1);after=os.fstat(stream.fileno())
  signature=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
  need(signature(before)==signature(opened)==signature(after)==signature(path.lstat())
       and len(raw)==reference['bytes']and hashlib.sha256(raw).hexdigest()==reference['sha256'],
       'fresh whole relative content, never an original-machine path read')
  self.refs[name]=dict(reference);self.raw[name]=raw;self.bytes+=len(raw);return raw
 def bind(self,rows):
  need(type(rows)is list and 1<=len(rows)<=90,'finite explicit original-to-relative map')
  maps={}
  for row in rows:
   need(type(row)is dict and set(row)=={'original','relative'},'explicit complete mapping row')
   key=reference_key(row['original']);name=str(relative(row['relative']))
   need(key not in maps,'one original complete identity mapping')
   maps[key]=dict(path=name,bytes=key[1],sha256=key[2])
  self.maps=maps
 def read(self,reference,again=False):
  key=reference_key(reference);need(key in self.maps,'all original reads require explicit included mapping')
  return self.physical(self.maps[key],again)
 def doc(self,reference):return decode(self.read(reference))
 def recheck(self):
  for reference in list(self.refs.values()):self.physical(reference,True)

 def multiply(self,A,B):
   self.products+=1;self.tick();need(self.products<=400000,'400000 direct matrix products')
   need(type(A)is tuple and type(B)is tuple and 1<=len(A)<=8 and 1<=len(B)<=8
    and 1<=len(B[0])<=8 and all(len(row)==len(B)for row in A)
    and all(len(row)==len(B[0])for row in B),'complete small compatible rectangular product')
   return tuple(tuple(sum(A[i][k]*B[k][j]for k in range(len(B)))%11 for j in range(len(B[0])))for i in range(len(A)))

 def image(self,row,mark):
   self.row_images+=1;self.tick();need(self.row_images<=200000,'200000 direct row images')
   return tuple(sum(row[k]*mark[k][j]for k in range(7))%11 for j in range(7))


def matrix(raw,n):
    need(type(raw) is list and len(raw) == n
        and all(type(row) is list and len(row) == n for row in raw)
        and all(type(x) is int and 0 <= x < 11 for row in raw for x in row),'Canonical field matrix')
    return tuple(tuple(row) for row in raw)

def flat(A):
    return [x for row in A for x in row]

def matrix2(v):
    need(type(v) in (list,tuple) and len(v) == 4
        and all(type(x) is int and 0 <= x < 11 for x in v),'Canonical 2 by 2 coefficients')
    return (tuple(v[:2]),tuple(v[2:]))

def determinant(A):
    return (A[0][0]*A[1][1]-A[0][1]*A[1][0]) % 11

def inverse2(A):
    r = pow(determinant(A),-1,11)
    return ((r*A[1][1] % 11,-r*A[0][1] % 11),(-r*A[1][0] % 11,r*A[0][0] % 11))

def canonical_pair(P,Q):
    values = tuple(flat(P)+flat(Q)); r = pow(next(x for x in values[:4] if x),-1,11)
    return tuple(r*x % 11 for x in values)

def catalogue_pair(row):
    need(type(row) is list and len(row) == 7
        and all(type(x) is int and 0 <= x < 11 for x in row),'Literal catalogue row')
    if row[0] == 0:
        return I2,((10,0),(0,10))
    _,x,y,z,a,b,c = row
    return ((x,y),(z,-x % 11)),((a,b),(c,-a % 11))

def operator(check,P,Q):
    invP = inverse2(P); rows = []
    for j in range(8):
        basis = tuple(tuple(int(2*r+s == j % 4) for s in range(2)) for r in range(2))
        image = check.multiply(check.multiply(P if j < 4 else Q,basis),invP)
        coeff = tuple(flat(image))
        rows.append(coeff+(0,0,0,0) if j < 4 else (0,0,0,0)+coeff)
    return tuple(rows)

def actual_operator(check,IR,R,P,Q):
    need(determinant(P) == determinant(Q) != 0,'Equal nonzero pair determinants')
    actual = check.multiply(check.multiply(IR,operator(check,P,Q)),R)
    need(actual[0] == (1,0,0,0,0,0,0,0)
        and all(actual[k][0] == 0 for k in range(1,8)),'Full unital pure-space transport')
    return tuple(tuple(actual[i][j] for j in range(1,8)) for i in range(1,8))

def expand_runs(runs, maximum):
 need(type(runs)is list,'literal position runs');out=[];last=0
 for a,b in runs:
  need(type(a)is type(b)is int and last<a<=b<=maximum,'ordered disjoint position runs')
  out.extend(range(a,b+1));last=b
 return out

def packed_runs(values):
 out=[]
 for x in sorted(values):
  if out and out[-1][1]+1==x:out[-1][1]=x
  else:out.append([x,x])
 return out

def context(plan,budget):
 projection=budget.doc(plan['projection']);gate=budget.doc(plan['Root_projection_acceptance'])
 manifest=budget.doc(plan['unpaid_manifest']);job=plan['original_job']
 need(gate['schema']=='ROOT_ACCEPTED_Q11_RANK4_DISPOSITION_PROJECTIONS_V1'and gate['root']=='/root'
  and gate['source_manifest']==plan['unpaid_manifest']and gate['no_new_mathematical_case_evaluations']is True,
  'separate actual Root adoption of the small metadata projection')
 rows=[r for r in gate['projections']if r[0]==job[0]]
 need(len(rows)==1 and rows[0][1:]==[plan['projection']['bytes'],plan['projection']['sha256']]
  and plan['projection']['path']==str(Path(gate['projection_directory'])/('job_%04d.json'%job[0])),
  'exact adopted same-job byte-identical projection')
 need(gate['scope_qualification']=='Set difference against explicitly inspected accepted registry; no global absence claim.',
  'inspected registry qualification is retained')
 registered=[r for r in manifest['jobs']if r['original_job']==job]
 need(len(registered)==1 and registered[0]['projection']['bytes']==plan['projection']['bytes']
  and registered[0]['projection']['sha256']==plan['projection']['sha256'],'same global registered projection bytes')
 refs=projection['original_domain_whole_pins']
 pt=budget.doc(refs['producer_terminal']);st=budget.doc(refs['Saved_terminal'])
 produced=budget.doc(refs['producer_result']);domain=budget.doc(refs['Saved_result']);export=budget.doc(refs['prefix_export'])
 for term,mode,result in((pt,'produce',refs['producer_result']),(st,'check',refs['Saved_result'])):
  need(term['schema']=='ROOT_CLOSED_F004_Q11_INDEXED_PREFIX_V1'and term['root']=='/root'
   and term['success']is True and term['rank']==4 and term['mode']==mode and term['original_job']==job
   and term['result']==result and term['prefix_export']==refs['prefix_export'],'existing genuine original indexed-domain closure')
 need(st['producer_terminal']==refs['producer_terminal']and st['complete_fresh_same_code_Saved_comparison']is True
  and st['Saved_ignored_observational_fields']==['seconds','peak_self_bytes'],'whole original Saved comparison')
 for x in(produced,domain):x.pop('seconds',None);x.pop('peak_self_bytes',None)
 need(can(produced)==can(domain),'all nonobservational original domain fields equal');del produced
 need(domain['schema']=='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
  and domain['certificate_verified']is True and domain['rank']==4 and domain['field']==11
  and domain['original_job']==export['original_job']==projection['original_job']==job
  and domain['prefix_export']==refs['prefix_export']and domain['selected_labels']==export['selected_labels']==[1,4,2]
  and export['end_order']==[1,4,2,3]and export['convention']=='RIGHT_ROW'
  and export['matrix_frame_result']==plan['matrix_frame_result']
  and domain['origin']==export['origin']and domain['original_prefix_index']==projection['original_prefix_index']==export['original_prefix_index']
  and domain['original_prefix_index_proof']==projection['original_prefix_index_proof']==export['origin']['original_prefix_index_proof'],
  'literal original prefix, labels and actual basis')
 need(domain['external_premises']==export['external_premises']and domain['external_premises']['root']=='/root'
  and domain['external_premises']['original_A_equals_G']is True,'original model and A=G premises')
 for field,key in(('indexed_source','indexed'),('generic_export_source','generic_export')):
  need(st[field]==plan['old_sources'][key],'exact old Source subjects, no PASS retag')
  for r in st[field].values():budget.read(r)
 binding=budget.doc(st['binding_terminal']);model=budget.doc(domain['external_premises']['model_source_join'])
 frame=budget.doc(domain['faithful_frame_acceptance']);normal=budget.doc(domain['normalization_result'])
 normal_acceptance=budget.doc(domain['normalization'])
 need(binding.get('root')=='/root'and binding.get('success')is True and model['root']=='/root'
  and model['actual_raw_model_alias_checked']is True and model['faithful_frame']==domain['faithful_frame_acceptance']
  and frame['status']=='ROOT_ACCEPTED_Q11_FAITHFUL_MATRIX_FRAME'and frame['result']==plan['matrix_frame_result']
  and frame['full_generator_point_checks']==354312 and frame['inverse_checks']==6 and frame['inputs_unchanged']is True,
  'borrowed complete faithful original point-frame join')
 need(normal['status']=='CERTIFIED_GF11_SPLIT_CAYLEY_COMPOSITION'and normal['certificate_verified']is True
  and normal['kappa']==7 and normal_acceptance['status']==plan['normalization_status'],
  'same acquired actual Cayley norm')
 R=matrix(domain['standard_to_actual_row_map'],8);IR=matrix(domain['actual_to_standard_row_map'],8)
 need(budget.multiply(R,IR)==budget.multiply(IR,R)==I8,'whole frame inverses')
 a,e,b=[matrix(x,7)for x in export['matrices']]
 for g,standard in zip((a,e,b),domain['standard_ordered_prefix_matrices']):
  ext=((1,0,0,0,0,0,0,0),)+tuple((0,)+row for row in g)
  need(budget.multiply(budget.multiply(IR,matrix(standard,8)),R)==ext,'same complete standard/actual prefix transport')
 need(len({a,e,b})==3 and all(g!=I7 and budget.multiply(g,g)==I7 for g in(a,e,b))
  and budget.multiply(a,e)==budget.multiply(e,a)and budget.multiply(b,e)==budget.multiply(e,b)
  and budget.multiply(a,b)!=budget.multiply(b,a),'fixed original nonidentity involution/string relations')
 need(domain['common_eigenspace_dimensions']==[1,2,2,2]and len(domain['frame'])==8
  and domain['frame'][1][0]==0 and domain['frame_norms'][1]==domain['delta']in(1,2),
  'acquired nonsingular common positive line and seed locator')
 seed=tuple(domain['frame'][1][1:]);need(len(seed)==7 and any(seed)
  and budget.image(seed,a)==budget.image(seed,e)==seed,'same actual seed and endpoint positive equations')
 q=matrix(normal['quadratic_form_matrix'],8);seed8=(0,)+seed
 need(sum(seed8[i]*q[i][j]*seed8[j]for i in range(8)for j in range(8))%11==domain['delta'],
  'same actual canonical nonsingular seed norm')
 saved_frame=budget.doc(plan['matrix_frame_result']);ambient=tuple(matrix(m,7)for m in saved_frame['source_matrices'])
 need(len(ambient)==2 and saved_frame['full_generator_point_checks']==354312
  and saved_frame['six_inverse_checks']==6,'two original known-G matrices in the acquired faithful frame')
 catalogue=domain['catalogue'];orbits=domain['orbits'];stabilizer=domain['prefix_stabilizer_indices']
 need(len(catalogue)==domain['catalogue_size']==14763 and digest(catalogue)==domain['catalogue_sha256']
  and domain['catalogue_schema']=='INDEX1_IS_A0_OTHER_ROWS_ARE_DELTA_PX_PY_PZ_QX_QY_QZ_SIMULTANEOUS_SIGN_QUOTIENT'
  and domain['selected_raw_domain_indices']==list(range(1,14764)), 'entire original raw J catalogue, never a new indexing')
 need(len(orbits)==projection['original_orbit_rows']and digest(orbits)==projection['full_orbit_array_sha256']
  and domain['orbit_action']==projection['orbit_action']and domain['orbit_schema']==projection['orbit_schema']
  and stabilizer==projection['prefix_stabilizer_indices'],'whole acquired orbit/member/transporter table')
 covered=[]
 for rep,members,transports,fixed in orbits:
  need(rep in members and members==sorted(set(members))and len(members)==len(transports)
   and all(type(j)is int and j in stabilizer for j in transports)
   and type(fixed)is int and fixed>0 and len(members)*fixed==len(stabilizer),'all matching original orbit transport roles')
  covered.extend(members)
 need(sorted(covered)==list(range(1,14764)),'whole disjoint14763-member original orbit partition')
 unpaid=expand_runs(projection['unpaid_representation']['runs'],len(orbits))
 need(digest(unpaid)==projection['unpaid_representation']['expanded_sha256']
  and len(unpaid)==projection['exact_unpaid_count_relative_to_inspected_accepted_registry'], 'exact adopted unpaid positions')
 paid=sorted({i for fact in projection['known_paid_facts']for i in fact['orbit_positions']})
 need(len(paid)==projection['known_paid_positions_count']and not set(paid)&set(unpaid)
  and sorted(paid+unpaid)==list(range(1,len(orbits)+1)), 'no paid position replayed or unpaid position omitted')
 return dict(projection=projection,domain=domain,export=export,refs=refs,R=R,IR=IR,
  a=a,b=b,e=e,seed=seed,ambient=ambient,catalogue=catalogue,orbits=orbits,unpaid=unpaid,paid=paid,
  inspected_registry_qualification=gate['scope_qualification'])

def power(value,exponent,budget):
 need(type(exponent)is int and exponent>=0,'fixed nonnegative direct exponent')
 result=I7
 while exponent:
  if exponent&1:result=budget.multiply(result,value)
  exponent//=2
  if exponent:value=budget.multiply(value,value)
 return result

def word_from_index(index):
    need(type(index)is int and 1<=index<=120,'literal original dictionary index1..120')
    offset=0
    for length in range(1,5):
        count=3**length
        if index<=offset+count:
            value=index-1-offset;digits=[0]*length
            for position in range(length-1,-1,-1):
                digits[position]=value%3;value//=3
            word=''.join('1'+('0','2','02')[digit]for digit in digits)
            need(2<=len(word)<=12 and set(word)<=set('012'),'same-section literal word')
            return word
        offset+=count
    raise ValueError('dictionary index exhausted')

def direct_order37(marks,section,index,budget):
    need(section in((0,1,2),(1,2,3)),'actual left or right end only')
    value=I7
    for letter in word_from_index(index):
        value=budget.multiply(value,marks[section[int(letter)]])
    witness=power(value,6,budget)
    need(witness!=I7 and power(witness,37,budget)==I7,'actual same-end word has exact prime37 order')
    return dict(section=list(section),dictionary_index=index)

def verify_records(records,selected,ctx,budget):
    need(type(records)is list and len(records)<=1024,'bounded supplied rows only')
    positions=[];members=0
    for row in records:
        need(type(row)is list and len(row)==5,'compact position/representative/SHA/two-indices record')
        position,representative,orbit_sha,left_index,right_index=row
        need(type(position)is int and position in selected and position not in positions,
             'one exact selected current position')
        orbit=ctx['orbits'][position-1]
        need(type(representative)is int and representative==orbit[0]and orbit_sha==digest(orbit),
             'same full original member/transporter orbit')
        c=actual_operator(budget,ctx['IR'],ctx['R'],*catalogue_pair(ctx['catalogue'][representative-1]))
        marks=(ctx['a'],ctx['b'],c,ctx['e'])
        need(len(set(marks))==4 and all(g!=I7 and budget.multiply(g,g)==I7 for g in marks)
             and all(budget.multiply(marks[i],marks[j])==budget.multiply(marks[j],marks[i])
                     for i in range(4)for j in range(i+2,4)),
             'actual original distinct nonidentity involutions and all string relations')
        direct_order37(marks,(0,1,2),left_index,budget)
        direct_order37(marks,(1,2,3),right_index,budget)
        positions.append(position);members+=len(orbit[1])
    need(positions==sorted(positions),'supplied original positions in exact sorted order')
    return positions,members

THEOREM_SHA='cd9d2848d12af4f0b195787c53e904446bb3839df59e36cb67e46ce25cb9ae42'
THEOREM_REVIEW_SHA='826de2cc7879e8d67850ddd34a813357d0af614598b2af96f7d045e2edd4766f'

PARENT_SHA='9f86b53a64c01061a3606c49f9dfd706728438885536a826140f003b9e887956'
DICTIONARY='V4_THREE_MARKS_LENGTH1_TO4_V1'

def same_mapped_object(budget,left,right):
 """Equality only through two explicitly declared whole original identities."""
 a,b=reference_key(left),reference_key(right)
 need(a in budget.maps and b in budget.maps and budget.maps[a]==budget.maps[b],
      'both exact original aliases explicitly resolve to the same whole corpus object')
 return True

def historical_plan(reference,budget):
 need(reference['bytes']<=65536,'bounded archived compressed scientific plan')
 packed=budget.read(reference);decoder=zlib.decompressobj(31)
 raw=decoder.decompress(packed,524289)
 need(len(raw)<=524288 and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
      'one complete bounded historical plan; no scientific module activation')
 return decode(raw)

def supplied_index_carrier(raw,plan):
 carrier=decode(raw)
 need(raw==can(carrier)+b'\n' and type(carrier)is dict
      and set(carrier)=={'schema','dictionary','original_job','projection','selector','records'}
      and carrier['schema']=='Q11_TWO_END37_SUPPLIED_WORDS_V1'
      and carrier['dictionary']==DICTIONARY
      and carrier['original_job']==plan['context']['original_job']
      and carrier['projection']==plan['context']['projection'],
      'whole canonical archived integer-word carrier in the exact original context')
 records=carrier['records']
 need(type(records)is list and 1<=len(records)<=1024,'nonempty bounded archived positive batch')
 positions=[]
 for row in records:
  need(type(row)is list and len(row)==5,'original position/representative/orbit SHA/two integer indices')
  position,representative,sha,left,right=row
  need(type(position)is int and position>0 and type(representative)is int and representative>0
       and type(sha)is str and len(sha)==64 and set(sha)<=set('0123456789abcdef'),
       'strict original record header types')
  word_from_index(left);word_from_index(right);positions.append(position)
 need(positions==sorted(set(positions)),'all archived positions sorted and distinct')
 return carrier

def validate_historical_subject(plan,authority,result,prior,carrier,budget):
 need(authority['schema']=='ROOT_ACCEPTED_Q11_RANK4_TWO_END37_IP_FACTS_V1'
      and authority['root']=='/root' and authority['adopted']is True
      and authority['proof_mode']=='DIRECT_TWO_WORD_CHECK'
      and authority['classification']=='FOUR_MARK_INTERSECTION_PROPERTY_FAILURE'
      and authority['four_mark_generation_or_nongeneration_claim']is False
      and authority['whole_original_credit']==authority['conjecture_credit']==authority['Lean_credit']==0,
      'imported adopted integer-word theorem batch, not fixed27 or a literal-word verdict')
 need(result['schema']=='Q11_TWO_END37_DIRECT_RESULT_V1'
      and result['status']=='VERIFIED_TWO_END37_ORIGINAL_RECORDS'
      and result['program']['sha256']==PARENT_SHA
      and result['word_search_or_row_reduction_calls']==result['proposer_or_kernel_imports']==0
      and result['four_mark_generation_or_nongeneration_claim']is False
      and result['whole_original_conjecture_Lean_or_measurement_credit']==0
      and prior['schema']=='Q11_TWO_END37_DIRECT_PLAN_V1'
      and prior['program']==result['program'] and prior['context']==plan['context'],
      'exact retained old9f result and complete historical mathematical context')
 need(authority['original_job']==result['original_job']==prior['original_job']==plan['context']['original_job']
      and authority['projection']==result['projection']==prior['projection']==plan['context']['projection']
      and authority['Root_projection_acceptance']==prior['Root_projection_acceptance']
          ==plan['context']['Root_projection_acceptance']
      and authority['Root_unresolved_selector']==result['selector']==prior['selector']==carrier['selector'],
      'same historical original domain/projection/selector; no current-unpaid reinterpretation')
 for left,right in[(authority['independent_direct_result'],plan['historical_result']),
                   (result['plan'],plan['historical_plan']),
                   (authority['supplied_carrier'],plan['carrier']),
                   (prior['records'],plan['carrier']),
                   (authority['direct_checker'],plan['literal_arithmetic_parent']),
                   (result['program'],plan['literal_arithmetic_parent']),
                   (authority['theorem'],plan['theorem']),
                   (authority['theorem_review'],plan['theorem_review']),
                   (result['theorem'],plan['theorem']),
                   (result['theorem_review'],plan['theorem_review']),
                   (prior['theorem'],plan['theorem']),
                   (prior['theorem_review'],plan['theorem_review'])]:
  same_mapped_object(budget,left,right)
 positions=[row[0]for row in carrier['records']]
 need(positions==plan['expected_positions']==authority['verified_IP_failure_positions']
      ==result['verified_IP_failure_positions']==prior['expected_positive_positions']
      and len(positions)==plan['expected_count']==authority['newly_settled_positions']
      and type(plan['expected_count'])is int and 1<=plan['expected_count']<=1024
      and all(type(i)is int for i in prior['selected_positions'])
      and set(positions)<=set(prior['selected_positions']),
      'all and only complete adopted original positions, with no subset or extra carrier rows')
 return positions

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
      and not sys.flags.optimize and all(k not in os.environ for k in ENV4),'minimal EBS/ENV4 interpreter')
 signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('125s portable integer-word batch')))
 signal.setitimer(signal.ITIMER_REAL,max(.001,125-(time.monotonic()-START)))
 parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--corpus-root',required=True)
 parser.add_argument('--plan',required=True);parser.add_argument('--plan-sha256',required=True)
 parser.add_argument('--self-sha256',required=True);args=parser.parse_args()
 root=Path(args.corpus_root);budget=Budget(root);own=Path(__file__).resolve(strict=True)
 need(own.is_relative_to(root),'new checker Source inside explicit corpus')
 ownref=dict(path=str(own.relative_to(root)),bytes=own.stat().st_size,sha256=args.self_sha256)
 need(ownref['bytes']<=65536,'bounded new checker Source');budget.bytes+=ownref['bytes']+4;budget.physical(ownref)
 planpath=root/relative(args.plan);planref=dict(path=args.plan,bytes=planpath.stat().st_size,sha256=args.plan_sha256)
 need(planref['bytes']<=65536,'bounded separate portable batch plan');plan=decode(budget.physical(planref))
 need(plan['schema']=='Q11_PORTABLE_ADOPTED_TWO_WORD_BATCH_PLAN_V1' and plan['program']==ownref
      and plan['Root_execution_authority_granted']is False,
      'new standalone mathematical replay; no historical caller or Root gate identity')
 need(plan['literal_arithmetic_parent']['sha256']==PARENT_SHA,'exact old9f context/arithmetic parent')
 budget.bind(plan['reference_map'])
 expected={str(relative(row['relative'])):dict(path=str(relative(row['relative'])),
           bytes=row['original']['bytes'],sha256=row['original']['sha256'])for row in plan['reference_map']}
 for row in plan['reference_map']:
  need(expected[str(relative(row['relative']))]['bytes']==row['original']['bytes']
       and expected[str(relative(row['relative']))]['sha256']==row['original']['sha256'],
       'one complete version per declared physical corpus object')
 for r in(ownref,planref):
  need(expected.get(r['path'],r)==r,'one whole Source/plan physical identity');expected[r['path']]=r
 need(len(expected)<=96 and ownref['bytes']+4+2*sum(r['bytes']for r in expected.values())<=8*2**20,
      'prepaid complete first/final relative closure plus interpreter Source reserve')
 for row in plan['reference_map']:budget.read(row['original'])
 budget.read(plan['literal_arithmetic_parent'])
 need(plan['theorem']['sha256']==THEOREM_SHA and plan['theorem_review']['sha256']==THEOREM_REVIEW_SHA,
      'exact retained written theorem and classified-end premises')
 budget.read(plan['theorem']);review=budget.doc(plan['theorem_review'])
 need(review['root']=='/root' and review['blockers']==[]
      and review['status']=='SUPPORTED_WRITTEN_THEOREM_AND_EXACT27_APPLICATIONS',
      'borrowed reviewed written theorem; never a new case verdict')
 authority=budget.doc(plan['existing_adoption']);result=budget.doc(plan['historical_result'])
 prior=historical_plan(plan['historical_plan'],budget)
 carrier=supplied_index_carrier(budget.read(plan['carrier']),plan)
 positions=validate_historical_subject(plan,authority,result,prior,carrier,budget)
 context_value=context(plan['context'],budget)
 verified,members=verify_records(carrier['records'],positions,context_value,budget)
 need(verified==positions and members==result['borrowed_original_members'],
      'complete fresh original-mark word checks and full original member weight')
 need(budget.refs==expected,'every actual physical read is in the explicit relative closure')
 budget.recheck();budget.tick()
 print(json.dumps(dict(schema='Q11_PORTABLE_ADOPTED_TWO_WORD_BATCH_RESULT_V1',status='VERIFIED_ARCHIVED_TWO_END37_BATCH',
  program=ownref,plan=planref,existing_adoption=plan['existing_adoption'],historical_result=plan['historical_result'],
  exact_carrier=plan['carrier'],verified_IP_failure_positions=verified,verified_count=len(verified),borrowed_original_members=members,
  literal_arithmetic_parent=plan['literal_arithmetic_parent'],model_and_classification_premises_imported=True,
  active_original_machine_path_reads=0,word_search_or_row_reduction_calls=0,prior_Source_or_caller_identity_claim=False,
  new_Root_adoption_or_selector_issued=False,whole_original_conjecture_Lean_or_measurement_credit=0,
  resources=dict(matrix_products=budget.products,row_images=budget.row_images,
                 physical_read_bytes_including_bootstrap_reserve=budget.bytes,physical_paths=len(budget.refs),peak_RSS=budget.peak),
  qualification='Fresh original-mark integer-word powers under exact imported faithfulG2/model/member/frame and classified-end premises. All historical runtime/Root proof bodies are archival provenance; this new Source does not rerun them, transfer their execution identity,change a paid ledger or close an Original.'),sort_keys=True))

if __name__=='__main__':main()
