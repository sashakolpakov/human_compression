import hashlib,json,shutil
from pathlib import Path
from pypdf import PdfReader,PdfWriter
P=Path(__file__).resolve().parent;S=P.parents[1];R=S.parents[1]/'math_compression';roots={'study':S,'public':R}
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
shutil.copy2(P/'author_check01/native/principal.pdf',P/'principal.pdf');shutil.copy2(P/'author_check01/native/text.txt',P/'native_expected.txt')
writer=PdfWriter();parts=[];offset=0
for id,source,p in [('principal',None,P/'principal.pdf')]+[(c['id'],c['pdf'],roots[c['pdf']['namespace']]/c['pdf']['path'])for c in json.loads((P/'components.json').read_text())['components']]:
 pdf=PdfReader(p);writer.append(pdf,import_outline=False);r=dict(id=id,first_page=offset+1,pages=len(pdf.pages));offset+=len(pdf.pages)
 if source:r['source']=source
 else:r['local_path']='principal.pdf'
 parts.append(r)
with (P/'complete_proof.pdf').open('wb')as f:writer.write(f)
save(P/'complete_proof_routes.json',dict(parts=parts,total_pages=offset,operation='Concatenation of the exact synthesis and all eight accepted manuscript PDFs. All TeX and full prior review/dependency closures remain separate acquired artifacts.'))
save(P/'visual_review.json',dict(principal_pages_directly_viewed=[1,2,3],source_native_page_rechecked=24,component_native_pages='Already directly viewed under each acquired distinct review; not redundantly rerendered.',complete_proof_join='Every extracted page is compared to its exact accepted input PDF by check.py.',layout='Clean final two-pass build: no overfull or reference warning.'))
save(P/'development.json',dict(author='l044_resume',status='AUTHOR_COMPLETE_AWAITING_DISTINCT_PRINCIPAL_REVIEW',new_mathematics='Principal joins and q81 inherited-result application only; all eight proof components already accepted.',new_searches=0,source_audit_assistance='publication_recovery independently checked principal/Section7 limits and exact Topic E q81 interface; not whole mathematical review.',history='Three failed patch-context attempts changed no frozen files; final current principal was built once in author_check01 and all three pages directly viewed. Source_contract01 and scope03 remain unchanged historical records.',owned_processes=[],whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0))
(P/'README.rst').write_text('Chiral constructions and regular subgroups in dimension three\n==============================================================\n\nThis is the complete corrected principal synthesis of L027, in the fixed\n25-page 2022 author edition. principal.tex is the reader overview.\ncomplete_proof.pdf appends all eight accepted full mathematical papers;\ncomponents.json retains their exact TeX, finite evidence and reviews.\n\nsource_map.json routes every numbered statement, all table rows and the\nremaining source clauses. retained_inputs.json distinguishes earlier\nsource-attributed classifications and missing census outputs from our\naccepted proofs. The PSU3(17) component proves three positive pairs only.\nThe quoted PSL2(81) negative is corrected by the accepted pointed theorem.\n\nReplay: global Python check.py --study STUDY --repo PUBLIC --out FRESH\n--render. This checks bindings, exact interfaces, all concatenated proof\npages, five damaged scopes and four optimization guards. It does not\nrerun already reviewed group censuses or count one whole original.\n\nFull source articles/text/renders are documentary hash-only for public\ntransport. Root alone owns admission, publication and any catalogue change.\n')
D=S/'corpus106_L027_principal_v1'
if D.exists():raise ValueError('immutable destination exists')
D.mkdir()
for p in sorted(P.iterdir()):
 if p.is_file() and p.suffix in ('.py','.json','.tex','.pdf','.txt','.rst'):shutil.copy2(p,D/p.name)
shutil.copytree(P/'author_check01',D/'author_receipt')
exports=[dict(path=str(p.relative_to(D)),**pin(p))for p in sorted(D.rglob('*'))if p.is_file()]
save(D/'manifest.json',dict(status='AUTHOR_COMPLETE_CORRECTED_L027_PRINCIPAL_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(path=str(D/'manifest.json'),**pin(D/'manifest.json'),exports=len(exports),complete_proof_pages=offset)))
