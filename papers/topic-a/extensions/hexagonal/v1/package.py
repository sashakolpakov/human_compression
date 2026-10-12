"""Mechanical final assembly metadata and lossless reader bundles; no new mathematics."""
from pathlib import Path
from pypdf import PdfReader,PdfWriter
import hashlib,json,shutil
P=Path(__file__).resolve().parent;S=P.parent;PUB=S.parents[1]/'math_compression'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,d):(P/n).write_text(json.dumps(d,indent=2)+'\n')
# Copies of accepted review packets are immutable provenance, not new adjudications.
accept=['topic_A_L003_bounded_root_adoption','topic_A_L003_shared_structures_root_review','topic_A_L003_structural_root_review','topic_A_L003_order768_independent_review','topic_A_L003_order768_root_adoption','topic_A_L003_correlation_root_review']
routes=load=json.loads((P/'copy_routes.json').read_text());routes=[r for r in routes if not r['destination'].startswith('acceptance/')]
for folder in accept:
 src=S/folder;dest=P/'acceptance'/folder;dest.mkdir(parents=True,exist_ok=True);m=json.loads((src/'manifest.json').read_text())
 for e in m['exports']+[dict(path='manifest.json',bytes=(src/'manifest.json').stat().st_size,sha256=sha(src/'manifest.json'))]:
  q=dest/e['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/e['path'],q);routes.append(dict(source=folder+'/'+e['path'],destination=str(q.relative_to(P)),bytes=e['bytes'],sha256=e['sha256']))
dump('copy_routes.json',routes)
bundles={'common_complete': [('retained/umbrella.pdf','Complete existing common paper'),('inputs/base/shared_supplement.pdf','Rotation and affine-period common supplement'),('inputs/shared_structures/shared_structures.pdf','Shared normal factors and splittings')], 'application_complete':[('hexagonal_extensions.pdf','Literal presentations and corrected source contract'),('inputs/finite_structures/structural_completion.pdf','Complete finite structural proofs'),('inputs/correlations/correlation_reduction.pdf','Complete correlation reductions'),('inputs/order768/order768.pdf','Complete order-768 and genus-four proof')]}
docs=[]
for name,files in bundles.items():
 writer=PdfWriter();offset=0;parts=[];expected=[]
 for f,title in files:
  pages=PdfReader(P/f).pages;writer.add_outline_item(title,offset)
  for page in pages:writer.add_page(page,excluded_keys=('/Annots',));expected.append(page.extract_text())
  parts.append(dict(path=f,bytes=(P/f).stat().st_size,sha256=sha(P/f),pages=len(pages),first_bundle_page=offset+1));offset+=len(pages)
 writer.write(P/(name+'.pdf'))
 actual=[q.extract_text() for q in PdfReader(P/(name+'.pdf')).pages];assert expected==actual
 docs.append(dict(id=name,path=name+'.pdf',parts=parts,pages=len(actual),page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in actual],role='Reading convenience: exactly the full constituent pages, never an additional counted manuscript',links='Per-source annotations removed from convenience copy to avoid invalid cross-document destinations; original constituent PDFs remain byte-identical and retain all original links.'))
dump('bundle_map.json',dict(bundles=docs,engine='pypdf PdfWriter.add_page, no retypesetting or source-text edits',canonical_measurement_boundary='Complete native constituent PDFs once each; bundle is an exactly text-equivalent alternative, never additive.',no_measurements=True))
# Current dispositions: one combined historical row is replaced by its nine precise clauses.
claim=json.loads((P/'claim_map.json').read_text());rows=[]
for r in claim['rows']:
 if r['id']=='Section3_correlations4_5':
  for sub in r['subclauses']:rows.append(dict(id=sub['id'],source_pages=sub['pages'],status=sub['status'],route='inputs/correlations/correlation_reduction.tex: '+sub['route'],accepted_review='acceptance/topic_A_L003_correlation_root_review/manifest.json',predecessor_id=r['id'],whole_source_admission_here=False))
 else:rows.append(r)
assert len(rows)==125 and len({r['id'] for r in rows})==125
dump('source_map.json',dict(status='COMPLETE_CORRECTED_CONTRACT_AUTHOR_ASSEMBLY_PENDING_REVIEW',source_id='L003',predecessor_dispositions=117,current_dispositions=125,positive_table_rows=73,rows=rows,full_original_accepted=False,new_question_credit=0))
# Exact inherited scientific and source files, kept as references instead of remeasured copies.
old=json.loads((S/'topic_A_L121_measurement_inputs/precount/documents.json').read_text())['documents']
dump('unchanged_A9_documents.json',{'documents':old,'qualification':'All nine source PDFs and first eight scientific applications retain their exact current bytes. The old A9 eleven-page application remains historical; the whole one-page adapter plus moved common bodies replace it. Code PDFs remain incomplete historical alternatives, not a whole enlarged programme representation.'})
dump('scope.json',dict(status='AUTHOR_COMPLETE_CORRECTED_SOURCE_ASSEMBLY_PENDING_DISTINCT_REVIEW',source_id='L003',source_pages=21,predecessor_rows=117,current_rows=125,positive_rows=73,structures=dict(previous_named=29,new_shared=7,new_finite_printed=34,new_corrected_nonsplit=1,order_refutations=2),main_source_corrections=['T5.8 full order5184000','T5.10 full order497664','12 ordinary local-period collapses','T8.11 literal final word not a torus period; actual localorder504/kernel determinant84','T4.8 printed splitting false; corrected nonsplit stage','Diagram4 rank-four marking needs d in addition to t,a,b'],source_limits=['Earlier Tables1/2 and Theorems3.1/3.2/3.3 retained with source attribution','Diagram5 flag-transitivity/existence remains the explicitly experimental source claim','No unqualified converse from presentation or parity alone','Bounded failed searches are not nonexistence proofs','Problems9.1/9.2 and Conjectures9.1/9.2/9.3 do not yield new question credit'],whole_common_parts=[23,14,4],L121_current_application_pages=1,L003_complete_application_parts=[7,4,4,2],unchanged_old_application_pages=45,required_companions_complete=True,software_inclusive_factor=None,measurements=None,new_Lean=0,inherited_partial_Lean='Six countermodel declarations inherited with the L121 proof; older complete A formal inventory retained separately and not rerun.',roles=dict(base_and_35_and_correlations='enumeration_review authorship; distinct root acceptances',seven_shared='enumeration_volume authorship; distinct root acceptance',order768='root authorship; distinct enumeration_volume review and root adoption',assembly='enumeration_volume; final migration and whole-source review pending'),whole_source_credit=0,new_question_credit=0))
print('payload routes',len(routes),'bundles',[(x['id'],x['pages']) for x in docs])
