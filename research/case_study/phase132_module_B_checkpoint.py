#!/usr/bin/env python3
"""Create an additive Module B author checkpoint; no mathematical census is run."""
import argparse, hashlib, json, re, shutil, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def binding(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def span(s,a,b):
 t=s[a:b];return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(t.encode()),'bytes':len(t.encode()),'NFC_whitespace_tokens':len(unicodedata.normalize('NFC',t).split())}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 if a.output.exists():raise SystemExit('Refusing existing output')
 s=(ROOT/'phase132_module_B_manuscript.md').read_text();intake=json.loads((ROOT/'phase132_module_B_intake.json').read_text());u=json.loads((ROOT/'phase123_umbrella_v2_contracts.json').read_text())
 heads=list(re.finditer(r'^\*\*(?:Theorem|Proposition|Lemma|Corollary) (B\.[A-Za-z0-9]+)',s,re.M))
 nodes={}
 for i,m in enumerate(heads):
  end=heads[i+1].start() if i+1<len(heads) else s.index('## References and retained inputs')
  # Give theorem blocks their actual preparatory context rather than omitting it.
  start=m.start()
  if m.group(1)=='B.F':start=s.index('## 2. A common forest')
  if m.group(1)=='B.Star':start=s.index('## 7. Weighted stars')
  if m.group(1)=='B.Aut':start=s.index('### 7.2. Recovering the types')
  nodes[m.group(1)]={'span':span(s,start,end),'includes_complete_proof':True,'formal_coverage':'written_proof_no_complete_exact_Lean_bridge_claimed'}
 deps={
 'B.Flags':[], 'B.F':['retained:Coset'], 'B.P':['B.F'],
 'B.Overgroups':[], 'B.Minimal':['B.F','B.Overgroups'],
 'B.Diagram':['B.Minimal','retained:B97'],
 'B.RelativeApplication':['B.Flags','U.RelativeBound','U.Relative'],
 'B.Blocks':['B.RelativeApplication','retained:W1'],
 'B.Extremal':['B.Blocks','B.F','B.P','B.Overgroups','retained:W1','retained:W2'],
 'B.Count':['B.Extremal','retained:Cayley'],
 'B.MaxRank':['B.F','B.P','B.Minimal','B.RelativeApplication','B.Extremal','B.Overgroups','retained:AutSn'],
 'B.FrattiniApplication':['B.Flags','U.FrattiniLadder','U.Coset','U.FrattiniTransport','U.Maximal'],
 'B.Coordinates':['B.FrattiniApplication','B.RelativeApplication','U.FrattiniLadder','retained:Pphi'],
 'B.Star':['B.F'], 'B.Distance':[], 'B.Johnson':[],
 'B.TypedAut':['B.Johnson','B.Distance','B.Star'], 'B.Aut':['B.TypedAut'],
 'B.BC98':['B.Diagram','B.Minimal','B.Overgroups','retained:B97'],
 'B.CC02':['B.Extremal','B.F','B.P','B.Count','B.MaxRank','B.RelativeApplication'],
 'B.ACK05':['B.FrattiniApplication','B.Coordinates','U.FrattiniTransport','U.FrattiniLadder'],
 'B.GL21':['B.Star','B.Distance','B.TypedAut','B.Aut']}
 for k,v in nodes.items():v['direct_dependencies']=deps[k]
 target_map={
 'A1':['B.BC98','B.Minimal','B.Diagram'],'A2':['B.BC98','B.Minimal'],'A3':['B.BC98','B.Overgroups'],'A4':['B.BC98','B.Minimal'],
 'B1':['B.RelativeApplication'],'B2':['B.Extremal','B.F','B.P'],'B3':['B.Count'],'B4':['B.Extremal','B.F','B.P'],'B5':['B.Extremal'],'B6':['B.RelativeApplication'],'B7':['B.MaxRank'],'B8':['B.MaxRank'],
 'C1':['B.FrattiniApplication'],'C2':['B.FrattiniApplication'],'C3':['B.FrattiniApplication'],'C4':['B.FrattiniApplication'],'C5':['B.FrattiniApplication'],'C6':['B.Coordinates'],'C7':['B.Coordinates'],'C8':['B.Coordinates'],'C9':['B.Coordinates'],'C10':['B.Coordinates'],'C11':['B.FrattiniApplication'],
 'D1':['B.Star'],'D2':['B.TypedAut','B.Aut'],'D3':['B.Star','B.Distance'],'D4':['B.Star'],'D5':['B.Star'],'D6':['B.Distance'],'D7':['B.Aut','B.Star']}
 rows=[]
 for x in intake['targets']:
  row={k:v for k,v in x.items() if k!='status'};row['application_nodes']=target_map[x['adapter']];row['status']='complete_author_derivation_pending_independent_review';rows.append(row)
 used=['U.Coset','U.RelativeBound','U.Relative','U.Maximal','U.FrattiniTransport','U.FrattiniLadder']
 contracts={x['id']:x for x in u['contracts'] if x['id'] in used}
 # Record all explanatory context in U as part of its fully charged body. The span subtotal is diagnostic only.
 sigbytes=sum(x['statement_binding']['utf8_bytes']+x['complete_proof_binding']['utf8_bytes'] for x in contracts.values())
 source_measures=[]
 for pid,file,begin,end,pages in [
  ('N001','sources/phase16_N001_browser_record.txt',10524,'References [1]',None),
  ('N003','sources/phase10_N003_extracted.txt',0,'References',12),
  ('N008','sources/phase16_frattini_geometries.txt',0,'Acknowledgement.',9),
  ('L030','sources/kneser_revised.txt',0,'Acknowledgements',10)]:
  st=(ROOT/file).read_text();stop=st.index(end,begin) if isinstance(end,str) else end
  source_measures.append({'source_id':pid,'text_file':binding(ROOT/file),'body_span':span(st,begin,stop),'physical_pdf_pages':pages,'metric':'raw_available_transcription_NFC_whitespace; not a normalized-houseformat or PDF-extraction comparison','source_body_boundary':'title through mathematical body before bibliography/acknowledgments; extraction page markers retained; exact codepoint boundaries bound'})
 app=binding(ROOT/'phase132_module_B_manuscript.md');ub=binding(ROOT/'phase123_umbrella_manuscript_v2.md')
 d={'schema':'phase132_module_B_author_checkpoint_v1','status':'complete_author_candidate_pending_independent_review','manuscript':app,'umbrella':ub,'node_spans_may_overlap':True,'node_spans_are_not_marginal_proof_costs':True,'nodes':nodes,'targets':rows,'umbrella_used_contracts':contracts,
 'cost':{'application_raw_utf8_bytes':app['bytes'],'application_raw_NFC_whitespace_tokens':len(unicodedata.normalize('NFC',s).split()),'whole_umbrella_raw_utf8_bytes':ub['bytes'],'complete_conservative_U_plus_B_raw_bytes':app['bytes']+ub['bytes'],'required_external_proof_programs':[],'used_U_statement_and_proof_span_bytes_diagnostic_only':sigbytes,'span_subtotal_is_not_complete_dependency_cost':True,'gross_application_addition_over_existing_U_bytes':app['bytes'],'gross_mathematical_removal_from_existing_U_bytes':0,'signed_increment_over_existing_U_bytes':app['bytes'],'model_acquisition_cost_quantified':False,'relocation_counted_as_zero_cost':False,'complete_source_ratio':None},
 'source_complexity_inventory':source_measures,'dependency_ablation_semantics':'Removing a declared dependency removes this written derivation; it does not prove semantic necessity or a lower bound on every possible proof.',
 'retained_input_caveat':'Exact named classical/classification inputs in manuscript and scope remain retained; no hidden project-proof import.',
 'rendering_dependencies':[binding(ROOT/'phase98_twelve_measurement.py'),binding(ROOT/'phase98_twelve_measurement_protocol.json')],
 'historical_proof_bank_dependencies_are_provenance_only':True,'complete_Lean_claim':False,'new_finite_mathematical_replay':False,'historical_novelty_claim':False,'open_conjecture_claim':False}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'target_rows':len(rows),'theorem_nodes':len(nodes),'U+B_bytes':app['bytes']+ub['bytes'],'application_bytes':app['bytes'],'ratio':None}))
if __name__=='__main__':main()
