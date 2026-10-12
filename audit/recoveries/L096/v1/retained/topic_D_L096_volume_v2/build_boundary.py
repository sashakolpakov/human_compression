#!/usr/bin/env python3
"""Whole-file dependency inventory for a private, unadmitted L096 assembly."""
from pathlib import Path
import hashlib,json,argparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=Path(__file__).resolve().parent

def load(p):return json.loads(p.read_text())
def bind(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\n')

PACKETS=[
 ('topic_D_L096_extended_candidate','topic_D_L096_extended_root_review'),
 ('topic_D_L096_J1_extension','topic_D_L096_J1_root_review'),
 ('topic_D_L096_J2_extension','topic_D_L096_J2_root_adoption'),
 ('topic_D_L096_M22_extension','topic_D_L096_M22_root_adoption'),
 ('topic_D_L096_M23_extension','topic_D_L096_M23_root_adoption'),
 ('topic_D_L096_HS_extension','topic_D_L096_HS_root_review'),
 ('topic_D_L096_J3_extension','topic_D_L096_J3_root_review'),
 ('topic_D_L096_M12_missing','topic_D_L096_M12_missing_root_adoption'),
 ('topic_D_L096_Sz8_candidate','topic_D_L096_Sz8_root_adoption'),
 ('topic_D_L096_tree_candidate','topic_D_L096_tree_root_adoption'),
 ('topic_D_L096_cover_formal','topic_D_L096_cover_formal_root_adoption'),
]

def role_map(packet):
    p=ROOT/packet; roles={}
    inv=p/'program_inventory.json'
    if inv.exists():
        d=load(inv)
        for row in d.get('files',d.get('whole_files',[])):roles[row['path']]=row['role']
    scope=p/'program_scope.json'
    if scope.exists():
        d=load(scope)
        for k in ['required','literal_data','reconstructors','operational','validation']:
            for n in d.get(k,[]):roles[n]={'required':'required_program','literal_data':'required_literal_data','reconstructors':'required_source_or_roster_constructor','operational':'operational_runner','validation':'optional_validation'}[k]
    return roles

def fallback(packet,name):
    f=Path(name)
    if f.suffix=='.lean':return 'scoped_formal_evidence_not_full_algorithm_premise'
    if 'attempt01' in name:return 'failed_experiment_not_premise'
    if name in ['check.py','run.py']:return 'operational_checker_or_driver'
    if name in ['small_models.g','check_small_models.py','retained_tree_check.py']:return 'optional_validation'
    if name in ['sz8_rows.g','sz8_shadow_results.g']:return 'generated_mathematical_roster_or_receipt'
    return 'required_program_or_literal_data'

def main():
    global ROOT,OUT
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=ROOT);ap.add_argument('--out',type=Path,default=OUT)
    args=ap.parse_args();ROOT=args.study_root.resolve();OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
    accepted=[];occurrences=[];all_exports=[]
    for packet,review in PACKETS:
        m=ROOT/packet/'manifest.json';a=ROOT/review/'manifest.json'
        accepted.append({'component':packet,'author_manifest':bind(m),'accepted_by':bind(a),
                         'historical_author_status_preserved':True})
        d=load(m);roles=role_map(packet)
        for row in d['exports']:
            p=ROOT/packet/row['path'];actual=bind(p)
            if any(actual[k]!=row[k] for k in ['bytes','sha256']):raise ValueError(f'changed frozen export {p}')
            all_exports.append({**actual,'author_manifest':str(m.relative_to(ROOT))})
            if p.suffix in ['.g','.py','.lean']:
                occurrences.append({**actual,'role':roles.get(row['path'],fallback(packet,row['path'])),'component':packet,
                    'role_basis':'frozen author role inventory' if row['path'] in roles else 'explicit assembly whole-file classification',
                    'whole_file':True})
    census=[]
    certs=['phase5_j2_certificate.json','phase6_sporadic_M12_certificate.json','phase6_sporadic_J1_certificate.json','phase7_sporadic_M22_2T_certificate.json','phase7_sporadic_M23_2T_certificate.json']
    for n in certs:
        p=ROOT/n;d=load(p);artifacts=[]
        for name,row in d['artifacts'].items():
            f=ROOT/name;actual=bind(f)
            if any(actual[k]!=row[k] for k in ['bytes','sha256']):raise ValueError(f'changed census premise {f}')
            artifacts.append(actual)
            if f.suffix in ['.g','.py']:
                if '_checkpoints/' in name:role='retained_complete_census_checkpoint_data'
                elif name.endswith(('_run.py','_finish.py')):role='retained_operational_census_driver'
                elif name.endswith('_representatives.g'):role='retained_complete_census_mathematical_data'
                else:role='retained_required_census_program_or_certificate_checker'
                occurrences.append({**actual,'role':role,'component':n,'whole_file':True,
                    'role_basis':'retained accepted complete census artifact closure; no rerun or discount'})
        census.append({'certificate':bind(p),'complete_artifact_bindings':artifacts,'imported_group_data':d.get('imported_group_data'),
                       'trust_boundary':d.get('trust_boundary'), 'executed_again_for_assembly':False})
    # Explicit additive closure for the current aggregation layer. These are
    # whole files; executing an installed copy must bind its actual local bytes.
    current_roles={'assemble.py':'required_aggregate_reconstruction_program',
                   'build_boundary.py':'operational_whole_file_inventory_driver',
                   'check.py':'operational_integrity_and_render_checker'}
    for name,role in current_roles.items():
        f=HERE/name;raw=f.read_bytes()
        occurrences.append({'path':'topic_D_L096_volume_v2/'+name,'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest(),'role':role,
            'component':'topic_D_L096_volume_v2','whole_file':True,
            'location_basis':'current packet directory, portable-copy bytes',
            'role_basis':'additive independent inventory-review correction'})
    direct_data=[
      'topic_D_L096_extended_candidate/mathieu_results.json',
      'topic_D_L096_J1_extension/results.json',
      'topic_D_L096_J2_extension/results.json',
      'topic_D_L096_M22_extension/results.json',
      'topic_D_L096_M23_extension/results.json',
      'topic_D_L096_HS_extension/shadow_results.json',
      'topic_D_L096_J3_extension/shadow_results.json',
      'topic_D_L096_table_contract/source_tables.json']
    for name in direct_data:
        occurrences.append({**bind(ROOT/name),
            'role':'required_source_contract_data' if name.endswith('/source_tables.json') else 'required_mathematical_directional_results',
            'component':'current_aggregation_input','whole_file':True,
            'role_basis':'exact whole JSON directly consumed by unchanged assemble.py'})
    by_content={}
    for r in occurrences:by_content.setdefault(r['sha256'],[]).append(r)
    inventory={'status':'FROZEN_WHOLE_FILE_INVENTORY_NO_LENGTH_COMPARISON',
      'all_occurrences':occurrences,
      'unique_contents':[{'sha256':h,'bytes':v[0]['bytes'],'paths':sorted({x['path'] for x in v}),
                          'roles':sorted({x['role'] for x in v})} for h,v in sorted(by_content.items())],
      'optional_validation_rule':'Included on both sides or excluded on both sides; not an unmatched software compression scalar.',
      'source_listing':'Complete Magma Section6 and executable Figure1 are present. Source listings and replacement code must have matched treatment.',
      'required_data':'Literal subgroup families, accepted complete census data/checkpoints and exact witness records remain visible; code snippets do not replace full files.',
      'external_software_cost':None,'primary_graphics_cost':None,'measurement_factor':None}
    write('whole_program_inventory.json',inventory)
    write('accepted_dependencies.json',{'status':'FROZEN_ACCEPTED_INPUT_BINDINGS','accepted_components':accepted,
      'all_frozen_component_exports':all_exports,'retained_complete_censuses':census,
      'old_D_common':'Complete public papers/topic-d/v2 common and application census dependency are retained; exact scientific overlap is in topic_D_dependency_overlap.json.',
      'receipt_policy':'Original exact executions are retained; this assembly reruns only binding, quantifier, migration and render checks.',
      'scope':'Does not promote unresolved historical labels or global HS/J3 classification to new proofs.'})
    print(json.dumps({'accepted_components':len(accepted),'frozen_exports':len(all_exports),'census_artifact_occurrences':sum(len(x['complete_artifact_bindings']) for x in census),'raw_file_occurrences':len(occurrences),'unique_raw_contents':len(by_content)}))

if __name__=='__main__':main()
