"""Exact disjoint prior receipts leave only two separately selectable anchors."""
import importlib.util
import json
from pathlib import Path
import sys
if not __debug__:
    raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
G34=Path(__file__).resolve().parent.parent
AUTHOR_SHA='c62f381fa9006ec3d4e6ed8ab0bdef46c4a48f4bc7e53244d35285c6c6f39250'
REVIEW_SHA='3f95242847e5b799788df747ff8ef16289c929bdfefd784829d3d439d52696b7'
RECEIPT_SHA='10058107380afde9a818e81c50134065a1a03269c7cfb96a5e53612a0862b7b4'
ACCEPTANCE_SHA='ab7e02b5330535db6f5d174ffb07390d586bda438389e8b9b7ee69ea118c3cab'
AUDIT_SHA='1fca4e9f32ba0cff7bfcf182f83c1e27762a9c7e49dcca0acc357c1d9cfe7680'
NEW_PREFIX=list(range(11,2,-1))
ALL_COMPLETED=list(range(95,2,-1))
UNPAID=[2,1]

def require(ok,reason):
    if not ok:raise ValueError(reason)

def validate_boundary(r,requested):
    require(requested in ([2],[1]),'only a single fixed unpaid anchor is allowed')
    require(r['status']=='PARTIAL_DEADLINE' and r['target_census'] is True,'wrong suffix terminal status')
    require(r['requested_anchors']==list(range(11,0,-1)),'wrong suffix request')
    require(r['completed_anchors']==NEW_PREFIX and r['unpaid_anchors']==UNPAID,'wrong suffix boundary')
    require(r['previously_completed_anchors']==list(range(95,11,-1)),'wrong inherited completed prefix')
    require(r['previously_completed_anchors']+r['completed_anchors']==ALL_COMPLETED,'prior receipts not a disjoint complete prefix')
    require(not set(requested)&set(ALL_COMPLETED),'completed anchor repeated')
    require(r['execution']['status']=='DEADLINE' and r['execution']['returncode'] is not None,'prior child not terminal')
    require(r['target_cap_seconds']==180 and r['execution']['cap_seconds']==180,'prior cap mismatch')
    require(r['audit']['status']=='RETURNED' and r['audit']['returncode']==0,'prior audit failed')
    require(r['audited_returned_rows']==r['reported_completed_rows'] and
            [x[0] for x in r['audited_returned_rows']]==NEW_PREFIX,'prior rows mismatch')

def bind_previous(manifest_gate,verify,pin,requested):
    old=G34/'exhaustion_suffix_interface_v1';review=G34/'exhaustion_suffix_review_v1'
    rows=manifest_gate(old,AUTHOR_SHA,'AUTHOR_COMPLETE_L100_SUFFIX_INTERFACE_V1_AWAITING_ROOT_REVIEW')
    rows+=manifest_gate(review,REVIEW_SHA,'ACCEPTED_L100_SUFFIX_TARGET_INTERFACE_V1')
    v=json.loads((review/'review.json').read_text())
    require(v['author_manifest']['path']==str(old/'manifest.json') and v['author_manifest']['sha256']==AUTHOR_SHA,'prior review author binding')
    # Literally reuse the accepted first-run boundary validator, after its export hash is verified.
    spec=importlib.util.spec_from_file_location('accepted_first_boundary',old/'previous_boundary.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    rows+=module.bind_previous(manifest_gate,verify,pin)
    paths=[(G34/'exhaustion_target02/receipt.json',RECEIPT_SHA),
           (G34/'exhaustion_target02_acceptance_before.json',ACCEPTANCE_SHA),
           (G34/'exhaustion_target02_terminal_audit.json',AUDIT_SHA)]
    for path,sha in paths:
        actual=pin(path);require(actual['sha256']==sha,'prior evidence identity: '+str(path));rows.append(actual)
    r=json.loads(paths[0][0].read_text());a=json.loads(paths[1][0].read_text());t=json.loads(paths[2][0].read_text())
    validate_boundary(r,requested)
    require(a['command']==v['authorized_next_run'],'prior actual command not the reviewed command')
    require(t['receipt']['sha256']==RECEIPT_SHA and t['newly_completed_anchors']==NEW_PREFIX and t['unpaid_anchors']==UNPAID,'prior terminal audit binding')
    for row in r['inputs']+r['outputs']+a['pins']:rows.append(verify(row))
    for name in ['target/stderr','audit/stderr']:
        require(not (G34/'exhaustion_target02'/name).read_bytes(),'prior stderr nonempty')
    require(r['execution']['command']==['/opt/homebrew/bin/gap','-q','-b',str(G34/'exhaustion_target02/prepared/driver.g')],'prior execution command changed')
    return rows
