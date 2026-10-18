"""Small adversarial transport fixtures; no project mathematics or native calls."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(output):
    source = Path(__file__).with_name('runtime.py')
    spec = importlib.util.spec_from_file_location('f012_transport_runtime', source)
    runtime = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runtime)
    checks = []
    with tempfile.TemporaryDirectory(prefix='f012-transport-controls-', dir='/private/tmp') as temp:
        base = Path(temp)
        package = base / 'package'
        package.mkdir()
        secret = base / 'legacy.txt'
        secret.write_bytes(b'old private bytes must never be read\n')
        raw = b'exact packaged bytes\n'
        header = b'// fixture source header\n'
        config = json.dumps({'payload': str(secret)}).encode()
        files = {}
        objects = {}
        for key, data, alias, target, role in [
            ('fixture/data.txt', raw, str(secret), 'study/data.txt', 'runtime'),
            ('fixture/header.hpp', header, str(base/'old.hpp'), 'study/header.hpp', 'source'),
            ('fixture/config.json', config, str(base/'old.json'), 'study/config.json', 'runtime'),
        ]:
            h = sha(data)
            part = 'data/edge_girth_regular_graphs/objects/' + h + '/0.bin'
            path = package / part
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            objects[h] = {'bytes': len(data), 'parts': [{'relative_path': part, 'bytes': len(data), 'sha256': h}]}
            files[key] = {'role': role, 'bytes': len(data), 'sha256': h, 'object': h,
                          'aliases': [alias], 'materialized_path': target}
        files['old/executable'] = {'role': 'provenance_only', 'bytes': 4, 'sha256': sha(b'old!'),
            'object': None, 'aliases': [str(base/'old-binary')], 'materialized_path': 'study/old-binary',
            'reason': 'Historical identity; this control never executes it.'}
        document = {'schema': runtime.SCHEMA, 'files': files, 'objects': objects, 'modes': {},
            'json_relocations': {'fixture': {'file': 'fixture/config.json',
                'fields': [{'pointer': ['payload'], 'original_alias': str(secret)}]}},
            'build_recipes': {'fixture': {'inputs': ['fixture/header.hpp'],
                'arguments': ['-std=c++17', {'input': 'fixture/header.hpp'}, '-o', {'output': True}],
                'toolchain_dependencies': ['configured_cxx', 'matching_C++17_standard_library'],
                'limits': {'execution': 'not executed'}, 'qualification': 'Fixture only'}}}
        count = 0

        def instance(doc=None, root=None):
            nonlocal count
            count += 1
            data = json.dumps(document if doc is None else doc, sort_keys=True).encode()
            name = 'manifest-' + str(count) + '.json'
            (package/name).write_bytes(data)
            return runtime.Runtime(package if root is None else root, name, sha(data))

        def rejected(name, action):
            try:
                action()
            except (ValueError, KeyError, IndexError, FileNotFoundError, NotADirectoryError):
                checks.append({'name': name, 'outcome': 'REJECTED'})
            else:
                raise AssertionError('Unexpected acceptance: ' + name)

        r = instance()
        assert r.read(str(secret)) == raw and secret.read_bytes() != raw
        assert r.historical_identity('old/executable')['status'] == 'PROVENANCE_IDENTITY_ONLY_NOT_EXECUTED'
        checks.append({'name': 'exact alias uses authenticated object, not existing private file', 'outcome': 'PASS'})
        for value in ('', '.', '..', './a', 'a/../b', '/a', 'a//b', 'a\\b'):
            rejected('noncanonical path ' + repr(value), lambda value=value: runtime.relative(value))
        rejected('unknown existing private path', lambda: r.read(str(secret.parent/'package'/ 'manifest-1.json')))
        rejected('historical executable as runtime', lambda: r.read('old/executable'))
        rejected('alias and logical selection duplicate',
                 lambda: r.materialize(['fixture/data.txt', str(secret)], base/'duplicate'))
        assert not (base/'duplicate').exists()
        for a, b in [('a', 'a/b'), ('a/b', 'a')]:
            d = copy.deepcopy(document)
            d['files']['fixture/data.txt']['materialized_path'] = a
            d['files']['fixture/header.hpp']['materialized_path'] = b
            rejected('prefix collision ' + a + ' / ' + b, lambda d=d: instance(d))
        for target in ('materialization.json', 'materialization.json/payload'):
            d = copy.deepcopy(document)
            d['files']['fixture/data.txt']['materialized_path'] = target
            rejected('reserved report ' + target, lambda d=d: instance(d))
        rejected('wrong external manifest digest', lambda: runtime.Runtime(package, 'manifest-1.json', '0'*64))
        part = package / objects[sha(raw)]['parts'][0]['relative_path']
        part.write_bytes(raw[:-1] + b'!')
        rejected('tampered object', lambda: r.materialize(['fixture/data.txt'], base/'tampered'))
        assert not (base/'tampered').exists()
        part.unlink()
        part.symlink_to(secret)
        rejected('payload symlink', lambda: r.read('fixture/data.txt'))
        part.unlink()
        part.write_bytes(raw)
        linked_root = base/'linked-package'
        linked_root.symlink_to(package, target_is_directory=True)
        rejected('package root symlink', lambda: instance(root=linked_root))
        output_parent = base/'linked-parent'
        output_parent.symlink_to(base, target_is_directory=True)
        rejected('output parent symlink', lambda: r.materialize(['fixture/data.txt'], output_parent/'bad'))
        work = base/'work'
        materialized = r.materialize(['fixture/data.txt', 'fixture/header.hpp', 'fixture/config.json'], work)
        assert materialized['whole_source_credit'] == 0 and r.resolve(str(secret), work).read_bytes() == raw
        relocated = r.relocated_json('fixture/config.json', 'fixture', work)
        assert relocated['payload'] == str(work/'study/data.txt')
        assert json.loads(r.read('fixture/config.json'))['payload'] == str(secret)
        checks.append({'name': 'exact materialization and one-field JSON relocation preserve original', 'outcome': 'PASS'})
        d = copy.deepcopy(document)
        d['json_relocations']['fixture']['fields'][0]['pointer'] = ['unknown']
        rejected('unknown JSON pointer', lambda: instance(d).relocated_json('fixture/config.json', 'fixture', work))
        d = copy.deepcopy(document)
        d['json_relocations']['fixture']['fields'][0]['original_alias'] = str(base/'wrong')
        rejected('wrong original JSON alias', lambda: instance(d).relocated_json('fixture/config.json', 'fixture', work))
        build = r.build_plan('fixture', work, '/explicit/compiler', base/'future-native')
        assert build['status'] == 'SOURCE_BUILD_PLAN_NOT_EXECUTED' and not (base/'future-native').exists()
        checks.append({'name': 'source/header build plan without execution', 'outcome': 'PASS'})
        for arg in ('/private/unlisted.cpp', '-fplugin=unlisted.so', '-Iprivate', {'input': 'unknown.cpp'}):
            d = copy.deepcopy(document)
            d['build_recipes']['fixture']['arguments'].insert(0, arg)
            rejected('hidden/unlisted build input ' + repr(arg),
                     lambda d=d: instance(d).build_plan('fixture', work, '/explicit/compiler', base/'future-native'))
        d = copy.deepcopy(document)
        d['build_recipes']['fixture']['toolchain_dependencies'] = []
        rejected('undeclared standard-library boundary',
                 lambda: instance(d).build_plan('fixture', work, '/explicit/compiler', base/'future-native'))
        d = copy.deepcopy(document)
        d['files']['fixture/data.txt']['role'] = 'unresolved_preserved'
        unresolved = instance(d)
        rejected('unresolved payload used as runtime', lambda: unresolved.read('fixture/data.txt'))
        assert unresolved.verify(['fixture/data.txt'])['status'] == 'VERIFIED_CONTENT_ONLY'
        checks.append({'name': 'unresolved object may be authenticated without runtime promotion', 'outcome': 'PASS'})
    report = {'status': 'PASS_TRANSPORT_ADVERSARIAL_FIXTURES_ONLY',
              'runtime': {'bytes': source.stat().st_size, 'sha256': sha(source.read_bytes())},
              'checks': checks, 'scientific_calls': 0, 'native_processes': 0,
              'private_legacy_fallback': False, 'whole_source_credit': 0}
    with Path(output).open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.out), indent=2))
