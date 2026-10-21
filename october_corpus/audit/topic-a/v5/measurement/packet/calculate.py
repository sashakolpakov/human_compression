#!/usr/bin/env python3
"""Exact arithmetic on accepted complete manuscripts; no text extraction."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import csv
import hashlib
import io
import json

R = Path(__file__).resolve().parent

def load(path):
    return json.loads(path.read_text())

def need(ok, message):
    if not ok:
        raise ValueError('A10_NUMERIC_REJECT: ' + message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def key(variant, normalization, unit):
    return '/'.join((variant, normalization, unit))

def fraction(source, replacement):
    f = Fraction(source, replacement)
    with localcontext() as context:
        context.prec = 50
        decimal = format(Decimal(source) / Decimal(replacement), '.12f')
    return dict(source_cost=source, replacement_cost=replacement,
                numerator=f.numerator, denominator=f.denominator, decimal=decimal)

def derive(protocol, counts, inventory, prior):
    order = protocol['source_order']
    apps = protocol['applications']
    bundles = protocol['application_documents']
    common = protocol['common_documents']
    need(len(order) == 10 and len(set(order)) == 10, 'ten distinct originals')
    need(set(counts['raw_files_measured']) == {r['id'] for r in inventory['contents']},
         'all whole contents')
    raw = []
    for rule in inventory['contents']:
        item = counts['raw_files_measured'][rule['id']]
        for field in ['sha256', 'bytes', 'occurrence_ids', 'roles', 'coarse_roles',
                      'accounting_class', 'mathematical_premise', 'inherited_A9_raw_id']:
            need(item[field] == rule[field], 'exact raw content and explicit role: ' + field)
        raw.append(dict(id=rule['id'], **item))
    groups = {}
    for group, expected in protocol['raw_classes'].items():
        rows = [r for r in raw if r['accounting_class'] == group]
        need(len(rows) == expected, 'disjoint whole-content class ' + group)
        groups[group] = dict(files=len(rows), literal_bytes=sum(r['bytes'] for r in rows),
                            metrics={n: {u: sum(r['metrics'][n][u] for r in rows)
                                         for u in protocol['units']}
                                     for n in protocol['normalizations']})
    need(sum(g['files'] for g in groups.values()) == len(raw) == 203, 'exhaustive disjoint roles')
    need([r['id'] for r in raw if r['mathematical_premise']] == protocol['required_contents'],
         'all99 required whole contents remain prerequisites')
    coordinates = {}
    for variant in protocol['variants']:
        for normalization in protocol['normalizations']:
            for unit in protocol['units']:
                coordinate = key(variant, normalization, unit)
                d = {name: doc['metrics'][variant][normalization][unit]
                     for name, doc in counts['documents'].items()}
                application_costs = {app: sum(d[name] for name in parts)
                                     for app, parts in bundles.items()}
                source_sum = sum(d[source] for source in order)
                whole_common = sum(d[name] for name in common)
                local = sum(application_costs[apps[source]] for source in order)
                conditionals = {source: fraction(d[source], application_costs[apps[source]])
                                for source in order}
                old = prior['coordinates'][coordinate]
                for source in protocol['unchanged_conditionals']:
                    need(conditionals[source] == old['conditional'][source],
                         'unchanged previous eight conditional fractions')
                for name, value in old['document_costs'].items():
                    if name != 'A9':
                        need(d[name] == value, 'unchanged previous21 complete document counts')
                coordinates[coordinate] = dict(
                    variant=variant, normalization=normalization, unit=unit,
                    document_costs=d, common_costs={name: d[name] for name in common},
                    application_costs=application_costs, source_sum=source_sum,
                    whole_common=whole_common, application_sum=local,
                    whole_written=whole_common + local,
                    written=fraction(source_sum, whole_common + local), conditional=conditionals,
                    prior_whole_written=old['written'],
                    prior_L121_conditional=old['conditional']['L121'],
                    change=dict(extra_source=d['L003'], extra_common=whole_common-old['whole_common'],
                                previous_L121_application=old['document_costs']['A9'],
                                current_L121_application=application_costs['A9'],
                                L003_application=application_costs['A10']),
                    separate_software=dict(
                        old_partial_printed_appendices={name: d[name] for name in
                                                       ['CODE_A', 'CODE_AFFINE', 'CODE_DIAGRAM']},
                        complete_enlarged_printed_cost=None,
                        raw_group_costs={g: r['metrics'][normalization][unit] for g, r in groups.items()},
                        software_inclusive_factor=None, historical_source_software_cost=None))
    primary_key = key(*(protocol['primary'][k] for k in ['variant', 'normalization', 'unit']))
    primary = coordinates[primary_key]
    stages = [dict(stage=0, acquired='All three common manuscripts', source_written=0,
                   replacement_written=primary['whole_common'],
                   required_program_data_and_external_premises_separate=True)]
    sources = 0
    replacement = primary['whole_common']
    for i, source in enumerate(order, 1):
        sources += primary['document_costs'][source]
        replacement += primary['application_costs'][apps[source]]
        stages.append(dict(stage=i, acquired=apps[source] + ' for ' + source,
                           source_written=sources, replacement_written=replacement,
                           required_program_data_and_external_premises_separate=True))
    return dict(
        status='AUTHOR_TEN_ORIGINAL_NUMERICAL_COMPARISON_PENDING_DISTINCT_REVIEW',
        title=protocol['title'], source_ids=order, source_count=10,
        applications=apps, application_documents=bundles, common_documents=common,
        source_pages=sum(counts['documents'][x]['pages'] for x in order),
        whole_common_pages=sum(counts['documents'][x]['pages'] for x in common),
        application_pages={a: sum(counts['documents'][x]['pages'] for x in parts)
                           for a, parts in bundles.items()},
        old_partial_printed_appendix_pages={x: counts['documents'][x]['pages'] for x in
                                           ['CODE_A', 'CODE_AFFINE', 'CODE_DIAGRAM']},
        primary_coordinate=primary_key, coordinate_count=30, exact_fraction_count=330,
        inherited_conditional_fractions_preserved=240, coordinates=coordinates, primary=primary,
        whole_file_inventory=raw, whole_file_group_costs=groups,
        primary_acquisition=stages,
        complete_enlarged_printed_program_representation=None,
        software_inclusive_factors=None, optional_validation_inclusive_factors=None,
        historical_source_software_cost=None, full_formalization_cost=None,
        unknown_costs=protocol['unknown_costs'], cross_topic_discount=False,
        new_source_credit=0, new_question_credit=0, new_formal_credit=0,
        no_extraction=True, no_scientific_or_formal_replay=True)

def csvtext(fields, rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()

def outputs(result):
    fractions, documents, raw = [], [], []
    for coordinate, c in result['coordinates'].items():
        fractions.append(dict(coordinate=coordinate, comparison='written', **c['written']))
        fractions.extend(dict(coordinate=coordinate, comparison=x, **f)
                         for x, f in c['conditional'].items())
        documents.extend(dict(coordinate=coordinate, document=x, cost=value)
                         for x, value in c['document_costs'].items())
    for item in result['whole_file_inventory']:
        for normalization, metrics in item['metrics'].items():
            for unit, value in metrics.items():
                if unit != 'collapsed_text_sha256':
                    raw.append(dict(id=item['id'], accounting_class=item['accounting_class'],
                                    bytes=item['bytes'], sha256=item['sha256'],
                                    normalization=normalization, unit=unit, cost=value))
    return {
        'results.json': json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        'fractions.csv': csvtext(['coordinate', 'comparison', 'source_cost', 'replacement_cost',
                                 'numerator', 'denominator', 'decimal'], fractions),
        'document_costs.csv': csvtext(['coordinate', 'document', 'cost'], documents),
        'whole_files.csv': csvtext(['id', 'accounting_class', 'bytes', 'sha256', 'normalization',
                                   'unit', 'cost'], raw),
        'acquisition.csv': csvtext(list(result['primary_acquisition'][0]), result['primary_acquisition'])}

if __name__ == '__main__':
    result = derive(load(R/'protocol.json'), load(R/'inputs/input/author_counts.json'),
                    load(R/'inputs/input/precount/raw_inventory.json'), load(R/'prior/results.json'))
    for name, content in outputs(result).items():
        (R/name).write_text(content)
    print(json.dumps(dict(primary=result['primary']['written'],
                          common=result['primary']['whole_common'],
                          applications=result['primary']['application_sum'],
                          conditionals=result['primary']['conditional'])))
