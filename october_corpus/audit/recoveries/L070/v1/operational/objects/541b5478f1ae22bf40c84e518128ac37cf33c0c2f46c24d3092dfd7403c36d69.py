import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');sys.path.insert(0,str(S/'reboot_20261013'))
from component_review_records import finish,pin
C=S/'geometry/chiral_atlases';W=C/'publication_work';ST=W/'stage02';D=ST/'audit/recoveries/L070/v1';R=Path('/Users/sasha/medusa/math_compression');F=W/'portable_root02'
m=json.loads((D/'manifest.json').read_text());t=json.loads((D/'transport.json').read_text());r=json.loads((F/'report.json').read_text())
assert pin(D/'manifest.json')['sha256']=='af38e0076f2ea564b1141a2530aa37225648be33c178e905c6be2cecc44eee82'
assert pin(D/'transport.json')['sha256']=='a94d6261bb207383b0b12158bce101150da1cd5640c756a0b1c628718fffd759'
assert r['status']=='PASS_PUBLIC_L070_COMPLETE_CLOSURE' and r['new_group_calls']==0 and r['complete_proof_pages']==41
bindings={}
for x in m['exports']:
 p=ST/x['path'];q=pin(p);assert(q['bytes'],q['sha256'])==(x['bytes'],x['sha256']);bindings[str(p)]=q
for x in t['existing_public_files']:
 p=R/x['path'];q=pin(p);assert(q['bytes'],q['sha256'])==(x['bytes'],x['sha256']);bindings[str(p)]=q
for p in [D/'manifest.json',W/'ready.json',W/'publication_files.json',W/'integration02/admission_proposal.json',W/'portable02/report.json',Path(__file__),*sorted(p for p in F.rglob('*')if p.is_file())]:bindings[str(p)]=pin(p)
finish('geometry/chiral_atlases/publication_operational_root_review','ACCEPTED_PUBLIC_L070_COMPLETE_CLOSURE_ADAPTER_V1',{
 'reviewer':'/root','adapter_authors':['/root/l044_resume','/root/l070_publication'],
 'independence':'Root read the complete storage codec, portable reader, boundary policies, proposal and source guide; root suggested explicit premise and standalone-manuscript checks. The implementation and final one-line report repair were authored by the listed agents. This is an operational review of an already accepted mathematical disposition, not another independent group census.',
 'root_portable_report':pin(F/'report.json'),'stage_manifest':pin(D/'manifest.json'),'transport':pin(D/'transport.json'),
 'scientific_acceptance':t['root_acceptance'],'proposal':pin(W/'integration02/admission_proposal.json'),
 'inspection':['Every payload object is read through complete encoded and decoded identities. New packs have exact nonoverlapping coverage; reused public objects are tracked files and decoded without private fallback.','The accepted root closure contains exactly the declared logical paths, with no omitted mathematical input. Individually listed original documents, rasters and installed software are explicit premises. HTTP acquisition receipts and the tiny original Magma companion are retained as payload.','Thirteen small exact inputs are materialized, both unchanged application readers are executed, and their whole outputs are compared. Only actual rebased selected-root paths in the vertex record are normalized after exact content checks.','All sixteen complete manuscript TeX/PDF pairs and source ledger are joined to accepted bytes. All forty-one native page content streams agree with the complete volume; the four-page synthesis is included once. Fresh synthesis text and all four rasters agree exactly.','The failed first portable attempt is preserved. Its TypeError was confined to final pack-byte summation; stage02 changes that report expression to iterate dictionary values, leaving transport and scientific bytes unchanged. The new complete run passed.'],
 'fresh_validation':{'session':51969,'seconds':r['seconds'],'logical_files':84412,'payload_objects':59720,'premise_objects':1168,'decoded_bytes':7402329545,'complete_manuscripts':16,'complete_proof_pages':41,'source_clauses':46,'fresh_native_pages':4,'selected_files':13,'new_group_calls':0,'new_censuses':0,'storage_controls':r['storage_controls'],'admission_controls':r['admission_controls']},
 'disposition':'Accept the exact public transport and its bounded unchanged scientific replay. The proposed ordinary source recovery remains subject to catalogue registration, final repository checks and publication. This decision alone changes no public count.',
 'scope_limits':['No new mathematical compression measurement.','No newly solved open conjecture or complete Lean formalization.','No repeated historical census or proof of the retained classification and software premises.'],
 'binding_acquisition':'The fresh checker validated all transport and native content. Every staged export and every reused public stored file was rehashed again on sealing; selected fresh outputs and handoff files are separately bound.'
},list(bindings.values()))
