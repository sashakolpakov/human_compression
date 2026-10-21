"""Source/ordinary metadata assembly only; does not export, import or call science."""
from pathlib import Path
import ast
import hashlib
import json

HERE=Path(__file__).absolute().parent
S=HERE.parents[2]
W=S/'computation/f004/small_inventory_work/cayley_centralizer_certificate'
DATA='data/g2_prefix8_certificates/'
PROGRAM='scripts/g2_prefix8_certificates/check.py'
AUTHOR='/root/resource_cleanup_audit'
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def raw_pin(p,b):return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def ordinary(p,sha=None):
    assert p.is_file()and not p.is_symlink()
    b=p.read_bytes();assert len(b)<=2**21
    q=raw_pin(p,b);assert sha is None or q['sha256']==sha
    return b,q
def doc(p,sha):
    b,q=ordinary(p,sha);return json.loads(b),q
def union(*tables):
    by={}
    for table in tables:
        for q in table:assert by.setdefault(q['path'],q)==q
    return[by[k]for k in sorted(by)]
def dump(v):return(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('ascii')

ap,ap_ref=doc(W/'prefix8_saved230_source_packet.json','bcc45222616ab87eea84ca9ff1f6dca377aaed67a984a0d7cd151990ae9a6739')
bp,bp_ref=doc(W/'prefix8_remaining_line_and_intersection_source_packet.json','ba3b8a61756f7c4b1fbac767c2cb63ceee7bb9e0321d9932a3c6039070488435')
gates={}
for key,path,sha in[
 ('proper230',W/'cases/prefix8_saved230_independent_verification/root_saved230_acceptance.json','803e958b0e0b5cfb89adf47e8be7fed35bfec36d8a876ee6835b2d1c3a05d651'),
 ('common118',W/'cases/prefix8_remaining_line_and_intersection/root_certificate_acceptance.json','ab4ef4b7a8c704b7fc898f272035c16c5e6d294c43acba7fb6b134f41776ee53')]:
    gates[key]=doc(path,sha)
core=bp['fixed_direct_runtime_inputs'];old47=ap['scientific_direct_inputs']
assert core==union(core)and len(core)==50 and sum(q['bytes']for q in core)==3005088
assert hashlib.sha256(canon(core)).hexdigest()=='cf75762a65a50b3718c3cd9577002acd5444b363a364c41700765bb1a23a90b1'
assert len(old47)==47 and union(old47,core)==core
adapter,adapter_ref=ordinary(HERE/'check.py');adapter_tree=ast.parse(adapter)
constants={}
for n in adapter_tree.body:
    if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in('PUBLIC_READER','SELF_BEFORE','SELF_AFTER','HISTORICAL_PROOF_ROLES'):
        constants[n.targets[0].id]=ast.literal_eval(n.value)
assert set(constants)=={'PUBLIC_READER','SELF_BEFORE','SELF_AFTER','HISTORICAL_PROOF_ROLES'}
routes={};inverses={};programs=[]
for key,packet,inputs in [('proper230',ap,old47),('common118',bp,core)]:
    q=packet['program'];raw,current=ordinary(Path(q['path']),q['sha256']);assert current==q
    text=raw.decode();nodes=[n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='read_exact'];assert len(nodes)==1
    edits=[dict(before=ast.get_source_segment(text,nodes[0]),after=constants['PUBLIC_READER'],count=1),
           dict(before=constants['SELF_BEFORE'],after=constants['SELF_AFTER'],count=1)]
    new=text
    for e in edits:assert new.count(e['before'])==1;new=new.replace(e['before'],e['after'],1)
    restored=new
    for e in reversed(edits):assert restored.count(e['after'])==1;restored=restored.replace(e['after'],e['before'],1)
    assert restored==text
    def definitions(source):
        return{n.name:(ast.get_source_segment(source,n),ast.dump(n,include_attributes=False))for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name not in('read_exact','main')}
    assert definitions(text)==definitions(new)
    # Main is a whole exact text transform of the four-line self-Source IO site.
    old_main=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='main')
    new_main=next(n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef)and n.name=='main')
    assert ast.get_source_segment(text,old_main).replace(constants['SELF_BEFORE'],constants['SELF_AFTER'],1)==ast.get_source_segment(new,new_main)
    transport=dict(edits=edits,effective_sha256=hashlib.sha256(new.encode()).hexdigest())
    routes[key]=dict(source_program=q,inputs=inputs,transport=transport,optional_word_pair_input_allowed=False)
    inverses[key]=dict(original=q,original_source_utf8=text,transport=transport,whole_inverse_exact=True,
        unchanged_mathematical_definitions=list(definitions(text)),only_main_self_io_site_changed=True,
        new_execution_program_role=PROGRAM,old_program_field='BORROWED_MATHEMATICAL_SOURCE_NOT_EXECUTION_IDENTITY')
    programs.append(q)
accepted={};extra=[];semantic={}
def label(q,name,role):
    entry=dict(public_path=DATA+name,role=role)
    assert semantic.setdefault(q['path'],entry)==entry
