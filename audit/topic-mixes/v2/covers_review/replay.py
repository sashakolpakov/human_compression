#!/usr/bin/env python3
"""Bounded independent L016 review replay; does not rerun unrelated science."""
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
PIN='a1398f54debff3981d1606cb1055060b4abc75ae51f056a00c46a03c7821401a'
def need(v,s):
    if not v:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scope_checks(s):
    need(len(s['source_rows'])==19 and len(s['proof_contexts'])==20,'exact scientific rows and contexts')
    rows={r['id']:r for r in s['source_rows']}
    need(rows['B3']['disposition']=='disproved_literal_auxiliary_with_repair','literal thin-only correction')
    need(rows['B5']['disposition']=='qualified_unused_background','inverse-poset qualification')
    need(rows['A1']['disposition']=='ancillary_not_rederived'and rows['A3']['disposition']=='ancillary_not_rederived','unrecovered censuses')
    need(rows['Q1']['disposition']=='excluded_unanswered_or_omitted','question boundary')
    need(not s['end_to_end_Lean'],'partial formalization')
    need(sum(len(f['declarations'])for f in s['formal'])==6,'six formal statements')
    need([p['role']for p in s['programs']]==['required finite premise','optional validation','optional validation'],'proof-code roles')
    need(s['whole_topic_cost_policy']['full_existing_Mixes_common'],'whole common dependency')
    need(s['whole_topic_cost_policy']['optional_validation_symmetric'],'symmetric validation boundary')
    need(s['whole_topic_cost_policy']['source_historical_GAP_and_Atlas_cost']is None,'unknown historical code')
    need(s['factor']is None and s['new_source_credit']==s['new_question_credit']==0,'no numerical or credit admission')
def run(cmd,out,cwd=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,text=True,timeout=180)
    out.write_text(r.stdout+r.stderr);need(r.returncode==0 and 'Error,'not in r.stdout+r.stderr,'command failed '+str(cmd[0]));return r.stdout+r.stderr
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap');a=ap.parse_args();need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
    if (P/'manifest.json').exists():
        own=json.loads((P/'manifest.json').read_text())
        for x in own['exports']:need(sha(P/x['path'])==x['sha256'],'changed independent review '+x['path'])
    author=a.study_root/'topic_Mix_L016_recovery';need(sha(author/'manifest.json')==PIN,'exact author freeze')
    m=json.loads((author/'manifest.json').read_text())
    for r in m['exports']:need(sha(author/r['path'])==r['sha256'],'author export '+r['path'])
    s=json.loads((author/'scope.json').read_text());scope_checks(s)
    for r in s['external_bindings']:need(sha(a.study_root/r['path'])==r['sha256'],'external binding '+r['path'])
    for r in s['proof_contexts']:
        t=(author/r['path']).read_text()[r['start']:r['end']];need(hashlib.sha256(t.encode()).hexdigest()==r['sha256'],'context '+r['id'])
    controls=[]
    mutations=[('end_to_end_formal',lambda x:x.update(end_to_end_Lean=True)),
      ('credit',lambda x:x.update(new_question_credit=1)),
      ('code_demotion',lambda x:x['programs'][0].update(role='optional validation')),
      ('asymmetric_validation',lambda x:x['whole_topic_cost_policy'].update(optional_validation_symmetric=False)),
      ('free_old_umbrella',lambda x:x['whole_topic_cost_policy'].update(full_existing_Mixes_common=False)),
      ('unknown_zero',lambda x:x['whole_topic_cost_policy'].update(source_historical_GAP_and_Atlas_cost=0)),
      ('literal_lemma_proved',lambda x:next(r for r in x['source_rows']if r['id']=='B3').update(disposition='proved')),
      ('atlas_census_recovered',lambda x:next(r for r in x['source_rows']if r['id']=='A3').update(disposition='proved'))]
    for name,mut in mutations:
        v=copy.deepcopy(s);mut(v)
        try:scope_checks(v)
        except RuntimeError:controls.append(name)
        else:raise RuntimeError('accepted scope mutation '+name)
    run([sys.executable,'-B','-O',P/'independent_models.py','--out',a.out/'models.json'],a.out/'models.log')
    log=run([a.gap,'-q','-T',P/'universal_base.g'],a.out/'universal_base.log')
    need('INDEPENDENT_PRESENTATION_INDEX4_FACET24_UNIVERSAL96_PASS'in log,'missing exact presentation result')
    result={'status':'PASS','author_manifest':PIN,'author_exports':len(m['exports']),'source_rows':19,'proof_contexts':20,
      'external_bindings':len(s['external_bindings']),'independent_sample_moduli':[1,2,4,7],
      'all_subset_intersections':1024,'rank_extension_samples':[5,6],'source_universal_order':96,
      'model_controls':4,'scope_controls':controls,'scope':'independent finite validation and scope integrity, not a substitute for full written mathematical review',
      'science_author':'rewrite_termination','reviewer':'enumeration_volume',
      'prior_reviewer_role':'earlier Topic E universal table authorship disclosed; current isolated presentation independently transcribed and rechecked',
      'factor':None,'source_credit':0,'question_credit':0}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
