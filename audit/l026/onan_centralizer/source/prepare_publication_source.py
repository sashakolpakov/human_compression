"""Assemble a private additive publication Source proposal; no Git or payload IO."""
import ast
import hashlib
import json
from pathlib import Path

D=Path(__file__).resolve().parent
R=D.with_name('l026_onan_centralizer')
P=Path('/Users/sasha/medusa/math_compression')
OPENED={}

def pin(path):
 p=Path(path);assert p.resolve()==p and p.is_file()and not p.is_symlink()and p.stat().st_size<=2**20
 raw=p.read_bytes();q=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());OPENED[str(p)]=q;return q
def read(path):pin(path);return json.loads(Path(path).read_bytes())
def put(path,value):
 raw=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
 with Path(path).open('xb')as f:assert f.write(raw)==len(raw)
 return pin(path)
def write(path,value):
 with Path(path).open('x')as f:assert f.write(value)==len(value)
 return pin(path)
def body(source,name):
 n=next(x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef)and x.name==name)
 return ast.get_source_segment(source,n)

plan=read(R/'registration_plan.json');proposal=read(R/'source_packet.json')
assert pin(R/'registration_plan.json')==proposal['registration_plan']
assert pin(R/'source_packet.json')['sha256']=='2693d874a455f174d0c4604cbe858f746f59c364b384adddff314c3d5cb917d0'
assert plan['baseline']=='4512492579d2809c32cadeda9250ae26ce661616'
for key in ['old_dispatch','old_guide','predecessor_registration','predecessor_policy']:
 assert pin(plan[key]['path'])==plan[key]
pin(D/'README.rst');pin(D/'registration_template.py');pin(__file__)
old_policy=read(plan['predecessor_policy']['path'])
old_code=Path(plan['predecessor_registration']['path']).read_text()
old_dispatch=Path(plan['old_dispatch']['path']).read_text();old_guide=Path(plan['old_guide']['path']).read_text()
pin(R/'guide_append.rst');unit_append=(R/'guide_append.rst').read_text()
guide_extra='''

Exact additive ON publication registration
------------------------------------------

The current ON layer retains the complete45124925 predecessor and its nested
G2/historical logic in an explicit frozen read/Git view. It separately checks
the entire actual current delta and exact8-file package. Metadata integrity
does not repeat a group calculation or grant census/whole L026 credit.
After real Source/replay proofs exist, Root supplies their exact finite frozen
publication_manifest.json and publication_delta.json under
audit/l026/onan_centralizer, prepares registration with both explicit SHA256
arguments, stages only that layer, and runs scripts/verify_snapshot.py. Read
audit/l026/onan_centralizer/README.rst for the exact schemas and commands.
The old strict CLI is never claimed to pass this enlarged tree.
'''
append=unit_append+guide_extra
new_main='''def main():
    spec = importlib.util.spec_from_file_location('onan_centralizer_publication_registration',
        ROOT/'scripts/onan_centralizer/registration.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    current = module.verify(ROOT, require_tracked=True)
    print(json.dumps(current, sort_keys=True))
    print('PASS: additive ON centralizer certificate; 102 fully treated originals and 3 remaining.')
    print('Scope: frozen45124925 G2 predecessor plus exact current delta; no fresh whole-corpus replay.')'''
old_main=body(old_dispatch,'main');assert old_dispatch.count(old_main)==1
new_dispatch=old_dispatch.replace(old_main,new_main,1)
assert new_dispatch.replace(new_main,old_main,1)==old_dispatch
before={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(old_dispatch).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name!='main'}
after={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(new_dispatch).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name!='main'}
assert before==after
new_read="""def read(root,name,cap=4*2**20):
    need(Path(root).absolute()==FROZEN_ROOT,'explicit frozen4512492 root')
    return FROZEN_READ(relative(name),cap)"""
new_git="""def git(root,*args):
    need(Path(root).absolute()==FROZEN_ROOT,'explicit frozen4512492 root')
    return FROZEN_GIT(tuple(args))"""
edits=[dict(before=body(old_code,'read'),after=new_read,occurrences=1),
       dict(before=body(old_code,'git'),after=new_git,occurrences=1)]
