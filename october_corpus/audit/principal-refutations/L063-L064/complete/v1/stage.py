"""Exact portable L063_L064 completion; reuse accepted codec and public principal data."""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import pack_codec as codec

P = Path(__file__).resolve().parent
F = P.parent
S = F.parents[1]
R = Path('/Users/sasha/medusa/math_compression')
A = F / 'source_synthesis'
PREFIX = 'audit/principal-refutations/L063-L064/complete/v1'
PAPER = 'papers/corrections/psl2_rank_two/v1'
AUTHOR_SHA = '2945e2fb811e92bc783b67f5edda97b638802f341652e7efba39ecd0acd8535e'
RESERVE = 4 * 2**30
need = codec.need


def load(path):
    return json.loads(path.read_text())


def pin(path):
    size, digest = codec.digest_file(path)
    return dict(path=str(path), bytes=size, sha256=digest)


def exact(path, row):
    need(codec.digest_file(path) == (row['bytes'], row['sha256']), 'changed bound input: ' + str(path))


def write(path, obj):
    need(not path.exists(), 'fresh metadata')
    path.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--acceptance', type=Path, required=True)
    parser.add_argument('--expected-acceptance', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root_path = args.acceptance.resolve()
    root = pin(root_path)
    need(root['sha256'] == args.expected_acceptance, 'externally fixed root acceptance')
    root_manifest = load(root_path)
    need(root_manifest['status'] == 'ACCEPTED_L063_L064_COMPLETE_FIXED_SOURCE_TREATMENT', 'exact source-completion acceptance')
    author = pin(A / 'manifest.json')
    need(author['sha256'] == AUTHOR_SHA, 'accepted exact synthesis')
    rows = load(root_path.parent / 'dependencies.json')
    rows += [dict(r, path=str(root_path.parent / r['path'])) for r in root_manifest['exports']]
    rows.append(root)
    logical = {r['path']: r for r in rows}
    need(len(rows) == len(logical), 'unique root closure')
    for row in rows:
        exact(Path(row['path']), row)
    required = load(A / 'dependencies.json')
    required += [dict(r, path=str(A / r['path'])) for r in load(A / 'manifest.json')['exports']]
    required.append(author)
    for row in required:
        need(logical.get(row['path']) == row, 'root closure includes all accepted scientific inputs')
    need(args.out.is_absolute() and not args.out.exists(), 'fresh absolute private stage')
    unique = {}
    for row in rows:
        if row['sha256'] in unique:
            need(unique[row['sha256']]['bytes'] == row['bytes'], 'one length per content hash')
        unique.setdefault(row['sha256'], row)
    bound = sum(r['bytes'] for r in unique.values()) + 40 * 2**20
    need(shutil.disk_usage(args.out.parent).free >= RESERVE + bound, 'stage fits unchanged 4GiB reserve')
    tracked = set(subprocess.run(['git', '-C', str(R), 'ls-files', '-z'],
                                check=True, capture_output=True).stdout.decode().split('\0'))
    public = {}
    reuse = {}
    for row in rows:
        path = Path(row['path'])
        if path.is_relative_to(R):
            name = str(path.relative_to(R))
            if name not in tracked:
                continue  # Retained local copy is packed, never claimed as public reuse.
            public[name] = dict(row, path=name)
            reuse.setdefault(row['sha256'], name)
    # Only the exact reviewed documentary/environment boundary is premise-only.
    candidate = load(P / 'premise_candidates.json')
    need(candidate['author_sha256'] == AUTHOR_SHA, 'exact premise inventory edition')
    premises = []
    for row in candidate['premises']:
        bound_row = {k: row[k] for k in ['path', 'bytes', 'sha256']}
        need(logical.get(row['path']) == bound_row, 'premise in accepted root closure')
        premises.append(dict(kind=row['kind'], bytes=row['bytes'], sha256=row['sha256'],
                             exact_locator=row['path'], reason=row['reason']))
    distinct_premises = {}
    for row in premises:
        previous = distinct_premises.setdefault(row['sha256'], row)
        need((previous['kind'], previous['bytes']) == (row['kind'], row['bytes']),
             'compatible exact premise aliases')
    premises = list(distinct_premises.values())
    premise_by_hash = {r['sha256']: r for r in premises}
    args.out.mkdir()
    d = args.out / PREFIX
    d.mkdir(parents=True)
    writer = codec.Writer(args.out, PREFIX + '/packs', reserve=RESERVE)
    objects = {}
    used_public = {}
    for digest, row in unique.items():
        if digest in premise_by_hash:
            objects[digest] = premise_by_hash[digest]
        elif digest in reuse:
            name = reuse[digest]
            old = public[name]
            used_public[name] = old
            objects[digest] = dict(kind='EXISTING_PUBLIC', public_path=name, bytes=row['bytes'], sha256=digest,
                                   encoding='identity', stored_bytes=row['bytes'], stored_sha256=digest,
                                   segments=[dict(path=name, offset=0, bytes=row['bytes'])] if row['bytes'] else [])
        else:
            objects[digest] = dict(writer.add(row['path'], row, 'gzip'), kind='NEW_PACKED_EXACT_CONTENT')
    packs = writer.finish()
    routes = []
    for row in rows:
        path = Path(row['path'])
        origin, name = ('study', str(path.relative_to(S))) if path.is_relative_to(S) else (
            ('public', str(path.relative_to(R))) if path.is_relative_to(R) else ('external', str(path)))
        routes.append(dict(origin=origin, path=name, original_path=row['path'],
                           bytes=row['bytes'], sha256=row['sha256']))
    transport = dict(format='L063_L064_COMPLETION_EXACT_CONTENT_V1', root_acceptance=root, author_manifest=author,
                     logical_files=routes, objects=objects, packs=packs, existing_public_files=list(used_public.values()),
                     premises=premises, new_scientific_targets=0, mathematical_compression_measurement=None)
    write(d / 'transport.json', transport)
    write(d / 'premises.json', dict(root=root, premises=premises))
    for name in ['pack_codec.py', 'prior_transport_reader.py', 'codec_controls.py', 'portable_check.py',
                 'reused_tools.json', 'premise_candidates.json', 'PUBLICATION.rst', 'stage.py']:
        shutil.copyfile(P / name, d / name)
    paper = args.out / PAPER
    paper.mkdir(parents=True)
    names = ['completion.tex', 'completion.pdf',
             'complete.tex', 'complete.pdf', 'L063_claims.json', 'L064_claims.json', 'edition_deltas.json', 'imports.json', 'parts.json', 'proof_routes.json', 'source_arc_rows.json']
    names += [row['destination']['path'] for row in load(A / 'imports.json')]
    for name in names:
        dest = paper / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(A / name, dest)
    write(d / 'roles.json', dict(author='/root/j3_recovery', mathematical_acceptance=root,
          portable_review='pending', ordinary_recovery_delta=0, principal_refutation_delta=0,
          source_ids=['L063', 'L064'], proposed_surviving_claim_obligations_delta=-2, new_Lean=0, new_measurement=None,
          reused_codec='Unchanged from accepted L091/L070 publication.', reserve_bytes=RESERVE,
          legacy_codec_text='The unchanged codec error mentions 8GiB; the explicit numeric reserve is 4GiB.'))
    exports = [dict(pin(path), path=str(path.relative_to(args.out)))
               for path in sorted(args.out.rglob('*')) if path.is_file()]
    write(d / 'manifest.json', dict(status='PRIVATE_L063_L064_COMPLETION_STAGE_PENDING_OPERATIONAL_REVIEW',
                                   root_acceptance=root, exports=exports))
    result = dict(manifest=pin(d / 'manifest.json'), transport=pin(d / 'transport.json'),
                  logical_files=len(rows), content_objects=len(objects), new_pack_bytes=sum(r['bytes'] for r in packs),
                  reused_public_files=len(used_public), premise_objects=len(premises), documentary_premises=candidate['documentary_count'], environment_premises=candidate['environment_count'],
                  public_mutations=0)
    write(P / (args.out.name + '_receipt.json'), result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
