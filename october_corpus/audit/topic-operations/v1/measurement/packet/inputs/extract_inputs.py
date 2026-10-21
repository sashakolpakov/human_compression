#!/usr/bin/env python3
"""Complete operations input recount; no programme execution and no ratios."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract as literal_extract,BANNER,BANNERS
from calibration import aliases_from
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
KEYS={'N005','N006','N007','U','A0','A1','A2','A2nine','A2HN','CODEold','CODEnew'}
def load(name):return json.loads((HERE/name).read_text())
def metrics(text,form):
 text=unicodedata.normalize(form,text);c=' '.join(text.split())
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',text)),characters_without_whitespace=sum(not x.isspace() for x in text),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))


def bound(row,args):
 root={'sources':args.sources_root,'public':args.public_root}[row['root']];path=root/row['path'];data=path.read_bytes()
 need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact whole input '+row['path']);return path,data


def furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='N005':
   if n==1:
    m=re.search(r'\n1\s*\Z',t);need(m is not None,'isolated first source page number');a=m.start()+1;b=len(t)
   else:
    literal=f'{n} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n' if n%2==0 else f'FROM GROUP OPERATIONS TO GEOMETRIC STRUCTURES {n}\n';need(t.startswith(literal),'exact N005 running header');a=0;b=len(literal)
  elif key=='N007':
   if n==1:
    a=t.rfind('\n1\n'+BANNER)+1;need(a>0,'isolated page number before retained banner');b=a+1
   else:
    literal=f'{n} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n' if n%2==0 else f'THEj-DIAGONALS TWISTING {n}\n';need(t.startswith(literal),'exact repeated source header');a=0;b=len(literal)
  elif key=='N006':
   if n==1:
    a=t.rfind('\n1\n'+BANNERS[key])+1;need(a>0,'source page number before retained banner');b=a+1
   else:
    literal=f'{n}\n';need(t.startswith(literal),'exact leading source page number');a=0;b=len(literal)
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated footer');a=m.start()+(t[m.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out


def validate_selection(key,raw,row,pages,meta):
 need(row['pages']==len(pages) and row['page_bindings']==pages,'every physical page '+key)
 need(row['extraction_sha256']==sha(raw.encode()),'complete raw extraction '+key)
 need(row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole manuscript including references')
 need([{k:x[k] for k in ('page','start','end','literal','sha256')} for x in row['excluded_furniture']]==furniture(key,raw,pages),'only literal repeated furniture')
 need(meta==row['extraction_metadata'],'generated newline/Form metadata exact')
 need(meta['returned_extraction_changed'] is False,'raw extraction unchanged')
 if key in BANNERS:need(raw.count(BANNERS[key])==1,'one retained version banner')


def selected(raw,row):
 parts=[];at=0
 for f in row['excluded_furniture']:parts.append(raw[at:f['start']]);at=f['end']
 parts.append(raw[at:]);return '\n'.join(parts)


def alias(event,aliases,key):
 if event is None:return None
 rows=[r for r in aliases if r['source']==key and r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
 need(len(rows)<=1,'unique actual dictionary/encoding class');return rows[0] if rows else None


def calibrate(raw,fonts,pages,events,row,aliases,key):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique glyph offset');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and g['input_font']==fonts[i],'actual decoded font/character')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual literal PDF byte/event')
  a=alias(events[i],aliases,key);need(a is not None and a['output']==g['output'] and a['kind']==g['kind'] and len(g['output'])==1,'one bound symbol or proposed graphical primitive')
  pg=pages[g['page']-1];a,b=g['context_start'],g['context_end'];need(pg['start']<=a<=i<b<=pg['end'] and sha(raw[a:b].encode())==g['context_sha256'],'exact local glyph evidence')
  need(g['page_offset']==i-pg['start'],'physical page offset')
  need(i not in row['extraction_metadata']['generated_newline_offsets'],'actual glyph is not generated line break')
  need(not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'visible glyph not cut')
  chars[i]=g['output']
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t') or c=='\ufffd') or i in seen,'all suspect glyphs classified')
  need(alias(events.get(i),aliases,key) is None or i in seen,'every actual visible glyph alias repaired')
 return ''.join(chars)


def validate_external(e):
 required=[x for x in e['inputs'] if x['stage_role'].startswith('required')]
 need(len(required)==e['required_representation_files']==4 and sum(x['bytes'] for x in required)==e['required_representation_bytes']==21960689,'complete exact external representations')
 installed=e['installed_files_once_by_identical_hash']
 need(len(installed)==16 and len({x['sha256'] for x in installed})==16 and sum(x['bytes'] for x in installed)==e['installed_file_bytes_once']==2516249,'complete inherited installed data/algorithm boundary')
 need(e['unknown_proof_cost'] is None and not e['compact_word_discount'] and not e['cross_topic_overlap_discount'],'outside proof cost unknown, no word or cross-topic discount')
 return dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249,classification_proof_cost=None,measurement_rechecks_actual_data=False,scope='Exact retained ledgers bound; optional external byte-only audit is separate. Neither GAP algorithms nor scientific assertions rerun for measurement.')


def external_ledger_identity(e,scientific):
 nine=json.loads(scientific['papers/topic-diagonal/v2/papers/sporadic/retained_inputs.json'])
 hn=json.loads(scientific['papers/topic-diagonal/v2/papers/harada-norton/retained_inputs.json'])
 expected=nine['external_atlas_inputs']+hn['binary_files']
 need(len(expected)==len(e['inputs']),'all inherited external representation entries')
 for old in expected:
  matches=[x for x in e['inputs'] if x['filename']==old['filename']]
  need(len(matches)==1 and all(matches[0][k]==v for k,v in old.items()),'literal inherited representation pin '+old['filename'])
 expected_files=nine['files']+hn['installed_catalogue_inputs']
 need({x['sha256'] for x in expected_files}=={x['sha256'] for x in e['installed_files_once_by_identical_hash']},'exact catalogue/algorithm hash union')
 for old in expected_files:
  current=next(x for x in e['installed_files_once_by_identical_hash'] if x['sha256']==old['sha256'])
  need(current['bytes']==old['bytes'],'exact full catalogue/algorithm bytes')


def source_events(pdf,raw,fonts,pages,meta,key,source):
 events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']))
 skipped=audit['unchanged_type0_dictionaries']
 if key=='N007':
  need(len(skipped)==1,'only N007 version-banner Type0');fname=skipped[0]['font'];banner=''.join(c for c,f in zip(raw,fonts) if f==fname);need(banner==BANNERS[key],'only exact version banner')
  audit['source_unicode_banner']=dict(literal=banner,retained_in_every_coordinate=True,scope='Only Type0 version stamp; all authored body Type1 glyphs aligned. Duplicate Form visitor callback is not an extra rendered text event.')
 elif source:
  need(not skipped,'complete source text fonts audited Type1')
  audit['source_unicode_banner']=dict(literal=BANNERS[key],retained_in_every_coordinate=True,scope='Banner has actual audited Type1 events, with no skipped font or duplicate Form callback.')
 else:audit['replacement_unicode_scope']='Type0 font dictionaries are bound separately; their literal Unicode extraction is unchanged. No Type1 outline claim for those fonts. Every page is separately viewed.'
 return events,audit

def validate_software(p):
 sw=load('software_inventory.json')
 for old,new in [('programs','programs'),('required_input_drivers','required_drivers'),('operational_drivers','drivers'),('formal_files','formal')]:
  expected=[]
  for r in sw[old]:
   path=Path(r['path']);public=Path('/Users/sasha/medusa/math_compression');study=Path('/Users/sasha/medusa/research/leemans');base=public if path.is_relative_to(public) else study
   expected.append({**r,'root':'public' if base==public else 'sources','path':str(path.relative_to(base))})
  need(p[new]==expected,'exact whole-file software identities and semantic roles '+new)

def validate_policy(p):
 validate_software(p)
 need(p['original_manuscripts']==3 and p['source_rows']=={'N005':81,'N006':27,'N007':32},'complete three-source scope')
 need(set(p['sources'])=={'N005','N006','N007'} and set(p['sources'])|set(p['replacements'])==KEYS,'complete document set')
 need({k:r['pages'] for k,r in p['sources'].items()}=={'N005':60,'N006':22,'N007':12},'whole source pages')
 need({k:r['pages'] for k,r in p['replacements'].items()}=={'U':21,'A0':18,'A1':5,'A2':8,'A2nine':5,'A2HN':4,'CODEold':2,'CODEnew':4},'whole current pages')
 need(p['written_documents']==['U','A0','A1','A2','A2nine','A2HN'],'whole written acquisition')
 need(p['application_bundles']=={'N005':['A0'],'N006':['A2','A2nine','A2HN'],'N007':['A1']},'complete conditional bundles')
 need(len(p['programs'])==23 and len(p['required_drivers'])==2 and len(p['drivers'])==5 and len(p['formal'])==3,'whole software boundary')
 allrows=[x for cat in ['programs','required_drivers','drivers','formal'] for x in p[cat]]
 need(len({(x['root'],x['path']) for x in allrows})==33,'whole distinct files')
 need(sum(x['logical_premise'] for x in p['programs'])==17 and sum(not x['logical_premise'] for x in p['programs'])==6,'required/validation roles')
 need(all(x['logical_premise'] for x in p['required_drivers']),'both required decoders')
 need(all(x['whole_file'] for x in p['programs']+p['required_drivers']+p['drivers']),'no routines removed')
 need(p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates')
 need(p['partial_formal_declarations']==17 and p['new_N005_formal_declarations']==0,'partial existing formal scope')
 need(not p['factors_permitted'] and p['ratio'] is None and p['new_source_credit']==p['new_question_credit']==0,'input only no factor/credit')
 need(all(x is None for x in p['unknown_costs'].values()),'outside costs unknown')
 need(p['source_exceptions_outside_this_edition']==['Fi22','Fi24prime'] and p['later_exception_certificates_not_added_here'],'answers separate')
 need(p['diagram_proxy_policy']['status']=='PROPOSED_PENDING_DISTINCT_REVIEW' and p['diagram_proxy_policy']['geometry_cost'] is None and not p['diagram_proxy_policy']['literal_unicode_extraction'],'graphics tokens explicitly proposed')
 need(p['diagram_proxy_policy']['text_only_alternative'] and p['diagram_proxy_policy']['raw_unaltered'],'both graphic sensitivities')
 need('including validation files and both required input drivers' in p['conditional_preacquisition'],'complete conditional preacquisition')
 need(p['baseline_old_common_not_added'] and p['whole_common_paper']=='U','shared complete new common paid once')

def appendix_inclusion(tex,text,programs,expected):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==expected,'whole appendix exact file sequence');need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no code range pruning')
 pack=lambda x:''.join(unicodedata.normalize('NFKC',x).split()).replace('↪','').replace('⌋','')
 for name in names:need(pack(programs[name]) in pack(text),'whole raw program in appendix '+name)
 return dict(whole_files=len(names),range_pruning=False,alternative_to_raw=True,added_to_same_raw=False,printed_wrap_markers_counted=True)

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)==KEYS,'all eleven PDFs')
 protocol=load('protocol.json');need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned libraries')
 for r in protocol['local_bindings']:
  b=(HERE/r['path']).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'fixed local metadata/helper '+r['path'])
 if (HERE/'manifest.json').exists():
  for r in load('manifest.json')['exports']:
   path=Path(r['path']);need(not path.is_absolute() and '..' not in path.parts,'safe export');b=(HERE/path).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'frozen export')
 scientific={r['path']:bound(r,args)[1] for r in p['scientific_bindings']}
 need(load('software_inventory.json')==json.loads(scientific['topic_Operations_input_contract_v1/software_inventory.json']),'software inventory inherited byte-bound contract');scope=load('source_boundary.json');need(scope['N005']['contract']==json.loads(scientific['corpus161_N005_integrated/source_migration.json']),'all N005 dispositions');need(len(scope['N005']['contract']['records'])==81,'all N005 rows')
 need(scope['N006']['contract']==json.loads(scientific['audit/topic-diagonal/v2/source_contract.json']),'all N006 rows');need(scope['N007']['source_clause_map']==json.loads(scientific['papers/topic-diagonal/v1/source_clause_map.json']),'all N007 rows')
 external_ledger_identity(load('external_data.json'),scientific)
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'actual dictionary-bound alias rule')
 docs={};audits={};cache={};alternatives={}
 for key,row in {**p['sources'],**p['replacements']}.items():
  need(all(spec[key][k]==v for k,v in row.items()),'same PDF in policy/spec');pdf,_=bound(row,args);raw,fonts,pages,meta=literal_extract(pdf,key if key in p['sources'] else False)
  need(raw=='\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(pdf).pages),'literal raw pypdf unchanged')
  validate_selection(key,raw,spec[key],pages,meta);events,audits[key]=source_events(pdf,raw,fonts,pages,meta,key,key in p['sources']);cal=calibrate(raw,fonts,pages,events,spec[key],aliases,key)
  texts={'raw_untrimmed':raw,'raw_selected':selected(raw,spec[key]),'calibrated_selected':selected(cal,spec[key])}
  proxies=[g for g in spec[key]['glyph_substitutions'] if g['kind']=='graphical_proxy'];text_only=list(cal)
  for g in proxies:text_only[g['offset']]=' '
  alternatives[key]=dict(proxy_events_removed=len(proxies),rule='Replace only bound proxy events by separators; do not delete ordinary labels or claim measured full graphics.',metrics={n:metrics(selected(''.join(text_only),spec[key]),n) for n in p['normalizations']})
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),graphical_proxy_events=len(proxies),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'fresh actual dictionary/event audit')
 raw_counts={};raw_files={}
 for cat in ['programs','required_drivers','drivers','formal']:
  raw_counts[cat]={}
  for row in p[cat]:
   _,b=bound(row,args);raw_files[row['id']]=b;raw_counts[cat][row['id']]=dict(path=row['path'],bytes=len(b),sha256=sha(b),role=row['role'],metrics={n:metrics(b.decode(),n) for n in p['normalizations']})
 app1=appendix_inclusion(scientific['papers/topic-diagonal/v1/programs.tex'].decode(),cache['CODEold']['texts']['raw_selected'],{'programs/diagonal_models.g':raw_files['P.N007.diagonal_models'].decode()},['programs/diagonal_models.g'])
 expected=['programs/affine_example.py','programs/presentation_identities.py','programs/literal_twist.py'];app2=appendix_inclusion(scientific['corpus161_N005_integrated/programs.tex'].decode(),cache['CODEnew']['texts']['raw_selected'],{name:raw_files['P.N005.'+Path(name).stem].decode() for name in expected},expected)
 previous=load('prior_count_reference.json')
 for k in ['N006','N007','A2nine','A2HN','CODEold']:need(docs[k]['metrics']==previous['documents'][k]['metrics'],'byte-identical prior coordinate '+k)
 return dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',original_manuscripts=3,pdf_documents=11,pdf_pages=161,pdf_metric_cells=330,raw_metric_cells=330,documents=docs,text_only_sensitivity=alternatives,text_only_sensitivity_cells=110,raw_files=raw_counts,partial_appendix_alternatives={'CODEold':app1,'CODEnew':app2},external=validate_external(load('external_data.json')),ratio=None,scientific_programs_executed=False,full_formalization_claim=False,unknown_costs=p['unknown_costs']),audits,cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);r,au,_=replay(a)
 for name,obj in [('counts.json',r),('font_audit.json',au)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS: eleven whole PDFs/161 pages; 330 PDF and 330 raw cells; no factors.')
if __name__=='__main__':main()
