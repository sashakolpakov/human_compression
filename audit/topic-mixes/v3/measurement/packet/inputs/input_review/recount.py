#!/usr/bin/env python3
"""Distinct three-source Mixes recount: own extraction masks, metric loops and PDF event walk.
Only the reviewed low-level embedded-font parser is shared and disclosed.
No author metric, furniture, calibration or replay function is imported.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import argparse,json,hashlib,unicodedata,re,sys
import pypdf
from pypdf.generic import ContentStream,TextStringObject,ByteStringObject
from pypdf import _cmap

def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def metric(t,normal):
 t=unicodedata.normalize(normal,t);words=t.split();c=' '.join(words);runs=0;prior=False;nonspace=0
 for ch in t:
  flag=ch.isalnum()
  if flag and not prior:runs+=1
  prior=flag;nonspace+=not ch.isspace()
 return dict(whitespace_tokens=len(words),alphanumeric_units=runs,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode('utf-8')),collapsed_text_sha256=digest(c.encode()))
def bound(root,row):
 rel=Path(row['path']);require(not rel.is_absolute()and'..'not in rel.parts,'relative path');f=root/rel;b=f.read_bytes();require(len(b)==row['bytes']and digest(b)==row['sha256'],'binding '+str(rel));return f,b

def own_cuts(k,pages):
 cuts=[];at=0
 for n,t in enumerate(pages,1):
  if k=='F007':
   if n>1:
    header=(f'23 Page {n} of 29 Journal of Algebraic Combinatorics (2026) 64:23 \n' if n%2==0 else f'Journal of Algebraic Combinatorics (2026) 64:23 Page {n} of 29 23 \n')
    require(t.startswith(header),'exact observed source header');cuts.append((at,at+len(header)))
   footer='0123456789().: V,-vol 123'if n==1 else'123'
   require(t.endswith(footer),'exact observed source footer');cuts.append((at+len(t)-len(footer),at+len(t)))
  else:
   require(t.endswith('\n'+str(n)),'own isolated folio');cuts.append((at+len(t)-len(str(n)),at+len(t)))
  at+=len(t)+1
 return cuts

def apply_mask(t,cuts):
 mask=bytearray(b'\1')*len(t)
 for a,b in cuts:
  require(0<=a<b<=len(t),'valid cut');require(all(mask[a:b]),'disjoint cuts');mask[a:b]=bytes(b-a)
 # Every removed run becomes one separator, exactly preserving the declared selection convention.
 out=[];inside=False
 for i,ch in enumerate(t):
  if mask[i]:out.append(ch);inside=False
  elif not inside:out.append('\n');inside=True
 return ''.join(out)

def plain(v):
 v=v.get_object()if hasattr(v,'get_object')else v
 if isinstance(v,dict):return {str(k):plain(w)for k,w in sorted(v.items())}
 if isinstance(v,list):return [plain(w)for w in v]
 return v if v is None or isinstance(v,(bool,int,float))else str(v)

def source_events(pdf,page_texts,font_parser):
 reader=pypdf.PdfReader(pdf);fonts={};uses=Counter();out={};offset=0;visible_white=[]
 def identity(f):
  r=f.indirect_reference;obj=dict(idnum=r.idnum,generation=r.generation);buf=BytesIO();f.write_to_stream(buf)
  base=dict(font_dictionary_object=obj,font_dictionary_sha256=digest(buf.getvalue()),pdf_encoding_declaration=plain(f.get('/Encoding')))
  fid=digest(json.dumps(base,sort_keys=True).encode())
  if fid not in fonts:
   stream,mapping,strings=font_parser(f);fonts[fid]=dict(base,font=str(f.get('/BaseFont','')),mapping=mapping,strings=strings,stream=stream)
  return fid
 def walk(reader,content,res,active=None):
  stack=[]
  for operands,op in ContentStream(content,reader).operations:
   if op==b'q':stack.append(active)
   elif op==b'Q':active=stack.pop()
   elif op==b'Tf':active=res['/Font'][operands[0]].get_object()
   elif op==b'Do':
    x=res['/XObject'][operands[0]].get_object()
    if x.get('/Subtype')=='/Form':yield from walk(reader,x,x.get('/Resources',res),active)
   elif op in (b'Tj',b'TJ',b"'",b'"'):
    require(active is not None and active.get('/Subtype')=='/Type1','actual one-byte source font');fid=identity(active);enc,cmap=_cmap.get_encoding(active)
    for part in operands[0]if op==b'TJ'else[operands[-1]]:
     if not isinstance(part,(TextStringObject,ByteStringObject)):continue
     data=part.original_bytes if hasattr(part,'original_bytes')else bytes(part)
     for byte in data:
      raw=enc.get(byte,chr(byte))if isinstance(enc,dict)else bytes([byte]).decode(enc);text=''.join(cmap.get(c,c)for c in raw);name=fonts[fid]['mapping'].get(byte)
      require(name not in (None,'.notdef'),'actual glyph encoding');uses[fid,byte,text,name]+=1
      if text.isspace():
       strings=fonts[fid]['strings']
       if strings is None:visible=name!='space'
       else:
        from fontTools.pens.recordingPen import RecordingPen
        pen=RecordingPen();strings[name].draw(pen);visible=any(k not in ('endPath','closePath')for k,v in pen.value)
       if visible:visible_white.append((fid,byte,text,name))
      for j,ch in enumerate(text):
       if not ch.isspace():yield ch,(fid,byte,name,j,text)
 for n,(pg,t)in enumerate(zip(reader.pages,page_texts),1):
  expected=[(i,ch)for i,ch in enumerate(t)if not ch.isspace()];actual=list(walk(reader,pg.get_contents(),pg['/Resources']))
  require(len(actual)==len(expected),'all nonspace actual source events '+str(n))
  for (ch,event),(i,ch2)in zip(actual,expected):require(ch==ch2,'actual event/extraction equality');out[offset+i]=event
  offset+=len(t)+1
 require(not visible_white,'no unpriced visible whitespace glyphs')
 return out,fonts,uses


def splice(raw,edits):
 at=0;parts=[]
 for a,b,t in sorted(edits):
  require(at<=a<b<=len(raw),'nonoverlapping actual text spans');parts.extend([raw[at:a],t]);at=b
 parts.append(raw[at:]);return ''.join(parts)

def check_policy(p,code):
 require(p['originals']==['F005','L016','F007']and p['new_source']=='F007','exact three originals')
 require(p['primary']=='raw_untrimmed/NFC/characters_without_whitespace','fixed whole raw primary')
 require(p['whole_documents']and not p['overlap_discount'],'whole documents no overlap discount')
 b=p['whole_topic_boundary'];require(b['source_documents']==['F005','L016','F007']and b['common_documents']==['U','U1','U2'],'whole three common/source papers')
 require(b['applications']=={'F005':['A1','A2'],'L016':['A3'],'F007':['A4','A5']},'whole five application papers including companion')
 require((b['source_pages'],b['common_pages'],b['application_pages'])==(62,13,27)and b['no_free_old_common']and b['companion_is_application'],'whole page inventories')
 require({k:r['pages']for k,r in p['new_documents'].items()}=={'F007':29,'U2':4,'A4':5,'A5':4},'all new pages')
 require(set(p['retained_documents'])=={'F005','U','A1','A2','CODE1','CODE2','L016','U1','REQ','VAL','A3'},'all old documents')
 s=p['software_boundary'];require([len(s[k])for k in ['required_full_programs','optional_full_programs','drivers','formal']]==[2,6,6,3],'whole software role split')
 roles={k:[r['path']for r in s[k]]for k in ['required_full_programs','optional_full_programs','drivers','formal']};allpaths=sum(roles.values(),[])
 require(len(set(allpaths))==17,'dual-role file counted once')
 require([Path(f).name for f in roles['required_full_programs']]==['check_coprime.g','base_certificate.g'],'exact required certificates')
 require(all(not r.get('mathematical_premise',r.get('uniform_mathematical_premise',False))for r in s['optional_full_programs']),'optional tests no proof premise')
 require(s['partial_declarations']==12 and not s['full_source_formalized'],'partial twelve declarations')
 require(s['printed_and_raw_never_additive']and s['dual_role_companion_checker_charged_once']and not s['new_optional_programs_printed'],'raw and printed alternative')
 require(p['symmetry']['manuscript_comparison_excludes_executable_listings_both_sides']and p['symmetry']['optional_validation_is_not_a_conditional_prerequisite'],'symmetric software boundary')
 require(p['symmetry']['software_inclusive_factor']is None and p['symmetry']['unprovided_historical_software']is None,'unknown software is null')
 require(all(v is None for v in p['unknown_costs'].values())and p['ratio']is None and not p['factors_permitted']and p['new_scientific_credit']==0,'no ratios or new credits')
 require(p['scope']['F005_rows']==35 and p['scope']['L016_rows']==19 and p['scope']['F007_numbered']==48 and p['scope']['F007_additional']==6,'exact inherited scientific boundary')
 require(p['scope']['F007_page25_chain_class_paragraph']=='not recovered'and p['scope']['F007_problems1_and2']=='unanswered','excluded claims remain visible')
 require(code['new_source']['physical_pages']==list(range(1,30))and code['new_source']['masks']==[]and code['new_source']['embedded_executable_blocks']==[]and code['new_source']['embedded_optional_validation']==[],'all-page no-listing boundary')
 require(code['new_replacement_masks']=={'U2':[],'A4':[],'A5':[]}and code['source_software_cost']is None,'symmetric empty masks/unknown software')

def compare_metrics(actual,want,label):
 require(actual==want,'independent cells/hash '+label)

def run(packet,root):
 import copy
 from fontTools import __version__ as ftversion
 require(pypdf.__version__=='6.13.0'and ftversion=='4.63.0','pinned extraction dependencies')
 load=lambda n:json.loads((packet/n).read_text());man=load('manifest.json')
 require(digest((packet/'manifest.json').read_bytes())=='693eef736aa202a3d633c3a9a00944d1391d1dd7af6cacfe49c953d5ec93b220','author freeze')
 for row in man['exports']:bound(packet,row)
 require(len(man['exports'])==30,'whole export count')
 p=load('policy.json');code=load('source_code_boundary.json');check_policy(p,code)
 require((packet/'policy_before_counts.json').read_bytes()==(packet/'policy.json').read_bytes(),'fixed before-count policy')
 for row in p['acceptances']+p['retained_counts']:bound(root,row)
 for row in p['retained_documents'].values():bound(root,row)
 for cat in ['required_full_programs','optional_full_programs','drivers','formal']:
  for row in p['software_boundary'][cat]:bound(root,row)
 spec=load('input_spec.json');expected=load('author_counts.json');audit=load('font_audit.json');aliases=load('glyph_aliases.json')['aliases']
 sys.path.insert(0,str(packet));from font_tools import embedded # only shared embedded-font-byte parser
 counts={};pdfcells=0;hashes=0;actualtexts={};fontreport={};source_repairs=[];source_cuts=[];unicode_fonts={}
 for key,row in p['new_documents'].items():
  path,_=bound(root,row);reader=pypdf.PdfReader(path);pages=[pg.extract_text()or''for pg in reader.pages];raw='\n'.join(pages);actualtexts[key]=raw
  require(len(pages)==row['pages'],'complete physical pages');require(digest(raw.encode())==spec[key]['extraction_sha256'],'whole extraction binding')
  require(spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=digest(raw.encode()))],'whole text selection')
  at=0
  for n,t in enumerate(pages,1):
   r=spec[key]['page_bindings'][n-1];require((r['page'],r['start'],r['end'],r['sha256'])==(n,at,at+len(t),digest(t.encode())),'all physical page bindings');at+=len(t)+1
  cuts=own_cuts(key,pages);require(cuts==[(r['start'],r['end'])for r in spec[key]['excluded_furniture']],'independent exact furniture spans')
  repairs=[]
  if key=='F007':
   events,fonts,uses=source_events(path,pages,embedded)
   want={(r['font_identity'],r['encoded_byte'],r['decoded_text'],r['glyph_name']):r['occurrences']for r in audit[key]['encoded_glyph_classes']}
   require(dict(uses)==want,'independent source class/event census');require(set(fonts)=={r['font_identity']for r in audit[key]['font_dictionaries']},'actual dictionary identity')
   for r in audit[key]['font_dictionaries']:
    f=fonts[r['font_identity']];require({str(k):v for k,v in f['mapping'].items()}==r['effective_encoding'],'full effective font encoding');require(f['stream']==r['font_stream_sha256'],'actual embedded stream')
   amap={(r['font_identity'],r['encoded_byte'],r['glyph_name']):r for r in aliases};require(len(amap)==18,'eighteen actual classes');applied=Counter()
   for i,(fid,byte,name,j,text)in events.items():
    if (fid,byte,name)in amap and j==0:
     r=amap[fid,byte,name];require(text==r['input']and len(r['output'])==1,'one observed glyph with possibly multi-character alias')
     require(raw[i:i+len(text)]==text,'contiguous actual encoded glyph text')
     for q,ch in enumerate(text):require(events[i+q]==(fid,byte,name,q,text),'every decoded character same actual glyph')
     repairs.append((i,i+len(text),r['output']));applied[fid,byte,name]+=1
   require(all(applied[k]==r['occurrences']for k,r in amap.items()),'all alias counts independently found')
   require(sorted(repairs)==[(r['start'],r['end'],r['output'])for r in spec[key]['glyph_substitutions']],'all actual substitutions independently located')
   for r in spec[key]['glyph_substitutions']:
    require(digest(raw[r['context_start']:r['context_end']].encode())==r['context_sha256'],'repair local context')
    own=[events[i]for i in range(r['start'],r['end'])];given=[(e['font_identity'],e['encoded_byte'],e['glyph_name'],e['decoded_character_index'],e['decoded_text'])for e in r['pdf_events']];require(own==given,'bound substitutions actual byte evidence')
   fontreport=dict(actual_dictionaries=len(fonts),encoded_classes=len(uses),alias_classes=len(amap),alias_events=len(repairs),unembedded_fonts=sum(r['stream']is None for r in fonts.values()),actual_space_events=sum(n for(fid,b,t,g),n in uses.items()if t.isspace()),visible_whitespace_glyphs=0,nonspace_extraction_characters=len(events))
   require((len(fonts),len(uses),len(repairs))==(20,443,1351),'exact source glyph census');source_repairs=list(repairs);source_cuts=list(cuts)
  else:
   identities={}
   # Fresh reader preserves original indirect DescendantFonts before pypdf extraction dereferences them.
   for pg in pypdf.PdfReader(path).pages:
    for ref in pg['/Resources']['/Font'].values():
     f=ref.get_object();require(f.get('/Subtype')=='/Type0','own Unicode Type0 font');r=f.indirect_reference;buf=BytesIO();f.write_to_stream(buf)
     identities[r.idnum,r.generation]=dict(font_dictionary_object=dict(idnum=r.idnum,generation=r.generation),font_dictionary_sha256=digest(buf.getvalue()),pdf_encoding_declaration=plain(f.get('/Encoding')),font=str(f.get('/BaseFont','')),subtype=str(f.get('/Subtype')))
   want={(r['font_dictionary_object']['idnum'],r['font_dictionary_object']['generation']):{k:v for k,v in r.items()if k!='scope'}for r in audit[key]['unchanged_type0_dictionaries']}
   require(identities==want,'independent own Unicode dictionary census');unicode_fonts[key]=len(identities)
   require(spec[key]['glyph_substitutions']==[],'own literal text no repairs')
   require(not any(ord(ch)<32 and not ch.isspace()or 0xE000<=ord(ch)<=0xF8FF or ch=='\uFFFD'for ch in raw),'own no control/PUA/replacement glyph')
  variants={'raw_untrimmed':raw,'raw_selected':splice(raw,[(a,b,'\n')for a,b in cuts]),'calibrated_selected':splice(raw,[(a,b,'\n')for a,b in cuts]+repairs)}
  counts[key]={}
  for variant,t in variants.items():
   counts[key][variant]={}
   for norm in ['NFC','NFKC']:
    got=metric(t,norm);compare_metrics(got,expected['documents'][key]['metrics'][variant][norm],key+'/'+variant+'/'+norm);counts[key][variant][norm]=got;pdfcells+=5;hashes+=1
 rawcells=0
 for cat,rows in p['new_raw_files'].items():
  for r in rows:
   _,b=bound(root,r)
   for norm in ['NFC','NFKC']:
    compare_metrics(metric(b.decode(),norm),expected['raw_files'][cat][r['path']]['metrics'][norm],r['path']+'/'+norm);rawcells+=5;hashes+=1
 old0=json.loads(bound(root,p['retained_counts'][0])[1]);old1=json.loads(bound(root,p['retained_counts'][1])[1]);ret=load('retained_counts.json')
 docs=dict(old0['documents'],**old1['documents']);require(ret['documents']==docs,'all330 retained document cells exact')
 require(old1['retained_accepted_inputs']==old0,'all old nested accepted objects unchanged')
 raws={k:dict(old0['raw_files'][k],**old1['raw_files'][k])for k in old0['raw_files']}
 require(ret['raw_files']==raws,'all130 retained raw cells exact');require(expected['retained_accepted_inputs']==ret,'new counts preserve exact retained objects')
 require(sum(len(rows)for rows in raws.values())==13 and len(docs)==11,'whole retained file counts')
 require(expected['whole_topic_boundary']==p['whole_topic_boundary']and expected['software_boundary']==p['software_boundary'],'counts exact complete boundary')
 require(expected['ratio']is None and expected['software_inclusive_factor']is None and not expected['scientific_programs_executed']and not expected['whole_source_formalized'],'no ratios or full theorem claim')
 # Meaningful tests bypass manifest binding and exercise their actual semantic validators.
 controls=[]
 def rejected(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):controls.append({'control':name,'rejected':True});return
  raise ValueError('control accepted '+name)
 def pol(name,mutate):
  q=copy.deepcopy(p);c=copy.deepcopy(code);mutate(q,c);rejected(name,lambda:check_policy(q,c))
 pol('omit full rank-three companion',lambda q,c:q['whole_topic_boundary']['applications']['F007'].remove('A5'))
 pol('silently free prior common theory',lambda q,c:q['whole_topic_boundary']['common_documents'].remove('U'))
 pol('discard short final companion page',lambda q,c:q['new_documents']['A5'].update(pages=3))
 pol('optional validation promoted to premise',lambda q,c:q['software_boundary']['optional_full_programs'][-1].update(mathematical_premise=True))
 pol('dual-role companion double charged',lambda q,c:q['software_boundary']['drivers'].append(q['software_boundary']['optional_full_programs'][-1]))
 pol('unknown historical code set to zero',lambda q,c:q['symmetry'].update(unprovided_historical_software=0))
 pol('raw plus printed program added',lambda q,c:q['software_boundary'].update(printed_and_raw_never_additive=False))
 pol('source-only executable exclusion',lambda q,c:c['new_source'].update(masks=[{'start':1,'end':3}]))
 pol('omit one source page from screening',lambda q,c:c['new_source']['physical_pages'].remove(29))
 pol('invent full formalization',lambda q,c:q['software_boundary'].update(full_source_formalized=True))
 pol('claim excluded paragraph recovered',lambda q,c:q['scope'].update(F007_page25_chain_class_paragraph='recovered'))
 pol('invent question answer',lambda q,c:q['scope'].update(F007_problems1_and2='answered'))
 pol('calculate factor before input acceptance',lambda q,c:q.update(ratio=1.0))
 pol('use calibrated ruler as fixed primary',lambda q,c:q.update(primary='calibrated_selected/NFC/characters_without_whitespace'))
 rejected('wrong actual encoded glyph substitution',lambda:require(source_repairs==[(r['start'],r['end'],'Z'if n==0 else r['output'])for n,r in enumerate(spec['F007']['glyph_substitutions'])],'actual glyph disagreement'))
 mutcut=list(source_cuts);mutcut[0]=(mutcut[0][0]-1,mutcut[0][1])
 rejected('remove one source body character as furniture',lambda:require(mutcut==source_cuts,'independent furniture mismatch'))
 rejected('alter one numeric coordinate',lambda:compare_metrics(dict(counts['F007']['raw_untrimmed']['NFC'],characters_without_whitespace=0),expected['documents']['F007']['metrics']['raw_untrimmed']['NFC'],'mutated scalar'))
 rejected('overlap calibration and furniture spans',lambda:splice('abcd',[(0,3,'x'),(2,4,'y')]))
 mutated=copy.deepcopy(ret['documents']);mutated['U']['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']+=1
 rejected('change retained common cost',lambda:require(mutated==docs,'retained values'))
 require((pdfcells,rawcells,hashes)==(120,40,32),'complete new cells and hashes')
 return dict(status='PASS_DISTINCT_INPUT_RECOUNT',author_manifest_sha256=digest((packet/'manifest.json').read_bytes()),new_PDF_cells=pdfcells,new_raw_cells=rawcells,new_collapsed_hashes=hashes,retained_PDF_cells_unchanged=330,retained_raw_cells_unchanged=130,new_metrics=counts,source_font_audit=fontreport,own_unicode_dictionaries=unicode_fonts,controls=controls,whole_source_pages=62,whole_common_pages=13,whole_application_pages=27,required_files=2,optional_files=6,drivers=6,formal_files=3,partial_declarations=12,shared_low_level_embedded_font_parser=True,author_metric_selection_calibration_event_helpers_imported=False,source_primary_text_exported=False,scientific_execution=False,ratios_evaluated=False)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();require(not x.out.exists(),'fresh output');r=run(x.packet,x.study_root);x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in('new_metrics','controls')}))
