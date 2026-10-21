#!/usr/bin/env python3
"""Complete Mathieu-census measurement inputs. No factors or proof replay."""
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
  if key=='L073':
   literal=f'the electronic journal of combinatorics 17 (2010), #N4 {n}'
   need(t.endswith(literal),'exact source journal footer');a=len(t)-len(literal);b=len(t)
  else:
   match=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(match is not None,'exact isolated footer');a=match.start()+(t[match.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];cuts.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def transform(raw,row,edits=()):
 changes=sorted([(x['start'],x['end'],'\n')for x in row['excluded_furniture']]+list(edits));parts=[];at=0
 for a,b,v in changes:need(at<=a<b<=len(raw),'exact disjoint edits');parts.extend([raw[at:a],v]);at=b
 parts.append(raw[at:]);return ''.join(parts)

def validate_policy(p):
 need((p['source_id'],p['source_clauses'],p['physical_source_rows'],p['original_manuscripts'])==('L073',14,431,1),'complete corrected source contract')
 need(list(p['replacements'])==['U','A1','CLASSES','ROWS','CODE'] and [p['replacements'][k]['pages']for k in p['replacements']]==[2,5,10,9,11]and p['source']['pages']==9,'all complete papers and tables')
 need(p['application_document_keys']==['A1','CLASSES','ROWS'],'whole local application includes both complete tables')
 need(p['whole_common_paper_charged']and p['no_old_umbrella_or_other_application_premise']and p['no_L095_special_group_theorem']and not p['cross_topic_discount'],'all common prerequisites charged')
 need(p['primary'].startswith('raw_untrimmed NFC characters_without_whitespace') and p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected']and p['normalizations']==['NFC','NFKC'],'all thirty policy coordinates')
 need([len(p[x])for x in ['programs','required_raw_data','drivers','generated_outputs','formal']]==[7,2,3,10,0]and p['all_whole_files'],'whole code, data, auxiliary and evidence boundaries')
 need(all(x['whole_file']for k in ['programs','required_raw_data','drivers','generated_outputs']for x in p[k]),'no partial files')
 need(p['formal_declarations']==0 and p['retained_notation_source']['pages']==48 and p['no_complete_predecessor_recovery']and p['historical_download_not_used'],'formal and retained-source limits')
 need(all(v is None for v in p['unknown_costs'].values())and p['ratio']is None and not p['factors_permitted']and p['new_source_credit']==p['new_question_credit']==p['new_formal_credit']==0,'no unknown zero, factor or credit')
 need([p[x]for x in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files','raw_metric_cells']]==[6,46,180,22,220],'complete physical boundary dimensions')

def validate_accounting(a,p):
 programs=[x['path']for x in p['programs']];data=[x['path']for x in p['required_raw_data']];written=['U','A1','CLASSES','ROWS']
 need(a['policy_sha256']==sha((H/'policy.json').read_bytes()),'exact precount policy for accounting routes')
 for key in ['written','computation_printed','computation_raw']:need(a[key]['source_documents']==['L073'],'one complete source per route')
 need(a['written']['replacement_documents']==written and not a['written']['required_raw_files'],'complete written route; computation separate')
 need(a['computation_printed']['replacement_documents']==written+['CODE']and a['computation_printed']['required_raw_files']==data,'whole printed code plus both full raw data inputs')
 need(a['computation_raw']['replacement_documents']==written and a['computation_raw']['required_raw_files']==programs+data,'whole raw code plus both full raw data inputs')
 q=a['conditional'];need(q['application_documents']==written[1:]and q['prepaid_common_documents']==['U']and q['additional_prepaid_raw_data']==data and q['prepaid_program_representation_alternatives']==dict(printed=['CODE'],raw=programs),'whole common/program/data acquisition before conditional result')
 need(q['retained_classical_and_catalogue_premises_remain_unknown']and a['no_factor']and a['printed_and_raw_programs_not_double_charged']and a['no_primary_or_historical_data_pruning'],'no hidden zero, double count or factor')
 need(a['separate_driver_files']==[x['path']for x in p['drivers']]and a['separate_generated_outputs']==[x['path']for x in p['generated_outputs']],'whole separate evidence inventory')

def validate_modular_approval(approval,review):
 need(approval['expected_manifest_sha256']=='dba5b09e539f6149ca16f251c28d1bb5e31354202041e35035e29a0333304f0e','distinct modular review pin')
 need(approval['modular_author_manifest_sha256']==review['author_manifest_sha256']=='50f4c08a990f3d6e43f4544fe5daa8e819649a62f5fbe47f7f89b9b8aa3b463d','accepted modular author edition')
 need(review['status']=='PASS_DISTINCT_ROOT_L073_MODULAR_MIGRATION'and review['prior_science_manifest_sha256']=='13aa42fa08b4a6517945c91c08c51ee3eaec87f572662dad991fe9b519cd6676','distinct complete migration and science acceptance')
 need(approval['precount_policy_sha256']==sha((H/'policy.json').read_bytes())and approval['boundary_and_counts_unchanged']and approval['no_factors'],'additive unchanged precount boundary')
 need(approval['counts_sha256']==sha((H/'author_counts.json').read_bytes()),'additive unchanged counts')

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
 events,typ=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L073',generated_newline_offsets=set(meta['generated_newline_offsets']));uni=unicode_audit(pdf,raw,fonts,pages)
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

def code_inclusion(tex,raw,programs):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==[Path(p).as_posix().split('corpus161_L073_recovery/')[1]for p in programs]and not re.search('firstline|lastline|firstnumber|lastnumber',tex),'seven complete literal program inputs')
 packed=lambda t:''.join(unicodedata.normalize('NFKC',t).split())
 text=packed(raw)
 for path,code in programs.items():need(packed(code)in text,'whole printed program '+path)
 return dict(full_files=7,no_pruning=True,no_printable_character_removed=True,normalization_for_inclusion_only=True)

def compute(study):
 p=load('policy.json');validate_policy(p);validate_accounting(load('accounting_boundary.json'),p);fixed=load('policy_freeze.json')
 row=fixed['policy'];need(row['sha256']==sha((H/'policy.json').read_bytes()),'fixed policy before counts')
 need(pypdf.__version__==p['pypdf_version']=='6.13.0'and fontTools.__version__==p['fonttools_version']=='4.63.0','exact extraction versions')
 science={r['path']:json.loads(bound(study,r)[1])for r in p['scientific_bindings']};need(science==load('source_boundary.json'),'complete accepted scientific boundary')
 scope=science['corpus161_L073_recovery/scope.json'];review=science['corpus161_L073_root_review/review.json'];ledger=science['corpus161_L073_recovery/source_ledger.json']
 need(len(ledger['clauses'])==14 and scope['physical_source_rows']==431 and scope['formal_declarations']==0,'all actual source clauses/rows and no Lean')
 need(review['status']=='PASS_DISTINCT_ROOT_COMPLETE_CORRECTED_L073' and review['primary']['sha256']==p['source']['sha256'],'distinct science acceptance and source identity')
 need(p['retained_theorems']==scope['retained'],'all retained classical/software premises')
 for row in p['scientific_bindings']:
  if row['path'].endswith('/manifest.json'):
   root=study/Path(row['path']).parent
   for e in science[row['path']]['exports']:bound(root,e)
 for row in p['replacements'].values():bound(study,row['tex'])
 arr=json.loads(bound(study,p['modular_arrangement'])[1]);bound(study,p['migration']);need(arr['finite_G_scope_correction'] and arr['source_contract']==scope['contract'],'exact modular arrangement and finite scope correction')
 if(H/'modular_acceptance.json').exists():
  approval=load('modular_acceptance.json')
  for row in approval['bindings']:
   data=bound(study,row)[1]
   if row['path'].endswith('/manifest.json'):
    for e in json.loads(data)['exports']:bound(study/Path(row['path']).parent,e)
  approval_review=json.loads(bound(study,next(r for r in approval['bindings']if r['path'].endswith('/review.json')))[1]);validate_modular_approval(approval,approval_review)
 specs={};audits={};aliases=[];docs={};cache={}
 for key,row in {'L073':p['source'],**p['replacements']}.items():
  specs[key],audits[key],als,docs[key],cache[key]=document(study,key,row);aliases.extend(als)
 raw_files={};contents={}
 for category in ['programs','required_raw_data','drivers','generated_outputs']:
  raw_files[category]={}
  for row in p[category]:
   _,data=bound(study,row);contents[row['path']]=data.decode();raw_files[category][row['path']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n)for n in p['normalizations']})
 tex=bound(study,p['replacements']['CODE']['tex'])[1].decode();inc=code_inclusion(tex,cache['CODE']['texts']['raw_selected'],{r['path']:contents[r['path']]for r in p['programs']})
 result=dict(status='AUTHOR_INPUT_COUNTS_PENDING_DISTINCT_REVIEW',source_id='L073',original_manuscripts=1,source_clauses=14,physical_source_rows=431,pdf_documents=6,pdf_pages=46,pdf_metric_cells=180,raw_files_count=22,raw_metric_cells=220,documents=docs,raw_files=raw_files,program_inclusion=inc,unknown_costs=p['unknown_costs'],ratio=None,new_source_credit=0,new_question_credit=0,new_formal_credit=0,scientific_programs_or_Lean_executed=False,whole_source_formalized=False)
 cache['_modular_review']=approval_review
 return result,specs,audits,aliases,cache

def validate_outputs(c,s,a,aliases,expected=None):
 need(set(c['documents'])==set(s)==set(a)=={'L073','U','A1','CLASSES','ROWS','CODE'},'six complete documents')
 need([c[k]for k in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files_count','raw_metric_cells']]==[6,46,180,22,220],'full dimensions')
 need(len(aliases)==6 and sum(x['occurrences']for x in aliases)==472 and all(x['document']=='L073'for x in aliases),'six observed script/fraktur classes, all 472 events')
 need(c['ratio']is None and c['new_source_credit']==c['new_question_credit']==c['new_formal_credit']==0 and all(v is None for v in c['unknown_costs'].values()),'no invented unknowns, factors or credits')
 need(not c['scientific_programs_or_Lean_executed']and not c['whole_source_formalized'],'no science replay claim')
 for k,row in s.items():need(len(row['page_bindings'])==row['pages']and a[k]['unicode']['status']=='ALL_USED_UNICODE_CLASSES_BOUND','all pages and used embedded Unicode classes')
 if expected is not None:need((c,s,a,aliases)==expected,'all exact cells, spans and actual dictionary/encoding/font evidence')

def validate_reader(c):
 text=(H/'reader.tex').read_text();labels={'L073':'2010 original','U':'Common proof','A1':'Mathieu application body','CLASSES':'All replacement class tables','ROWS':'All physical-source-row dispositions','CODE':'All seven mathematical programs'}
 for key,label in labels.items():
  doc=c['documents'][key];value=doc['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace'];need(f"{label}&{doc['pages']}&{value:,}"in text,'literal reader complete-document count '+key)
 for key in ['programs','drivers','generated_outputs']:
  need(f"{sum(x['bytes']for x in c['raw_files'][key].values()):,}"in text,'full raw byte inventory in reader '+key)
 for x in c['raw_files']['required_raw_data'].values():need(f"{x['bytes']:,}"in text,'both mandatory data sizes in reader')

def controls(c,s,a,aliases,cache):
 names=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError,IndexError):names.append(name)
  else:raise ValueError('control escaped: '+name)
 p=load('policy.json')
 for name,edit in [('omit application reference page',lambda x:x['replacements']['A1'].update(pages=4)),('omit class-table page',lambda x:x['replacements']['CLASSES'].update(pages=9)),('omit source row table',lambda x:x['application_document_keys'].remove('ROWS')),('free common paper',lambda x:x.update(whole_common_paper_charged=False)),('free old umbrella premise',lambda x:x.update(no_old_umbrella_or_other_application_premise=False)),('omit mandatory historical data',lambda x:x['required_raw_data'].pop()),('prune program',lambda x:x['programs'][0].update(whole_file=False)),('omit generated output',lambda x:x['generated_outputs'].pop()),('claim formal declaration',lambda x:x.update(formal_declarations=1)),('recover whole predecessor',lambda x:x.update(no_complete_predecessor_recovery=False)),('unknown as zero',lambda x:x['unknown_costs'].update(full_graphics=0)),('invent factor',lambda x:x.update(ratio=1.2))]:
  q=copy.deepcopy(p);edit(q);reject(name,lambda:validate_policy(q))
 approval=load('modular_acceptance.json');q=copy.deepcopy(cache['_modular_review']);q['status']='PENDING'
 reject('unaccepted modular migration',lambda:validate_modular_approval(approval,q))
 changed=copy.deepcopy(approval);changed['boundary_and_counts_unchanged']=False
 reject('silently change precount boundary',lambda:validate_modular_approval(changed,cache['_modular_review']))
 ac=load('accounting_boundary.json')
 for name,edit in [('omit raw data from printed route',lambda x:x['computation_printed']['required_raw_files'].pop()),('double charge raw and printed program',lambda x:x['computation_raw']['replacement_documents'].append('CODE')),('omit local row table from conditional',lambda x:x['conditional']['application_documents'].remove('ROWS')),('omit common acquisition',lambda x:x['conditional']['prepaid_common_documents'].clear())]:
  q=copy.deepcopy(ac);edit(q);reject(name,lambda:validate_accounting(q,p))
 expected=(c,s,a,aliases)
 for name,edit in [('change source count',lambda C,S,A,L:C['documents']['L073']['metrics']['raw_untrimmed']['NFC'].update(characters_without_whitespace=1)),('erase fraktur repair',lambda C,S,A,L:S['L073']['glyph_substitutions'].pop()),('wrong script letter',lambda C,S,A,L:L[0].update(output='A')),('wrong encoding identity',lambda C,S,A,L:A['L073']['type1']['encoded_glyph_classes'][0].update(font_identity='0'*64)),('drop Unicode glyph class',lambda C,S,A,L:A['U']['unicode']['encoded_glyph_classes'].pop())]:
  q=copy.deepcopy(expected);edit(*q);reject(name,lambda:validate_outputs(*q,expected))
 raw=cache['L073'];spec=copy.deepcopy(s['L073']);spec['glyph_substitutions'][0]['output']='A'
 reject('unobserved visible replacement',lambda:validate_glyphs(raw['raw'],raw['fonts'],raw['pages'],raw['events'],spec,aliases))
 spec=copy.deepcopy(s['L073']);spec['glyph_substitutions'][0]['pdf_events'][0]['font_identity']='0'*64
 reject('literal dictionary event mismatch',lambda:validate_glyphs(raw['raw'],raw['fonts'],raw['pages'],raw['events'],spec,aliases))
 codes={r['path']:'unique_'+str(i)+'_complete;'for i,r in enumerate(p['programs'])};tex='\n'.join('\\VerbatimInput{'+k.split('corpus161_L073_recovery/')[1]+'}'for k in codes);text='\n'.join(codes.values());code_inclusion(tex,text,codes)
 reject('truncated printed program',lambda:code_inclusion(tex,text[:-3],codes));reject('line-pruned program',lambda:code_inclusion(tex.replace('\\VerbatimInput{','\\VerbatimInput[firstline=2]{',1),text,codes))
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);x=ap.parse_args();need(not x.out.exists(),'fresh output');need(not x.prepare or not(H/'manifest.json').exists(),'frozen inputs cannot regenerate');x.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for row in load('manifest.json')['exports']:bound(H,row)
 if(H/'protocol.json').exists():
  for row in load('protocol.json')['local_bindings']:bound(H,row)
 c,s,a,aliases,cache=compute(x.study_root);validate_outputs(c,s,a,aliases);validate_reader(c)
 if not x.prepare:validate_outputs(c,s,a,aliases,(load('author_counts.json'),load('input_spec.json'),load('font_audit.json'),load('glyph_aliases.json')))
 tests=controls(c,s,a,aliases,cache)
 for name,v in [('counts.json',c),('input_spec.json',s),('font_audit.json',a),('glyph_aliases.json',aliases)]:save(x.out/name,v)
 report=dict(status='PASS',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_cells=180,raw_cells=220,pages=46,glyph_classes=6,glyph_occurrences=472,semantic_controls=tests,no_factors=True,no_scientific_replay=True);save(x.out/'report.json',report);print(json.dumps(report))
 if x.prepare:
  for dst,src in [('author_counts.json','counts.json'),('input_spec.json','input_spec.json'),('font_audit.json','font_audit.json'),('glyph_aliases.json','glyph_aliases.json')]: (H/dst).write_bytes((x.out/src).read_bytes())
if __name__=='__main__':main()
