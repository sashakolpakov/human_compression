#!/usr/bin/env python3
"""Complete rank-contraction measurement inputs. No factors or proof replay."""
from pathlib import Path
import argparse,copy,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract
from unicode_fonts import audit as unicode_audit
from calibration import output
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def load(n):return json.loads((H/n).read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def binding(p,path=None):
 data=p.read_bytes();return dict(path=path or p.name,bytes=len(data),sha256=sha(data))
def bound(root,row):
 path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'safe relative path');p=root/path;data=p.read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'whole exact file '+row['path']);return p,data

def metrics(text,n):
 text=unicodedata.normalize(n,text);collapsed=' '.join(text.split())
 return dict(whitespace_tokens=len(collapsed.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',text)),characters_without_whitespace=sum(not x.isspace()for x in text),characters_with_collapsed_whitespace=len(collapsed),utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),normalized_text_sha256=sha(text.encode()),collapsed_text_sha256=sha(collapsed.encode()))

def furniture(key,raw,pages):
 cuts=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L037' and n>=2:
   literal=f'{n} PETER A. BROOKSBANK AND DIMITRI LEEMANS\n' if n%2==0 else f'RANK REDUCTION OF STRING C-GROUP REPRESENTATIONS {n}\n'
   need(t.startswith(literal),'exact repeated source header');a=0;b=len(literal)
  else:
   match=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(match is not None,'exact isolated footer');a=match.start()+(t[match.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];cuts.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def transform(raw,row,edits=()):
 changes=sorted([(x['start'],x['end'],'\n')for x in row['excluded_furniture']]+list(edits));parts=[];at=0
 for a,b,v in changes:need(at<=a<b<=len(raw),'exact disjoint edits');parts.extend([raw[at:a],v]);at=b
 parts.append(raw[at:]);return ''.join(parts)

def validate_policy(p):
 need((p['source_id'],p['source_rows'],p['proof_contexts'],p['original_manuscripts'])==('L037',22,20,1),'accepted complete source contract')
 need(list(p['replacements'])==['U','A1','CODE'] and [p['replacements'][k]['pages']for k in p['replacements']]==[3,5,1] and p['source']['pages']==6,'all complete documents and final bibliography page')
 need(p['whole_common_paper_charged'] and p['existing_B_common_is_not_a_prerequisite'] and p['cross_topic_discount']is False,'whole local common paper without cross-topic discount')
 need(p['primary'].startswith('raw_untrimmed NFC characters_without_whitespace') and p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates and raw primary')
 need([p[x]for x in ['program_files','local_finite_certificate_programs','uniform_required_programs','driver_files','formal_files','partial_formal_declarations']]==[1,1,0,1,1,4],'program/driver/scoped-formal roles')
 need(len(p['programs'])==len(p['drivers'])==len(p['formal'])==1 and p['programs'][0]['whole_file_required'] and not p['programs'][0]['uniform_mathematical_premise'],'one complete finite certificate, not uniform sampled proof')
 need(p['formal'][0]['declarations']==4 and not p['whole_source_formalized'],'partial formal scope')
 need(p['all_declared_code_prepurchased_for_conditional_results'] and p['raw_and_printed_code_are_alternatives'],'full program prepayment; alternatives not double charged')
 need(set(p['unknown_costs'])=={'full_graphics','retained_external_proofs','historical_software','full_formalization'} and all(v is None for v in p['unknown_costs'].values()),'unknown costs not zero')
 need(p['ratio']is None and not p['factors_permitted'] and p['new_scientific_credit']==p['new_formal_credit']==0,'no factor or new credit')
 need([p[x]for x in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files','raw_metric_cells']]==[4,15,120,3,30],'whole input dimensions')

def validate_glyphs(raw,fonts,pages,events,spec,aliases):
 covered=set();edits=[];classes={(r['font_identity'],r['encoded_byte']):r for r in aliases}
 for g in spec['glyph_substitutions']:
  a,b=g['start'],g['end'];need(0<=a<b<=len(raw) and not covered.intersection(range(a,b)),'one disjoint glyph');covered.update(range(a,b))
  need(raw[a:b]==g['input'] and all(fonts[j]==g['input_font']for j in range(a,b)),'literal font-bound glyph')
  need([events.get(j)for j in range(a,b)]==g['pdf_events'] and events.get(a)is not None,'all actual dictionary/encoding/byte events')
  e=events[a];need(e['decoded_character_index']==0 and e['decoded_text']==g['input'],'whole decoded glyph')
  need([events[j]['decoded_character_index']for j in range(a,b)]==list(range(b-a)),'exact consecutive decoded characters')
  r=classes.get((e['font_identity'],e['encoded_byte']));need(r is not None and r['glyph_name']==e['glyph_name'] and g['output']==r['output'] and len(g['output'])==1,'observed component, no invented symbol')
  pg=pages[g['page']-1];x,y=g['context_start'],g['context_end'];need(pg['start']<=x<=a<b<=y<=pg['end'] and sha(raw[x:y].encode())==g['context_sha256'] and g['page_offset']==a-pg['start'],'bound visible context')
  need(not any(max(a,z['start'])<min(b,z['end'])for z in spec['excluded_furniture']),'no scientific glyph removed as furniture')
  edits.append((a,b,g['output']))
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c)in['Cc','Co'] and c not in '\n\r\t')or c=='\ufffd')or i in covered,'unresolved control/private/replacement character')
  e=events.get(i);need(e is None or (e['font_identity'],e['encoded_byte'])not in classes or i in covered,'every observed alias included')
 need(not covered.intersection(spec['extraction_metadata']['generated_newline_offsets']),'no generated layout character calibrated')
 return edits

def document(root,key,row):
 pdf,_=bound(root,row);raw,fonts,pages,meta=extract(pdf,False)
 need(raw=='\n'.join(x.extract_text()or''for x in pypdf.PdfReader(pdf).pages),'unaltered returned extraction');need(len(pages)==row['pages'],'full physical extent')
 events,typ=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L037',generated_newline_offsets=set(meta['generated_newline_offsets']));uni=unicode_audit(pdf,raw,fonts,pages)
 aliases=[]
 for r in typ['encoded_glyph_classes']:
  v=output(r)
  if v is not None:aliases.append(dict(document=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=v,output_name=unicodedata.name(v),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']))
 repairs=[];lookup={(r['font_identity'],r['encoded_byte']):r for r in aliases}
 for i,e in events.items():
  g=lookup.get((e['font_identity'],e['encoded_byte']))
  if g is None or e['decoded_character_index']!=0:continue
  end=i+len(g['input']);need(raw[i:end]==g['input'],'literal alias');pg=pages[e['page']-1];a=max(pg['start'],i-30);b=min(pg['end'],end+30)
  repairs.append(dict(start=i,end=end,page=e['page'],page_offset=i-pg['start'],input=g['input'],input_font=fonts[i],output=g['output'],pdf_events=[events[j]for j in range(i,end)],context_start=a,context_end=b,context_sha256=sha(raw[a:b].encode())))
 spec=dict(row,page_bindings=pages,extraction_sha256=sha(raw.encode()),included_spans=[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],excluded_furniture=furniture(key,raw,pages),glyph_substitutions=sorted(repairs,key=lambda x:x['start']),extraction_metadata=meta)
 edits=validate_glyphs(raw,fonts,pages,events,spec,aliases);texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec),calibrated_selected=transform(raw,spec,edits))
 result=dict(pdf_sha256=row['sha256'],pages=len(pages),furniture_cuts=len(spec['excluded_furniture']),glyph_repairs=len(edits),metrics={v:{n:metrics(t,n)for n in ['NFC','NFKC']}for v,t in texts.items()})
 return spec,dict(type1=typ,unicode=uni),aliases,result,dict(raw=raw,fonts=fonts,events=events,pages=pages,texts=texts)

def code_inclusion(tex,raw,code):
 need(re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)==['check_examples.g'] and not re.search('firstline|lastline|firstnumber|lastnumber',tex),'one complete program, no pruning')
 packed=lambda t:''.join(unicodedata.normalize('NFKC',t).split())
 need(packed(code)in packed(raw),'complete literal printed program')
 return dict(full_files=1,no_pruning=True,no_printable_character_removed=True,normalization_for_inclusion_only=True)

def compute(study):
 p=load('policy.json');validate_policy(p);fixed=load('policy_freeze.json')
 for row in [fixed['policy'],fixed['source_boundary'],*fixed['helpers']]:bound(H,row)
 need(pypdf.__version__==p['pypdf_version']=='6.13.0' and fontTools.__version__==p['fonttools_version']=='4.63.0','exact extraction versions')
 science={r['path']:json.loads(bound(study,r)[1])for r in p['scientific_bindings']};need(science==load('source_boundary.json'),'accepted complete scientific scopes')
 scope=science['topic_B_L037_recovery/scope.json'];review=science['topic_B_L037_root_review/review.json']
 need(len(scope['source_rows'])==22 and len(scope['proof_contexts'])==20 and len(scope['declarations'])==4,'actual accepted clause and partial-formal counts')
 need(review['status']=='PASS_DISTINCT_ROOT_REVIEW_COMPLETE_L037_CONTRACT' and review['complete_corrected_principal_recovery_accepted'] and review['source_pdf_sha256']==p['source']['sha256'],'distinct scientific acceptance and exact source edition')
 retained=list(dict.fromkeys(x for row in scope['source_rows']for x in row['retained_inputs']if x!='check_examples.g'))
 need(p['retained_facts']==retained and p['missing_full_external_primary']==scope['retained_inputs_missing_complete_local_primary'],'all retained and missing-primary premises stay explicit')
 for row in p['scientific_bindings']:
  if row['path'].endswith('/manifest.json'):
   root=study/Path(row['path']).parent
   for e in science[row['path']]['exports']:bound(root,e)
 for row in p['replacements'].values():bound(study,row['tex'])
 specs={};audits={};aliases=[];docs={};cache={}
 for key,row in {'L037':p['source'],**p['replacements']}.items():
  specs[key],audits[key],als,docs[key],cache[key]=document(study,key,row);aliases.extend(als)
 raw_files={};contents={}
 for category in ['programs','drivers','formal']:
  raw_files[category]={}
  for row in p[category]:
   _,data=bound(study,row);contents[row['path']]=data.decode();raw_files[category][row['path']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n)for n in p['normalizations']})
 tex=bound(study,p['replacements']['CODE']['tex'])[1].decode();inc=code_inclusion(tex,cache['CODE']['texts']['raw_selected'],contents[p['programs'][0]['path']])
 result=dict(status='AUTHOR_INPUT_COUNTS_PENDING_DISTINCT_REVIEW',source_id='L037',original_manuscripts=1,source_rows=22,proof_contexts=20,pdf_documents=4,pdf_pages=15,pdf_metric_cells=120,raw_files_count=3,raw_metric_cells=30,documents=docs,raw_files=raw_files,program_inclusion=inc,unknown_costs=p['unknown_costs'],ratio=None,new_scientific_credit=0,new_formal_credit=0,scientific_programs_or_Lean_executed=False,whole_source_formalized=False)
 return result,specs,audits,aliases,cache

