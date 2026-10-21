#!/usr/bin/env python3
"""Bounded review replay; --programs additionally reruns the actual finite certificates."""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, json, shutil, subprocess, sys
from data_audit import audit, need

ROOT = Path(__file__).resolve().parent
AUTHOR = 'dc458cf7d9d693d57daf106a0cd2f2abb6f64f75123836d9cf8da41fcbc02df4'
STATUS = '938b7d519849b4290180b4d8972113fe56cca56d1eaaf387d09fcadad4279cc2'
PRIMARY = 'a0c307e0a41eeb8b190de4cb0b4af331973866993c55ee4f0fcb66b932c6db61'
MARKER = 'INDEPENDENT_LITERAL_COSETS PASS 98properIP 6all-flag-families 30full-subset-identities'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def bound_files(root, pin=None):
    mf = root/'manifest.json'
    if pin is not None: need(sha(mf) == pin, 'manifest pin mismatch')
    rows = load(mf)['exports']; seen = set()
    for row in rows:
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen, 'unsafe export path')
        seen.add(str(rel)); p = root/rel
        need(not any((root/Path(*rel.parts[:i])).is_symlink() for i in range(1,len(rel.parts)+1)), 'export symlink')
        need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'export mismatch: '+str(rel))
    return len(rows)

def scope_check(s):
    exact = {'group':'Fi22:2', 'constructor':'PrimitiveGroup(3510,2)',
             'group_order':129123503308800, 'socle_order':64561751654400,
             'string_pair_orders':[6,2,13], 'triangle_pair_orders':[6,6,13],
             'proper_IP_pairs':[49,49], 'remaining_IP_pairs_elementary':[15,15],
             'flag_equalities':[3,3], 'streamed_product_pairs':[464,768],
             'Lean_declarations':0, 'priority_claim':False, 'external_classification_proof_cost':None,
             'known_ten_case_recovery_separate':True, 'Fi24prime_unresolved_here':True,
             'actual_generated_group_equality_verified':True,
             'finite_required_programs':['programs/local_geometry.g','programs/verify.g'],
             'literal_witness':'witnesses/Fi22.g', 'complete_driver':'check.py'}
    for k,v in exact.items(): need(s[k] == v, 'scope differs: '+k)

def replay_check(r):
    need(r['status'] == 'PASS' and r['exact_generated_group_equality'] is True, 'finite result not accepted')
    need(r['named_group_identity_retained'] is True and r['maximal_subgroup_list_only_additional_validation'] is True,
         'retained/validation scope lost')
    need(r['Lean_declarations'] == 0 and r['priority_claim'] is False, 'inflated formal/priority scope')
    need(len(r['controls']) == 6 and all(x['rejected'] is True for x in r['controls']), 'finite controls')

