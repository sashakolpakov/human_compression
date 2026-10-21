"""Strict additive ON centralizer publication; no arithmetic or scientific imports.

The unchanged G2 verifier runs only in an explicit frozen4512492 read/Git view.
The actual current4512492 delta is checked separately before and after it.
"""
import argparse,ast,hashlib,json,os,stat,subprocess,sys,time
from pathlib import Path,PurePosixPath

BASELINE='4512492579d2809c32cadeda9250ae26ce661616'
G2_BASELINE='ce9970599fc1e7334f9f3f74ae37929346fbe4ad'
OLD_BASELINE='de0864a7bde3c992239427d3c838fe0fe8ea370d'
DIRECTORY='audit/l026/onan_centralizer/'
CODE='scripts/onan_centralizer/registration.py'
POLICY=DIRECTORY+'publication_policy.json'
POLICY_SHA='175395319e1559c0d39afec2f06e6db614b85a2b559d474ddeca0fdd30fbe096'
MANIFEST=DIRECTORY+'publication_manifest.json'
DELTA=DIRECTORY+'publication_delta.json'
REGISTRATION=DIRECTORY+'registration.json'
OLD_CODE='scripts/g2_prefix8_certificates/registration.py'
DISPATCH='scripts/verify_snapshot.py'
GUIDE='docs/REPRODUCING.rst'
START=time.monotonic()

def need(ok,why):
    if not ok:raise ValueError(why)

def relative(name):
    need(type(name)is str,'literal relative path')
    p=PurePosixPath(name)
    need(not p.is_absolute()and str(p)==name and '..'not in p.parts
         and '\0'not in name and '\n'not in name,'canonical relative path')
    return name

def pin_bytes(name,raw):
    return dict(path=relative(name),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def read(root,name,cap=4*2**20):
    need(time.monotonic()-START<120,'bounded metadata time')
    p=root/relative(name);a=p.lstat()
    need(p.resolve(strict=True)==p and all(not x.is_symlink()for x in(p,*p.parents))
         and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=cap,'ordinary bounded public bytes')
    signature=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    with p.open('rb')as f:b=os.fstat(f.fileno());raw=f.read(cap+1);z=os.fstat(f.fileno())
    need(signature(a)==signature(b)==signature(z)==signature(p.lstat())and len(raw)==a.st_size<=cap,
         'stable complete public bytes')
    return raw

def document(root,name):return json.loads(read(root,name))
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')
def same_bytes(a,b):return(a['bytes'],a['sha256'])==(b['bytes'],b['sha256'])

def git(root,*args):
    value=subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false',
        '-c','core.untrackedCache=false',*args],cwd=root,capture_output=True,timeout=60)
    need(value.returncode==0 and len(value.stdout)<=32*2**20,'bounded read-only retained Git metadata')
    return value.stdout

def policy(root):
    raw=read(root,POLICY)
    need(hashlib.sha256(raw).hexdigest()==POLICY_SHA,'fixed independently reviewed policy; no arbitrary manifest')
    p=json.loads(raw)
    need(p['schema']=='ONAN_CENTRALIZER_4512492_PUBLICATION_POLICY_V1'and p['baseline']==BASELINE,
         'exact4512492 additive policy')
    return p

def tool(q):
    need(type(q)is dict and set(q)=={'handle','initial_chunk','terminal_chunk','exit_code','synchronous'},'genuine five-field tool')
    need(type(q['exit_code'])is int and q['exit_code']==0 and type(q['synchronous'])is bool
         and all(type(q[k])is str and q[k]for k in ['initial_chunk','terminal_chunk']),'successful actual tool')
    need((q['synchronous']and q['handle']is None and q['initial_chunk']==q['terminal_chunk'])or
         (not q['synchronous']and type(q['handle'])is int and q['handle']>0),'canonical captured tool identity')

