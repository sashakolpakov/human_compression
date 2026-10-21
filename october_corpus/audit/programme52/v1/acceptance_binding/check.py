#!/usr/bin/env python3
"""Bounded final adoption binding; no arithmetic, source or science replay."""
from pathlib import Path
from copy import deepcopy
import argparse,json,hashlib
H=Path(__file__).resolve().parent
BASE='cc05d285ebedf5e75c71479897839dd47cfa8ec98c1e073ae33ec32163df455b';ROOT='e44d226e0b6729b2e10b85bf601e45b029532e20a68f9b84c2292a3d17ba7b09';AUTHOR='7a4d46b0bc00aa2a84a4cc76f5668ac677124caa8e8a0a1a149bce3073efa5fe'
def load(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p,z):need(p.stat().st_size==z['bytes']and sha(p)==z['sha256'],'exact '+str(p))
def check(admission,pointer,review):
 need(admission['author_manifest']['sha256']==AUTHOR and admission['independent_manifest']['sha256']==ROOT,'actual distinct acceptance')
 need(review['author_manifest']['sha256']==AUTHOR and review['status']=='ROOT_ACCEPTED_DISTINCT_OVERVIEW_PENDING_PUBLICATION_REGISTRATION','actual scope')
 need([admission[k]for k in ['topic_count','distinct_originals','mathematical_pending_originals','editorial_originals','archived_originals','exact_fractions','actual_SVG_bars','actual_PDF_bars']]==[19,52,53,1,55,71,161,161],'partition and comparisons')
 need(admission['newly_registered_originals']==['L047']and admission['unchanged_prior_fractions']==69 and admission['software_inclusive_factors']is None and admission['pooled_factor']is None,'one original and manuscript scope')
 need(pointer['recovered_originals']==52 and pointer['mathematical_pending_originals']==53 and pointer['admission']['path']=='audit/overview/v18/admission.json','new pointer')
 need(pointer['reader']['path']=='audit/overview/v18/packet/reader.pdf','reader route')
def main(study):
 if(H/'manifest.json').exists():
  for z in load(H/'manifest.json')['exports']:bind(H/z['path'],z)
 P=study/'topic_B_L047_publication_proposal';R=study/'corpus106_overview_v18_root_review';O=study/'corpus106_overview_v18_candidate_v2'
 need(sha(P/'manifest.json')==BASE and sha(R/'manifest.json')==ROOT and sha(O/'manifest.json')==AUTHOR,'frozen chain')
 for d in [P,R,O]:
  for z in load(d/'manifest.json')['exports']:bind(d/z['path'],z)
 plan=load(H/'copy_plan_addition.json');need(len(plan['files'])==7 and len({z['public_path']for z in plan['files']})==7,'exact7 additive routes')
 for z in plan['files']:bind(study/z['study_path'],z)
 a=load(H/'overview_admission_template.json');p=load(H/'overview_pointer_template.json');r=load(R/'review.json');check(a,p,r)
 bind(H/'overview_admission_template.json',p['admission']);bind(O/'reader.pdf',p['reader'])
 for key in ['current_corpus','current_catalogue','active_original_catalogue','original_registration','registration_report']:bind(P/'wrappers'/a[key]['path'],a[key])
 controls=[]
 for label,edit in [('wrong review',lambda q:q['independent_manifest'].update(sha256=AUTHOR)),('extra credit',lambda q:q.update(newly_registered_originals=['N001','L047'])),('software scalar',lambda q:q.update(software_inclusive_factors=1)),('wrong fraction extent',lambda q:q.update(exact_fractions=70))]:
  q=deepcopy(a);edit(q)
  try:check(q,p,r)
  except ValueError:controls.append(label)
  else:raise ValueError('mutation survived '+label)
 return dict(status='PASS_ADDITIVE_ACCEPTANCE_BINDING',prior_payloads=289,additional_payloads=7,total_payloads=296,packets=7,controls=controls,public_mutations=False,root_installation_required=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');r=main(a.study_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
