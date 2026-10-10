#!/usr/bin/env python3
"""Verify the frozen author U+A checkpoint; no mathematical admission or census replay."""
import argparse, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(p,m):
    if not p: raise RuntimeError(m)
def resolve(rec):
    if rec.get('root')=='formal':
        choices=[ROOT.parent/'formal',ROOT.parent.parent/'math_compression/research/case_study/formal']
        for base in choices:
            if (base/rec['path']).is_file(): return base/rec['path']
        raise RuntimeError('Missing formal binding '+rec['path'])
    return ROOT/rec['path']
def check(rec):
    p=resolve(rec);require(p.is_file(),'Missing '+str(p));require(sha(p)==rec['sha256'],'Hash mismatch '+str(p))
def nodes(x,t):
    if isinstance(x,dict):
        return ([x['c']] if x.get('t')==t else [])+[z for v in x.values() for z in nodes(v,t)]
    if isinstance(x,list): return [z for v in x for z in nodes(v,t)]
    return []
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--primary-check',action='store_true');ap.add_argument('--private-visual',action='store_true')
    ap.add_argument('--rebuild',action='store_true');a=ap.parse_args()
    require(not a.output.exists(),'Refusing existing output')
    manifest=json.loads((ROOT/'phase117_two_group_application_manifest.json').read_text())
    for rec in manifest['exports']+manifest['required_shared_bindings']: check(rec)
    ledger=json.loads((ROOT/'phase117_two_group_application_ledger_checkpoint04.json').read_text())
    cost=json.loads((ROOT/'phase117_two_group_application_checkpoint04.json').read_text())
    text=(ROOT/'phase117_two_group_application.md').read_text()
    require(len(ledger['contract_rows'])==44 and len(ledger['detailed_multiclauses'])==17,'Contract size')
    old=json.loads((ROOT/'phase78_n009_integration_ledger.json').read_text())
    byid={r['integration_id']:r for r in old['contracts']}
    for row in ledger['contract_rows']:
        oldrow=byid[row['id'][2:]]
        require(row['exact_normalized_target']==oldrow['full_source_formulation_normalized'],'Target changed')
        for loc in row['proof_locations']:
            s=text[loc['start_codepoint']:loc['end_codepoint_exclusive']]
            require(hashlib.sha256(s.encode()).hexdigest()==loc['sha256_utf8'],'Adapter span changed')
    expected_sources={'L032','L035','F013','F016','N009'}
    require(set(ledger['source_bundle'])==expected_sources,'Source bundle')
    inherited=json.loads((ROOT/'phase98_twelve_measurement_report.json').read_text())
    for sid,doc in ledger['source_versions_and_measurement_boundaries'].items():
        source=inherited['source_documents'][sid]
        require(doc['pdf_binding']['sha256']==source['pdf_sha256'],'Edition binding')
        require(doc['selected_body']==source['selected_body'] and doc['exclusions']==source['exclusions'],'Source boundary')
        require(doc['inherited_main_body_metrics']==source['metrics'],'Inherited source measurement')
        if a.primary_check: check(doc['pdf_binding'])
    programs=ledger['certificate_artifacts']
    require(sum(x['utf8_bytes'] for x in programs)==56375,'Full certificate cost')
    require(len(text.encode())==78524,'Application cost')
    u=ROOT/ledger['umbrella']['proof']['path'];require(u.stat().st_size==56096,'Full U cost')
    total=len(text.encode())+u.stat().st_size+sum(x['utf8_bytes'] for x in programs)
    require(total==cost['complete_U_plus_A_raw_bytes']==190995,'Full proof cost')
    require(cost['gross_added_bytes']-cost['gross_removed_bytes']==cost['signed_rewrite_delta_bytes']==809,'Edit accounting')
    require(cost['ratio'] is None and ledger['claims']['ratio'] is None,'Unapproved ratio')
    source_total=sum(x['inherited_main_body_metrics']['NFC']['whitespace_tokens'] for x in ledger['source_versions_and_measurement_boundaries'].values())
    require(source_total==40373==cost['same_source_PDF_NFC_totals']['whitespace_tokens'],'Source total')
    render=ROOT/'phase117_two_group_application_render'
    visual=json.loads((ROOT/'phase117_two_group_application_visual.json').read_text())
    report=json.loads((render/'render_report.json').read_text())
    require(report['pages']==21 and visual['all_pages_inspected'] and len(visual['pages'])==21,'Visual scope')
    require(report['PDF_sha256']==sha(render/'application.pdf')==visual['pdf_sha256'],'Rendered PDF')
    require(visual['manuscript_sha256']==sha(ROOT/'phase117_two_group_application.md')==report['manuscript']['sha256'],'Render manuscript')
    require((render/'source.md').read_text()==text,'Render source')
    s=json.loads((render/'source.json').read_text());r=json.loads((render/'render.json').read_text())
    for typ in ['Math','Table','CodeBlock']: require(nodes(s,typ)==nodes(r,typ),'Changed AST '+typ)
    require(not any(re.search('Missing|Overfull',line,re.I) for line in report['diagnostics']),'Rendering diagnostic')
    extracted=''.join((render/'application_extraction.txt').read_text().split())
    for probe in ['{4,4}*32','{4,4}*128','{4,8}*128a']:require(probe in extracted,'Lost literal Atlas star')
    if a.private_visual:
        for rec in visual['pages']:check(rec)
    rebuilt=False
    if a.rebuild:
        with tempfile.TemporaryDirectory(prefix='phase117-rebuild-') as d:
            out=Path(d)/'A.md'
            result=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase117_two_group_application_build.py'),'--output',str(out)],capture_output=True,text=True)
            require(result.returncode==0,'Builder failed: '+result.stderr)
            require(out.read_bytes()==(ROOT/'phase117_two_group_application.md').read_bytes(),'Builder output changed')
        rebuilt=True
    result=dict(status='PASS_author_checkpoint_integrity_not_independent_mathematical_review',manifest_sha256=sha(ROOT/'phase117_two_group_application_manifest.json'),
        manuscript_sha256=sha(ROOT/'phase117_two_group_application.md'),source_bundle=sorted(expected_sources),contract_rows=44,multipart_clauses=17,
        application_pages=21,complete_raw_proof_bytes=total,source_PDF_tokens_inherited=source_total,ratio=None,
        primary_PDF_hashes_checked=a.primary_check,private_visual_hashes_checked=a.private_visual,rebuild_byte_exact=rebuilt,
        all_exports_read_and_hashed=True,group_computations_rerun=False,full_Lean_verification=False)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
