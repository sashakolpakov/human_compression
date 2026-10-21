"""Compare whole printed arrays under every possible equal-index label join."""
from pathlib import Path
from itertools import permutations, product
import argparse
import json

TABLE1 = {'M12.2': 166, 'J2.2': 334, 'J3.2': 546,
          'HS.2': 339, 'McL.2': 443, 'He.2': 4074}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def join_one(source, calculated, order):
    indices = source['column_indices']
    actual_indices = [order // n for n in calculated['maximal_orders']]
    need(sorted(indices) == sorted(actual_indices), 'Same complete list of primitive degrees')
    blocks = []
    for degree in sorted(set(indices)):
        source_rows = [i for i, x in enumerate(indices) if x == degree]
        computed_rows = [i for i, x in enumerate(actual_indices) if x == degree]
        blocks.append((source_rows, list(permutations(computed_rows))))
    trials = []
    best = None
    winners = []
    matrix = calculated['full_suborbit_matrix']
    for choices in product(*(options for _, options in blocks)):
        mapping = [None] * len(indices)
        for (source_rows, _), computed_rows in zip(blocks, choices):
            for i, j in zip(source_rows, computed_rows):
                mapping[i] = j
        differences = []
        for i, row in enumerate(source['cells']):
            for j, cell in enumerate(row):
                actual = matrix[mapping[i]][mapping[j]]['lengths']
                if cell['lengths'] != actual:
                    differences.append(dict(source_row=i + 1, source_column=j + 1,
                                            printed=cell['printed'], printed_lengths=cell['lengths'],
                                            computed_lengths=actual))
        trial = dict(source_rows_to_computed_rows=[i + 1 for i in mapping], differences=differences)
        trials.append(dict(mapping=trial['source_rows_to_computed_rows'], changed_cells=len(differences)))
        if best is None or len(differences) < best:
            best = len(differences)
            winners = [trial]
        elif len(differences) == best:
            winners.append(trial)
    chosen = winners[0]
    mapping = [i - 1 for i in chosen['source_rows_to_computed_rows']]
    labels = [dict(source_row=i + 1, source_label=source['row_labels'][i], degree=indices[i],
                   Tom_class=calculated['maximal_classes'][j],
                   character_table_name=calculated['maximal_names_in_Tom_order'][j])
              for i, j in enumerate(mapping)]
    return dict(name=source['name'], physical_page=source['physical_page'],
                source_table_number=source['table_number'], cells=len(indices)**2,
                possible_equal_index_joins=len(trials), trials=trials,
                minimum_changed_cells=best, chosen_join=chosen,
                other_minimal_joins=winners[1:], source_labels_to_actual_classes=labels,
                exact_array_agreement=(best == 0),
                interpretation='All joins allowed by equal degrees are exhausted. A nonzero minimum is retained as a discrepancy, never normalized.',
                upper_triangle_without_singletons=calculated['upper_triangle_without_singletons'])


def compare(source, result, accepted_character):
    counts = {r['name']: r for r in result['counts']}
    prior = {r['name']: r for r in accepted_character['groups']}
    for name in ['M11', 'M23', 'J1']:
        need(counts[name]['unordered_pair_orbits'] == prior[name]['unordered_pair_orbits'],
             'Independent marks and accepted character totals agree')
    tables = {t['name']: t for t in result['suborbits']}
    joined = [join_one(t, tables[t['name']], counts[t['name']]['order']) for t in source['tables']]
    label_certificate = result['structural_label_certificates'][0]
    M23 = next(row for row in joined if row['name'] == 'M23')
    shapes = {r['Tom_class']: r['shape'] for r in label_certificate['shapes']}
    label_corrections = []
    printed_shapes = {2: 'L3(4):2', 3: '2^4:A7'}
    for row in M23['source_labels_to_actual_classes']:
        if row['source_row'] in printed_shapes:
            actual = shapes[row['Tom_class']]
            if actual != printed_shapes[row['source_row']]:
                label_corrections.append(dict(source_row=row['source_row'],
                                              printed=printed_shapes[row['source_row']], corrected=actual,
                                              Tom_class=row['Tom_class']))
    M23['row_label_corrections'] = label_corrections
    M23['structural_label_certificate'] = label_certificate
    M23['numerical_cells_changed'] = 0
    outer = [dict(group=name.removesuffix('.2'), acting_group=name,
                  printed=printed, computed=counts[name]['unordered_pair_orbits'],
                  agrees=printed == counts[name]['unordered_pair_orbits'])
             for name, printed in TABLE1.items()]
    return dict(status='L036_EXACT_SOURCE_TABLE_COMPARISON', source_pdf_sha256=source['source_pdf_sha256'],
                Table1_outer_counts=outer, suborbit_tables=joined,
                numerical_arrays_agree=all(t['exact_array_agreement'] for t in joined),
                M23_printed_labels_corrected=bool(label_corrections),
                independent_existing_character_agreement=['M11', 'M23', 'J1'],
                existing_M22_full_automorphism_total=81,
                M22_total_attribution='Previously accepted L073 import; the new M22 mark calculation uses only inner automorphisms.',
                whole_source_accepted=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--arithmetic', type=Path, required=True)
    parser.add_argument('--accepted-character', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(args.out.is_absolute() and not args.out.exists(), 'Fresh absolute comparison')
    result = compare(json.loads(args.source.read_text()), json.loads(args.arithmetic.read_text()),
                     json.loads(args.accepted_character.read_text()))
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status=result['status'], outer=result['Table1_outer_counts'],
                         changed_cells={r['name']: r['minimum_changed_cells'] for r in result['suborbit_tables']})))
