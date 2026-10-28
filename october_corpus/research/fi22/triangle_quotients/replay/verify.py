"""UNRUN relative replay of the acquired Fi22 finite-quotient formulas.
New interface author /root/compact_proof_author. The finite kernel below
is borrowed literally from /root/prime_theory_audit, full parent767df337.
No old caller, Owner, Source4 or named-model acquisition is represented.
Only already supplied finite arrays and certificate slices are checked.
"""
import time
START=time.monotonic()
import argparse,hashlib,json,math,os,resource,signal,stat,struct,sys
from pathlib import Path,PurePosixPath
N=500178
MISSING=4294967295
ENV4=('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')

def need(ok,why):
 if not ok:raise ValueError(why)

def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'unique JSON key');out[k]=v
  return out
 def finite(text):
  v=float(text);need(math.isfinite(v),'finite JSON');return v
 return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:(_ for _ in()).throw(ValueError('finite JSON')))

def relative(text):
 need(type(text)is str and text and text.isascii(),'literal relative path')
 p=PurePosixPath(text);need(not p.is_absolute()and str(p)==text
  and not set(p.parts)&{'.','..','.git','__pycache__','.lake'},'relative corpus input only')
 return Path(*p.parts)

def identity(r):
 need(type(r)is dict and set(r)=={'path','bytes','sha256'}and type(r['path'])is str
  and type(r['bytes'])is int and 0<=r['bytes']<=2**21
  and type(r['sha256'])is str and len(r['sha256'])==64
  and set(r['sha256'])<=set('0123456789abcdef'),'whole bounded content descriptor')
 return(r['path'],r['bytes'],r['sha256'])

class Budget:
 def __init__(self,root):
  need(root.is_absolute()and root.resolve(strict=True)==root,'explicit canonical corpus root')
  self.root=root;self.refs={};self.cache={};self.bytes=0;self.peak=0;self.work=None
 def tick(self):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  self.peak=max(self.peak,rss);need(rss<128*2**20 and time.monotonic()-START<140,'128MiB140s ordinary envelope')
 def physical(self,r,again=False):
  self.tick();identity(r);name=str(relative(r['path']))
  need(self.refs.get(name,r)==r,'one physical identity')
  if name in self.cache and not again:return self.cache[name]
  need(self.bytes+r['bytes']<=8*2**20 and(name in self.refs or len(self.refs)<32),'8MiB32paths full physical read cap')
  p=self.root/relative(name);a=p.lstat()
  need(p.resolve(strict=True)==p and p.is_relative_to(self.root)and stat.S_ISREG(a.st_mode)
   and a.st_nlink==1 and a.st_size==r['bytes'],'canonical ordinary single-link relative file')
  with p.open('rb')as f:b=os.fstat(f.fileno());raw=f.read(r['bytes']+1);c=os.fstat(f.fileno())
  sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
  need(sig(a)==sig(b)==sig(c)==sig(p.lstat())and len(raw)==r['bytes']
   and hashlib.sha256(raw).hexdigest()==r['sha256'],'fresh whole relative input bytes')
  self.refs[name]=dict(r);self.cache[name]=raw;self.bytes+=len(raw);return raw
 def mapped(self,binding):
  need(type(binding)is dict and set(binding)=={'original','relative'},'explicit full original-to-relative binding')
  old=binding['original'];identity(old)
  return self.physical(dict(path=binding['relative'],bytes=old['bytes'],sha256=old['sha256']))
 def final(self):
  for r in list(self.refs.values()):self.physical(r,True)
  self.tick()

class Work:
 def __init__(self,budget):self.budget=budget;self.units=0;self.start=time.monotonic()
 def charge(self,count,role):
  need(type(count)is int and count>=0 and type(role)is str,'explicit nonnegative finite work charge')
  self.units+=count;self.budget.tick()
  need(self.units<=10000000 and time.monotonic()-self.start<20,'10M units20s strict Saved mathematical envelope')
class View:
    def __init__(self,raw,n,width,need,work,nullable=False):
        need(type(raw)is bytes and type(n)is int and n>0 and width in(2,4)
             and len(raw)==n*width and sys.byteorder=='little','whole explicit little-host typed owner-map field')
        # Charge every imported byte although cast itself makes no full copy.
        work.charge(len(raw),'entire_acquired_typed_map_bytes')
        self.data=memoryview(raw).cast('H'if width==2 else'I')
        need(self.data.readonly and self.data.itemsize==width and len(self.data)==n,'read-only native view, no rich integer list')
        self.n,self.need,self.work,self.nullable=n,need,work,nullable
    def get(self,i,allow_missing=False):
        self.need(type(i)is int and 0<=i<self.n,'typed exact original owner index')
        self.work.charge(4,'direct_readonly_owner_map_scalar')
        v=self.data[i]
        self.need((allow_missing and self.nullable and v==MISSING)or 0<=v<self.n,
                  'typed actual owner target, no guessed sentinel');return v
    def value(self,i,cap):
        self.need(type(i)is int and 0<=i<self.n,'typed original mass index')
        self.work.charge(4,'direct_readonly_mass_scalar');v=self.data[i]
        self.need(0<=v<=cap,'whole bounded actual orbit mass');return v

