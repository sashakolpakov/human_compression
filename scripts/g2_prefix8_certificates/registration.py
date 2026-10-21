"""Exact additive F004 publication layer; no mathematical or runtime replay.

The predecessor is checked in an explicitly frozen ce997 Git view. The actual
current index/working-tree delta is checked separately, without allowlist
waivers in the predecessor or a claim that its old CLI passed this new tree.
"""
import argparse,ast,hashlib,json,os,stat,subprocess,sys,time
from pathlib import Path,PurePosixPath

BASELINE='ce9970599fc1e7334f9f3f74ae37929346fbe4ad'
OLD_BASELINE='de0864a7bde3c992239427d3c838fe0fe8ea370d'
DIRECTORY='audit/f004/prefix8_certificates/'
CODE='scripts/g2_prefix8_certificates/registration.py'
POLICY=DIRECTORY+'publication_policy.json'
POLICY_SHA='9393ac41fb6bf7b86b32543c1ef85625f217a128294ebaf811b8b7d93eb2ea5b'
REGISTRATION=DIRECTORY+'registration.json'
DISPATCH='scripts/verify_snapshot.py'
GUIDE='docs/REPRODUCING.rst'
OLD_CODE='scripts/catalogue_completion_registration.py'
SOURCE_REVIEW=DIRECTORY+'publication_source_review.json'
SOURCE_EXECUTION=DIRECTORY+'publication_source_execution.json'
SOURCE_PACKET=DIRECTORY+'publication_source_packet.json'
SOURCE_PREPARATION=DIRECTORY+'publication_source_preparation_execution.json'
START=time.monotonic()

def need(ok,message):
    if not ok:raise ValueError(message)

def relative(name):
    need(type(name)is str,'literal relative path')
    p=PurePosixPath(name)
    need(not p.is_absolute()and str(p)==name and '..'not in p.parts and '\n'not in name and '\0'not in name,
         'canonical relative publication path')
    return name

def pin_bytes(name,raw):
    return dict(path=relative(name),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')

def read(root,name,cap=4*2**20):
    need(time.monotonic()-START<120,'bounded publication metadata time')
    p=root/relative(name)
    need(all(not q.is_symlink()for q in(p,*p.parents))and p.resolve(strict=True)==p,'ordinary public-only path')
    a=p.lstat();sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=cap,'bounded ordinary publication file')
    with p.open('rb')as f:
        b=os.fstat(f.fileno());raw=f.read(cap+1);z=os.fstat(f.fileno())
    need(sig(a)==sig(b)==sig(z)==sig(p.lstat())and len(raw)==a.st_size<=cap,'stable full publication bytes')
    return raw

def document(root,name):return json.loads(read(root,name))

def git(root,*args):
    q=subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false','-c','core.untrackedCache=false',*args],
        cwd=root,capture_output=True,timeout=60)
    need(q.returncode==0 and len(q.stdout)<=32*2**20,'bounded read-only retained Git metadata: '+' '.join(args))
    return q.stdout

def policy(root):
    raw=read(root,POLICY)
    need(hashlib.sha256(raw).hexdigest()==POLICY_SHA,'exact reviewed publication policy; no arbitrary manifests')
    p=json.loads(raw)
    need(p['schema']=='F004_PREFIX8_CE997_ADDITIVE_PUBLICATION_POLICY_V1'and p['baseline']==BASELINE,
         'fixed additive predecessor policy')
    return p

def byte_equal(a,b):return(a['bytes'],a['sha256'])==(b['bytes'],b['sha256'])

def canonical_tool(q):
    need(type(q)is dict and set(q)=={'handle','initial_chunk','terminal_chunk','exit_code','synchronous'},'canonical real tool')
    need(type(q['exit_code'])is int and q['exit_code']==0 and type(q['synchronous'])is bool,'genuine completed zero exit')
    need(type(q['initial_chunk'])is str and bool(q['initial_chunk'])and type(q['terminal_chunk'])is str and bool(q['terminal_chunk']),'genuine chunk identity')
    if q['synchronous']:need(q['handle']is None and q['initial_chunk']==q['terminal_chunk'],'synchronous identity')
    else:need(type(q['handle'])is int and q['handle']>0,'genuine async handle')

def proof(root,p,role):
    row=p['proof_roles'][role]
    raw=read(root,row['public']['path'])
    need(pin_bytes(row['public']['path'],raw)==row['public']and byte_equal(row['original'],row['public']),
         'exact original/public historical proof bytes')
    return row['original'],json.loads(raw)

