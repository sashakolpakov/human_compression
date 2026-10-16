"""Portable exact L029 completion; no private-file fallback or new acquisition."""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import time
from pypdf import PdfReader
import pack_codec as codec
from prior_transport_reader import Archive

S = '/Users/sasha/medusa/research/leemans'
R = '/Users/sasha/medusa/math_compression'
F = S + '/geometry/cplus_firmness'
A = F + '/source_synthesis_v1'
Q = F + '/panel_criterion_v1'
ROOT = F + '/source_synthesis_root_review'
ROOT_SHA = '6e30660c5f5dcd59e9992935fb453ef1fba8f0f42fc24004a2f50c4b5f44edfb'
AUTHOR_SHA = 'd6f03cda7ed4f4f309ccb36dfadde813b6c4d75edcd9f716ad659fdffefc4fce'
PREFIX = 'audit/principal-refutations/L029/complete/v1'
PAPER = 'papers/corrections/L029/v1'
need = codec.need


def load(path):
    return json.loads(path.read_text())


def pin(path):
    size, digest = codec.digest_file(path)
    return dict(path=str(path), bytes=size, sha256=digest)


def exact(path, row):
    need(codec.digest_file(path) == (row['bytes'], row['sha256']), 'exact file: ' + str(path))


def metadata(ar):
    t = ar.t
    need(t['format'] == 'L029_COMPLETION_EXACT_CONTENT_V1', 'known transport format')
    need(t['root_acceptance']['sha256'] == ROOT_SHA and t['author_manifest']['sha256'] == AUTHOR_SHA,
         'exact accepted root and author')
    root = ar.load(ROOT + '/manifest.json')
    need(root['status'] == 'ACCEPTED_L029_COMPLETE_SOURCE_SYNTHESIS', 'accepted complete-source status')
    rows = ar.load(ROOT + '/dependencies.json')
    rows += [dict(r, path=ROOT + '/' + r['path']) for r in root['exports']]
    rows.append(t['root_acceptance'])
    declared = {r['path']: r for r in rows}
    need(len(rows) == len(declared) and set(declared) == set(ar.originals), 'exact whole accepted closure')
    for row in rows:
        ar.exact(row)
    author = ar.load(A + '/manifest.json')
    for row in author['exports']:
        ar.exact(dict(row, path=A + '/' + row['path']))
    for row in ar.load(A + '/dependencies.json'):
        ar.exact(row)
    claims = ar.load(A + '/claims.json')
    expected = {claims[k]['sha256']: claims[k] for k in ['source_pdf', 'source_text']}
    actual = {h: r for h, r in ar.objects.items() if r['kind'] not in ['NEW_PACKED_EXACT_CONTENT', 'EXISTING_PUBLIC']}
    premises = {r['sha256']: r for r in t['premises']}
    need(set(actual) == set(expected) == set(premises) and len(t['premises']) == 2,
         'only the two fixed original-source documentary premises')
    for h, row in actual.items():
        need(row == premises[h] and row['kind'] == 'ORIGINAL_SOURCE_DOCUMENTARY_PREMISE', 'exact documentary premise kind')
        need(row['bytes'] == expected[h]['bytes'] and row['exact_locator'] == expected[h]['path'], 'exact original-source locator')
    return dict(root_closure=len(rows), author_exports=len(author['exports']))


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--expected-stage', required=True)
    parser.add_argument('--expected-transport', required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    repo = args.repo.resolve()
    stage = args.stage.resolve() if args.stage else repo
    d = stage / PREFIX
    need(args.out.is_absolute() and not args.out.exists(), 'fresh absolute output')
    need(shutil.disk_usage(args.out.parent).free >= 4 * 2**30 + 40 * 2**20, 'unchanged 4GiB replay reserve')
    need(pin(d / 'manifest.json')['sha256'] == args.expected_stage, 'externally pinned stage')
    need(pin(d / 'transport.json')['sha256'] == args.expected_transport, 'externally pinned transport')
    manifest = load(d / 'manifest.json')
    need(manifest['status'] == 'PRIVATE_L029_COMPLETION_STAGE_PENDING_OPERATIONAL_REVIEW', 'known stage status')
    exports = {r['path']: r for r in manifest['exports']}
    need(len(exports) == len(manifest['exports']), 'unique stage exports')
    for row in exports.values():
        exact(codec.resolve(row['path'], [stage]), row)
    for row in load(d / 'reused_tools.json'):
        exact(d / row['path'], row)
    t = load(d / 'transport.json')
    policy = load(d / 'premises.json')
    need(policy == dict(root=t['root_acceptance'], premises=t['premises']), 'exact premise inventory')
    ar = Archive(stage, repo, t)
    closure = metadata(ar)
    packs = {r['path']: r for r in t['packs']}
    need(len(packs) == len(t['packs']), 'unique packs')
    need({str(p.relative_to(stage)) for p in (d / 'packs').rglob('*') if p.is_file()} == set(packs), 'complete physical pack inventory')
    for name, row in packs.items():
        need(exports.get(name) == row and 0 < row['bytes'] <= 48 * 2**20, 'bounded exact pack')
    public = {r['path']: r for r in t['existing_public_files']}
    need(len(public) == len(t['existing_public_files']), 'unique public reuse files')
    tracked = set(subprocess.run(['git', '-C', str(repo), 'ls-files', '-z'], check=True,
                                capture_output=True).stdout.decode().split('\0'))
    for name, row in public.items():
        need(name in tracked, 'reused content is tracked')
        exact(codec.resolve(name, [repo]), row)
    spans = {name: [] for name in packs}
    used_public = set()
    verified = decoded = 0
    for h, row in ar.objects.items():
        need(h == row['sha256'], 'object hash identity')
        if row['kind'] == 'NEW_PACKED_EXACT_CONTENT':
            for segment in row['segments']:
                need(segment['path'] in packs, 'declared new pack')
                spans[segment['path']].append((segment['offset'], segment['offset'] + segment['bytes']))
            roots = [stage]
        elif row['kind'] == 'EXISTING_PUBLIC':
            name = row['public_path']
            old = public[name]
            need(row['encoding'] == 'identity' and (row['bytes'], h) == (old['bytes'], old['sha256']), 'exact old complete object')
            need(row['segments'] == ([dict(path=name, offset=0, bytes=old['bytes'])] if old['bytes'] else []), 'complete old public file')
            used_public.add(name)
            roots = [repo]
        else:
            continue
        codec.verify(row, roots)
        verified += 1
        decoded += row['bytes']
    for name, ranges in spans.items():
        end = 0
        for lo, hi in sorted(ranges):
            need(lo == end and hi > lo, 'nonoverlapping exact pack coverage')
            end = hi
        need(end == packs[name]['bytes'], 'no unindexed packed bytes')
    need(used_public == set(public), 'no unused public declarations')
    args.out.mkdir()
    selected = args.out / 'selected'
    names = ['panel_criterion_v1/' + n for n in ['check.py', 'check_seven.py', 'controls.py']]
    names += ['psl27_execution01/data/' + n for n in ['model.json'] + [f'marking{i:02d}.json' for i in range(1, 5)]]
    names.append('source_synthesis_v1/check.py')
    for name in names:
        ar.extract(F + '/' + name, selected / name)
    runs = []
    def run(label, command, cwd=None, timeout=30):
        result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
        (args.out / (label + '.stdout')).write_bytes(result.stdout)
        (args.out / (label + '.stderr')).write_bytes(result.stderr)
        runs.append(dict(label=label, command=command, returncode=result.returncode))
        need(result.returncode == 0 and not result.stderr, 'clean replay: ' + label)
        return result
    for name in ['check.py', 'check_seven.py', 'controls.py']:
        result = run(name, [sys.executable, str(selected / 'panel_criterion_v1' / name)])
        need(result.stdout == ar.content(Q + '/final05/' + name + '.stdout'), 'entire exact accepted finite output: ' + name)
    joined = module(selected / 'source_synthesis_v1/check.py', 'accepted_L029_assembly')
    claims = ar.load(A + '/claims.json')
    admission = ar.load(R + '/corrections/chiral-residues/v1/admission.json')
    joined.check_ledger(claims)
    joined.check_principal(admission)
    damage_names = []
    for name, mutate in [('missing_claim', lambda x: x['claims'].pop()),
                         ('ordinary_credit', lambda x: x.update(ordinary_recovery_credit=1)),
                         ('hidden_unproved_variant', lambda x: x.update(unproved_corrected_variants=[])),
                         ('refutation_called_proof', lambda x: x['claims'][0].update(status='PROVED'))]:
        bad = copy.deepcopy(claims)
        mutate(bad)
        try:
            joined.check_ledger(bad)
        except ValueError:
            damage_names.append(name)
        else:
            raise ValueError('accepted damaged claim ledger')
    bad = copy.deepcopy(admission)
    bad['accepted_counterexample']['full_group_order'] = 1092
    try:
        joined.check_principal(bad)
    except ValueError:
        damage_names.append('conflated_groups')
    else:
        raise ValueError('accepted wrong principal group')
    paper = stage / PAPER
    readable = ['residues.tex', 'residues.pdf', 'complete.tex', 'complete.pdf', 'claims.json', 'completion.rst']
    readable += ['proofs/' + stem + ext for stem in ['principal', 'panels', 'chirality'] for ext in ['.tex', '.pdf']]
    for name in readable:
        exact(paper / name, ar.record(A + '/' + name))
    volume = PdfReader(paper / 'complete.pdf')
    need(len(volume.pages) == 18, 'complete readable volume')
    offset = 1
    for name, count in [('residues.pdf', 7), ('proofs/principal.pdf', 5), ('proofs/panels.pdf', 3), ('proofs/chirality.pdf', 2)]:
        doc = PdfReader(paper / name)
        need(len(doc.pages) == count, 'whole manuscript length')
        for page in doc.pages:
            need(joined.normalized_text(page) == joined.normalized_text(volume.pages[offset]), 'exact included page text')
            content = page.get_contents().get_data()
            forms = [obj.get_object() for obj in volume.pages[offset]['/Resources']['/XObject'].values()]
            need(sum(obj.get('/Subtype') == '/Form' and obj.get_data() == content for obj in forms) == 1,
                 'exact included mathematical page stream')
            offset += 1
    need(offset == 18, 'all seventeen mathematical pages')
    native_pages = 0
    if args.render:
        native = args.out / 'native'
        native.mkdir()
        texbin, gs = shutil.which('pdflatex'), shutil.which('gs')
        need(texbin and gs, 'TeX and Ghostscript available')
        for name in ['residues', 'complete', 'proofs/principal', 'proofs/panels', 'proofs/chirality']:
            tex = paper / (name + '.tex')
            dest = native / Path(name).name
            dest.mkdir()
            for i in range(3):
                run(Path(name).name + '_tex' + str(i), [texbin, '-interaction=nonstopmode', '-halt-on-error',
                    '-output-directory', str(dest), tex.name], cwd=tex.parent)
            log = (dest / (tex.stem + '.log')).read_text()
            need('Overfull' not in log and 'undefined references' not in log, 'clean rebuilt native layout')
            fresh = PdfReader(dest / (tex.stem + '.pdf'))
            old = PdfReader(tex.with_suffix('.pdf'))
            need([p.extract_text() for p in fresh.pages] == [p.extract_text() for p in old.pages], 'unchanged rebuilt mathematical text')
        run('native_render', [gs, '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r105',
                            '-sOutputFile=' + str(native / 'page-%02d.png'), str(native / 'residues/residues.pdf')])
        images = sorted(native.glob('page-*.png'))
        need(len(images) == 7, 'seven synthesis native pages')
        for i, path in enumerate(images, 1):
            need(path.read_bytes() == ar.content(A + f'/residues-{i:02d}.png'), 'exact directly viewed synthesis raster')
        native_pages = 7
    run('codec_controls', [sys.executable, str(d / 'codec_controls.py'), '--out', str(args.out / 'codec_controls')])
    for flag in ['-O', '-OO']:
        result = subprocess.run([sys.executable, flag, str(d / 'portable_check.py')], capture_output=True, timeout=10)
        need(result.returncode != 0 and b'ordinary Python required' in result.stderr, 'portable optimization guard')
    result = dict(status='PASS_PORTABLE_L029_SOURCE_COMPLETION', stage_manifest=pin(d / 'manifest.json'),
                  transport=pin(d / 'transport.json'), root_acceptance=t['root_acceptance'], **closure,
                  logical_files=len(ar.rows), unique_objects=len(ar.objects), verified_payload_objects=verified,
                  verified_decoded_bytes=decoded, documentary_premises=2, existing_public_files=len(public),
                  restored_selected_files=len(names), exact_finite_replays=3, claim_damage_controls=damage_names,
                  native_entry_points=5, new_native_pages=native_pages, mathematical_pages=17, volume_pages=18,
                  page_texts_and_content_streams_match=True, codec_controls=load(args.out / 'codec_controls/report.json'),
                  optimization_guards=2, new_group_acquisitions=0, principal_acquisition_repeated=False,
                  ordinary_recovery_delta=0, principal_refutation_delta=0, surviving_claim_registration_delta=0,
                  new_Lean=0, mathematical_compression_measurement=None, seconds=time.monotonic() - start, runs=runs)
    (args.out / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}))


if __name__ == '__main__':
    main()
