#!/usr/bin/env python3
"""Bind the five-source A draft and checkpoint exact, non-rendered proof costs.

Source PDF metrics are inherited with their protocol and verified source hashes;
they are never divided by Markdown metrics. The full frozen U v2 is charged.
This is a draft inventory and does not claim independent mathematical admission.
"""
import argparse
import difflib
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ['L032','L035','F013','F016','N009']
PROGRAMS = ['phase78_n009_integration_census.g','phase78_n009_integration_finite.g',
            'phase78_n009_integration_data.g','phase78_n009_integration_run.py']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
    text = p.read_text()
    return dict(path=p.name,sha256=sha(p),utf8_bytes=p.stat().st_size,
                codepoints=len(text),plain_NFC_whitespace_tokens=len(unicodedata.normalize('NFC',text).split()))
def require(p,m):
    if not p: raise RuntimeError(m)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--label',default='checkpoint04')
    args=ap.parse_args()
    require(re.fullmatch(r'checkpoint\d{2}',args.label) is not None,'Bad checkpoint label')
    require(not args.output_dir.exists(),'Refusing existing output directory')
    old_path=ROOT/'phase78_n009_integration_ledger.json'
    require(sha(old_path)=='d1b08624baee1c2bf4a53dacc23d12643e6ee901a680fe039aa61a4899733367','Source contract changed')
    old=json.loads(old_path.read_text())
    umbrella_path=ROOT/'phase123_umbrella_manuscript_v2.md'
    require(sha(umbrella_path)=='d6c5d4b087c4bb4cab29f4729314dfc1dbaa640410d1d0ca9a73f33651058e2c','Umbrella v2 proof changed')
    umbrella_manifest=ROOT/'phase123_umbrella_v2_manifest.json'
    require(sha(umbrella_manifest)=='9002027eadbe57af96e66149b76a0327cd0fc64136cef5ac8062c68aab26fa87','Umbrella v2 manifest changed')
    a=ROOT/'phase117_two_group_application.md'
    text=a.read_text()
    headings=list(re.finditer(r'^## (\d+)\. .+$',text,re.M))
    require([int(x.group(1)) for x in headings]==list(range(1,10)),'Nine scientific sections absent')
    boundaries=[x.start() for x in headings]+[text.index('## Appendix C.')]
    sections={str(i+1):dict(start_codepoint=boundaries[i],end_codepoint_exclusive=boundaries[i+1],
               sha256_utf8=hashlib.sha256(text[boundaries[i]:boundaries[i+1]].encode()).hexdigest(),
               utf8_bytes=len(text[boundaries[i]:boundaries[i+1]].encode())) for i in range(9)}
    calls={
      'U.D1':(['3','4'],['U.SK','U.DEL'],'A4.1'),
      'U.D2':(['3','4'],['U.SK','U.DEL'],'A4.1, d=3'),
      'U.D3':(['2','3','5','7'],['U.PHI','U.FQ','U.LAD'],'A5.1–A5.2, complete models and bounded seed'),
      'U.D4':(['2'],['U.PHI'],'A2.1–A2.4'),
      'U.D5':(['2'],['U.PHI'],'A2.4 and retained cover correspondence'),
      'U.D6':(['2','3','4'],['U.SK','U.DEL'],'A4.2 path and separator bindings'),
      'U.D7':(['2','3','4'],['U.SK','U.DEL','U.Order'],'A4.3 and bare universal presentation/order bound'),
      'U.D8':(['2','3','4'],['U.SK','U.DEL'],'A4.2 fork fiber-isomorphism and geometric assembly'),
      'U.D9':(['8'],['U.TOR'],'regular free-extension identification'),
      'U.D10':(['8'],['U.TOR'],'oriented chiral identification; only facet rotations embed'),
      'U.D11':(['8'],['U.TOR'],'universal alternating identification and optional branch swap'),
    }
    rows=[]
    for r in old['contracts']:
        if r['paper'] not in SOURCES: continue
        rid=r['integration_id']
        if r['paper']=='N009':
            n=int(rid.split('.')[1])
            if n in [1,6]: loc,u,target=['1'],[],'marking/equivalence definitions'
            elif n in [2,3,4]: loc,u,target=['6'],[],'explicit retained low-rank intersection criterion'
            elif n in [5,7]: loc,u,target=['6'],[],'N1 endpoint-coset proof or defining Coxeter epimorphism'
            elif n==8: loc,u,target=['6'],['U.PHI'],'binary Frattini coordinate characters'
            elif n in [9,10,11]: loc,u,target=['6'],['U.Q'],'quotient intersection criterion and marked dihedral end checks'
            elif n in [12,13]: loc,u,target=['6'],['U.PHI'],'N2 central-in-end-product proof, including the Frattini obstruction'
            elif n in [14,15]: loc,u,target=['6'],['U.Q','U.PHI'],'N2–N3 central descent with explicit order-eight boundary'
            elif n in [16,28]: loc,u,target=['6'],[],'N4 complete binary relator lift and exact presentation-order proof'
            elif n in [18,19]: loc,u,target=['7'],[],'combined presentation definition and explicitly retained geometric universality'
            elif n in [23,25]: loc,u,target=['7'],[],'explicit retained square-quotient or infinite-decomposition theorem'
            elif n==24: loc,u,target=['3','7'],[],'A3.1 affine model and N5 direct fixed-translation calculation'
            elif n==26: loc,u,target=['7'],['U.PHI'],'N6 coordinate-character proof conditional on retained decomposition'
            elif n in [20,21,22,29,30,31]: loc,u,target=['7'],[],'complete raw-presentation enumeration and actual marked isomorphisms'
            else:
                loc,u,target=['2','7'],['U.FQ','U.LAD','U.PHI'],'A2.5 complete census with A2.1 class-two premise, and exact named-object recognition'
        else: loc,u,target=calls[rid]
        rename={'U.SK':'U.SK','U.DEL':'U.D','U.PHI':'U.Phi','U.FQ':'U.Nilpotent','U.LAD':'U.Ladder','U.TOR':'U.Amalgam','U.Q':'U.Q','U.Order':'U.Order'}
        rows.append(dict(id='A.'+rid,source_id=r['paper'],source_reference=r['source_reference'],
          exact_normalized_target=r['full_source_formulation_normalized'],
          source_status=r['literal_or_scoped'],proof_locations=[dict(section=s,**sections[s]) for s in loc],
          principal_result_or_inventory_record=('source_inventory_record' if r['paper']=='N009' else 'principal_result'),
          application_derivation=target,umbrella_calls=[rename[x] for x in u],
          source_imports=r.get('retained_inputs',r.get('selected_imported_inputs',[])),
          scope_corrections_section='9',
          use_map_status='author_declared_actual_derivation_bound_to_frozen_U_v2_independent_review_pending',
          section_spans_are_not_dependency_closures=True,
          semantic_necessity_claim=False,full_Lean_verification=False))
    require(len(rows)==44,'Wrong five-source contract size')
    source_report_path=ROOT/'phase98_twelve_measurement_report.json'
    measured=json.loads(source_report_path.read_text())
    docs={}
    for sid in SOURCES:
        doc=measured['source_documents'][sid]
        p=ROOT/doc['pdf_path']
        require(sha(p)==doc['pdf_sha256'],'Source edition hash mismatch: '+sid)
        docs[sid]=dict(source_id=sid,pdf_binding=dict(path=doc['pdf_path'],sha256=doc['pdf_sha256'],pages=doc['pdf_pages']),
          source_version=(old['source_versions']['Unified'][sid] if sid!='N009' else old['source_versions']['N009']),
          inherited_main_body_metrics=doc['metrics'],selected_body=doc['selected_body'],exclusions=doc['exclusions'],
          extraction_freshly_repeated_in_this_checkpoint=False,
          same_source_PDF_bytes_verified=True,
          newly_normalized_house_format_measurement=False,
          whole_source_body_is_not_exact_target_proof_slice=True)
    formal_root=ROOT.parent.parent/'math_compression/research/case_study/formal'
    formal={}
    for n in ['BooleanRetractions.lean','GradedSupport.lean','CoordinateKernels.lean','LiftCertificate.lean','QuotientIntersectionCriterion.lean']:
        formal[n]=record(formal_root/n)
    ledger=dict(schema='focused_two_group_application_contract_v1',status='author_checkpoint_independent_review_pending',
      source_bundle=SOURCES,contract_rows=rows,contract_row_count=44,
      detailed_multiclauses=old['detailed_two_group_clause_rows'],
      source_versions_and_measurement_boundaries=docs,
      source_contract_material=dict(path=old_path.name,sha256=sha(old_path),role='reused exact source contracts; no monolith product or benchmark'),
      application=record(a),section_bindings=sections,
      umbrella=dict(status='complete_second_author_checkpoint_bound_independent_admission_pending',
                    proof=record(umbrella_path),contract=record(ROOT/'phase123_umbrella_v2_contracts.json'),
                    manifest=record(umbrella_manifest),full_shared_proof_charged_once=True,
                    exclusion_as_zero_cost_forbidden=True),
      certificate_artifacts=[record(ROOT/n) for n in PROGRAMS],
      certificate_replay='python3 -B -O research/leemans/phase78_n009_integration_run.py --output-dir /private/tmp/NEW-two-group-certificate',
      unchanged_computations_reexecuted=False,
      formal_artifacts=formal,
      formalization_map=[
        dict(theorem='A4.3',scope='complete stated four-marker group lemma',
             artifact='BooleanRetractions.lean',declaration='MathCompression.BooleanRetractions.four_marker_centralization',
             source_application_full_Lean=False,compiled_evidence='existing published compile; not rerun or altered here'),
        dict(theorem='A2.1–A2.3',scope='only split-kernel image disjointness and cardinality-to-factorization components',
             artifact='GradedSupport.lean',full_theorem=False,
             missing=['lower-central descending induction','graded Lie support','forest independence and quotient identification']),
        dict(theorem='U.SK used in A4.1/A4.2',scope='only supported-coordinate meet and resulting intersection transport',
             artifact='CoordinateKernels.lean',full_theorem=False,
             missing=['local kernel isolation by inclusion induction','full fiber generation','derived deletion/lower-central/separator clauses'])],
      claims=dict(new_conjecture_solution=False,historical_priority=False,ratio=None,source_papers_fully_Lean_verified=False,
                  five_source_mathematical_admission=False))
    programs=[record(ROOT/n) for n in PROGRAMS]
    metric_keys=['whitespace_tokens','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    previous=ROOT/'phase117_two_group_application_checkpoint01.md'
    oldtext=previous.read_text()
    changes=[]
    oldlines=oldtext.splitlines(keepends=True);newlines=text.splitlines(keepends=True)
    for tag,i,j,k,l in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
        if tag!='equal':
            before=''.join(oldlines[i:j]);after=''.join(newlines[k:l])
            changes.append(dict(tag=tag,old_codepoints=len(before),new_codepoints=len(after),
              old_bytes=len(before.encode()),new_bytes=len(after.encode())))
    checkpoint=dict(schema='U_plus_A_acquisition_checkpoint_v1',status=args.label,
      application=record(a),complete_external_certificate_cost=programs,
      application_plus_certificate_bytes=a.stat().st_size+sum(x['utf8_bytes'] for x in programs),
      umbrella_required_cost=record(umbrella_path),
      complete_U_plus_A_raw_bytes=umbrella_path.stat().st_size+a.stat().st_size+sum(x['utf8_bytes'] for x in programs),
      source_body_protocol=dict(report=source_report_path.name,sha256=sha(source_report_path),
          protocol_sha256=measured['protocol_sha256'],role='existing source PDF complexity only; no mixed-metric ratio'),
      same_source_PDF_NFC_totals={k:sum(docs[s]['inherited_main_body_metrics']['NFC'][k] for s in SOURCES) for k in metric_keys},
      source_normalized_house_format_cost=None,replacement_rendered_cost=None,ratio=None,
      previous_application=record(previous),
      signed_rewrite_delta_bytes=a.stat().st_size-previous.stat().st_size,
      gross_added_bytes=sum(x['new_bytes'] for x in changes),
      gross_removed_bytes=sum(x['old_bytes'] for x in changes),
      exact_text_diff_method='difflib.SequenceMatcher whole-line opcodes, autojunk=False; gross replacement-line bytes, not minimal character edits, semantic proof novelty or intrinsic marginal complexity',
      delta_note='Same44-source-contract application and unchanged four full certificates. Full U acquisition now bound and charged once; its initial inclusion is gross acquisition, not marginal application reuse. Changes in A since01 are stable theorem IDs, human mathematical typography, explicit G binding and title/table-label corrections, not proof compression. No zero cost from relocation.',
      old_monolith_used_as_product_or_benchmark=False,
      dependency_ablation_limit='Removal invalidates only this declared derivation, not every possible proof.',
      reuse_note='Existing branch proofs/certificates reused; this is not a new model-acquisition experiment or a replay of unchanged computations.')
    require(a.read_text()==text,'Application changed during checkpoint; discard this run')
    args.output_dir.mkdir(parents=True)
    (args.output_dir/('phase117_two_group_application_ledger_'+args.label+'.json')).write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    (args.output_dir/('phase117_two_group_application_'+args.label+'.json')).write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='DRAFT_INVENTORY',rows=len(rows),application_bytes=a.stat().st_size,
          certificate_bytes=sum(x['utf8_bytes'] for x in programs),
          full_U_plus_A_raw_bytes=checkpoint['complete_U_plus_A_raw_bytes'],ratio=None)))

if __name__=='__main__': main()