def rows(value):
    need(type(value)is list,'literal publication table')
    by={}
    for q in value:
        need(type(q)is dict and set(q)=={'path','bytes','sha256'}and relative(q['path'])not in by
             and type(q['bytes'])is int and 0<=q['bytes']<=4*2**20 and type(q['sha256'])is str
             and len(q['sha256'])==64 and all(x in '0123456789abcdef'for x in q['sha256']),'unique complete publication pin')
        by[q['path']]=q
    need(value==[by[k]for k in sorted(by)],'sorted literal complete publication table')
    return by

def original_proof(root,m,role,table):
    link=m['proof_roles'][role]
    need(set(link)=={'original','public'}and table.get(link['public']['path'])==link['public']
         and same_bytes(link['original'],link['public']),'exact original/public proof bytes: '+role)
    return link['original'],document(root,link['public']['path'])

def evidence(root,p,m,table):
    packet_ref,packet=original_proof(root,m,'portable_source_packet',table)
    peer_ref,peer=original_proof(root,m,'portable_source_review',table)
    ex_ref,ex=original_proof(root,m,'portable_source_execution',table)
    need(peer['status']=='PASS_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE'and peer['blockers']==[]
         and peer['source_author']==packet['source_author']=='/root/unit_actual_review'
         and peer['reviewer']!=peer['source_author']and peer['source_packet']==packet_ref
         and ex['source_packet']==packet_ref and ex['review']==peer_ref and ex['actor']==peer['reviewer'],
         'genuine independent portable Source authority')
    tool(ex['actual_tool'])
    need(packet['program']==peer['program']==ex['program']and
         ex['status']=='COMPLETED_GENUINE_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE_REVIEW'
         and same_bytes(packet['program'],p['package_program'])and same_bytes(packet['manifest'],p['package_manifest']),
         'exact fixed8 Source/manifest approval')
    export_ref,export=original_proof(root,m,'root_staged_export',table)
    _,execution=original_proof(root,m,'root_portable_replay_execution',table)
    need(export['schema']=='ROOT_ONAN_CENTRALIZER_PORTABLE_EXPORT_V1'and export['root']=='/root'
         and export['files']==p['package_files']and export['payloads_freshly_hashed']is True
         and export['source_packet']==packet_ref and export['source_review']==peer_ref and export['source_execution']==ex_ref,
         'genuine exact eight-file Root export wrapper')
    tool(export['actual_tool'])
    need(execution['schema']=='ROOT_ONAN_CENTRALIZER_PUBLIC_ONLY_REPLAY_V1'and execution['root']=='/root'
         and execution['export']==export_ref and execution['source_review']==peer_ref
         and execution['source_execution']==ex_ref and execution['private_study_access_denied_by_audit_hook']is True
         and execution['private_denial_positive_control']is True and execution['whole_original_credit']==0,
         'genuine public-only replay and private-denial authority')
    seen=[]
    need(1<=len(execution['operations'])<=4,'one all-route or four separately captured selected calls')
    for op in execution['operations']:
        tool(op['actual_tool'])
        rq,report=original_proof(root,m,op['receipt_role'],table)
        oq,outer=original_proof(root,m,op['guard_role'],table)
        need(op['receipt']==rq and op['guard_receipt']==oq and
             report['schema']=='ONAN_CENTRALIZER_PUBLIC_ONLY_REPLAY_V1'
             and report['status']=='PASS_SELECTED_ONAN_CENTRALIZER_PORTABLE_REPLAY'
             and report['execution_program']==p['package_program']and report['manifest']==p['package_manifest']
             and report['private_fallback']is False and report['original_source_bodies_unchanged']is True,
             'actual unchanged-body public facade report')
        need(all(report[k]is False for k in ['named_model_reidentified','centralizer_upper_bound_reproved',
             'matrix45D_homomorphism_proved','L026_complete'])and
             all(report[k]==0 for k in ['census_credit','conjecture_credit','whole_original_credit']),
             'borrowed model/centralizer bound; no census45D or original credit')
        need(outer['status']=='PASS'and outer['stop']=='RETURNED'and outer['returncode']==0
             and outer['error']is None and outer['cleanup']['remaining']==outer['cleanup']['errors']==[]
             and outer['limits']['total_rss']==256*2**20 and outer['limits']['wall_seconds']==150
             and outer['seconds']<=150 and outer['peaks']['total_rss']<=256*2**20,'actual drained256MiB150s guard')
        need(len(op['result_roles'])==len(report['selected_results']),'complete actual route result roles')
        for item,role in zip(report['selected_results'],op['result_roles']):
            result_ref,result=original_proof(root,m,role,table)
            mode=item['mode'];need(mode in p['routes']and mode not in seen,'each exact route once')
            seen.append(mode)
            need(item['result']==result_ref and item['status']==result['status']==p['routes'][mode],
                 'literal exact original returned result: '+mode)
            if mode=='standard-controls':need(result['count']==9,'nine literal standard controls')
            if mode=='pair-controls':need(result['count']==13,'thirteen pair-tree controls')
            if mode=='standard-pair':need(result['degree']==245520 and result['named_group_identification_reproved']is False,
                 'standard pair finite scope')
            if mode=='check-centralizer':
                need(result['degree']==245520 and result['seed']==[0,1]and result['complete']is True
                     and result['reached_pairs']==161280 and result['verified_edges']==161279
                     and result['centralizer_upper_bound_borrowed']==161280 and result['named_model_reproved']is False
                     and same_bytes(result['certificate'],p['tree']),'whole saved centralizer certificate actual check')
    need(set(seen)==set(p['routes']),'all four actual portable routes acquired')

