#!/usr/bin/env python3
"""Whole unified B input boundary; no compression factors are evaluated."""
from pathlib import Path
import argparse,copy,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract
from unicode_fonts import audit as unicode_audit
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def read(path):return json.loads(Path(path).read_text())
def save(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def binding(path,name=None):
 p=Path(path);data=p.read_bytes();return dict(path=name or p.name,bytes=len(data),sha256=sha(data))
def bound(root,row):
 rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe relative binding')
 p=root/rel;data=p.read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact binding '+str(rel));return data

def verify_manifest(root,row):
 data=bound(root,row);obj=json.loads(data)
 for export in obj['exports']:bound(root,export)
 return obj

def metrics(text,normalization):
 text=unicodedata.normalize(normalization,text);collapsed=' '.join(text.split())
 return dict(whitespace_tokens=len(collapsed.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',text)),characters_without_whitespace=sum(not c.isspace() for c in text),characters_with_collapsed_whitespace=len(collapsed),utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),normalized_text_sha256=sha(text.encode()),collapsed_text_sha256=sha(collapsed.encode()))

def furniture(raw,pages):
 rows=[]
 for page in pages:
  s=raw[page['start']:page['end']];m=re.search(r'(?:^|\n)'+str(page['page'])+r'\s*\Z',s);need(m is not None,'exact isolated physical footer')
  a=page['start']+m.start()+(s[m.start()]=='\n');b=page['end'];rows.append(dict(page=page['page'],start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return rows

def selected(raw,row):
 at=0;parts=[]
 for cut in row['excluded_furniture']:
  a,b=cut['start'],cut['end'];need(at<=a<b<=len(raw) and raw[a:b]==cut['literal'],'exact disjoint furniture only');parts.extend([raw[at:a],'\n']);at=b
 parts.append(raw[at:]);return ''.join(parts)

def validate_policy(p):
 need(p['originals']==['N001','N003','N008','L030','L040'] and p['source_rows']==65 and p['proof_contexts']==56,'five unchanged full contracts')
 need(list(p['replacements'])==['U_B','B1','B2','B3','B4','B5','CODE'],'whole common and five applications plus complete code')
 need([r['pages'] for r in p['replacements'].values()]==[16,3,4,4,5,11,7],'all fifty pages including references')
 need(p['whole_common_once'] and p['complete_program_appendix_once'] and p['full_applications']==['B1','B2','B3','B4','B5'],'one entire common and all local contexts')
 need(p['primary']=='raw_untrimmed NFC characters_without_whitespace; N001 literal authored rendering unchanged','unchanged primary convention')
 need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'] and p['units']==UNITS,'all thirty policy coordinates')
 need([r['role'] for r in p['programs']]==['required_finite_primitive_inputs','finite_validation','finite_validation','required_only_for_auxiliary_n8_and_validation_of_branching'],'four complete programs retain actual proof roles')
 need(len(p['drivers'])==2 and len(p['formal'])==2 and sum(r['declarations'] for r in p['formal'])==p['partial_formal_declarations']==14 and p['new_formal_declarations']==0,'two drivers and fourteen reused partial declarations')
 need(p['raw_and_printed_programs_alternatives'] and all(r['whole_file_printed'] for r in p['programs']),'full alternative code representations')
 need(all(v is None for v in p['unknown_costs'].values()),'unknowns remain null')
 need(p['new_scientific_credit']==0 and p['ratio'] is None and not p['factors_permitted'],'inputs only, no factor or new credit')

def retained_sources(public,p):
 for row in p['retained_public_bindings']:bound(public,row)
 old=read(public/'audit/b5-measurement/v1/packet/results.json');rows=[]
 for r in old['rows']:
  rows.append(dict(variant=r['variant'],normalization=r['normalization'],unit=r['unit'],sources={z['source']:z['source_cost'] for z in r['individual']},source_representations={z['source']:z['source_representation'] for z in r['individual']},L040_article_only=r['article_only_sensitivity']['L040_article_cost']))
 retained=read(H/'retained_source_counts.json');need(retained['source_order']==p['originals'] and retained['coordinates']==rows,'all 150 admitted source cells and thirty article-only cells unchanged')
 need(len(rows)==30 and all(list(r['sources'])==p['originals'] for r in rows),'all five source costs in every coordinate')
 need(all(r['source_representations']['N001']=='literal_authored_rendering' for r in rows),'N001 representation is not an acquired PDF')
 return retained

def code_inclusion(tex,raw,programs):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==list(programs) and not re.search('firstline|lastline|firstnumber|lastnumber',tex),'all four complete VerbatimInput files without line pruning')
 def packed(s):return ''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','')
 for name,code in programs.items():need(packed(code) in packed(raw),'complete printed file '+name)
 return dict(files=4,all_lines_included=True,normalization_only_for_inclusion_not_counts=True,wrap_symbols_retained_in_measured_text=True)

def document(author,key,row):
 pdf=author/row['path'];raw,fonts,pages,meta=extract(pdf,False)
 need(raw=='\n'.join(page.extract_text() or '' for page in pypdf.PdfReader(pdf).pages),'unaltered returned pypdf text')
 need(len(pages)==row['pages'],'full page extent')
 need(not any(unicodedata.category(c) in ('Co',) or c=='\ufffd' or (unicodedata.category(c)=='Cc' and c not in '\n\r\t') for c in raw),'no unresolved controls/private or replacement characters')
 events,type1=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']))
 uni=unicode_audit(pdf,raw,fonts,pages)
 spec=dict(row,page_bindings=pages,extraction_sha256=sha(raw.encode()),included_spans=[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],excluded_furniture=furniture(raw,pages),glyph_substitutions=[],extraction_metadata=meta)
 text=selected(raw,spec);texts=dict(raw_untrimmed=raw,raw_selected=text,calibrated_selected=text)
 audit=dict(type1_symbols=type1,unicode_fonts=uni)
 result=dict(pdf_sha256=row['sha256'],pages=len(pages),furniture_cuts=len(pages),glyph_repairs=0,metrics={v:{n:metrics(t,n) for n in ['NFC','NFKC']} for v,t in texts.items()})
 return spec,audit,result,texts

def science(author,study,p):
 verify_manifest(author,p['author_manifest'])
 r=p['scientific_review_manifest'];review=study/r['path'];need(binding(review,r['path'])==r,'exact distinct scientific review manifest');verify_manifest(review.parent,dict(r,path='manifest.json'))
 for row in p['replacements'].values():bound(author,row);bound(author,row['tex'])
 for category in ['programs','drivers','formal']:
  for row in p[category]:bound(author,row)

def compute(args):
 p=read(H/'policy.json');validate_policy(p);fixed=read(H/'policy_freeze.json');bound(H,fixed['policy']);bound(H,fixed['retained_source_counts'])
 for row in fixed['helpers']:bound(H,row)
 need(pypdf.__version__==p['pypdf_version']=='6.13.0' and fontTools.__version__==p['fonttools_version']=='4.63.0','pinned parser versions')
 science(args.author_root,args.study_root,p);retained=retained_sources(args.public_root,p)
 specs={};audits={};docs={};texts={}
 for key,row in p['replacements'].items():specs[key],audits[key],docs[key],texts[key]=document(args.author_root,key,row)
 raw_files={}
 for category in ['programs','drivers','formal']:
  raw_files[category]={}
  for row in p[category]:
   data=bound(args.author_root,row);raw_files[category][row['path']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n) for n in p['normalizations']})
 programs={r['path']:(args.author_root/r['path']).read_text() for r in p['programs']}
 included=code_inclusion((args.author_root/'program-appendix.tex').read_text(),texts['CODE']['raw_selected'],programs)
 old=read(args.public_root/'audit/b5-measurement/v1/packet/results.json')
 for r in old['rows']:
  for key in ['B1','B3','B4','CODE']:
   current=docs[key]['metrics'][r['variant']][r['normalization']][r['unit']]
   previous=r['printed_program_cost'] if key=='CODE' else next(z['application_cost'] for z in r['individual'] if z['application']==key)
   need(current==previous,'unchanged complete application/code coordinate '+key)
 result=dict(status='AUTHOR_INPUT_COUNTS_PENDING_DISTINCT_REVIEW',originals=p['originals'],source_rows=65,proof_contexts=56,pdf_documents=7,pdf_pages=50,pdf_metric_cells=210,retained_source_cells=150,retained_article_only_cells=30,raw_files_count=8,raw_metric_cells=80,documents=docs,raw_files=raw_files,program_inclusion=included,unknown_costs=p['unknown_costs'],ratio=None,new_scientific_credit=0,new_formal_credit=0,originals_reextracted=False,GAP_or_Lean_reexecuted=False)
 return result,specs,audits,texts

def validate_outputs(counts,specs,audits,expected=None):
 need(set(specs)==set(audits)==set(counts['documents'])=={'U_B','B1','B2','B3','B4','B5','CODE'},'seven complete documents')
 need([counts[k] for k in ['pdf_documents','pdf_pages','pdf_metric_cells','retained_source_cells','retained_article_only_cells','raw_files_count','raw_metric_cells']]==[7,50,210,150,30,8,80],'exact complete input dimensions')
 need(counts['ratio'] is None and not counts['new_scientific_credit'] and not counts['new_formal_credit'] and all(v is None for v in counts['unknown_costs'].values()),'no factors/credits/invented unknown values')
 for key,row in specs.items():
  need(row['glyph_substitutions']==[] and len(row['page_bindings'])==row['pages'],'all pages, no unverified substitutions')
  need(audits[key]['unicode_fonts']['status']=='ALL_USED_UNICODE_CLASSES_BOUND','actual embedded Unicode font audit')
 if expected is not None:need((counts,specs,audits)==expected,'all exact cells, spans and font dictionaries/encodings/outlines')

def controls(counts,specs,audits):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (AssertionError,ValueError,KeyError,TypeError):rejected.append(name);return
  raise ValueError('control was accepted: '+name)
 p=read(H/'policy.json')
 for name,edit in [('omit application',lambda q:q['replacements'].pop('B3')),('remove references page',lambda q:q['replacements']['B5'].update(pages=10)),('promote validation',lambda q:q['programs'][1].update(role='required_finite_primitive_inputs')),('omit complete program',lambda q:q['programs'].pop()),('source PDF invention',lambda q:q.update(primary='N001 original PDF')),('unknown as zero',lambda q:q['unknown_costs'].update(full_graphics=0)),('ratio claim',lambda q:q.update(ratio=1.0)),('new formal credit',lambda q:q.update(new_formal_declarations=14)),('omit driver',lambda q:q['drivers'].pop()),('duplicate program charge',lambda q:q.update(raw_and_printed_programs_alternatives=False))]:
  q=copy.deepcopy(p);edit(q);reject(name,lambda q=q:validate_policy(q))
 for name,edit in [('count corruption',lambda c,s,a:c['documents']['U_B']['metrics']['raw_untrimmed']['NFC'].__setitem__('characters_without_whitespace',1)),('drop full source sensitivity',lambda c,s,a:c.update(retained_article_only_cells=0)),('invent glyph calibration',lambda c,s,a:s['U_B']['glyph_substitutions'].append({'output':'X'})),('wrong actual dictionary',lambda c,s,a:next(iter(a['U_B']['unicode_fonts']['actual_font_dictionaries'].values())).__setitem__('dictionary_sha256','0'*64)),('drop encoded glyph class',lambda c,s,a:a['CODE']['unicode_fonts']['encoded_glyph_classes'].pop()),('strip primary code wrap',lambda c,s,a:c['documents']['CODE']['metrics']['raw_untrimmed']['NFC'].__setitem__('normalized_text_sha256','0'*64))]:
  c,s,a=copy.deepcopy((counts,specs,audits));edit(c,s,a);reject(name,lambda c=c,s=s,a=a:validate_outputs(c,s,a,(counts,specs,audits)))
 # A literal complete-input check rejects truncation independently of fixed hashes.
 author_programs={f'p{i}.g':f'Print("unique-{i}");\n' for i in range(4)};tex='\n'.join('\\VerbatimInput{'+k+'}' for k in author_programs)
 raw=''.join(author_programs.values());code_inclusion(tex,raw,author_programs)
 reject('truncated printed program',lambda:code_inclusion(tex,raw[:-7],author_programs))
 reject('line-pruned appendix',lambda:code_inclusion(tex.replace('VerbatimInput{','VerbatimInput[firstline=2]{',1),raw,author_programs))
 return rejected

def run(args):
 need(not args.out.exists(),'fresh output directory');need(not args.prepare or not (H/'manifest.json').exists(),'frozen packet cannot regenerate its adopted input records');args.out.mkdir(parents=True)
 if (H/'manifest.json').exists():verify_manifest(H,binding(H/'manifest.json'))
 if (H/'protocol.json').exists():
  for row in read(H/'protocol.json')['local_bindings']:bound(H,row)
 counts,specs,audits,texts=compute(args);validate_outputs(counts,specs,audits)
 if not args.prepare:validate_outputs(counts,specs,audits,(read(H/'author_counts.json'),read(H/'input_spec.json'),read(H/'font_audit.json')))
 tests=controls(counts,specs,audits)
 for name,obj in [('counts.json',counts),('input_spec.json',specs),('font_audit.json',audits)]:save(args.out/name,obj)
 report=dict(status='PASS',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_cells=210,raw_cells=80,retained_source_cells=150,retained_article_only_cells=30,pages=50,semantic_controls=tests,ratio=None)
 save(args.out/'report.json',report);print(json.dumps(report))
 if args.prepare:
  for n,src in [('author_counts.json','counts.json'),('input_spec.json','input_spec.json'),('font_audit.json','font_audit.json')]: (H/n).write_bytes((args.out/src).read_bytes())
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--author-root',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);a=ap.parse_args();a.author_root=a.author_root or a.study_root/'topic_B_unified';run(a)
