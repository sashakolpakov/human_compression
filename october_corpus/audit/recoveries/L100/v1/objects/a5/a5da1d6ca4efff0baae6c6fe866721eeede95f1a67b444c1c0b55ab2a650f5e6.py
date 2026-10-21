import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'principal_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable fresh packet');P.mkdir()
    for n in ['assemble.py','check.py','principal.tex','catalogue.tex','README.rst','freeze.py','acquired_roots.json']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native03/principal.pdf',P/'principal.pdf');shutil.copytree(W/'native03',P/'native_author');shutil.copytree(W/'join04',P/'expected')
    H=P/'history';H.mkdir()
    for n in ['native01','native02','join01','join02','join03']:shutil.copytree(W/n,H/n)
    shutil.copyfile(W/'history_assemble01.py',H/'assemble_before_table_escape.py')
    deps={}
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'exact acquired binding '+str(p))
        if str(p) in deps:need(deps[str(p)]==r,'binding conflict '+str(p))
        deps[str(p)]=r
    for root in read(W/'acquired_roots.json'):
        M=S/root['path'];add(M,root);R=M.parent
        for r in read(M)['exports']:
            q=Path(r['path']);add(q if q.is_absolute()else R/q,r)
        need((R/'dependencies.json').is_file(),'explicit acquired dependency list '+str(R))
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute()else S/p,r)
    # Bind every actual input/output named by the completed target receipts.
    def literal_pins(obj):
        if isinstance(obj,dict):
            if all(k in obj for k in ['path','bytes','sha256']):
                q=Path(obj['path']);add(q if q.is_absolute()else S/q,obj)
            for x in obj.values():literal_pins(x)
        elif isinstance(obj,list):
            for x in obj:literal_pins(x)
    for n in ['exhaustion_target01','exhaustion_target02','exhaustion_target03_anchor2','exhaustion_target04_anchor1','exhaustion_target05_level_resume','postprocess_target01','incremental_target01','incremental_target02']:
        q=G/n/'receipt.json';add(q);literal_pins(read(q))
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:add(p)
    for p in [S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',G/'typography_advisory_l044/report01.json',G/'typography_advisory_l044/lemma43_transcription02.json']:add(p)
    save(P/'scope.json',dict(source_id='L100',kind='COMPLETE_CORRECTED_PRINCIPAL_RECOVERY_RELATIVE_TO_NAMED_INPUTS',fixed_source='corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf',rank_counts=[7,7,11,4,0],source_clauses=55,bibliography_attributions=47,correction_records=6,retained_input_records=8,principal_refutation=False,journal_collated=False,new_measurements=0,new_Lean=0,new_question_credit=0,public_admission=False))
    save(P/'development.json',dict(native01='Title had accidental undefined control sequence; both failed passes and exact input retained. No scientific execution.',table_escape='Initial assembly used two non-raw Python strings for times in group names; corrected rendering only, initial script and generated table retained.',native02='Seven pages built, two small overfull prose lines; shortened equivalent sentences.',native03='Seven clean final pages, all directly viewed; immediate catalogue.tex included.',finite='Only exact source/interface/receipt joins run; all previously complete group/geometry/graph targets acquired, not repeated.',all_owned_handles_terminal=True))
    save(P/'roles.json',dict(author='publication_recovery',root='Authored earlier rank-two component; reviewed many later finite components. Requested complete source scope and publication. Has not supplied a new synthesis argument; any final review must disclose acquired authorship roles.',l044='Bounded native typography and Lemma4.3 source-only readings; their exact reports are acquired.',f003='Earlier native recipe assistance retained through butterfly component.',distinct_synthesis_review='pending',public_writer='root only'))
    save(P/'publication_interface.json',dict(source_id='L100',disposition='ordinary_recovery',principal_tex='principal.tex',principal_pdf='principal.pdf',native_inputs=['catalogue.tex'],source_claim_register='expected/claim_register.json',literal_catalogue='expected/catalogue.json',execution_join='expected/execution_join.json',bibliography_routes='expected/bibliography_routes.json',acquired_roots='acquired_roots.json',complete_component_proofs='exact manifests and entire dependency closure; public transport must preserve these, without duplicating already published common citations',required_later_gates=['distinct principal acceptance','root adoption','public-only portable review','registration review'],new_measurements=0,new_Lean=0,new_question_credit=0))
    out=[]
    for p,r in sorted(deps.items()):
        p=Path(p);out.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',out);exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()]
    save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_PRINCIPAL_SYNTHESIS_V1',exports=exports,dependencies=len(out)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(out)),indent=2))
if __name__=='__main__':main()