def current_source(root,p,m,table):
    docs={k:document(root,DIRECTORY+k)for k in ['publication_source_packet.json','publication_source_review.json',
         'publication_source_execution.json','publication_source_preparation_execution.json']}
    packet,peer,ex,prep=[docs[k]for k in ['publication_source_packet.json','publication_source_review.json',
         'publication_source_execution.json','publication_source_preparation_execution.json']]
    need(peer['status']=='PASS_DISTINCT_L026_ONAN_CENTRALIZER_PUBLICATION_SOURCE'and peer['blockers']==[]
         and packet['source_author']==peer['source_author']=='/root/resource_cleanup_audit'
         and peer['reviewer']!=peer['source_author']and ex['actor']==peer['reviewer'], 'distinct current registration Source review')
    need(packet['program']==peer['program']==ex['program']and same_bytes(packet['program'],table[CODE])
         and packet['publication_policy']['sha256']==POLICY_SHA,'exact current registration program/policy roles')
    need(peer['source_packet']==ex['source_packet']and same_bytes(peer['source_packet'],table[DIRECTORY+'publication_source_packet.json'])
         and same_bytes(ex['review'],table[DIRECTORY+'publication_source_review.json']), 'nonretargeted current Source packet/peer/ex')
    need(ex['status']=='COMPLETED_GENUINE_DISTINCT_L026_ONAN_CENTRALIZER_PUBLICATION_SOURCE_REVIEW',
         'current canonical publication Source execution status')
    for key,name in [('inverse','publication_source_inverse.json'),('argument','README.rst'),
                     ('checks','publication_source_checks.json')]:
        need(same_bytes(packet[key],table[DIRECTORY+name]),'current packet exact '+key+' bytes')
    need(same_bytes(packet['dispatcher'],table[DISPATCH])and same_bytes(packet['guide'],table[GUIDE]),
         'Source-reviewed exact dispatcher and appended guide')
    tool(ex['actual_tool'])
    need(ex['full_tool_return']['exit_code']==0 and ex['full_tool_return']['chunk_id']==ex['actual_tool']['terminal_chunk'],
         'genuine current Source execution raw capture')
    need(prep['program']==packet['program']and same_bytes(prep['source_packet'],table[DIRECTORY+'publication_source_packet.json'])
         and prep['public_writes']==prep['git_calls']==prep['represented_calls']==0,'genuine late Source-only preparation')

