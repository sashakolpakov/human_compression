#!/usr/bin/env python3
"""Portable numerical replay. Reuses accepted counts, never source extraction."""
from pathlib import Path
import argparse,copy,csv,hashlib,io,json,math,os,re,shutil,subprocess,tempfile
from decimal import Decimal,localcontext
from pypdf import PdfReader
from calculate import R,inputs,derive,outputs,load,need,bound,sha
from presentation import plot,tex
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def validate(r,p,docs,raw):
 """Direct sums and integer gcd checks, separate from the fraction builder."""
 need(r['source_ids']==['F005','L016','F007'] and r['source_count']==3,'three original identities')
 need(r['common_documents']==['U','U1','U2'],'all three whole common papers')
 need(r['application_documents']=={'F005':['A1','A2'],'L016':['A3'],'F007':['A4','A5']},'all five whole applications')
 need(r['primary_coordinate']=='raw_untrimmed/NFC/characters_without_whitespace','fixed primary')
 need(r['source_pages']==62 and r['whole_common_pages']==13 and r['application_pages']=={'F005':12,'L016':6,'F007':9} and r['inventory_pages']==114,'all physical pages')
 need(r['complete_document_metric_vectors']=={k:v['metrics']for k,v in docs.items()},'all accepted450 PDF cells')
 need(r['source_cells_unchanged']==450 and r['raw_cells_unchanged']==170,'all620 input cells')
 keys={'/'.join([v,n,u])for v in p['variants']for n in p['normalizations']for u in p['units']}
 need(set(r['coordinates'])==keys and r['coordinate_count']==30 and r['exact_fraction_count']==120,'all30 coordinates')
 for key,c in r['coordinates'].items():
  v,n,u=key.split('/');d={k:q['metrics'][v][n][u]for k,q in docs.items()}
  need(c['document_costs']==d and c['variant']==v and c['normalization']==n and c['unit']==u,'literal full document vectors')
  S=d['F005']+d['L016']+d['F007'];U=d['U']+d['U1']+d['U2'];A={'F005':d['A1']+d['A2'],'L016':d['A3'],'F007':d['A4']+d['A5']};D=U+sum(A.values())
  need((c['source_sum'],c['whole_common'],c['application_sum'],c['whole_written'])==(S,U,sum(A.values()),D)and c['application_bundles']==A,'whole common and companion sums')
  need(set(c['conditional'])==set(A),'three conditional rows')
  for f,a,b in [(c['written'],S,D)]+[(c['conditional'][s],d[s],A[s])for s in A]:
   g=math.gcd(a,b);num=a//g;den=b//g
   with localcontext()as ctx:ctx.prec=50;dec=format(Decimal(a)/Decimal(b),'.12f')
   need(f==dict(source_cost=a,replacement_cost=b,numerator=num,denominator=den,exact_fraction=str(num)if den==1 else f'{num}/{den}',decimal=dec),'exact reduced fraction')
  inv=c['separate_inventory']
  for group,g in r['whole_file_group_costs'].items():need(inv[group]==g['metrics'][n][u],'raw code inventory only')
  need(inv['required_printed_alternative']==d['REQ']and inv['partial_optional_printed_inventory']==d['VAL']and inv['historical_mixed_printed_inventory']==d['CODE1']+d['CODE2'],'printed full-file alternatives')
  need(inv['full_optional_printed_representation']is None and inv['software_inclusive_factor']is None and inv['original_software_cost']is None,'no unmatched program factor')
 need(r['primary']==r['coordinates'][r['primary_coordinate']],'primary exact coordinate')
 roles=p['program_roles'];required={q['path']for q in roles['required_full_programs']};optional={q['path']for q in roles['optional_full_programs']}
 need(set(r['required_files'])==required and set(r['optional_files'])==optional and len(required)==2 and len(optional)==6,'required never optional')
 need(len(r['whole_file_inventory'])==17 and len({q['path']for q in r['whole_file_inventory']})==17,'unique whole17 rawfiles')
 lookup={path:(group,row)for group,rs in raw.items()for path,row in rs.items()}
 for q in r['whole_file_inventory']:
  group,row=lookup[q['path']];expected=('required_finite_certificate'if q['path']in required else'optional_validation')if group=='programs'else'operational_driver'if group=='drivers'else'partial_formal_evidence'
  need(q['group']==expected and q['inherited_role']==row['role'] and all(q[k]==row[k]for k in['bytes','sha256','metrics']),'whole-file identity/role/all170cells')
 for group,g in r['whole_file_group_costs'].items():
  qs=[q for q in r['whole_file_inventory']if q['group']==group]
  need(g['files']==len(qs)and g['literal_bytes']==sum(q['bytes']for q in qs),'whole group files/bytes')
  for n in p['normalizations']:
   for u in p['units']:need(g['metrics'][n][u]==sum(q['metrics'][n][u]for q in qs),'complete raw group totals')
 need(r['mandatory_nonprogram_data_files']==[]and r['full_required_only_printed_representation']=='REQ' and not r['new_optional_programs_have_printed_representation'],'no hidden data/printed claims')
 need(r['required_printed_coverage']=={'REQ':['topic_Mix_F005_recovery/check_coprime.g','topic_Mix_L016_recovery/base_certificate.g'],'CODE1':['topic_Mix_F005_recovery/check_coprime.g']},'literal printed required coverage')
 need(r['conditional_prepaid']==p['conditional_prepaid']and r['source_scope']==p['source_scope'],'conditional and source scope')
 need(r['software_inclusive_factors']is None and r['optional_validation_inclusive_factors']is None and r['historical_source_software_cost']is None and r['unknown_costs']==p['unknown_costs'],'unknown software/external costs')
 need(r['partial_formal_files']==3 and r['partial_formal_declarations']==12 and not r['full_source_formalized'],'partial Lean only')
 need(r['whole_common_paid_once'] and r['required_certificates_not_optional'] and r['source_and_replacement_programs_excluded'],'symmetric boundary')
 for flag in['overlap_discount','cross_topic_discount','sawtooth_claim','node_count_complexity_factor','source_extraction_repeated','scientific_programs_reexecuted']:need(r[flag]is False,'no '+flag)
 for flag in['new_source_credit','new_question_credit','new_formal_credit']:need(r[flag]==0,'no numerical credit')
 need(r['source_scope_limits']==derive(p,docs,raw)['source_scope_limits'],'bounded source qualifications')
 ss=0;own=r['primary']['whole_common']
 need(len(r['primary_acquisition'])==4,'whole acquisition stages')
 for i,a in enumerate(r['primary_acquisition']):
  if i: s=r['source_ids'][i-1];ss+=r['primary']['document_costs'][s];own+=r['primary']['application_bundles'][s]
  need(a['stage']==i and a['source_written']==ss and a['replacement_written']==own and a['sources_acquired']==r['source_ids'][:i]and a['whole_common_acquired']and a['required_certificates_prepaid'],'whole acquisition closure')
 return dict(PDF_cells=450,raw_cells=170,coordinates=30,exact_fractions=120,unique_raw_files=17)

