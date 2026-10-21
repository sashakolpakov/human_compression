"""Prepare typed F012 environment metadata; no package import or scientific run.

Run with the Python interpreter intended for the reviewed execution. The CLI
reads installed distribution metadata and explicitly selected files. It does
not install, build, import a third-party module, or certify ABI equivalence.
"""
import argparse
import hashlib
import importlib.machinery
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import sys
import sysconfig

sys.dont_write_bytecode = True
MIB = 2**20


def need(value, message):
    if not value:
        raise ValueError(message)


def plain(value):
    path = Path(value)
    need(path.is_absolute() and '..' not in path.parts, 'Absolute ordinary path')
    for ancestor in (path, *path.parents):
        if os.path.lexists(ancestor):
            need(not ancestor.is_symlink(), 'No unrecorded operational alias: ' + str(ancestor))
    return path


def pin(value):
    path = plain(value)
    need(path.is_file(), 'Ordinary declared environment file')
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(MIB), b''):
            size += len(block)
            digest.update(block)
    return dict(path=str(path), bytes=size, sha256=digest.hexdigest())


def relative(base, value):
    rel = PurePosixPath(value)
    need(not rel.is_absolute() and rel.parts and str(rel) == value
         and all(x not in ('', '.', '..') for x in rel.parts), 'Declared relative environment name')
    return plain(base.joinpath(*rel.parts))


def normalize(name):
    return name.lower().replace('-', '_').replace('.', '_')


def distributions(site, requirements):
    found = {}
    for distribution in importlib.metadata.distributions(path=[str(site)]):
        name = normalize(distribution.metadata.get('Name', ''))
        if name not in requirements:
            continue
        need(name not in found, 'Unambiguous installed distribution: ' + name)
        version = distribution.version
        expected = requirements[name]
        need(expected is None or version == expected, 'Preserved package-version premise: ' + name)
        found[name] = distribution
    need(set(found) == set(requirements), 'All declared distribution metadata is installed')
    return found


def distribution_file(distribution, relative_name=None, metadata_name=None, extension_stem=None):
    files = distribution.files
    need(files is not None, 'Distribution has an explicit file inventory')
    choices = []
    for item in files:
        name = str(item)
        if relative_name is not None and name == relative_name:
            choices.append(item)
        if metadata_name is not None and name.endswith('.dist-info/' + metadata_name):
            choices.append(item)
        if extension_stem is not None and any(name == extension_stem + suffix
                for suffix in importlib.machinery.EXTENSION_SUFFIXES):
            choices.append(item)
    need(len(choices) == 1, 'One exact distribution-file role')
    return plain(Path(distribution.locate_file(choices[0])))


def main():
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'Ordinary Python required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--compiler', type=Path, required=True)
    parser.add_argument('--nauty-prefix', type=Path, required=True)
    parser.add_argument('--python-site', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(sys.platform == 'darwin', 'First acquired ownership environment is Darwin only')
    root, site, prefix, output = map(plain, (args.root, args.python_site, args.nauty_prefix, args.out))
    need(site.is_dir() and prefix.is_dir(), 'Existing explicit environment directories')
    need(site in {plain(Path(sysconfig.get_path(key))) for key in ('purelib', 'platlib')},
         'Metadata location belongs to the interpreter used for this generator')
    need(not os.path.lexists(output) and output.parent.is_dir(), 'Fresh environment output')
    need(not output.is_relative_to(root), 'Environment metadata stays outside package')
    plan_path = relative(root, 'data/edge_girth_regular_graphs/execution/binding_plan.json')
    raw = plan_path.read_bytes()
    need(len(raw) <= 4*MIB and hashlib.sha256(raw).hexdigest() == args.plan_sha256, 'Externally bound plan')
    plan = json.loads(raw)
    need(plan['schema'] == 'F012_PACKAGE_EXECUTION_BINDING_PLAN_ROLES_V1', 'Typed environment plan')
    generator = plan['environment_generator']
    need(Path(__file__).resolve() == relative(root, generator['relative_path'])
         and all(pin(Path(__file__).resolve())[k] == generator[k] for k in ('bytes', 'sha256')),
         'Exact installed metadata generator')
    specs = plan['environment_roles']
    requirements = plan['environment_package_versions']
    installed = distributions(site, requirements)
    bindings = {}
    for role, spec in specs.items():
        locator = spec['locator']
        source = locator['source']
        if source == 'compiler':
            path = plain(args.compiler)
        elif source == 'nauty_prefix':
            path = relative(prefix, locator['relative_path'])
        elif source == 'distribution':
            distribution = installed[locator['package']]
            path = distribution_file(distribution, locator.get('relative_path'),
                locator.get('metadata_name'), locator.get('extension_stem'))
            need(path.is_relative_to(site), 'Declared package files stay in selected site directory')
        else:
            need(source == 'nauty_alias', 'Known explicit role locator')
            # Only this role admits a final-component alias. Its parent and
            # resolved target are ordinary paths, and its exact link is fixed.
            parent = relative(prefix, locator['parent'])
            path = parent / locator['name']
        kind = spec['kind']
        if kind == 'file':
            bindings[role] = dict(kind='file', identity=pin(path))
        elif kind == 'directory':
            need(path.is_dir(), 'Ordinary include/library directory')
            bindings[role] = dict(kind='directory', path=str(path))
        else:
            need(kind == 'symlink' and path.is_symlink(), 'Explicit nauty linker alias')
            link = os.readlink(path)
            need(link == spec['required_link'], 'Preserved exact nauty link/version premise')
            target = plain(path.resolve(strict=True))
            need(target.parent == path.parent, 'Link target stays in selected library directory')
            bindings[role] = dict(kind='symlink', path=str(path), link=link, target=pin(target))
    for role, spec in specs.items():
        if spec['kind'] == 'symlink':
            need(bindings[role]['target'] == bindings[spec['target_role']]['identity'],
                 'Linker alias and pinned library target agree')
    package_metadata = {}
    for name, distribution in installed.items():
        metadata = distribution_file(distribution, metadata_name='METADATA')
        package_metadata[name] = dict(version=distribution.version, metadata=pin(metadata))
    value = dict(schema='F012_PACKAGE_ENVIRONMENT_ROLES_V1', platform='darwin',
        bindings=bindings, extra_input_pins=[x['metadata'] for x in package_metadata.values()],
        packages=package_metadata, python=dict(executable=sys.executable,
            version=sys.version, site=str(site)), plan_sha256=args.plan_sha256,
        generator=pin(Path(__file__).resolve()), acceptance=None,
        qualification='Installed metadata/file identities only. No third-party import, compiler/build, ABI/convention test, installation or scientific execution.')
    encoded = (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()
    need(len(encoded) <= MIB, 'Bounded environment metadata')
    with output.open('xb') as stream:
        stream.write(encoded)
    print(json.dumps(dict(status='PREPARED_ENVIRONMENT_METADATA_ONLY', environment=pin(output),
        roles=len(bindings), package_imports=0, scientific_calls=0, acceptance=None)))


if __name__ == '__main__':
    main()