def source_documents(root,p):
    paths=p['source_documents'];docs={name:pin_bytes(name,read(root,name))for name in paths}
    packet=document(root,SOURCE_PACKET);peer=document(root,SOURCE_REVIEW);ex=document(root,SOURCE_EXECUTION)
    origin=p['publication_source_origins'];code=pin_bytes(CODE,read(root,CODE))
    need(packet['program']==peer['program']==ex['program']and byte_equal(packet['program'],code)
         and packet['program']['path']==origin['program'],'truthful current program Source label')
    need(peer['status']=='PASS_DISTINCT_F004_PREFIX8_ADDITIVE_PUBLICATION_SOURCE'and peer['blockers']==[]
         and peer['source_author']==packet['source_author']=='/root/resource_cleanup_audit'
         and peer['reviewer']!='/root/resource_cleanup_audit','distinct current publication Source review')
    need(peer['source_packet']==ex['source_packet']and peer['source_packet']['path']==origin['source_packet']
         and byte_equal(peer['source_packet'],docs[SOURCE_PACKET]),'current exact packet, no future-hash guess')
    need(ex['review']['path']==origin['source_review']and byte_equal(ex['review'],docs[SOURCE_REVIEW])
         and ex['actor']==peer['reviewer'],'canonical Source execution review join')
    need(ex['status']=='COMPLETED_GENUINE_DISTINCT_F004_PREFIX8_ADDITIVE_PUBLICATION_SOURCE_REVIEW',
         'current canonical publication Source execution status')
    canonical_tool(ex['actual_tool'])
    raw=ex['full_tool_return']
    need(raw['exit_code']==0 and raw['chunk_id']==ex['actual_tool']['terminal_chunk'],'genuine Source tool return')
    need(packet['publication_policy']['path']==origin['policy']and byte_equal(packet['publication_policy'],pin_bytes(POLICY,read(root,POLICY))),
         'exact current policy Source role')
    for key,name in [('inverse',DIRECTORY+'publication_source_inverse.json'),('argument',DIRECTORY+'PUBLICATION.rst'),('checks',DIRECTORY+'publication_source_checks.json')]:
        need(byte_equal(packet[key],docs[name]),'current Source packet '+key)
    preparation=document(root,SOURCE_PREPARATION)
    need(preparation['program']==packet['program']and preparation['source_packet']['path']==origin['source_packet']
         and byte_equal(preparation['source_packet'],docs[SOURCE_PACKET]),'genuine late Source preparation role')
    need(preparation['represented_calls']==preparation['public_writes']==preparation['git_calls']==0,'Source-only author preparation')
    return docs

