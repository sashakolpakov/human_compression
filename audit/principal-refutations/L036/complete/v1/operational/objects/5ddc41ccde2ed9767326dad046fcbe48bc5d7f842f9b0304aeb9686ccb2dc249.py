from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/primitive_pairs';W=P/'publication_work';T=W/'stage01'
A=T/'audit/principal-refutations/L036/complete/v1';O=W/'root_portable01'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/primitive_pairs/source_synthesis_root_review')
c.add(A/'manifest.json')
for row in json.loads((A/'manifest.json').read_text())['exports']:c.add(T/row['path'],row)
for row in json.loads((A/'transport.json').read_text())['existing_public_files']:c.add(Path('/Users/sasha/medusa/math_compression')/row['path'],row)
for p in O.rglob('*'):
 if p.is_file():c.add(p)
for p in [W/'root_portable01.stdout',W/'root_portable01.stderr',Path(__file__)]:c.add(p)
r=json.loads((O/'report.json').read_text())
if r['status']!='PASS_PORTABLE_L036_SOURCE_COMPLETION' or r['native_pages']!=24 or r['root_closure']!=910 or (W/'root_portable01.stderr').stat().st_size:raise ValueError('portable gate')
c.finish('geometry/primitive_pairs/portable_completion_root_review','ACCEPTED_L036_PORTABLE_COMPLETE_SOURCE_TREATMENT',dict(
 reviewer='root',author='j3_recovery',review=[
 'Read the complete portable checker, reused Archive read interfaces, publication scope and all23 documentary premise occurrences. The mathematical acceptance and frozen stage are externally pinned. Only original documentary pages and installed software/library records are premise-only; every derived proof, array, program, review and comparison remains available payload.',
 'The exact accepted closure has910 logical bindings. The archive authenticates all370 payload objects,13 reused public files and218 explicitly declared premise objects, with exact nonoverlapping pack coverage. Scientific replay has no private-path fallback: missing payload bytes fail the Archive interface.',
 'Fresh root replay independently recomputed all five character totals, eleven mark-table calculations and308 source cells; all37 M11 graphs,70 design comparisons,20 structural joins and2304 GL2(3) products; and the order-four coset algorithm witness. Original discrepancies remain alongside corrected joins.',
 'The complete claim ledger and all twelve group routes match the accepted synthesis. Six meaningful scope/finite damages and the reused codec controls passed. The external representative files remain unverified, and group/library completeness is explicitly retained as a premise.',
 'Freshly built all eight TeX entrypoints and the24-page volume. All23 mathematical page streams and font programs match their accepted parts, and all24 fresh native rasters are byte-identical to the accepted rasters. No target enumeration, new formalization or new compression measurement was performed.'
 ],stage_manifest_sha256='9f63fd60a85394a15224c91517e71f9081ea42f929637c777074e2f44b252cff',transport_sha256='2263fb1a4b9508b744cdb49fdb776e506c46b5ee136bfc8ac0102e762003a741',portable_root_seconds=r['seconds'],complete_fixed_source_mathematics=True,public_registration='Pending concrete registration candidate and root integration.',ordinary_recovery_delta=0,principal_refutation_delta=0))
