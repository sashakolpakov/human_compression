#!/usr/bin/env python3
"""Source assembly only: no compilation, represented imports or target reads."""
from pathlib import Path
import hashlib
import json
import re

S=Path('/Users/sasha/medusa/research/leemans')
D=S/'geometry/onan_regular_maps/permutation_model/middle_partition/packed_conjugacy_keys'
METHOD=Path(__file__).resolve()
BORROWED=[
 'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_work/argument.rst',
 'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_work/fusion.g',
 'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_root_review/manifest.json',
 'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_root_review/review.json',
 'geometry/sporadic_polytopes/endpoint_method_work/streamed_conjugacy_fusion_work/argument.rst',
 'geometry/sporadic_polytopes/endpoint_method_work/streamed_conjugacy_fusion_root_review/manifest.json',
 'geometry/sporadic_polytopes/endpoint_method_work/streamed_conjugacy_fusion_root_review/review.json',
 'geometry/sporadic_polytopes/endpoint_method_work/orbit_graph_work/orbit_graph.tex',
 'geometry/onan_regular_maps/permutation_model/endpoint_setup/README.rst',
 'geometry/onan_regular_maps/permutation_model/endpoint_setup/source_packet.json',
 'geometry/onan_regular_maps/permutation_model/middle_partition/README.rst',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/checkpoint_hex/endpoint_elements.g',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/driver.g',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/route_tree_cache/direct_point_rows/route_trees.g',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/runs/four_orbits_from_thirteen/produce/output/report.g',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/runs/four_orbits_from_thirteen/produce/observation/receipt.json',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/runs/four_orbits_from_thirteen/check/observation/receipt.json',
 'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/runs/four_orbits_from_thirteen/root_acceptance.json',
]
OWN=['packed_keys.h','packed_keys.c','controls.c','ARGUMENT.rst','INTERFACE.rst','RESOURCE_AND_NEXT_STAGE.rst']
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,j):
    p.write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
def lexical_c(text):
    """Delimiter check only; explicitly not a C compiler or semantic verifier."""
    clean=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '',text,flags=re.S)
    stack=[];op={'(':')','{':'}','[':']'}
    for c in clean:
        if c in op: stack.append(op[c])
        elif c in op.values():
            assert stack and stack.pop()==c
    assert not stack
