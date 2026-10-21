"""Independent portable Source/literal review; no exports or represented calls."""
import ast,hashlib,json,os,resource,stat,sys,time
from pathlib import Path,PurePosixPath
R=Path('/Users/sasha/medusa/research/leemans/maintenance/reproducibility/f004_prefix8_portable')
START=time.monotonic();SEEN={};TOTAL=0
def guard():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':rss*=1024
    assert rss<128*2**20 and time.monotonic()-START<120
def raw(path,expected=None):
    global TOTAL
    guard();p=Path(path);a=p.lstat()
    assert p.is_absolute()and p.resolve(strict=True)==p and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=2*2**20
    with p.open('rb')as f:b=os.fstat(f.fileno());v=f.read(a.st_size+1);z=os.fstat(f.fileno())
    sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert sig(a)==sig(b)==sig(z)==sig(p.lstat())and len(v)==a.st_size
    q=dict(path=str(p),bytes=len(v),sha256=hashlib.sha256(v).hexdigest())
    assert expected is None or q==expected
    assert SEEN.setdefault(q['path'],q)==q
    TOTAL+=len(v);assert TOTAL<=64*2**20
    return q,v
def doc(path,expected=None):
    q,v=raw(path,expected);return q,json.loads(v)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def merge(*groups):
    by={}
    for group in groups:
        for q in group:
            assert set(q)=={'path','bytes','sha256'}and type(q['bytes'])is int and q['bytes']>=0
            assert by.setdefault(q['path'],q)==q
    return[by[k]for k in sorted(by)]
def scope(rows):
    return dict(count=len(rows),bytes=sum(q['bytes']for q in rows),tuple_sha256=hashlib.sha256(canonical(rows)).hexdigest())
