"""Record the private, unaccepted applicability boundary without target execution."""
import hashlib,json,pathlib
if not __debug__:raise SystemExit('optimized execution forbidden')
HERE=pathlib.Path(__file__).resolve().parent;S=HERE.parents[2]
def pin(p):
    p=pathlib.Path(p).resolve();b=p.read_bytes()
    try:q=str(p.relative_to(S));ns='study'
    except ValueError:q=str(p);ns='runtime'
    return dict(namespace=ns,path=q,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def main():
    evidence={
      'input_probe01':'PASS_RETAINED_TABLE_METADATA_NO_EXTENSION',
      'model_probe01':'PASS_EXPLICIT_NAMED_MODEL_ISOMORPHISM_NO_EXTENSION',
      'input_catalogue_execution01':'PASS_COMPLETE_RETAINED_INPUT_PREPARATION_NO_EXTENSIONS',
      'small_execution01':'PASS_SMALL_MODELS_UNCHANGED_ENGINE_NO_L100_CENSUS',
      'rank3_execution01':'PASS_POSITIVE_RANK_THREE_CONTROL_NO_TARGET',
      'recognition_execution01':'PASS_BROAD_RECOGNITION_SMALL_MODELS count=64 non_2T=8',
      'loader_execution02':'PASS_LOADER_ONLY_NO_BOREL_OR_EXTENSION_CALL'}
    checked=[]
    for folder,marker in evidence.items():
        d=HERE/folder;r=json.loads((d/'receipt.json').read_text())
        assert r['status']=='RETURNED' and r['returncode']==0 and not (d/'stderr').read_bytes()
        assert marker in (d/'stdout').read_text() and 'Error,' not in (d/'stdout').read_text()
        for k in ['input','stdout','stderr']:
            p=pathlib.Path(r[k]['path']);b=p.read_bytes()
            assert len(b)==r[k]['bytes'] and hashlib.sha256(b).hexdigest()==r[k]['sha256']
        checked.append(dict(receipt=pin(d/'receipt.json'),semantic_marker=marker,semantic_pass=True))
    fail=json.loads((HERE/'loader_execution01/receipt.json').read_text())
    assert (HERE/'loader_execution01/stderr').read_bytes() and fail['returncode']==0
    models=[]
    for d in ['literal01','rank3_literal01']:
        r=json.loads((HERE/d/'report.json').read_text());assert r['status'].startswith('PASS_')
        models+=r['models']
    totals={k:sum(m['counts'].get(k,0) for m in models) for k in models[0]['counts']}
    assert totals==dict(literal_panel_subsets=403,literal_valid_families=188,inner_type_classes=160,borels=46,full_classes=86)
    write('controls_summary.json',dict(status='PASS_DRAFT_BOUNDED_APPLICABILITY_CONTROLS_NO_TARGET',
      executions=checked,literal_totals=totals,models=[m['name'] for m in models],
      independent_model_reports=[pin(HERE/d/'report.json') for d in ['literal01','rank3_literal01']],
      damage_report=pin(HERE/'damage01/report.json'),
      failed_initial_loader=dict(receipt=pin(HERE/'loader_execution01/receipt.json'),accepted=False),
      target_runs=0,owned_live_handles=[]))
    write('input_contract.json',dict(status='RETAINED_COMPLETE_INPUT_PREPARED_NO_TARGET',
      group='PSL(3,4)',order=20160,degree=21,table='L3(4)',tomlib='1.2.11',gap='4.15.1',
      subgroup_classes=95,maximal_inclusion_classes=367,locally_2T_inclusions=311,
      table_file='tomlib/data/tmlino.tom.gz',explicit_model_map='input_catalogue01.g:source_generators,image_generators',
      catalogue=pin(HERE/'input_catalogue01.g'),
      actual_named_model=pin(S/'geometry/psl3_4/result.g'),
      input_proof='Every retained subgroup representative and maximal inclusion is transported by the same saved verified bijective homomorphism; reconstructed actual generators give the same named group.',
      retained=['TomLib complete subgroup conjugacy classification and stored representatives',
      'GAP complete ConjugacyClassesMaximalSubgroups for every actual representative',
      'Exact group homomorphism/size/transporter/orbit/coset algorithms'],
      not_inferred=['Completeness from matching subgroup orders','Named group from order alone','Fresh isomorphism choices are identical','Primitivity implies local2T'],
      software_note='RepresentativeTom sets cached size from the retained table; this is not a new independent order proof. The loader reconstructs groups from the saved literal generators and checks all recorded orders.'))
    write('integration_limits.json',dict(status='READ_EXACT_LEGACY_BOUNDARIES',findings=[
      dict(file='phase7_sporadic_search.g',issue='Default REQUIRE_2T=true',route='Explicit false, exact functions preserved'),
      dict(file='phase7_sporadic_verify.g',issue='Unconditional r.twot required; reconstructs original TomLib model',route='Reuse phase4 VerifyGeometry unchanged, omit only twot acceptance filter, report actual local flags; use exact common named model'),
      dict(file='phase7_sporadic_finish.py',issue='--require-2t default True/store_true has no false route',route='Do not call this historical driver for L100'),
      dict(file='phase7_sporadic_fuse.g',issue='Original TomLib model; truncations skip non-2T source and target',route='Future separate same-model fusion/metadata adapter; no blind truncation claim')],
      equivalence='Inner/type output first; full Aut/type fusion next; bare incidence isomorphism requires its own complete test or proved implication.',
      source_attribution='These are scope limits of reuse, not errors in historical locally-2T applications.'))
    write('target_proposal.json',dict(status='PROPOSED_NOT_LAUNCHED',prepared_request=pin(HERE/'prepared02/request.json'),
      selected_anchors=list(range(95,0,-1)),cap_seconds=60,require_2T=False,
      complete_target_boundary='Every subgroup-conjugacy Borel of the fixed PSL34 model, all ranks and partial joins; only full-group joins become geometry outputs.',
      termination='Rank<=Omega([G:B])<=10; demand an empty next level, at most11. Every completed anchor must be separately bound; unfinished anchors remain unpaid.',
      wrapper_requirement='A separate target receipt owner must recheck all request inputs, record process/semantic status, preserve stdout/stderr and all partial checkpoints, and never treat exit0 alone as success.',
      would_advance=['L100 Principal-contract: complete specified-G candidate enumeration for ranks3,4,5 and all higher ranks',
                     'Classification-method: independent residue-extension exhaustion under retained input premises',
                     'Rank2 candidate crosscheck against accepted component; new per-witness order/type/local-primitive data'],
      would_not_discharge=['Bare incidence isomorphism class counts without fusion/separation',
                          'Full Aut/Cor groups, kernel/group names, all printed fusion multiplicities',
                          'Remaining incidence constructions, doubling and source-wide recovery'],
      new_credit=0))
    study_names=['phase6_sporadic_search.g','phase6_sporadic_theory.md','phase7_sporadic_search.g','phase7_sporadic_theory.md',
      'phase7_sporadic_verify.g','phase7_sporadic_fuse.g','phase7_sporadic_finish.py','phase4_geometry_checks.g',
      'topic_D_volume/manifest.json','topic_D_volume/umbrella.tex','topic_D_volume/preamble.tex',
      'topic_D_volume/sections/01-actions.tex','topic_D_volume/sections/02-support.tex','topic_D_volume/sections/03-panels.tex',
      'topic_D_volume_independent_review/manifest.json','topic_D_volume_independent_review/review.json',
      'topic_D_root_adoption/manifest.json','topic_D_root_adoption/review.json',
      'topic_G_L102_root_review/manifest.json','topic_G_L102_root_review/review.rst',
      'corpus106_source_reading_L091_L100_L102/L100_intake.json',
      'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf',
      'corpus106_L100_rank_two_v2/manifest.json','corpus106_L100_rank_two_independent_review/manifest.json',
      'corpus106_L100_rank_two_root_adoption/manifest.json','geometry/psl3_4/result.g',
      'geometry/psl3_4/constructions_component_v1/manifest.json','geometry/psl3_4/constructions_review_v1/manifest.json',
      'geometry/psl3_4/constructions_root_adoption/manifest.json',
      'reboot_20261013/phase7_rwpri_preliminary_review/report.json','reboot_20261013/L100_higher_advisory/report01.json']
    runtime_root=pathlib.Path('/opt/homebrew/Cellar/gap/4.15.1')
    runtime=[runtime_root/'lib/gap/pkg/tomlib'/n for n in ['PackageInfo.g','data/tmlino.tom.gz','data/tmprimar.tom.gz','gap/tmstdrd.tom','gap/tmadmin.tmi','doc/chap1.txt']]
    runtime += [runtime_root/'share/gap/lib'/n for n in ['tom.gi','grplatt.gi']]
    runtime += [pathlib.Path('/opt/homebrew/bin/gap')]
    write('dependencies.json',[pin(S/n) for n in study_names]+[pin(p) for p in runtime])
    log=(HERE/'applicability.log').read_text();assert not any(x in log for x in ['Overfull','Underfull','LaTeX Warning'])
    write('native_review.json',dict(status='THREE_FINAL_NATIVE_PAGES_DIRECTLY_VIEWED',manuscript=pin(HERE/'applicability.tex'),pdf=pin(HERE/'applicability.pdf'),
      pages=[pin(HERE/f'page-{i:02}.png') for i in range(1,4)],layout='No warnings or overfull/underfull boxes',
      initial_layout_preserved=['initial_layout.pdf','initial_layout.log']))
    excluded={'draft_manifest.json'}
    exports=[pin(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in excluded and p.suffix not in ('.aux','.out')]
    write('draft_manifest.json',dict(status='AUTHOR_WORKING_DRAFT_FOR_APPLICABILITY_REVIEW_NO_TARGET',exports=exports,
      export_count=len(exports),owned_live_handles=[],no_target=True,new_source_credit=0,
      scope='Broad primitive recognition/augmentation adaptation, exact retained input map and small complete controls; no production or full L100 classification acceptance.'))
    print(json.dumps(dict(manifest=pin(HERE/'draft_manifest.json'),totals=totals),indent=2))
if __name__=='__main__':main()
