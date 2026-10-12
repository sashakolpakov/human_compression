#!/usr/bin/env python3
"""Assemble private documentation metadata from the committed baseline."""
from pathlib import Path
import hashlib,json,shutil
from pypdf import PdfReader
H=Path(__file__).resolve().parent

def bind(path, label=None):
    b=path.read_bytes();return dict(path=label or str(path),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(name,obj):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    base=json.loads((H/'baseline.json').read_text()); rows={r['path']:r for r in base['files']}
    docnames=['README.rst','audit/protocol.tex','audit/protocol.pdf']
    history={'README.rst':'audit/documentation/v1/previous/README.rst','audit/protocol.tex':'audit/documentation/v1/previous/protocol.tex','audit/protocol.pdf':'audit/documentation/v1/previous/protocol.pdf'}
    pagehashes=[hashlib.sha256((p.extract_text()or'').encode()).hexdigest() for p in PdfReader(H/'replacements/audit/protocol.pdf').pages]
    boundary=dict(status='PRIVATE_DOCUMENTATION_CANDIDATE',base_commit=base['commit'],
                  active_originals=106,measured_originals=51,mathematical_pending_originals=54,
                  editorial_original_ids=['L022'],archived_originals=55,current_topics=19,
                  accepted_written_factors=19,accepted_conditional_factors=51,
                  software_inclusive_factor=None,pooled_factor=None,whole_source_formalized=False,
                  no_new_mathematical_or_numerical_admission=True,public_writer='root',
                  old_nonmain_ASTs=base['nonmain_verifier_functions'],
                  preserved_scripts=[rows[k] for k in ['scripts/build_papers.py','scripts/check_programme51.py']],
                  historical_document_routes=history,
                  protocol_pages=len(pagehashes),protocol_page_text_sha256=pagehashes,
                  originalREADME_bytes=rows['README.rst']['bytes'],replacementREADME_bytes=(H/'replacements/README.rst').stat().st_size,
                  protocol_scope='Current policy and definitions, not a replacement mathematical or numerical proof.')
    put('boundary.json',boundary)
    mapping=[]
    for name in docnames:mapping.append(dict(proposal_path='replacements/'+name,public_path=name,role='replacement_document',**{k:v for k,v in bind(H/'replacements'/name).items()if k!='path'}))
    for name,target in history.items():mapping.append(dict(proposal_path='baseline/'+name,public_path=target,role='historical_document',**{k:v for k,v in rows[name].items()if k!='path'}))
    for source,target in [('proposed/scripts/check_current_documentation.py','scripts/check_current_documentation.py'),('boundary.json','audit/documentation/v1/packet/boundary.json'),('topic_table.json','audit/documentation/v1/packet/topic_table.json'),('proposed/integration/new_guard_functions.py','audit/documentation/v1/packet/new_guard_functions.py')]:
        mapping.append(dict(proposal_path=source,public_path=target,role='new_support',**{k:v for k,v in bind(H/source).items()if k!='path'}))
    put('copy_plan.json',dict(status='PRIVATE_ADDITIVE_DOCUMENTATION_MAPPING',base_commit=base['commit'],files=mapping,public_writes=False,unchanged_science_measurement_and_admission_payloads=True))
    def mapped(role):return [dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])for r in mapping if r['role']==role]
    admission=dict(status='ROOT_REVIEW_REQUIRED',scope='Documentation-only successor after programme51; no new source, mathematical, numerical, question or formal credit.',
                   base_commit=base['commit'],replacement_documents=mapped('replacement_document'),historical_documents=mapped('historical_document'),supporting_files=mapped('new_support'),
                   accepted_programme=[rows[k]for k in ['audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue.json','audit/overview/latest.json','audit/overview/v17/admission.json','audit/overview/v17/packet/results.json']],
                   root_review=None,author_manifest=None,
                   old_nonmain_functions_preserved=128,source_intake_added=0,new_recovery_credit=0,new_question_credit=0,new_formal_credit=0,software_inclusive_factor=None,pooled_factor=None)
    put('admission_template.json',admission)
    put('integration_plan.json',dict(status='ROOT_ONLY_PUBLIC_INTEGRATION_PROPOSAL',current_document_replacements=docnames,historical_documents=history,
      verifier_steps=['Copy every final frozen proposal export and manifest unchanged under audit/documentation/v1/proposal/; bind its manifest in the root admission.','Keep every existing non-main function AST unchanged.','Append the two definitions in new_guard_functions.py.','In main only, replace programme51 = check_programme51() with programme51 = check_programme51_documentation_history().','In main only, add check_current_documentation() after the historical programme51 replay.','Root creates audit/documentation/v1/admission.json with actual distinct/root review, author manifest, and status ROOT_ADOPTED_CURRENT_DOCUMENTATION.','Run normal snapshot with the actual staged docs; no current corpus/catalogue/overview/admission pointer changes.'],
      old_function_bodies_changed=False,old_programme_guard_runs_against_exact_saved_docs=True,
      new_guard_checks_current_docs=True,existing_paper_builder_unchanged=True))
    print('Prepared exact documentation routes:',len(mapping))
if __name__=='__main__':main()