def command(args, cwd, log, marker=None):
    p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    log.write_bytes(p.stdout); text = p.stdout.decode(errors='replace').replace('\\\n','')
    need(p.returncode == 0 and 'Error,' not in text and 'Syntax error:' not in text, 'process failed: '+str(log))
    if marker: need(marker in text, 'completion marker absent')
    return {'path':str(log.name),'sha256':sha(log),'returncode':p.returncode}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--packet-root',type=Path); ap.add_argument('--status-root',type=Path)
    ap.add_argument('--verify-primary',action='store_true'); ap.add_argument('--programs',action='store_true')
    ap.add_argument('--gap',default='gap'); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'output exists or is a dangling symlink')
    packet=a.packet_root or a.study_root/'corpus161_N006_Fi22_v2'
    status=a.status_root or a.study_root/'corpus161_N006_Fi22_status'
    own=bound_files(ROOT) if (ROOT/'manifest.json').exists() else None
    count=bound_files(packet,AUTHOR); status_count=bound_files(status,STATUS)
    scope=load(packet/'scope.json'); scope_check(scope)
    r=load(ROOT/'fresh_author/report.json'); replay_check(r)
    need(sha(ROOT/'fresh_author'/r['finite_replay']['path']) == r['finite_replay']['sha256'],'finite log changed')
    for rel,pin in r['source_bindings'].items(): need(sha(packet/rel)==pin,'fresh replay source changed')
    lit=(ROOT/'independent_literal.log').read_text().replace('\\\n','')
    need(MARKER in lit and 'FRESH_GROUP_HAS_SIZE false' in lit and 'PRIMITIVE_ROUTE 34 ' in lit,'independent evidence')
    raw=audit(packet/'witnesses/Fi22.g'); expected=load(ROOT/'data_audit.json')
    for k,v in raw.items(): need(expected[k]==v,'literal data mismatch')
    evidence=load(status/'evidence.json')
    need(evidence['own_mathematical_packet']['sha256']==AUTHOR and evidence['question_credit_change']==0,'status target changed')
    need(evidence['status']=='bounded_edition_and_literature_audit_not_priority_proof','status overclaim')
    if a.verify_primary: need(sha(a.study_root/'sources/phase283_geometry_wreath.pdf')==PRIMARY,'primary edition mismatch')
    mutations={'IP_not_enough':('flag_equalities',[0,0]),'wrong_type':('triangle_pair_orders',[6,2,13]),
               'identity_from_order':('actual_generated_group_equality_verified',False),
               'Fi24_overclaim':('Fi24prime_unresolved_here',False),'formal_overclaim':('Lean_declarations',1),
               'priority_overclaim':('priority_claim',True),'external_cost_zero':('external_classification_proof_cost',0),
               'pruned_program':('finite_required_programs',['programs/verify.g'])}
    controls=[]
    for name,(key,value) in mutations.items():
        bad=copy.deepcopy(scope); bad[key]=value
        try: scope_check(bad)
        except (RuntimeError,KeyError): controls.append({'name':name,'rejected':True})
        else: raise RuntimeError('control accepted: '+name)
    out=a.out.resolve(); out.mkdir(parents=True); live={}
    if a.programs:
        stage=out/'author_copy'; stage.mkdir()
        for row in load(packet/'manifest.json')['exports']:
            dst=stage/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(packet/row['path'],dst)
        shutil.copyfile(packet/'manifest.json',stage/'manifest.json')
        command([sys.executable,'-B','-O',str(stage/'check.py'),'--gap',a.gap,'--out',str(out/'author_replay')],stage,out/'author.log')
        replay_check(load(out/'author_replay/report.json'))
        gapq='LoadPackage("primgrp");Print(Filename(DirectoriesPackageLibrary("primgrp","")[1],""),"\\n");QUIT;'
        pkg=Path(subprocess.check_output([a.gap,'-q','-c',gapq],text=True).strip())
        d=audit(stage/'witnesses/Fi22.g',pkg)
        for key in ['decompressed_gps34_bytes','decompressed_gps34_sha256']:
            need(d[key]==expected[key],'catalogue data audit')
        for key in ['sha256','bytes']:
            need(d['additional_loader_index_binding'][key]==expected['additional_loader_index_binding'][key],'loader index changed')
        wrapper=out/'literal.g'
        # JSON quoting is GAP string quoting for these ordinary absolute file paths; no shell interpolation is used.
        wrapper.write_text('WitnessPath:='+json.dumps(str(stage/'witnesses/Fi22.g'))+';;\nRead('+json.dumps(str(ROOT/'literal_cosets.g'))+');;\n')
        live['literal']=command([a.gap,'-q','-T',str(wrapper)],out,out/'literal.log',MARKER)
        live['author_report_sha256']=sha(out/'author_replay/report.json')
    report={'status':'PASS','author_manifest_sha256':AUTHOR,'author_exports':count,'status_manifest_sha256':STATUS,
            'status_exports':status_count,'review_exports_checked':own,'source_primary_checked':a.verify_primary,
            'finite_markings':2,'proper_IP_pairs':98,'elementary_full_subset_pairs':30,'all_flag_families':6,
            'source_cases':'Fi22 possible exception only; Fi24prime untouched; ten affirmative cases separate',
            'semantic_controls':controls,'fresh_program_replay':live,'Lean_declarations':0,
            'priority_claim':False,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))

if __name__=='__main__':
    try: main()
    except Exception as e: print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
