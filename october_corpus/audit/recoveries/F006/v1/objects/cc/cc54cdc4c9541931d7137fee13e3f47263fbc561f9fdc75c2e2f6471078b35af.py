"""Check the retained evidence of the corrected whole F006 recovery.

This checks exact executions and their recorded proofs; it does not rerun
discovery, replace mathematical review, or claim kernel formalization.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

HISTORICAL = Path('/Users/sasha/medusa/research/leemans')
PATTERN = (r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)'
           r'\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def verify(packet, study, allow_absent_primary=False):
    packet, study = Path(packet).resolve(), Path(study).resolve()
    def locate(name):
        p = Path(name)
        if p.is_absolute():
            need(p.is_relative_to(HISTORICAL), 'Unknown absolute evidence namespace')
            p = p.relative_to(HISTORICAL)
        need('..' not in p.parts, 'Parent traversal')
        result = study/p
        need(result.resolve().is_relative_to(study), 'Evidence escapes study root')
        return result
    def binding(row, parent=None):
        p = (parent/row['path']) if parent is not None else locate(row['path'])
        b = p.read_bytes()
        need(hashlib.sha256(b).hexdigest()==row['sha256'] and
             ('bytes' not in row or len(b)==row['bytes']), 'Changed binding: '+str(p))
    for row in read(packet/'manifest.json')['exports']:
        binding(row, packet)
    deps = read(packet/'dependencies.json')
    skipped = []
    for row in deps['bindings']:
        p = locate(row['path'])
        if not p.exists() and allow_absent_primary and row['path'] in deps['primary_files_hash_only']:
            skipped.append(row['path'])
        else:
            binding(row)
    scope = read(packet/'scope.json')
    need(scope['source_ids']==['F006'] and scope['principal_results']==['Theorem1','Theorem2','Theorem3','Table1'],
         'Exact whole-source contract')
    need(scope['corrected_literal_cases']==['I2(m), m=2 modulo4','H3','E7'], 'Exact corrections')
    need(scope['proposed_principal_recovery_credit']==1 and scope['whole_original_credit']==0,
         'Author proposal is not a publication admission')
    need(all(scope[k]==0 for k in ['new_question_credit','new_Lean_credit','new_measurements']),
         'Unearned new credit')
    need(scope['compression_factor'] is None and scope['software_factor'] is None,
         'No measurement in intake')
    execution = read(packet/'executions.json')
    all_rows = {}
    for entry in execution['enumerations']:
        run = locate(entry['run']);receipt = read(run/'report.json')
        need(receipt['status']=='EXITED' and receipt['returncode']==0 and
             receipt['complete_marker'] and receipt['unchanged'], 'Complete census required')
        need(not (run/'stderr.log').read_bytes(), 'Census stderr')
        for row in receipt['pins']:
            p = Path(row['path'])
            binding(dict(row,path=str(Path(entry['input_root'])/p)) if not p.is_absolute() else row)
        raw = (run/'stdout.log').read_text()
        need(raw.count('COMPLETE_EXHAUSTION')==1, 'Unique exhaustion record')
        rows = [list(map(int,x)) for x in re.findall(PATTERN,raw)]
        need([r[0] for r in rows]==list(range(1,entry['rank_limit']+1)), 'Every rank required')
        need(all(2*r[3]==r[1]+r[2] and 2*r[6]==r[4]+r[5] for r in rows), 'Reversal arithmetic')
        need(all(0<=r[2]<=r[1] and 0<=r[5]<=r[4]<=r[1] for r in rows), 'Count containment')
        marker = 'COMPLETE_TUPLES_RANK_' if entry['name']=='E8' else 'COMPLETE_MARKS_RANK_'
        need(list(map(int,re.findall(marker+r'(\d+) ',raw)))==[r[0] for r in rows],
             'Literal tuple record at every rank')
        all_rows[entry['name']] = rows
    need(set(all_rows)=={'F4','H4','E6','E7','E8'}, 'All five exceptional censuses')
    warning = execution['separate_warning_assessment']
    binding(warning)
    need(read(locate(warning['path'])).get('accepted') is True, 'Distinct exact-warning assessment')
    warning_text = ('Syntax warning: Unbound global variable in validate.g:28\n'
                    '  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);\n'
                    '                                 ^\n'
                    'Syntax warning: Unbound global variable in validate.g:28\n'
                    '  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);\n'
                    '                                      ^\n')
    validations = []
    for name in execution['positive_validation_receipts']:
        p = locate(name);d = read(p);run=p.parent
        need(d['returncode']==0 and d['complete_marker'] and d['unchanged'], 'Terminal positive validation')
        for row in d['pins']:
            binding(row)
        raw=(run/'stdout.log').read_text();stderr=(run/'stderr.log').read_text()
        if run.name in ['F4','H4','E7']:
            model=run.name
            need(d['status']=='FAILED_NO_CERTIFICATE' and stderr==warning_text,
                 'Only the separately reviewed exact warning stream is allowed')
            need(raw.count('COMPLETE_EXCEPTIONAL_ROW_VALIDATION')==1, 'Complete row validation')
            rows=[(int(rank),list(map(int,body.split(',')))) for rank,body in
                  re.findall(r'VERIFIED_RANK\s+(\d+)\s+\[\s*([\d,\s]+)\]',raw)]
            need([[rank]+values for rank,values in rows]==all_rows[model], 'Every rank revalidated')
        else:
            model='E8'
            need(d['status']=='EXITED' and not stderr and d['all_subset_intersections_checked'],
                 'Clean complete E8 validation')
            need(raw.count('COMPLETE_REMAINING_MODEL_VALIDATION')==1, 'Complete E8 positive validation')
            need(list(map(int,re.findall(r'VERIFIED_TYPE_COUNTS (\d+) ',raw)))==list(range(1,30)),
                 'E8 checks at all ranks')
        need(d['recorded_tuples']==sum(r[1] for r in all_rows[model]), 'Every tuple checked')
        validations.append(dict(model=model,tuples=d['recorded_tuples'],known_warnings=bool(stderr)))
    need({r['model'] for r in validations}=={'F4','H4','E7','E8'}, 'All four new positive validations')
    e6=locate(execution['E6_full_IP']);d=read(e6)
    need(d['status']=='EXITED' and d['returncode']==0 and d['complete_marker'] and d['unchanged'],
         'Acquired E6 validation')
    for row in d['pins']:binding(row)
    raw=(e6.parent/'stdout.log').read_text()
    need('COMPLETE_LITERAL_ORBIT_BIJECTION_AND_FULL_IP 276' in raw, 'All276 E6 markings transported')
    need([(int(a),int(b)) for a,b in re.findall(r'RANK_ORBIT_BIJECTION (\d+) (\d+)',raw)]==
         [(r[0],r[1]) for r in all_rows['E6']], 'Every E6 rank covered')
    source=read(locate(execution['source_table']))
    need(source['status']=='ALL_SIX_CONNECTED_SOURCE_ROWS_MATCH' and source['printed_cells']==42,
         'Complete printed table comparison')
    need(source['complete_enumeration_rows']==all_rows and source['source']==source['computed_connected'],
         'Comparison uses these exact censuses')
    need(set(source['literal_definition_discrepancies'])=={'H3','E7'}, 'Disconnected distinctions retained')
    model=read(locate(execution['model_identifications']))
    need(model['status']=='PASS' and model['returncode']==0 and model['complete_marker'] and model['unchanged'],
         'Complete literal Coxeter model identifications')
    for row in model['pins']:binding(row)
    return dict(status='PASS_COMPLETE_F006_RETAINED_EVIDENCE',dependencies=len(deps['bindings']),
        primary_files_not_read=skipped,exceptional_ordered_tuples=sum(sum(r[1] for r in rows) for rows in all_rows.values()),
        new_positive_validations=validations,reused_E6_full_IP=276,printed_cells=42,
        source_ids=['F006'],whole_original_credit=0,distinct_whole_source_review_required=True,
        no_new_enumeration=True,no_whole_source_Lean_claim=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True)
    p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--allow-absent-primary',action='store_true')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    report=verify(a.packet,a.study,a.allow_absent_primary)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
