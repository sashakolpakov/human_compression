#!/usr/bin/env python3
"""Bind executed label/universal-order adapter artifacts; primary full texts excluded."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=['phase22_N009_table_labels.md','phase22_N009_atlas_extract.py','phase22_N009_atlas4_extract.py','phase22_N009_atlas_fetch_plan.json','phase22_N009_atlas4_fetch_plan.json','phase22_N009_atlas_library.json','phase22_N009_atlas_library.g','phase22_N009_atlas4_library.json','phase22_N009_atlas4_library.g','phase22_N009_facet_input.g','phase22_N009_facet_check.g','phase22_N009_facet_check.log','phase22_N009_facet_matches.json','phase22_N009_atlas_duals.json','phase22_N009_rank5_labels_check.g','phase22_N009_rank5_labels_check.log','phase22_N009_rank5_facet_matches.json','phase22_N009_rank4_atlas_duals.json','phase22_N009_universal_input.g','phase22_N009_universal_check.g','phase22_N009_universal_check.log','phase22_N009_universal_orders.json','phase22_N009_atlas_presentation_orders.json','phase22_N009_universal5_input.g','phase22_N009_universal5_check.g','phase22_N009_universal5_check.log','phase22_N009_universal5_orders.json','phase22_N009_atlas4_presentation_orders.json','phase22_N009_table6_rows.json','phase22_N009_table_compare.py','phase22_N009_table_compare.json','phase22_N009_table_labels_build.py']
for n in ['facet_check','rank5_labels_check','universal_check','universal5_check']:
 text=(R/('phase22_N009_'+n+'.log')).read_text();assert 'PASS' in text and 'Error,' not in text
retained=['phase21_rank4_census.accepted.json','phase21_kernel_census.g','phase21_kernel_ladder.md','phase17_k1_classification.md','phase21_N009_presentations.md','phase22_N009_lemma_adapters.md']
# A data-only duplicate must agree exactly with the retained census input.
x=(R/'phase22_N009_facet_input.g').read_text();assert x.startswith('accepted22:=') and x.endswith(';;\n')
assert json.loads(x[len('accepted22:='):-3])==json.loads((R/'phase21_rank4_census.accepted.json').read_text())
report=json.loads((R/'phase22_N009_table_compare.json').read_text());assert report['rank4']['all_labels_match'] and report['rank5']['all_labels_match'] and report['finite_universal_amalgams_verified']==106
libraries=[json.loads((R/f'phase22_N009_atlas{s}_library.json').read_text()) for s in ['', '4']]
assets=[]
for lib in libraries:
 for a in lib:
  f=R/'sources'/a['primary_snapshot'];assert sha(f)==a['primary_sha256']
  assets.append(dict(path='sources/'+a['primary_snapshot'],url=a['url'],sha256=sha(f),excluded_from_export=True,scope='Primary named mathematical object; ordered permutations and presentation parsed as data.'))
for file,url in [('phase22_atlas_FAQ.html','https://abstract-polytopes.com/atlas-FAQ.html'),('phase22_atlas_home.html','https://www.abstract-polytopes.com/'),('phase17_gomi_loyola2018.pdf','https://cdm.ucalgary.ca/article/download/62475/46803'),('phase17_gomi_loyola2018.txt','https://cdm.ucalgary.ca/article/download/62475/46803')]:
 assets.append(dict(path='sources/'+file,url=url,sha256=sha(R/'sources'/file),excluded_from_export=True))
certificate=dict(schema_version=1,date='2026-10-10',status='PASS author exact checks; independent review separate',scope='All Table 6 marked labels/counts and all finite universal orders; one infinite structural input retained; no new whole-paper or priority claim.',rank4=dict(ordered=199,self_dual=11,classes=105,source_rows=99,facet_isomorphisms=398),rank5=dict(candidates=127,ordered=15,self_dual=1,classes=8,source_rows=8,actual_IP_meets=130048,facet_isomorphisms=30),atlas=dict(rank3_markings=56,rank4_markings=11,unique_complete_presentation_orders=67,actual_IP_meets=6400,scope='Exact named models, not an Atlas completeness assumption'),finite_universal_orders={'1024':101,'2048':5},infinite_universal_input='Quoted McMullen–Schulte decomposition, N009 Theorem5.3.',source_orientation_qualification='Four printed {4,16,4} rows use dual vertex-figure marking {16,4}; unchanged suffixes/counts; visually checked printed p16.',primary_assets=assets,artifacts=[dict(path=n,sha256=sha(R/n)) for n in files],retained_dependencies=[dict(path=n,sha256=sha(R/n)) for n in retained],trust_boundary=['GAP finite permutation/subgroup algorithms','GAP complete Todd–Coxeter coset enumeration','NQ universal nilpotent quotient computation','Reviewed support/completeness theorems in retained notes','Primary Atlas mapping between fixed canonical labels and explicit marked permutations','Retained infinite McMullen–Schulte decomposition'])
(R/'phase22_N009_table_labels_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
files.append('phase22_N009_table_labels_certificate.json')
manifest=dict(schema_version=1,scope=certificate['scope'],original_files=[dict(path=n,sha256=sha(R/n)) for n in files],retained_dependencies=certificate['retained_dependencies'],excluded_primary_assets=assets)
(R/'phase22_N009_table_labels_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'PASS','original_files_including_manifest':len(files)+1,'proof_sha256':sha(R/'phase22_N009_table_labels.md'),'certificate_sha256':sha(R/'phase22_N009_table_labels_certificate.json'),'manifest_sha256':sha(R/'phase22_N009_table_labels_manifest.json')}))