def validate_outputs(c,s,a,aliases,expected=None):
 need(set(c['documents'])==set(s)==set(a)=={'L037','U','A1','CODE'},'four complete documents')
 need([c[k]for k in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files_count','raw_metric_cells']]==[4,15,120,3,30],'full dimensions')
 need(len(aliases)==6 and sum(x['occurrences']for x in aliases)==8 and all(x['document']=='L037'for x in aliases),'six observed component classes, eight events')
 need(c['ratio']is None and c['new_scientific_credit']==c['new_formal_credit']==0 and all(v is None for v in c['unknown_costs'].values()),'no invented unknowns, factors or credits')
 need(not c['scientific_programs_or_Lean_executed'] and not c['whole_source_formalized'],'no science replay claim')
 for k,row in s.items():need(len(row['page_bindings'])==row['pages'] and a[k]['unicode']['status']=='ALL_USED_UNICODE_CLASSES_BOUND','all pages and used embedded Unicode classes')
 if expected is not None:need((c,s,a,aliases)==expected,'all exact cells, source spans and actual dictionary/encoding/font evidence')

def controls(c,s,a,aliases,cache):
 names=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError,IndexError):names.append(name)
  else:raise ValueError('control escaped: '+name)
 p=load('policy.json')
 for name,edit in [('omit application reference page',lambda x:x['replacements']['A1'].update(pages=4)),('omit source page',lambda x:x['source'].update(pages=5)),('free common paper',lambda x:x.update(whole_common_paper_charged=False)),('free old B premise',lambda x:x.update(existing_B_common_is_not_a_prerequisite=False)),('promote finite example to uniform proof',lambda x:x['programs'][0].update(uniform_mathematical_premise=True)),('omit driver',lambda x:x['drivers'].clear()),('inflate formal count',lambda x:x.update(partial_formal_declarations=5)),('unknown as zero',lambda x:x['unknown_costs'].update(full_graphics=0)),('invent factor',lambda x:x.update(ratio=1.2)),('double charge printed and raw program',lambda x:x.update(raw_and_printed_code_are_alternatives=False))]:
  q=copy.deepcopy(p);edit(q);reject(name,lambda:validate_policy(q))
 expected=(c,s,a,aliases)
 for name,edit in [('change source count',lambda C,S,A,L:C['documents']['L037']['metrics']['raw_untrimmed']['NFC'].update(characters_without_whitespace=1)),('erase component repair',lambda C,S,A,L:S['L037']['glyph_substitutions'].pop()),('collapse bracket components',lambda C,S,A,L:L[0].update(output='[')),('wrong encoding identity',lambda C,S,A,L:A['L037']['type1']['encoded_glyph_classes'][0].update(font_identity='0'*64)),('drop Unicode glyph class',lambda C,S,A,L:A['U']['unicode']['encoded_glyph_classes'].pop())]:
  q=copy.deepcopy(expected);edit(*q);reject(name,lambda:validate_outputs(*q,expected))
 raw=cache['L037'];spec=copy.deepcopy(s['L037']);spec['glyph_substitutions'][0]['output']='['
 reject('unobserved visible replacement',lambda:validate_glyphs(raw['raw'],raw['fonts'],raw['pages'],raw['events'],spec,aliases))
 spec=copy.deepcopy(s['L037']);spec['glyph_substitutions'][0]['pdf_events'][0]['font_identity']='0'*64
 reject('literal dictionary event mismatch',lambda:validate_glyphs(raw['raw'],raw['fonts'],raw['pages'],raw['events'],spec,aliases))
 code='Print("complete-code");';tex=r'\VerbatimInput{check_examples.g}'
 code_inclusion(tex,code,code)
 reject('truncated program',lambda:code_inclusion(tex,code[:-3],code));reject('line-pruned program',lambda:code_inclusion(tex.replace('{check','[firstline=2]{check'),code,code))
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);x=ap.parse_args();need(not x.out.exists(),'fresh output');need(not x.prepare or not(H/'manifest.json').exists(),'frozen inputs cannot regenerate');x.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for row in load('manifest.json')['exports']:bound(H,row)
 if(H/'protocol.json').exists():
  for row in load('protocol.json')['local_bindings']:bound(H,row)
 c,s,a,aliases,cache=compute(x.study_root);validate_outputs(c,s,a,aliases)
 if not x.prepare:validate_outputs(c,s,a,aliases,(load('author_counts.json'),load('input_spec.json'),load('font_audit.json'),load('glyph_aliases.json')))
 tests=controls(c,s,a,aliases,cache)
 for name,v in [('counts.json',c),('input_spec.json',s),('font_audit.json',a),('glyph_aliases.json',aliases)]:save(x.out/name,v)
 report=dict(status='PASS',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_cells=120,raw_cells=30,pages=15,glyph_classes=6,glyph_occurrences=8,semantic_controls=tests,no_factors=True,no_scientific_replay=True);save(x.out/'report.json',report);print(json.dumps(report))
 if x.prepare:
  for dst,src in [('author_counts.json','counts.json'),('input_spec.json','input_spec.json'),('font_audit.json','font_audit.json'),('glyph_aliases.json','glyph_aliases.json')]: (H/dst).write_bytes((x.out/src).read_bytes())
if __name__=='__main__':main()
