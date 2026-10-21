#!/usr/bin/env python3
"""Collect exact certificate outputs; never substitute source expectations for actual results."""
import argparse, hashlib,json,pathlib,re,shutil
HERE=pathlib.Path(__file__).resolve().parent

def bind(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def one(text,key):
 m=re.search(r'^'+re.escape(key)+r' (.*)$',text,re.M);assert m,key;return m[1]
def parse(row,folder):
 receipt=json.loads((folder/'receipt.json').read_text());text=(folder/'stdout').read_text()
 assert receipt['status'].startswith('PASS') and ('PASS_L003_ROW '+row['id']) in text
 rotation=int(one(text,'ROTATION_ORDER'));full=int(one(text,'FULL_ORDER'))
 localstr=one(text,'MARKED_LOCAL_PRESENTATIONS')
 pat=r'\[\s*(\d),\s*"([^"]+)",\s*(\[[^\]]*\]),\s*("[^"]*"|\d+),\s*(\d+),\s*(\[(?:[^\[\]]|\[[^\]]*\])*\]),\s*\['
 locals=[]
 for i,kind,params,upper,actual,hnf in re.findall(pat,localstr):
  locals.append({'omitted_type':int(i)-1,'kind':kind,'literal_period_parameters':json.loads(params),'literal_standard_local_order':json.loads(upper),'actual_marked_local_order':int(actual),'actual_translation_kernel_basis':json.loads(hnf)})
 assert len(locals)==4,(row['id'],localstr)
 failed=json.loads(one(text,'INVERTED_RELATOR_FAILURES'));regularity='chiral' if failed else 'regular'
 return {'id':row['id'],'literal_parameters':row['literal_parameters'],'source_full_order':row['source_full_automorphism_order'],'actual_rotation_order':rotation,'actual_full_type_preserving_order':full,'source_regularity':row['source_regularity'],'actual_regularity':regularity,'source_full_order_matches':full==row['source_full_automorphism_order'],'pair_orders':json.loads(one(text,'PAIR_ORDERS')),'all_16_Cplus_subgroup_orders':json.loads(one(text,'ICPLUS_SUBGROUP_ORDERS')),'Cplus_intersection_pairs':256,'normalized_rotation_flags':json.loads(one(text,'ROTATION_FLAGS')),'actual_rank_two_residues':json.loads(one(text,'RANK2_RESIDUES')),'marked_residues':locals,'failed_inverse_relators':failed,'regular_full_IP_pairs':256 if regularity=='regular' else None,'regular_normalized_flags':json.loads(one(text,'FULL_FLAGS')) if regularity=='regular' else None,'proof_route':'complete fp isomorphism' if row['id']!='T8.8' else 'completed ACE index17280 times independent local upper150 equals image2592000','receipt':bind(folder/'receipt.json'),'stdout':bind(folder/'stdout'),'stderr':bind(folder/'stderr'),'group_type_column':'exact marked presentation and permutation group established; printed extension abbreviation not yet independently identified'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--batches',nargs='+',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args()
 found={}
 for batch in args.batches:
  for rec in json.loads((batch/'report.json').read_text())['rows']:
   if rec['status'].startswith('PASS'):found[rec['id']]=batch/rec['id']
 rows=json.loads((HERE/'table_roster.json').read_text())['rows'];results=[];missing=[]
 for row in rows:
  if row['prior_reuse_route'] is not None:continue
  if row['id'] not in found:missing.append(row['id']);continue
  results.append(parse(row,found[row['id']]))
 output={'status':'AUTHOR_COMPUTED_LITERAL_FINITE_ROWS_NOT_INDEPENDENT_ACCEPTANCE','rows':results,'completed':len(results),'missing':missing,'source_order_discrepancies':[r['id'] for r in results if not r['source_full_order_matches']],'local_parameter_collapses':[{'row':r['id'],'omitted_type':loc['omitted_type'],'standard_order':loc['literal_standard_local_order'],'actual_order':loc['actual_marked_local_order']} for r in results for loc in r['marked_residues'] if loc['literal_standard_local_order']!=loc['actual_marked_local_order']],'proof_scope':'All computed rows have exact universal orders, marked local quotient presentations/lattices, IC+, actual flags and connectivity, and regular/chiral tests. Named extension abbreviations and complete source-wide migration remain separate.'}
 args.out.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('rows','proof_scope')},indent=2))
if __name__=='__main__':main()