for key in ['proper230','common118']:
    gate,gate_ref=gates[key];area='proper_ends_230'if key=='proper230'else'common_lines_118'
    proofs={role:gate[role]for role in constants['HISTORICAL_PROOF_ROLES']}
    accepted[key]=dict(gate=gate_ref,result=gate['result'],journal=gate['journal'],historical_proofs=proofs)
    extra.extend([gate_ref,gate['result'],gate['journal'],*proofs.values()])
    label(gate_ref,area+'/acceptance.json','ACCEPTED_ROOT_COMPONENT_GATE')
    label(gate['result'],area+'/accepted_result.json','ACCEPTED_MATHEMATICAL_REPORT')
    label(gate['journal'],area+'/certificates.jsonl','ACCEPTED_COMPLETE_CERTIFICATE_JOURNAL')
    for role,q in proofs.items():
        if q['path']not in semantic:
            ext=Path(q['path']).suffix
            label(q,'provenance/'+area+'/'+role+ext,'HISTORICAL_'+role.upper())
selected=union(core,programs,[ap_ref,bp_ref],extra)
lookup={q['path']:q for q in selected}
for q in core:
    if q['path']in semantic:continue
    name=Path(q['path']).name
    if q['sha256']=='e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8':dest='premises/indexed_cayley_catalogue.json'
    elif q['sha256']=='6494e0d434e5b62a68d6966227e361bd3118c8afe936bc9900bd776924c2b8d6':dest='premises/original_prefix8_coordinates.json'
    elif q['sha256']=='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1':dest='premises/cayley_norm.json'
    elif q['sha256']=='38d27708ce1b4be9d10fe24ffae68705d1a63d8f9796c2fd4b7d3fd366b8f6b3':dest='premises/model_source_join.json'
    elif q['sha256']=='cc7bedda717a6bb757185fdf22f73c4efaa0871e540e21f5ba890ef253ae9b94':dest='premises/accepted_prior_3283.json'
    elif Path(name).suffix in('.py','.g'):dest='sources/'+name
    elif Path(name).suffix in('.rst','.tex'):dest='premises/proofs/'+name
    else:dest='premises/history/'+q['sha256'][:16]+'-'+name
    label(q,dest,'UNCHANGED_MATHEMATICAL_CORE')
for q in programs:
    if q['path']not in semantic:label(q,'sources/'+Path(q['path']).name,'BORROWED_MATHEMATICAL_VERIFIER_SOURCE')
assert set(semantic)==set(lookup)
files_by_content={};logical=[]
for q in selected:
    row=semantic[q['path']];identity=(q['bytes'],q['sha256'])
    public=files_by_content.setdefault(identity,dict(path=row['public_path'],bytes=q['bytes'],sha256=q['sha256']))
    logical.append(dict(original=q,public_path=public['path'],role=row['role']))
readme,readme_ref=ordinary(HERE/'README.rst')
public_files=list(files_by_content.values())+[dict(path=PROGRAM,bytes=adapter_ref['bytes'],sha256=adapter_ref['sha256']),dict(path=DATA+'README.rst',bytes=readme_ref['bytes'],sha256=readme_ref['sha256'])]
public_files=sorted(public_files,key=lambda q:q['path'])
assert len({q['path']for q in public_files})==len(public_files)<=256
assert sum(q['bytes']for q in public_files)<=32*2**20 and all(q['bytes']<=2**21 for q in public_files)
premises=dict(
 previous3283=dict(status='BORROWED_ACCEPTED_HISTORY_NOT_REPLAYED',gate=next(q for q in core if q['sha256'].startswith('cc7bedda'))),
 full_natural_image=dict(status='BORROWED_CLASSICAL_FULL_AUT_AND_A_EQUALS_G_JOIN',source=next(q for q in core if q['sha256'].startswith('a754edb5')),join=next(q for q in core if q['sha256'].startswith('38d27708'))),
 faithful_original_prefix=dict(status='BORROWED_PAID_FRAME_AND_ORIGINAL_INDEX_TRANSPORT',export=next(q for q in core if q['sha256'].startswith('6494e0d4')),original_job=[8,4],original_prefix_index=8),
 complete_catalogue=dict(status='BORROWED_ACQUIRED_DOMAIN_AND_ORBIT_REPRESENTATIVES',result=next(q for q in core if q['sha256'].startswith('e7124783'))),
 weights=dict(status='BORROWED_NOT_RECOMPUTED',new_original_weight_credit=0),
 historical_runtime_tables=dict(status='EXACT_DOCUMENTARY_BYTES_ONLY_NOT_FRESH_LEAF_OR_RUNTIME_REPLAY',recursive_history_expansion=False),
 original_recovery=dict(status='NO_WHOLE_PREFIX_OR_PAPER_COMPLETION',whole_original_credit=0))
