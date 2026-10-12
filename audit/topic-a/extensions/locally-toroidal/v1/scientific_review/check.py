#!/usr/bin/env python3
"""Bounded assembly review replay; prior component mathematics remains separately accepted."""
import argparse,copy,json,re,shutil,subprocess,sys
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
from migration import need,read,sha,validate
PIN='a9acb0e60065cdef16f63fee0328200357347c29a22175beafb1dc5b87981f1e'
IDS=['background','cubic-presentation','cubic-order','cubic-ambient','cubic-IP','cubic-residue-first','cubic-residue-variable','cubic-spherical','cubic-CPR-even','cubic-CPR-odd','degree-suggestion','cubic-flags','cubic-hypertope','square-generators','square-variable-residue','square-residue-1','square-residue-2','square-residue-3','square-word-orders','square-IP','square-flags','square-universal','finite-1-residues','finite-1-replacement','finite-2-residues','finite-2-replacement','residue-order-warning']
ORIGINS={'cubic':'topic_A_L121_cubic_candidate','square':'topic_A_L121_f4_candidate','finite':'topic_A_L121_section5_candidate','cubic_relation':'topic_A_L121_cubic_relation_v2'}
def bound(base,x):
 p=base/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'bound '+str(p))
def manifest(base):
 m=read(base/'manifest.json')
 for x in m['exports']:bound(base,x)
 return m

