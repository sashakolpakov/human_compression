#!/usr/bin/env python3
"""Topic D arithmetic from independently accepted complete-document inputs."""
import argparse,csv,hashlib,json
from pathlib import Path
from fractions import Fraction
HERE=Path(__file__).resolve().parent
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
PAIRS=(('L066','D1'),('L074','D2'),('L104','D3'))
PINS={'previous/manifest.json':'86cc1bbd21ce8f73e8aa89049b69248fdbcad521dd0adc1c78e787b0ac8a94d9','inputs/manifest.json':'8f7729bd219adb61212d3e0c6215b7b84a09e798640ee47e3d5688239edb80d0','independent/manifest.json':'61f1d290429b9d30e2c106beb15ee5eaaadce984c433abd68100288aa90c85ff'}
def need(v,s):
 if not v:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def inputs(root):
 for path,h in PINS.items():need(sha(root/path)==h,'exact historical/corrected/review manifest')
 for folder in ['previous','inputs','independent']:
  for e in load(root/folder/'manifest.json')['exports']:
   p=root/folder/e['path'];need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'all unchanged input exports')
 review=load(root/'independent/review.json');need(review['measurement_inputs_accepted'] is True and review['unresolved_corrections']==[],'independent corrected inputs accepted')
 need(review['corrected_proposal_manifest_sha256']==PINS['inputs/manifest.json'] and review['original_proposal_corrected_not_accepted'] is True,'use corrected input edition')
 a=load(root/'inputs/author_counts.json');b=load(root/'independent/recount_corrected.json');spec=load(root/'inputs/replacement_input_spec.json')
 need(set(a['documents'])==set(b['documents'])=={'L066','L074','L104','U_D','D1','D2','D3','CODE'},'exact eight whole PDFs')
 for key,d in b['documents'].items():need({k:a['documents'][key][k] for k in d}==d,'independent document metrics and hashes '+key)
 for group in ['raw_program_alternative','full_drivers_separate']:
  need(set(a[group])==set(b['raw_records'][group]),'all raw files independently measured')
  for key,d in b['raw_records'][group].items():need({k:a[group][key][k] for k in d}==d,'independent raw-file metrics and hashes '+key)
 need(len(spec['complete_mathematical_programs'])==8 and len(spec['complete_drivers'])==2,'complete programs/drivers')
 for group,rs in [('raw_program_alternative',spec['complete_mathematical_programs']),('full_drivers_separate',spec['complete_drivers'])]:
  for row in rs:
   d=a[group][Path(row['path']).name];need(d['sha256']==row['sha256'] and d['bytes']==row['bytes'] and d['classification']==row['classification'],'full program and role')
 return a,b,spec

def fraction(n,d):
 f=Fraction(n,d);return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,exact_fraction=str(f),factor=float(f))

