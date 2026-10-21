#!/usr/bin/env python3
"""Replay exact review bindings and finite interfaces, not the prose review."""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from local_cases import run as local_cases

HERE = Path(__file__).resolve().parent
AUTHOR = '087fc503dd4d3f11df74cf751f251c3b585dd9f1ec9aefbb94a8dc3af4124e63'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text())


def bound(root, row):
    rel = Path(row['path'])
    need(not rel.is_absolute() and '..' not in rel.parts, 'invalid bound path')
    p = root / rel
    need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'binding: ' + str(p))


def semantic(scope, formal, inventory, questions, report):
    need(scope['counts'] == {'L008':9, 'N016':18, 'proof_spans':22}, 'scope counts')
    need(len(scope['rows']) == 27 and len({x['id'] for x in scope['rows']}) == 27, 'row completeness')
    rows = {x['id']: x for x in scope['rows']}
    need(rows['H02']['status'] == 'qualified_infinite_formulation', 'infinite qualification')
    need(rows['H09']['status'] == 'excluded_ancillary_implementation', 'software exclusion')
    need(rows['R07']['status'] == 'recovered_with_identity_wording_correction', 'identity correction')
    need(all(rows[x]['status'] == 'separate_question_not_principal_credit' for x in ['R17','R18']), 'question scope')
    need(scope['new_question_credit'] == 0 and scope['compression_factor'] is None, 'no new count or factor')
    need(formal['total_axiom_reports'] == 14 and formal['new_axiom_reports'] == 7 and formal['end_to_end_application_formalized'] is False, 'formal scope')
    need([x['reports'] for x in formal['modules']] == [4,3,7], 'module report map')
    need(inventory['required_mathematical_files'] == 1 and inventory['diagnostic_files'] == 1 and inventory['archival_drivers'] == 2 and inventory['current_drivers'] == 1, 'program roles')
    required = [r['path'] for r in inventory['programs'] if r['required_mathematical_premise']]
    need(required == ['programs/chiral_cover.g'], 'required program boundary')
    need(inventory['historical_code_cost'] is None, 'historical code unknown')
    need(all(q['proof_premise_here'] is False for q in questions['questions']), 'separate question premise')
    need(next(q for q in questions['questions'] if q['id']=='allrankfinite')['accepted_record'] is None, 'all-rank finite open')
    need(report['status'] == 'PASS' and report['total_formal_reports'] == 14, 'fresh formal completion')
    need(len(report['formal']) == 3 and sum(x['reports'] for x in report['formal']) == 14, 'fresh module completion')
    need(len(report['controls']) == 5 and all(x['status']=='REJECTED' for x in report['controls']), 'fresh controls')
    need([(x['stem'],x['pages'],x['same_per_page_text']) for x in report['renders']] == [('umbrella',6,True),('testing-chirality',3,True),('minimal-regular-covers',6,True),('programs',3,True)], 'four complete PDFs')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh report path required')
    a=args.study_root/'topic_Chamber_volume'
    need(sha(a/'manifest.json') == AUTHOR, 'author freeze')
    man=load(a/'manifest.json')
    for row in man['exports']: bound(a,row)
    b=load(HERE/'bindings.json')
    for row in b['study_bindings']+[b['author_manifest'],b['root_preliminary_reading']]: bound(args.study_root,row)
    for row in b['public_question_bindings']: bound(args.public_root,row)
    if (HERE/'manifest.json').exists():
        for row in load(HERE/'manifest.json')['exports']:bound(HERE,row)
    scope=load(a/'scope.json');formal=load(a/'formal/scope.json');inventory=load(a/'program_inventory.json');questions=load(a/'question_map.json');report=load(HERE/'fresh_replay/report.json')
    semantic(scope,formal,inventory,questions,report)
    coverage=load(HERE/'coverage_review.json')
    need([{k:v for k,v in row.items() if k not in ['review_status','independent_note']} for row in coverage['rows']] == scope['rows'], 'exact source-row interface')
    proof=load(HERE/'proof_reading.json')
    need(set(proof['spans']) == set(scope['proof_spans']), 'all proof spans read')
    for key,row in scope['proof_spans'].items():
        text=(a/row['path']).read_text();start=text.index(row['start_anchor']);end=text.index(row['end_anchor'],start+len(row['start_anchor'])) if row['end_anchor'] else len(text)
        data=text[start:end].encode()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], 'proof span '+key)
        need(proof['spans'][key]['binding']==row, 'review span binding')
    for row in report['programs']+report['controls']+report['formal']:
        need(sha(HERE/'fresh_replay'/(row['label']+'.log'))==row['log_sha256'], 'fresh log '+row['label'])
    gap=(HERE/'fresh_replay/finite_cover.log').read_text()
    need(len(re.findall(r'^ROW ',gap,re.M))==6 and 'PASS GAP 4.15.1' in gap, 'six exact GAP outputs')
    for row in formal['modules']:
        text=(HERE/'fresh_replay'/(Path(row['path']).stem+'.log')).read_text()
        found=re.findall(r'depends on axioms:\s*\[([^]]*)\]',text)
        need(len(found)==row['reports'] and all(set(x.strip() for x in s.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'} for s in found), 'actual axiom reports')
        need('warning:' not in text and 'sorryAx' not in text, 'Lean diagnostics')
    current=local_cases();need(current==load(HERE/'local_cases.json'), 'independent local replay')
    controls=[]
    cases=[('infinite cardinality qualification',0,lambda x:x['rows'][1].update(status='recovered')),
           ('ancillary source software scope',0,lambda x:x['rows'][8].update(status='recovered')),
           ('identity-power correction',0,lambda x:x['rows'][15].update(status='recovered')),
           ('new question credit',0,lambda x:x.update(new_question_credit=1)),
           ('end-to-end formal inflation',1,lambda x:x.update(end_to_end_application_formalized=True)),
           ('missing old Lean module reports',1,lambda x:x['modules'][0].update(reports=0)),
           ('diagnostic promoted to premise',2,lambda x:x['programs'][1].update(required_mathematical_premise=True)),
           ('unknown old code converted to zero',2,lambda x:x.update(historical_code_cost=0)),
           ('later question used as premise',3,lambda x:x['questions'][0].update(proof_premise_here=True)),
           ('dropped current PDF',4,lambda x:x['renders'].pop()),
           ('accepted bad Lean mutation',4,lambda x:x['controls'][2].update(status='PASS'))]
    for label,i,f in cases:
        data=copy.deepcopy([scope,formal,inventory,questions,report]);f(data[i])
        try:semantic(*data)
        except RuntimeError:controls.append({'label':label,'status':'REJECTED'})
        else:raise RuntimeError('control accepted '+label)
    output={'status':'PASS','author_manifest_sha256':AUTHOR,'author_exports':len(man['exports']),'source_rows':27,'proof_spans':22,'fresh_formal_reports':14,'new_formal_reports':7,'full_required_programs':1,'validation_programs':1,'independent_models':current,'scope_controls':controls,'limits':'Exact evidence and scope replay plus bounded interface checks; written proof review is recorded separately. No new source/question credit or ratio.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'status':'PASS','exports':len(man['exports']),'scope_controls':len(controls),'rows':27,'spans':22}))


if __name__=='__main__':main()
