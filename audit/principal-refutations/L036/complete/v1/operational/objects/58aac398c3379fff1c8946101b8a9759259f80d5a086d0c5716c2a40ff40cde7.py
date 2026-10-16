from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/primitive_pairs';A=P/'m11_application';O=P/'m11_application_root01'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/primitive_pairs/m11_application');c.packet('geometry/primitive_pairs/m11_graph_memory_root_review')
for row in json.loads((A/'dependencies.json').read_text()):c.binding(row)
for p in O.iterdir():
 if p.is_file():c.add(p)
report=json.loads((O/'report.json').read_text())
if report['status']!='PASS_L036_M11_GRAPHS_AND_SOURCE_CORRECTIONS'or len(report['native_pages'])!=6:raise ValueError('replay')
for p in ['source-page07.png','source-page08.png']:c.add(A/p)
c.add(Path(__file__))
c.finish('geometry/primitive_pairs/m11_application_root_review','ACCEPTED_L036_M11_TABLES_WITH_FOUR_ORIENTATION_CORRECTIONS',dict(
 reviewer='root',author='j3_recovery',review=[
 'Read the entire finite certificate verifier, exact source transcription, original and corrected joins, literal matrix isomorphism verifier and all six proof pages. Independently read source PDF pages1through5 and directly viewed source Tables3and4, then all six freshly rendered proof pages.',
 'The finite maximal-subgroup lists are closed under the actual generators and each named class orbit is connected. The supplied partition of all47586 unordered pairs is closed and each part connected, proving precisely37 pair orbits. All6278 right cosets and28498 uniform-design subset counts were independently checked.',
 'Graph incidence is literal common-element incidence. Inversion transports right cosets to left cosets preserving types, so it cannot account for a diameter exchange. The verifier computes eccentricity at one vertex per transitive type and girth by multi-source search in the graph with a root removed; transitivity puts both roots on a globally shortest cycle.',
 'Actual intersection conjugators join20 structural imports to their accepted literal subgroup generators. The order48 subgroup is identified with GL2(3) by a complete48-element bijection checking all2304 products. This uses no new subgroup classification.',
 'The source defines point/line diameter at G1/G2 in Section2, physical page3. With that convention Table3 rows12and18 require[4,2,3] androws23and35require[4,3,3]. The original opposite triples and failed original join remain intact. All70 design entries are unchanged; their point orientation is separately tracked.',
 'The subdivided K11 interpretation independently verifies row35, and K12 verifies row23. Two pairs of indistinguishable printed profiles retain both permissible orbit assignments. Complete incidence in omitted rows31and32 is documented under the source literal design definition and conventional proper-block restriction.',
 'Fresh root replay passed61 exact dependencies,20 structural joins,seven damaged finite certificates, a damaged printed design entry, optimization guards and six exact native pages. No scientific target rerun. The component cites Section3 where it should say Section2/page3; this textual citation correction is required in the final synthesis/publication edition and does not change any mathematics.'
 ],whole_source_disposition='Pending complete-source synthesis and publication; this component supplies Tables3and4 only.',target_reexecuted=False,source_geometry_rows=37,source_design_rows=70,corrected_rows=[12,18,23,35],source_credit=0))
