"""Full-manuscript Topic E accounting; closed intake, no Markdown dependency.

Requires pypdf 6.13.0. Pass the private existing study as --sources-root and
public research/case_study as --artifacts-root. Output must be fresh.
No primary text is exported. This is a length audit, not a mathematical replay.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import pypdf

PROTOCOL_SHA256 = '52d01294d4462b15e0cc7a0a8ddfeac07334a055e186c697b7116d78b8aad3a9'


def need(ok, message):
    if not ok:
        raise ValueError('TOPIC_E_MEASUREMENT_REJECT ' + message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_bound(path, expected, label):
    data = path.read_bytes()
    need(sha(data) == expected, label + ' hash')
    return data


def metrics(text, normalization):
    normalized = unicodedata.normalize(normalization, text)
    collapsed = ' '.join(normalized.split())
    return dict(whitespace_tokens=len(collapsed.split()),
                alphanumeric_units=len(re.findall(r'[^\W_]+', normalized)),
                characters_without_whitespace=sum(not c.isspace() for c in normalized),
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                collapsed_text_sha256=sha(collapsed.encode()))


def select(raw, binding):
    for group in ['included_spans', 'excluded_furniture']:
        previous = -1
        for span in binding[group]:
            a, b = span['start'], span['end']
            need(previous <= a < b <= len(raw), 'invalid/overlapping ' + group)
            need(sha(raw[a:b].encode()) == span['sha256'], group + ' hash')
            previous = b
    for furniture in binding['excluded_furniture']:
        need(any(s['start'] <= furniture['start'] < furniture['end'] <= s['end']
                 for s in binding['included_spans']), 'furniture not in selected manuscript')
    pieces = []
    for span in binding['included_spans']:
        at = span['start']
        for furniture in binding['excluded_furniture']:
            if span['start'] <= furniture['start'] < furniture['end'] <= span['end']:
                pieces.append(raw[at:furniture['start']])
                at = furniture['end']
        pieces.append(raw[at:span['end']])
    return '\n'.join(pieces)


def read_pdf(root, key, binding):
    path = root / binding['path']
    read_bound(path, binding['pdf_sha256'], key + ' PDF')
    pages = [page.extract_text() or '' for page in pypdf.PdfReader(path).pages]
    need(len(pages) == binding['pages'], key + ' pages')
    raw = '\n'.join(pages)
    need(sha(raw.encode()) == binding['extraction_sha256'], key + ' extraction')
    at = 0
    for i, (page, record) in enumerate(zip(pages, binding['page_bindings']), 1):
        need(record == dict(page=i, start=at, end=at+len(page), sha256=sha(page.encode())), key + ' page binding')
        at += len(page) + 1
    need(len(binding['page_bindings']) == len(pages), key + ' page binding count')
    return raw


def reject_controls(protocol, raw, code):
    rejected = []
    cases = []
    changed = copy.deepcopy(protocol['sources']['L083'])
    changed['included_spans'][0]['end'] -= 1
    cases.append(('changed_full_manuscript_boundary', lambda: select(raw['L083'], changed)))
    cases.append(('changed_extracted_source', lambda: select(raw['L083'] + 'x', dict(protocol['sources']['L083'],
                  included_spans=[dict(protocol['sources']['L083']['included_spans'][0], end=len(raw['L083'])+1)]))))
    cases.append(('changed_required_program', lambda: need(sha(code+b' ') == protocol['render']['code_sha256'], 'required program hash')))
    changed_protocol = copy.deepcopy(protocol)
    changed_protocol['third_application_included'] = True
    cases.append(('changed_protocol_scope', lambda: need(sha((json.dumps(changed_protocol,indent=2,ensure_ascii=False)+'\n').encode()) == PROTOCOL_SHA256, 'protocol hash')))
    for label, action in cases:
        try:
            action()
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('accepted negative control ' + label)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources-root', type=Path, required=True)
    parser.add_argument('--artifacts-root', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, default=Path(__file__).with_name('topic_E_full_manuscript_protocol.json'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output required')
    protocol = json.loads(read_bound(args.protocol, PROTOCOL_SHA256, 'protocol'))
    need(pypdf.__version__ == protocol['pypdf_version'], 'pypdf version')
    old = json.loads(read_bound(args.artifacts_root/protocol['prior_boundaries_path'],
                               protocol['prior_boundaries_sha256'], 'old boundaries'))
    old_result = json.loads(read_bound(args.artifacts_root/protocol['prior_measurement_path'],
                                      protocol['prior_measurement_sha256'], 'old measurement'))
    need(protocol['ours'] == old['ours'] and protocol['render'] == old['render'], 'unchanged replacement boundary')
    raw, costs, old_costs, raw_costs = {}, {}, {}, {}
    for key, binding in (protocol['sources'] | protocol['ours']).items():
        root = args.sources_root if key in protocol['sources'] else args.artifacts_root
        raw[key] = read_pdf(root, key, binding)
        text = select(raw[key], binding)
        costs[key] = {form: metrics(text, form) for form in protocol['normalizations']}
        previous_binding = (old['sources'] | old['ours'])[key]
        old_costs[key] = {form: metrics(select(raw[key],previous_binding),form) for form in protocol['normalizations']}
        need(old_costs[key] == old_result['costs'][key], key + ' prior ten-coordinate replay')
        if key in protocol['sources']:
            raw_costs[key] = {form: metrics(raw[key],form) for form in protocol['normalizations']}
    code = read_bound(args.artifacts_root/protocol['render']['code_path'], protocol['render']['code_sha256'], 'required code')
    read_bound(args.artifacts_root/protocol['render']['config'], protocol['render']['config_sha256'], 'code rendering configuration')
    need(re.sub(r'\s+', '', code.decode()) in re.sub(r'\s+', '', select(raw['Code'],protocol['ours']['Code'])), 'complete program in counted appendix')
    comparisons = {}
    for form in protocol['normalizations']:
        comparisons[form] = {}
        for metric in protocol['metrics']:
            c = {key: values[form][metric] for key,values in costs.items()}
            oldc = {key: values[form][metric] for key,values in old_costs.items()}
            full = c['L083']+c['L079']
            written = c['U_E']+c['A1']+c['A2']
            with_code = written+c['Code']
            comparisons[form][metric] = dict(
                full_source_manuscripts=full,
                source_matched_proof_spans=oldc['L083']+oldc['L079'],
                replacement_complete_manuscripts=written,
                replacement_complete_manuscripts_and_required_code=with_code,
                full_manuscript_written_factor=full/written,
                full_source_text_over_our_known_proof_and_code=full/with_code,
                exact_all_artifact_factor=None,
                matched_proof_written_factor=(oldc['L083']+oldc['L079'])/written,
                full_document_untrimmed_source_sensitivity=sum(v[form][metric] for v in raw_costs.values()),
                local_factors_conditioned_on_full_umbrella_and_shared_program={'L083':c['L083']/c['A1'],'L079':c['L079']/c['A2']},
                acquisition={'umbrella':c['U_E'],'shared_program':c['Code'],'total':c['U_E']+c['Code']},
                source_sequence=[c['L083'],c['L079']],
                source_cumulative=[c['L083'],full],
                replacement_application_sequence=[c['A1'],c['A2']],
                replacement_written_cumulative=[c['U_E']+c['A1'],written],
                replacement_with_code_cumulative=[c['U_E']+c['Code']+c['A1'],with_code])
    result = dict(status='PASS_PRIVATE_MEASUREMENT_PENDING_ROOT_REVIEW',
        scope='Two complete source manuscripts for the predeclared principal results; L021 excluded. Full manuscript length does not assert every ancillary statement is rederived.',
        protocol_sha256=PROTOCOL_SHA256,checker_sha256=sha(Path(__file__).read_bytes()),
        prior_boundaries_sha256=protocol['prior_boundaries_sha256'],prior_measurement_sha256=protocol['prior_measurement_sha256'],
        pypdf=pypdf.__version__,primary=protocol['primary'],costs=costs,comparisons=comparisons,
        raw_source_extraction_sensitivity=raw_costs,
        source_pages={k:v['pages'] for k,v in protocol['sources'].items()},
        replacement_pages={k:v['pages'] for k,v in protocol['ours'].items()},
        source_pdf_hashes={k:v['pdf_sha256'] for k,v in protocol['sources'].items()},
        replacement_pdf_hashes={k:v['pdf_sha256'] for k,v in protocol['ours'].items()},
        main_result_contracts=protocol['main_result_contracts'],
        historical_required_program_cost=None,external_library_unconditional_cost=None,
        exact_all_artifact_factor=None,
        known_cost_coordinate_interpretation='The source text divided by our complete manuscript-plus-code cost is a known-cost coordinate. It is not an exact comparison of all historical and replacement artifacts because historical code cost is unknown. Under the same retained-library convention and nonnegative unknown historical code it also gives a conservative lower bound; that bound alone is not total proof-cost compression.',
        old_ten_coordinate_document_replay=True,complete_required_code_present=True,
        negative_controls=reject_controls(protocol,raw,code),
        measurement_limits=['No new source, result or conjecture credit.','No minimum-description-length claim.','One acquisition followed by two applications; not a repeated sawtooth or long-run trend.','Optional partial Lean and audit infrastructure not included as mathematical premises.','All source ancillary discussion and references counted but omissions remain explicit.','No altered source formulas, OCR repair, or primary text redistribution.'])
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result['comparisons']['NFC']['characters_without_whitespace'],indent=2))

if __name__ == '__main__':
    main()
