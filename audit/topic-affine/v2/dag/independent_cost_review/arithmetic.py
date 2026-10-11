#!/usr/bin/env python3
"""Independent cost arithmetic; semantic ownership reading is a separate review.

Reuses only the already accepted input extractor. No cost-author allocator,
interface builder, route code or reader is imported.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unicodedata

PIN = '7a1cd77556e3addc9a9453f010d9ddfa1b94f816d0a648060d00e0874a363216'
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def empty():
    return {v: {f: dict.fromkeys(UNITS, 0) for f in FORMS} for v in VARIANTS}


def total(owners, costs):
    names = set(owners)
    return {v: {f: {u: sum(costs[n][v][f][u] for n in names) for u in UNITS}
                for f in FORMS} for v in VARIANTS}


def allocate(text, spans, form):
    # Normalize each exact passage and check that no normalization crosses a cut.
    tagged = []
    for span in spans:
        tagged.extend((c, span['owner']) for c in unicodedata.normalize(
            form, text[span['start']:span['end']]))
    require(''.join(c for c, _ in tagged) == unicodedata.normalize(form, text),
            'Normalization crosses an ownership boundary')
    out = {s['owner']: dict.fromkeys(UNITS, 0) for s in spans}
    in_word = in_alphanum = False
    had_text = False
    pending_space_owner = None
    for char, owner in tagged:
        nonspace = not char.isspace()
        alphanum = char.isalnum()
        if nonspace and not in_word:
            out[owner]['whitespace_tokens'] += 1
        if alphanum and not in_alphanum:
            out[owner]['alphanumeric_units'] += 1
        if nonspace:
            if pending_space_owner is not None:
                out[pending_space_owner]['characters_with_collapsed_whitespace'] += 1
                out[pending_space_owner]['utf8_bytes_with_collapsed_whitespace'] += 1
            pending_space_owner = None
            out[owner]['characters_without_whitespace'] += 1
            out[owner]['characters_with_collapsed_whitespace'] += 1
            out[owner]['utf8_bytes_with_collapsed_whitespace'] += len(char.encode())
            had_text = True
        elif had_text and pending_space_owner is None:
            pending_space_owner = owner
        in_word, in_alphanum = nonspace, alphanum
    return out


def check(study, packet):
    manifest = packet / 'manifest.json'
    require(digest(manifest.read_bytes()) == PIN, 'Exact cost author manifest')
    for row in read(manifest)['exports']:
        data = (packet / row['path']).read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'],
                'Changed author export: ' + row['path'])
    for name, pin in read(packet / 'protocol.json')['input_pins'].items():
        require(digest((study / name).read_bytes()) == pin, 'Changed accepted input: ' + name)
    spec = importlib.util.spec_from_file_location('accepted_affine_extraction',
                                                study / 'topic_Affine_measurement/extract_inputs.py')
    sys.path.insert(0, str(study / 'topic_Affine_measurement'))
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    require(extractor.pypdf.__version__ == '6.13.0', 'Pinned parser')
    source = read(study / 'topic_Affine_measurement/source_input_spec.json')['sources']
    replacements = read(study / 'topic_Affine_measurement/replacement_input_spec.json')
    inputs = source | replacements['ours']
    partition = read(packet / 'partition.json')
    weights = read(packet / 'weights.json')
    require(all(weights[k] is None for k in [
        'expanded_external_proof_cost', 'historical_software_cost', 'graphic_cost',
        'minimum_description_cost', 'compression_ratio']),
        'Unmeasured global costs and proof-compression factor remain unknown')
    require(all(weights[k] == 0 for k in [
        'new_source_credit', 'new_question_credit', 'new_formal_credit']), 'No new credit')
    graph = read(study / 'topic_Affine_logical_dag_v2/logical_graph.json')
    coverage = read(study / 'topic_Affine_logical_dag_v2/coverage.json')
    accepted_counts = read(study / 'topic_Affine_measurement_independent_review/recount.json')['documents']
    owners = partition['owners']
    costs = {n: empty() for n in owners}
    spans_checked = 0
    for name, inp in inputs.items():
        extracted = extractor.document(study, name, inp)
        document = partition['documents'][name]
        require(document['pdf_sha256'] == inp['pdf_sha256'] and document['pages'] == inp['pages'],
                'Same measured document')
        for variant, text in zip(VARIANTS, extracted[:3]):
            record = document['variants'][variant]
            require(len(text) == record['length'] and digest(text.encode()) == record['sha256'],
                    'Complete extracted text')
            end = 0
            for span in record['spans']:
                start, stop = span['start'], span['end']
                require(start == end and start < stop <= len(text), 'Disjoint exhaustive passage cuts')
                require(digest(text[start:stop].encode()) == span['sha256'], 'Exact passage content')
                require(owners[span['owner']]['document'] == name and
                        owners[span['owner']]['category'] == span['category'], 'Owner document and category')
                end = stop
                spans_checked += 1
            require(end == len(text), 'No omitted document suffix')
            if name == 'L012':
                kernels = [s for s in record['spans'] if s['owner'] == 'h.64.Kernels.remaining']
                require(len(kernels) == 1 and text[kernels[0]['start']:kernels[0]['end']].startswith(
                    'Similarly, L and M\nare also'), 'Complete kernel subject belongs to kernel proof')
            for form in FORMS:
                values = allocate(text, record['spans'], form)
                for owner, units in values.items():
                    costs[owner][variant][form] = units
                expected = {u: accepted_counts[name]['variants'][variant][form][u] for u in UNITS}
                require({u: sum(x[u] for x in values.values()) for u in UNITS} == expected,
                        'Conservation against independent full-document counts')
    require(costs == weights['owner_costs'], 'Every independent owner metric')
    require(weights['document_costs'] == {d: total([n for n, o in owners.items() if o['document'] == d], costs)
                                        for d in inputs}, 'Every document weight conserves its owners')
    raw_files_checked = 0
    for category, source_category, size in [
            ('raw_program_alternative', 'complete_mathematical_programs', 6),
            ('raw_auxiliary_files', 'complete_auxiliary_scripts', 3),
            ('raw_formal_files', 'complete_formal_files', 3)]:
        records = weights[category]
        declared = {r['path']: r for r in replacements[source_category]}
        require(len(records) == len(declared) == size and
                {r['binding']['path'] for r in records.values()} == set(declared), 'Complete raw inventory')
        for record in records.values():
            binding = record['binding']
            require(binding == declared[binding['path']], 'Exact accepted raw-file role and binding')
            data = (study / binding['path']).read_bytes()
            require(len(data) == binding['bytes'] and digest(data) == binding['sha256'], 'Whole raw-file bytes')
            text = data.decode()
            metrics = {f: allocate(text, [{'start': 0, 'end': len(text), 'owner': 'whole'}], f)['whole']
                       for f in FORMS}
            require(metrics == record['metrics'], 'Independent whole raw-file metrics')
            raw_files_checked += 1
    nodes = {n['id']: n for n in graph['nodes']}
    parents = {n: set() for n in nodes}
    for edge in graph['edges']:
        if edge['kind'] in graph['logical_edge_kinds']:
            parents[edge['target']].add(edge['source'])

    def closure(start):
        out = set(start)
        while True:
            new = out | {p for n in out for p in parents[n]}
            if new == out:
                return out
            out = new

    links = weights['node_interfaces']
    require(set(links) == set(nodes), 'Every logical interface')
    for name, link in links.items():
        require(len(link['owners']) == len(set(link['owners'])) and set(link['owners']) <= owners.keys(),
                'Distinct existing interface owners')
        if nodes[name]['side'] in ['external', 'verification']:
            require(link['owners'] == [] and link['known_weight'] is None, 'Unknown proof cost is not zero')
        else:
            require(link['known_weight'] == total(link['owners'], costs), 'Interface sum')
    routes_checked = 0

    def route(record, expected):
        nonlocal routes_checked
        require(record['logical_nodes'] == sorted(expected), 'Exact logical prerequisite closure')
        owned = {p for n in expected for p in links[n]['owners']}
        require(record['owners'] == sorted(owned), 'Union before sum')
        require(record['known_extracted_subtotal'] == total(owned, costs), 'Route subtotal')
        docs = {owners[n]['document'] for n in owned}
        require(record['by_document'] == {d: total([n for n in owned if owners[n]['document'] == d], costs)
                                         for d in sorted(docs)}, 'Route costs by document')
        raw = weights['raw_program_alternative']
        programs = set(expected) & raw.keys()
        written = {n for n in owned if owners[n]['document'] != 'CODE'}
        alternative = total(written, costs)
        for v in VARIANTS:
            for f in FORMS:
                for u in UNITS:
                    alternative[v][f][u] += sum(raw[n]['metrics'][f][u] for n in programs)
        require(record['raw_program_alternative_subtotal'] == alternative, 'Whole raw alternative without printed charge')
        require(record['unknown_inputs'] == sorted(n for n in expected if links[n]['known_weight'] is None),
                'Unknown dependencies preserved')
        require(record['expanded_dependency_cost'] is None and record['graphics_cost'] is None,
                'Unmeasured cost stays null')
        routes_checked += 1

    for name in nodes:
        route(weights['individual_node_closures'][name], closure([name]))
    require(len(weights['source_contract_closures']) == len(coverage['rows']) == 33, 'All source rows')
    for actual, declared in zip(weights['source_contract_closures'], coverage['rows']):
        require(actual['id'] == declared['id'], 'Exact source row')
        route(actual['historical'], set(declared['historical_closure']))
        route(actual['replacement'], set(declared['new_closure']))
        route(actual['retained_and_qualification_context'],
              set(declared['retained_context_closure']) | set(declared['qualification_context_nodes']))
    for name, nodeset in graph['new_output_closures'].items():
        route(weights['new_application_closures'][name], set(nodeset))
    route(weights['full_record_closure'], set(graph['full_record_closure']))
    for name, nodeset in graph['additional_current_outputs'].items():
        route(weights['additional_current_outputs'][name], set(nodeset))
    require(weights['unchanged_complete_document_measurement'] ==
            read(study / 'topic_Affine_measurement_results/results.json'), 'Whole document ratios unchanged')
    acquisition = read(packet / 'acquisition.json')
    require([s['stage'] for s in acquisition['stages']] == ['U_Affine', 'CODE', 'AF1'],
            'Full library acquired before application')
    paid = set()
    for stage in acquisition['stages']:
        local = {n for n, owner in owners.items() if owner['document'] == stage['stage']}
        require(not paid.intersection(local), 'No repeated document charge')
        require(stage['complete_owner_ids'] == sorted(local) and stage['new_cost'] == total(local, costs),
                'Acquire complete local document, including context')
        paid.update(local)
        require(stage['cumulative_owner_ids'] == sorted(paid) and stage['cumulative_cost'] == total(paid, costs),
                'Cumulative complete library union')
    require(acquisition['historical_full_document_cost'] == total(
                [n for n, owner in owners.items() if owner['document'] == 'L012'], costs),
            'Whole historical comparison')
    require(acquisition['cross_topic_discount'] is False and acquisition['expanded_external_proof_cost'] is None
            and acquisition['graphics_cost'] is None, 'Acquisition cost boundary')
    return {'status': 'PASS_INDEPENDENT_ARITHMETIC_ONLY_SEMANTIC_REVIEW_PENDING',
            'author_manifest_sha256': PIN, 'documents': len(inputs), 'owners': len(costs),
            'owner_metric_cells': len(costs) * 30, 'all_variant_spans_checked': spans_checked,
            'routes_checked': routes_checked, 'document_metric_cells': len(inputs) * 30,
            'whole_raw_files_checked': raw_files_checked, 'raw_metric_cells': raw_files_checked * 10,
            'complete_acquisition_stages': len(acquisition['stages']),
            'interface_ownership_semantically_accepted': False, 'primary_text_exported': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'Fresh output required')
    result = check(args.study_root, args.packet)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
