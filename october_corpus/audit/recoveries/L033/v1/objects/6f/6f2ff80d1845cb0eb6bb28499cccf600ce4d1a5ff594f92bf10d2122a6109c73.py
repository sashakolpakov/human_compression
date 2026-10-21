from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;Q=W.parent;P=Q/'principal_stage01'
def read(p):return json.loads(p.read_text())
def pin(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def main():
    need(not P.exists(),'fresh stage');P.mkdir()
    for n in ['principal.tex','prepare.py','collect.py','joins.py','validate.py','check.py','volume.py','stage.py','README.rst','named_table.tex','minimum_table.tex','complete_proofs.pdf','volume.json']:
        shutil.copyfile(W/n,P/n)
    shutil.copytree(W/'join03',P/'expected');shutil.copytree(W/'native03',P/'native_author');shutil.copyfile(W/'native03/principal.pdf',P/'principal.pdf');shutil.copyfile(W/'small_controls01/report.json',P/'small_report.json')
    H=P/'history';H.mkdir()
    for n in ['join01','join02','acquisition01','acquisition02','native01','native02','volume01','volume02','contract01','small_controls01']:
        shutil.copytree(W/n,H/n)
    deps={r['path']:r for r in read(W/'acquisition03/dependencies.json')}
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:deps[str(p)]=pin(p)
    save(P/'dependencies.json',[deps[k]for k in sorted(deps)])
    save(P/'scope.json',dict(source_id='L033',disposition='COMPLETE_CORRECTED_ORDINARY_RECOVERY_RELATIVE_TO_NAMED_INPUTS',source_clauses=109,component_manuscripts=12,principal_pages=9,complete_reading_pages=50,retained_premises=8,correction_groups=7,source_bibliography_entries=29,new_censuses=0,new_Lean=0,new_measurements=0,new_question_credit=0,principal_refutation=False,distinct_principal_review='pending',public_admission=False))
    save(P/'roles.json',dict(synthesis_author='publication_recovery',new_mathematical_joins=['generic typed right-coset action and exact core kernel','disconnected C-group factors and direct-sum incidence','explicit fourth-type nonextension for D4 sourceExample3.3'],root='Scope requests and acquired component authorship/reviews; final distinct synthesis reviewer must disclose those roles. No new synthesis argument supplied.',l044='Prior period adapter author; optional source-outline read separately, not presumed here.',author_prior_roles='Authored hyperbolic core, names and methods; reviewed cubic, divisor and ninth-square. Not an independent review of the present synthesis.',public_writer='root only'))
    save(P/'development.json',dict(acquisition01='Collector incorrectly placed namespace:absolute relative software pins under study. Exact diagnostic and code retained; explicit namespace resolver repaired this and all37 occurrences resolved to existing exact bytes.',native01='Nine pages, two overfull prose lines and longtable glue diagnostic; exact source retained.',native02='Prose linebreaks repaired; longtable glue diagnostic persisted, table changed to an ordinary complete tabular block.',native03='Nine pages, clean two-pass log; all9 native rasters directly viewed.',volume01='Exact50page text concatenation passed; pypdf emitted annotation count warnings.',volume02='Explicit excluded annotation field still emitted the same pypdf count warnings. Exact output retained.',final_volume='In-memory source annotations explicitly removed before append; unchanged original files; all50 page texts and decoded content streams exact, clean return.',scientific='Only literal metadata joins,12element direct-sum/coset controls and24root D4 checks. No acquired census or weight orbit rerun.',all_owned_handles_terminal=True))
    save(P/'visual_review.json',dict(status='ALL_NINE_NATIVE_PAGES_DIRECTLY_VIEWED',pdf=pin(P/'principal.pdf',P),pages=[pin(p,P)for p in sorted((P/'native_author').glob('page-*.png'))],clean_native_log=True,complete_volume='50 exact acquired page texts/content streams; old components acquired with their own native reviews'))
    save(P/'publication_interface.json',dict(source_id='L033',principal_tex='principal.tex',principal_pdf='principal.pdf',literal_native_inputs=['named_table.tex','minimum_table.tex'],reading_volume='complete_proofs.pdf',source_ledger='expected/claim_register.json',bibliography='expected/bibliography_routes.json',retained_component_interfaces='expected/components.json',disposition='ordinary corrected recovery',required_later_gates=['distinct principal review','root adoption','portable transport acceptance','distinct registration review'],new_measurements=0,new_Lean=0,new_question_credit=0))
    exports=[pin(p,P)for p in sorted(P.rglob('*'))if p.is_file()]
    save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L033_PRINCIPAL_SYNTHESIS_V1',exports=exports,dependencies=len(deps)))
    print(json.dumps(dict(stage=str(P),exports=len(exports),dependencies=len(deps),manifest=pin(P/'manifest.json'))))
if __name__=='__main__':main()
