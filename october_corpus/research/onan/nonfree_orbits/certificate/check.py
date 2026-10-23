"""Portable finite validation of the1776 L026 nonfree-orbit certificates.

New publication Source adapted by Final from frozen private checker375b5149.
The pure typed-index/ledger validators are attributed copies under new names;
all path resolution, optional-overlap and output behavior is new Source.
No project import, group arithmetic or private absolute-path fallback exists.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys

ROOT=Path(__file__).resolve().parent
N=2857239
ORDERS=(256,144)
STATUSES=('GENERATING','NONGENERATING_NONFREE','NONGENERATING_INVARIANT_SET','UNPAID','UNTRIED')
MAPPING={}
OPENED={}

def need(ok,why):
    if not ok:raise ValueError(why)


def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def verify_index(v):
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


def verify_borrowed_parent(v,index_ref,index,by):
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


def local_pin(p):
    p=Path(p);a=p.stat();h=hashlib.sha256();size=0
    need(p.is_file()and not p.is_symlink()and a.st_size<=8*2**20,'ordinary complete file8MiB')
    with p.open('rb')as f:
        q=os.fstat(f.fileno())
        for raw in iter(lambda:f.read(2**20),b''):h.update(raw);size+=len(raw)
        z=os.fstat(f.fileno())
    sig=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(sig(a)==sig(q)==sig(z)==sig(p.stat())and size==a.st_size,'stable entire bytes')
    return dict(bytes=size,sha256=h.hexdigest())


def package_path(relative):
    need(type(relative)is str and relative and not Path(relative).is_absolute()
         and all(x not in('', '.', '..')for x in relative.split('/')),'strict relative package path')
    p=ROOT
    for part in relative.split('/'):
        p=p/part;need(not p.is_symlink(),'no package symlink')
    need(p.resolve(strict=True).is_relative_to(ROOT),'path stays inside package')
    return p


def strict_json(p):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'unique JSON key');out[k]=v
        return out
    return json.loads(p.read_bytes(),object_pairs_hook=pairs,
        parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))


def mapped_path(ref):
    need(type(ref)is dict and set(ref)=={'path','bytes','sha256'}and ref['path']in MAPPING,
         'source reference must have an explicit portable mapping')
    entry=MAPPING[ref['path']]
    need(ref['bytes']==entry['bytes']and ref['sha256']==entry['sha256'],'same original whole Source pin')
    p=package_path(entry['relative_path']);need(local_pin(p)==dict(bytes=ref['bytes'],sha256=ref['sha256']),
         'whole portable copy equals original pin')
    OPENED[entry['relative_path']]=dict(relative_path=entry['relative_path'],bytes=ref['bytes'],sha256=ref['sha256'])
    return p


def document(ref):
    p=mapped_path(ref);value=strict_json(p);mapped_path(ref);return value


def main():
    global MAPPING
    p=argparse.ArgumentParser(allow_abbrev=False);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--parent-ledger');p.add_argument('--parent-ledger-sha256');a=p.parse_args()
    need((a.parent_ledger is None)==(a.parent_ledger_sha256 is None),'optional borrowed parent needs paired PATH/SHA')
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated ordinary -I-B or -E-B invocation')
    manifest_path=package_path('SourceManifest.json');manifest_pin=local_pin(manifest_path);m=strict_json(manifest_path)
    need(m['schema']=='L026_NONFREE_PUBLIC_SOURCE_MANIFEST_V1','portable Source manifest schema')
    need(m['portable_program']['relative_path']=='check.py'and local_pin(ROOT/'check.py')
         =={k:m['portable_program'][k]for k in('bytes','sha256')},'exact portable checker Source')
    for ref in m['authored_files']:
        need(local_pin(package_path(ref['relative_path']))=={k:ref[k]for k in('bytes','sha256')},
             'whole authored proof/scope/Source derivation bytes')
    MAPPING=m['original_path_map']
    # Authenticate every copied leaf without following unused private JSON refs.
    for original,entry in MAPPING.items():mapped_path(dict(path=original,bytes=entry['bytes'],sha256=entry['sha256']))
    refs=m['inputs'];cert=document(refs['certificate']);gate=document(refs['index_acceptance']);index=document(refs['index'])
    need(refs['index_acceptance']==cert['index_acceptance']and refs['index']==cert['index']==gate['index']
         and gate['schema']=='ROOT_ACCEPTED_L026_COMPLETE_REPRESENTATIVE_INDEX_V1'and gate['root']is gate['adopted']is True
         and gate['generation_counted']is False and gate['whole_original_credit']==0,'same accepted historical index premise')
    need(gate['accepted_partitions']==index['accepted_partitions']==cert['accepted_partitions']
         and gate['counts']==index['counts']and gate['masses']==index['masses']and gate['free_counts']==index['free_counts'],
         'same original partition namespace and summaries')
    by=verify_index(index);family=[r for r in index['rows']if r[2]<ORDERS[r[0]-1]]
    need(cert['schema']=='L026_LITERAL_NONFREE_ORBIT_FAMILY_V1'and canonical(cert['rows'])==canonical(family)
         and cert['inner_stabilizer_orders']==list(ORDERS)and cert['representative_counts']==index['counts']
         and cert['free_counts']==index['free_counts']and cert['nonfree_counts']==[771,1005]
         and len(family)==cert['nonfree_representatives']==1776,'ALL and ONLY exact1776 nonfree records')
    need(mapped_path(refs['certificate']).read_bytes()==canonical(cert),'complete canonical literal family')
    setup=document(cert['borrowed_premises']['endpoint_setup'])
    need(setup['root']=='/root'and setup['status']=='ROOT_ACCEPTED_CONDITIONAL_ONAN_ENDPOINT_SETUP'
         and setup['inner_stabilizer_orders']==list(ORDERS)and setup['endpoint_class_sizes']==[630,1120],
         'borrowed inner pointwise endpoint groups, not Aut denominators')
    parts=[document(cert['accepted_partitions'][k])for k in('t1_acceptance','t2_acceptance')]
    need(all(x['root']is x['adopted']is True and x['native']['complete']is True and x['native']['count']==N for x in parts)
         and parts[0]['conditional_chain_premise']==parts[1]['conditional_chain_premise'],'exact borrowed complete partitions and model qualification')
    need(cert['proof_kind']=='ORBIT_STABILIZER_AND_CENTERLESS_NAMED_G'
         and cert['historical_partition_and_named_model_premises_borrowed']is True
         and cert['existing_worker_or_Saved_replayed']is False and cert['Original_Aut_IP_or_census_credit']==0,'new finite family boundary')
    for ref in cert['borrowed_premises'].values():mapped_path(ref)
    stabilizers=[]
    for ep,node,w,key in family:
        quotient=ORDERS[ep-1]//w;need(quotient>1 and quotient*w==ORDERS[ep-1],'each exact stabilizer order is nontrivial')
        stabilizers.append([ep,node,quotient])
    masses=[sum(r[2]for r in family if r[0]==ep)for ep in(1,2)]
    need(masses==m['expected']['family_inner_masses']==[89879,63351]
         and m['expected']['family_count']==1776 and m['expected']['nonfree_counts']==[771,1005],
         'complete separate inner masses and family counts')
    overlap=None
    if a.parent_ledger is not None:
        ref=m['optional_parent_ledger'];entry=MAPPING[ref['path']]
        need(a.parent_ledger==entry['relative_path']and a.parent_ledger_sha256==ref['sha256'],
             'explicit exact borrowed parent, no default overlap claim')
        parent=document(ref);paid,unpaid=verify_borrowed_parent(parent,refs['index'],index,by)
        old=[];new=[];previously_unpaid=[];untried=[]
        for row in family:
            key=row[0],row[1]
            if key in paid:need(paid[key]==1,'no conflicting prior paid family status');old.append(row)
            else:
                new.append(row)
                if key in unpaid:previously_unpaid.append(row)
                else:untried.append(row)
        need(len(old)+len(new)==1776 and len(previously_unpaid)+len(untried)==len(new),'complete disjoint optional overlap')
        overlap=dict(parent=ref,parent_is_borrowed_metadata_only=True,other_parent_generation_or_subset_certificates_verified=False,
            already_paid_nonfree=old,newly_supported=new,previously_unpaid=previously_unpaid,previously_untried=untried,
            already_paid_count=len(old),newly_supported_count=len(new),parent_paid_count=len(paid),
            borrowed_union_arithmetic_count=len(paid)+len(new),borrowed_union_is_not_an_adoption=True)
    need(local_pin(manifest_path)==manifest_pin,'Source manifest unchanged after')
    for original,entry in MAPPING.items():mapped_path(dict(path=original,bytes=entry['bytes'],sha256=entry['sha256']))
    value=dict(schema='PORTABLE_VERIFIED_L026_NONFREE_ORBIT_FAMILY_V1',status='VERIFIED_EXACT_NONFREE_ORBIT_FAMILY',
        family_count=1776,nonfree_counts=[771,1005],family_rows=family,family_inner_masses=masses,stabilizer_orders=stabilizers,
        proof_kind=cert['proof_kind'],conditional_chain_premise=parts[0]['conditional_chain_premise'],
        named_centerless_group_model_and_historical_orbits_borrowed=True,group_classification_or_partition_arithmetic_replayed=False,
        optional_borrowed_parent_overlap=overlap,Source_manifest=manifest_pin,authenticated_copied_files=sorted(OPENED.values(),key=lambda x:x['relative_path']),
        authenticated_authored_files=m['authored_files'],
        ledger_or_gate_or_checkout_written=False,whole_Original_Aut_IP_reversal_census_Lean_measurement_credit=0)
    out=a.out;need(out.is_absolute()and out.parent.resolve(strict=True)==out.parent and not os.path.lexists(out)
         and not out.parent.is_relative_to(ROOT),'fresh output must be outside package')
    raw=canonical(value);need(len(raw)<=8*2**20,'whole result8MiB')
    with out.open('xb')as f:need(f.write(raw)==len(raw),'whole exclusive output')
    print(json.dumps(dict(status=value['status'],result=dict(path=str(out),**local_pin(out)),family_count=1776,
        family_inner_masses=masses,borrowed_parent_overlap=overlap is not None,checkout_written=False,whole_Original_credit=0),sort_keys=True))


if __name__=='__main__':main()