def main():
    before={str(p):pin(p) for p in [METHOD,*[D/x for x in OWN],*[S/x for x in BORROWED]]}
    texts={name:(D/name).read_text() for name in OWN}
    for name in ['packed_keys.h','packed_keys.c','controls.c']:lexical_c(texts[name])
    controls=re.findall(r'pass\("([^"]+)"\)',texts['controls.c'])
    assert len(controls)==len(set(controls))==18
    assert 'NEED(passed==18)' in texts['controls.c']
    assert 'c->count==before)return PCK_OLD' in texts['packed_keys.c']
    assert 'memcmp(key,c->keys+' in texts['packed_keys.c']
    assert 'return tail==orbit->weight?PCK_OK:PCK_BAD;' in texts['packed_keys.c']
    assert 'sizeof(struct pck_context)<=256' in texts['packed_keys.c']
    direct=(S/BORROWED[0]).read_text()
    assert 'b^(t^-1 z t) = ((b/t)^z)^t' in direct
    endpoint=json.loads((S/BORROWED[9]).read_bytes())
    gate=json.loads((S/BORROWED[-1]).read_bytes())
    assert gate['adopted'] is True and (gate['covered'],gate['orbit_count'],gate['cursor'])==(4097,17,18)
    assert before[str(S/BORROWED[-1])]['sha256']=='33a1d7e2338a276238003bef820223bd39129852fce78f1559199c5a9fdecc92'
    resource=[]
    for phase,rel in [('produce',BORROWED[-3]),('check',BORROWED[-2])]:
        j=json.loads((S/rel).read_bytes())
        assert j['status']=='PASS' and j['returncode']==0
        assert j['limits']['total_rss']==536870912 and j['limits']['wall_seconds']==150
        resource.append(dict(phase=phase,receipt=pin(S/rel),seconds=j['seconds'],peaks=j['peaks']))
    inverse=dict(schema='L026_PACKED_KEYS_NEW_SOURCE_CONSTRUCTION_V1',
      source_author='C5',unchanged_program_body_claim=False,c_compilation=False,
      whole_new_programs={name:dict(pin=pin(D/name),utf8=texts[name]) for name in ['packed_keys.h','packed_keys.c','controls.c']},
      borrowed_mathematics=[pin(S/BORROWED[i]) for i in [0,2,3,4,5,6,7]],
      exact_borrowed_formula='b^(t^-1 z t) = ((b/t)^z)^t',
      changed_representation='Exact 17-bit whole-base keys, fixed open addressing, literal earlier-parent factors, atomic orbit closure and supplied-edge Saved verification.',
      prior_accepted_programs_and_proofs_modified=False)
    write(D/'source_inverse.json',inverse)
    checks=dict(schema='SOURCE_ONLY_L026_PACKED_KEYS_CHECKS_V1',
      status='SOURCE_ASSEMBLED_NOT_COMPILED_OR_EXECUTED',
      checks=['Full new C/header/control Source retained in construction inverse.',
              'Lexical delimiter balance only, not compiler/semantic execution.',
              'All eighteen distinct control names present; controls remain UNRUN.',
              'Full-byte dictionary comparison, duplicate sentinel and supplied-edge/reachability paths present.',
              'Current accepted parent and ordinary receipt scalar fields joined.'],
      expected_controls=controls,resource_metadata=resource,
      no_target_or_payload_read=True,no_guard_or_liveness_or_state_call=True,
      control_or_target_fit=False,whole_original_credit=0)
    write(D/'source_checks.json',checks)
    rows=[before[k] for k in sorted(before)]
    write(D/'source_readset.json',dict(schema='L026_PACKED_KEYS_SOURCE_READSET_V1',
      current_source_and_ordinary_metadata=rows,rows=len(rows),bytes=sum(r['bytes'] for r in rows),
      historical_dependency_tables_are_closed_not_recursively_opened=True,
      no_workspace_model_or_scientific_payload_read_or_hash=True))
    programs={k:pin(D/v) for k,v in dict(kernel='packed_keys.c',header='packed_keys.h',controls='controls.c').items()}
    packet=dict(schema='L026_PACKED_CONJUGACY_KEYS_SOURCE_V1',source_author='C5',
      program=programs['kernel'],programs=programs,inverse=pin(D/'source_inverse.json'),
      argument=pin(D/'ARGUMENT.rst'),interface=pin(D/'INTERFACE.rst'),checks=pin(D/'source_checks.json'),
      method=pin(METHOD),resource_note=pin(D/'RESOURCE_AND_NEXT_STAGE.rst'),
      source_readset=pin(D/'source_readset.json'),source_inputs=rows,
      closed_authorities=dict(direct_key_review=pin(S/BORROWED[3]),
        fusion_review=pin(S/BORROWED[6]),endpoint_source=pin(S/BORROWED[9]),
        acquired_named_parent=pin(S/BORROWED[-1]),endpoint_premises=endpoint['premises']),
      expected_review_status='PASS_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE',
      expected_execution_status='COMPLETED_GENUINE_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE_REVIEW',
      future_mandatory_preparation_path=str(D/'source_preparation_execution.json'),
      controls=dict(expected_count=18,status='UNRUN',program=programs['controls']),
      bounds=dict(max_degree=131072,max_class=2857239,max_base=20,max_factors=16,
        max_endpoint_order=256,max_word=8192,max_key_bytes=43,hash_slots=8388608,
        max_retained_core_bytes=184805296,max_borrowed_maps_bytes=8912896,
        temporary_seen_bytes=131072,prospective_outer_rss_bytes=536870912,
        prospective_outer_wall_seconds=150,physical_fit_acquired=False),
      current_scope='New representation/acquisition core. Portable IO, actual base/map export, runtime/toolchain admission and guarded production/Saved wrapper still owed.',
      conclusions=dict(new_partition_acquired=False,generation_acquired=False,reversal_acquired=False,whole_original_credit=0))
    write(D/'source_packet.json',packet)
    assert all(pin(Path(path))==row for path,row in before.items())
    allpaths=[*[Path(k) for k in before],D/'source_inverse.json',D/'source_checks.json',D/'source_readset.json',D/'source_packet.json']
    full=sorted([pin(p) for p in allpaths],key=lambda r:r['path'])
    print(json.dumps(dict(status='COMPLETED_SOURCE_ONLY_PACKED_KEYS_ASSEMBLY',
      controls_unrun=18,compilation=False,target_calls=False,programs=programs,
      packet=pin(D/'source_packet.json'),required_root_admission_inputs=full,
      rows=len(full),bytes=sum(r['bytes'] for r in full)),sort_keys=True))
if __name__=='__main__':main()
