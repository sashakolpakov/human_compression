"""Independent audit of the actual combined registration diff, not its mathematics."""
from pathlib import Path
import ast, hashlib, importlib.util, json, os, re, subprocess
S=Path(__file__).resolve().parents[2];W=S/'reboot_20261013/science76_registration_distinct';P=S/'reboot_20261013/publication76';R=S.parents[1]/'math_compression';T=P/'review_repo01';AUD='audit/science76/v1';IDS={'F001','N012'}
def need(v,s):
 if not v:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='6670d59d1172044616c808846cf1a1f220c83941','fixed predecessor')
 tracked=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')if p]
 old=load(R/'audit/corpus/latest.json');new=load(T/'audit/corpus/latest.json');history=load(T/AUD/'history_routes.json')['routes']
 need(set(history)=={'README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py'},'exact eight archived mutable files')
 changed=[]
 for rel in tracked:
  a,b=R/rel,T/rel
  if a.is_symlink():
   need(b.is_symlink()and os.readlink(a)==os.readlink(b),'old symbolic route changed '+rel)
   continue
  need(b.is_file(),'old public file missing '+rel)
  if os.path.samefile(a,b) or a.read_bytes()==b.read_bytes():continue
  changed.append(rel)
 need(set(changed)==set(history),'only eight old files changed')
 for rel,pin in history.items():
  archived=T/pin['path'];need(archived.read_bytes()==(R/rel).read_bytes(),'prior file not preserved '+rel);need(archived.stat().st_size==pin['bytes']and sha(archived)==pin['sha256'],'archive pin')
 # The fixture also contains ignored legacy working notes from the checkout.
 # Only staged new paths belong to the proposed public transaction.
 stage=P/'stage01';tracked_set=set(tracked)
 additions=sorted(str(p.relative_to(stage))for p in stage.rglob('*')if p.is_file()and str(p.relative_to(stage))not in tracked_set)
 need(not any(p.endswith('.md')for p in additions),'new public Markdown')
 active=set(new['active_original_ids']);editorial=set(new['editorial_original_ids']);admitted=set(new['admitted_original_ids']);refuted=set(new['refuted_principal_original_ids']);pending=set(new['accessible_pending_original_ids']);measured=set(new['measured_original_ids']);unmeasured=set(new['measurement_pending_original_ids'])
 need(len(active)==106 and len(editorial)==1 and len(active-editorial)==105,'fixed corpus')
 need(not(admitted&refuted or admitted&pending or refuted&pending),'dispositions disjoint');need(admitted|refuted|pending==active-editorial,'complete mathematical partition')
 need((len(admitted),len(refuted),len(admitted|refuted),len(pending))==(76,1,77,28),'current counts')
 need(admitted-set(old['admitted_original_ids'])==IDS and set(old['accessible_pending_original_ids'])-pending==IDS,'exact pair added')
 need(measured==set(old['measured_original_ids']) and len(measured)==53 and unmeasured==admitted-measured and len(unmeasured)==23,'measurement boundary')
 need(set(new['archived_original_ids'])==set(old['archived_original_ids'])and len(new['archived_original_ids'])==55,'archive unchanged')
 before=load(R/old['active_catalogue']['path']);after=load(T/new['active_catalogue']['path']);bd={e['original_id']:e for e in before['entries']};ad={e['original_id']:e for e in after['entries']};need(set(bd)==set(ad)==active,'same original IDs')
 changed_rows=[]
 for key in sorted(active):
  if bd[key]==ad[key]:continue
  changed_rows.append(key);need(key in IDS,'unrelated original changed')
  need({k:v for k,v in bd[key].items()if k not in ['current_principal_recovery','next_obligation']}=={k:v for k,v in ad[key].items()if k not in ['current_principal_recovery','next_obligation']},'original evidence changed')
  need(ad[key]['current_principal_recovery']['historical_admission_evidence']==bd[key]['current_principal_recovery'],'prior principal status lost')
 need(set(changed_rows)==IDS,'exact two changed rows')
 need(ad['F001']['current_principal_recovery']['literal_principal_theorem_recovered']is True,'F001 principal truth')
 need(ad['N012']['current_principal_recovery']['literal_principal_theorem_recovered']is False,'N012 corrected clause')
 need('Lemma4.1' in ad['F001']['current_principal_recovery']['auxiliary_correction'],'separate F001 auxiliary correction')
 need('Corollary 4.2.1' in ad['N012']['current_principal_recovery']['corrected_numbered_claim'],'N012 correction retained')
 bn=load(R/'papers/catalogue_corrected_unmeasured.json');an=load(T/'papers/catalogue_corrected_unmeasured.json');tail=an['entries'][len(bn['entries']):]
 need(an['entries'][:len(bn['entries'])]==bn['entries']and len(tail)==12,'old document rows unchanged plus twelve')
 need(len({r['id']for r in an['entries']})==len(an['entries']),'unique document IDs')
 need([sum(r['physical_pages']for r in tail if r['source_ids']==[o])for o in ['F001','N012']]==[22,30],'document inventory only')
 for row in tail:
  need(not row['measured']and row['compression_factor']is None,'no new factor');need((T/row['tex']).is_file()and(T/row['pdf']).is_file(),'new native routes')
 oldtree=ast.parse((R/'scripts/verify_snapshot.py').read_text());newtree=ast.parse((T/'scripts/verify_snapshot.py').read_text())
 def functions(t):return {n.name:ast.dump(n,include_attributes=False)for n in t.body if isinstance(n,ast.FunctionDef)}
 of,nf=functions(oldtree),functions(newtree);need(all(nf[k]==v for k,v in of.items()if k!='main'),'prior verifier bodies preserved')
 allowed=of['main'].replace("id='check_previous_science74'","id='check_previous_science76'").replace("id='check_science74'","id='check_science76'")
 need(nf['main']==allowed,'only two main call substitutions')
 route_links=0
 for rel in ['papers/recoveries/F001/v1/PUBLICATION.rst','papers/recoveries/N012/v1/PUBLICATION.rst']:
  p=T/rel
  for link in re.findall(r'<([^>]+)>`_',p.read_text()):
   need(not link.startswith(('http:','https:'))and(p.parent/link).resolve().is_file(),'new reader route '+link);route_links+=1
 for o in ['F001','N012']:
  adm=load(T/('audit/recoveries/'+o+'/v1/admission.json'));need(adm['publication_gate']==AUD+'/root_integration.json','one common publication gate')
  need(adm['whole_original_credit']==0 and adm['new_measurements']==adm['new_Lean_declarations']==adm['new_question_credit']==0 and adm['compression_factor']is None,'proposal no credit')
 spec=importlib.util.spec_from_file_location('science76_registration_candidate',T/'scripts/check_science76.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);preflight=m.verify(T,require_root=False)
 report=dict(status='PASS_DISTINCT_F001_N012_REGISTRATION_DIFF',old_tracked_files_checked=len(tracked),changed_old_files=changed,exact_archives=8,changed_original_rows=changed_rows,unchanged_original_rows=104,new_document_records=12,new_document_pages={'F001':22,'N012':30},new_guide_links=route_links,new_public_markdown=0,old_verifier_functions_preserved=len(of)-1,main_call_substitutions=2,independent_partition={'active':106,'mathematical':105,'recoveries':76,'refutations':1,'handled':77,'pending':28,'measured':53,'unmeasured':23,'editorial':1,'archived':55},candidate_preflight=preflight,root_gate_not_yet_required=True,public_writes=False,mathematical_reapproval=False)
 (W/'transition_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
