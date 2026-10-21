#!/usr/bin/env python3
"""Additive public programme52 guard; never changes historical guard bodies."""
from pathlib import Path
import argparse,importlib.util,json,sys,subprocess,tempfile,hashlib

def need(v,m):
 if not v:raise ValueError('PROGRAMME52: '+m)
def verify(root,allow_pending_overview=False):
 root=Path(root);packet=root/'audit/programme52/v1/publication_plan';sys.path.insert(0,str(packet))
 try:
  spec=importlib.util.spec_from_file_location('programme52_routes',packet/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);result=mod.verify(root,root,root)
 finally:sys.path.pop(0)
 def load(n):return json.loads((root/n).read_text())
 def bind(row):
  b=(root/row['path']).read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'exact '+row['path'])
 corpus=load('audit/corpus/latest.json');cat=load('papers/latest_catalogue.json');topic=load('papers/topic-b/latest.json')
 for z in [corpus['active_catalogue'],corpus['snapshot'],cat['unified_B_current_edition'],topic['admission'],topic['measurement'],topic['reader']]:bind(z)
 need(cat['unified_B_current_edition']['path']=='papers/topic-b/latest.json','current B binding')
 admission=load('audit/topic-b/v4/measurement/admission.json');bind(admission['author_manifest']);bind(admission['independent_manifest']);review=load('audit/topic-b/v4/measurement/independent_review/review.json');need(review['status']=='ACCEPTED_DISTINCT_NUMERICAL_REVIEW_AND_ROOT_ADOPTION','distinct arithmetic adoption')
 overview=load('audit/overview/v18/packet/results.json');need(overview['original_manuscript_count']==52 and overview['available_written_and_conditional_comparisons']==71,'complete52 overview')
 B=next(t for t in overview['topics']if t['topic']=='B');need((B['source_sum'],B['common_theory'],B['applications_sum'],B['written_denominator'])==(144877,74303,74768,149071),'all B manuscripts paid')
 table=load('audit/programme52/v1/current_topic_table.json')['topics'];readme=(root/'README.rst').read_text();tex=(root/'audit/protocol.tex').read_text()
 need(len(table)==19 and sum(len(t['original_ids'])for t in table)==52,'current19/52 table')
 for z in table:
  block=f"   * - `{z['title']} <{z['guide']}>`_\n     - {', '.join(z['original_ids'])}\n     - {z['display']}\n";need(block in readme,'current exact topic row '+z['topic'])
 for text in ['52 accessible originals','53 await mathematical recovery','fifty-two individual','remaining twenty-six','audit/overview/v18/','29,398-character common addition','0.971866','3.629111','Executable software is excluded symmetrically','there is no pooled factor']:
  need(text in readme,'current README '+text)
 need('106=52'in tex and '}+53\\'in tex and 'overview v18'in tex,'current protocol partition')
 if not allow_pending_overview:
  pointer=load('audit/overview/latest.json');need(pointer['recovered_originals']==52 and pointer['current_conditional_factors']==52 and pointer['current_whole_factors']==19,'current overview pointer');bind(pointer['admission']);bind(pointer['reader']);need(pointer['admission']['path']=='audit/overview/v18/admission.json','root overview admission route');a=load(pointer['admission']['path']);need('ROOT'in a['status']and ('ADMIT'in a['status']or'ACCEPT'in a['status']),'root current overview admission')
 with tempfile.TemporaryDirectory(prefix='programme52-numeric-')as tmp:
  out=Path(tmp)/'check';q=subprocess.run([sys.executable,'-B','-O',str(root/'audit/topic-b/v4/measurement/packet/check.py'),'--out',str(out)],capture_output=True,text=True);need(q.returncode==0,'B6 portable replay '+q.stderr);a=load_report(out/'report.json');need(a['exact_fractions']==270,'all270 fractions')
 with tempfile.TemporaryDirectory(prefix='programme52-overview-')as tmp:
  out=Path(tmp)/'check';q=subprocess.run([sys.executable,'-B','-O',str(root/'audit/overview/v18/packet/check.py'),'--out',str(out)],capture_output=True,text=True);need(q.returncode==0,'overview replay '+q.stderr);a=load_report(out/'report.json');need(a['exact_fractions']==71 and a['actual_bars_per_format']==161,'71 factors161 actual bars')
 result.update(status='PASS_PROGRAMME52'if not allow_pending_overview else'PASS_PROPOSED_PROGRAMME52_PENDING_OVERVIEW_ADMISSION',overview_fractions=71,overview_bars=161,topic_fractions=270,root_overview_admission_checked=not allow_pending_overview)
 return result

def load_report(p):return json.loads(p.read_text())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--allow-pending-overview',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,a.allow_pending_overview),indent=2))