def controls(r,p,d,w):
 rows=[]
 def reject(name,action):
  try:action()
  except (ValueError,KeyError):rows.append(dict(control=name,rejected=True));return
  raise ValueError('UNREJECTED CONTROL '+name)
 def mutation(name,fn):
  q=copy.deepcopy(r);fn(q);reject(name,lambda:validate(q,p,d,w))
 mutation('omit old common U',lambda q:q['common_documents'].remove('U'))
 mutation('omit cover common U1',lambda q:q['common_documents'].remove('U1'))
 mutation('omit extension common U2',lambda q:q['common_documents'].remove('U2'))
 mutation('omit F005 companion',lambda q:q['application_documents']['F005'].remove('A2'))
 mutation('omit F007 companion',lambda q:q['application_documents']['F007'].remove('A5'))
 mutation('switch primary to calibrated',lambda q:q.update(primary_coordinate='calibrated_selected/NFC/characters_without_whitespace'))
 mutation('alter accepted old vector',lambda q:q['complete_document_metric_vectors']['U']['raw_untrimmed']['NFC'].update(characters_without_whitespace=1))
 mutation('alter nonprimary numerator',lambda q:q['coordinates']['calibrated_selected/NFKC/whitespace_tokens']['written'].update(numerator=1))
 mutation('alter primary conditional denominator',lambda q:q['coordinates'][q['primary_coordinate']]['conditional']['F007'].update(denominator=1))
 mutation('required becomes optional',lambda q:q['required_files'].clear())
 mutation('duplicate dual-role checker',lambda q:q['whole_file_inventory'].append(q['whole_file_inventory'][-1]))
 mutation('omit operational driver',lambda q:q['whole_file_inventory'].pop(8))
 mutation('change full rawfile byte count',lambda q:q['whole_file_inventory'][0].update(bytes=0))
 mutation('unknown external becomes zero',lambda q:q['unknown_costs'].update(retained_external_proofs=0))
 mutation('invent software-inclusive factor',lambda q:q.update(software_inclusive_factors=2))
 mutation('omit F005 from full required printed coverage',lambda q:q['required_printed_coverage']['REQ'].remove(q['required_files'][0]))
 mutation('erase complete required printed alternative',lambda q:q.update(full_required_only_printed_representation=None))
 mutation('invent full formalization',lambda q:q.update(full_source_formalized=True))
 mutation('erase question qualification',lambda q:q['source_scope'].update(F007_problems1_and2='solved'))
 mutation('omit common at first acquisition',lambda q:q['primary_acquisition'][0].update(replacement_written=0))
 mutation('claim free cross-topic common',lambda q:q.update(cross_topic_discount=True))
 return rows

