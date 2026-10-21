#!/usr/bin/env python3
"""Verify the frozen proof and completed independent review evidence bindings."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MANIFEST='50b12774841fdc68d27edefd748c4bd81a8417f55bb90fe7437c41a2ab943491'
ERRATUM='9d49979b49443615dde8acd6e6f562642e31e23f6f810f66619b24984edbb4b2'

def require(ok,message):
    if not ok:raise ValueError(message)

def binding(path):
    raw=path.read_bytes()
    return dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    require(not a.report.exists() and not a.report.is_symlink(),'Fresh report required')
    manifest_name='phase83_nonabelian_cover_manifest.json'
    require(binding(ROOT/manifest_name)['sha256']==MANIFEST,'Author manifest changed')
    manifest=json.loads((ROOT/manifest_name).read_text())
    entries={**manifest['files'],**manifest['retained_inputs']}
    require(len(entries)==19,'Expected 19 author input bindings')
    for name,expected in entries.items():
        require(binding(ROOT/name)==expected,'Bound source changed: '+name)
    erratum='phase83_nonabelian_cover_erratum.md'
    require(binding(ROOT/erratum)['sha256']==ERRATUM,'Required erratum changed')
    evidence=['phase86_nonabelian_cover_trace_check.py','phase86_nonabelian_cover_trace_check.json',
              'phase86_nonabelian_cover_cells_check.py','phase86_nonabelian_cover_cells_check.json',
              'phase86_nonabelian_cover_controls.py','phase86_nonabelian_cover_controls.json',
              'phase86_nonabelian_cover_replay.json','phase86_nonabelian_cover_lean.log',
              'phase86_nonabelian_cover_recent_audit.md']
    def report(name):return json.loads((ROOT/name).read_text())
    trace=report(evidence[1]);cells=report(evidence[3]);controls=report(evidence[5]);replay=report(evidence[6])
    require(trace['status']=='PASS_exact_original_relator_implication','Trace did not pass')
    require(cells['status']=='PASS_35_cell_original_relation_implication','Cell check did not pass')
    for script,row in [(evidence[0],trace),(evidence[2],cells),(evidence[4],controls)]:
        require(row['checker_sha256']==binding(ROOT/script)['sha256'],'Checker/report binding mismatch')
    require(trace['certificate_sha256']==entries['phase83_word_elimination.json']['sha256'],'Trace certificate mismatch')
    require(trace['model_sha256']==entries['phase66_coprime_cover_permutation_model.json']['sha256'],'Trace model mismatch')
    for key,name in [('model','phase66_coprime_cover_permutation_model.json'),
                     ('certificate','phase83_word_elimination.json'),('lean','formal/OddKernelWord.lean')]:
        require(cells['input_sha256'][key]==entries[name]['sha256'],'Selected-cell binding mismatch')
    require((trace['original_relators'],trace['eliminations'],trace['remaining_nontrivial_relators'])==(1024,111,512),'Trace counts')
    require((cells['cell_count'],cells['eliminations'])==(35,34),'Cell counts')
    require(cells['marked_defect_after_eliminations']==trace['marked_defect']==[-6,7],'Defect mismatch')
    require(cells['final_relator']==[-32,16,-6,7,-6,7,-16,32],'Selected final row')
    require(replay['status']=='PASS' and replay['regenerated_trace_identical'] and replay['regenerated_lean_identical'],'Fresh runner did not pass')
    for name,sha in replay['input_sha256'].items():require(entries[name]['sha256']==sha,'Replay input mismatch')
    require(replay['runner_sha256']==entries['phase83_nonabelian_cover_check.py']['sha256'],'Runner changed')
    log=binding(ROOT/evidence[7])
    require(log['sha256']==replay['build_log_sha256']==entries['phase83_nonabelian_cover_lean.log']['sha256'],'Axiom log differs')
    require(replay['axiom_reports']=={'defect_square':['Quot.sound','propext'],
            'defect_trivial_of_odd_card':['Classical.choice','Quot.sound','propext']},'Unexpected formal axioms')
    require(controls['status']=='PASS' and len(controls['mutation_controls'])==11 and
            len(controls['no_clobber_controls'])==3 and len(controls['preserved_successful_output_files'])==7,'Controls incomplete')
    require(controls['preserved_successful_output_files']['report.json']==binding(ROOT/evidence[6])['sha256'],'Control/replay binding mismatch')
    require(all(r['report_absent'] and r['returncode']!=0 for r in controls['mutation_controls']),'Mutation not rejected')
    all_bindings={**entries,manifest_name:binding(ROOT/manifest_name),erratum:binding(ROOT/erratum),
                  **{name:binding(ROOT/name) for name in evidence}}
    result=dict(status='PASS',date='2026-10-10',proof_requires_erratum=True,
                original_author_input_bindings=19,total_bound_files=len(all_bindings),
                bound_files=all_bindings,checker_sha256=binding(Path(__file__))['sha256'],
                scope='Frozen source and evidence binding recheck, not a second execution of Lean or a replacement for the written proof review.')
    with a.report.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','original_author_input_bindings','total_bound_files']}))

if __name__=='__main__':main()
