#!/usr/bin/env python3
"""Derive Topic C arithmetic from accepted complete-document measurements."""
import argparse,csv,hashlib,json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
PAIRS=(('L088','C1'),('N013','C2'),('L108','C3'),('F014','C4'))
PINS={'inputs/manifest.json':'2d7362de8060e5e20be435193b7c95c40b67799508cb84d086d37425db5acb00','independent/manifest.json':'da559bab5cf59c5441ebbe7e7e06943ce653d1adf2947d2cf2b8dd7243dc628a'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def inputs(root):
 for n,pin in PINS.items():need(sha(root/n)==pin,'accepted input manifest')
 for folder in ['inputs','independent']:
  for r in load(root/folder/'manifest.json')['exports']:
   q=root/folder/r['path'];need(q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'complete bound input export')
 review=load(root/'independent/review.json');need(review['status']=='ACCEPT_INDEPENDENT_DOCUMENT_MEASUREMENT','independent input acceptance')
 return load(root/'inputs/author_counts.json'),load(root/'independent/recount.json'),load(root/'inputs/replacement_input_spec.json')
def derive(author,recount,spec):
 docs=author['documents'];need(set(docs)=={'L088','N013','F014','U_C','C1','C2','C3','C4','CODE'},'exact nine PDFs')
 need(docs==recount['documents'],'independent complete PDF measurements')
 need(author['raw_program_alternative']==recount['raw_program_alternative'],'independent complete raw programs')
 need(author['source_pdf_metrics_unknown']=={'L108':None} and author['four_source_pdf_total'] is None,'L108 unknown')
 programs=spec['required_mathematical_programs'];raw=author['raw_program_alternative']
 need(len(programs)==2 and {Path(p['path']).name for p in programs}==set(raw),'two complete required programs')
 for p in programs:
  r=raw[Path(p['path']).name];need(r['sha256']==p['sha256'] and r['bytes']==p['bytes'],'program hash and full byte count')
 coords=[]
 for variant in VARIANTS:
  for form in ('NFC','NFKC'):
   for unit in UNITS:
    costs={k:d['variants'][variant][form][unit] for k,d in docs.items()}
    common=costs['U_C'];local=sum(costs[a] for s,a in PAIRS);written=common+local;code=costs['CODE'];rawcost=sum(r['variants'][form][unit] for r in raw.values());known=sum(costs[s] for s,a in PAIRS if s in costs)
    pairs=[]
    for source,app in PAIRS:
     n=costs.get(source);den=costs[app];f=None if n is None else Fraction(n,den)
     pairs.append(dict(source=source,application=app,source_cost=n,application_cost=den,fraction=None if f is None else str(f),factor=None if f is None else float(f)))
    formulas={k:dict(unknown_source='L108',unknown_numerator_coefficient=1,known_numerator=known,denominator=den,overall_factor=None) for k,den in [('complete_printed_programs',written+code),('written_papers_only',written),('complete_raw_programs',written+rawcost)]}
    coords.append(dict(variant=variant,normalization=form,unit=unit,common_theory=common,all_applications=local,written_denominator=written,complete_printed_program_cost=code,complete_raw_program_cost=rawcost,complete_denominator=written+code,raw_program_denominator=written+rawcost,known_source_sum=known,unknown_source='L108',complete_source_sum=None,overall_factor=None,overall_formulas=formulas,per_result=pairs))
 primary=next(r for r in coords if (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
 return dict(status='DERIVED_FROM_ACCEPTED_COUNTS_PENDING_INDEPENDENT_ARITHMETIC_REVIEW',primary=primary,coordinates=coords,known_conditional_fractions=90,unknown_conditional_coordinates=30,unknown_overall_coordinates_per_representation=30,
  primary_program_representation='Complete printed CODE appendix once',alternative_program_representation='Both complete raw programs once, instead of CODE; never added to CODE',raw_program_metrics_summed_per_file=True,
  complete_common_and_programs_prepaid_for_conditional_factors=True,common_theory_discount_for_other_topics=False,all_four_applications_charged=True,required_mathematical_programs=programs,raw_program_total_bytes=sum(r['bytes'] for r in raw.values()),
  outside_proof_cost=None,unextracted_graphic_cost=None,minimum_mathematical_complexity=None,source_pages_available=33,replacement_scientific_pages=27,required_program_appendix_pages=4,L108_pdf_pages=None,source_scope_rows=40,new_source_credit=0,new_question_credit=0)

def csv_rows(result):
 overall=[];conditional=[]
 for r in result['coordinates']:
  key={k:r[k] for k in ['variant','normalization','unit']}
  for representation,f in r['overall_formulas'].items():
   overall.append(dict(**key,representation=representation,common_theory=r['common_theory'],all_applications=r['all_applications'],program_cost=(0 if representation=='written_papers_only' else r['complete_raw_program_cost'] if representation=='complete_raw_programs' else r['complete_printed_program_cost']),known_source_sum=r['known_source_sum'],unknown_source='L108',complete_denominator=f['denominator'],overall_factor='unknown',formula=f"(x+{r['known_source_sum']})/{f['denominator']}"))
  for q in r['per_result']:conditional.append(dict(**key,source=q['source'],application=q['application'],source_cost='unknown' if q['source_cost'] is None else q['source_cost'],application_cost=q['application_cost'],fraction='unknown' if q['fraction'] is None else q['fraction'],factor='unknown' if q['factor'] is None else q['factor'],prepaid='whole U_C and both complete programs'))
 return overall,conditional

def write_csv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True,help='Fresh output directory');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 result=derive(*inputs(HERE));result['bindings']={str(p.relative_to(HERE)):sha(p) for p in [HERE/'inputs/author_counts.json',HERE/'independent/recount.json',HERE/'inputs/protocol.json',HERE/'inputs/replacement_input_spec.json',HERE/'inputs/manifest.json',HERE/'independent/manifest.json',HERE/'independent/review.json',Path(__file__)]}
 a.out.mkdir(parents=True);(a.out/'results.json').write_text(json.dumps(result,indent=2)+'\n');overall,conditional=csv_rows(result);write_csv(a.out/'overall_costs.csv',overall);write_csv(a.out/'conditional_costs.csv',conditional)
 print(json.dumps(dict(primary=result['primary'],overall_csv_rows=len(overall),conditional_csv_rows=len(conditional))))
if __name__=='__main__':main()
