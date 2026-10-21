from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/primitive_pairs'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/primitive_pairs/table_application');c.packet('geometry/primitive_pairs/table_request02_root_review')
O=P/'table_application_root01'
for p in O.iterdir():
 if p.is_file():c.add(p)
c.add(Path('/private/tmp/l036-table2.png'));c.add(Path(__file__))
r=json.loads((O/'report.json').read_text())
if r['status']!='PASS_L036_SIX_OUTER_TOTALS_AND_SUBORBIT_TABLES' or r['printed_numeric_cells']!=308 or r['numeric_cell_changes']!=0 or r['M23_row_label_corrections']!=2:raise ValueError('exact application replay')
if len(r['controls']['rejected_mathematical_damages'])!=7 or not r['controls']['detected_printed_cell_damage']:raise ValueError('damage controls')
c.finish('geometry/primitive_pairs/table_application_root_review','ACCEPTED_L036_SIX_OUTER_TOTALS_AND_SUBORBIT_TABLES',dict(
 reviewer='root',author='j3_recovery',
 review=[
 'Read the complete four-page mathematical application and all arithmetic, sparse mark decomposition, source extraction, source joining, damage controls and replay code. Viewed all four fresh native proof pages and original physical pages6,9,10,11.',
 'The accepted normalizer and Burnside formulas apply to the full automorphism group. Normalizers, fixed subgroup counts and squared-element terms give166,334,546,339,443,4074 for M12,J2,J3,HS,McL,He. Subgroup classification and table/fusion completeness remain explicit borrowed premises.',
 'The triangular mark-row product gives an exact nonnegative decomposition of each product G-set. Stabilizer orders then give all suborbit lengths. Exhausting the simultaneous equal-degree row/column joins recovers308 original numerical cells without changing any entry; source superscripts are multiplicities.',
 'The number of ambient conjugates of L contained in M is m(M,L)|M|/|N_G(L)|. In M23, class201 and class33 give1*40320/(16*2520)=1. This produces an actual normal subgroup of order16, and complete cyclic fusion plus15 involutions proves that it is elementary abelian.',
 'The borrowed two-shape list and simplicity of L3(4) distinguish the two index253 subgroups: L3(4):2 cannot have a normal16-subgroup. Direct inspection of native Table7 confirms the two printed labels are interchanged. Coincident permutation characters are not treated as an embedding identifier.',
 'The upper-triangle38/268 quantities retain both orientations of certain diagonal double cosets. Inner unordered totals37/255 and full-automorphism M12 total166 are distinct quantities; the application explains and computes each.',
 'Fresh root replay checked214 exact dependencies, all numerical cells and six new outer counts; seven altered mathematical inputs were rejected, altered printed data remained a discrepancy, both Python optimization modes rejected, and all four fresh native pages matched the retained version.'
 ],
 printed_numeric_cells=308,numeric_cell_changes=0,M23_row_label_corrections=2,
 outer_totals=dict(M12=166,J2=334,J3=546,HS=339,McL=443,He=4074),
 scope='Tables1,2,5–8 and preliminary counts only, with explicit library premises. Tables3–4, the37 M11 geometries and complete source synthesis remain unpaid. No repeated Ru principal-refutation credit, new conjecture, Lean or compression credit.',
 GAP_launched=False,new_target_calls=0,new_principal_refutation_credit=0,source_completion_credit=0))