manifest=dict(schema='F004_PREFIX8_PORTABLE_CERTIFICATE_COMPONENT_V1',scope='CONDITIONAL_SELECTED230_AND118_CERTIFICATES',
 source_author=AUTHOR,private_path_fallback=False,whole_original_credit=0,files=public_files,
 logical_sources=logical,mathematical_core=core,routes=routes,accepted=accepted,imported_premises=premises,
 declared_export_only=True,public_payload_export_performed=False,portable_replay_acquired=False,
 no_runtime_manifest_leaf_freshness_claimed=True)
manifest_raw=dump(manifest);manifest_ref=raw_pin(HERE/'manifest.json',manifest_raw)
inverse=dict(schema='F004_PREFIX8_PORTABLE_IO_SOURCE_TRANSPORT_V1',source_author=AUTHOR,adapter=adapter_ref,
 borrowed_routes=inverses,mathematical_core=dict(count=50,bytes=3005088,tuple_sha256=hashlib.sha256(canon(core)).hexdigest()),
 public_only=True,private_fallback=False,represented_calls=0,scientific_payload_reads=0,scientific_payload_hashes=0,
 role='Finite Source-only IO transport; not a new independent mathematical implementation or portable actual PASS')
inverse_raw=dump(inverse);inverse_ref=raw_pin(HERE/'source_inverse.json',inverse_raw)
plan_path=S/'maintenance/reproducibility/f004_prefix8_and_s16_scopes_publication_plan.rst'
_,plan_ref=ordinary(plan_path,'51821884b9f49d1714e8236b61b1dc775ea8a456ff1fe64df3488fbfa3b1ceb3')
checks=dict(status='COMPLETED_SOURCE_ONLY_PORTABLE_SELECTION_AND_TWO_IO_INVERSES',source_author=AUTHOR,
 fixed_core_count=50,fixed_core_bytes=3005088,old47_is_subset=True,
 historical_logical_files=len(logical),public_files=len(public_files),public_bytes=sum(q['bytes']for q in public_files),
 declared_public_payloads_hashed=False,bytes_physically_exported=0,represented_calls=0,source_imports=0,
 mathematical_helper_sources_and_asts_unchanged=True,per_route_io_edits=2,exact_old_sources_in_inverse=True,
 previous3283_and_model_premises_explicit=True,metadata_and_mathematical_replay_separate=True,
 public_or_git_writes=0,portable_actual_test_owed=True,independent_source_review_owed=True)
checks_raw=dump(checks);checks_ref=raw_pin(HERE/'source_checks.json',checks_raw)
_,own_ref=ordinary(Path(__file__).absolute())
packet=dict(schema='F004_PREFIX8_PORTABLE_CERTIFICATE_ADAPTER_SOURCE_V1',source_author=AUTHOR,
 program=adapter_ref,proposed_public_program=PROGRAM,manifest=manifest_ref,proposed_public_manifest=DATA+'manifest.json',
 inverse=inverse_ref,argument=readme_ref,checks=checks_ref,preparation_source=own_ref,publication_plan=plan_ref,
 parent_mathematical_sources=programs,mathematical_source_packets=[ap_ref,bp_ref],accepted_component_gates=[gates[k][1]for k in ['proper230','common118']],
 expected_distinct_source_status='PASS_DISTINCT_F004_PREFIX8_PORTABLE_CERTIFICATE_ADAPTER_SOURCE',
 late_author_preparation_required=str(HERE/'source_preparation_execution.json'),
 source_only=True,public_tree_modified=False,payload_exported=False,portable_actual_replay=False,
 required_current_source_inputs=[adapter_ref,readme_ref,own_ref,inverse_ref,checks_ref,manifest_ref,plan_ref,ap_ref,bp_ref,*programs,*[gates[k][1]for k in ['proper230','common118']]],
 future_root_duties=['Resolve every literal logical input to actual public bytes and fresh-hash the whole selected package.',
 'Obtain distinct Source review and a genuine selected public-only replay with private paths unavailable.',
 'Introduce only the exact reviewed additive public registration/navigation; preserve original pending statuses.'],
 candidate_credit=0,census_credit=0,whole_original_credit=0)
packet_raw=dump(packet);packet_ref=raw_pin(HERE/'source_packet.json',packet_raw)
outputs=[(HERE/'manifest.json',manifest_raw),(HERE/'source_inverse.json',inverse_raw),(HERE/'source_checks.json',checks_raw),(HERE/'source_packet.json',packet_raw)]
assert all(not p.exists()for p,_ in outputs)
for p,b in outputs:
    with p.open('xb')as f:assert f.write(b)==len(b)
print(json.dumps(dict(status='UNMATERIALIZED_SOURCE_ONLY_PORTABLE_PROPOSAL',program=adapter_ref,manifest=manifest_ref,inverse=inverse_ref,argument=readme_ref,checks=checks_ref,source_packet=packet_ref,preparation_source=own_ref,
 public_files=len(public_files),public_bytes=sum(q['bytes']for q in public_files),logical_files=len(logical),mathematical_core_files=50,mathematical_core_bytes=3005088,
 represented_calls=0,scientific_payload_reads=0,scientific_payload_hashes=0,public_writes=0,portable_replay_acquired=False),sort_keys=True))