def content(root,p,manifest_ref,delta_ref):
    need(manifest_ref['path']==MANIFEST and delta_ref['path']==DELTA,'fixed explicit frozen publication inputs')
    need(pin_bytes(MANIFEST,read(root,MANIFEST))==manifest_ref and pin_bytes(DELTA,read(root,DELTA))==delta_ref,
         'SHA-bound complete manifest and delta, no future pin defaults')
    m=document(root,MANIFEST);d=document(root,DELTA)
    need(m['schema']=='ONAN_CENTRALIZER_PUBLICATION_MANIFEST_V1'and m['baseline']==BASELINE
         and d['schema']=='ONAN_CENTRALIZER_PUBLICATION_DELTA_V1'and d['baseline']==BASELINE,'exact publication schemas')
    table=rows(m['files']);fixed={q['path']:q for q in p['package_files']}
    need(all(table.get(k)==v for k,v in fixed.items()),'all eight fixed mathematical Source/data/manifest bytes')
    need(set(table)<=set(p['allowed_files'])and set(p['required_files'])<=set(table)
         and len(table)<=80 and sum(q['bytes']for q in table.values())<=16*2**20,'finite semantic publication closure only')
    need(not{MANIFEST,DELTA,REGISTRATION}.intersection(table),'acyclic complete publication inputs')
    for name,q in table.items():need(pin_bytes(name,read(root,name))==q,'fresh full current publication bytes: '+name)
    old_dispatch=git(root,'show',BASELINE+':'+DISPATCH);old_guide=git(root,'show',BASELINE+':'+GUIDE)
    need(pin_bytes(DISPATCH,old_dispatch)==p['old_dispatch']and pin_bytes(GUIDE,old_guide)==p['old_guide'],'whole retained baseline admin bytes')
    e=p['dispatcher_inverse'];need(old_dispatch.count(e['before'].encode())==1 and
         read(root,DISPATCH)==old_dispatch.replace(e['before'].encode(),e['after'].encode(),1),'one whole dispatcher main inverse')
    need(read(root,GUIDE)==old_guide+p['guide_append'].encode(),'strict append-only guide')
    need(d['modified']==[table[x]for x in sorted([DISPATCH,GUIDE])]and
         d['added']==[table[x]for x in sorted(set(table)-{DISPATCH,GUIDE})], 'exact literal delta, no undeclared administrative change')
    current_source(root,p,m,table);evidence(root,p,m,table)
    return m,d,table

def current_delta(root,table,require_tracked):
    git(root,'merge-base','--is-ancestor',BASELINE,'HEAD')
    baseline={}
    for line in git(root,'ls-tree','-r','--full-tree','-z',BASELINE).split(b'\0'):
        if not line:continue
        head,name=line.split(b'\t',1);mode,kind,oid=head.decode().split();name=name.decode()
        need(name not in baseline,'unique full baseline Git path');baseline[name]=(mode,oid,kind)
    index={}
    for line in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not line:continue
        head,name=line.split(b'\t',1);mode,oid,stage=head.decode().split();name=name.decode()
        need(stage=='0'and name not in index,'unique resolved index');index[name]=(mode,oid)
    modified={DISPATCH,GUIDE};new=(set(table)-modified)|{MANIFEST,DELTA,REGISTRATION}
    need(not new.intersection(baseline)and modified<=set(baseline),'strict additive path domains')
    need(set(baseline)<=set(index)<=set(baseline)|new,'all prior tracked paths retained; no foreign tracked addition')
    for name,(mode,oid,kind)in baseline.items():
        if name not in modified:need(index[name]==(mode,oid),'full inherited Git mode/blob identity: '+name)
    changed=set(filter(None,git(root,'diff','--no-ext-diff','--no-renames','--name-only','-z',BASELINE,'--').decode().split('\0')))
    untracked=set(filter(None,git(root,'ls-files','--others','--exclude-standard','-z').decode().split('\0')))
    need(changed<=new|modified and untracked<=new,'no undeclared tracked or ordinary untracked current delta')
    pending=[]
    for name in sorted(new|modified):
        raw=read(root,name);oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        mode=baseline[name][0]if name in modified else'100644'
        need(bool((root/name).stat().st_mode&0o111)==(mode=='100755'),'exact current executable mode')
        if index.get(name)!=(mode,oid):pending.append(name)
    need(not require_tracked or not pending,'stage exactly complete publication before final verification')
    return dict(baseline_commit=BASELINE,baseline_tree=git(root,'rev-parse',BASELINE+'^{tree}').decode().strip(),
        inherited_paths=len(baseline),current_files=len(new|modified),pending_tracking=pending)

