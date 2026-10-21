"""Independent fixed-source inventory; no group enumeration or proof claim."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode = True
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def norm(text):
    return ' '.join(text.split())


def inventory(tex, source, legacy, register):
    problems = list(re.finditer(r'\\begin\{prob\}(.*?)\\end\{prob\}', tex, re.S))
    need(len(problems) == len(source['numbered_problems']) == 34, 'Exactly34 source problem blocks')
    positions = []
    for number, (match, row, joined) in enumerate(zip(problems, source['numbered_problems'], register['questions']), 1):
        label = re.findall(r'\\label\{([^}]+)\}', match.group(1))
        line = tex[:match.start()].count('\n') + 1
        need((number, line, label) == (row['number'], row['tex_line'], [row['tex_label']]),
             'Exact ordinal/line/label source position')
        need(all(joined[k] == value for k, value in row.items()), 'Question join preserves all source fields')
        positions.append(dict(number=number, line=line, label=label[0]))
    bibliography = dict((m.group(1), norm(m.group(2))) for m in re.finditer(
        r'\\bibitem\{([^}]+)\}\s*(.*?)(?=\\bibitem|\\end\{thebibliography\})', tex, re.S))
    need(len(bibliography) == 66, 'Exactly66 literal source bibliography entries')
    expected = {k: norm(v) for k, v in source['source_bibliography'].items()}
    need(bibliography == expected == {k: norm(v) for k, v in register['source_bibliography'].items()},
         'Every bibliography key and complete entry matches')
    need(len(legacy['rows']) == 51, 'Unchanged historical51row register')
    for old, row in zip(legacy['rows'], register['established_clauses']):
        need(norm(old['source_anchor']) in norm(tex), 'Actual retained source anchor')
        need(all(key in bibliography for key in old['source_citation_keys']), 'Actual source citation keys')
        need(all(row[k] == v for k,v in old.items() if k != 'disposition'), 'Exact legacy clause fields')
        need(row['source_register_disposition'] == old['disposition'], 'Historical disposition retained')
    secondary = source['embedded_questions_and_conjectures']
    need(len(secondary) == len(register['secondary_records']) == 14, 'Fourteen exact secondary records')
    need(all(all(new[k] == v for k,v in old.items()) for old,new in zip(secondary,register['secondary_records'])),
         'All secondary scope/parent/kind fields retained')
    count = len(register['established_clauses'])
    need(count in (51,52), 'Reviewed edition clause count')
    if count == 52:
        row = register['established_clauses'][-1]
        need(row['id'] == 'R52' and row['context'] == 'C07', 'Additional locally-projective clause')
        need(norm(row['source_anchor']) in norm(tex), 'R52 literal source anchor')
        need(row['independently_inspected_primary_classification'] is False, 'R52 retains uninspected classification boundary')
    need(register['source_only_aggregates'] == [17,441] and register['corrected_family_count'] == 137
         and register['corrected_global_total'] is None, 'Family and global totals stay separate')
    need(not register['all_classifications_reproved'] and not register['source_questions_asserted_currently_open'],
         'No complete classification/current status assertion')
    return dict(numbered_problems=positions, bibliography_entries=len(bibliography),
                retained_source_anchors=51, preserved_legacy_rows=51, synthesis_clauses=count,
                secondary_records=14)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'Fresh output file')
    study = args.study.resolve()
    work = study/'reboot_20261013'
    files = [work/'N010_work/SchulteWeiss.tex',work/'N010_work/source_contract02.json',
             work/'N010_retained_inputs/register01/retained_register.json',args.packet/'claim_register.json']
    tex = files[0].read_text()
    source,legacy,register = [json.loads(p.read_text()) for p in files[1:]]
    result = inventory(tex,source,legacy,register)
    damages = []
    for name in ['ordinal','line','duplicate_label','bibliography_content','citation','source_anchor','secondary_scope',
                 'old_disposition','global_subtraction','current_status']:
        ss,ll,rr = copy.deepcopy((source,legacy,register))
        if name == 'ordinal': ss['numbered_problems'][0]['number'] = 2
        elif name == 'line': ss['numbered_problems'][0]['tex_line'] += 1
        elif name == 'duplicate_label': ss['numbered_problems'][0]['tex_label'] = 'reguni'
        elif name == 'bibliography_content': ss['source_bibliography']['arri'] += ' invented'
        elif name == 'citation': ll['rows'][0]['source_citation_keys'].append('absent_key')
        elif name == 'source_anchor': ll['rows'][0]['source_anchor'] = 'absent literal source anchor'
        elif name == 'secondary_scope': rr['secondary_records'][0]['scope'] += ' solved'
        elif name == 'old_disposition': rr['established_clauses'][0]['source_register_disposition'] = 'REPROVED'
        elif name == 'global_subtraction': rr['corrected_global_total'] = 441-145+137
        else: rr['source_questions_asserted_currently_open'] = True
        try:
            inventory(tex,ss,ll,rr)
        except (ValueError,KeyError):
            damages.append(name)
        else:
            raise ValueError('Missed damaged source inventory: '+name)
    pins = [dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
    report = dict(status='PASS_INDEPENDENT_N010_SOURCE_INVENTORY',counts=result,damaged_controls=damages,
                  inputs=pins,mathematical_proof_verified_by_program=False,new_census=False)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],source_problems=34,bibliography=66,
                         legacy_anchors=51,clauses=result['synthesis_clauses'],damage_controls=len(damages))))


if __name__ == '__main__':
    main()
