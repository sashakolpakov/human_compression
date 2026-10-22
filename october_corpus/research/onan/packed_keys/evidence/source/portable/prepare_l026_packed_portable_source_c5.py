#!/usr/bin/env python3
"""Plain Source/ordinary-proof assembly only. No represented program is loaded."""
from pathlib import Path
import ast
import hashlib
import json
import re

S=Path('/Users/sasha/medusa/research/leemans')
CORE=S/'geometry/onan_regular_maps/permutation_model/middle_partition/packed_conjugacy_keys'
D=CORE/'portable_io'
METHOD=Path(__file__).resolve()
PROGRAMS={'portable':D/'portable.py','native':D/'portable_cli.c','exporter':D/'export_maps.g',
 'export_driver':D/'export_driver.g','controls':D/'controls_io.py',
 'kernel':CORE/'packed_keys.c','header':CORE/'packed_keys.h','core_controls':CORE/'controls.c'}
BORROWED=[
 CORE/'source_packet.json',CORE/'source_freeze.json',CORE/'source_inverse.json',
 CORE/'source_preparation_execution.json',CORE/'ARGUMENT.rst',CORE/'INTERFACE.rst',
 CORE/'distinct_source_review.json',CORE/'distinct_source_execution.json',
 S/'geometry/onan_regular_maps/permutation_model/middle_partition/rank_blocks.g',
 S/'geometry/sporadic_polytopes/endpoint_method_work/lazy_coset_rank_work/index.g',
 S/'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_work/argument.rst',
 S/'geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_root_review/review.json',
 S/'geometry/sporadic_polytopes/endpoint_method_work/streamed_conjugacy_fusion_work/argument.rst',
 S/'geometry/sporadic_polytopes/endpoint_method_work/streamed_conjugacy_fusion_root_review/review.json',
 S/'geometry/onan_regular_maps/permutation_model/endpoint_setup/README.rst',
 S/'geometry/onan_regular_maps/permutation_model/endpoint_setup/validation/setup/root_certificate_acceptance.json',
 S/'geometry/onan_regular_maps/permutation_model/endpoint_setup/validation/setup/output/report.json',
 S/'geometry/onan_regular_maps/permutation_model/middle_partition/endpoint_elements/direct_point_rows_named_continuation/launch.py',
 Path('/opt/homebrew/Cellar/gap/4.15.1/share/gap/lib/streams.gd'),
 Path('/opt/homebrew/Cellar/gap/4.15.1/share/gap/lib/streams.gi'),
]
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,j):p.write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
def lexical_c(text):
    clean=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '',text,flags=re.S)
    stack=[];op={'(':')','{':'}','[':']'}
    for c in clean:
        if c in op:stack.append(op[c])
        elif c in op.values():assert stack and stack.pop()==c
    assert not stack
