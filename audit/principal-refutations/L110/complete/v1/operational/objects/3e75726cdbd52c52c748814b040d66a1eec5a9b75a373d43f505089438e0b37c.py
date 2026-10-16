"""Seal the written Suzuki component and its finite quotient controls."""
from pathlib import Path
import hashlib
import json
import sys
from pypdf import PdfReader

W = Path(__file__).resolve().parent
S = W.parents[2]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    path = Path(path).absolute()
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            h.update(b)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=h.hexdigest())


def main():
    need(not (W/'manifest.json').exists(), 'fresh frozen component')
    rows = {}
    def include(q):
        need(pin(q['path']) == q, 'unchanged acquired binding')
        need(q['path'] not in rows or rows[q['path']] == q, 'consistent duplicate binding')
        rows[q['path']] = q
    packet = W.parent/'preliminaries_review_adoption'
    q = pin(packet/'manifest.json')
    need(q['sha256'] == '10355f1d80ef410e1c2a4260e593cf685bab2d9b232e05f597a37e05cb85c7ce',
         'exact accepted preliminary results')
    include(q)
    for e in json.loads((packet/'manifest.json').read_text())['exports']:
        q = pin(packet/e['path'])
        need((q['bytes'], q['sha256']) == (e['bytes'], e['sha256']), 'accepted review export')
        include(q)
    for q in json.loads((packet/'dependencies.json').read_text()):
        include(q)
    source = S/'sources/older_L115_emis.pdf'
    q = pin(source)
    need(q['sha256'] == '8a94f8a0d72f46fececd21e7a6f437d76106936ef27c0dd18c55f6cd49dd6c51',
         'exact original source')
    include(q)
    include(pin(S/'sources/older_L115_emis.txt'))
    include(pin(S/'corpus106_L115_scalar_subspaces_v1/central_covers.tex'))
    include(pin(S/'corpus106_L115_scalar_subspaces_root_adoption/manifest.json'))
    for p in [Path(sys.executable), Path('/opt/homebrew/bin/pdflatex').resolve(),
              Path('/opt/homebrew/bin/gs').resolve()]:
        include(pin(p))
    proof = W/'families.tex'
    (W/'native02/families.tex').write_bytes(proof.read_bytes())
    need(len(PdfReader(W/'native02/families.pdf').pages) == 8, 'final eight native pages')
    log = (W/'native02/families.log').read_text()
    need('undefined' not in log.lower() and 'Overfull' not in log, 'complete native references and layout')
    c = json.loads((W/'quotient_controls01.json').read_text())
    need(c['status'] == 'PASS_LITERAL_SUZUKI_ROOT_QUOTIENT_CONTROLS', 'literal controls passed')
    need([x['q'] for x in c['rows']] == [8,32,128], 'exact small control parameters')
    contract = dict(source=pin(source), source_printed_pages=[105,106,107,108,109,110,111],
        source_pdf_page_offset=96, source_lemmas_rederived=['6.2','6.3','6.4','6.5','6.6','6.8'],
        source_lemma_retained={'6.7':'Classical Suzuki subgroup classification, attributed in source to Suzuki (1962).'},
        tables_rederived=[2,3,4,5,6,7], table6_correction=dict(printed_page=110,
        printed_condition='p prime dividing beta_q', corrected_condition='p prime dividing alpha_q',
        retained_hypothesis='beta_q prime', justification='Opposite nonsplit torus family; the printed condition repeats the first row.'),
        source_row_equivalence='Aut(G) on subgroup pairs, allowing type interchange; no arbitrary geometry isomorphism claim.',
        mathematical_new_ingredients=['Common normalizer incidence formula','Two root-group quotients and Frobenius/inversion actions',
        'Elementary embedding argument through equivariant additive maps'],
        priority_claim=False, new_conjecture_credit=0, whole_original_credit=0, Lean_certificate=False,
        remaining=['Remaining maximal-subfield parabolic families','Corrected global classification and global counts',
                   'Whole-source numerical examples and final synthesis'])
    (W/'source_contract.json').write_text(json.dumps(contract, indent=2)+'\n')
    (W/'audit.rst').write_text('Normalizer fibres in Suzuki geometries\n=====================================\n\n'
        'This is an author-complete component awaiting distinct review, not a complete L115 recovery.\n'
        'The eight-page proof treats Lemmas 6.2--6.6 and 6.8 and Tables 2--7.\n'
        'Lemma 6.7 is explicitly retained from Suzuki, as in the source.\n'
        'Table 6 needs p dividing alpha_q in its second row; its printed beta_q condition is preserved in the source contract.\n\n'
        'The author read the original printed pages 105--111 and directly viewed all eight final native proof pages.\n'
        'The earlier native01 is retained as an initial build; native02 is the final complete proof.\n'
        'The root-group controls use literal arithmetic at q=8,32,128 and no ambient Suzuki subgroup census.\n'
        'They verify coset partitions, normalizers inside the acquired involution centralizer, subgroup closure,\n'
        'Frobenius fixed sets, inversion classes, and all seven displayed orbit-count formulas.\n'
        'Run quotient_controls.py --out FRESH_PATH for a fresh independent replay.\n\n'
        'The preliminary component is acquired through its exact independent adoption.\n'
        'The scalar-subspace correction is cited for the remaining scope; its global conclusion is not reproduced.\n'
        'No global classification, new-conjecture answer, Lean verification, measurement, or whole-original credit is claimed.\n')
    (W/'dependencies.json').write_text(json.dumps(list(rows.values()), indent=2)+'\n')
    exports = []
    for p in sorted(W.rglob('*')):
        if p.is_file():
            q = pin(p)
            exports.append(dict(path=str(p.relative_to(W)), bytes=q['bytes'], sha256=q['sha256']))
    manifest = dict(status='AUTHOR_COMPLETE_L115_NORMALIZER_FAMILIES_AWAITING_DISTINCT_REVIEW',
                    author='l070_publication', exports=exports, proof_pages=8,
                    whole_original_credit=0, new_conjecture_credit=0, Lean_certificate=False)
    (W/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(dict(manifest=pin(W/'manifest.json'), exports=len(exports), dependencies=len(rows),
                         proof_pages=8, whole_original_credit=0)))


if __name__ == '__main__':
    main()
