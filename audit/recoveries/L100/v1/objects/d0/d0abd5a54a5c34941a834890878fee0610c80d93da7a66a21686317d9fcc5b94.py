import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
B=Path(__file__).resolve().parent;G=B.parent;S=G.parents[1];W=B/'final_stage01';P=G/'baer_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base)) if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable destination exists');P.mkdir()
    for name in ['probe_engine.py','verify.py','controls.py','check.py','baer.tex','README.rst','source_clauses.json']:shutil.copyfile(W/name,P/name)
    for name in ['inputs','expected','native_source']:shutil.copytree(W/name,P/name)
    shutil.copyfile(B/'native_final01/baer.pdf',P/'baer.pdf');shutil.copytree(B/'native_final01',P/'native_author')
    H=P/'history';H.mkdir()
    for name in ['certificate.py','certificate_v2.py','certificate_v3.py','run_probe.py','run_probe_v2.py','controls.py','baer.tex','plan.rst','source_clauses.json','probe_request01.json','probe_request02.json','probe_request03.json','probe_request04.json','ordering_correction.diff','ordering_correction.json','ordering_control.py','ordering_control_report.json','join_diagnosis01.json','join_diagnosis02.json','join_diagnosis03.json','diagnose_join01.py','native_initial_failure.json','owner_checkpoint02.json']:
        if (B/name).exists():shutil.copyfile(B/name,H/name)
    for name in ['probe01','probe01_receipt','probe02','probe02_receipt','controls01','verify01','final_controls01']:shutil.copytree(B/name,H/name)
    for name in ['probe02_terminal.stdout','probe02_terminal.stderr']:shutil.copyfile(B/name,H/name)
    shutil.copyfile(Path(__file__),P/'freeze.py')
    roots={
      'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
      'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
      'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86',
      'palette_serialization_v1':'5399e45468b83a49e0d2750a2087cb8e6006919b08548d0434b5195ed550eff3',
      'palette_serialization_review_v1':'6a09697960e322a8d10bcabc9354504f8e0b1e6c17a9ed485ab36c25aa6ab96a',
      'source_join_component_v2':'2e69c5d047fa7d15fb8d101090a78c18a69f3100db2aeb111abc107878639ffb',
      'source_join_review_v2':'1cbc91ca8ba73e421cf2e6412b20654a5057f7545ffc232d29566d169f41fd00'}
    deps={};rootrows=[]
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'binding '+str(p))
        if str(p) in deps:need(deps[str(p)]==r,'conflicting binding')
        deps[str(p)]=r
    for name,h in roots.items():
        R=G/name;M=R/'manifest.json';need(row(M)['sha256']==h,'acquired root');rootrows.append(row(M,S));add(M)
        for r in read(M)['exports']:add(R/r['path'],r)
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute() else S/p,r)
    aliases=[]
    for copy,original in [('inputs/projective_model.json',G/'constructions_component_v1/expected/model.json'),('inputs/group_elements.json',G/'palette_serialization_v1/derived/group_elements.json'),('inputs/catalogue_model10.json',G/'palette_serialization_v1/derived/model10.json'),('inputs/source_projection.json',G/'palette_serialization_frozen01/fresh/source_projection.json'),('inputs/baer_orbits.json',B/'probe01/baer_orbits.json'),('expected/certificate.json',B/'probe02/certificate.json'),('probe_engine.py',B/'certificate_v3.py')]:
        r=row(original);need(row(P/copy)['sha256']==r['sha256'],'exact input copy');aliases.append(dict(original=str(original),copy=copy,bytes=r['bytes'],sha256=r['sha256']));add(original)
    for name in ['probe_request03.json','probe_request04.json']:
        request=read(B/name);add(B/name)
        for r in request['inputs']:add(Path(r['path']),r)
    for r in read(B/'probe02_receipt/receipt.json')['inputs']:add(Path(r['path']),r)
    for p in B.rglob('*'):
        if p.is_file() and not p.is_relative_to(W) and not p.is_relative_to(B/'native_final01') and '__pycache__' not in p.parts:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    for p in [Path(sys.executable),Path('/opt/homebrew/bin/pdflatex'),Path('/opt/homebrew/bin/gs')]:add(p)
    save(P/'input_aliases.json',aliases);save(P/'acquired_roots.json',rootrows)
    save(P/'roles.json',dict(author='publication_recovery',source_mathematics='Gottschalk--Leemans Geometry3.3, fixed Halle preprint',root_input='Scope/retained-input requests; prelaunch mask-sort ordering error identified in code review; permission for changed finite map probe. No supplied new frame lemma or corrected-incidence proof.',prior_roles='Author of acquired construction/source joins; those have separate root distinct reviews. Root supplied other acquired group/census inputs as recorded there.',distinct_review='pending',priority_claim=False))
    save(P/'source_routes.json',dict(source=read(P/'source_clauses.json'),scope=['Geometry3.3 recipe on physical19: all three printed relations transcribed','Printed third relation degree18; one nonextendible flag certified in each of three orbits','Corrected third relation requires a common Baer from the selected orbit','All three corrected incidence/action maps to accepted catalogue10; degree6','Complete360 input by projective frames and literal set checks'],principal_classification_refuted=False,other_claims_pending=['Other source constructions','Abstract Borel/parabolic/kernel/Aut/Cor group names','Concrete doubling and remaining truncation/fusion joins','Whole-source disposition'],source_credit=0,whole_source_credit=0,measurement_credit=0,question_credit=0,Lean_credit=0))
    save(P/'native_review.json',dict(proof_pages=3,proof_pages_directly_viewed=True,source_physical_pages=[19],source_native_directly_viewed=True,clean_log=True,source_edition='fixed Halle preprint; journal uncollated'))
    save(P/'development.json',dict(first_probe='Complete360 input saved; uncured printed incidence map join failed. No negative source inference from failure alone.',root_prelaunch_fix='Tuple-combination order differs from numerical mask order; exact correction/control preserved.',second_probe='Reused360 input, corrected third relation, all3 complete maps; terminal0 in1.316s.',current_verifier='Verifies stored maps; no map discovery or seven-subset scan.',native_failure='One output-directory setup error before successful two-pass native build; preserved.',all_live_handles_terminal=True))
    final=[]
    for p,r in sorted(deps.items()):
        p=Path(p)
        final.append({**r,'path':str(p.relative_to(S)) if p.is_relative_to(S) else str(p),'namespace':'study' if p.is_relative_to(S) else 'runtime'})
    save(P/'dependencies.json',final)
    exports=[row(p,P) for p in sorted(P.rglob('*')) if p.is_file()]
    save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_BAER_CORRECTION_COMPONENT_V1',exports=exports,dependencies=len(final)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(final)),indent=2))
if __name__=='__main__':main()