derived=old_code
for e in edits:assert derived.count(e['before'])==1;derived=derived.replace(e['before'],e['after'],1)
back=derived
for e in reversed(edits):assert back.count(e['after'])==1;back=back.replace(e['after'],e['before'],1)
assert back==old_code
for n in ast.parse(old_code).body:
 if isinstance(n,ast.FunctionDef)and n.name not in {'read','git'}:
  assert body(old_code,n.name)==body(derived,n.name)
prefix='audit/l026/onan_centralizer/'
source_docs=[prefix+x for x in ['README.rst','publication_source_packet.json','publication_source_inverse.json',
 'publication_source_checks.json','publication_source_preparation_execution.json',
 'publication_source_review.json','publication_source_execution.json']]
portable_docs=[prefix+x for x in ['PORTABLE.rst','portable_source_packet.json','portable_source_inverse.json',
 'portable_source_checks.json','portable_source_preparation_execution.json','portable_source_review.json',
 'portable_source_execution.json','portable_registration_plan.json','portable_copy_recipe.json']]
root_docs=[prefix+'root_staged_export.json',prefix+'root_portable_replay_execution.json']
modes=['all','standard-controls','standard-pair','pair-controls','check-centralizer']
replay_docs=[prefix+'replay/'+mode+'/'+name for mode in modes for name in ['portable_receipt.json','guard_receipt.json','result.json']]
optional_sources=[prefix+'source/'+name for name in ['prepare_portable_source.py','portable_source_method.py',
 'prepare_publication_source.py','publication_source_method.py']]
fixed=sorted(plan['proposed_additions'],key=lambda q:q['path'])
by={q['path']:q for q in fixed};assert len(fixed)==8
assert sum(q['bytes']for q in fixed)==4561806
code='scripts/onan_centralizer/registration.py';policy_name=prefix+'publication_policy.json'
required=sorted(set(by)|set(source_docs)|{prefix+'portable_source_packet.json',prefix+'portable_source_review.json',
 prefix+'portable_source_execution.json',*root_docs,code,policy_name,'scripts/verify_snapshot.py','docs/REPRODUCING.rst'})
frozen_names=sorted(set([q['path']for q in old_policy['fixed_files']]+old_policy['source_documents']+
 ['scripts/g2_prefix8_certificates/registration.py','audit/f004/prefix8_certificates/publication_policy.json',
  'audit/f004/prefix8_certificates/registration.json','scripts/verify_snapshot.py','docs/REPRODUCING.rst']))
historical=sorted(set('ce9970599fc1e7334f9f3f74ae37929346fbe4ad:'+name for name in
 old_policy['old_current_read_names']+[old_policy['old_code']['path'],'scripts/verify_snapshot.py','docs/REPRODUCING.rst'])|
 set('de0864a7bde3c992239427d3c838fe0fe8ea370d:'+name for name in old_policy['old_historical_read_names']))
policy=dict(schema='ONAN_CENTRALIZER_4512492_PUBLICATION_POLICY_V1',baseline=plan['baseline'],
 old_registration=dict(plan['predecessor_registration'],path='scripts/g2_prefix8_certificates/registration.py'),
 old_g2_policy=dict(plan['predecessor_policy'],path='audit/f004/prefix8_certificates/publication_policy.json'),
 old_dispatch=dict(plan['old_dispatch'],path='scripts/verify_snapshot.py'),old_guide=dict(plan['old_guide'],path='docs/REPRODUCING.rst'),
 package_files=fixed,package_program=by['scripts/onan_centralizer/check.py'],
 package_manifest=by['data/onan_centralizer/manifest.json'],tree=by['data/onan_centralizer/pairs.bin'],
 required_files=required,allowed_files=sorted(set(required)|set(portable_docs+replay_docs+optional_sources)),
 frozen_current_read_names=frozen_names,historical_show_specs=historical,
 predecessor_IO_transport=dict(edits=edits,effective_sha256=hashlib.sha256(derived.encode()).hexdigest(),
     all_other_functions_Source_AST_unchanged=True,current_physical_modes_separately_prevalidated=True),
 dispatcher_inverse=dict(before=old_main,after=new_main),guide_append=append,
 routes={'standard-controls':'PASS_FOCUSED_LITERAL_PERMUTATION_CONTROLS',
 'standard-pair':'VERIFIED_CACHED_ON_STANDARD_PAIR_WORD_ORDERS',
 'pair-controls':'PASS_FOCUSED_CENTRALIZER_PAIR_ORBIT_CONTROLS',
 'check-centralizer':'VERIFIED_REACHABLE_CENTRALIZER_PAIR_TREE'},
 historical_g2_cutoff=dict(prior_borrowed=3283,proper230=230,common118=118,unpaid=148),
 fully_treated_originals=102,mathematical_originals=105,pending=['F004','F009','L026'],
 mathematical_payloads_read_or_hashed_or_copied=0,whole_original_credit=0)
