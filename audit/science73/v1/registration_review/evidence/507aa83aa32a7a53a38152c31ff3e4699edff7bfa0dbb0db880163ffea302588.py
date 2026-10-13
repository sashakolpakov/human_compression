"""Prepare only L038 publication metadata; preserve the complete prior disposition."""
from pathlib import Path
import ast,copy,hashlib,json,shutil,subprocess
S=Path('/Users/sasha/medusa/research/leemans');R=S.parents[1]/'math_compression'
W=S/'reboot_20261013/L038_publication_work';I=W/'integration01';T=W/'stage01'
AUD='audit/science73/v1';REC='audit/recoveries/L038/v1';NAT='papers/recoveries/L038/v1'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,v):
 p=T/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v if isinstance(v,bytes)else(v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()))
def pin(n):
 p=T/n
 if not p.exists():p=R/n
 b=p.read_bytes();return dict(path=n,bytes=len(b),sha256=sha(b))
assert not(T/AUD/'baseline.json').exists()
old=load(R/'audit/corpus/latest.json');oldcat=load(R/old['active_catalogue']['path'])
assert (old['admitted_principal_originals'],old['refuted_principal_originals'],old['handled_mathematical_originals'],old['accessible_pending_complete_recovery'])==(72,1,73,32)
assert 'L038'in old['accessible_pending_original_ids']and 'L038'not in old['admitted_original_ids']
tr=load(T/REC/'transport.json');assert pin(REC+'/transport.json')['sha256']=='a45f08074515fb0dd1c4347c4c955d9d912ebf88f68f4bee77cdd67dcb415d1c'
history={}
for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
 target=AUD+'/previous/'+n;put(target,(R/n).read_bytes());history[n]=pin(target)
commit=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()
put(AUD+'/history_routes.json',dict(base_commit=commit,routes=history,scope='Eight mutable prior documents and pointers; exact F003 and science72 history remains required.'))
put(AUD+'/baseline.json',dict(base_commit=commit,old_catalogue=old['active_catalogue'],history=history,measured_overview=pin('audit/overview/v19/admission.json')))
put(REC+'/scope_routes.json',(I/'scope_routes.json').read_bytes())
guide=(I/'PUBLICATION.rst').read_text().replace('Publication registration is still being prepared.','The publication gate and original register record the final reviewed principal recovery.');put(NAT+'/PUBLICATION.rst',guide)
put(REC+'/checker/portable.py',(S/'reboot_20261013/L038_portable_check.py').read_bytes())
put(AUD+'/reports/portable.json',(W/'portable01/report.json').read_bytes())
# The distinct operational review remains verbatim. Its entire declared evidence is mapped.
directory=S/'corpus106_L038_portable_independent_review';ops={}
paths=[directory/'manifest.json']+[directory/r['path']for r in load(directory/'manifest.json')['exports']]+[S/r['path']for r in load(directory/'dependencies.json')['bindings']]
for p in paths:
 logical=str(p.relative_to(S));b=p.read_bytes();name=REC+'/operational-review/objects/'+sha(b)+p.suffix
 put(name,b);ops[logical]=pin(name)
put(REC+'/operational-review/mapping.json',dict(bindings=ops,scope='Lossless mapping of the complete distinct portable review and all its declared inputs. Private names are historical identifiers, never runtime fallbacks.'))
ad=load(I/'admission_proposal.json');ad.update(status='ROOT_ACCEPTED_COMPONENTS_PUBLICATION_REQUIRES_SCIENCE73_GATE',publication_gate=AUD+'/root_integration.json',source_map=pin(REC+'/scope_routes.json'),portable_report=pin(AUD+'/reports/portable.json'),portable_checker=pin(REC+'/checker/portable.py'),portable_review=pin(REC+'/operational-review/mapping.json'),publication_gate_remaining=True)
put(REC+'/admission.json',ad);adpin=pin(REC+'/admission.json')
reg=dict(status='ROOT_ACCEPTED_COMPONENTS_REGISTRATION_REQUIRES_SCIENCE73_GATE',source_ids=['L038'],admissions=[adpin],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration'])
put(AUD+'/new_original_registration.json',reg);regpin=pin(AUD+'/new_original_registration.json')
unmeasured=sorted(old['measurement_pending_original_ids']+['L038']);handled=sorted(old['handled_mathematical_original_ids']+['L038'])
cat=copy.deepcopy(oldcat);cat.update(status='CURRENT_ACCESSIBLE106_73_RECOVERED_1_REFUTED_31_PENDING',admitted_principal_originals=73,accessible_pending_complete_recovery=31,handled_mathematical_originals=74,handled_mathematical_original_ids=handled,measurement_pending_original_ids=unmeasured,new_proof_credit=1,new_principal_refutation_credit=0,review_revision='Only L038 becomes a complete principal recovery; every other original record is unchanged.',previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=73,refuted=1,handled=74,measured=53,measurement_pending=20,pending=31,editorial=1))
row=next(x for x in cat['entries']if x['original_id']=='L038');previous=copy.deepcopy(row['current_principal_recovery'])
row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[adpin],historical_admission_evidence=previous,principal_contract_admitted=True,all_original_assertions_claimed=False,literal_principal_theorem_recovered=True,measured=False,summary=ad['principal_contract'],retained_inputs=ad['retained_inputs'],auxiliary_type_limits=ad['auxiliary_type_limits'],publication_gate=AUD+'/root_integration.json')
row['next_obligation']='No principal rank-existence case remains. Measurement and further formalization remain deferred until the fixed intake stopping point; exact auxiliary type limits remain declared.'
assert all(a==b for a,b in zip(oldcat['entries'],cat['entries'])if a['original_id']!='L038')
cp='audit/corpus/accessible106/updates/corrected-unmeasured73-catalogue.json';put(cp,cat)
c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_73_RECOVERED_1_REFUTED_31_PENDING_1_EDITORIAL',admitted_principal_originals=73,accessible_pending_complete_recovery=31,handled_mathematical_originals=74,handled_mathematical_original_ids=handled,admitted_original_ids=sorted(old['admitted_original_ids']+['L038']),accessible_pending_original_ids=[x for x in old['accessible_pending_original_ids']if x!='L038'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pin(cp),current_science_registration=regpin)
c['added_admissions'].append(regpin);c.pop('snapshot',None)
sp='audit/corpus/updates/accessible106-corrected-unmeasured73.json';put(sp,c);c['snapshot']=pin(sp);put('audit/corpus/latest.json',c)
sc=load(R/'papers/catalogue_corrected_unmeasured.json')
for p in ad['new_native_manuscripts']:
 sc['entries'].append(dict(id=p['id'],title=p['title'],tex=p['tex']['path'],pdf=p['pdf']['path'],tex_inputs=[],compiler='pdflatex',physical_pages=p['physical_pages'],role='Complete principal recovery component',source_ids=['L038'],topic='Alternating group constructions',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=False,admission=adpin))
