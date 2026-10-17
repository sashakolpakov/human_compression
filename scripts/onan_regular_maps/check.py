"""Authenticate the L046 canonical closure and replay its exact synthesis.

Only the public repository and the supplied stage are input roots. Original
absolute paths are names in provenance, never fallback filesystem locations.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

DATA = 'data/onan_regular_maps'
PAPER = 'papers/onan_regular_maps'
CODEC = 'audit/recoveries/L070/v1/pack_codec.py'
OLD = '/Users/sasha/medusa/research/leemans'
O = OLD + '/geometry/onan_regular_maps'
D = O + '/source_synthesis_work'
SYNTHESIS = '27238130dda9fb1d8a0343e1602dc7ecbe7eb1ee6398d42d680e6a410487e8eb'
REVIEW = 'fa03e55dd19c4712062ffe106972d3b9ce094be7227af52614b2770ff154cdf1'
PAYLOAD = {'NEW_PACKED_EXACT_CONTENT', 'CANONICAL_READABLE', 'EXISTING_PUBLIC'}
BOUNDARY = {'BUILD_PROVENANCE', 'DOCUMENTARY_SOURCE_PREMISE',
            'INSTALLED_ENVIRONMENT_PROVENANCE', 'RENDERED_PROOF_PROVENANCE',
            'INHERITED_EXPLICIT_PREMISE'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def read(p):
    return json.loads(Path(p).read_text())


def digest(p):
    h = hashlib.sha256()
    n = 0
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            n += len(b)
            h.update(b)
    return n, h.hexdigest()


def exact(p, r):
    need(digest(p) == (r['bytes'], r['sha256']), 'exact file: ' + str(p))


class Archive:
    def __init__(self, stage, repo, transport, codec):
        self.stage, self.repo, self.t, self.codec = stage, repo, transport, codec
        self.objects = transport['objects']
        self.originals = {}
        self.logical = {}
        for r in transport['logical_files']:
            key = r['origin'], r['path']
            need(key not in self.logical and r['original_path'] not in self.originals,
                 'unique logical and original paths')
            if r['origin'] in {'study', 'public'}:
                codec.relative(r['path'])
            else:
                need(r['origin'] == 'external' and Path(r['path']).is_absolute(),
                     'explicit documentary external locator')
            if r['origin'] == 'study':
                need(r['original_path'] == OLD + '/' + r['path'], 'study locator join')
            obj = self.objects[r['sha256']]
            need((obj['bytes'], obj['sha256']) == (r['bytes'], r['sha256']),
                 'logical content identity')
            self.logical[key] = r
            self.originals[r['original_path']] = r
        need(set(self.objects) == {r['sha256'] for r in self.originals.values()},
             'no missing or unreferenced content object')
        for h, r in self.objects.items():
            need(h == r['sha256'] and r['kind'] in PAYLOAD | BOUNDARY,
                 'exact object key and known kind')

    def record(self, original):
        need(original in self.originals, 'declared logical input: ' + original)
        return self.objects[self.originals[original]['sha256']]

    def bound(self, item, parent=OLD):
        name = item['path']
        name = name if Path(name).is_absolute() else parent + '/' + name
        rec = self.record(name)
        need(rec['sha256'] == item['sha256'] and
             ('bytes' not in item or rec['bytes'] == item['bytes']), 'exact declared pin')
        return name

    def roots(self, r):
        return [self.repo] if r['kind'] == 'EXISTING_PUBLIC' else [self.stage]

    def content(self, original):
        r = self.record(original)
        need(r['kind'] in PAYLOAD, 'mathematical input requires actual bytes: ' + original)
        return b''.join(self.codec.decoded(r, self.roots(r)))

    def load(self, original):
        return json.loads(self.content(original))


def closure(ar, policy):
    t = ar.t
    need(t['format'] == 'L046_SEGMENTED_CANONICAL_CONTENT_V1', 'transport format')
    need(t['synthesis']['sha256'] == SYNTHESIS and
         t['distinct_synthesis']['sha256'] == REVIEW, 'exact acquired synthesis')
    need(t['whole_original_credit'] == 0 and t['historical_science_replayed'] is False,
         'staged scope')
    boundary = {r['sha256']: r for r in policy['objects']}
    need(len(boundary) == len(policy['objects']), 'unique boundary objects')
    actual = {h: r for h, r in ar.objects.items() if r['kind'] in BOUNDARY}
    need(set(boundary) == set(actual), 'all and only explicit boundary objects')
    for h, r in actual.items():
        need({k: boundary[h][k] for k in ('bytes', 'sha256', 'kind', 'reason')} == r,
             'exact boundary disposition')
        need(set(boundary[h]['aliases']) ==
             {n for n, v in ar.originals.items() if v['sha256'] == h}, 'boundary aliases')
    need(policy['scientific_payload_omissions'] == [] and
         policy['no_old_runtime_hash_prerequisite'] is True, 'publication boundary scope')
    declared = {}
    def add(r, parent=OLD):
        name = ar.bound(r, parent)
        q = ar.originals[name]
        old = declared.setdefault(name, (q['bytes'], q['sha256']))
        need(old == (q['bytes'], q['sha256']), 'consistent declared closure')
    source = ar.load(D + '/source_closure.json')
    for r in source['inputs']:
        add(r)
        name = ar.bound(r)
        if Path(name).name == 'dependencies.json':
            deps = ar.load(name)
            parent = OLD
            if isinstance(deps, dict) and isinstance(deps.get('bindings'), list):
                parent = deps.get('root', parent)
                deps = deps['bindings']
            need(isinstance(deps, list), 'declared flat dependency schema')
            for q in deps:
                add(q, parent)
    request = O + '/even_triples_work/inner_eleven_seven_acquisition_request.json'
    add(dict(ar.originals[request], path=request))
    for r in ar.load(request)['inputs']:
        add(r)
    for name in ('synthesis_packet.json', 'synthesis_distinct_review.json',
                 'synthesis_distinct_check.json'):
        add(dict(ar.originals[D + '/' + name], path=D + '/' + name))
    for r in ar.load(D + '/synthesis_packet.json')['exports']:
        add(r, D)
    need(set(declared) == set(ar.originals), 'complete exact declared transitive input roster')
    need(ar.load(D + '/synthesis_distinct_review.json')['status'] ==
         'DISTINCT_ACCEPTED_L046_CORRECTED_SOURCE_SYNTHESIS_V1', 'distinct synthesis status')
    return source


def verify_content(ar, exports):
    codec, t = ar.codec, ar.t
    packs = {r['path']: r for r in t['packs']}
    need(len(packs) == len(t['packs']), 'unique pack paths')
    for name, r in packs.items():
        need(exports.get(name) == r and 0 < r['bytes'] <= 48*2**20,
             'complete bounded pack exported')
    physical = {str(p.relative_to(ar.stage)) for p in (ar.stage/DATA/'packs').rglob('*') if p.is_file()}
    need(physical == set(packs), 'exact physical pack inventory')
    tracked = set(subprocess.run(['git', '-C', str(ar.repo), 'ls-files', '-z'],
                               check=True, capture_output=True).stdout.decode().split('\0'))
    intervals = {name: [] for name in packs}
    totals = dict(objects=0, decoded_bytes=0, stored_bytes=0, reused_files=set())
    for r in ar.objects.values():
        if r['kind'] not in PAYLOAD:
            continue
        for s in r['segments']:
            if r['kind'] == 'NEW_PACKED_EXACT_CONTENT':
                need(s['path'] in packs, 'new stream uses declared pack')
                intervals[s['path']].append((s['offset'], s['offset'] + s['bytes']))
            elif r['kind'] == 'EXISTING_PUBLIC':
                need(s['path'] in tracked, 'reused stream is tracked public content')
                totals['reused_files'].add(s['path'])
            else:
                need(s['path'] in exports and s['offset'] == 0 and
                     s['bytes'] == r['bytes'], 'readable canonical export')
        codec.verify(r, ar.roots(r))
        totals['objects'] += 1
        totals['decoded_bytes'] += r['bytes']
        totals['stored_bytes'] += r['stored_bytes']
    for name, rows in intervals.items():
        end = 0
        for lo, hi in sorted(rows):
            need(lo == end and hi > lo, 'exact nonoverlapping pack coverage')
            end = hi
        need(end == packs[name]['bytes'], 'no unindexed pack bytes')
    totals['reused_files'] = sorted(totals['reused_files'])
    return totals


def extract_synthesis(ar, source, selected):
    names = {OLD + '/' + r['path'] for r in source['inputs']}
    names |= {D + '/' + n for n in ('check_synthesis.py', 'claims.json', 'source_closure.json',
                                   'component_proofs.json', 'exact_table.tex', 'source_concordance.tex')}
    # The unchanged synthesis reads these additional canonical joins directly.
    names |= {O + '/projective_six_root_adoption/review.json',
              O + '/even_triples_work/inner_eleven_seven_acceptance.json',
              O + '/operations/complete_reflexible_type_spectra.json'}
    omitted = {}
    for name in sorted(names):
        r = ar.record(name)
        need(name.startswith(OLD + '/'), 'selected study-local input')
        rel = name[len(OLD)+1:]
        if r['kind'] in BOUNDARY:
            omitted[rel] = dict(path=rel, bytes=r['bytes'], sha256=r['sha256'], kind=r['kind'])
            continue
    # Only the actual program needs a filesystem location. The unchanged
    # JSON reader below consumes authenticated canonical streams directly,
    # avoiding redundant decoded copies of large flat input inventories.
    name = D+'/check_synthesis.py'
    r = ar.record(name)
    ar.codec.materialize(r, ar.roots(r), selected/name[len(OLD)+1:])
    return omitted, 1


def replay_synthesis(ar, source, selected):
    omitted, count = extract_synthesis(ar, source, selected)
    code = selected/'geometry/onan_regular_maps/source_synthesis_work/check_synthesis.py'
    spec = importlib.util.spec_from_file_location('l046_original_synthesis', code)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    admitted = set()
    payload_pins = set()
    def local_path(path):
        name = str(path)
        if name == OLD or name.startswith(OLD+'/'):
            path = selected/name[len(OLD)+1:]
        path = Path(path).resolve()
        need(path.is_relative_to(selected), 'no private input fallback: '+str(path))
        return path
    def portable_pin(path):
        path = local_path(path)
        rel = str(path.relative_to(selected))
        if rel in omitted:
            r = omitted[rel]
            need(r['kind'] != 'INSTALLED_ENVIRONMENT_PROVENANCE',
                 'runtime cannot replace mathematical input')
            admitted.add(rel)
            return {k: r[k] for k in ('path', 'bytes', 'sha256')}
        original = OLD+'/'+rel
        r = ar.record(original)
        need(r['kind'] in PAYLOAD, 'undeclared documentary admission')
        payload_pins.add(rel)
        return dict(path=rel, bytes=r['bytes'], sha256=r['sha256'])
    def portable_read(path):
        path = local_path(path)
        return ar.load(OLD+'/'+str(path.relative_to(selected)))
    module.pin = portable_pin
    module.read = portable_read
    # This changes file-identity admission and JSON storage access only. All mathematical
    # predicates, source dispositions and complete output comparisons are the
    # unchanged acquired functions. Premise bytes cannot be read or executed.
    report, table, concordance = module.derive()
    need(json.loads(json.dumps(report)) == source, 'entire synthesis output')
    need(table.encode() == ar.content(D+'/exact_table.tex'), 'entire exact table output')
    need(concordance.encode() == ar.content(D+'/source_concordance.tex'),
         'entire source concordance output')
    need(admitted == set(omitted), 'all selected boundary admissions accounted for')
    return dict(selected_files=count, documentary_or_build_bindings=sorted(admitted),
                authenticated_payload_bindings=len(payload_pins),
                input_bindings=len(source['inputs']), clauses=len(report['clauses']),
                numerical_cells=report['numerical_cells'], table_sum=report['table_sum'],
                positive_rotation_types=report['positive_rotation_types'],
                positive_chiral_types=report['positive_chiral_types'],
                exact_inner_type_count=report['exact_inner_type_count'],
                exact_outer_type_count=report['exact_outer_type_count'])


def replay_character_arithmetic(ar, selected):
    """Two original pure-arithmetic programs; no path transformation."""
    modules = {}
    for label, original in [('bounds', OLD+'/corpus106_L046_maximal_bounds_v1/bounds.py'),
                            ('prime', O+'/large_prime_columns_work/evaluate.py')]:
        dest = selected/original[len(OLD)+1:]
        ar.codec.materialize(ar.record(original), ar.roots(ar.record(original)), dest)
        spec = importlib.util.spec_from_file_location('l046_'+label, dest)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[label] = module
    b = modules['bounds']
    tables, maxima = b.read_vectors(ar.content(OLD+'/corpus106_L046_maximal_bounds_v1/maximal_vectors.g.stdout').decode())
    bounds = b.derive(tables, maxima)
    need(bounds == ar.load(OLD+'/corpus106_L046_maximal_bounds_v1/bounds.json'),
         'whole fresh 136-row character bound calculation')
    primes = modules['prime'].derive(tables, maxima)
    need(json.loads(json.dumps(primes)) == ar.load(O+'/large_prime_columns_distinct_review/replay01/counts.json'),
         'whole fresh prime-column subtraction')
    exact_cells = {(r['p'], r['q']): r['lower'] for r in bounds['rows'] if r['lower']==r['upper']}
    for r in primes['distinct_cells']:
        key = tuple(r['source_type'])
        need(key not in exact_cells or exact_cells[key] == r['orbits'], 'fresh arithmetic overlap')
        exact_cells[key] = r['orbits']
    return dict(character_bound_rows=len(bounds['rows']), prime_column_cells=len(primes['distinct_cells']),
                distinct_exact_cells=len(exact_cells), cells=[dict(type=list(k),count=v) for k,v in sorted(exact_cells.items())],
                imported_character_vectors=True, imported_unique_overgroup_theorem=True,
                new_group_calls=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--stage', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--expected-manifest')
    ap.add_argument('--expected-transport')
    ap.add_argument('--admission', type=Path,
                    help='external publication admission, independently bound by registration')
    ap.add_argument('--restore', action='append', default=[],
                    help='exact study-relative canonical input to restore; may be repeated')
    a = ap.parse_args()
    start = time.monotonic()
    repo = a.repo.resolve()
    stage = a.stage.resolve() if a.stage else repo
    if a.admission is not None:
        need(a.expected_manifest is None and a.expected_transport is None, 'one admission interface')
        admission = read(a.admission)
        a.expected_manifest = admission['manifest_sha256']
        a.expected_transport = admission['transport_sha256']
    need(a.expected_manifest and a.expected_transport, 'external exact admission required')
    need(a.out.is_absolute() and not a.out.exists(), 'fresh absolute output directory')
    need(not a.out.is_relative_to(repo) and not a.out.is_relative_to(stage),
         'outputs outside canonical input trees')
    need(shutil.disk_usage(a.out.parent).free >= 4*2**30 + 64*2**20,
         '4 GiB reserve plus 64 MiB small replay allowance')
    mp, tp = stage/DATA/'manifest.json', stage/DATA/'transport.json'
    need(digest(mp)[1] == a.expected_manifest and digest(tp)[1] == a.expected_transport,
         'externally pinned manifest and transport')
    m, t = read(mp), read(tp)
    need(m['status'] == 'PRIVATE_L046_PUBLICATION_STAGE_PENDING_PORTABLE_REVIEW',
         'exact staged review status')
    exports = {r['path']: r for r in m['exports']}
    need(len(exports) == len(m['exports']), 'unique stage exports')
    codecpath = repo/CODEC
    exact(codecpath, t['codec'])
    spec = importlib.util.spec_from_file_location('l046_acquired_codec', codecpath)
    codec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(codec)
    for name, r in exports.items():
        codec.relative(name)
        exact(codec.resolve(name, [stage]), r)
    need(exports.get(DATA+'/transport.json', {}).get('sha256') == a.expected_transport,
         'transport bound by stage')
    own = 'scripts/onan_regular_maps/check.py'
    need(digest(Path(__file__)) == (exports[own]['bytes'], exports[own]['sha256']),
         'executing exact staged checker')
    ar = Archive(stage, repo, t, codec)
    source = closure(ar, read(stage/DATA/'premises.json'))
    payload = verify_content(ar, exports)
    a.out.mkdir()
    # A hard failure on an old study read makes relocation testable even when
    # the original private tree happens to be present on the test machine.
    def no_private_read(event, args):
        if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
            name = os.fsdecode(args[0])
            need(not name.startswith(OLD+'/') or
                 Path(name).is_relative_to(stage) or Path(name).is_relative_to(a.out),
                 'private source access forbidden')
    sys.addaudithook(no_private_read)
    selected = a.out/'selected/study'
    result = replay_synthesis(ar, source, selected)
    result['character_arithmetic'] = replay_character_arithmetic(ar, selected)
    restored = []
    need(len(a.restore) == len(set(a.restore)), 'unique requested restoration paths')
    total = 0
    for name in a.restore:
        codec.relative(name)
        r = ar.record(OLD+'/'+name)
        need(r['kind'] in PAYLOAD, 'only actual canonical bytes can be restored')
        total += r['bytes']
        need(total <= 32*2**20, 'bounded explicit restoration set')
        dest = a.out/'restored'/name
        codec.materialize(r, ar.roots(r), dest)
        restored.append(dict(path=name,bytes=r['bytes'],sha256=r['sha256']))
    result.update(status='PASS_L046_PUBLIC_TRANSPORT_AND_SYNTHESIS',
                  authenticated_payload=payload, logical_files=len(ar.originals),
                  unique_objects=len(ar.objects),
                  manifest_sha256=a.expected_manifest, transport_sha256=a.expected_transport,
                  seconds=time.monotonic()-start, new_censuses=0,
                  historical_science_replayed=False,
                  component_arithmetic_replays=2, restored_inputs=restored,
                  whole_original_registration_credit=0,
                  limitation='Exact composition and two arithmetic replays; other component mathematical and source-reading premises remain explicit.')
    (a.out/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
