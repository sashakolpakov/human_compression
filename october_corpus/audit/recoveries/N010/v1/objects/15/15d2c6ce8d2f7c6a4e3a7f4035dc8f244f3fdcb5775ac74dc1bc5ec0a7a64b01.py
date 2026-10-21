"""Bind accepted proofs and produce the complete N010 source-disposition record."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
import gzip
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter

W = Path(__file__).resolve().parent
S = Path('/Users/sasha/medusa/research/leemans')
R = Path('/Users/sasha/medusa/math_compression')
bindings = {}


def load(p):
    return json.loads(p.read_text())


def save(name, data):
    (W / name).write_text(json.dumps(data, indent=2) + '\n')


def bind(p, expected=None):
    p = p.resolve()
    raw = p.read_bytes()
    h = hashlib.sha256(raw).hexdigest()
    if expected and (h != expected['sha256'] or len(raw) != expected.get('bytes', len(raw))):
        raise ValueError('Changed acquired bytes: ' + str(p))
    root, ns = (S, 'study') if p.is_relative_to(S) else (R, 'public')
    if not p.is_relative_to(root):
        raise ValueError('Unregistered root: ' + str(p))
    row = dict(namespace=ns, path=str(p.relative_to(root)), bytes=len(raw), sha256=h)
    bindings[ns, row['path']] = row
    return row


def visit(x, base):
    if isinstance(x, dict):
        if isinstance(x.get('path'), str) and isinstance(x.get('sha256'), str):
            name = x['path']
            p = Path(name)
            if name.startswith('PUBLIC:'):
                candidates = [R / name[7:]]
            elif p.is_absolute():
                candidates = [p]
            elif x.get('namespace') == 'public' or x.get('root') == 'public_repo':
                candidates = [R / p]
            else:
                candidates = [base / p, S / p, R / p]
            matches = [q for q in candidates if q.is_file()
                       and hashlib.sha256(q.read_bytes()).hexdigest() == x['sha256']]
            if not matches:
                raise ValueError('Unresolved acquired pin: ' + str(base) + ' ' + name)
            bind(matches[0], x)
        for value in x.values():
            visit(value, base)
    elif isinstance(x, list):
        for value in x:
            visit(value, base)


private_names = [
    'corpus106_N010_source_contract_root_adoption',
    'corpus106_N010_realization_cone_v1',
    'corpus106_N010_realization_cone_independent_review',
    'corpus106_N010_realization_cone_root_adoption',
    'corpus106_N010_chamber_words_v1',
    'corpus106_N010_chamber_words_independent_review',
    'corpus106_N010_chamber_words_root_adoption',
    'corpus106_N010_universal_amalgamation_v1',
    'corpus106_N010_universal_amalgamation_independent_review',
    'corpus106_N010_universal_amalgamation_root_adoption',
    'corpus106_N010_oriented_examples_v1',
    'corpus106_N010_oriented_examples_root_review',
    'corpus106_L052_residue_theory_v1',
    'corpus106_L052_residue_theory_independent_review',
    'corpus106_L052_residue_theory_root_adoption',
]
private = []
for name in private_names:
    p = S / name
    m = load(p / 'manifest.json')
    private.append(dict(id=name, manifest=bind(p / 'manifest.json'), status=m['status']))
    for row in m['exports']:
        bind(p / row['path'], row)
        if row['path'] in ['dependencies.json', 'bindings.json', 'acquired_packets.json']:
            visit(load(p / row['path']), p)

for p in [W / 'source_contract02.json', W / 'SchulteWeiss.tex',
          W.parent / 'N010_retained_inputs/register01/manifest.json',
          W.parent / 'N010_retained_inputs/register01/retained_register.json',
          W.parent / 'N010_retained_inputs/register01/register.rst']:
    bind(p)
for row in load(W / 'source_contract02.json')['fixed_inputs']:
    visit(row, W)

# Existing public evidence is acquired in its published form. Each complete
# transport retains both its logical decoded pins and its actual stored bytes.
# No group census or proof-assistant build is repeated here.
published = []
decoded_cache = {}
for name in ['L038', 'L044', 'L045']:
    audit = R / f'audit/recoveries/{name}/v1'
    papers = R / f'papers/recoveries/{name}/v1'
    for directory in [audit, papers]:
        for p in sorted(directory.rglob('*')):
            if p.is_file():
                bind(p)
    transport = load(audit / 'transport.json')
    scientific = 0
    omitted = []
    for row in transport['files']:
        if 'public_path' not in row:
            if not row['transport'].endswith('HASH_ONLY'):
                raise ValueError('Unclassified public transport row')
            omitted.append(row)
            continue
        p = R / row['public_path']
        bind(p, dict(bytes=row['stored_bytes'], sha256=row['stored_sha256']))
        key = row['sha256'], row['bytes']
        if key not in decoded_cache:
            raw = p.read_bytes()
            if row['encoding'] == 'gzip':
                raw = gzip.decompress(raw)
            elif row['encoding'] != 'identity':
                raise ValueError('Unsupported published encoding')
            if (len(raw), hashlib.sha256(raw).hexdigest()) != (row['bytes'], row['sha256']):
                raise ValueError('Changed decoded public evidence')
            decoded_cache[key] = True
        scientific += 1
    published.append(dict(original=name, admission=bind(audit / 'admission.json'),
                          transport=bind(audit / 'transport.json'),
                          logical_records=len(transport['files']),
                          complete_scientific_records=scientific,
                          inherited_documentary_omissions=omitted,
                          all_stored_and_decoded_scientific_bytes_verified=True))

for topic in ['topic-a/v3', 'topic-locally-projective/v1', 'topic-chamber/v2']:
    directories = [R / 'papers' / topic, R / 'audit' / topic]
    count = 0
    for directory in directories:
        for p in sorted(directory.rglob('*')):
            if p.is_file():
                bind(p)
                count += 1
    published.append(dict(topic=topic, admission=bind(R / 'audit' / topic / 'admission.json'),
                          complete_published_files=count,
                          exact_scientific_scope='Only interfaces stated in the source and retained-input registers are used.'))

manuscripts = []
for ident, folder, stem, pages in [
    ('cone', 'corpus106_N010_realization_cone_v1', 'realization_cones', 4),
    ('words', 'corpus106_N010_chamber_words_v1', 'chamber_words', 3),
    ('amalgamation', 'corpus106_N010_universal_amalgamation_v1', 'universal_amalgamation', 2),
    ('examples', 'corpus106_N010_oriented_examples_v1', 'oriented_examples', 2)]:
    p = S / folder
    pdf = p / (stem + '.pdf')
    if len(PdfReader(pdf).pages) != pages:
        raise ValueError('Changed complete component page count')
    manuscripts.append(dict(id=ident, tex=bind(p / (stem + '.tex')),
                            pdf=bind(pdf), pages=pages, complete=True))

pdf = PdfReader(W / 'principal.pdf')
if len(pdf.pages) != 11:
    raise ValueError('Expected eleven synthesis pages')
(W / 'principal_expected.txt').write_text('\n\f\n'.join(p.extract_text() for p in pdf.pages))
volume = PdfWriter()
volume.append(W / 'principal.pdf')
for row in manuscripts:
    volume.append(S / row['pdf']['path'])
with (W / 'principal_and_components.pdf').open('wb') as f:
    volume.write(f)
save('acquired_manuscripts.json', dict(synthesis_pages=11, immediate_components=manuscripts,
                                      immediate_reading_volume_pages=22,
                                      older_acquired_proofs_are_additional=True))
save('acquired_packets.json', dict(private=private, published=published,
                                  no_new_census=True, no_new_Lean=True))
save('dependencies.json', sorted(bindings.values(), key=lambda x: (x['namespace'], x['path'])))
save('scope.json', dict(original='N010', source_kind='historical survey and problem collection',
     principal_disposition='Complete survey routing with common proofs, exact finite examples, earlier acquired answers and explicit retained classifications/reports; not all surveyed classifications are reproved.',
     contexts=16, established_clauses=51, numbered_questions=34, secondary_records=14,
     bibliography_entries=66, immediate_synthesis_pages=11, immediate_component_pages=11,
     new_question_credit=0, whole_original_credit=0, new_Lean_declarations=0,
     new_measurements=0, compression_factor=None, all_classifications_reproved=False,
     global_aggregates_reproduced=False, present_open_status_claimed=False))
save('provenance.json', dict(author='/root', distinct_principal_review='PENDING',
     common_theory_author='/root', common_theory_distinct_reviewer='/root/l044_resume',
     finite_examples_author='/root/l044_resume', finite_examples_distinct_reviewer='/root',
     source_contract_and_retained_register='Distinct source inspection by l044_resume; final synthesis joins and neighborliness proof by root.',
     new_mathematical_priority_claim=False,
     attribution='Established statements retain their authors in the survey bibliography and the exact earlier acquired manuscripts.'))
print(json.dumps(dict(status='N010_METADATA_AND_ACQUIRED_EDITIONS_PREPARED',
                      bindings=len(bindings), private_packets=len(private),
                      published_routes=len(published), decoded_public_objects=len(decoded_cache),
                      immediate_pages=22)))
