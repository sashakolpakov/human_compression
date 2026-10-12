#!/usr/bin/env python3
"""Portable binding/scope/rebuild check; it does not decide proof truth."""
from pathlib import Path
import argparse,copy,hashlib,json,re,subprocess,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
EXPECTED_PRIOR={
 'bounded_author':'a52c3201765fd7360a39ae30b37cd40c30ac0b23f04ea6a22b8dc579a8061696',
 'bounded_review':'a9ca73620f01a9a2972a908ad39d81f8ea9266d56c148919b2ce3ebb0981ff11',
 'bounded_root':'4abdf4c180d1fc08f52402f98faa5cd71b5c1ebecd5bdc84aed272cbf712691b'}
LABELS=['dihedral','end','degree','fixed','parabolic','cubic','seven','exception','principal']
INPUTS=['Ree.classification','Ree.pair_centralizers','Ree.Sylow2_outer','Ree.fixed_field','Ree.unique_3_fixed_point','Ree.four_group_normalizer','PSL2.structure','Figure1.normalizers','Polytopes.C_groups']
def need(ok,msg):
 if not ok: raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def binding(root,item):
 p=root/item['path'];need(p.is_file(),'absent '+str(p));need(p.stat().st_size==item['bytes'],'bytes '+str(p));need(sha(p)==item['sha256'],'hash '+str(p))
def semantic(sc,dp,pr,pm,mi,ed):
 need(sc['original_id']=='L039','original');need(len(sc['rows'])==31,'full31');rr={r['id']:r for r in sc['rows']};need(len(rr)==31,'unique dispositions')
 need(sc['native_pages']=={'replacement':7,'whole_bounded_companion':3},'whole manuscripts')
 need(sc['whole_original_credit']==0 and sc['new_question_credit']==0 and sc['measurements'] is None and sc['new_formalization'] is None,'no premature credit')
 need(sc['required_finite_premises']==[] and sc['unresolved_principal']==[],'written principal route')
 need(rr['Question.chiral']['disposition']=='SOURCE_RECORDED_UNANSWERED_NO_CURRENT_STATUS_CLAIM','question retained')
 need(rr['L7']['disposition']=='RECOVERED_WITH_NONDEGENERATE_STRING_QUALIFICATION','nondegenerate scope')
 need(rr['L6.a']['disposition']=='RECOVERED_WITH_SIGN_ROUTING_CORRECTION','sign correction')
 need('FALSE_NORMALITY' in rr['L14']['disposition'],'false normality acknowledged')
 for key in ('L9','L13.1','L13.3'):need('CONDITIONAL_CLAIM_DISCHARGED_BY_NONEXISTENCE' in rr[key]['disposition'],'conditional scope '+key)
 need(rr['Figure1']['disposition']=='RECOVERED_FROM_RETAINED_NORMALIZERS_AND_DOUBLE_COUNTING','diagram basis')
 need('selected D14 class' in rr['Figure1']['route'],'diagram class')
 need(sc['published_edition']['sha256'] is None and sc['published_edition']['local_bytes'] is None,'published byte caveat')
 need([x['id'] for x in dp['retained_inputs']]==INPUTS,'retained inputs')
 need(all(x['full_external_proof_cost'] is None for x in dp['retained_inputs']),'external unknown costs')
 need('Kleidman1988 Lemma6.2' in dp['retained_inputs'][3]['source_locator'] and 'Nagy2021' in dp['retained_inputs'][3]['source_locator'],'fixed field locator')
 need(dp['no_retention_of_false_normality'] and dp['no_retention_of_middle_dihedral_restriction'],'discarded route')
 need(pr['required_mathematical_programs']==[] and pr['required_mathematical_data']==[],'no finite premises')
 need([x['path'] for x in pr['optional_validation']]==['diagnostics.py'] and pr['formal_files']==[],'validation role')
 need(pr['software_inclusive_factor'] is None and pr['source_software_cost'] is None,'software unknown')
 need([x['label'] for x in pm['new_environments']]==LABELS and pm['retained_inputs']==INPUTS,'proof routes')
 need(pm['whole_companion']=='inputs/bounded_author/ree_involutions.tex','full companion')
 need(len(mi['copied_files'])==18 and 'root authored' in mi['roles']['bounded_author'] and 'enumeration_volume' in mi['roles']['new_replacement'],'authorship')
 need(ed['copied_third_party_text'] is False,'no primary export')
 return True

