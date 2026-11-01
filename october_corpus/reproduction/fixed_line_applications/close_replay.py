"""Join three mechanical replays; the group-model and cover remain imports."""
import hashlib,json,math,os,resource,stat,sys,time
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def can(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def unique(rows):
    out={}
    for k,v in rows:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out

def decode(raw):
    def bad(x):raise ValueError('nonfinite JSON constant')
    value=json.loads(raw,object_pairs_hook=unique,parse_constant=bad)
    def check(item,path=()):
        if type(item)is float:
            need(path==('counts','elapsed_seconds')and math.isfinite(item)and item>=0,
                 'only finite nonnegative elapsed timing may be floating point')
        elif type(item)is dict:
            for key,child in item.items():check(child,path+(key,))
        elif type(item)is list:
            for index,child in enumerate(item):check(child,path+(index,))
    check(value)
    return value

class Inputs:
    def __init__(self):self.bytes=0;self.pins={};self.started=time.monotonic()
    def tick(self):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
        need(time.monotonic()-self.started<90 and rss<112*2**20,'90s/112MiB cooperative join limit')
    def read(self,path):
        self.tick()
        path=Path(path).absolute();a=path.lstat()
        need(path.resolve(strict=True)==path and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and 0<a.st_size<=262144,'bounded ordinary role artifact')
        need(self.bytes+a.st_size<=8388608 and len(self.pins|{str(path):None})<=96,'one8MiB/96path join bank')
        signature=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        with path.open('rb')as f:
            q=os.fstat(f.fileno());raw=f.read(a.st_size+1);z=os.fstat(f.fileno())
        need(signature(a)==signature(q)==signature(z)==signature(path.lstat())and len(raw)==a.st_size,'whole stable artifact')
        self.bytes+=len(raw);pin=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        need(str(path)not in self.pins or self.pins[str(path)]==pin,'one artifact version')
        self.pins[str(path)]=pin;return raw
    def doc(self,path):return decode(self.read(path))

def joined(binding,acquired,wjob,wproof,wresult,rjob,rproof,rresult):
    need(type(binding)is dict and set(binding)=={'schema','original_job','position','representative_J_index','end','end_id'}
         and binding['schema']=='F004_FIXED_LINE_PORTABLE_CASE_V1'and binding['original_job']==[24,4], 'explicit selected case metadata')
    position=binding['position'];representative=binding['representative_J_index'];end=binding['end']
    need(type(position)is int and 1<=position<=3779 and type(representative)is int and 1<=representative<=14763
         and end in('left','right')and binding['end_id']=='position%04d_%s'%(position,end),'typed original/end identity')
    labels,omitted=([0,1,2],3)if end=='left'else([1,2,3],0)
    need(acquired['schema']=='F004_FIXED_LINE_ORIGINAL_REPLAY_V1'and acquired['original_job']==[24,4]
         and type(acquired['position'])is int and acquired['position']==position
         and type(acquired['representative_J_index'])is int and acquired['representative_J_index']==representative
         and acquired['status']=='ORIGINAL_QUARTET_RECONSTRUCTED_ONLY','same freshly reconstructed original')
    marks=acquired['marks'];need(type(marks)is list and len(marks)==4,'whole original quartet')
    need(hashlib.sha256(can(marks)).hexdigest()==acquired['marks_sha256'],'acquired original mark digest')
    need(wjob['schema']=='F004_ORDER19_FIXED_SEED_CONSUMER_V1'and rjob['schema']=='F004_ORDER19_REACHABILITY_CONSUMER_V1','exact component job schemas')
    need(wproof['schema']=='F004_ORDER19_FIXED_SEED_CONSUMER_PROOF_V1'and rproof['schema']=='F004_ORDER19_REACHABILITY_CONSUMER_PROOF_V1','exact independent proof schemas')
    need(wresult['schema']=='F004_ORDER19_FIXED_SEED_CONSUMER_RESULT_V1'and rresult['schema']=='F004_ORDER19_REACHABILITY_CONSUMER_RESULT_V1','exact result schemas')
    triple=marks[:3]if end=='left'else marks[1:]
    need(triple==wjob['end_marks']==rjob['end_marks'],'both actual ordered triples equal this original/end reconstruction')
    need(wjob['end_id']==rjob['end_id']==wproof['end_id']==rproof['end_id']==binding['end_id'],'one ordered end identity')
    wa=wresult['answer'];ra=rresult['answer'];cert=wjob['certificate']
    need(wproof['certificate']==cert and rproof['certificate']==rjob['certificate'],'same whole supplied certificates')
    need(cert['word']==rjob['word']==wa['word']and cert['seed']==rjob['seed']==wa['selected_seed'],'same actual word and nonzero seed across roles')
    need(wa['status']=='VERIFIED_END_WORD_ORDER19_AND_FIXED_SEED_ONLY'and type(wa['fixed_dimension'])is int and wa['fixed_dimension']==1 and type(wa['exact_prime_order'])is int and wa['exact_prime_order']==19,'verified complete one-dimensional fixed kernel and prime order')
    need(ra['status']=='VERIFIED_9241_REACHABLE_AND_ORDER19_STABILIZER_ONLY'and type(ra['reachable_distinct'])is int and ra['reachable_distinct']==9241 and type(ra['parent_images_verified'])is int and ra['parent_images_verified']==9240 and ra['concrete_end_order_lower_bound']==175579,'dedicated strict9241 replay, never a storage-cap result')
    need(wproof['supplier_or_solver_imported']is False and rproof['supplier_discovery_or_solver_imported']is False,'independent consumer roles')
    return dict(position=position,representative_J_index=representative,end=end.upper(),end_labels=labels,omitted_label=omitted,
        fixed_dimension=1,exact_prime_order=19,reachable_distinct=9241,parent_images_verified=9240,
        end_order_lower_bound=175579,conditional_conclusion=end.upper()+'_EQUALS_G2_11_AND_ORIGINAL_MARKING_FAILS_IP',
        imported_premises=['named faithful original G2(11) model, indexed membership and natural row frame',
            'every proper order19 overgroup preserves a rational line or lies in J1 of order175560'],
        Root_authority=False,new_case_original_Lean_or_conjecture_credit=0)

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'require-E-B-S/no-O')
    need(len(sys.argv)==7,'acquisition-proof word-output reach-output case-directory common-verifier-root fresh-output')
    a,w,r,case,common,out=map(Path,sys.argv[1:]);b=Inputs()
    binding=b.doc(case/'case.json')
    refs=[a,case/'word_job.json',w/'proof.json',w/'result.json',case/'reachable_job.json',r/'proof.json',r/'result.json']
    docs=[b.doc(p)for p in refs]
    need(docs[2]['input_pins']['job_sha256']==b.pins[str(refs[1].absolute())]['sha256']and docs[5]['input_pins']['job_sha256']==b.pins[str(refs[4].absolute())]['sha256'],'exact job hashes in actual independent outputs')
    manifests=[b.read(common/name/'source_manifest.json')for name in('word19','reachable')]
    need(all(proof['input_pins']['manifest_sha256']==hashlib.sha256(raw).hexdigest()for proof,raw in zip((docs[2],docs[5]),manifests)),'same whole component Source manifests')
    answer=joined(binding,*docs)
    for path,pin in list(b.pins.items()):b.read(path);need(b.pins[path]==pin,'all final artifact hashes stable')
    out=out.absolute();need(out.parent.resolve(strict=True)==out.parent and not out.exists(),'fresh bounded join output')
    body=can(dict(schema='F004_FIXED_LINE_PORTABLE_JOIN_V1',answer=answer,inputs=b.pins,read_bytes=b.bytes))+b'\n'
    need(len(body)<=131072,'128KiB join output');out.mkdir()
    with(out/'result.json').open('xb')as f:f.write(body)
    b.tick()
    print(can(answer).decode())

if __name__=='__main__':main()
