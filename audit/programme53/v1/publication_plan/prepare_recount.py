#!/usr/bin/env python3
"""Bind exact existing public files to original study locators for portable recount."""
from pathlib import Path
import argparse,json,hashlib,subprocess
from prepare import H,NUM,SCI,load,rec,need,write

def prepare(study,repo):
 inputdir=study/'topic_A_L003_measurement_inputs';refs=[]
 refs+=load(inputdir/'precount/bindings.json')['references']
 docs=load(inputdir/'precount/documents.json');refs+=[x['file']for x in docs['documents']+docs['excluded_current_PDFs']]
 sourcepaths={x['file']['path']for x in docs['documents']if x['kind']=='source'}
 raw=load(inputdir/'precount/raw_inventory.json')['occurrences']
 refs+=raw;refs+=[x['current_exact_copy']for x in raw if'current_exact_copy'in x]
 refs+=[dict(root='study',**rec(study/'topic_A_L003_complete_assembly/whole_file_inventory.json','topic_A_L003_complete_assembly/whole_file_inventory.json'))]
 for x in load(inputdir/'document_map.json')['documents']:refs.append(dict(root='study',path=x['path'],bytes=x['bytes'],sha256=x['sha256']))
 unique={}
 for r in refs:
  key=(r['root'],r['path']);v=dict(root=r['root'],path=r['path'],bytes=r['bytes'],sha256=r['sha256']);need(key not in unique or unique[key]==v,'same original locator');unique[key]=v
 plan=load(H/'copy_plan.json');candidates={}
 for r in plan['files']:candidates.setdefault((r['bytes'],r['sha256']),[]).append(r['public_path'])
 wanted={r['bytes']for r in unique.values()if r['path']not in sourcepaths}
 for n in subprocess.check_output(['rg','--files','--hidden','-g','!.git'],cwd=repo,text=True).splitlines():
  p=repo/n
  if p.is_file()and p.stat().st_size in wanted:
   q=rec(p,n);candidates.setdefault((q['bytes'],q['sha256']),[]).append(n)
 rows=[];extra={}
 for r in unique.values():
  if r['root']=='public':dest=r['path'];extra[dest]=rec(repo/dest,dest);kind='public'
  elif r['path']in sourcepaths:dest=r['path'];kind='user_original'
  else:
   opts=candidates.get((r['bytes'],r['sha256']),[]);need(opts,'exact public counterpart '+r['path']);dest=sorted(opts,key=lambda x:(not x.startswith(SCI+'/'),len(x),x))[0];kind='public'
   if(repo/dest).exists():extra[dest]=rec(repo/dest,dest)
  rows.append(dict(r,from_root=kind,from_path=dest))
 write('public_input_routes.json',dict(input_packet=NUM+'/packet/inputs/input',routes=rows,user_original_count=len(sourcepaths),user_original_assets_distributed=False,source_text_assets_exported=False,purpose='Reconstruct only exact declared paths in a fresh private directory; run unchanged accepted input checker.'))
 write('recount_retained_public.json',dict(files=list(extra.values())))
 print(json.dumps(dict(routes=len(rows),user_originals=len(sourcepaths),retained_public_files=len(extra))))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();prepare(a.study_root,a.repo)