def derive(author,recount,spec):
 docs=author['documents'];raw=author['raw_program_alternative'];drivers=author['full_drivers_separate'];coordinates=[]
 for variant in VARIANTS:
  for form in ['NFC','NFKC']:
   for unit in UNITS:
    costs={k:d['variants'][variant][form][unit] for k,d in docs.items()};u=costs['U_D'];apps=sum(costs[a] for s,a in PAIRS);source=sum(costs[s] for s,a in PAIRS);printed=costs['CODE'];rawcost=sum(x['variants'][form][unit] for x in raw.values());drivecost=sum(x['variants'][form][unit] for x in drivers.values())
    coordinates.append(dict(variant=variant,normalization=form,unit=unit,document_costs=costs,source_sum=source,common_theory=u,all_applications=apps,written_denominator=u+apps,printed_program_cost=printed,raw_program_cost=rawcost,separate_driver_cost=drivecost,comparisons={'written_papers':fraction(source,u+apps),'including_printed_program':fraction(source,u+apps+printed),'including_raw_program_alternative':fraction(source,u+apps+rawcost)},per_result=[dict(source=s,application=a,source_cost=costs[s],application_cost=costs[a],**fraction(costs[s],costs[a])) for s,a in PAIRS],raw_program_role_costs={role:sum(x['variants'][form][unit] for x in raw.values() if x['classification']==role) for role in ['required','diagnostic']}))
 primary=next(c for c in coordinates if (c['variant'],c['normalization'],c['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
 return dict(schema='topic_d_complete_document_measurement_v1',status='AUTHOR_ARITHMETIC_PENDING_INDEPENDENT_REVIEW',public_scientific_commit='2d631760842796450899761f8763b0e9a9ff4b77',public_proof_admission_sha256='65bcfb731a5cab716c6703964fba6e10bb318a2cab91b62107358ac7884ff1ae',primary=primary,coordinates=coordinates,policy_coordinates=30,exact_combined_fractions=90,exact_conditional_fractions=90,source_contract_rows=37,comparison_order=['written_papers','per_result_conditional','including_printed_program','including_raw_program_alternative'],whole_common_paper_charged_once=True,all_three_complete_applications_charged=True,cross_topic_common_discount=False,conditional_prepaid='Whole U_D and the whole complete programme boundary, including five required programs and three complete diagnostics; not a selected local fraction.',program_boundary=dict(complete_programs=8,required=5,diagnostic=3,complete_drivers_separate=2,printed_representation='Whole 12-page appendix, counted once',raw_representation='All eight complete raw programs, alternative to printed appendix, never additional',raw_metrics_summed_per_file=True,no_diagnostic_pruning=True,drivers_not_added_to_any_comparison=True),complete_mathematical_programs=spec['complete_mathematical_programs'],complete_drivers=spec['complete_drivers'],physical_pages=dict(source=26,common=6,applications=[5,6,2],scientific_replacement=19,printed_program=12,total_input_pages=57),source_to_application_sequence=[dict(source=s,application=a,source_pages=docs[s]['pages'],application_pages=docs[a]['pages']) for s,a in PAIRS],raw_file_bytes=dict(programs=sum(x['bytes'] for x in raw.values()),drivers=sum(x['bytes'] for x in drivers.values())),retained_external_proof_cost=None,catalogue_and_algorithm_construction_cost=None,historical_software_cost=None,graphics_and_formula_layout_cost=None,minimal_mathematical_complexity=None,formal_validation_cost_separate=True,formal_source_application_claim=False,missing_original_source_pdfs=[],full_visible_text_claim=False,source_corrections_and_exclusions='Exact accepted 37-row scope retained. In particular L104 diagrams, complete Aut/Cor, doubling and supplement assertions remain excluded; their original extracted text is still counted.',extraction_correction='Fourteen L066 square brackets originally collided with brace components in extracted character encoding. V2 binds actual PDF events/bytes. This font has no ToUnicode stream. Only its calibrated UTF8 totals changed by -28 under each normalization.',new_source_credit=0,new_question_credit=0)

def csv_rows(r):
 overall=[];conditional=[];raw=[]
 for c in r['coordinates']:
  key={k:c[k] for k in ['variant','normalization','unit']}
  for representation,f in c['comparisons'].items():overall.append(dict(**key,representation=representation,source_sum=c['source_sum'],whole_common=c['common_theory'],all_applications=c['all_applications'],program_cost=0 if representation=='written_papers' else c['printed_program_cost'] if representation=='including_printed_program' else c['raw_program_cost'],**f))
  for q in c['per_result']:conditional.append(dict(**key,**q,prepaid=r['conditional_prepaid']))
 return overall,conditional

def write_csv(path,rs):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 r=derive(*inputs(HERE));r['bindings']={n:sha(HERE/n) for n in ['previous/manifest.json','inputs/manifest.json','inputs/protocol.json','inputs/author_counts.json','inputs/replacement_input_spec.json','inputs/source_contract_boundary.json','independent/manifest.json','independent/review.json','independent/recount_corrected.json','compute.py']};a.out.mkdir(parents=True);(a.out/'results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 for n,rows in zip(['overall_costs.csv','conditional_costs.csv'],csv_rows(r)):write_csv(a.out/n,rows)
 print(json.dumps(dict(primary=r['primary'],exact_fractions=180,scope_rows=37)))
if __name__=='__main__':main()
