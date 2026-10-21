#!/usr/bin/env python3
"""Distinct B5 arithmetic from independent recount and accepted old B data."""
import argparse,copy,csv,hashlib,itertools,json
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
from pypdf import PdfReader
import xml.etree.ElementTree as ET
from plot_checks import need,svg_check,pdf_check
V=['raw_untrimmed','raw_selected','calibrated_selected']
N=['NFC','NFKC']
U=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
AUTHOR='d2235b7763974660f93b0f7b0e5fc18a3a5c5768fdb15544dc1ce55579eec886'
REVIEW='d757974f2f82f4758d60b46a69aaf16a1b8fa458485ca01cb3f1c6887bd88f91'
OLD='5e2a72716609b460b87d96c8906bbfc619a2f315b5ab030b9d94700fe9bb3dbb'
def read(p):return json.loads(p.read_text())
def checked(p,h):
 need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'bound file '+str(p));return read(p)
def exports(p,h):
 m=checked(p/'manifest.json',h)
 for x in m['exports']:
  b=(p/x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'export '+x['path'])
def reconstruction(old,recount):
 expected={}
 for v,n,u in itertools.product(V,N,U):
  hits=[r for r in old['rows'] if tuple(r[k] for k in ['topic','PDF_variant','normalization','unit'])==('B',v,n,u)]
  need(len(hits)==1,'old coordinate');b=hits[0]
  new={k:x['metrics'][v][n][u] for k,x in recount['documents'].items()}
  pairs=[tuple(x[k] for k in ['source','application','source_cost','application_cost','source_representation']) for x in b['individual']]
  need([x[0] for x in pairs]==['N001','N003','N008','L030'],'old original roster')
  pairs.append(('L040','B5',new['L040'],new['A5'],'complete_PDF_'+v))
  inv={c:{p:x['metrics'][n][u] for p,x in files.items()} for c,files in recount['raw_files'].items()}
  expected[v,n,u]=dict(pairs=pairs,common={'U_B_previous':b['common_theory'],'U_B_high_rank':new['U_ADD']},printed={'previous_complete_bundle':b['printed_program_cost'],'new_complete_appendix':new['CODE']},raw={'previous_complete_files':b['raw_program_alternative'],'new_complete_files':sum(inv['programs'].values())},inventory=inv,article=recount['source_article_only'][v][n][u])
 return expected

def arithmetic(r,expected):
 need(r['topic']=='B' and r['original_manuscripts']==5 and r['additional_originals']==1 and r['new_topics']==0,'scope')
 need(r['coordinates']==30 and r['main_exact_fractions']==240 and r['cover_sensitivity_fractions']==120,'counts')
 need(r['whole_new_programs']==4 and r['program_roles']==dict(principal_required=1,validation=2,auxiliary_example=1),'whole programs')
 need(r['operational_drivers']==2 and r['new_partial_formal_declarations']==8 and not r['full_formalization_claim'],'formal scope')
 need(r['new_source_credit']==r['new_question_credit']==0 and all(x is None for x in r['unknown_costs'].values()),'credits and unknowns')
 need(all(r[k] for k in ['full_old_common_retained','full_new_common_retained','source_cover_retained_in_primary','source_contracts_unchanged','old_measurements_unchanged']),'complete closure')
 rows={tuple(x[k] for k in ['variant','normalization','unit']):x for x in r['rows']}
 need(set(rows)==set(expected) and len(r['rows'])==30,'all coordinates exactly once')
 facts={}
 def exact(q,s,d):
  f=Fraction(s,d)
  with localcontext() as ctx:
   ctx.prec=40;dec=str(Decimal(s)/Decimal(d))
  need(q==dict(numerator=s,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=dec),'fraction')
  return s,d,dec
 for key,e in expected.items():
  row=rows[key];v,n,u=key
  s=sum(x[2] for x in e['pairs']);a=sum(x[3] for x in e['pairs']);c=sum(e['common'].values());p=sum(e['printed'].values());raw=sum(e['raw'].values())
  need(row['topic']=='B' and row['original_manuscripts']==5,'row scope')
  need(row['source_sum']==s and row['applications']==a and row['written_denominator']==c+a,'whole sums')
  need(row['common_components']==e['common'] and row['common_theory']==c,'entire common papers')
  need(row['printed_program_components']==e['printed'] and row['printed_program_cost']==p,'whole printed appendix')
  need(row['raw_program_components']==e['raw'] and row['raw_program_alternative']==raw,'whole raw programs')
  need(row['new_raw_file_inventory']==e['inventory'],'raw inventory')
  need(row['conditional_acquisition']==dict(full_common=c,full_printed_programs=p,full_raw_programs=raw,printed_and_raw_are_alternatives=True),'full conditional acquisition')
  for kind,d in [('written',c+a),('including_printed_programs',c+a+p),('including_raw_programs',c+a+raw)]:facts['B','all','full_originals',v,n,u,kind]=exact(row['whole'][kind],s,d)
  need(len(row['individual'])==5,'five applications')
  for got,want in zip(row['individual'],e['pairs']):
   need(tuple(got[k] for k in ['source','application','source_cost','application_cost','source_representation'])==want,'complete original and application')
   facts['B',want[0],'full_originals',v,n,u,'conditional_application']=exact(got['conditional'],want[2],want[3])
  art=row['article_only_sensitivity'];sa=s-e['pairs'][-1][2]+e['article']
  need(art['L040_article_cost']==e['article'] and art['source_sum']==sa,'direct article extraction')
  need(all(art[k] for k in ['earlier_four_conditionals_unchanged','all_replacement_costs_unchanged','direct_article_extraction']),'only cover boundary changes')
  for kind,d in [('written',c+a),('including_printed_programs',c+a+p),('including_raw_programs',c+a+raw)]:facts['B','all','L040_article_only',v,n,u,kind]=exact(art['whole'][kind],sa,d)
  facts['B','L040','L040_article_only',v,n,u,'conditional_application']=exact(art['L040_conditional'],e['article'],e['pairs'][-1][3])
 need(r['primary']=={'B':rows[V[0],N[0],U[2]]},'raw untrimmed primary')
 need(len(facts)==360,'360 fractions');return facts