def boundary(scope,smap):
 need(smap['clause_count']==27 and [x['id'] for x in smap['clauses']]==IDS,'all 27 source dispositions')
 rows={x['id']:x for x in smap['clauses']}
 need(rows['background']['disposition']=='retained_classical_background','background remains retained')
 need(rows['cubic-ambient']['disposition']=='corrected','cubic ambient corrected')
 need(rows['degree-suggestion']['disposition']=='disproved_for_unrestricted_faithful_degree','minimum-degree scope')
 need(rows['square-word-orders']['disposition']=='reproved_with_terminology_correction','source word/cube distinction')
 for k in ['finite-1-replacement','finite-2-replacement']:need(rows[k]['disposition']=='disproved_and_corrected','both literal replacement corrections')
 need(rows['residue-order-warning']['disposition']=='retained_qualification','ordered local types retained')
 need(Counter(x['role'] for x in scope['required_whole_files'])=={'required_program':8,'required_data':1,'operational_validation_runner':3,'partial_formal':2},'all whole file roles')
 need(not scope['full_Lean'] and 'Exactly six' in scope['formal_scope'] and 'No group orders or geometry' in scope['formal_scope'],'partial formal scope')
 need(scope['source_software_cost'] is None and scope['compression_factor'] is None and scope['whole_original_credit']==0 and scope['new_open_question_credit']==0,'unknown costs and no premature credit')
 need(scope['interfaces']==['AL.1','AL.2','AA.ParabolicPeriods','UA.K','UA.SK.Helly','UA.Geometry'] and 'entire accepted common paper' in scope['common_theory'],'entire common dependency')
 return {'source_clauses':27,'whole_files':14,'mathematical_programs':8,'mandatory_data':1,'nested_runners':3,'partial_formal_files':2,'top_level_runner_additional':1}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=Path('/Users/sasha/medusa/research/leemans'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--reuse-replay',type=Path);a=ap.parse_args();b=a.study_root;p=b/'topic_A_L121_application';out=a.out;need(not out.exists(),'fresh output');out.mkdir(parents=True)
 need(sha(p/'manifest.json')==PIN,'exact assembly author');m=manifest(p);need(len(m['exports'])==28,'all 28 exports')
 scope=read(p/'scope.json');smap=read(p/'source_map.json');bound(b,scope['source'])
 for x in scope['retained_bindings']:bound(b,x);manifest((b/x['path']).parent)
 common_binding=read(b/'topic_A_affine_independent_review/manifest.json')['candidate_manifest'];bound(b,common_binding);manifest((b/common_binding['path']).parent)
 for x in scope['required_whole_files']:
  bound(p,x);part,rest=x['path'].split('/',1);need((p/x['path']).read_bytes()==(b/ORIGINS[part]/rest).read_bytes(),'exact whole accepted program copy '+x['path'])
 migration=validate(b,p);coverage=boundary(scope,smap)
 controls=[]
 for name in ['omit_clause','restore_full_toroid','overstate_minimum_transitive','restore_finite_claim','drop_required_data','claim_full_Lean','free_common','software_zero']:
  sc=copy.deepcopy(scope);sm=copy.deepcopy(smap)
  if name=='omit_clause':sm['clauses'].pop()
  elif name=='restore_full_toroid':sm['clauses'][3]['disposition']='reproved'
  elif name=='overstate_minimum_transitive':sm['clauses'][10]['disposition']='disproved_for_transitive_degree'
  elif name=='restore_finite_claim':sm['clauses'][23]['disposition']='reproved'
  elif name=='drop_required_data':sc['required_whole_files']=[x for x in sc['required_whole_files'] if x['role']!='required_data']
  elif name=='claim_full_Lean':sc['full_Lean']=True
  elif name=='free_common':sc['common_theory']='previously paid elsewhere'
  else:sc['source_software_cost']=0
  try:boundary(sc,sm)
  except ValueError as e:controls.append({'name':name,'rejected_at':str(e)})
  else:raise ValueError('accepted bad boundary '+name)
 for name,file,old,new in [('lost_nonidentity','sections/03-finite.tex','nontrivial involutions','involutions'),('lost_integral_complement','sections/02-square.tex',r'K\cap s\Z^4=sK',r'K\cap s\Z^4=K'),('wrong_residue_order','sections/03-finite.tex','$(c,d,b)$','$(d,c,b)$')]:
  bodies={f:(p/f).read_text() for f in ['sections/01-cubic.tex','sections/02-square.tex','sections/03-finite.tex','sections/04-cubic-relation.tex']};need(old in bodies[file],'actual semantic mutation');bodies[file]=bodies[file].replace(old,new)
  try:validate(b,p,bodies)
  except ValueError as e:controls.append({'name':name,'rejected_at':str(e)})
  else:raise ValueError('accepted changed proof '+name)
 if a.reuse_replay:replay=read(a.reuse_replay)
 else:
  export=out/'exports';export.mkdir()
  for x in m['exports']:
   q=export/x['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p/x['path'],q)
  shutil.copy2(p/'manifest.json',export/'manifest.json')
  q=subprocess.run([sys.executable,'-B','-O',str(export/'check.py'),'--study-root',str(b),'--out',str(out/'author_replay'),'--render','--formal'],capture_output=True,text=True,timeout=180)
  (out/'author.stdout').write_text(q.stdout+q.stderr);need(q.returncode==0,'whole exported replay');replay=read(out/'author_replay/report.json')
 need(replay['status']=='PASS_ASSEMBLED_L121_APPLICATION' and replay['formal_rebuilt'],'whole replay and scoped formal')
 need(len(replay['finite']['formal']['declarations'])==6 and replay['finite']['abstract_presentation']['all_marked_torus_isomorphisms']==8 and replay['square']['kernel_ranks']==[4,4,2],'actual retained component outputs')
 pages=[x.extract_text() for x in PdfReader(p/'application.pdf').pages]
 from hashlib import sha256
 need(len(pages)==11 and [sha256(x.encode()).hexdigest() for x in pages]==replay['render']['page_text_sha256'],'all eleven rebuilt page texts')
 need(not replay['render']['diagnostics'],'clean render')
 report={'status':'PASS_DISTINCT_L121_ASSEMBLY','author_manifest':PIN,'exports':28,'retained_bindings':len(scope['retained_bindings']),'common_manifest':common_binding['sha256'],'migration':migration,'coverage':coverage,'semantic_controls':controls,'control_count':len(controls),'full_export_only_replay':'PASS','formal_declarations':6,'rendered_pages':11,'unrelated_LCD_enumeration_or_common_Lean_build_repeated':False,'whole_original_credit':0,'new_question_credit':0}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