def acquired_selected_evidence(root,p):
    _,peer=proof(root,p,'portable_source_review');_,ex=proof(root,p,'portable_source_execution')
    need(peer['status']=='PASS_DISTINCT_F004_PREFIX8_PORTABLE_CERTIFICATE_ADAPTER_SOURCE'and peer['blockers']==[]
         and peer['source_author']=='/root/resource_cleanup_audit'and peer['reviewer']!='/root/resource_cleanup_audit',
         'retained distinct portable Source review')
    need(ex['review']==p['proof_roles']['portable_source_review']['original']and ex['actor']==peer['reviewer']
         and peer['program']==ex['program']and peer['source_packet']==ex['source_packet'],'retained canonical Source joins')
    canonical_tool(ex['actual_tool'])
    need(byte_equal(peer['program'],p['component_program'])and byte_equal(peer['manifest'],p['component_manifest']),
         'selected Source and manifest bytes')
    _,export=proof(root,p,'root_staged_export');_,execution=proof(root,p,'root_portable_replay_execution')
    need(export['root']==execution['root']=='/root'and export['status']=='ROOT_ACTUAL_EXACT_F004_PORTABLE_EXPORT_TO_STAGED_CHECKOUT'
         and execution['status']=='ROOT_ACTUAL_PUBLIC_ONLY_SELECTED_F004_CERTIFICATE_REPLAY','genuine selected export/replay authority')
    need(execution['export']==p['proof_roles']['root_staged_export']['original']and execution['source_review']==export['source_review']==p['proof_roles']['portable_source_review']['original']
         and execution['source_execution']==export['source_execution']==p['proof_roles']['portable_source_execution']['original'],'exact later Root proof joins')
    need(export['selected_cutoff']==dict(prior_borrowed=3283,proper230=230,common118=118,unpaid=148)
         and execution['selected_cutoff']==dict(borrowed_prior=3283,proper230=230,common118=118,unpaid=148),'historical selected cutoff, not later86')
    need(execution['private_study_access_denied_by_audit_hook']is execution['private_denial_positive_control']is True
         and execution['public_git_modified']is False and execution['original_model_reidentified']is False
         and execution['whole_original_credit']==0,'retained private-unavailable replay and limits')
    stage=PurePosixPath(export['stage_root'])
    rows=[dict(q,path=str(PurePosixPath(q['path']).relative_to(stage)))for q in export['exported_files']]
    manifest=document(root,p['component_manifest']['path'])
    need(rows==manifest['files']and export['exported_count']==len(rows)==81 and export['exported_payload_bytes']==8630284
         and export['mathematical_core_count']==50 and export['mathematical_core_bytes']==3005088,'exact acquired complete selected export')
    need(byte_equal(export['public_manifest'],p['component_manifest'])and byte_equal(export['source_manifest'],p['component_manifest']),
         'same acquired manifest bytes')
    for mode in('metadata','proper230','common118'):
        rq,report=proof(root,p,mode+'_report')
        need(execution['outputs'][mode]['report']==rq and report['manifest']==p['component_manifest']
             and report['mode']==mode and report['public_files_authenticated']==81
             and report['private_fallback']is False and report['whole_original_credit']==0,'actual selected report '+mode)
        canonical_tool(execution['operations'][mode]['actual_tool'])
        initial=execution['operations'][mode]['initial']
        need(initial['exit_code']==0 and initial['chunk_id']==execution['operations'][mode]['actual_tool']['terminal_chunk'],'genuine selected raw return')
        if mode=='metadata':
            need(report['status']=='PASS_PUBLIC_INPUT_AND_ACCEPTED_METADATA_INTEGRITY_ONLY'and report['mathematical_predicates_replayed']is False
                 and report['accepted230']==230 and report['accepted118']==118 and report['total_rejected']==3631 and report['unpaid']==148,
                 'integrity only scope')
            continue
        need(report['status']=='PASS_SELECTED_MATHEMATICAL_CERTIFICATE_REPLAY'and report['execution_program']==p['component_program']
             and report['reverified']==(230 if mode=='proper230'else 118)and report['old_private_CLI_claimed_executed']is False,
             'selected actual predicates, truthful adapter identity')
        need(report['full_model_reidentified']is report['original_weights_reproved']is False,'imported model/weights remain')
        result_ref,result=proof(root,p,mode+'_mathematical_result')
        need(report['result']==result_ref and report['journal']==p['journal_aliases'][mode]['original']
             and byte_equal(report['journal'],p['journal_aliases'][mode]['public']),
             'retained derived result; exact journal bytes reused once')
        need(len(result['newly_verified_representatives'])==report['reverified']and result['program']==report['borrowed_mathematical_source']
             and result['journal']==report['journal']and result['word_search_executed']is False,'actual mathematical report links')
        oq,outer=proof(root,p,mode+'_outer_receipt')
        need(execution['outputs'][mode]['outer_receipt']==oq and outer['status']=='PASS'and outer['stop']=='RETURNED'
             and outer['returncode']==0 and outer['error']is None and outer['cleanup']['errors']==outer['cleanup']['remaining']==[],
             'genuine drained selected guard receipt')
        need(outer['limits']['total_rss']==256*2**20 and outer['limits']['wall_seconds']==150
             and outer['seconds']<=150 and outer['peaks']['total_rss']<=256*2**20,'unchanged acquired selected limits')