def main():
    inputs=sorted(set([METHOD,*PROGRAMS.values(),*BORROWED,D/'ARGUMENT.rst',D/'INTERFACE.rst']),key=str)
    before={str(p):pin(p)for p in inputs}
    cp=json.loads((CORE/'source_packet.json').read_bytes())
    cr=json.loads((CORE/'distinct_source_review.json').read_bytes())
    ce=json.loads((CORE/'distinct_source_execution.json').read_bytes())
    assert before[str(CORE/'packed_keys.c')]['sha256']=='4be81f03c9be5ffdebf81dbd506ce7967561d8eff7fd9db73d8ec6de04e4c53a'
    assert before[str(CORE/'packed_keys.h')]['sha256']=='c208f29e960a08fa1e3a29ca6d389cfb63ebbd9bd3fa1d3b1ccfa7830c524d73'
    assert before[str(CORE/'controls.c')]['sha256']=='ef315d0000a97450b21ab6d11561d0864c713c5d11d2c7aaf4f99774107f032f'
    assert before[str(CORE/'distinct_source_review.json')]['sha256']=='b11323c0ddc59c5acabdfe17d3656ca05cffa5629ba977ef7bbd36b6f1d7512d'
    assert before[str(CORE/'distinct_source_execution.json')]['sha256']=='b60e3255d958fa97e26211dea7fa8873e5fe3b6b5eb55666c2d9978de84652c2'
    assert ce['actor']==cr['reviewer']and ce['review']==before[str(CORE/'distinct_source_review.json')]
    for j in [cr,ce]:assert j['programs']==cp['programs']and j['blockers']==[]and j['late_author_preparation']==before[str(CORE/'source_preparation_execution.json')]
    setup=json.loads(BORROWED[15].read_bytes());report=json.loads(BORROWED[16].read_bytes())
    assert before[str(BORROWED[15])]['sha256']=='42d0261db2ef8a613df9382e08fddb5dfda8c3e87215a715a43464d74a56e21c'
    assert before[str(BORROWED[16])]['sha256']=='1ac994bee3a815bd044e2f60ee82ac23ed73bb8499ba414613f6f9a08c2f87cf'
    assert setup['inner_stabilizer_orders']==[256,144]
    assert [(e['index'],e['pointwise_inner_order'],e['J_class_size'],len(e['generators']))for e in report['endpoints']]==[(1,256,630,4),(2,144,1120,4)]
    texts={k:p.read_text()for k,p in PROGRAMS.items()}
    parsed={k:ast.parse(texts[k],filename=str(PROGRAMS[k]))for k in ['portable','controls']}
    lexical_c(texts['native'])
    for token in ['#include "../packed_keys.c"','restore_closed_node','verify_old_transitions','pck_check_append','pck_check_orbit','wbx','PCKFEED1','synthetic_only']:
        assert token in texts['native']
    assert 'pck_close(' not in texts['native'].split('if(check){',1)[1].split('}else{',1)[0]
    assert 'canonical(native)==canonical(expected)'in texts['portable']
    assert 'native_invoked=False'in texts['portable'] and 'exact_authenticated_bytes_streamed_to_child=True'in texts['portable']
    names=re.findall(r"names\.append\('([^']+)'\)",texts['controls']);assert len(names)==len(set(names))==10
    assert 'SetPrintFormattingStatus(stream,false)'in texts['exporter'] and 'WriteAll(stream,buffer)'in texts['exporter']
    assert 'base.index.root.chain'in texts['exporter'] and 'Read('not in texts['exporter']
    assert 'rank_blocks.g'not in texts['export_driver']
    source_functions={k:[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]for k,tree in parsed.items()}
    inv=dict(schema='L026_PACKED_PORTABLE_WHOLE_CONSTRUCTION_V1',source_author='C5',
      whole_new_sources={k:dict(pin=before[str(PROGRAMS[k])],utf8=texts[k])for k in ['portable','native','exporter','export_driver','controls']},
      unchanged_whole_included_sources={k:dict(pin=before[str(PROGRAMS[k])],utf8=texts[k])for k in ['kernel','header','core_controls']},
      whole_included_core_is_byte_exact=True,core_global_or_macro_rebinding=False,
      new_private_restore_adapter='Explicit closed-parent attribution using unchanged append; no historical word arithmetic replay claim.',
      previous_named_checkpoint_transfer='UNPAID; no old rank/node relabel.',python_source_definitions=source_functions)
    write(D/'source_inverse.json',inv)
    checks=dict(schema='SOURCE_ONLY_L026_PACKED_PORTABLE_CHECKS_V1',status='SOURCE_ASSEMBLED_UNCOMPILED_UNINVOKED',
      plain_python_AST_parsed=list(parsed),C_lexical_delimiters_only=True,C_compilation=False,
      frozen_core_full_byte_identity=True,core_source_actor_map_peer_join=True,
      actual_endpoint_orders=[256,144],actual_endpoint_generators=[4,4],IO_control_names=names,
      controls_unrun=10,core_controls_not_reexecuted=18,workspace_or_model_or_payload_body_reads=False,
      no_represented_import_or_helper_or_guard_or_liveness_or_state_call=True,
      physical_fit=False,partition_credit=0,whole_original_credit=0)
    write(D/'source_checks.json',checks)
    rows=[before[k]for k in sorted(before)]+[pin(D/'source_inverse.json'),pin(D/'source_checks.json')]
    rows=sorted(rows,key=lambda r:r['path'])
    write(D/'source_readset.json',dict(schema='L026_PACKED_PORTABLE_SOURCE_READSET_V1',inputs=rows,rows=len(rows),bytes=sum(x['bytes']for x in rows),
      closed_ancestor_tables_not_recursively_freshened=True,no_workspace_or_math_payload_body_hash=True))
    current=sorted(rows+[pin(D/'source_readset.json')],key=lambda r:r['path'])
    packet=dict(schema='L026_PACKED_PORTABLE_SOURCE_V1',source_author='C5',program=pin(PROGRAMS['portable']),
      programs={k:pin(p)for k,p in PROGRAMS.items()},inverse=pin(D/'source_inverse.json'),argument=pin(D/'ARGUMENT.rst'),
      interface=pin(D/'INTERFACE.rst'),checks=pin(D/'source_checks.json'),method=pin(METHOD),source_readset=pin(D/'source_readset.json'),
      required_current_source_inputs=current,
      closed_core_source=dict(program=cp['program'],source_packet=pin(CORE/'source_packet.json'),source_review=pin(CORE/'distinct_source_review.json'),source_execution=pin(CORE/'distinct_source_execution.json')),
      actual_endpoint_setup=dict(acceptance=pin(BORROWED[15]),report=pin(BORROWED[16])),
      expected_review_status='PASS_DISTINCT_L026_PACKED_CLASS_PORTABLE_SOURCE',
      expected_execution_status='COMPLETED_GENUINE_DISTINCT_L026_PACKED_CLASS_PORTABLE_SOURCE_REVIEW',
      future_mandatory_preparation_path=str(D/'source_preparation_execution.json'),
      expected_control_count=10,controls_status='UNRUN',runtime_compile_export_target_fit='UNACQUIRED',
      bounds=dict(outer_rss_bytes=536870912,outer_wall_seconds=150,metadata_self_rss_bytes=134217728,
        metadata_check_seconds=140,native_work_cpu_seconds=20,native_total_cpu_seconds=100,native_rss_bytes=402653184,
        tape_bytes=402653184,piece_bytes=67108864,source_runtime_files=1024,source_runtime_bytes=134217728,
        opaque_data_logical_bytes=2147483648,max_new_nodes=65536,max_new_orbits=65536,max_blocks=65536),
      qualified_new_scope='Exact raw binary input/maps and whole portable tape IO; closed parent restored by attributed authority; every new key/word/edge/cursor prefix Saved-verified. New big-data domains explicit, not old profile coverage.',
      old4097_transfer='UNPAID',endpoint2_known_catalogue_partition='Separate future consumer; no T-context mixing.',
      generation_counted=False,whole_original_credit=0)
    write(D/'source_packet.json',packet)
    assert all(pin(Path(k))==v for k,v in before.items())
    full=sorted(current+[pin(D/'source_packet.json')],key=lambda r:r['path'])
    print(json.dumps(dict(status='COMPLETED_SOURCE_ONLY_PACKED_PORTABLE_ASSEMBLY',
      programs=packet['programs'],packet=pin(D/'source_packet.json'),required_root_admission_inputs=full,
      rows=len(full),bytes=sum(x['bytes']for x in full),C_compilation=False,represented_calls=False,controls_unrun=10),sort_keys=True))
if __name__=='__main__':main()
