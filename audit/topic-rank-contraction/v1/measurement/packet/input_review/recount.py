#!/usr/bin/env python3
"""Independent L037 input recount. Uses pypdf/fontTools, no author Python imports."""
import argparse, copy, hashlib, io, json, re, unicodedata
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
from fontTools.cffLib import CFFFontSet
from fontTools.pens.recordingPen import RecordingPen

AUTHOR_SHA='4df2508c988ca14e00c550a8da68d485c3631061bbf19888b86f521886deefaf'
PDFS={'L037':('sources/rank_reduction2019.pdf',6),'U':('topic_B_L037_recovery/umbrella.pdf',3),'A1':('topic_B_L037_recovery/rank_spectra.pdf',5),'CODE':('topic_B_L037_recovery/programs.pdf',1)}
RAW={'programs':'topic_B_L037_recovery/check_examples.g','drivers':'topic_B_L037_recovery/check.py','formal':'topic_B_L037_recovery/RankContraction.lean'}
BRACKETS={50:('bracketlefttp','\uf8ee','⎡'),51:('bracketrighttp','\uf8f9','⎤'),52:('bracketleftbt','\uf8f0','⎣'),53:('bracketrightbt','\uf8fb','⎦'),54:('bracketleftex','\uf8ef','⎢'),55:('bracketrightex','\uf8fa','⎥')}
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(b,m):
 if not b: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def textsha(s): return sha(s.encode())
def load(p): return json.loads(p.read_text())
def pin(p): return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def counts(s,norm):
 s=unicodedata.normalize(norm,s);words=s.split();c=' '.join(words)
 # Independent maximal alphanumeric runs; underscores and punctuation terminate runs.
 runs=0;inside=False
 for ch in s:
  if ch.isalnum():
   if not inside:runs+=1
   inside=True
  else:inside=False
 return dict(zip(UNITS,[len(words),runs,sum(not ch.isspace() for ch in s),len(c),len(c.encode())]),normalized_text_sha256=textsha(s),collapsed_text_sha256=textsha(c))
def edits(s,events):
 for a,b,v in sorted(events,reverse=True): s=s[:a]+v+s[b:]
 return s

def extract(study):
 docs={};texts={};furniture={};pages_by_doc={}
 for key,(path,np) in PDFS.items():
  reader=PdfReader(study/path);pages=[p.extract_text() for p in reader.pages];need(len(pages)==np,'complete page count '+key)
  body='\n'.join(pages);cuts=[];offs=0
  for i,p in enumerate(pages,1):
   if key=='L037' and i>1:
    header=f'{i} PETER A. BROOKSBANK AND DIMITRI LEEMANS\n' if i%2==0 else f'RANK REDUCTION OF STRING C-GROUP REPRESENTATIONS {i}\n'
    need(p.startswith(header),'running header');a=offs;b=offs+len(header)
   else:
    need(p.endswith('\n'+str(i)),'isolated trailing page number '+key);a=offs+len(p)-len(str(i));b=offs+len(p)
   cuts.append({'page':i,'start':a,'end':b,'literal':body[a:b],'sha256':textsha(body[a:b])});offs+=len(p)+1
  furniture[key]=cuts;pages_by_doc[key]=pages;texts[key]=body
  docs[key]={'pdf_sha256':sha((study/path).read_bytes()),'pages':np,'furniture_cuts':len(cuts),'glyph_repairs':8 if key=='L037' else 0}
 return docs,texts,furniture,pages_by_doc