def definitions(text):
    return{n.name:(ast.get_source_segment(text,n),ast.dump(n,include_attributes=False))for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
pr,p=doc(R/'source_packet.json');assert pr['sha256']=='e6618cc133ebfc11f364aef944c534afc379439cfcef9c242ac1569435be11c1'
assert p['source_author']=='/root/resource_cleanup_audit'and p['source_only']is True
for q in p['required_current_source_inputs']:raw(q['path'],q)
late,_=raw(R/'source_preparation_execution.json');assert late['sha256']=='cf41011ce0c8c9929b7e18286142a5eaf6cf372c657c4eb4e1afca02b969c5de'
program,text=raw(p['program']['path'],p['program']);text=text.decode()
mr,m=doc(p['manifest']['path'],p['manifest']);ir,inv=doc(p['inverse']['path'],p['inverse'])
assert mr['sha256']=='01cea5727b680dc902fdb9065aadc4cfa6d04759b1c13120931ae5965815e141'
assert program['sha256']=='bdafdd184ef195de0e6eb240c547e4bf39547844c09831afe8b9ff2db4c64f18'
tree=ast.parse(text);constants={};cap_nodes={}
for n in tree.body:
    if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        if n.targets[0].id in('DOCUMENT_CAP','FILE_COUNT_CAP','INPUT_BYTES_CAP','SECONDS','RSS_CAP'):
            cap_nodes[n.targets[0].id]=ast.get_source_segment(text,n.value)
        if n.targets[0].id in('DATA','PROGRAM','PUBLIC_READER','SELF_BEFORE','SELF_AFTER','HISTORICAL_PROOF_ROLES'):
            constants[n.targets[0].id]=ast.literal_eval(n.value)
DATA,PROGRAM=constants['DATA'],constants['PROGRAM']
assert DATA=='data/g2_prefix8_certificates/'and PROGRAM=='scripts/g2_prefix8_certificates/check.py'
assert [cap_nodes[k]for k in('DOCUMENT_CAP','FILE_COUNT_CAP','INPUT_BYTES_CAP','SECONDS','RSS_CAP')]==['2**21','256','32*2**20','100','128*2**20']
assert m['schema']=='F004_PREFIX8_PORTABLE_CERTIFICATE_COMPONENT_V1'and m['scope']=='CONDITIONAL_SELECTED230_AND118_CERTIFICATES'
assert m['private_path_fallback']is False and m['whole_original_credit']==0 and m['public_payload_export_performed']is False and m['portable_replay_acquired']is False
assert m['no_runtime_manifest_leaf_freshness_claimed']is True
files=m['files'];assert files==merge(files)and len(files)==81 and sum(q['bytes']for q in files)==8630284
assert all(q['bytes']<=2**21 for q in files)
for q in files:
    name=q['path'];path=PurePosixPath(name)
    assert not path.is_absolute()and str(path)==name and '..'not in path.parts and(name.startswith(DATA)or name==PROGRAM)
fb={q['path']:q for q in files}
assert fb[PROGRAM]==dict(path=PROGRAM,bytes=program['bytes'],sha256=program['sha256'])
assert fb[DATA+'README.rst']==dict(path=DATA+'README.rst',bytes=p['argument']['bytes'],sha256=p['argument']['sha256'])
labels=m['logical_sources'];assert len(labels)==79 and len({q['original']['path']for q in labels})==79
bylabel={q['original']['path']:q for q in labels}
for row in labels:
    assert set(row)=={'original','public_path','role'}
    q=row['original'];public=fb[row['public_path']]
    assert Path(q['path']).is_absolute()and str(Path(q['path']))==q['path']and '..'not in Path(q['path']).parts
    assert(q['bytes'],q['sha256'])==(public['bytes'],public['sha256'])
assert {q['public_path']for q in labels}==set(fb)-{PROGRAM,DATA+'README.rst'}
core=m['mathematical_core'];assert core==merge(core)and len(core)==50 and sum(q['bytes']for q in core)==3005088
assert hashlib.sha256(canonical(core)).hexdigest()=='cf75762a65a50b3718c3cd9577002acd5444b363a364c41700765bb1a23a90b1'
packets=[doc(q['path'],q)[1]for q in p['mathematical_source_packets']]
assert m['routes']['proper230']['inputs']==packets[0]['scientific_direct_inputs']and len(m['routes']['proper230']['inputs'])==47
assert m['routes']['common118']['inputs']==packets[1]['fixed_direct_runtime_inputs']==core
assert merge(m['routes']['proper230']['inputs'],core)==core
expected=list(core);proof=[];gates={}
for key,count in[('proper230',22),('common118',28)]:
    route=m['routes'][key];item=inv['borrowed_routes'][key];source_ref=route['source_program']
    assert source_ref==item['original']and route['transport']==item['transport']and route['optional_word_pair_input_allowed']is False
    _,old=raw(source_ref['path'],source_ref);old=old.decode();assert old==item['original_source_utf8']
    parsed=ast.parse(old);reader=next(n for n in parsed.body if isinstance(n,ast.FunctionDef)and n.name=='read_exact')
    required=[dict(before=ast.get_source_segment(old,reader),after=constants['PUBLIC_READER'],count=1),dict(before=constants['SELF_BEFORE'],after=constants['SELF_AFTER'],count=1)]
    assert route['transport']['edits']==required
    forward=old
    for e in required:assert forward.count(e['before'])==e['count'];forward=forward.replace(e['before'],e['after'])
    reverse=forward
    for e in reversed(required):assert reverse.count(e['after'])==e['count'];reverse=reverse.replace(e['after'],e['before'])
    assert reverse==old and hashlib.sha256(forward.encode()).hexdigest()==route['transport']['effective_sha256']
    od,nd=definitions(old),definitions(forward);names=[name for name in od if name not in('read_exact','main')]
    assert names==item['unchanged_mathematical_definitions']and len(names)==count
    helperproof={}
    for name in names:
        assert od[name]==nd[name]
        helperproof[name]=dict(source_sha256=hashlib.sha256(od[name][0].encode()).hexdigest(),AST_sha256=hashlib.sha256(od[name][1].encode()).hexdigest())
    assert od['main'][0].replace(constants['SELF_BEFORE'],constants['SELF_AFTER'])==nd['main'][0]
    assert 'source_path.lstat()'not in forward and "p=Path(ref['path']);a=p.lstat()"not in forward
    if key=='common118':
        assert "if args.word_pairs is not None:"in forward
        assert "p=args.word_pairs"in forward
    # Literal Source-only I/O inventory: no historical pin is ever opened outside
    # transported read_exact. Other reads are fresh caller output files; common118
    # optional pairs are syntactically unreachable with the adapter's exact argv.
    access=[dict(line=n.lineno,call=ast.get_source_segment(forward,n))for n in ast.walk(ast.parse(forward))
        if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('open','read_text','read_bytes','lstat','resolve')]
    accepted=m['accepted'][key];gr,gate=doc(accepted['gate']['path'],accepted['gate']);gates[key]=gate
    assert gr in p['accepted_component_gates']
    assert gate['program']==source_ref and gate['result']==accepted['result']and gate['journal']==accepted['journal']
    assert set(accepted['historical_proofs'])==set(constants['HISTORICAL_PROOF_ROLES'])
    assert all(gate[role]==q for role,q in accepted['historical_proofs'].items())
    expected.extend([source_ref,accepted['gate'],accepted['result'],accepted['journal'],*accepted['historical_proofs'].values()])
    proof.append(dict(route=key,source_program=source_ref,IO_groups=2,whole_forward=True,whole_reverse=True,effective_sha256=route['transport']['effective_sha256'],main_only_self_IO_changed=True,whole_helper_identities=helperproof,effective_IO_call_inventory=access))
expected.extend(p['mathematical_source_packets'])
assert [q['original']for q in labels]==merge(expected)
assert gates['proper230']['prefix_complete']is gates['common118']['prefix_complete']is False
assert gates['proper230']['whole_original_credit']==gates['common118']['whole_original_credit']==0
# Scope derivation uses accepted gate metadata only; no candidate, result/journal
# mathematical data or core payload is read or evaluated by this Source review.
for key in('proper230','common118'):
    for ref in m['routes'][key]['inputs']+[m['routes'][key]['source_program']]:
        assert bylabel[ref['path']]['original']==ref
assert "p=self.root.joinpath(*q.parts)"in text and "self.files[row['public_path']]"in text
assert "def content(self,q):return self.exact(self.bound(q))"in text
assert "allowed.get(ref['path'])==ref"in text and "return ar.content(ref)"in text
assert "sys.argv=[PROGRAM,'--output',str(result),'--journal',str(journal)]"in text
assert "scope=dict(__name__='f004_portable_borrowed_mathematical_body',__file__=q['path']"in text
assert "ar.unchanged()"in text and "no private or symlink fallback"in text
assert "need(current['stop']is None"in text and "current['supplied_word_pair_count']==0"in text
assert "full_model_reidentified=False,original_weights_reproved=False,whole_original_credit=0"in text
reviewer_history,_=raw(R/'unit_source_history.json')
method,_=raw(__file__);rows=[SEEN[k]for k in sorted(SEEN)]
checks=dict(status='PASS_SOURCE_ONLY_F004_PREFIX8_PORTABLE_COMPONENT',reviewer='/root/unit_actual_review',source_author=p['source_author'],program=program,manifest=mr,source_packet=pr,inverse=ir,argument=p['argument'],method=method,blockers=[],complete_supported_path_read=True,transport_derivations=proof,IO_groups=4,whole_mathematical_helper_identities=50,historical_labels=79,mathematical_core=dict(count=50,bytes=3005088,tuple_sha256=hashlib.sha256(canonical(core)).hexdigest()),proposed_public_scope=dict(files=81,bytes=8630284,manifest_bytes=mr['bytes']),late_author_preparation=late,checked_current_source_inputs=rows,checked_current_source_scope=scope(rows),
 findings=['Full adapter/README/manifest/Source assembler and both IO derivations were independently read. Each route has exactly2 whole reversible IO edits;22+28 mathematical helper Source/AST identities and each entire main outside its self-Source IO site are preserved.',
 'Exact79 historical labels equal the complete literal union of core50, both mathematical Sources/Source packets, two selected gates/results/journals and11 historical proof roles each. Core50 tuple/3,005,088B is unchanged and old47 is its exact subset. Proposed81 public objects/8,630,284B plus manifest are declared, not materialized or payload-authenticated here.',
 'The only input resolver accepts allowlisted canonical relative public files, rejects symlinks/hardlinks/traversal, checks complete pins and maps exact historical labels through declared public bytes. No private fallback exists. Transported body pins are borrowed semantic Source labels while execution_program identifies the public adapter.',
 'The metadata command authenticates public bytes and exact accepted-partition/provenance joins only. Separate proper230/common118 calls run preserved predicates on selected positive certificates; argv supplies only output/journal, so optional proposal file IO is unavailable. Every complete selected set/type count must match the accepted report; any miss/stop/count mismatch refuses. No148 or worker148 credit is granted.',
 'Resource checks and document/input/output caps remain explicit observed fail-closed checks, not a new acquired supervisor or tested fit. Public manifest and all declared files are rehashed after the selected operation. Output is fresh external/exclusive; no registry/Root adoption/publication is performed by this Source review.'],
 qualifications=['Unit authored EDF and earlier metadata/inventory/review machinery; Cleanup authored8038 and this portable integration. Reused mathematics and historical evidence are borrowed explicitly, not a distinct new arithmetic implementation. This reviewer did not import/execute the adapter or retained bodies.',
 'Only ordinary bounded Source/Source-packet/manifest/selected small gate/proof preparation documents were read/hashed. No mathematical core payload, candidate, matrix, result/journal, fixture, permutation, Reader/runtime/process/state/Git or publication/export operation occurred.',
 'All79 logical/public payload mappings were checked as literal pin metadata; their actual bytes remain Root export duties. No private-free replay, portability/fit/test/registration or real public snapshot check is acquired. Root must materialize/hash/export exact bytes and run a genuine public-only selected replay with the private study unavailable before advertising tested commands.',
 'Reviewer-only preoutput a2c362 Source-cap literal parser stop and original reviewer Source are preserved in current history; only reviewer cap-expression comparison changed, with no author or target change.',
 'Previous3283, complete catalogue, full naturalG2(11)/A=G model/original frame transport and original orbit weights remain exact imported premises. Reading historical runtime Source tables does not newly authenticate the private leaves. Selected3631/3779 with148unpaid is the fixed two-gate cutoff; whole-prefix/F004/paper/Lean credit stays zero.'],
represented_calls=0,scientific_payload_reads=0,scientific_payload_hashes=0,fixture_calls=0,exports=0,public_writes=0,root_state_writes=0,process_queries=0,author_bytes_changed=False)
out=R/'unit_source_checks.json';assert not out.exists()
value=(json.dumps(checks,sort_keys=True,indent=2)+'\n').encode();assert len(value)<=2*2**20;guard()
with out.open('xb')as f:assert f.write(value)==len(value);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(checks=dict(path=str(out),bytes=len(value),sha256=hashlib.sha256(value).hexdigest()),method=method,program=program,manifest=mr,source_packet=pr,source_scope=scope(rows),IO_groups=4,helper_identities=50,logical_labels=79,blockers=[]),sort_keys=True))

