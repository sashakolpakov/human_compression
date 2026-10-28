"""Join actual bounded relative arithmetic runs; no mathematical source execution."""
import argparse,hashlib,json,os,resource,stat,sys,time
from pathlib import Path
START=time.monotonic();READ=0;REFS={}
def need(ok,why):
    if not ok:raise ValueError(why)
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    if rss>=128*2**20 or time.monotonic()-START>=90:raise RuntimeError('128MiB90s metadata join')
def read(p,cap=131072):
    global READ
    p=Path(p);a=p.lstat()
    need(p.is_absolute() and p.resolve(strict=True)==p and stat.S_ISREG(a.st_mode) and a.st_nlink==1 and a.st_size<=cap,'bounded ordinary metadata')
    need(READ+a.st_size<=32*2**20 and (str(p)in REFS or len(REFS)<1024),'32MiB1024paths including rereads')
    with p.open('rb')as f:b=os.fstat(f.fileno());raw=f.read(cap+1);c=os.fstat(f.fileno())
    sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(sig(a)==sig(b)==sig(c)==sig(p.lstat()) and len(raw)==a.st_size,'whole stable metadata')
    r=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());need(REFS.get(str(p),r)==r,'one whole input identity');REFS[str(p)]=r;READ+=len(raw)
    return raw,r
def doc(p,cap=131072):
    raw,r=read(p,cap)
    def pairs(xs):
        out={}
        for k,v in xs:need(k not in out,'unique metadata keys');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs),r
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--runs',required=True);ap.add_argument('--recipe',required=True);ap.add_argument('--corpus-root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    base=Path(a.runs);root=Path(a.corpus_root);recipe,recipe_ref=doc(a.recipe)
    plan,planref=doc(root/'research/fi22/triangle_quotients/replay/plan.json',65536)
    program=dict(path='research/fi22/triangle_quotients/replay/verify.py',bytes=14623,sha256='be99b562182debe898d86b53c68540d10ef8e4303e1b40233e3941b5681f6af3')
    need(plan['program']==program and planref['sha256']=='ab3d1cf464274a2745057560c9b5a3ff9732c62cadeaf1e9230a81e2e87e47b4','whole final reviewed source/plan')
    totals={k:dict(parts=0,rows=0,selected=0,mass=0,fixed=0)for k in plan['stages']};runs=[]
    for item in recipe['parts']:
        stage,index=item['stage'],item['index'];part=plan['stages'][stage]['parts'][index-1]
        label='fi22_'+stage.replace('-','_')+'_'+str(index).zfill(4);directory=base/'guards'/label
        result,rref=doc(directory/'stdout.log');guard,gref=doc(directory/'receipt.json');started,sref=doc(directory/'started.json');capture,cref=doc(base/'captures'/(label+'.json'));stderr,eref=read(directory/'stderr.log')
        command=[sys.executable if x=='python3'else x.replace('/ABS/october_corpus',str(root))for x in item['argv']]
        need(guard['status']=='PASS' and guard['stop']=='RETURNED' and guard['returncode']==0 and guard['error']is None and guard['command']==started['command']==command,'actual successful exact guarded command')
        need(guard['cleanup']['remaining']==guard['cleanup']['errors']==[] and guard['limits']['total_rss']==256*2**20 and guard['limits']['wall_seconds']==150 and not stderr,'unchanged bounded closed run')
        frames=capture['all_genuine_api_frames'];issued=capture['issued_argv']
        need(capture['root']==capture['actor']=='/root' and capture['actual_tool']['exit_code']==0 and frames and frames[-1]['exit_code']==0 and 'session_id'not in frames[-1] and issued==capture['child_argv'] and issued.count('--')==1 and issued[issued.index('--')+1:]==command,'genuine complete original transport')
        actual=json.loads(''.join(f['output']for f in frames))
        need(actual['status']=='PASS'and actual['receipt']==str(directory/'receipt.json'),'actual tool report names exact guard')
        expected_plan=dict(planref,path='research/fi22/triangle_quotients/replay/plan.json')
        need(result['schema']=='PORTABLE_FI22_FINITE_REPLAY_PART_V1'and result['status']=='VERIFIED_FINITE_PART'and result['program']==program and result['plan']==expected_plan and result['scope_digest']==plan['scope_digest']and result['stage']==stage and result['index']==index,'whole exact same scope/source/plan/part')
        f=result['facts'];need(f['start']==item['start']==part['start']and f['stop']==item['stop']==part['stop']and f['rows']==f['stop']-f['start']and result['certificate']==part['certificate']and result['selected_records']==part['selected_records'],'exact interval and independently recomputed record bytes')
        need(result['imported_model_Reader_word_graph_class_two_fibre_H_B_and_input_map_meaning_retained']is True and result['original_group_point_graph_or_word_actions']==0 and result['prior_caller_or_Source_identity_claim']is False and result['whole_original_conjecture_Lean_or_compression_credit']==0,'qualified arithmetic scope only')
        t=totals[stage];need(f['start']==t['rows']and index==t['parts']+1,'complete ordered gap-free disjoint intervals')
        for k,v in [('parts',1),('rows',f['rows']),('selected',f['selected_representatives']),('mass',f['selected_product_mass']),('fixed',f['fixed_partner_components'])]:t[k]+=v
        runs.append(dict(stage=stage,index=index,result=rref,guard=gref,started=sref,capture=cref,stderr=eref))
    need(len(runs)==78 and totals['s3-minimum']==dict(parts=31,rows=500178,selected=89069,mass=0,fixed=0)and totals['partner-resolution']==dict(parts=31,rows=500178,selected=46596,mass=0,fixed=4123)and totals['product-mass']==dict(parts=16,rows=500178,selected=46596,mass=36486450,fixed=0),'exact complete finite totals; mass stage does not recount fixed owners')
    need(4123+2*(46596-4123)==89069,'fixed/exchanged partner identities')
    output=dict(schema='ROOT_COMPLETE_RELATIVE_FI22_ARITHMETIC_REPLAY_V1',root='/root',status='VERIFIED_ALL_78_FINITE_PARTS_UNDER_IMPORTED_PREMISES',program=program,plan=expected_plan,scope_digest=plan['scope_digest'],totals=totals,exchanged_partner_components=42473,runs=runs,metadata_physical_read_bytes=READ,original_conjecture_Lean_or_compression_credit=0,qualification='Fresh finite arithmetic rechecked only. Original model/Reader/action/word/graph/class/two-fibre/H=B and input-map meanings remain imports. No generation, reversal, other endpoint or full original is established.')
    p=Path(a.out);need(p.is_absolute()and p.is_relative_to('/private/tmp')and not p.exists(),'fresh temporary metadata output')
    raw=(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n').encode()
    with p.open('xb')as f:f.write(raw)
    print(json.dumps(dict(status=output['status'],report=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),totals=totals,physical_metadata_read_bytes=READ,scientific_calls=0),sort_keys=True))
if __name__=='__main__':main()