def bars(e):
 s=sum(x[2] for x in e['pairs']);a=sum(x[3] for x in e['pairs']);c=sum(e['common'].values());p=sum(e['printed'].values())
 return [('bar-B-'+name,role,cost,bottom) for name,role,cost,bottom in [('source','source',s,0),('common-written','common',c,0),('application-written','application',a,c),('common-printed','common',c,0),('application-printed','application',a,c),('program','program',p,c+a)]]

def main():
 ap=argparse.ArgumentParser()
 for name in ['author','input-review','public-root','out']:ap.add_argument('--'+name,type=Path,required=True)
 q=ap.parse_args();need(not q.out.exists(),'fresh output');q.out.mkdir(parents=True)
 exports(q.author,AUTHOR);exports(q.input_review,REVIEW)
 old=checked(q.public_root/'audit/available-text/v1/packet/results.json',OLD)
 expected=reconstruction(old,read(q.input_review/'recount.json'));r=read(q.author/'results.json');f=arithmetic(r,expected)
 seen={}
 for x in csv.DictReader((q.author/'comparisons.csv').open()):
  k=tuple(x[z] for z in ['topic','source','source_boundary','variant','normalization','unit','comparison'])
  need(k not in seen,'unique CSV row');seen[k]=int(x['numerator']),int(x['denominator']),x['decimal']
 need(seen==f,'all CSV fractions')
 b=bars(expected[V[0],N[0],U[2]]);svg=(q.author/'whole_costs.svg').read_bytes()
 sn=svg_check(svg,b);pn=pdf_check(q.author/'whole_costs.pdf',b)
 controls=[]
 for label,mutate in [('erase common',lambda z:z['rows'][0]['common_components'].update(U_B_previous=0)),('erase new common',lambda z:z['rows'][0]['common_components'].update(U_B_high_rank=0)),('erase program',lambda z:z['rows'][1].update(raw_program_alternative=0)),('alter exact factor',lambda z:z['rows'][0]['whole']['written'].update(denominator=1)),('erase acquisition',lambda z:z['rows'][0]['conditional_acquisition'].update(full_common=0)),('unknown to zero',lambda z:z['unknown_costs'].update(external=0)),('clauses as manuscripts',lambda z:z.update(original_manuscripts=35)),('cover subtracted from denominator',lambda z:z['rows'][0]['article_only_sensitivity']['whole']['written'].update(denominator=1)),('roles conflated',lambda z:z['program_roles'].update(principal_required=4))]:
  wrong=copy.deepcopy(r);mutate(wrong)
  try:arithmetic(wrong,expected)
  except ValueError:controls.append(label)
  else:raise ValueError('control accepted '+label)
 for gid in ['bar-B-common-written','bar-B-application-printed']:
  root=ET.fromstring(svg)
  for group in root.iter():
   if group.get('id')==gid:next(x for x in group.iter() if x.tag.endswith('path')).set('d','M 0 0 L 1 0 L 1 1 L 0 1 z')
  try:svg_check(ET.tostring(root),b)
  except ValueError:controls.append('distorted '+gid)
  else:raise ValueError('graph control accepted')
 pages=PdfReader(q.author/'measurement.pdf').pages;need(len(pages)==2,'two-page reader');text='\n'.join(p.extract_text() or '' for p in pages)
 pr=r['primary']['B']
 for val in list(pr['whole'].values())+[x['conditional'] for x in pr['individual']]+list(pr['article_only_sensitivity']['whole'].values())+[pr['article_only_sensitivity']['L040_conditional']]:need(f"{float(val['decimal']):.3f}" in text,'reader factor')
 report=dict(status='PASS_DISTINCT_NUMERICAL_REVIEW',coordinates=30,main_fractions=240,direct_cover_sensitivity_fractions=120,csv_rows=360,svg_bars=sn,pdf_bars=pn,baselines_and_stacking=True,independent_controls=controls,primary=pr,new_source_credit=0,new_question_credit=0,source_extraction_repeated=False,scientific_programs_executed=False)
 (q.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
