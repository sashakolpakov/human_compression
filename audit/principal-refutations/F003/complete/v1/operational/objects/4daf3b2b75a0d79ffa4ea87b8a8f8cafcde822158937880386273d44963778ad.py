from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');F=S/'geometry/suzuki_source_completion';W=F/'publication_work';ST=W/'stage01';D=ST/'audit/principal-refutations/F003/complete/v1'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_source_completion/source_synthesis_root_review')
c.add(D/'manifest.json')
for row in json.loads((D/'manifest.json').read_text())['exports']:c.add(ST/row['path'],row)
for name in ['portable_check.py','pack_codec.py','prior_transport_reader.py']:c.add(W/name)
for p in(W/'portable_root01').rglob('*'):
 if p.is_file():c.add(p)
c.add(Path(__file__))
r=json.loads((W/'portable_root01/report.json').read_text())
if r['status']!='PASS_PORTABLE_F003_SOURCE_COMPLETION':raise ValueError('Portable check failed')
c.finish('geometry/suzuki_source_completion/portable_completion_root_review','ACCEPTED_F003_PORTABLE_COMPLETE_SOURCE_TREATMENT',dict(
 reviewer='root',author='j3_recovery',
 review=[
 'Read complete new portable checker; accepted codec and archive reader are acquired byte-identically through reused_tools.json.',
 'Root replay verifies the exact236-file accepted proof closure:172 payload objects,116 existing public files and exactly six explicit source documentary premises. The four source page images, source PDF and source extraction are not represented as distributed payload.',
 'Fresh literal binary check, six witness/scope damages, two optimization guards and unchanged codec damage controls pass.',
 'All three TeX entry points rebuild. Eleven embedded page drawing streams and font programs match, and all seven fresh cover/supplement rasters equal the directly reviewed author pages. Existing principal proof is byte-identical.',
 'No private fallback, new group acquisition, duplicate refutation, Lean claim or compression measurement is introduced. Registration remains a separate final step.'
 ],
 report=c.add(W/'portable_root01/report.json'),stage_manifest=c.add(D/'manifest.json'),transport=c.add(D/'transport.json'),
 ordinary_recovery_delta=0,principal_refutation_delta=0,registration_pending=True))
