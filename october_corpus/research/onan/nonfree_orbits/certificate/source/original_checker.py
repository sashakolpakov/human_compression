"""Finite index/literal-family/overlap checker; stdlib only, no group arithmetic.

Source author Final. This is a NEW orbit-stabilizer family proof boundary,
not a claim that a historical worker, producer or Saved processed these rows.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys

R=Path(__file__).resolve().parent
N=2857239
ORDERS=(256,144)
STATUSES=('GENERATING','NONGENERATING_NONFREE','NONGENERATING_INVARIANT_SET','UNPAID','UNTRIED')
OPENED={}


def need(ok,why):
    if not ok:raise ValueError(why)


def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def pin(path):
    p=Path(path);a=p.stat();need(p.is_absolute()and p.resolve(strict=True)==p and p.is_file()and not p.is_symlink(),'canonical whole ordinary file')
    need(a.st_size<=8*2**20,'bounded input8MiB');h=hashlib.sha256();size=0
    with p.open('rb')as f:
        q=os.fstat(f.fileno())
        for raw in iter(lambda:f.read(2**20),b''):h.update(raw);size+=len(raw)
        z=os.fstat(f.fileno())
    sig=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(sig(a)==sig(q)==sig(z)==sig(p.stat())and size==a.st_size,'whole stable byte pin')
    ref=dict(path=str(p),bytes=size,sha256=h.hexdigest());need(OPENED.get(str(p),ref)==ref,'same immutable input');OPENED[str(p)]=ref
    return ref


def doc(ref):
    need(type(ref)is dict and set(ref)=={'path','bytes','sha256'}and pin(ref['path'])==ref,'exact whole input pin')
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'unique JSON key');out[k]=v
        return out
    value=json.loads(Path(ref['path']).read_bytes(),object_pairs_hook=pairs,
        parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
    need(pin(ref['path'])==ref,'same entire JSON');return value


def typed_index(v):
    need(set(v)=={'schema','accepted_partitions','representatives','key_bytes','rows','counts','masses','free_counts'}
         and v['schema']=='L026_COMPLETE_GENERATION_REPRESENTATIVE_INDEX_V1'
         and type(v['key_bytes'])is int and v['key_bytes']==9
         and type(v['rows'])is list and len(v['rows'])==v['representatives']==31988,'whole original complete index')
    previous=(0,0);counts=[0,0];masses=[0,0];free=[0,0]
    for row in v['rows']:
        need(type(row)is list and len(row)==4,'exact compact original row');ep,node,w,key=row
        need(type(ep)is type(node)is type(w)is int and ep in(1,2)and 1<=node<=N
             and (ep,node)>previous and 1<=w<=ORDERS[ep-1]and ORDERS[ep-1]%w==0
             and type(key)is str and len(key)==18 and all(x in'0123456789abcdef'for x in key),'typed ordered identity/full key/exact inner weight')
        previous=ep,node;counts[ep-1]+=1;masses[ep-1]+=w;free[ep-1]+=w==ORDERS[ep-1]
    need(counts==v['counts']==[11581,20407]and masses==v['masses']==[N,N]
         and free==v['free_counts']==[10810,19402],'both entire orbit partitions/counts/masses/free histogram')
    return {(r[0],r[1]):r for r in v['rows']}


def typed_ledger(v,index_ref,index,by):
    need(v['schema']=='ROOT_L026_GENERATION_PAID_ROW_LEDGER_V1'and v['root']is v['adopted']is True
         and v['index']==index_ref and v['accepted_partitions']==index['accepted_partitions'],'explicit prior Root ledger of this exact index')
    need(type(v['gates'])is list and len(v['gates'])<=31988,'finite historical batch references')
    paid={};unpaid={}
    for r in v['paid']:
        need(type(r)is list and len(r)==4,'compact paid row');ep,node,status,gate=r
        need(type(ep)is type(node)is type(status)is type(gate)is int and (ep,node)in by
             and (ep,node)not in paid and 0<=status<=2 and 0<=gate<len(v['gates']),'unique typed paid identity/status/evidence')
        paid[ep,node]=status
    for r in v['unpaid']:
        need(type(r)is list and len(r)==3,'compact unresolved row');ep,node,gate=r
        need(type(ep)is type(node)is type(gate)is int and (ep,node)in by and (ep,node)not in paid
             and (ep,node)not in unpaid and 0<=gate<len(v['gates']),'unique typed unresolved identity/evidence')
        unpaid[ep,node]=gate
    need(v['paid']==sorted(v['paid'])and v['unpaid']==sorted(v['unpaid']),'same ordered immutable ledger')
    coverage={str(ep):{s:dict(rows=0,mass=0)for s in STATUSES}for ep in(1,2)}
    for ep,node,w,key in index['rows']:
        k=ep,node;s=STATUSES[paid[k]]if k in paid else'UNPAID'if k in unpaid else'UNTRIED'
        coverage[str(ep)][s]['rows']+=1;coverage[str(ep)][s]['mass']+=w
    need(canonical(v['coverage'])==canonical(coverage)and type(v['complete_generation_census'])is bool
         and v['complete_generation_census']==(len(paid)==31988)and v['Aut_or_IP_counted']is False
         and type(v['whole_original_credit'])is int and v['whole_original_credit']==0,'entire prior ledger coverage and zero global credit')
    return paid,unpaid


def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for key in('index_acceptance','index','certificate','ledger'):
        flag='--'+key.replace('_','-');p.add_argument(flag,type=Path,required=True);p.add_argument(flag+'-sha256',required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary bounded -E-B checker')
    refs={k:pin(getattr(a,k))for k in('index_acceptance','index','certificate','ledger')}
    need(all(r['sha256']==getattr(a,k+'_sha256')for k,r in refs.items()),'literal PATH/SHA inputs')
    freeze=doc(pin(R/'source_freeze.json'));need(freeze['program']==pin(Path(__file__).resolve())
         and freeze['certificate']==refs['certificate']and freeze['argument']==pin(R/'ARGUMENT.rst'),
         'exact frozen new family method/certificate/proof')
    cert=doc(refs['certificate']);gate=doc(refs['index_acceptance']);index=doc(refs['index'])
    need(refs['index_acceptance']==cert['index_acceptance']and refs['index']==cert['index']==gate['index']
         and gate['schema']=='ROOT_ACCEPTED_L026_COMPLETE_REPRESENTATIVE_INDEX_V1'and gate['root']is gate['adopted']is True
         and gate['generation_counted']is False and gate['whole_original_credit']==0,'same genuinely accepted closed index premise, no worker PASS retarget')
    need(gate['accepted_partitions']==index['accepted_partitions']==cert['accepted_partitions']
         and gate['counts']==index['counts']and gate['masses']==index['masses']and gate['free_counts']==index['free_counts'],'whole same accepted partitions/index summaries')
    by=typed_index(index);expected=[r for r in index['rows']if r[2]<ORDERS[r[0]-1]]
    need(cert['schema']=='L026_LITERAL_NONFREE_ORBIT_FAMILY_V1'and canonical(cert['rows'])==canonical(expected)
         and cert['inner_stabilizer_orders']==list(ORDERS)and cert['representative_counts']==index['counts']
         and cert['free_counts']==index['free_counts']and cert['nonfree_counts']==[771,1005]
         and len(expected)==cert['nonfree_representatives']==1776,'ALL and ONLY1776 literal nonfree rows, no clipping or replacement')
    need(Path(refs['certificate']['path']).read_bytes()==canonical(cert),'whole frozen canonical family bytes')
    setup=doc(cert['borrowed_premises']['endpoint_setup'])
    need(setup['root']=='/root'and setup['status']=='ROOT_ACCEPTED_CONDITIONAL_ONAN_ENDPOINT_SETUP'
         and setup['inner_stabilizer_orders']==list(ORDERS)and setup['endpoint_class_sizes']==[630,1120],
         'exact acquired inner endpoint groups, not full-Aut denominators')
    partitions=[doc(r)for r in cert['accepted_partitions'].values()]
    need(all(v['root']is v['adopted']is True and v['native']['complete']is True and v['native']['count']==N for v in partitions)
         and partitions[0]['conditional_chain_premise']==partitions[1]['conditional_chain_premise'],'accepted whole partitions with same retained conditional model premise')
    need(cert['proof_kind']=='ORBIT_STABILIZER_AND_CENTERLESS_NAMED_G'
         and cert['historical_partition_and_named_model_premises_borrowed']is True
         and cert['existing_worker_or_Saved_replayed']is False and cert['Original_Aut_IP_or_census_credit']==0,'honest new mathematical family boundary')
    for r in cert['borrowed_premises'].values():need(pin(r['path'])==r,'whole retained proof premise Source')
    paid,unpaid=typed_ledger(doc(refs['ledger']),refs['index'],index,by)
    overlap=[];unresolved=[];untried=[];new=[];stab=[]
    for row in expected:
        ep,node,w,key=row;k=ep,node;order=ORDERS[ep-1]//w
        need(order>1 and order*w==ORDERS[ep-1],'nontrivial exact orbit stabilizer order')
        stab.append([ep,node,order])
        if k in paid:
            need(paid[k]==1,'prior paid nonfree row must agree; no silent overwrite of conflicting proof');overlap.append(row)
        else:
            new.append(row)
            if k in unpaid:unresolved.append(row)
            else:untried.append(row)
    need(len(overlap)+len(new)==1776 and len(unresolved)+len(untried)==len(new),'complete explicit disjoint overlap/new partition')
    pin(R/'ARGUMENT.rst');rows=sorted(OPENED.values(),key=lambda r:r['path'])
    need(len(rows)<=32 and sum(r['bytes']for r in rows)<=64*2**20,'finite ordinary direct32/64MiB')
    for r in rows:need(pin(r['path'])==r,'fresh whole finite input scope')
    value=dict(schema='VERIFIED_L026_NONFREE_ORBIT_FAMILY_V1',status='VERIFIED_EXACT_NONFREE_ORBIT_FAMILY',
        proof_kind=cert['proof_kind'],index_acceptance=refs['index_acceptance'],index=refs['index'],certificate=refs['certificate'],parent_ledger=refs['ledger'],
        accepted_partitions=index['accepted_partitions'],borrowed_premises=cert['borrowed_premises'],conditional_chain_premise=partitions[0]['conditional_chain_premise'],
        endpoint_orders=list(ORDERS),nonfree_counts=[771,1005],family_rows=expected,stabilizer_orders=stab,
        family_inner_masses=[sum(r[2]for r in expected if r[0]==ep)for ep in(1,2)],
        already_paid_nonfree=overlap,newly_supported=new,previously_unpaid=unresolved,previously_untried=untried,
        family_count=1776,already_paid_count=len(overlap),newly_supported_count=len(new),all_rows_nongenerating_by_centerless_stabilizer=True,
        existing_worker_or_producer_or_Saved_replayed=False,old_actual_status_or_gate_retargeted=False,
        named_centerless_group_and_historical_orbit_premises_borrowed=True,complete_root_admission_inputs=rows,
        ledger_or_gate_or_Current_Status_mutated=False,whole_Original_credit=0,Aut_IP_reversal_census_Lean_measurement_credit=0)
    out=a.out;need(out.is_absolute()and out.parent.resolve(strict=True)==out.parent and not os.path.lexists(out),'fresh canonical result outside existing artifacts')
    raw=canonical(value);need(len(raw)<=8*2**20,'whole finite result8MiB')
    with out.open('xb')as f:need(f.write(raw)==len(raw),'whole exclusive result')
    print(json.dumps(dict(status=value['status'],result=pin(out),family_count=1776,already_paid=len(overlap),newly_supported=len(new),ledger_mutated=False,whole_Original_credit=0),sort_keys=True))


if __name__=='__main__':main()
