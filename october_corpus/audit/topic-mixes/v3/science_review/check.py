#!/usr/bin/env python3
"""Frozen scope/binding replay; mathematical reading is recorded separately."""
import argparse,hashlib,json,re,copy
from pathlib import Path
from pypdf import PdfReader
PIN='e85c3b18a253545082d49eeef05fba7b661549464d9766f79a42a09817f2c1f4'
SOURCE='b6d437c2a53357d98c2d8b446795c410f9dfc27f7421226183914cb8d5be82c1'
R=Path(__file__).resolve().parent
NAMES=['common_maps_jointly_separate','separates_of_injective_on_one_class','transporter_membership','common_transporter_membership','common_nonempty_transporter_is_coset','equal_color_forces_matched_choice']
def need(x,s):
 if not x:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def scope(s,f,a,u,c):
 need(s['original_id']=='F007' and s['source']['sha256']==SOURCE,'exact original/edition')
 need(len(s['rows'])==54 and sum('physical_page'in r for r in s['rows'])==48,'48 named results plus six explicit dispositions')
 need(not s['required_new_programs'] and s['optional_new_programs']==['check_small_maps.py','companion/check.py'],'only optional new diagnostics')
 need(s['whole_previous_common_papers_remain_charged']and s['numerical_factor']is None and s['historical_software_cost']is None,'whole existing theory and unknown software')
 need(s['whole_source_credit']==0 and s['new_question_credit']==0,'no automatic credit')
 need(f['declarations']==NAMES and f['count']==6 and f['full_source_formalization']is False,'exact scoped formalization')
 rr={r['source_clause']:r for r in s['rows']}
 need('facet chain-equivalence' in rr['Proposition 3.21']['qualification'],'3.21 qualified hypothesis')
 need(rr['Section8 Problem1']['status']==rr['Section8 Problem2']['status']=='unanswered','unsolved first two problems')
 need('finite' in rr['Section8 Problem3']['qualification']and 'No unrestricted infinite' in rr['Section8 Problem3']['qualification'],'Problem3 exact interpretation')
 need(rr['Page25 unnumbered exact chain-class description after Proposition5.10']['status']=='ancillary_not_rederived','unnumbered paragraph not silently claimed')
 need('Proposition 4.14 alone' in a and 'orientable criterion (2)' in a and 'is not asserted' in a and 'same statements follow directly' not in a,'nonorientable correction')
 need('d=h' in c and 'd=hb' in c and 'Exchange the layer names' in c,'corrected construction and degenerate converse')
 need('If $b\\ne c$'in c and 'finite even' in c,'base simplicity and finite facets')
 need('For finite $P$'in u,'finite abstract-isomorphism necessity')

def audit(P,source=None):
 need(sha(P/'manifest.json')==PIN,'exact v2 author freeze');m=load(P/'manifest.json')
 for e in m['exports']:
  p=Path(e['path']);need(not p.is_absolute()and '..'not in p.parts,'safe export');q=P/p;need(q.stat().st_size==e['bytes']and sha(q)==e['sha256'],'bound '+e['path'])
 s=load(P/'source_contract.json');f=load(P/'formal_scope.json');a=(P/'faithfulness_application.tex').read_text();u=(P/'relations_and_flags.tex').read_text();c=(P/'companion/rank_three.tex').read_text();scope(s,f,a,u,c)
 named={r['source_clause']for r in s['rows']if 'physical_page'in r};need(named==set(load(R/'source_review.json')['named_results']),'exact independently read named scope')
 if source:
  need(sha(source)==SOURCE and source.stat().st_size==698883,'primary binding');pages=PdfReader(source).pages;need(len(pages)==29,'29 complete primary pages');t='\n'.join(p.extract_text()or''for p in pages);seen={' '.join(x)for x in re.findall(r'(?m)^(Lemma|Proposition|Corollary|Theorem)\s+([3-7]\.\d+)(?=\s)',t)};need(seen==named,'48 literal primary named rows')
 need(load(P/'companion/manifest.json')['scope'].startswith('Bounded F007'),'companion does not itself claim full review')
 raw=(P/'RelationFibers.lean').read_text();clean=re.sub(r'/\-.*?\-/|--[^\n]*','',raw,flags=re.S);need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',clean),'no formal placeholder')
 need(re.findall(r'^theorem\s+(\w+)',clean,re.M)==NAMES,'six actual types')
 pages={x:len(PdfReader(P/x).pages)for x in ['relations_and_flags.pdf','faithfulness_application.pdf','companion/rank_three.pdf']};need(list(pages.values())==[4,5,4],'all13 replacement pages')
 cases=[('omit required proposition',lambda z:z[0]['rows'].pop(0)),('drop facet equivalence qualification',lambda z:next(r for r in z[0]['rows']if r['source_clause']=='Proposition 3.21').update(qualification='literal path')),('claim open problem1 solved',lambda z:next(r for r in z[0]['rows']if r['source_clause']=='Section8 Problem1').update(status='solved')),('claim infinite arbitrary isomorphism',lambda z:next(r for r in z[0]['rows']if r['source_clause']=='Section8 Problem3').update(qualification='All infinite isomorphisms')),('claim paragraph25 recovered',lambda z:next(r for r in z[0]['rows']if r['source_clause'].startswith('Page25')).update(status='recovered')),('validation made required',lambda z:z[0]['required_new_programs'].append('check_small_maps.py')),('old common free',lambda z:z[0].update(whole_previous_common_papers_remain_charged=False)),('full source Lean claim',lambda z:z[1].update(full_source_formalization=True)),('new question credit',lambda z:z[0].update(new_question_credit=1)),('restore nonorientable assertion',lambda z:z.__setitem__(2,z[2].replace('Proposition 4.14 alone','the same statements'))),('restore wrong torus mark',lambda z:z.__setitem__(4,z[4].replace('d=hb','d=ha')))]
 rejected=[]
 for name,mutate in cases:
  z=copy.deepcopy([s,f,a,u,c]);mutate(z)
  try:scope(*z)
  except(ValueError,KeyError):rejected.append(name)
  else:raise ValueError('accepted bad scope '+name)
 return dict(status='PASS_DISTINCT_SCOPE_AND_BINDING_REPLAY',author_manifest_sha256=PIN,author_exports=len(m['exports']),named_results=48,other_dispositions=6,partial_Lean_declarations=6,complete_replacement_pages=pages,primary_checked=bool(source),scope_controls_rejected=rejected,warning='This integrity replay does not replace the independent mathematical/source reading recorded in proof_reading.json and source_review.json.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');d=audit(a.packet,a.source);a.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