def frozen_predecessor(root,p):
    raw=git(root,'show',BASELINE+':'+OLD_CODE)
    need(pin_bytes(OLD_CODE,raw)==p['old_registration'],'exact unchanged4512492 G2 verifier Source')
    source=raw.decode();edits=p['predecessor_IO_transport']['edits']
    for e in edits:
        need(source.count(e['before'])==1,'one exact frozen IO provider transport')
        source=source.replace(e['before'],e['after'],1)
    back=source
    for e in reversed(edits):back=back.replace(e['after'],e['before'],1)
    need(back.encode()==raw and hashlib.sha256(source.encode()).hexdigest()==p['predecessor_IO_transport']['effective_sha256'],
         'whole predecessor inverse; all semantic functions remain Source-exact')
    def frozen_read(name,cap):
        need(name in p['frozen_current_read_names'],'finite frozen4512492 read set')
        value=git(root,'show',BASELINE+':'+relative(name));need(len(value)<=cap,'original read cap retained');return value
    def frozen_git(args):
        if args==('merge-base','--is-ancestor',G2_BASELINE,'HEAD'):
            return git(root,'merge-base','--is-ancestor',G2_BASELINE,BASELINE)
        if args==('ls-files','--stage','-z'):
            result=[]
            for line in git(root,'ls-tree','-r','--full-tree','-z',BASELINE).split(b'\0'):
                if line:
                    head,name=line.split(b'\t',1);mode,kind,oid=head.split()
                    result.append(mode+b' '+oid+b' 0\t'+name+b'\0')
            return b''.join(result)
        if args==('diff','--no-ext-diff','--no-renames','--name-only','-z',G2_BASELINE,'--'):
            return git(root,'diff','--no-ext-diff','--no-renames','--name-only','-z',G2_BASELINE,BASELINE,'--')
        if args in [('ls-tree','-r','--full-tree','-z',G2_BASELINE),('rev-parse',G2_BASELINE+'^{tree}'),
                    ('merge-base','--is-ancestor',OLD_BASELINE,G2_BASELINE),
                    ('ls-tree','-r','--name-only','-z',G2_BASELINE),('ls-tree','-r','--name-only','-z',OLD_BASELINE),
                    ('diff','--no-ext-diff','--no-renames','--name-only',OLD_BASELINE,G2_BASELINE,'--'),
                    ('rev-parse',OLD_BASELINE+':provenance/publication_manifest.json'),
                    ('cat-file','-s',OLD_BASELINE+':provenance/publication_manifest.json')]:return git(root,*args)
        if len(args)==2 and args[0]=='show'and args[1]in p['historical_show_specs']:return git(root,*args)
        raise ValueError('undeclared nested retained Git query')
    ns=dict(__name__='explicit_frozen4512492_g2_registration',__file__=str(root/OLD_CODE),
        FROZEN_ROOT=root,FROZEN_READ=frozen_read,FROZEN_GIT=frozen_git)
    exec(compile(source,str(root/OLD_CODE)+'::frozen4512492-IO-edition','exec',dont_inherit=True),ns)
    result=ns['verify'](root,require_tracked=True)
    need(result['fully_treated_originals']==102 and result['mathematical_originals']==105 and
         result['pending']==['F004','F009','L026']and result['selected_cutoff']==p['historical_g2_cutoff'],
         'entire prior G2/corpus logic and historical cutoff unchanged')
    return dict(status='PASS_EXPLICIT_FROZEN4512492_G2_REGISTRATION_VIEW',
        old_cli_passed_enlarged_tree=False,current_modes_prevalidated_against_baseline=True,result=result)

