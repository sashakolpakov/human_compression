"""Stage the two reviewed recoveries without changing the public checkout."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import shutil
import subprocess

S = Path('/Users/sasha/medusa/research/leemans')
R = S.parents[1] / 'math_compression'
W = S / 'reboot_20261013'
T = W / 'publication76/stage01'
AUD = 'audit/science76/v1'
IDS = ['F001', 'N012']
BASE = '6670d59d1172044616c808846cf1a1f220c83941'


def load(p):
    return json.loads(p.read_text())


def put(name, value):
    p = T / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(value, bytes):
        value = (value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    p.write_bytes(value)


def pin(name):
    p = T / name
    if not p.exists():
        p = R / name
    b = p.read_bytes()
    return dict(path=name, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def prepare():
    assert subprocess.check_output(['git', '-C', str(R), 'rev-parse', 'HEAD'], text=True).strip() == BASE
    assert not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain'], text=True).strip()
    assert not (T / AUD / 'baseline.json').exists()
    old = load(R / 'audit/corpus/latest.json')
    oldcat = load(R / old['active_catalogue']['path'])
    assert (old['admitted_principal_originals'], old['handled_mathematical_originals'], old['accessible_pending_complete_recovery']) == (74, 75, 30)
    assert set(IDS).issubset(old['accessible_pending_original_ids'])
    for orig in IDS:
        stage = W / (orig + '_publication_work/stage01')
        for p in stage.rglob('*'):
            if p.is_file():
                assert p.suffix != '.md'
                name = str(p.relative_to(stage))
                if (T / name).exists():
                    assert (T / name).read_bytes() == p.read_bytes()
                put(name, p.read_bytes())
    history = {}
    for name in ['README.rst', 'audit/completion.rst', 'audit/protocol.tex', 'audit/protocol.pdf', 'audit/corpus/latest.json', 'papers/latest_catalogue.json', 'papers/catalogue_corrected_unmeasured.json', 'scripts/verify_snapshot.py']:
        target = AUD + '/previous/' + name
        put(target, (R / name).read_bytes())
        history[name] = pin(target)
    put(AUD + '/history_routes.json', dict(base_commit=BASE, routes=history, scope='Eight exact prior mutable files; all earlier science and refutation checks remain required.'))
    put(AUD + '/baseline.json', dict(base_commit=BASE, old_catalogue=old['active_catalogue'], history=history, measured_overview=pin('audit/overview/v19/admission.json')))
    ads = {}
    adpins = {}
    for orig in IDS:
        ow = W / (orig + '_publication_work')
        integration = ow / 'integration01'
        rec = 'audit/recoveries/' + orig + '/v1'
        nat = 'papers/recoveries/' + orig + '/v1'
        put(rec + '/scope_routes.json', (integration / 'scope_routes.json').read_bytes())
        put(nat + '/PUBLICATION.rst', (integration / 'PUBLICATION.rst').read_bytes())
        checker = ow / 'portable_check.py' if orig == 'F001' else W / 'N012_portable_check.py'
        put(rec + '/checker/portable.py', checker.read_bytes())
        put(AUD + '/reports/' + orig + '-portable.json', (ow / 'portable01/report.json').read_bytes())
        directory = S / ('corpus106_' + orig + '_portable_independent_review')
        manifest = load(directory / 'manifest.json')
        paths = [directory / 'manifest.json'] + [directory / r['path'] for r in manifest['exports']]
        paths += [S / r['path'] for r in load(directory / 'dependencies.json')['bindings']]
        mapping = {}
        for p in paths:
            b = p.read_bytes()
            name = rec + '/operational-review/objects/' + hashlib.sha256(b).hexdigest() + ('.txt' if p.suffix == '.md' else p.suffix)
            put(name, b)
            mapping[str(p.relative_to(S))] = pin(name)
        put(rec + '/operational-review/mapping.json', dict(bindings=mapping, scope='Exact distinct operational review and all declared inputs; historical private identifiers are never runtime fallbacks.'))
        ad = load(integration / 'admission_proposal.json')
        ad.update(status='ROOT_ACCEPTED_COMPONENTS_PUBLICATION_REQUIRES_SCIENCE76_GATE', publication_gate=AUD + '/root_integration.json', source_map=pin(rec + '/scope_routes.json'), portable_report=pin(AUD + '/reports/' + orig + '-portable.json'), portable_checker=pin(rec + '/checker/portable.py'), portable_review=pin(rec + '/operational-review/mapping.json'), publication_gate_remaining=True)
        put(rec + '/admission.json', ad)
        ads[orig] = ad
        adpins[orig] = pin(rec + '/admission.json')
    reg = dict(status='ROOT_ACCEPTED_COMPONENTS_REGISTRATION_REQUIRES_SCIENCE76_GATE', source_ids=IDS, admissions=[adpins[x] for x in IDS], principal_originals_added=2, measurement_originals_added=0, new_question_credit=0, new_Lean_declarations=0, whole_source_formalized=False, comparison_topics_added=0, compression_factor=None, previous_registration=old['current_science_registration'])
    put(AUD + '/new_original_registration.json', reg)
    regpin = pin(AUD + '/new_original_registration.json')
    unmeasured = sorted(old['measurement_pending_original_ids'] + IDS)
    handled = sorted(old['handled_mathematical_original_ids'] + IDS)
    cat = copy.deepcopy(oldcat)
    cat.update(status='CURRENT_ACCESSIBLE106_76_RECOVERED_1_REFUTED_28_PENDING', admitted_principal_originals=76, accessible_pending_complete_recovery=28, handled_mathematical_originals=77, handled_mathematical_original_ids=handled, measurement_pending_original_ids=unmeasured, new_proof_credit=2, new_principal_refutation_credit=0, review_revision='Only F001 and N012 become complete reviewed principal recoveries; all other original records are unchanged. N012 includes an explicit correction to Corollary 4.2.1.', previous_catalogue=old['active_catalogue'], current_recovery_counts=dict(active=106, admitted=76, refuted=1, handled=77, measured=53, measurement_pending=23, pending=28, editorial=1))
    for row in cat['entries']:
        orig = row['original_id']
        if orig not in IDS:
            continue
        ad = ads[orig]
        previous = copy.deepcopy(row['current_principal_recovery'])
        row['current_principal_recovery'] = dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING', latest_admission_references=[adpins[orig]], historical_admission_evidence=previous, principal_contract_admitted=True, all_original_assertions_claimed=False, literal_principal_theorem_recovered=ad['literal_principal_theorem_recovered'], measured=False, summary=ad['principal_contract'], retained_inputs=ad['retained_inputs'], publication_gate=AUD + '/root_integration.json')
        if orig == 'F001':
            row['current_principal_recovery']['auxiliary_correction'] = ad['auxiliary_correction']
            row['next_obligation'] = 'No principal rank-spectrum case remains. The separate auxiliary correction is retained. Measurement, the higher-dimensional question and further formalization are deferred until the fixed intake stopping point.'
        else:
            row['current_principal_recovery']['corrected_numbered_claim'] = ad['corrected_numbered_claim']
            row['next_obligation'] = 'No case of the twelve principal classifications or either table remains. Corollary 4.2.1 has the explicitly corrected centre structure. Measurement and further formalization are deferred until the fixed intake stopping point.'
    assert all(a == b for a, b in zip(oldcat['entries'], cat['entries']) if a['original_id'] not in IDS)
    cp = 'audit/corpus/accessible106/updates/corrected-unmeasured76-catalogue.json'
    put(cp, cat)
    c = copy.deepcopy(old)
    c.update(status='CURRENT_PROGRAMME_76_RECOVERED_1_REFUTED_28_PENDING_1_EDITORIAL', admitted_principal_originals=76, accessible_pending_complete_recovery=28, handled_mathematical_originals=77, handled_mathematical_original_ids=handled, admitted_original_ids=sorted(old['admitted_original_ids'] + IDS), accessible_pending_original_ids=[x for x in old['accessible_pending_original_ids'] if x not in IDS], measurement_pending_original_ids=unmeasured, scientific_unmeasured_original_ids=unmeasured, previous_snapshot=history['audit/corpus/latest.json'], active_catalogue=pin(cp), current_science_registration=regpin)
    c['added_admissions'].append(regpin)
    c.pop('snapshot', None)
    sp = 'audit/corpus/updates/accessible106-corrected-unmeasured76.json'
    put(sp, c)
    c['snapshot'] = pin(sp)
    put('audit/corpus/latest.json', c)
    sc = load(R / 'papers/catalogue_corrected_unmeasured.json')
    for orig in IDS:
        for p in ads[orig]['new_native_manuscripts']:
            sc['entries'].append(dict(id=p['id'], title=p['title'], tex=p['tex']['path'], pdf=p['pdf']['path'], tex_inputs=[], compiler='pdflatex', physical_pages=p['physical_pages'], role=p.get('role', 'Complete principal recovery component'), source_ids=[orig], topic='Classical groups and regular polytopes', comparison_topic_created=False, measured=False, compression_factor=None, existing_public_dependency=not p['pdf']['path'].startswith('papers/recoveries/' + orig + '/v1/'), admission=adpins[orig]))
    sc['original_ids'] += IDS
    sc['root_publication_gate'] = AUD + '/root_integration.json'
    put('papers/catalogue_corrected_unmeasured.json', sc)
    pa = load(R / 'papers/latest_catalogue.json')
    pa.update(status='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_TWENTY_THREE_CORRECTED_UNMEASURED', active_source_catalogue=pin(cp), corrected_unmeasured_scientific_catalogue=pin('papers/catalogue_corrected_unmeasured.json'))
    put('papers/latest_catalogue.json', pa)
    summary = ('F001 recovers the complete rank spectrum of the projective symplectic group\nin dimension four over every finite field. A separate counterexample corrects\nan auxiliary lemma on orthogonal subgroups; the principal theorem holds. N012\nrecovers all twelve principal classifications and both tables in the 2025\nthesis on linear groups, with an explicit correction to the centre structure in\nCorollary 4.2.1. Their complete proofs, retained inputs and distinct component\nreviews are available through their publication guides. Neither recovery\nadds a compression factor, an open-conjecture claim or a complete Lean proof.\n\n')
    for name in ['README.rst', 'audit/completion.rst', 'audit/protocol.tex']:
        txt = (R / name).read_text()
        for a, b in [('74 accessible originals', '76 accessible originals'), ('74 reviewed corrected principal recoveries', '76 reviewed corrected principal recoveries'), ('53 are measured and twenty-one', '53 are measured and twenty-three'), ('L038 and F006', 'L038, F006, F001 and N012'), ('30 await a complete', '28 await a complete'), ('30 originals\n', '28 originals\n'), ('Thus 75 of', 'Thus 77 of'), ('handled: 74 recoveries', 'handled: 76 recoveries'), ('All twenty-one source editions', 'All twenty-three source editions'), ('None of these twenty-one recoveries', 'None of these twenty-three recoveries'), ('science74/v1/new_original_registration.json', 'science76/v1/new_original_registration.json'), ('Of the 74 corrected recoveries', 'Of the 76 corrected recoveries'), ('106={}&74', '106={}&76'), ('&+30\\', '&+28\\')]:
            txt = txt.replace(a, b)
        if name == 'README.rst':
            marker = 'All twenty-three source editions'
            insert = 'The `F001 guide <papers/recoveries/F001/v1/PUBLICATION.rst>`_ and\n`N012 guide <papers/recoveries/N012/v1/PUBLICATION.rst>`_ give the two new recoveries.\n\n' + summary
        else:
            marker = 'The `current overview' if name.endswith('.rst') else 'The accepted overview v19'
            insert = summary.replace('linear-group', 'linear group').replace('orthogonal-subgroup', 'orthogonal subgroup')
        assert marker in txt
        put(name, txt.replace(marker, insert + marker, 1))
    oldv = (R / 'scripts/verify_snapshot.py').read_text()
    added = '''def check_previous_science76():
    spec=importlib.util.spec_from_file_location('science76_history',ROOT/'scripts/check_science76_history.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def check_science76():
    spec=importlib.util.spec_from_file_location('science76',ROOT/'scripts/check_science76.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

'''
    newv = oldv.replace('def main():', added + 'def main():', 1).replace('science_history = check_previous_science74()', 'science_history = check_previous_science76()').replace('science72 = check_science74()', 'science72 = check_science76()')
    ast.parse(newv)
    put('scripts/verify_snapshot.py', newv)
    hist = (R / 'scripts/check_science74_history.py').read_text()
    hist = hist.replace('science72', 'science74').replace('SCIENCE73', 'SCIENCE74').replace("AUD='audit/science74/v1'", "AUD='audit/science76/v1'").replace('module.check_previous_science73()', 'module.check_previous_science74()').replace('module.check_science73()', 'module.check_science74()').replace("['corrected_recoveries']!=73", "['corrected_recoveries']!=74").replace("['mathematical_pending']!=31", "['mathematical_pending']!=30").replace("prefix='F003-history-'", "prefix='science76-history-'")
    ast.parse(hist)
    put('scripts/check_science76_history.py', hist)
    print(json.dumps(dict(status='PREPARED_PRIVATE_SCIENCE76', stage=str(T), recoveries=76, refutations=1, handled=77, pending=28, measured=53, unmeasured=23, public_written=False)))


if __name__ == '__main__':
    prepare()