def frozen_predecessor(root,p):
    old_raw=git(root,'show',BASELINE+':'+OLD_CODE)
    need(pin_bytes(OLD_CODE,old_raw)==p['old_code'],'retained exact old checker Source')
    text=old_raw.decode();edits=p['predecessor_IO_transport']['edits']
    need(len(edits)==2,'only the read/Git providers change')
    for e in edits:
        need(text.count(e['before'])==1,'exact predecessor Source transport site')
        text=text.replace(e['before'],e['after'],1)
    back=text
    for e in reversed(edits):back=back.replace(e['after'],e['before'],1)
    need(back.encode()==old_raw and hashlib.sha256(text.encode()).hexdigest()==p['predecessor_IO_transport']['effective_sha256'],
         'whole old Source inverse; no semantic checker relaxation')
    def fixed_read(name):
        need(name in p['old_current_read_names'],'finite frozen current metadata read')
        return git(root,'show',BASELINE+':'+relative(name))
    def fixed_git(args):
        args=tuple(args)
        if args==('merge-base','--is-ancestor',OLD_BASELINE,'HEAD'):
            return git(root,'merge-base','--is-ancestor',OLD_BASELINE,BASELINE)
        if args==('ls-files','-z'):return git(root,'ls-tree','-r','--name-only','-z',BASELINE)
        if args==('diff','--no-ext-diff','--no-renames','--name-only',OLD_BASELINE,'--'):
            return git(root,'diff','--no-ext-diff','--no-renames','--name-only',OLD_BASELINE,BASELINE,'--')
        if args==('ls-tree','-r','--name-only','-z',OLD_BASELINE):return git(root,*args)
        if len(args)==2 and args[0]=='show'and args[1]in {OLD_BASELINE+':'+x for x in p['old_historical_read_names']}:return git(root,*args)
        if args in [('rev-parse',OLD_BASELINE+':provenance/publication_manifest.json'),('cat-file','-s',OLD_BASELINE+':provenance/publication_manifest.json')]:return git(root,*args)
        raise ValueError('Undeclared frozen predecessor Git query')
    scope=dict(__name__='explicit_frozen_ce997_predecessor_view',__file__=str(root/OLD_CODE),
        FROZEN_ROOT=root,FROZEN_READ=fixed_read,FROZEN_GIT=fixed_git)
    exec(compile(text,str(root/OLD_CODE)+'::frozen-ce997-IO-edition','exec',dont_inherit=True),scope)
    result=scope['verify'](root,require_tracked=True)
    need(result['fully_treated']==102 and result['mathematical_originals']==105 and result['pending']==['F004','F009','L026'],
         'preserved exact original partition')
    return dict(status='PASS_EXPLICIT_FROZEN_CE997_PREDECESSOR_REGISTRATION_VIEW',
        borrowed_program=p['old_code'],old_cli_passed_enlarged_tree=False,predecessor_result=result)

def expected_edits(root,p):
    old_dispatch=git(root,'show',BASELINE+':'+DISPATCH);old_guide=git(root,'show',BASELINE+':'+GUIDE)
    need(pin_bytes(DISPATCH,old_dispatch)==p['old_dispatch']and pin_bytes(GUIDE,old_guide)==p['old_guide'],
         'exact baseline dispatcher and guide')
    change=p['dispatcher_inverse'];before=change['before'].encode();after=change['after'].encode()
    need(old_dispatch.count(before)==1,'one whole main Source edit')
    need(read(root,DISPATCH)==old_dispatch.replace(before,after,1),'dispatcher exact Source inverse')
    need(read(root,GUIDE)==old_guide+p['guide_append'].encode(),'guide exact appended section; no rewritten old text')

