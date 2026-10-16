from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');A=S/'algebra/subgroup_atlas';P=A/'publication_work';ST=P/'stage02';D=ST/'audit/recoveries/L054/v1';O=P/'portable_root01'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();t=json.loads((D/'transport.json').read_text());sm=json.loads((D/'manifest.json').read_text());report=json.loads((O/'report.json').read_text())
assert report['status']=='PASS_PUBLIC_L054_ARTICLE_MAIN_RESULTS_COMPLETE_CLOSURE'
assert (report['complete_groups'],report['structural_rows'],report['complete_proof_pages'],report['source_clauses'],report['native_pages'])==(134,15988,107,21,7)
assert not report['all_current_companion_tables_recovered'] and not report['companion_socle_bound_established']
for row in sm['exports']:c.add(ST/row['path'],row)
for row in t['existing_public_files']:c.add(R/row['path'],row)
c.add(D/'manifest.json');c.add(D/'transport.json');c.binding(t['root_acceptance'])
for folder in [O]:
    for q in folder.rglob('*'):
        if q.is_file():c.add(q)
for n in ['ready.json','publication_files.json','integration01/admission_proposal.json','portable_report_amendment01.diff','portable_report_amendment01.json']:
    c.add(P/n)
c.add(__file__)
c.finish('algebra/subgroup_atlas/publication_operational_root_review','ACCEPTED_L054_PORTABLE_PUBLICATION_V1',dict(
 author='l070_publication',reviewer='root',stage_manifest=c.add(D/'manifest.json'),transport=c.add(D/'transport.json'),
 mathematical_authority=c.add(A/'principal_v2_root_review/manifest.json'),root_portable_report=c.add(O/'report.json'),
 fresh_validation=dict(report=c.add(O/'report.json')),review=[
 'Read the complete content codec, public archive verifier, explicit selected-file replay adapter, admission controls and publication proposal. The adapter runs the exact accepted source/application join using only20 extracted input files; undeclared private paths fail. No scientific group calculation is repeated.',
 'Fresh root portable replay passed in36.08seconds. It verified all77176 logical bindings and47660 complete materialized content objects, including7.327GB decoded content, and authenticated the1160 expressly retained documentary/software premises. All31 new packs are exactly indexed with no gaps or overlaps, and earlier public payloads are tracked exact reuse.',
 'All107 native mathematical page streams,42 complete manuscripts with recursive TeX inputs, seven freshly rebuilt identical synthesis rasters, normal and optimized finite joins,15 damaged synthesis cases, storage corruption/path controls,12 metadata/boundary rejections,two actual CLI rejections and six optimization guards passed. Earlier native mathematical review is acquired; this operational pass does not reauthor those proofs.',
 'The first author-stage report-construction error is retained explicitly; the changed packs.values() report expression is separate and leaves the mathematical inputs unchanged. The exact successful stage02 and actual root report are bound.',
 'The134 complete applications contain15988 subgroup rows. The scope remains the article generic and quantified main results, not the entire historical/current companion atlas, stronger socle-order domain or every attributed sporadic output. Complete companion ledger and recognition/software premises remain explicit.',
 'This operational acceptance alone adds no original, conjecture, Lean or compression credit. Concrete source registration and public Git publication remain separate.'
 ]))