def prepare(root,manifest_sha256,delta_sha256):
    root=Path(root).absolute();p=policy(root)
    need(not os.path.lexists(root/REGISTRATION),'fresh explicit noncyclic registration')
    manifest_ref=pin_bytes(MANIFEST,read(root,MANIFEST));delta_ref=pin_bytes(DELTA,read(root,DELTA))
    need(manifest_ref['sha256']==manifest_sha256 and delta_ref['sha256']==delta_sha256,'explicit real frozen manifest/delta CLI SHAs')
    _,_,table=content(root,p,manifest_ref,delta_ref)
    value=dict(schema='ONAN_CENTRALIZER_4512492_PUBLICATION_REGISTRATION_V1',baseline=BASELINE,
        publication_manifest=manifest_ref,publication_delta=delta_ref,files=[table[k]for k in sorted(table)],
        fully_treated_originals=102,mathematical_originals=105,pending=['F004','F009','L026'],
        old_cli_passed_enlarged_tree=False,fresh_scientific_replay=False,whole_original_credit=0)
    raw=json.dumps(value,sort_keys=True,indent=2).encode()+b'\n';need(len(raw)<=256*2**10,'bounded final registration')
    with(root/REGISTRATION).open('xb')as f:need(f.write(raw)==len(raw),'complete exclusive registration write')
    return dict(status='PREPARED_ONAN_CENTRALIZER_REGISTRATION_NOT_YET_CURRENT_INDEX_PASS',registration=pin_bytes(REGISTRATION,raw))

def verify(root,require_tracked=False):
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated ordinary -E -B')
    root=Path(root).absolute();need(root.resolve(strict=True)==root,'canonical public checkout')
    p=policy(root);v=document(root,REGISTRATION)
    need(v['schema']=='ONAN_CENTRALIZER_4512492_PUBLICATION_REGISTRATION_V1'and v['baseline']==BASELINE,
         'current exact registration')
    _,_,table=content(root,p,v['publication_manifest'],v['publication_delta'])
    need(v['files']==[table[k]for k in sorted(table)]and v['fully_treated_originals']==102
         and v['mathematical_originals']==105 and v['pending']==['F004','F009','L026']
         and v['old_cli_passed_enlarged_tree']is v['fresh_scientific_replay']is False
         and v['whole_original_credit']==0,'unchanged102/105 and no new whole-original credit')
    before=current_delta(root,table,require_tracked)
    prior=frozen_predecessor(root,p)
    after=current_delta(root,table,require_tracked)
    need(before==after,'stable complete current delta around frozen predecessor evaluation')
    return dict(status='PASS_ADDITIVE_ONAN_CENTRALIZER_PUBLICATION_LAYER',baseline=BASELINE,
        frozen_predecessor=prior,current_delta=after,fully_treated_originals=102,mathematical_originals=105,
        pending=v['pending'],historical_g2_cutoff=p['historical_g2_cutoff'],fresh_scientific_replay=False,
        private_fallback=False,L026_complete=False,whole_original_credit=0)

if __name__=='__main__':
    ap=argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--prepare-registration',action='store_true')
    ap.add_argument('--publication-manifest-sha256');ap.add_argument('--publication-delta-sha256')
    ap.add_argument('--require-tracked',action='store_true');args=ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated ordinary -E -B')
    if args.prepare_registration:
        need(args.publication_manifest_sha256 and args.publication_delta_sha256,'explicit real manifest/delta SHAs required')
        result=prepare(args.root,args.publication_manifest_sha256,args.publication_delta_sha256)
    else:result=verify(args.root,args.require_tracked)
    print(json.dumps(result,sort_keys=True))
