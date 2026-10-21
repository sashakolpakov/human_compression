#!/usr/bin/env python3
"""Current two-source Representation: exact admissions and complete cost scope."""
import argparse, hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction
from pathlib import Path
from pypdf import PdfReader
P='papers/topic-representation/v3/packet/'
A='audit/topic-representation/v3/'
PINS=['0e3911279dc5aba060b0dca1e00108134567aec58f44eae9738ce80434a8322f','b855471dbb35482443c1047e3910e17f07cdbb08ed40bba4c51d716526ddf58a','245c635d713ad0b2ad3c9667405af0e61ced5360a5b3573646b19da8617dbdd1','1412b88efdd3985fd5d6332420660808b20bba732287beda43baad1c563cc3c3','4c61d955ddc8178c759e7943cde62deefb3c6696878a54d095146e207e5c8b29','3c103ab2a8991bbbd532e572b5fead2940783de74bcb71d480263d102be6f8f1','6455c8cb576814818bd563dcb12d776aeff829fbebfad19d90686f7736334a1e','2b9f3078221231d7db32b17d20517531ca3956ba5caa8fbab6f18b3b2bf645d3','ae53e8aa210bb54fcaf57861f2ff17b279ceb40193c8085b845a53f573331ebb','e52ed6fff70311e54c866402da59d69912d4e07b560956f365f4175049364f4e']
def need(x,m):
 if not x:raise ValueError('REPRESENTATION_V3: '+m)
def validate(a,n,r,inputs):
 need(a['status']=='ROOT_ADMITTED_CORRECTED_PRINCIPAL_CONTRACTS_AND_SYMMETRIC_MEASUREMENT' and a['source_ids']==['F010','L126']and a['principal_originals_added']==['L126']and a['retained_originals']==['F010'],'source admission')
 need(a['source_pages']=={'F010':13,'L126':13}and a['whole_common_pages']==13 and a['whole_application_pages']=={'F010':4,'L126':12}and a['program_appendix_pages']==16,'complete pages')
 need(a['source_dispositions']==dict(F010_principal_blocks=6,L126_dispositions=31),'full source disposition map')
 need(a['computation']==dict(required_programs=1,required_graph_data_files=1,optional_programs=9,orchestration_helpers=2,partial_Lean_files=4,partial_declarations=22),'complete required/optional/formal scope')
 need(a['no_sibling_application_dependency']and a['whole_common_paid_once']and a['symmetric_program_exclusion']and not a['whole_source_formalized']and not a['optional_validation_is_prerequisite']and not a['cross_topic_discount'],'dependency or symmetric scope')
 need(a['original_intake_added']==a['new_question_credit']==a['new_formal_credit']==0 and a['software_inclusive_factor']is a['historical_source_software_cost']is None and a['unknown_costs']==r['unknown_costs']and all(x is None for x in a['unknown_costs'].values()),'unknown costs or credit')
 need([x['sha256']for x in a['accepted_packets']]==PINS,'distinct acceptance pins')
 need(n['status']=='ROOT_ADMITTED_REPRESENTATION_SUCCESSOR_NUMERICAL_COMPARISON'and n['source_ids']==a['source_ids']and n['accepted_packets']==a['accepted_packets'][4:]and n['primary']==a['primary']==r['primary'],'numerical admission')
 need(a['primary_coordinate']==r['primary_coordinate'],'summary primary policy')
 need(n['coordinates']==a['coordinates']==r['coordinate_count']==30 and n['exact_fractions']==a['exact_fractions']==r['exact_fraction_count']==90,'complete sensitivities')
 need(n['whole_common_paid_once']and n['no_sibling_application_dependency']and n['software_inclusive_factor']is None and n['new_question_credit']==n['new_formal_credit']==0,'numeric summary')
 need(r['scope']==dict(F010_blocks=6,L126_dispositions=31,whole_common_once=True,both_complete_applications=True,no_sibling_application_dependency=True,programs_excluded_symmetrically=True,optional_validation_required_for_conditional=False,required_certificate_and_graph_data_for_L126=True,retained_classical_premises_acquired=True,whole_required_files_never_discounted=True,full_source_formalized=False,partial_Lean_declarations=22,software_inclusive_factor=None,source_software_cost=None),'exact prerequisite boundary')
 seen=set();count=0
 for c in r['coordinates']:
  v,f,u=[c[k]for k in ['variant','normalization','unit']];need((v,f,u)not in seen,'duplicate coordinate');seen.add((v,f,u))
  costs={k:d['variants'][v][f][u]for k,d in inputs['documents'].items()};raw={role:sum(x['metrics'][f][u]for x in inputs['raw_files'].values()if x['role']==role)for role in {x['role']for x in inputs['raw_files'].values()}}
  need(c['costs']==costs and c['raw_costs']==raw,'accepted complete coordinate')
  total=dict(source=costs['F010']+costs['L126'],common=costs['U_R'],applications=costs['R1']+costs['R2'],written=costs['U_R']+costs['R1']+costs['R2']);need(c['totals']==total,'complete sum')
  defs={'written':(total['source'],total['written']),'conditional_F010':(costs['F010'],costs['R1']),'conditional_L126':(costs['L126'],costs['R2'])};need(set(c['comparisons'])==set(defs),'asymmetric ratio added')
  for k,(num,den)in defs.items():
   q=Fraction(num,den)
   with localcontext()as ctx:ctx.prec=50;decimal=format(Decimal(num)/Decimal(den),'.12f')
   need(c['comparisons'][k]==dict(numerator=num,denominator=den,reduced_numerator=q.numerator,reduced_denominator=q.denominator,decimal=decimal),'exact fraction');count+=1
  need(c['software_inclusive_factor']is None and c['inventory']==dict(printed_all10_programs=costs['CODE'],raw_all10_programs=raw['required_finite_certificate']+raw['optional_validation'],mandatory_graph_data=raw['required_graph_data'],printed_and_raw_code_are_alternatives=True,data_is_not_in_printed_code=True,source_software_cost=None),'whole data and software inventory')
 need(len(seen)==30 and count==90 and r['primary_coordinate']==['calibrated_selected','NFC','characters_without_whitespace'],'primary and coordinates')
 need(r['primary']['totals']==dict(source=60472,common=36715,applications=45437,written=82152),'whole expansion cost')
 need(r['acquisition']['L126_required_software']==['certificate/check.py','certificate/graph.json']and r['acquisition']['F010_required_software']==[]and r['acquisition']['optional_validation_is_not_prepaid'],'actual mandatory acquisition')
 return count

