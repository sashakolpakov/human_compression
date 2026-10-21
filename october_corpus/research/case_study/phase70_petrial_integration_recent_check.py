#!/usr/bin/env python3
"""Independent integrity/reconstruction/finite replay; mathematical audit is separate."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys,tempfile,time
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);args=ap.parse_args()
assert not args.output_dir.exists() and not args.report.exists(),'fresh output paths required'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mf=root/'phase65_petrial_integration_manifest.json'
assert sha(mf)=='1636904c041cf0540ae452adbc962eb0ef914c3cab83f250a9b92bdfbe3bbc34'
m=json.loads(mf.read_text());before={mf.name:sha(mf)}
for group in ['files','retained_input_bindings']:
    for name,binding in m[group].items():
        assert sha(root/name)==binding['sha256'] and (root/name).stat().st_size==binding['bytes'],name
        before[name]=binding['sha256']
# Reconstruct all three assembly outputs, using the frozen builder in isolation.
with tempfile.TemporaryDirectory(prefix='phase70_reconstruction_') as td:
    tmp=Path(td)
    copies=set(m['retained_input_bindings'])|{'phase65_petrial_integration_build.py','phase65_petrial_integration_core.md','phase65_petrial_integration_branch.md','phase65_petrial_integration_check.py'}
    for name in copies:
        p=tmp/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((root/name).read_bytes())
    built=subprocess.run([sys.executable,str(tmp/'phase65_petrial_integration_build.py')],capture_output=True,text=True,cwd=td)
    assert built.returncode==0 and not built.stderr,built.stderr
    for name in ['phase65_petrial_integration_manuscript.md','phase65_petrial_integration_ledger.json','phase65_petrial_integration_assembly.json']:
        assert (tmp/name).read_bytes()==(root/name).read_bytes(),name
# Independently compare every old adapter's actual proof bytes with only the approved erratum.
base=(root/'phase45_ten_source_manuscript.md').read_text();text=(root/'phase65_petrial_integration_manuscript.md').read_text()
old=json.loads((root/'phase45_ten_source_adapter_map.json').read_text());new=json.loads((root/'phase65_petrial_integration_ledger.json').read_text());err=json.loads((root/'phase45_ten_source_errata.json').read_text())
oldby={x['integration_id']:x for x in old['contracts']};same=[];corrected=[]
for row in new['contracts']:
    if row['integration_id'] not in oldby:continue
    prev=oldby[row['integration_id']];p=prev['integrated_proof_span'];s=base[p['start_codepoint']:p['end_codepoint_exclusive']];expected=s
    for e in err['changes']:expected=expected.replace(e['old'],e['new'])
    p=row['integrated_proof_span'];actual=text[p['start_codepoint']:p['end_codepoint_exclusive']]
    assert actual==expected,row['integration_id'];(same if s==actual else corrected).append(row['integration_id'])
assert len(same)==73 and len(corrected)==6
pet=[r for r in new['contracts'] if r.get('paper')=='L108'];assert len(pet)==8
assert [r['integration_id'] for r in pet if r['literal_or_scoped']=='corrected_not_literal']==['PET.4','PET.8']
# Fresh execution extracts the exact manuscript code, never running a mutable default-output path.
start=time.monotonic();cmd=[sys.executable,str(root/'phase65_petrial_integration_verify.py'),'--output-dir',str(args.output_dir),'--run-petrial'];r=subprocess.run(cmd,capture_output=True,text=True);elapsed=time.monotonic()-start
assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
controls=json.loads((args.output_dir/'petrial_results.json').read_text());author=json.loads((root/'phase65_petrial_integration_controls.json').read_text());assert controls==author
assert controls['summary']=={'examples':7,'nonfaithful_petrial_actions':2,'original_chambers':188,'thin_petrials':4}
cases=controls['cases'];assert len(cases)==7
assert cases[0]['petrial']['type_sizes']==[2,2,1] and cases[0]['group_order']==8 and cases[0]['induced_action_order']==4
assert all(c['computed_core_order']==c['action_kernel_order']==(2 if c['face_marker_central'] else 1) for c in cases)
assert cases[2]['base_face_fixed_by_b'] and not cases[3]['base_face_fixed_by_b']
assert all(c.get('bidual_face_shadows_exact') and c.get('induced_action_chamber_regular') for c in cases if c['petrial']['thin'])
assert any(x=={'chambers':6,'edges':3,'vertices':3} for x in cases[1]['petrie_cycles'])
# Repeat with existing directory: rejection must leave all replay files byte-identical.
replay_before={p.name:sha(p) for p in args.output_dir.iterdir() if p.is_file()};rejected=subprocess.run(cmd,capture_output=True,text=True)
assert rejected.returncode!=0 and 'Refusing existing output directory' in rejected.stderr
assert {p.name:sha(p) for p in args.output_dir.iterdir() if p.is_file()}==replay_before
for name,digest in before.items():assert sha(root/name)==digest,name
report={'date':'2026-10-10','status':'PASS','mathematical_audit_separate':True,'runner_sha256':sha(Path(__file__)),'frozen_manifest_sha256':sha(mf),'all_inputs_pre_post_sha256':before,'reconstruction_byte_identical':True,'earlier_adapter_spans_unchanged':same,'earlier_adapter_spans_only_approved_erratum':corrected,'new_source_rows':8,'new_corrected_not_literal_rows':['PET.4','PET.8'],'Petrial_replay_seconds':elapsed,'Petrial_results_byte_identical_to_author':(args.output_dir/'petrial_results.json').read_bytes()==(root/'phase65_petrial_integration_controls.json').read_bytes(),'summary':controls['summary'],'replay_artifact_hashes':replay_before,'no_clobber':True,'old_GAP_programs':'exact bytes verified, not rerun','source_reading':'complete seven-page authored rendered text; no primary PDF','exhaustive_geometry_census':False,'Lean_claim':False,'priority_claim':False}
args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':elapsed,'manifest':sha(mf),'report':sha(args.report)},indent=2))