def actual_glyphs(study,pages):
 reader=PdfReader(study/PDFS['L037'][0]);events=[];xy=[];offset=0;visitor_events=[];outlines={};fontpins={}
 for page_no,page in enumerate(reader.pages,1):
  chunks=[]
  def visit(t,cm,tm,font,size):
   chunks.append((t,font))
  need(page.extract_text(visitor_text=visit)==pages[page_no-1],'visitor extraction')
  need(''.join(x[0] for x in chunks)==pages[page_no-1],'visitor concatenation')
  local=0
  for t,font in chunks:
   for j,ch in enumerate(t):
    if 0xE000<=ord(ch)<=0xF8FF:
     need(font is not None and font['/BaseFont']=='/QJOUSI+CMEX10','unexpected source PUA')
     visitor_events.append({'page':page_no,'page_offset':local+j,'start':offset+local+j,'input':ch})
   local+=len(t)
  current=None
  for op_index,(args,op) in enumerate(page.get_contents().operations):
   if op==b'Tf':current=str(args[0])
   if op not in (b'Tj',b'TJ',b"'",b'"'):continue
   parts=args[0] if op==b'TJ' else [args[-1]]
   font=page['/Resources']['/Font'][current];name=str(font['/BaseFont'])
   if name not in ['/QJOUSI+CMEX10','/TFMQEJ+XYCIRC-Medium']:continue
   enc={};at=None
   for e in font['/Encoding']['/Differences']:
    if isinstance(e,int):at=e
    else:enc[at]=str(e)[1:];at+=1
   ident=font.indirect_reference
   fs=font['/FontDescriptor']['/FontFile3'].get_data();fontpins[name]={'object':ident.idnum,'generation':ident.generation,'stream_sha256':sha(fs),'encoding_differences':list(font['/Encoding']['/Differences']),'to_unicode_present':'/ToUnicode' in font}
   if name=='/QJOUSI+CMEX10':
    cmap=font['/ToUnicode'].get_data().decode();mapping={}
    # This font uses exactly six one-byte, singleton bfrange records.
    for block in re.findall(r'beginbfrange(.*?)endbfrange',cmap,re.S):
     for lo,hi,out in re.findall(r'<([0-9a-f]+)>\s*<([0-9a-f]+)>\s*<([0-9a-f]+)>',block):
      need(lo==hi,'singleton bracket cmap');mapping[int(lo,16)]=bytes.fromhex(out).decode('utf-16-be')
    need(set(mapping)==set(BRACKETS),'bracket cmap domain')
   for part_index,part in enumerate(parts):
    if not isinstance(part,(str,bytes)):continue
    raw=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
    for byte_index,b in enumerate(raw):
     ev={'page':page_no,'operator_index':op_index,'operator':op.decode(),'part_index':part_index,'byte_index':byte_index,'encoded_byte':b,'font_resource':current,'font_dictionary_object':{'idnum':ident.idnum,'generation':ident.generation},'text_part_sha256':sha(raw),'glyph_name':enc[b],'font_stream_sha256':sha(fs)}
     if name=='/QJOUSI+CMEX10' and b in BRACKETS:
      glyph,decoded,output=BRACKETS[b];need(enc[b]==glyph and mapping[b]==decoded,'actual byte/encoding/ToUnicode mismatch');ev.update(input=decoded,output=output);events.append(ev)
     elif name=='/TFMQEJ+XYCIRC-Medium':
      need(16<=b<=23 and enc[b]==f'c{b}','literal diagram encoded glyph');xy.append(ev)
   if name not in outlines:
    cff=CFFFontSet();cff.decompile(io.BytesIO(fs),None);cs=cff[cff.fontNames[0]].CharStrings
    outlines[name]={}
    for b in sorted(BRACKETS if name=='/QJOUSI+CMEX10' else range(16,24)):
     pen=RecordingPen();cs[enc[b]].draw(pen);need(bool(pen.value),'nonempty visible outline');outlines[name][str(b)]={'glyph':enc[b],'drawing':pen.value,'drawing_sha256':textsha(json.dumps(pen.value,separators=(',',':')))}
  offset+=len(pages[page_no-1])+1
 need(len(events)==len(visitor_events)==8,'eight actual bracket events')
 for e,v in zip(events,visitor_events):
  need(e['page']==v['page'] and e['input']==v['input'],'event to extraction occurrence alignment');e.update(v);e['end']=e['start']+1
 need(Counter(e['encoded_byte'] for e in xy)==Counter({i:33 for i in range(16,24)}),'all 264 diagram events')
 for i in range(16,24):need(''.join(pages).count(f'/c{i}')==33,'literal diagram strings')
 return events,xy,fontpins,outlines

