"""Reject altered mark evidence and detect altered printed cells."""
import sys
sys.dont_write_bytecode = True
import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def run(data, source, result):
    a = module('arithmetic')
    j = module('join')
    cases = [('zero_identity_mark', 0, lambda r: r[5][0].__setitem__(0, 0)),
             ('missing_full_row_mark', 0, lambda r: r[5][-1].pop()),
             ('fusion_outside_table', 0, lambda r: r[9].__setitem__(0, len(r[3]) + 1)),
             ('wrong_element_order', 0, lambda r: r[8].__setitem__(0, 2)),
             ('square_outside_classes', 0, lambda r: r[7].__setitem__(0, len(r[6]) + 1)),
             ('maximal_bijection_duplicate', 7, lambda r: r[11].__setitem__(0, r[11][1]))]
    rejected = []
    for name, position, mutate in cases:
        row = copy.deepcopy(data[position])
        mutate(row)
        try:
            a.MarkData(row)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Accepted damaged certificate: ' + name)
    row = copy.deepcopy(next(r for r in data if r[0] == 'M23'))
    cert = result['structural_label_certificates'][0]['witness']
    m, l = cert['maximal_class'] - 1, cert['normal_class'] - 1
    at = row[4][m].index(l + 1)
    row[5][m][at] *= 2
    try:
        a.MarkData(row).M23_label_certificate()
    except ValueError:
        rejected.append('nonunique_normal_subgroup')
    else:
        raise ValueError('Accepted missing normal-subgroup certificate')
    bad = copy.deepcopy(source['tables'][0])
    bad['cells'][0][0]['lengths'][0][0] += 1
    calculated = next(r for r in result['suborbits'] if r['name'] == 'M11')
    changed = j.join_one(bad, calculated, 7920)
    a.need(changed['minimum_changed_cells'] == 1 and not changed['exact_array_agreement'],
           'A changed source cell must remain a reported discrepancy')
    return dict(rejected_mathematical_damages=rejected,
                detected_printed_cell_damage=True, printed_cell_automatically_repaired=False)


if __name__ == '__main__':
    a = module('arithmetic')
    data, intervals = a.parse((HERE.parent / 'table_execution01/stdout').read_bytes())
    source = json.loads((HERE / 'printed01/tables.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    print(json.dumps(run(data, source, result)))