def controls(objects):
 tests=[('missing_source_clause',lambda x:x[0]['rows'].pop()),('duplicate_clause',lambda x:x[0]['rows'].__setitem__(1,x[0]['rows'][0])),('companion_omitted',lambda x:x[0]['native_pages'].__setitem__('whole_bounded_companion',0)),('credit_invented',lambda x:x[0].__setitem__('whole_original_credit',1)),('question_solved',lambda x:next(r for r in x[0]['rows'] if r['id']=='Question.chiral').__setitem__('disposition','SOLVED')),('nondegenerate_scope_dropped',lambda x:next(r for r in x[0]['rows'] if r['id']=='L7').__setitem__('disposition','RECOVERED_UNCHANGED')),('normality_hidden',lambda x:next(r for r in x[0]['rows'] if r['id']=='L14').__setitem__('disposition','RECOVERED_UNCHANGED')),('middle_restriction_promoted',lambda x:next(r for r in x[0]['rows'] if r['id']=='L13.3').__setitem__('disposition','UNCONDITIONAL_NORMALIZER_THEOREM')),('all_D14_classes',lambda x:next(r for r in x[0]['rows'] if r['id']=='Figure1').__setitem__('route','all abstract subgroups')),('published_hash_invented',lambda x:x[0]['published_edition'].__setitem__('sha256','0'*64)),('fixed_field_input_removed',lambda x:x[1]['retained_inputs'].pop(3)),('free_external_proof',lambda x:x[1]['retained_inputs'][0].__setitem__('full_external_proof_cost',0)),('fixed_field_locator_removed',lambda x:x[1]['retained_inputs'][3].__setitem__('source_locator','standard fact')),('false_route_restored',lambda x:x[1].__setitem__('no_retention_of_false_normality',False)),('diagnostic_made_premise',lambda x:x[2]['required_mathematical_programs'].append('diagnostics.py')),('formalization_invented',lambda x:x[2]['formal_files'].append('Full.lean')),('software_zero',lambda x:x[2].__setitem__('source_software_cost',0)),('proof_route_missing',lambda x:x[3]['new_environments'].pop()),('companion_route_missing',lambda x:x[3].__setitem__('whole_companion','')),('prior_role_erased',lambda x:x[4]['roles'].__setitem__('bounded_author','current author'))]
 result=[]
 for name,mut in tests:
  obj=copy.deepcopy(objects);mut(obj)
  try:semantic(*obj)
  except ValueError:result.append({'name':name,'rejected':True})
  else:raise ValueError('mutation survived '+name)
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--diagnostics',action='store_true');ap.add_argument('--study-root');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');ap.add_argument('--pre-freeze',action='store_true');args=ap.parse_args()
 out=Path(args.out);need(not out.exists(),'fresh output directory required');out.mkdir(parents=True)
 manifest=ROOT/'manifest.json';exports=0
 if manifest.exists():
  mf=read('manifest.json');paths=[x['path'] for x in mf['exports']];need(len(paths)==len(set(paths)),'unique exports')
  for it in mf['exports']:binding(ROOT,it)
  exports=len(paths)
 else:need(args.pre_freeze,'manifest required')
 objects=[read(n) for n in ['source_contract.json','dependencies.json','program_roles.json','proof_map.json','migration.json','edition_comparison.json']];semantic(*objects);sc,dp,pr,pm,mi,ed=objects
 for key,h in EXPECTED_PRIOR.items():need(sha(ROOT/'inputs'/key/'manifest.json')==h,'prior pin '+key)
 for it in mi['copied_files']:binding(ROOT,it['current']);need(it['current']['sha256']==it['original']['sha256'] and it['current']['bytes']==it['original']['bytes'],'exact copy')
 lines=(ROOT/'rank_four_replacement.tex').read_text().splitlines(keepends=True)
 for sp in pm['new_environments']:
  block=''.join(lines[sp['start_line']-1:sp['end_line']]).encode();need(hashlib.sha256(block).hexdigest()==sp['sha256'],'proof span '+sp['label'])
 pages={}
 for name,n in [('rank_four_replacement.pdf',7),('inputs/bounded_author/ree_involutions.pdf',3)]:
  pages[name]=len(PdfReader(ROOT/name).pages);need(pages[name]==n,'page extent '+name)
 if args.study_root:
  for it in (sc['primary'],sc['auxiliary']):binding(Path(args.study_root),it)
 diag=None
 if args.diagnostics:
  raw=subprocess.check_output([sys.executable,'-B','-O',str(ROOT/'diagnostics.py')],text=True);diag=json.loads(raw);need(diag==read('diagnostics_report.json'),'optional diagnostic replay');(out/'diagnostics.json').write_text(raw)
 renders=[]
 if args.render:
  for i,(name,n) in enumerate([('rank_four_replacement.tex',7),('inputs/bounded_author/ree_involutions.tex',3)]):
   build=out/('build'+str(i));build.mkdir();p=ROOT/name
   for k in range(2):
    res=subprocess.run([args.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(build),str(p)],cwd=p.parent,text=True,capture_output=True);(build/('pass'+str(k)+'.txt')).write_text(res.stdout+res.stderr);need(res.returncode==0,'TeX failed '+name)
   log=(build/(p.stem+'.log')).read_text();need(not re.search(r'Overfull|undefined references|undefined citations|LaTeX Error',log),'render diagnostics '+name)
   current=PdfReader(build/(p.stem+'.pdf'));old=PdfReader(p.with_suffix('.pdf'));need(len(current.pages)==n,'render pages '+name);need([x.extract_text() for x in current.pages]==[x.extract_text() for x in old.pages],'render text '+name);renders.append({'path':name,'pages':n,'exact_page_text':True,'diagnostics':[]})
 report=dict(status='PASS',scope='Bindings, complete-source dispositions, proof spans, exact rebuild and optional diagnostic only; no automated proof adjudication.',frozen_exports=exports,source_rows=31,retained_input_classes=9,new_proof_environments=9,exact_prior_files=18,native_pages=pages,controls=controls(objects),optional_diagnostics=diag,renders=renders,source_bindings_checked=bool(args.study_root))
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','exports':exports,'controls':len(report['controls']),'source_rows':31,'renders':renders}))
if __name__=='__main__':main()
