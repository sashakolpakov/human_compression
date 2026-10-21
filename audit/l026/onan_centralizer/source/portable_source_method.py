"""Independent Source/AST/ordinary-metadata audit; never execute the proposal."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

R = Path(__file__).resolve().parent
S = R.parents[2]
ACTOR = '/root/resource_cleanup_audit'
AUTHOR = '/root/unit_actual_review'
START = time.monotonic()
OPENED = {}
PACKET_SHA = '2693d874a455f174d0c4604cbe858f746f59c364b384adddff314c3d5cb917d0'
LATE_SHA = 'eb1dea4e0f0baa65f89151d0611445a486dd952ff545ca48c235d97b4097364c'
STATUS = 'PASS_DISTINCT_L026_ONAN_CENTRALIZER_PORTABLE_SOURCE'


def need(ok, why):
    if not ok:
        raise ValueError(why)
    if time.monotonic() - START > 30:
        raise RuntimeError('bounded Source audit')


def pin(raw, path):
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def signature(a):
    return (a.st_dev, a.st_ino, a.st_mode, a.st_nlink, a.st_size,
            a.st_mtime_ns, a.st_ctime_ns)


def read(path, expected=None):
    path = Path(path)
    need(path.is_absolute() and path.resolve(strict=True) == path,
         'literal ordinary Source/metadata path')
    need(not path.name.endswith(('.g1', '.g2', '.bin')),
         'model and tree payload reads prohibited')
    a = path.lstat()
    need(stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and a.st_size <= 4*2**20,
         'bounded ordinary Source/metadata file')
    with path.open('rb') as stream:
        b = os.fstat(stream.fileno())
        raw = stream.read(4*2**20 + 1)
        z = os.fstat(stream.fileno())
    need(signature(a) == signature(b) == signature(z) == signature(path.lstat())
         and len(raw) == a.st_size, 'stable whole ordinary Source/metadata')
    q = pin(raw, path)
    if expected is not None:
        need(set(expected) == {'path', 'bytes', 'sha256'} and q == expected,
             'exact handed ordinary Source/metadata pin')
    previous = OPENED.get(str(path))
    need(previous is None or previous == q, 'same repeated Source identity')
    OPENED[str(path)] = q
    return raw


def decode(path, expected=None):
    return json.loads(read(path, expected))


def defs(text):
    tree = ast.parse(text)
    return {n.name: ast.get_source_segment(text, n)
            for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


def literal(tree, name):
    hits = [n.value for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    need(len(hits) == 1, 'one literal Source declaration: ' + name)
    return ast.literal_eval(hits[0])


def put(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    need(len(raw) <= 2*2**20, 'bounded reviewer output')
    with path.open('xb') as stream:
        need(stream.write(raw) == len(raw), 'whole fresh reviewer output')
        stream.flush()
        os.fsync(stream.fileno())
    return pin(raw, path)


def main():
    packet_raw = read(R/'source_packet.json')
    packet_ref = pin(packet_raw, R/'source_packet.json')
    need(packet_ref['sha256'] == PACKET_SHA, 'frozen Source packet')
    packet = json.loads(packet_raw)
    late_raw = read(R/'source_preparation_execution.json')
    late_ref = pin(late_raw, R/'source_preparation_execution.json')
    need(late_ref['sha256'] == LATE_SHA, 'mandatory late genuine author receipt')
    late = json.loads(late_raw)
    need(packet['source_author'] == AUTHOR and AUTHOR != ACTOR,
         'distinct Source author and reviewer')
    need(packet['expected_source_status'] == STATUS
         and packet['expected_peer_basename'] == 'distinct_source_review.json'
         and packet['expected_execution_basename'] == 'distinct_source_execution.json',
         'exact expected Source peer ABI')
    rows = packet['required_source_inputs']
    need(len(rows) == 26 and len({q['path'] for q in rows}) == 26,
         'finite exact Source-only declared roster')
    for q in rows:
        read(q['path'], q)
    need(sum(q['bytes'] for q in OPENED.values()) <= 8*2**20,
         'bounded complete Source/ordinary-metadata readset')
    inverse = decode(packet['inverse']['path'], packet['inverse'])
    facade = read(packet['program']['path'], packet['program']).decode()
    tree = ast.parse(facade)
    manifest = decode(packet['manifest']['path'], packet['manifest'])
    recipe = decode(packet['copy_recipe']['path'], packet['copy_recipe'])
    plan = decode(packet['registration_plan']['path'], packet['registration_plan'])
    need(inverse['schema'] == 'ONAN_CENTRALIZER_IO_FACADE_SOURCE_INVERSE_V1'
         and inverse['scientific_text_edits'] == []
         and inverse['copied_Source_whole_bytes_identical'] is True
         and inverse['no_private_fallback'] is True
         and inverse['old_private_CLI_PASS_retargeted'] is False,
         'truthful whole Source inverse and unchanged mathematical bodies')
    body_counts = {}
    for name, field in [('standard', 'whole_original_standard_Source_utf8'),
                        ('pair', 'whole_original_pair_Source_utf8')]:
        old = next(q for q in inverse['originals']
                   if q['sha256'] == packet['programs'][name]['sha256'])
        original = read(old['path'], old).decode()
        copied = read(packet['programs'][name]['path'], packet['programs'][name]).decode()
        need(original == copied == inverse[field], 'exact complete original Source: ' + name)
        need(defs(original) == defs(copied), 'all original Source definitions: ' + name)
        body_counts[name] = len(defs(original))
    need(literal(tree, 'MANIFEST_SHA') == packet['manifest']['sha256']
         and literal(tree, 'MANIFEST') == 'data/onan_centralizer/manifest.json'
         and literal(tree, 'MODES') == ('standard-controls', 'standard-pair',
                                       'pair-controls', 'check-centralizer'),
         'exact manifest and four explicit route declarations')
    bind_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'bind')
    writes = [ast.unparse(n) for n in ast.walk(bind_node)
              if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store)]
    need(sorted(writes) == ['pair.helper', 'standard.FILES', 'standard.S'],
         'only three explicit original-module I/O attribute transports')
    main_source = defs(facade)['main']
    invoke_source = defs(facade)['invoke']
    need('module.main()' in invoke_source and 'finally:\n        sys.argv=old_argv' in invoke_source,
         'complete unchanged mains and restored explicit argv')
    need("module.__file__=str(path)" in facade
         and "'public_on_standard_body'" in facade and "'public_on_pair_body'" in facade,
         'truthful relocated nonmain module contexts')
    need('/Users/' not in facade and 'subprocess' not in facade
         and 'importlib' not in facade and 'pair.helper=public_helper' in facade,
         'public facade has no private resolver or process fallback')
    need("'ordinary isolated -E -B Python'" in main_source
         and 'peak>=128*2**20' in facade and '>=30' in facade
         and 'len(encoded)<=65536' in main_source,
         'unchanged combined self limits and bounded public receipt')
    need(manifest['schema'] == 'ONAN_CENTRALIZER_PORTABLE_INPUT_MANIFEST_V1'
         and manifest['degree'] == 245520 and manifest['goal'] == 161280
         and manifest['seed'] == [0, 1]
         and manifest['archival_labels_are_runtime_dependencies'] is False,
         'fixed manifest and purely documentary archival labels')
    need(manifest['mathematical_scope']['census_credit'] == 0
         and manifest['mathematical_scope']['L026_complete'] is False
         and manifest['mathematical_scope']['matrix45D_homomorphism_proved'] is False
         and manifest['mathematical_scope']['centralizer_upper_bound_is_borrowed'] is True
         and manifest['mathematical_scope']['named_model_is_borrowed'] is True,
         'conditional model/classification premises and zero original/census credit')
    destinations = recipe['source_exports'] + recipe['payloads_declared_not_read_hashed_or_copied']
    need(len(destinations) == 8 and recipe['declared_new_file_count'] == 8
         and recipe['declared_new_bytes'] == 4561806
         and recipe['declared_payload_bytes'] == 4527065,
         'exact finite eight-file proposal totals from declared pins only')
    need(sum(x['destination']['bytes'] for x in destinations) == recipe['declared_new_bytes'],
         'complete package declared-byte composition')
    need(sorted((x['destination'] for x in destinations), key=lambda x:x['path'])
         == sorted(plan['proposed_additions'], key=lambda x:x['path']),
         'exact copy recipe and registration-plan destination roster')
    for x in destinations:
        d, q = x['destination'], x['source']
        need(not Path(d['path']).is_absolute() and '..' not in Path(d['path']).parts
             and d['bytes'] == q['bytes'] and d['sha256'] == q['sha256'],
             'semantic public-relative destination preserves exact bytes')
    for x in recipe['source_exports']:
        read(x['source']['path'], x['source'])
    payloads = [manifest['models']['c'], manifest['models']['d'], manifest['tree']]
    need(sorted(payloads, key=lambda q:q['path'])
         == sorted([x['destination'] for x in recipe['payloads_declared_not_read_hashed_or_copied']],
                   key=lambda q:q['path']), 'three exact declared payload identities, never opened')
    need(all(q['path'] not in OPENED for q in
             [x['source'] for x in recipe['payloads_declared_not_read_hashed_or_copied']]),
         'no model or tree payload touched')
    need(plan['baseline'] == '4512492579d2809c32cadeda9250ae26ce661616'
         and plan['predecessor_CLI_passed_enlarged_tree'] is False
         and plan['registration_source_authored'] is False,
         'honest frozen publication plan, not current registration execution')
    tool = late['actual_tool']
    need(tool == dict(handle=None, initial_chunk='22d3eb', terminal_chunk='22d3eb',
                      exit_code=0, synchronous=True), 'genuine captured author Source tool')
    need(late['scientific_calls'] == 0 if 'scientific_calls' in late else
         late.get('target_function_calls') == 0, 'author Source-only receipt')
    # Reauthenticate the finite readset, without following nested provenance pins.
    before = list(OPENED.values())
    for q in before:
        read(q['path'], q)
    own = pin(Path(__file__).read_bytes(), Path(__file__).resolve())
    roster = sorted([*OPENED.values(), own], key=lambda q:q['path'])
    need(len({q['path'] for q in roster}) == len(roster), 'unique literal reviewer roster')
    qualifications = [
        'Source/AST/ordinary-metadata review only; no executable target compilation, import, function, fixture, checker, permutation, tree, Git, public-write or process call.',
        'The complete original scientific bodies are unchanged. Only the explicitly named I/O/module-context/argv bindings are transported; original private CLIs are not claimed to pass publicly.',
        'The standard core retains dormant historical private S/FILES literals. The authenticated facade overwrites them before every original main call and replaces the pair helper with the same authenticated public module.',
        'The named ATLAS model, inner-kernel/classification facts and centralizer upper bound 161280 are borrowed premises; no 45D identification, complete L026, census or original credit follows.',
        'Actual materialization, all four public replays, absence of private access, guarded fit, exact export hashes and additive registration remain Root duties. This Source proposal records historical preparation-time absence of those later acquisitions.',
        'The facade conservatively compares whole stat results for returned reports; an ordinary atime change may cause refusal, never false mathematical credit.',
        'Reviewer Cleanup authored the related private publication registration layer and earlier actual-metadata audits of these Root-authored cores. Unit authored this independent facade and Source proposal; Cleanup did not author its code.'
    ]
    checks = dict(schema='INDEPENDENT_ONAN_PORTABLE_SOURCE_CHECKS_V1',
                  status='PASSED_SOURCE_ONLY', reviewer=ACTOR, source_author=AUTHOR,
                  complete_original_definition_counts=body_counts,
                  entire_source_inverse_verified=True, explicit_io_attributes=writes,
                  declared_package_files=8, declared_payload_files=3,
                  declared_package_bytes=4561806, declared_payload_bytes=4527065,
                  input_count=len(roster), input_bytes=sum(q['bytes'] for q in roster),
                  required_root_admission_inputs=roster,
                  payloads_opened_or_hashed=0, target_imports=0,
                  target_executable_compiles=0, target_function_calls=0,
                  fixture_calls=0, git_calls=0, public_writes=0,
                  blockers=[], qualifications=qualifications)
    check_ref = put(R/'independent_source_checks.json', checks)
    peer = dict(status=STATUS, source_author=AUTHOR, reviewer=ACTOR,
                program=packet['program'], programs=packet['programs'],
                manifest=packet['manifest'], source_packet=packet_ref,
                inverse=packet['inverse'], argument=packet['argument'],
                checks=check_ref, method=own, source_preparation_execution=late_ref,
                required_root_admission_inputs=sorted([*roster, check_ref],key=lambda q:q['path']),
                blockers=[], qualifications=qualifications,
                whole_original_credit=0, scientific_credit=0, census_credit=0)
    peer_ref = put(R/'distinct_source_review.json', peer)
    print(json.dumps(dict(status=STATUS, review=peer_ref, checks=check_ref,
                          method=own, input_count=len(roster),
                          input_bytes=sum(q['bytes'] for q in roster),
                          unchanged_definition_counts=body_counts)))


if __name__ == '__main__':
    main()