sc['original_ids'].append('L038');sc['root_publication_gate']=AUD+'/root_integration.json';put('papers/catalogue_corrected_unmeasured.json',sc)
pa=load(R/'papers/latest_catalogue.json');pa.update(status='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_TWENTY_CORRECTED_UNMEASURED',active_source_catalogue=pin(cp),corrected_unmeasured_scientific_catalogue=pin('papers/catalogue_corrected_unmeasured.json'));put('papers/latest_catalogue.json',pa)
summary=('L038 recovers every rank from 3 to floor((n-1)/2) for all alternating\ngroups of degree n >= 12. The three complete papers contain 17 pages;\nfinite end groups, signed permutation groups and acquired rank contraction\ncover every congruence and endpoint. Three earlier maximal constructions\nremain explicit theorem inputs. Some auxiliary types differ from the source.\nAll 3,200 finite subset-pair checks passed; the infinite arguments are\nwritten proofs. No measurement, new conjecture result or Lean claim is added.\n\n')
for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
 txt=(R/name).read_text()
 for a,b in [('72 accessible originals','73 accessible originals'),('72 reviewed corrected principal recoveries','73 reviewed corrected principal recoveries'),('53 are measured and nineteen','53 are measured and twenty'),('F002 and L071','F002, L071 and L038'),('32 await a complete','31 await a complete'),('32 originals','31 originals'),('Thus 73 of','Thus 74 of'),('handled: 72 recoveries','handled: 73 recoveries'),('All nineteen source editions','All twenty source editions'),('None of these nineteen recoveries','None of these twenty recoveries'),('science72/v1/new_original_registration.json','science73/v1/new_original_registration.json'),('Of the 72 corrected recoveries','Of the 73 corrected recoveries'),('106={}&72','106={}&73'),('&+32\\','&+31\\')]:txt=txt.replace(a,b)
 if name=='README.rst':
  marker='All twenty source editions';txt=txt.replace(marker,'The `L038 guide <papers/recoveries/L038/v1/PUBLICATION.rst>`_ presents the full rank-existence recovery.\n\n'+summary+marker,1)
 elif name=='audit/completion.rst':
  marker='The `current overview';assert marker in txt;txt=txt.replace(marker,summary+marker,1)
 else:
  marker='The accepted overview v19';assert marker in txt;txt=txt.replace(marker,summary+marker,1)
 put(name,txt)
oldv=(R/'scripts/verify_snapshot.py').read_text()
added='''def check_previous_science73():
    spec=importlib.util.spec_from_file_location('science73_history',ROOT/'scripts/check_science73_history.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def check_science73():
    spec=importlib.util.spec_from_file_location('science73',ROOT/'scripts/check_science73.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

'''
oldv=oldv.replace('def main():',added+'def main():',1).replace('science_history = check_previous_F003_disposition()','science_history = check_previous_science73()').replace('science72 = check_F003_disposition()','science72 = check_science73()')
put('scripts/verify_snapshot.py',oldv)
print(json.dumps(dict(status='PREPARED_L038_METADATA',stage=str(T),recoveries=73,refutations=1,handled=74,pending=31,measured=53,unmeasured=20,public_written=False)))