def interval(start,stop,n,limit,need,work):
    work.charge(16,'whole_finite_classification_interval')
    need(type(start)is type(stop)is int and 0<=start<stop<=n and stop-start<=limit,
         'exact bounded classification slice')

def s3_row(s,t,i,need,work):
    # Right-action representatives 1,s,t,st,ts,sts. Relations are checked
    # at every original i across the complete certified family.
    a=s.get(i);b=t.get(i);ab=t.get(a);ba=s.get(b);aba=s.get(ab)
    need(s.get(a)==i and t.get(b)==i and t.get(ba)==aba,
         'both involutions and exact braid relation at this original owner')
    work.charge(48,'six_exact_S3_images_and_canonical_minimum')
    images=(i,a,b,ab,ba,aba);distinct=set(images)
    need(len(distinct)in(3,6),'original2-group B permits only3- or6-owner unordered fibres')
    return min(images),len(distinct)

def resolve_row(minimum,partner_raw,i,need,work):
    work.charge(48,'whole_unordered_partner_resolution')
    m=minimum.get(i);need(minimum.get(m)==m,'accepted canonical minimum is idempotent')
    raw=partner_raw.get(i,allow_missing=True)
    if m!=i:
        need(raw==MISSING,'no invented ordered partner lift outside unordered representatives')
        return MISSING,0
    need(raw!=MISSING,'every original unordered owner has a separately checked partner witness')
    target=minimum.get(raw);need(minimum.get(target)==target,'actual target unordered owner')
    back_raw=partner_raw.get(target,allow_missing=True)
    need(back_raw!=MISSING and minimum.get(back_raw)==i,'whole induced partner involution')
    return target,1 if target==i else 2

def mass_row(partner,masses,i,need,work):
    work.charge(48,'whole_partner_component_mass_formula')
    target=partner.get(i,allow_missing=True);m=masses.value(i,1024)
    if target==MISSING:
        need(m==0,'noncanonical raw owners carry no duplicate unordered mass');return 0,0
    need(partner.get(target,allow_missing=True)==i and m>0 and masses.value(target,1024)==m,
         'same whole unordered B mass on both partner owners')
    if i>target:return 0,0
    size=1 if target==i else 2
    need((size*m)%2==0,'exact product mass integrality, including fixed partner owners')
    value=size*m//2;need(0<value<=1024,'actual product B orbit mass')
    return value,size

def prepare(raw_left,raw_right,stage,n,need,work):
    need(stage in('s3-minimum','partner-resolution','product-mass'),'finite mathematical quotient stage')
    left=View(raw_left,n,4,need,work,nullable=stage=='product-mass')
    right=View(raw_right,n,2 if stage=='product-mass'else 4,need,work,nullable=stage=='partner-resolution')
    return left,right

def row(left,right,stage,i,need,work):
    if stage=='s3-minimum':return s3_row(left,right,i,need,work)
    if stage=='partner-resolution':return resolve_row(left,right,i,need,work)
    return mass_row(left,right,i,need,work)

def verify(left,right,stage,start,stop,raw,need,work):
    limit=32768 if stage=='product-mass'else 16384;width=2 if stage=='product-mass'else 4
    interval(start,stop,left.n,limit,need,work)
    need(type(raw)is bytes and len(raw)==width*(stop-start),'entire supplied typed quotient certificate')
    data=memoryview(raw).cast('H'if width==2 else'I');need(data.readonly,'supplied immutable typed view')
    selected=bytearray();count=0;total=0;fixed=0
    for at,i in enumerate(range(start,stop)):
        v,size=row(left,right,stage,i,need,work);work.charge(4,'whole_supplied_quotient_cell')
        need(data[at]==v,'every exact supplied quotient value independently recomputed')
        if stage=='s3-minimum'and v==i:
            selected.extend(struct.pack('<IB',i,size));work.charge(5,'certified_unordered_representative_record');count+=1
        elif stage=='partner-resolution'and v!=MISSING and i<=v:
            selected.extend(struct.pack('<IB',i,size));work.charge(5,'certified_product_representative_record');count+=1;fixed+=int(size==1)
        elif stage=='product-mass'and v:
            selected.extend(struct.pack('<IH',i,v));work.charge(6,'certified_product_mass_record');count+=1;total+=v
    facts=dict(start=start,stop=stop,rows=stop-start,selected_representatives=count,
      selected_product_mass=total,fixed_partner_components=fixed,
      global_cover_and_global_assembly_still_required=True,all_nonfree_branches_retained=True)
    if stage=='s3-minimum':facts['global_relations_required_for_orbit_minimum_theorem']=True
    work.charge(len(selected),'whole_certified_record_copy');return bytes(selected),facts

