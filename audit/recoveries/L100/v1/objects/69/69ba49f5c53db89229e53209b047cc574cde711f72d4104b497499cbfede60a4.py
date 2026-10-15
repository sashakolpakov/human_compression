import hashlib,json
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans');G=S/'geometry/psl3_4';W=G/'source_join_work'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
# Literal native-page transcription, node order is explicitly only a multiset.
sizes={
'2.1':[21,21],'2.2':[210,56],'2.3':[56,280],'2.4':[120,120],'2.5':[210,120],'2.6':[280,280],'2.7':[280,1260],
'3.1':[21,210,56],'3.2':[56,1260,56],'3.3':[120,210,210],'3.4':[56,210,210],'3.5':[1120,120,120],'3.6':[56,210,56],'3.7':[21,105,21],
'4.1':[21,210,56,56],'4.2':[56,1260,21,21],'4.3':[120,1260,56,56],'4.4':[21,1260,56,56],'4.5':[56,1260,21,21],'4.6':[120,1260,21,56],'4.7':[120,1260,21,21],'4.8':[56,21,21,56],'4.9':[56,21,210,56],'4.10':[21,56,56,210],'4.11':[120,120,336,336],
'5.1':[21,56,56,210,21],'5.2':[21,56,56,210,21],'5.3':[21,56,21,56,21],'5.4':[21,56,21,56,21]}
borel=[192,24,36,21,24,8,8,12,4,8,8,3,6,12,3,2,2,2,2,2,2,3,2,2,1,1,1,1,1]
not2t={'2.2','3.2','4.2','5.1','5.2','5.3','5.4'}
intake=S/'corpus106_source_reading_L091_L100_L102/L100_intake.json';x=json.loads(intake.read_text());rows=[]
for q,b in zip([q for q in x['items'] if q['id'].startswith('Diagram-')],borel):
 label=q['detail']['geometry_label'];r=dict(label=label,physical_pages=q['physical_pages'],type_size_multiset=sorted(sizes[label]),printed_borel_order=b,printed_local_2T_marker=label not in not2t,printed_G_conjugacy_fusion_multiplicity=q['detail']['conjugacy_classes_fused'],construction_route=q['detail']['construction_route'],status='SOURCE_TRANSCRIPTION_ONLY_NO_ACTUAL_CLASS_IDENTIFICATION')
 r['native_inputs']=[pin(W/'native'/f'source-{p-6:02d}.png')for p in q['physical_pages'] if p>=7]
 rows.append(r)
assert len(rows)==29 and len(borel)==29
out=dict(status='WORKING_LITERAL_SOURCE_JOIN_INVENTORY',source=pin(S/'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf'),intake=pin(intake),rows=rows,qualifications=['Native pages7–13 were directly viewed. This projection records only type-size multisets, Borel orders, printed local2T markers and fusion multiplicities.','Diagram edge labels, local action kernels, group names and source-to-actual maps remain unpaid. Equal signatures do not identify geometries.','The printed fusion counts refer to G-conjugacy classes fused under Aut(G); the exact type-equivalence convention must be joined to the actual enumeration.','No computed result is required to match a source value. Mismatches must be retained.'],source_credit=0)
(W/'diagram_inventory01.json').write_text(json.dumps(out,indent=2)+'\n');print('29 source rows saved')
