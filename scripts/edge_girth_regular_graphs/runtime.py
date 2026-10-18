"""Authenticate and materialize the declared F012 package; never read the old study.

This module does not infer theorem truth from transport hashes. Native builds and
scientific checks are separate, explicitly listed commands and are never started
by inspect, verify, materialize, resolve or plan-build.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

SCHEMA = 'F012_PORTABLE_RUNTIME_MANIFEST_V1'
HASH = re.compile(r'[0-9a-f]{64}\Z')
ROLES = frozenset({'runtime', 'source', 'certificate', 'written_premise',
                   'documentary', 'unresolved_preserved', 'provenance_only'})
READABLE = ROLES - {'provenance_only', 'unresolved_preserved'}
CHUNK = 1024 * 1024


def need(value, message):
    if not value:
        raise ValueError(message)


def relative(value):
    need(type(value) is str and value and '\\' not in value, 'Relative POSIX path')
    q = PurePosixPath(value)
    need(bool(q.parts) and not q.is_absolute() and str(q) == value and
         all(x not in ('', '.', '..') for x in q.parts), 'Canonical relative path')
    return q.parts


def regular(root, name):
    """Reject every symlink component, including root, without using resolve()."""
    root = Path(root).absolute()
    at = Path(root.anchor)
    for part in root.parts[1:]:
        at /= part
        info = at.lstat()
        need(not stat.S_ISLNK(info.st_mode) and stat.S_ISDIR(info.st_mode),
             'Non-symlink directory chain')
    at = root
    parts = relative(name)
    for i, part in enumerate(parts):
        at /= part
        info = at.lstat()
        need(not stat.S_ISLNK(info.st_mode), 'No symlink payload')
        need(stat.S_ISREG(info.st_mode) if i == len(parts)-1 else stat.S_ISDIR(info.st_mode),
             'Regular payload / directory chain')
    return at


def digest(path):
    count = 0
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(CHUNK), b''):
            h.update(block)
            count += len(block)
    return count, h.hexdigest()


class Runtime:
    def __init__(self, root, manifest, manifest_sha256):
        need(not sys.flags.optimize, 'Ordinary Python required')
        need(HASH.fullmatch(manifest_sha256) is not None, 'External manifest digest')
        self.root = Path(root).absolute()
        raw = regular(self.root, manifest).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == manifest_sha256, 'Manifest identity')
        self.manifest_sha256 = manifest_sha256
        self.document = json.loads(raw)
        need(self.document.get('schema') == SCHEMA, 'Manifest schema')
        self.files = self.document['files']
        self.objects = self.document['objects']
        need(type(self.files) is dict and type(self.objects) is dict, 'Explicit maps')
        self.aliases = {}
        destinations = set()
        for key, item in self.files.items():
            relative(key)
            need(item['role'] in ROLES, 'Declared file role')
            need(type(item['bytes']) is int and item['bytes'] >= 0 and
                 HASH.fullmatch(item['sha256']) is not None, 'Content identity')
            relative(item['materialized_path'])
            target = item['materialized_path']
            need(relative(target)[0] != 'materialization.json', 'Reserved output report path')
            need(target not in destinations and not any(target.startswith(old + '/') or old.startswith(target + '/') for old in destinations),
                 'Unique, non-prefix-colliding materialized paths')
            destinations.add(item['materialized_path'])
            need(type(item['aliases']) is list and item['aliases'], 'Exact legacy aliases')
            for alias in item['aliases']:
                need(type(alias) is str and alias.startswith('/') and
                     alias not in self.aliases, 'Unique absolute provenance alias')
                self.aliases[alias] = key
            if item['role'] == 'provenance_only':
                need(item.get('object') is None and bool(item.get('reason')),
                     'Provenance identity cannot be opened as a runtime object')
            else:
                need(item['object'] == item['sha256'] and item['object'] in self.objects,
                     'Declared content object')
                obj = self.objects[item['object']]
                need(obj['bytes'] == item['bytes'] and type(obj['parts']) is list and obj['parts'],
                     'Same exact content object')
                need(sum(part['bytes'] for part in obj['parts']) == item['bytes'], 'Whole object size')
                for index, part in enumerate(obj['parts']):
                    need(part['relative_path'] == 'data/edge_girth_regular_graphs/objects/' + item['sha256'] + '/' + str(index) + '.bin'
                         and type(part['bytes']) is int and 0 <= part['bytes'] <= 32 * 2**20
                         and HASH.fullmatch(part['sha256']) is not None, 'Exact bounded chunk')
        used = {r['object'] for r in self.files.values() if r.get('object')}
        need(used == set(self.objects), 'No undeclared or unused content objects')

    def entry(self, logical_or_alias, allow_unresolved=False):
        key = self.aliases.get(logical_or_alias, logical_or_alias)
        need(key in self.files, 'No unlisted/private fallback: ' + str(logical_or_alias))
        item = self.files[key]
        need(item['role'] != 'provenance_only', 'Historical identity is not runtime data')
        need(allow_unresolved or item['role'] in READABLE,
             'Unresolved classification cannot silently become a runtime input')
        return key, item

    def object_blocks(self, logical_or_alias, allow_unresolved=False):
        key, item = self.entry(logical_or_alias, allow_unresolved)
        whole = hashlib.sha256()
        total = 0
        for part in self.objects[item['object']]['parts']:
            path = regular(self.root, part['relative_path'])
            h = hashlib.sha256()
            count = 0
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(CHUNK), b''):
                    h.update(block)
                    whole.update(block)
                    count += len(block)
                    total += len(block)
                    need(count <= part['bytes'] and total <= item['bytes'], 'Bounded actual payload')
                    yield block
            need((count, h.hexdigest()) == (part['bytes'], part['sha256']), 'Exact part bytes: ' + key)
        need((total, whole.hexdigest()) == (item['bytes'], item['sha256']), 'Exact whole object: ' + key)

    def read(self, logical_or_alias):
        _, item = self.entry(logical_or_alias)
        need(item['bytes'] <= 32 * 2**20, 'Large objects must be streamed or materialized')
        return b''.join(self.object_blocks(logical_or_alias))

    def historical_identity(self, logical_or_alias):
        key = self.aliases.get(logical_or_alias, logical_or_alias)
        need(key in self.files and self.files[key]['role'] == 'provenance_only',
             'Explicit historical identity boundary')
        item = self.files[key]
        return {'status': 'PROVENANCE_IDENTITY_ONLY_NOT_EXECUTED', 'bytes': item['bytes'],
                'sha256': item['sha256'], 'reason': item['reason']}

    def verify(self, keys):
        checked = set()
        for key in keys:
            _, item = self.entry(key, allow_unresolved=True)
            if item['object'] not in checked:
                for _ in self.object_blocks(key, allow_unresolved=True):
                    pass
                checked.add(item['object'])
        return {'status': 'VERIFIED_CONTENT_ONLY', 'objects': len(checked),
                'bytes': sum(self.objects[k]['bytes'] for k in checked), 'whole_source_credit': 0}

    def materialize(self, keys, output, allow_unresolved=False):
        output = Path(output).absolute()
        need(not output.exists() and not output.is_symlink(), 'Fresh output root')
        selected = [self.entry(key, allow_unresolved) for key in keys]
        need(len({key for key, _ in selected}) == len(selected), 'No repeated selection')
        logical_bytes = sum(item['bytes'] for _, item in selected)
        # Output is created only after all input objects have been authenticated.
        self.verify([key for key, _ in selected])
        parent = output.parent
        regular_parent = Path(parent.anchor)
        for part in parent.parts[1:]:
            regular_parent /= part
            info = regular_parent.lstat()
            need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
                 'Non-symlink output parent')
        space = os.statvfs(parent)
        need(space.f_bavail * space.f_frsize >= logical_bytes + 4 * 2**30,
             'Four GiB reserve plus complete materialization bytes')
        output.mkdir()
        for key, item in selected:
            target = output.joinpath(*relative(item['materialized_path']))
            target.parent.mkdir(parents=True, exist_ok=True)
            h = hashlib.sha256()
            count = 0
            with target.open('xb') as dst:
                for block in self.object_blocks(key, allow_unresolved):
                    dst.write(block)
                    h.update(block)
                    count += len(block)
            need((count, h.hexdigest()) == (item['bytes'], item['sha256']),
                 'Copied complete verified object: ' + key)
        report = {'status': 'MATERIALIZED_EXACT_FILES_NO_SCIENTIFIC_CHECK',
                  'manifest_sha256': self.manifest_sha256, 'files': [k for k, _ in selected],
                  'logical_bytes': logical_bytes, 'unresolved_preserved_only': allow_unresolved,
                  'private_fallback': False, 'whole_source_credit': 0}
        (output / 'materialization.json').write_text(json.dumps(report, indent=2) + '\n')
        return report

    def resolve(self, alias, work):
        key, item = self.entry(alias)
        path = regular(Path(work), item['materialized_path'])
        need(digest(path) == (item['bytes'], item['sha256']), 'Materialized identity: ' + key)
        return path

    def relocated_json(self, logical, recipe, work):
        """Apply only manifest-listed JSON pointer locations after original authentication."""
        spec = self.document['json_relocations'][recipe]
        need(spec['file'] == logical, 'Exact relocation recipe input')
        value = json.loads(self.read(logical))
        result = copy.deepcopy(value)
        for change in spec['fields']:
            parts = change['pointer']
            need(type(parts) is list and parts and all(type(x) is str and x or type(x) is int and x >= 0 for x in parts),
                 'Literal JSON field path')
            at = result
            for part in parts[:-1]:
                at = at[part]
            need(at[parts[-1]] == change['original_alias'], 'Exact old path field')
            at[parts[-1]] = str(self.resolve(change['original_alias'], work))
        return result

    def build_plan(self, name, work, cxx, output):
        spec = self.document['build_recipes'][name]
        need(set(spec) == {'inputs', 'arguments', 'toolchain_dependencies', 'limits', 'qualification'},
             'Explicit build recipe fields')
        need(spec['toolchain_dependencies'] == ['configured_cxx', 'matching_C++17_standard_library'],
             'Explicit compiler/standard-library environment boundary')
        need(type(spec['inputs']) is list and len(set(spec['inputs'])) == len(spec['inputs']),
             'Unique complete source/header roster')
        need(all(self.entry(key)[1]['role'] == 'source' for key in spec['inputs']),
             'Build inputs are declared source roles')
        sources = {key: str(self.resolve(key, work)) for key in spec['inputs']}
        need(Path(cxx).is_absolute(), 'Explicit compiler path')
        need(Path(output).is_absolute() and not Path(output).exists() and not Path(output).is_symlink(),
             'Fresh absolute native output')
        command = [cxx]
        used = set()
        outputs = 0
        for arg in spec['arguments']:
            if type(arg) is str:
                need(arg in ('-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-o'),
                     'Exact ordinary flags; no file/toolchain/plugin arguments hidden in flags')
                command.append(arg)
            else:
                need(type(arg) is dict and len(arg) == 1, 'Structured file-bearing argument')
                if 'input' in arg:
                    need(arg['input'] in sources, 'Declared verified source argument')
                    command.append(sources[arg['input']])
                    used.add(arg['input'])
                else:
                    need(arg == {'output': True}, 'Only explicit output marker allowed')
                    command.append(str(output))
                    outputs += 1
        need(used and outputs == 1, 'Source input and exactly one output')
        return {'status': 'SOURCE_BUILD_PLAN_NOT_EXECUTED', 'command': command,
                'verified_sources_and_headers': spec['inputs'], 'historical_binary_required': False,
                'toolchain_dependencies': spec['toolchain_dependencies'],
                'limits': spec['limits'], 'qualification': spec['qualification']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--manifest', default='data/edge_girth_regular_graphs/runtime_manifest.json')
    p.add_argument('--manifest-sha256', required=True)
    sub = p.add_subparsers(dest='action', required=True)
    sub.add_parser('inspect')
    verify = sub.add_parser('verify')
    verify.add_argument('--selection', choices=('all-preserved', 'runtime', 'sources', 'certificates'),
                        default='runtime')
    materialize = sub.add_parser('materialize')
    materialize.add_argument('--selection', choices=('all-preserved', 'runtime', 'sources', 'certificates'),
                             default='runtime')
    materialize.add_argument('--out', type=Path, required=True)
    resolve = sub.add_parser('resolve')
    resolve.add_argument('--legacy', required=True)
    resolve.add_argument('--work', type=Path, required=True)
    build = sub.add_parser('plan-build')
    build.add_argument('--recipe', required=True)
    build.add_argument('--work', type=Path, required=True)
    build.add_argument('--cxx', required=True)
    build.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    runtime = Runtime(a.root, a.manifest, a.manifest_sha256)
    if a.action == 'inspect':
        report = {'status': 'VALID_MANIFEST_NO_PAYLOAD_OR_SCIENCE_CHECK',
                  'files': len(runtime.files), 'objects': len(runtime.objects),
                  'unresolved': sum(x['role'] == 'unresolved_preserved' for x in runtime.files.values()),
                  'modes': runtime.document['modes'], 'whole_source_credit': 0}
    elif a.action in ('verify', 'materialize'):
        roles = {'all-preserved': ROLES - {'provenance_only'},
                 'runtime': {'runtime', 'source', 'certificate'},
                 'sources': {'source', 'written_premise'}, 'certificates': {'certificate'}}[a.selection]
        keys = sorted(k for k, item in runtime.files.items() if item['role'] in roles)
        report = (runtime.verify(keys) if a.action == 'verify' else
                  runtime.materialize(keys, a.out, allow_unresolved=a.selection == 'all-preserved'))
    elif a.action == 'resolve':
        report = {'resolved': str(runtime.resolve(a.legacy, a.work))}
    else:
        report = runtime.build_plan(a.recipe, a.work, a.cxx, a.output)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