SCOPE='7795d9d9d4bbf392cb5a943053372149950eef15d4bd468a63e0cc41f5fcce3a'
KERNEL_SHA='767df337ae79071778e19a43a5407098986c1bfc0e4779e7c2f902273cdefbbc'

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
  and not sys.flags.optimize and all(k not in os.environ for k in ENV4),'minimal EBS/ENV4 interpreter')
 signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('140s relative finite replay')))
 signal.setitimer(signal.ITIMER_REAL,max(.001,140-(time.monotonic()-START)))
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--corpus-root',required=True)
 ap.add_argument('--plan',required=True);ap.add_argument('--plan-sha256',required=True)
 ap.add_argument('--self-sha256',required=True);ap.add_argument('--stage',required=True,
  choices=['s3-minimum','partner-resolution','product-mass']);ap.add_argument('--part',type=int,required=True)
 a=ap.parse_args();root=Path(a.corpus_root);budget=Budget(root);own=Path(__file__).resolve(strict=True)
 need(own.is_relative_to(root),'new replay Source inside corpus')
 ownref=dict(path=str(own.relative_to(root)),bytes=own.stat().st_size,sha256=a.self_sha256)
 need(ownref['bytes']<=50000,'full mathematical namespace Source <=50k bytes')
 budget.bytes+=ownref['bytes']+4;budget.physical(ownref)
 path=root/relative(a.plan);pr=dict(path=a.plan,bytes=path.stat().st_size,sha256=a.plan_sha256)
 need(pr['bytes']<=65536,'bounded generic plan');plan=decode(budget.physical(pr))
 need(plan['schema']=='PORTABLE_FI22_FINITE_REPLAY_PLAN_V1'and plan['program']==ownref
  and plan['Root_execution_authority_granted']is False and plan['scope_digest']==SCOPE,
  'new truthful standalone finite Source; no inherited caller/verdict identity')
 stage=plan['stages'][a.stage];parts=stage['parts']
 need(type(a.part)is int and 1<=a.part<=len(parts),'one exact finite part')
 last=0
 for index,item in enumerate(parts,1):
  need(item['index']==index and item['start']==last and type(item['stop'])is int
   and last<item['stop']<=N and item['stop']-last<=(32768 if a.stage=='product-mass'else 16384),
   'complete bounded disjoint stage interval partition')
  last=item['stop']
 need(last==N,'all original500178 rows covered by the generic plan')
 part=parts[a.part-1];parent=stage['kernel_parent'];parent_raw=budget.mapped(parent)
 need(parent['original']['sha256']==KERNEL_SHA,'exact literal finite-kernel parent')
 adoption=decode(budget.mapped(stage['root_adoption']));accepted=decode(budget.mapped(stage['stage_adoption']))
 family=decode(budget.mapped(stage['original_family_plan']))
 need(adoption['root']==accepted['root']=='/root'and adoption['adopted']is accepted['adopted']is True
  and adoption['scope_digest']==accepted['scope_digest']==plan['scope_digest']
  and adoption['stage_acceptance']==stage['stage_adoption']['original']
  and accepted['family_plan']==stage['original_family_plan']['original']
  and family['scope_digest']==plan['scope_digest']
  and family['program']==accepted['program']
  and accepted['stage']==family['stage']==a.stage and family['owners']==accepted['original_owners']==N
  and adoption.get('original_owners',adoption.get('ordered_owners'))==N
  and family['left']==stage['left']['original']and family['right']==stage['right']['original']
  and family['kernel']==parent['original']and accepted['kernel']==parent['original']
  and accepted['all_nonfree_branches_retained']is True,
  'whole actual fixed-scope operands and conditional acquisition provenance remain joined')
 raw_left=budget.mapped(stage['left']);raw_right=budget.mapped(stage['right'])
 supplied=budget.physical(part['certificate']);work=Work(budget)
 left,right=prepare(raw_left,raw_right,a.stage,N,need,work)
 selected,facts=verify(left,right,a.stage,part['start'],part['stop'],supplied,need,work)
 need(len(selected)==part['selected_records']['bytes']
  and hashlib.sha256(selected).hexdigest()==part['selected_records']['sha256'],
  'whole finite selected-record bytes match the exact published interval projection')
 budget.final()
 print(json.dumps(dict(schema='PORTABLE_FI22_FINITE_REPLAY_PART_V1',status='VERIFIED_FINITE_PART',program=ownref,plan=pr,
  stage=a.stage,index=a.part,scope_digest=SCOPE,certificate=part['certificate'],facts=facts,
  selected_records=dict(bytes=len(selected),sha256=hashlib.sha256(selected).hexdigest()),
  resources=dict(physical_read_bytes=budget.bytes,paths=len(budget.refs),work_units=work.units,peak_RSS=budget.peak),
  imported_model_Reader_word_graph_class_two_fibre_H_B_and_input_map_meaning_retained=True,
  original_group_point_graph_or_word_actions=0,prior_caller_or_Source_identity_claim=False,
  full_stage_completion_owed=True,whole_original_conjecture_Lean_or_compression_credit=0,
  qualification='Literal finite formulas only, on whole acquired relative arrays and supplied exact certificate slices. A separate complete-part join is required; original geometric/model premises are imports.'),sort_keys=True))

if __name__=='__main__':main()