def verify(root):
 def read(p):return json.loads((root/p).read_text())
 def bind(e):
  p=Path(e['path']);need(not p.is_absolute()and '..'not in p.parts,'unsafepath');b=(root/p).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'binding '+str(p))
 a=read(A+'admission.json');n=read(A+'measurement/admission.json');r=read(A+'measurement/packet/results.json');inputs=read(A+'measurement/inputs/author_counts.json')
 count=validate(a,n,r,inputs)
 need(a['reader']['path']==n['reader']['path']==A+'measurement/packet/reader.pdf'and a['measurement']['path']==A+'measurement/packet/results.json'and n['scientific_admission']['path']==A+'admission.json','current public routes')
 need([x['path']for x in a['required_graph']]==[P+'certificate/check.py',P+'certificate/graph.json'],'both literal required inputs')
 for row in a['artifacts']+a['accepted_packets']+[n['scientific_admission'],a['reader'],a['measurement'],n['reader'],a['source_contract'],a['scientific_scope'],a['retained_F010_contract']]+a['required_graph']:bind(row)
 files=0
 for row in a['accepted_packets']:
  folder=Path(row['path']).parent
  for e in read(row['path'])['exports']:bind(dict(e,path=str(folder/e['path'])));files+=1
 need(read(A+'root_adoption/adoption.json')['no_sibling_application_dependency']and read(A+'measurement/root_adoption/adoption.json')['status']=='ROOT_ACCEPTED_REPRESENTATION_SUCCESSOR_NUMERICAL_COMPARISON','root authorities')
 need(a['source_corrections']==read(A+'root_adoption/adoption.json')['source_corrections'],'exact corrected source attribution')
 s=read(P+'scope.json');need(s['source_rows']==a['source_dispositions']and s['unresolved_source_questions']==a['unresolved_source_questions']and s['retained_inputs']==a['retained_inputs'],'scientific correction scope')
 for file,pages in [('umbrella',13),('finite-normal-pairs',4),('representations-by-incidence',12),('program-appendix',16)]:need(len(PdfReader(root/P/'volume'/f'{file}.pdf').pages)==pages,'whole rendered PDF')
 need(len(inputs['raw_files'])==17 and Counter(x['role']for x in inputs['raw_files'].values())==dict(required_finite_certificate=1,required_graph_data=1,optional_validation=9,current_orchestration_driver=2,partial_formal_evidence=4),'17 whole actual files')
 for path,row in inputs['raw_files'].items():bind(dict(row,path=P+path))
 return dict(status='PASS_REPRESENTATION_SUCCESSOR',sources=2,new_originals=['L126'],source_dispositions=31,retained_F010_blocks=6,exact_fractions=count,packet_exports=files,whole_raw_files=17,partial_declarations=22,software_inclusive_factor=None)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);print(json.dumps(verify(p.parse_args().repo),indent=2))