def current_delta(root,p,files,require_tracked):
    git(root,'merge-base','--is-ancestor',BASELINE,'HEAD')
    baseline={}
    for record in git(root,'ls-tree','-r','--full-tree','-z',BASELINE).split(b'\0'):
        if not record:continue
        head,path=record.split(b'\t',1);mode,kind,oid=head.decode().split();name=path.decode()
        need(name not in baseline,'unique baseline Git identity');baseline[name]=(mode,oid,kind)
    index={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        head,path=record.split(b'\t',1);mode,oid,stage=head.decode().split();name=path.decode()
        need(stage=='0'and name not in index,'no unresolved index or repeated path');index[name]=(mode,oid)
    modified={DISPATCH,GUIDE};new=set(files)-modified|{REGISTRATION}
    need(not new.intersection(baseline)and modified<=set(baseline),'additive exact semantic targets')
    need(set(index)<=set(baseline)|new and set(baseline)<=set(index),'no deleted or undeclared inherited/new tracked path')
    for name,(mode,oid,kind)in baseline.items():
        if name not in modified:need(index[name]==(mode,oid),'every inherited Git mode/blob retained: '+name)
    changed=set(filter(None,git(root,'diff','--no-ext-diff','--no-renames','--name-only','-z',BASELINE,'--').decode().split('\0')))
    need(changed<=new|modified,'no undeclared current tracked byte change')
    pending=[]
    for name in sorted(new|modified):
        raw=read(root,name);oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        mode=baseline[name][0]if name in modified else'100644'
        executable=bool((root/name).stat().st_mode&0o111)
        need(executable==(mode=='100755'),'preserved/new Git executable mode: '+name)
        if index.get(name)!=(mode,oid):pending.append(name)
    need(not require_tracked or not pending,'stage the exact complete declared layer before final check')
    tree=git(root,'rev-parse',BASELINE+'^{tree}').decode().strip()
    return dict(baseline_commit=BASELINE,baseline_tree=tree,inherited_paths=len(baseline),
        exact_current_files=len(files)+1,pending_tracking=pending,whole_inherited_payload_rehash_claimed=False)

def validate_content(root,p):
    expected={q['path']:q for q in p['fixed_files']}
    need(len(expected)==len(p['fixed_files']),'finite unique fixed export set')
    files=dict(expected)
    for name in p['source_documents']+[CODE,POLICY,DISPATCH,GUIDE]:
        need(name not in files,'no fixed/source role collision');files[name]=pin_bytes(name,read(root,name))
    need(len(files)<=256 and sum(q['bytes']for q in files.values())<=32*2**20,'bounded exact additive payload, no runtime tree')
    for name,q in files.items():need(pin_bytes(name,read(root,name))==q,'exact declared publication bytes: '+name)
    need(p['component_manifest']['sha256']=='01cea5727b680dc902fdb9065aadc4cfa6d04759b1c13120931ae5965815e141',
         'fixed acquired component manifest, never caller-selected arbitrary content')
    manifest=document(root,p['component_manifest']['path'])
    need(manifest['files']==p['component_files']and len(manifest['files'])==81 and len(manifest['mathematical_core'])==50,
         'exact selected complete mathematical payload')
    source_documents(root,p);acquired_selected_evidence(root,p);expected_edits(root,p)
    return[files[name]for name in sorted(files)]

def prepare(root):
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated Python -E -B')
    root=Path(root).absolute();need(root.resolve(strict=True)==root,'canonical public root')
    p=policy(root);need(not os.path.lexists(root/REGISTRATION),'fresh noncyclic registration document')
    files=validate_content(root,p)
    value=dict(schema='F004_PREFIX8_CE997_ADDITIVE_PUBLICATION_LAYER_V1',baseline=BASELINE,
        policy=pin_bytes(POLICY,read(root,POLICY)),files=files,source_review=next(q for q in files if q['path']==SOURCE_REVIEW),
        source_execution=next(q for q in files if q['path']==SOURCE_EXECUTION),
        selected_cutoff=dict(prior_borrowed=3283,proper230=230,common118=118,unpaid=148),
        fully_treated_originals=102,mathematical_originals=105,pending=['F004','F009','L026'],
        whole_original_credit=0,old_cli_passed_enlarged_tree=False,fresh_scientific_replay=False)
    raw=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode('ascii');need(len(raw)<=2**21,'bounded final registration')
    with(root/REGISTRATION).open('xb')as f:need(f.write(raw)==len(raw),'whole fresh registration')
    return dict(status='PREPARED_EXACT_ADDITIVE_REGISTRATION_NOT_YET_CURRENT_GIT_CHECK',registration=pin_bytes(REGISTRATION,raw),files=len(files))

def verify(root,require_tracked=False):
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated Python -E -B')
    root=Path(root).absolute();need(root.resolve(strict=True)==root,'canonical public checkout')
    p=policy(root);registered=document(root,REGISTRATION)
    need(registered['schema']=='F004_PREFIX8_CE997_ADDITIVE_PUBLICATION_LAYER_V1'and registered['baseline']==BASELINE,
         'exact new registration layer')
    files=validate_content(root,p)
    need(registered['files']==files and registered['policy']==pin_bytes(POLICY,read(root,POLICY)),
         'exact noncyclic complete final registration table')
    table={q['path']:q for q in files}
    need(registered['source_review']==table[SOURCE_REVIEW]and registered['source_execution']==table[SOURCE_EXECUTION],
         'final registration current Source proof roles')
    need(registered['fully_treated_originals']==102 and registered['mathematical_originals']==105 and registered['pending']==['F004','F009','L026']
         and registered['whole_original_credit']==0 and registered['old_cli_passed_enlarged_tree']is False and registered['fresh_scientific_replay']is False,
         'no original-level or fresh mathematics credit')
    need(registered['selected_cutoff']==dict(prior_borrowed=3283,proper230=230,common118=118,unpaid=148),'fixed historical cutoff')
    predecessor=frozen_predecessor(root,p)
    current=current_delta(root,p,{q['path']:q for q in files},require_tracked)
    need(time.monotonic()-START<120,'bounded complete registration time')
    return dict(status='PASS_ADDITIVE_F004_PREFIX8_PUBLICATION_LAYER',baseline=BASELINE,
        frozen_predecessor=predecessor,current_delta=current,selected_cutoff=registered['selected_cutoff'],
        fully_treated_originals=102,mathematical_originals=105,pending=registered['pending'],
        acquired_selected_replays={'proper230':230,'common118':118},fresh_scientific_replay=False,
        fresh_whole_corpus_replay=False,private_source_fallback=False,whole_original_credit=0)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--prepare-registration',action='store_true')
    parser.add_argument('--require-tracked',action='store_true')
    args=parser.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'isolated Python -E -B')
    print(json.dumps(prepare(args.root)if args.prepare_registration else verify(args.root,args.require_tracked),sort_keys=True))
