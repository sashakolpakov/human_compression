from pathlib import Path
import argparse,json,shutil
from decimal import Decimal,localcontext
from prepare import H,TOP,REG,SNAP,load,write,rec,need

def make(repo,overview):
 need(not(H/'manifest.json').exists(),'preserve frozen proposal')
 r=load(overview/'results.json');readme=(H/'baseline/README.rst').read_text();tex=(H/'baseline/audit/protocol.tex').read_text()
 changes=[('51 accessible originals','52 accessible originals'),('54 await mathematical recovery','53 await mathematical recovery'),('fifty-one individual','fifty-two individual'),('remaining twenty-five','remaining twenty-six'),('audit/overview/v17/','audit/overview/v18/'),('selects v17','selects v18'),('papers/topic-b/v3/README.rst',TOP+'/README.rst'),('N001, N003, N008, L030, L040\n     - 1.094035','N001, N003, N008, L030, L040, L047\n     - 0.971866'),('audit/documentation/v1/previous/README.rst',REG+'/previous/README.rst'),('audit/documentation/v1/previous/protocol.pdf',REG+'/previous/audit/protocol.pdf')]
 for a,b in changes:need(a in readme,'exact README predecessor '+a);readme=readme.replace(a,b)
 marker='Current papers and comparisons\n------------------------------'
 extra='Topic B now includes L047. Its complete old and new common papers cost 74,303\ncharacters before the six applications: the whole factor is **0.971866**, an\nexpansion. L047\'s **3.629111** conditional factor assumes that enlarged common\nacquisition and all required premises; the five earlier conditional values\nremain unchanged. The topic reader shows the 29,398-character common addition\nas a separate acquisition stage.\n\n'
 readme=readme.replace(marker,extra+marker)
 for a,b in [('106=51','106=52'),('}+54\\','}+53\\'),('overview v17','overview v18'),('fifty-one','fifty-two'),('overview/v17/','overview/v18/')]:need(a in tex,'exact protocol predecessor '+a);tex=tex.replace(a,b)
 for n,text in [('README.rst',readme),('audit/protocol.tex',tex)]:p=H/'wrappers'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 table=load(repo/'audit/documentation/v1/packet/topic_table.json');table['source']='audit/overview/v18/packet/results.json'
 for row,t in zip(table['topics'],r['topics']):
  row.update(original_ids=t['source_ids'],accepted_factor=t['written'])
  with localcontext()as c:c.prec=50;row['display']=format(Decimal(t['written']['numerator'])/Decimal(t['written']['denominator']),'.6f')
  if t['topic']=='B':row['guide']=TOP+'/README.rst'
 write('wrappers/'+REG+'/current_topic_table.json',table)
 prior=load(H/'baseline/audit/overview/latest.json');next=prior.copy();next.update(status='PROPOSED_OVERVIEW52_PENDING_ROOT_ADMISSION',admission={'path':'audit/overview/v18/admission.json','bytes':None,'sha256':None},reader=rec(overview/'reader.pdf','audit/overview/v18/packet/reader.pdf'),counts_source=rec(H/'wrappers'/SNAP,SNAP),pending_accessible_originals=53,recovered_originals=52,historically_measured_originals=52,current_conditional_factors=52,mathematical_pending_originals=53,unmeasured_accessible_originals=54,written_factors_status='NINETEEN_WHOLE_AND_FIFTY_TWO_CONDITIONAL_MANUSCRIPT_FACTORS',publication_requires_actual_root_bindings=True,previous_pointer=rec(H/'baseline/audit/overview/latest.json',REG+'/previous/audit/overview/latest.json'))
 write('proposed_overview_pointer.json',next)
 write('documentation_delta.json',dict(README_replacements=changes,README_added_common_acquisition_paragraph=extra,protocol_replacements=[['106=51','106=52'],['}+54\\','}+53\\'],['v17','v18'],['fifty-one','fifty-two']],historical_current_docs_retained=True,unchanged_topic_rows=18))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--overview',type=Path,required=True);a=p.parse_args();make(a.repo,a.overview)
