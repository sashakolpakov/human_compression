"""Portable exact F003 completion; no private-file fallback or new acquisition."""
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
F = S + '/geometry/suzuki_source_completion'
A = F + '/source_synthesis_v1'
ROOT = F + '/source_synthesis_root_review'
ROOT_SHA = '67b7fc885fbe290f0f730915e84af2dc2eb6c053562dc747787d291256cb6187'
AUTHOR_SHA = 'd8b81f8cd4ff74c3eda508f47ff8ffd278b58df698f40b56863f0ede1087f0ba'
PREFIX = 'audit/principal-refutations/F003/complete/v1'
PAPER = 'papers/corrections/F003/v1'
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
    need(t['format'] == 'F003_COMPLETION_EXACT_CONTENT_V1', 'known transport format')
    need(t['root_acceptance']['sha256'] == ROOT_SHA and t['author_manifest']['sha256'] == AUTHOR_SHA,
         'exact accepted root and author')
    root = ar.load(ROOT + '/manifest.json')
    need(root['status'] == 'ACCEPTED_F003_COMPLETE_SOURCE_TREATMENT', 'accepted complete-source status')
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
    for i in range(1, 5):
        original = A + ('/source-%02d.png' % i)
        row = ar.record(original)
        expected[row['sha256']] = dict(row, path=original)
    actual = {h: r for h, r in ar.objects.items() if r['kind'] not in ['NEW_PACKED_EXACT_CONTENT', 'EXISTING_PUBLIC']}
    premises = {r['sha256']: r for r in t['premises']}
    need(set(actual) == set(expected) == set(premises) and len(t['premises']) == 6,
         'only the six fixed original-source documentary premises')
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
    need(manifest['status'] == 'PRIVATE_F003_COMPLETION_STAGE_PENDING_OPERATIONAL_REVIEW', 'known stage status')
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
    selected.mkdir()
    for name in ['check.py', 'binary.py']:
        ar.extract(A + '/' + name, selected / name)
    sys.path.insert(0, str(selected))
    joined = module(selected / 'check.py', 'accepted_F003_assembly')
    claims = ar.load(A + '/claims.json')
    joined.ledger_check(claims)
    binary = joined.binary_check(joined.MATRIX)
    need(binary == ar.load(A + '/binary_result.json'), 'entire exact binary result')
    gate = ar.load(R + '/audit/principal-refutations/F003/v1/root_integration.json')
    need(gate['status'] == 'ROOT_ACCEPTED_F003_PRINCIPAL_REFUTATION_PUBLICATION', 'prior principal acceptance')
    need(gate['principal_refutation_credit'] == 1 and gate['ordinary_recovery_credit'] == 0,
         'prior principal disposition is unchanged')
    damage_names = []
    for name, mutate in [
        ('missing_source_case', lambda x: x['claims'].pop(11)),
        ('false_recovery_credit', lambda x: x.update(ordinary_recovery_credit=1)),
        ('conditional_argument_promoted', lambda x: x['claims'][-1].update(status='PROVED')),
        ('borrowed_premise_hidden', lambda x: x.update(borrowed_premises=[])),
    ]:
        bad = copy.deepcopy(claims)
        mutate(bad)
        try:
            joined.ledger_check(bad)
        except ValueError:
            damage_names.append(name)
        else:
            raise ValueError('accepted damaged claim ledger')
    for name, bad in [
        ('broken_symmetry', [[0, 0, 0, 1], *copy.deepcopy(joined.MATRIX[1:])]),
        ('identity_has_no_nonzero_defect', [[int(i == j) for j in range(4)] for i in range(4)]),
    ]:
        try:
            joined.binary_check(bad)
        except ValueError:
            damage_names.append(name)
        else:
            raise ValueError('accepted damaged binary witness')
    paper = stage / PAPER
    readable = ['symmetric.tex', 'symmetric.pdf', 'complete.tex', 'complete.pdf', 'claims.json', 'completion.rst',
                'proofs/principal.tex', 'proofs/principal.pdf']
    for name in readable:
        exact(paper / name, ar.record(A + '/' + name))
    for ext in ['.tex', '.pdf']:
        need((paper / ('proofs/principal' + ext)).read_bytes()
             == ar.content(R + '/corrections/suzuki-rank/v1/proof/rank4_counterexample' + ext),
             'accepted principal proof is unchanged')
    volume = PdfReader(paper / 'complete.pdf')
    need(len(volume.pages) == 12, 'complete readable volume')
    offset = 1
    for name, count in [('symmetric.pdf', 6), ('proofs/principal.pdf', 5)]:
        doc = PdfReader(paper / name)
        need(len(doc.pages) == count, 'whole manuscript length')
        for page in doc.pages:
            joined.embedded_page_check(page, volume.pages[offset])
            offset += 1
    need(offset == 12, 'all eleven mathematical pages')
    runs = []
    def run(label, command, cwd=None, timeout=30):
        result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
        (args.out / (label + '.stdout')).write_bytes(result.stdout)
        (args.out / (label + '.stderr')).write_bytes(result.stderr)
        runs.append(dict(label=label, command=command, returncode=result.returncode))
        need(result.returncode == 0 and not result.stderr, 'clean replay: ' + label)
        return result
    native_pages = 0
    if args.render:
        native = args.out / 'native'
        native.mkdir()
        texbin, gs = shutil.which('pdflatex'), shutil.which('gs')
        need(texbin and gs, 'TeX and Ghostscript available')
        for name in ['symmetric', 'complete', 'proofs/principal']:
            tex = paper / (name + '.tex')
            dest = native / Path(name).name
            dest.mkdir()
            for i in range(3):
                run(Path(name).name + '_tex' + str(i), [texbin, '-interaction=nonstopmode', '-halt-on-error',
                    '-output-directory', str(dest), tex.name], cwd=tex.parent)
            log = (dest / (tex.stem + '.log')).read_text()
            need('Overfull' not in log and 'undefined references' not in log, 'clean rebuilt native layout')
            joined.compare_pdfs(tex.with_suffix('.pdf'), dest / (tex.stem + '.pdf'))
        run('native_render', [gs, '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r105',
                            '-sOutputFile=' + str(native / 'page-%02d.png'), str(native / 'complete/complete.pdf')])
        images = sorted(native.glob('page-*.png'))
        need(len(images) == 12, 'twelve complete-volume native pages')
        for i, path in enumerate(images[:7], 1):
            need(path.read_bytes() == ar.content(A + f'/native/volume-{i:02d}.png'),
                 'exact directly viewed new manuscript raster')
        native_pages = 7
    run('codec_controls', [sys.executable, str(d / 'codec_controls.py'), '--out', str(args.out / 'codec_controls')])
    for flag in ['-O', '-OO']:
        result = subprocess.run([sys.executable, flag, str(d / 'portable_check.py')], capture_output=True, timeout=10)
        need(result.returncode != 0 and b'ordinary Python required' in result.stderr, 'portable optimization guard')
    result = dict(status='PASS_PORTABLE_F003_SOURCE_COMPLETION', stage_manifest=pin(d / 'manifest.json'),
                  transport=pin(d / 'transport.json'), root_acceptance=t['root_acceptance'], **closure,
                  logical_files=len(ar.rows), unique_objects=len(ar.objects), verified_payload_objects=verified,
                  verified_decoded_bytes=decoded, documentary_premises=6, existing_public_files=len(public),
                  restored_selected_files=2, exact_finite_replays=1, finite_result=binary,
                  claim_and_witness_damage_controls=damage_names,
                  native_entry_points=3, new_native_pages=native_pages, mathematical_pages=11, volume_pages=12,
                  page_drawing_streams_and_glyph_programs_match=True,
                  codec_controls=load(args.out / 'codec_controls/report.json'),
                  optimization_guards=2, new_group_acquisitions=0, principal_acquisition_repeated=False,
                  ordinary_recovery_delta=0, principal_refutation_delta=0, surviving_claim_registration_delta=0,
                  new_Lean=0, mathematical_compression_measurement=None, seconds=time.monotonic() - start, runs=runs)
    (args.out / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}))


if __name__ == '__main__':
    main()