policy_ref=put(D/'publication_policy.json',policy)
template=(D/'registration_template.py').read_text();assert template.count('__PUBLICATION_POLICY_SHA256__')==1
program=write(D/'registration.py',template.replace('__PUBLICATION_POLICY_SHA256__',policy_ref['sha256']))
dispatch=write(D/'verify_snapshot.py',new_dispatch);guide=write(D/'REPRODUCING.rst',old_guide+append)
ast.parse((D/'registration.py').read_text())
inverse=put(D/'source_inverse.json',dict(schema='ONAN_CENTRALIZER_PUBLICATION_SOURCE_INVERSE_V1',
 old_registration=plan['predecessor_registration'],whole_old_registration_utf8=old_code,
 predecessor_IO_transport=policy['predecessor_IO_transport'],old_dispatch=plan['old_dispatch'],
 whole_old_dispatch_utf8=old_dispatch,dispatcher_inverse=policy['dispatcher_inverse'],
 unchanged_dispatcher_definitions=sorted(before),old_guide=plan['old_guide'],whole_old_guide_utf8=old_guide,
 guide_append=append,dispatcher=dispatch,guide=guide,registration_program=program,
 proposed_payloads_read_or_hashed_or_copied=0,git_calls=0,represented_calls=0))
checks=put(D/'source_checks.json',dict(status='PASSED_SOURCE_ONLY_ONAN_ADDITIVE_PUBLICATION_ASSEMBLY',
 program=program,policy=policy_ref,dispatcher=dispatch,guide=guide,whole_dispatcher_inverse=True,
 unchanged_dispatcher_definitions=len(before),whole_old_G2_inverse=True,
 unchanged_old_G2_functions=sum(isinstance(n,ast.FunctionDef)and n.name not in {'read','git'}for n in ast.parse(old_code).body),
 fixed_package_files=len(fixed),declared_package_bytes=sum(q['bytes']for q in fixed),
 frozen_predecessor_read_names=len(frozen_names),finite_allowed_paths=len(policy['allowed_files']),
 actual_manifest_or_delta_or_registration_created=False,public_writes=0,git_calls=0,represented_calls=0))
packet=put(D/'source_packet.json',dict(schema='ONAN_CENTRALIZER_ADDITIVE_PUBLICATION_SOURCE_PACKET_V1',
 source_author='/root/resource_cleanup_audit',program=program,publication_policy=policy_ref,
 dispatcher=dispatch,guide=guide,argument=pin(D/'README.rst'),inverse=inverse,checks=checks,
 portable_source_packet=pin(R/'source_packet.json'),registration_plan=pin(R/'registration_plan.json'),
 expected_source_status='PASS_DISTINCT_L026_ONAN_CENTRALIZER_PUBLICATION_SOURCE',
 expected_source_execution_status='COMPLETED_GENUINE_DISTINCT_L026_ONAN_CENTRALIZER_PUBLICATION_SOURCE_REVIEW',
 expected_peer_basename='distinct_source_review.json',expected_execution_basename='distinct_source_execution.json',
 mandatory_late_author_proof=str(D/'source_preparation_execution.json'),
 required_source_inputs=sorted(OPENED.values(),key=lambda q:q['path']),
 future_frozen_manifest_and_delta_required=True,public_writes=0,git_calls=0,represented_calls=0,
 mathematical_payloads_read_or_hashed_or_copied=0,whole_original_credit=0))
print(json.dumps(dict(program=program,policy=policy_ref,source_packet=packet,inverse=inverse,
 dispatcher=dispatch,guide=guide,checks=checks,source_rows=len(OPENED),
 represented_calls=0,public_writes=0,git_calls=0),sort_keys=True))