def compare(actual,expected,label):need(actual==expected,label)
def run(study,author,out):
 need(not out.exists() and not out.is_symlink(),'fresh output required');out.mkdir(parents=True)
 need(sha((author/'manifest.json').read_bytes())==AUTHOR_SHA,'immutable author manifest')
 manifest=load(author/'manifest.json')
 for e in manifest['exports']:compare(pin(author/e['path']),{k:e[k] for k in ('bytes','sha256')},'author export '+e['path'])
 policy=load(author/'policy.json');spec=load(author/'input_spec.json');expected=load(author/'author_counts.json')
 for binding in policy['scientific_bindings']:
  compare(pin(study/binding['path']),{k:binding[k] for k in ('bytes','sha256')},'scientific boundary pin')
 need(policy['primary']=='raw_untrimmed NFC characters_without_whitespace; complete source/common/application including all furniture','raw complete primary')
 need(policy['source_rows']==22 and policy['proof_contexts']==20 and policy['original_manuscripts']==1,'scientific scope cardinalities')
 need(policy['whole_common_paper_charged'] and policy['existing_B_common_is_not_a_prerequisite'] and not policy['cross_topic_discount'],'common acquisition')
 need(policy['all_declared_code_prepurchased_for_conditional_results'] and policy['raw_and_printed_code_are_alternatives'],'complete alternative code policy')
 need(policy['program_files']==policy['local_finite_certificate_programs']==1 and policy['uniform_required_programs']==0 and policy['driver_files']==policy['formal_files']==1,'distinct code roles')
 need(policy['partial_formal_declarations']==4 and not policy['whole_source_formalized'],'scoped formal boundary')
 need(all(x is None for x in policy['unknown_costs'].values()) and policy['ratio'] is None and policy['factors_permitted'] is False,'unknowns and no factors')
 docs,texts,furniture,pages=extract(study)
 events,xy,fontpins,outlines=actual_glyphs(study,pages['L037'])
 for key in PDFS:
  compare(pin(study/PDFS[key][0]),{k:spec[key][k] for k in ('bytes','sha256')},'PDF pin')
  compare(furniture[key],spec[key]['excluded_furniture'],'independent furniture '+key)
  need(spec[key]['included_spans']==[{'start':0,'end':len(texts[key]),'sha256':textsha(texts[key])}],'whole PDF input '+key)
  need(len(pages[key])==len(spec[key]['page_bindings']),'all page bindings')
  offset=0
  for p,record in zip(pages[key],spec[key]['page_bindings']):
   need(record['start']==offset and record['end']==offset+len(p) and record['sha256']==textsha(p),'page text binding');offset+=len(p)+1
  selected=edits(texts[key],[(c['start'],c['end'],'\n') for c in furniture[key]])
  substitutions=[(e['start'],e['end'],e['output']) for e in events] if key=='L037' else []
  calibrated=edits(texts[key],substitutions+[(c['start'],c['end'],'\n') for c in furniture[key]])
  variants={'raw_untrimmed':texts[key],'raw_selected':selected,'calibrated_selected':calibrated}
  docs[key]['metrics']={v:{n:counts(s,n) for n in ('NFC','NFKC')} for v,s in variants.items()}
  compare(docs[key],expected['documents'][key],'all document counts and hashes '+key)
 for e,want in zip(events,spec['L037']['glyph_substitutions']):
  for k in ['start','end','page','page_offset','input','output']:compare(e[k],want[k],'event '+k)
  for k in ['operator_index','operator','part_index','byte_index','encoded_byte','font_resource','font_dictionary_object','text_part_sha256','glyph_name','font_stream_sha256']:compare(e[k],want['pdf_events'][0][k],'actual event '+k)
  need(textsha(texts['L037'][want['context_start']:want['context_end']])==want['context_sha256'],'bound glyph context')
 compare(len(spec['L037']['glyph_substitutions']),8,'repair cardinality')
 raw={}
 for category,path in RAW.items():
  p=study/path;row=expected['raw_files'][category][path];compare(pin(p),{k:row[k] for k in ('bytes','sha256')},'raw pin')
  m={n:counts(p.read_text(),n) for n in ('NFC','NFKC')};compare(m,row['metrics'],'whole raw count '+path);raw[path]={'category':category,**pin(p),'metrics':m}
 tex=(study/'topic_B_L037_recovery/programs.tex').read_text()
 need(len(re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{check_examples\.g\}',tex))==1 and 'firstline' not in tex and 'lastline' not in tex,'complete printed program')
 need('References' in texts['A1'] and 'References' in texts['L037'],'references included')
 # Focused controls operate on independent recomputations, not the author's verifier.
 controls=[]
 def reject(name,fn):
  try:fn()
  except ValueError:controls.append({'name':name,'rejected':True});return
  raise ValueError('control accepted '+name)
 reject('omit application references-only last page',lambda:compare(counts('\n'.join(pages['A1'][:-1]),'NFC'),docs['A1']['metrics']['raw_untrimmed']['NFC'],'lost references'))
 reject('omit source title and arxiv banner',lambda:compare(counts('\n'.join(pages['L037'][1:]),'NFC'),docs['L037']['metrics']['raw_untrimmed']['NFC'],'lost title'))
 reject('misdeclare raw primary as furniture-removed',lambda:compare(docs['L037']['metrics']['raw_selected'],docs['L037']['metrics']['raw_untrimmed'],'primary changed'))
 reject('drop whole common theory',lambda:compare(set(docs)-{'U'},set(PDFS),'common omitted'))
 reject('truncate required local certificate',lambda:compare(counts((study/RAW['programs']).read_text()[:1000],'NFC'),raw[RAW['programs']]['metrics']['NFC'],'program truncated'))
 reject('erase diagram strings',lambda:compare(counts(re.sub(r'/c(?:1[6-9]|2[0-3])','',texts['L037']),'NFC'),docs['L037']['metrics']['raw_untrimmed']['NFC'],'diagram erased'))
 reject('replace diagrams by circle proxies',lambda:compare(counts(re.sub(r'/c(?:1[6-9]|2[0-3])','○',texts['L037']),'NFC'),docs['L037']['metrics']['raw_untrimmed']['NFC'],'proxy unapproved'))
 mutated=copy.deepcopy(spec['L037']['glyph_substitutions']);mutated[0]['output']='⎧'
 reject('bracket changed to brace at bound occurrence',lambda:compare(mutated[0]['output'],events[0]['output'],'incorrect visible outline'))
 reject('shift bracket event byte',lambda:compare(events[0]['encoded_byte']+1,spec['L037']['glyph_substitutions'][0]['pdf_events'][0]['encoded_byte'],'incorrect byte'))
 reject('shift bracket font dictionary',lambda:compare({'idnum':96,'generation':0},events[0]['font_dictionary_object'],'wrong dictionary'))
 reject('forget bracket repair despite unchanged five metrics',lambda:compare(docs['L037']['metrics']['raw_selected']['NFC']['normalized_text_sha256'],docs['L037']['metrics']['calibrated_selected']['NFC']['normalized_text_sha256'],'wrong calibrated text'))
 reject('change collapsed whitespace policy',lambda:compare(counts(texts['U'].replace('\n',''),'NFC'),docs['U']['metrics']['raw_untrimmed']['NFC'],'joined words'))
 reject('normalize raw formal file only NFC',lambda:compare(raw[RAW['formal']]['metrics']['NFC'],raw[RAW['formal']]['metrics']['NFKC'],'NFKC omitted'))
 reject('truncate final source addresses',lambda:compare(counts(texts['L037'][:-400],'NFC'),docs['L037']['metrics']['raw_untrimmed']['NFC'],'addresses omitted'))
 result={'status':'PASS','author_manifest_sha256':AUTHOR_SHA,'implementation':'Independent pypdf extraction, line-based furniture, content-operator/Encoding/ToUnicode/CFF event verification; no author Python imports.','pdf_metric_cells':120,'raw_metric_cells':30,'normalized_and_collapsed_text_hashes_compared':60,'pages':15,'bracket_events':8,'diagram_encoded_events':264,'diagram_literal_strings_preserved':True,'document_counts':docs,'raw_counts':raw,'furniture':furniture,'bracket_event_evidence':events,'font_pins':fontpins,'outline_records':{font:{byte:{k:v for k,v in record.items() if k!='drawing'} for byte,record in records.items()} for font,records in outlines.items()},'controls':controls,'science_replayed':False,'factors_computed':False}
 (out/'recount.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','normalized_and_collapsed_text_hashes_compared','pages','bracket_events','diagram_encoded_events']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--author',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.study_root.resolve(),a.author.resolve() if a.author else a.study_root.resolve()/'topic_B_L037_measurement_inputs',a.out)
