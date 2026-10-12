#!/usr/bin/env python3
"""Replay exact locally read HTML/disposition bindings; never infer genre from keywords."""
from pathlib import Path
import argparse,copy,hashlib,json,re
from html.parser import HTMLParser
H=Path(__file__).resolve().parent
AUTHOR='f5f8f9b6d9f247e264c2107b516a7bcb9d6c78f017c7081a85ff72f114f1322e'
SOURCE='3cb9f4b688c7e8697609490041d8b9a84a57a0960696d697e92538cc28502527'
def need(b,s):
 if not b:raise ValueError('L022_REVIEW: '+s)
def digest(b):return hashlib.sha256(b).hexdigest()
class Text(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_data(self,d):self.parts.append(d)
def paragraph_bindings(b):
 t=b.decode('utf8');ans=[]
 for i,m in enumerate(re.finditer(r'<p>(.*?)</p>',t,re.S),1):
  h=Text();h.feed(m.group(1));s=' '.join(''.join(h.parts).split());ans.append(dict(paragraph=i,start_utf8_byte=len(t[:m.start()].encode()),end_utf8_byte=len(t[:m.end()].encode()),literal_sha256=digest(m.group(0).encode()),normalized_text_sha256=digest(s.encode())))
 need(len(ans)==5,'five complete editorial paragraphs');return ans
def semantic(d):
 need(d['original_id']=='L022'and d['title']=='Preface'and d['doi']=='10.2140/iig.2023.20.63','exact original identity')
 need(d['source']['sha256']==SOURCE and d['source']['bytes']==26208 and d['source']['format']=='publisher complete article HTML'and d['source']['printed_page_range']==[63,64],'exact available representation')
 need(d['document_kind']=='memorial editorial preface'and d['recovery_status']=='NO_PRINCIPAL_MATHEMATICAL_RESULT_TO_RECOVER','read-source disposition')
 need(d['principal_mathematical_results']==[]and d['open_questions_or_conjectures_stated']==[]and not d['replacement_manuscript_required'],'no invented mathematical target')
 need(len(d['content_dispositions'])==5 and all(not x['mathematical_result_to_reprove']for x in d['content_dispositions'])and d['content_dispositions'][2]['other_authors_results_are_not_results_proved_here'],'five exact content dispositions')
 need(d['accessible_original_retained']and not d['exclude_from_active_catalogue']and not d['count_as_measured_mathematical_recovery'],'accessible original preserved without measured recovery')
 need(d['compression_factor']is None and not d['public_catalogue_changed'],'no factor or public mutation')
 need(d['new_original_credit']==d['new_question_credit']==d['new_formal_credit']==0,'no new credit')
 return True

def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh report')
 if(H/'manifest.json').exists():
  for e in json.loads((H/'manifest.json').read_text())['exports']:
   b=(H/e['path']).read_bytes();need(len(b)==e['bytes']and digest(b)==e['sha256'],'exact review export')
 src=a.study_root/'sources/preface2023.html';b=src.read_bytes();need(len(b)==26208 and digest(b)==SOURCE,'exact locally read whole HTML')
 author=a.study_root/'L022_editorial_disposition';need(digest((author/'manifest.json').read_bytes())==AUTHOR,'exact root disposition freeze')
 for e in json.loads((author/'manifest.json').read_text())['exports']:
  v=(author/e['path']).read_bytes();need(len(v)==e['bytes']and digest(v)==e['sha256'],'author export')
 d=json.loads((author/'disposition.json').read_text());semantic(d)
 need(paragraph_bindings(b)==json.loads((H/'reading_receipt.json').read_text())['paragraphs'],'exact paragraphs personally read, not new automated classification')
 controls=[]
 changes=[('invent zero factor',lambda d:d.update(compression_factor=0)),('invent infinite factor',lambda d:d.update(compression_factor='infinity')),('measured recovery credit',lambda d:d.update(count_as_measured_mathematical_recovery=True)),('drop accessible original',lambda d:d.update(accessible_original_retained=False)),('exclude original',lambda d:d.update(exclude_from_active_catalogue=True)),('keep nonexistent theorem pending',lambda d:d.update(replacement_manuscript_required=True)),('claim described other-paper result',lambda d:d['content_dispositions'][2].update(other_authors_results_are_not_results_proved_here=False)),('new question credit',lambda d:d.update(new_question_credit=1)),('premature public mutation',lambda d:d.update(public_catalogue_changed=True))]
 for name,f in changes:
  x=copy.deepcopy(d);f(x)
  try:semantic(x)
  except ValueError:controls.append(name)
  else:raise ValueError('mutation survived '+name)
 report=dict(status='PASS_DISTINCT_EDITORIAL_DISPOSITION',source_bytes=26208,complete_editorial_paragraphs=5,accessible_original_retained=True,mathematical_recovery_required=False,count_as_measured=False,factor=None,new_credit=0,network_used=False,source_assets_exported=False,public_changed=False,controls=controls)
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