def page_texts(path):return [p.extract_text()or''for p in PdfReader(path).pages]
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',required=True,type=Path);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a.add_argument('--study-root',type=Path);args=a.parse_args()
 out=args.out.resolve();need(not out.exists(),'fresh output directory');out.mkdir(parents=True)
 if (R/'manifest.json').exists():
  for q in load(R/'manifest.json')['exports']:bound(q,R)
 p,d,w=inputs();r=load(R/'results.json');report=validate(r,p,d,w);expected=derive(p,d,w);need(r==expected,'full deterministic results')
 previous=load(R/'previous_manifest.json');need(sha((R/'previous_manifest.json').read_bytes())=='05c778a72a1a7963013fa79f92c084f04f6b8b9707db18592ce173da4f1a9b68','exact immutable predecessor')
 priorrows={q['path']:q for q in previous['exports']}
 for name,q in priorrows.items():
  if name.startswith('inputs/')or name in['protocol.json','protocol_freeze.json','fractions.csv','document_costs.csv','whole_files.csv','acquisition.csv','costs.svg','costs.pdf','plot_data.json']:bound(q,R)
 prior=copy.deepcopy(r);prior['required_printed_coverage']={'REQ':['topic_Mix_L016_recovery/base_certificate.g'],'CODE1':['topic_Mix_F005_recovery/check_coprime.g']};prior['full_required_only_printed_representation']=None
 b=(json.dumps(prior,ensure_ascii=False,indent=2)+'\n').encode();need(sha(b)==priorrows['results.json']['sha256'],'only two descriptive result fields changed; all arithmetic identical')
 included=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',(R/'evidence/required_program.tex').read_text());need(included==['check_coprime.g','base_certificate.g'],'actual complete REQ TeX includes both required files')
 for name,content in outputs(expected).items():
  need((R/name).read_text()==content,'exact JSON/CSV '+name);(out/name).write_text(content)
 cs=controls(r,p,d,w)
 graph=plot(r,out);need(graph==load(R/'plot_data.json'),'fresh plot specification');need(graph['bars']==16,'all16 bars');save(out/'plot_data.json',graph)
 for base in[R,out]:
  compare_geometry(svg_rectangles((base/'costs.svg').read_text()),graph['expected_rectangles']);rects,H=pdf_rectangles(base/'costs.pdf');compare_pdf(rects,H,graph['expected_rectangles'],0)
 actual=svg_rectangles((R/'costs.svg').read_text());bad=copy.deepcopy(actual);bad['bar-whole-source'][2]*=.9
 for name,values in [('distorted actual SVG bar',bad),('missing actual SVG bar',{k:v for k,v in actual.items()if k!='bar-whole-U2'})]:
  try:compare_geometry(values,graph['expected_rectangles'])
  except ValueError:cs.append(dict(control=name,rejected=True))
  else:raise ValueError('unrejected graph control')
 txt=tex(r);need(txt==(R/'reader.tex').read_text(),'exact generated reader');(out/'reader.tex').write_text(txt)
 sourcepages=page_texts(R/'reader.pdf');need(len(sourcepages)==3,'three authoritative reader pages')
 render=None
 if args.render:
  for run in[1,2]:
   proc=subprocess.run([args.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/f'xelatex{run}.txt').write_text(proc.stdout);need(proc.returncode==0,'reader fresh compile')
  log=(out/'reader.log').read_text();diagnostics=[l for l in log.splitlines()if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning',l)];need(not diagnostics,'empty reader diagnostics');need(page_texts(out/'reader.pdf')==sourcepages,'all3 exact reader page texts');render=dict(pages=3,diagnostics=[],page_texts_equal=True)
 if args.study_root:
  for q in r['whole_file_inventory']:bound(q,args.study_root)
  report['actual_whole_files_rehashed']=17
 save(out/'controls.json',cs)
 report.update(status='PASS',author_role=p['author_role'],protocol_sha256=sha((R/'protocol.json').read_bytes()),input_manifest_sha256=sha((R/'inputs/input/manifest.json').read_bytes()),input_review_manifest_sha256=sha((R/'inputs/input_review/manifest.json').read_bytes()),input_adoption_manifest_sha256=sha((R/'inputs/input_adoption/manifest.json').read_bytes()),controls=len(cs),CSV_rows={n:len(list(csv.DictReader(io.StringIO((R/n).read_text()))))for n in['fractions.csv','document_costs.csv','whole_files.csv','acquisition.csv']},actual_SVG_bars=16,actual_PDF_bars=16,authoritative_reader_pages=3,render=render,source_extraction_repeated=False,scientific_programs_or_Lean_replayed=False,software_inclusive_factor=None,primary=r['primary']['written'])
 save(out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
