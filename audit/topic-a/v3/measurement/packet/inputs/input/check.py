#!/usr/bin/env python3
"""Whole unified Affine–A input replay. Lengths only, with no factor operation.

Extraction/selection and the five counters follow the accepted A, Affine and
A/C addition conventions. Exact inherited source mappings are replayed, not
claimed to have undergone a new independent font-outline audit here.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse,hashlib,json,re,unicodedata,io
import pypdf
H=Path(__file__).resolve().parent
IDS=['L032','L034','F016','F013','L035','N009','L128','L012']
OWN=['U']+[f'A{i}'for i in range(1,9)]+['CODE_A','CODE_AFFINE','CODE_DIAGRAM']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
BANNER='arXiv:2610.09711v1  [math.GR]  7 Oct 2026'
def need(ok,m):
 if not ok:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((H/n).read_text())
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def bound(row,roots):
 p=Path(row['path']);need(not p.is_absolute() and '..'not in p.parts,'relative bound path');f=roots[row['root']]/p;b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact bound file '+str(p));return f,b

def metric(t,n):
 t=unicodedata.normalize(n,t);c=' '.join(t.split())
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace()for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))

def validate_policy(p,spec,raw):
 need(p['source_ids']==IDS and list(spec)==IDS+OWN,'eight sources and twelve complete replacement PDFs')
 need(p['source_to_application']==dict(zip(IDS,[f'A{i}'for i in range(1,9)])),'exact eight principal application mappings')
 need(p['common_documents']==['U'] and p['application_documents']==OWN[1:9] and p['complete_program_appendices']==OWN[9:],'whole common/applications/appendices')
 need(p['pdf_documents']==len(spec)==20 and p['physical_pages']==sum(x['pages']for x in spec.values())==217,'whole physical boundary')
 need([p[k]for k in ('source_pages','common_pages','application_pages','program_appendix_pages')]==[119,23,45,30],'full page components')
 need(p['primary']=={'variant':'calibrated_selected','normalization':'NFC','metric':'characters_without_whitespace','rationale':'Preserves the current admitted A and Affine source coordinate; raw-untrimmed and raw-selected sensitivities remain complete.'},'fixed primary before counts')
 need(p['variants']==VARIANTS and p['normalizations']==['NFC','NFKC'] and p['metrics']==UNITS,'all thirty PDF coordinates')
 need(p['ratios']is None and p['symmetric_software_factors']is None,'no factors from an input packet')
 need(all(x is None for x in p['unknown_costs'].values()) and len(p['unknown_costs'])==5,'unknown costs null never zero')
 need(p['new_credit']==dict(source=0,question=0,formal=0) and not p['new_science_execution'] and not p['new_formal_compile'],'no new credit or replay claim')
 roles=Counter(x['role']for x in raw);need(roles==dict(required_program_or_data=11,inherited_auxiliary=3,current_operational_driver=2,partial_formal_evidence=14),'full raw role census')
 need(len(raw)==p['raw_files']==30 and len({x['file']['path']for x in raw})==30,'whole unique raw files')
 need(p['programs_are_alternate_representations']is True,'no code double charge')
 need([p[k]for k in ('required_complete_files','auxiliary_scripts','current_operational_drivers','partial_formal_modules')]==[11,3,2,14],'full raw scope')


def extract(pdf,key):
 texts=[];fonts=[];pages=[];at=0;duplicates=0
 for i,page in enumerate(pypdf.PdfReader(pdf).pages,1):
  chunks=[];local=[]
  def visitor(t,cm,tm,f,size):
   nonlocal duplicates
   if key=='L128' and i==1 and f is None and t==BANNER and chunks and chunks[-1]==t:
    duplicates+=1;return
   chunks.append(t);local.extend([str(f.get('/BaseFont',f.get('/Name','')))if f else '']*len(t))
  t=page.extract_text(visitor_text=visitor)or'';need(t==''.join(chunks) and len(t)==len(local),'literal font visitor alignment '+key)
  texts.append(t);fonts.extend(local);fonts.append('');pages.append(dict(page=i,start=at,end=at+len(t),sha256=sha(t.encode()),empty_extraction=not t));at+=len(t)+1
 need(duplicates==int(key=='L128'),'only exact inherited arXiv Form duplicate')
 return '\n'.join(texts),fonts[:-1],pages

def validate_text(key,raw,fonts,pages,row):
 b=row['boundary'];need(pages==b['page_bindings'] and len(pages)==row['pages']==b['pages'],'all exact page texts '+key)
 need(sha(raw.encode())==b['extraction_sha256'],'literal extraction '+key)
 spans=b['included_spans'];need(len(spans)==1 and spans[0]['start']==0 and spans[0]['end']==len(raw) and spans[0]['sha256']==sha(raw.encode()),'complete document '+key)
 last=0
 for f in b['excluded_furniture']:
  a,z=f['start'],f['end'];need(last<=a<z<=len(raw) and raw[a:z]==f['literal'] and sha(raw[a:z].encode())==f['sha256'],'exact furniture '+key);last=z
  pg=pages[f['page']-1];need(pg['start']<=a<z<=pg['end'],'within physical page')
  if key in OWN:need(z==pg['end'] and f['literal']=='\n'+str(f['page']),'only trailing own page number')
 if key in OWN:need(len(b['excluded_furniture'])==len(pages) and b['glyph_substitutions']==[],'no own glyph rewrite')
 edits=[];covered=set()
 for g in b['glyph_substitutions']:
  a=g.get('start',g.get('offset'));z=g.get('end',a+1);literal=g.get('input',chr(int(g['input_codepoint'][2:],16)) if 'input_codepoint'in g else None)
  need(0<=a<z<=len(raw) and not covered.intersection(range(a,z)),'disjoint source glyph');covered.update(range(a,z))
  need(raw[a:z]==literal and all(fonts[j]==g['input_font'] for j in range(a,z)),'actual source font/literal occurrence '+key)
  need(len(g['output'])==1,'one visible glyph per accepted repair')
  pg=pages[g['page']-1];x,y=g['context_start'],g['context_end'];need(pg['start']<=x<=a<z<=y<=pg['end'] and a==pg['start']+g['page_offset'] and sha(raw[x:y].encode())==g['context_sha256'],'source glyph bound context')
  need(not any(max(a,f['start'])<min(z,f['end'])for f in b['excluded_furniture']),'calibration not lost as furniture');edits.append((a,z,g['output']))
 for i,c in enumerate(raw):
  bad=(ord(c)<32 and c not in '\n\r\t')or unicodedata.category(c)=='Co'or c=='\ufffd'
  need(not bad or i in covered,'unclassified extracted glyph '+key+' '+hex(ord(c)))
 return edits

def transform(raw,b,edits=(),style='single_character'):
 if style=='single_character':
  chars=list(raw)
  for a,z,out in edits:need(z==a+1,'one-character source calibration');chars[a]=out
  t=''.join(chars);parts=[];at=0
  for f in b['excluded_furniture']:parts.append(t[at:f['start']]);at=f['end']
  parts.append(t[at:]);return '\n'.join(parts)
 # Accepted L128 selected policy uses one replacement newline per exact cut.
 all_edits=sorted([(f['start'],f['end'],'\n')for f in b['excluded_furniture']]+list(edits));parts=[];at=0
 for a,z,value in all_edits:need(at<=a<z,'disjoint selection/calibration edits');parts.extend([raw[at:a],value]);at=z
 parts.append(raw[at:]);return ''.join(parts)

def font_audit(pdf):
 fonts={};bad=[]
 for i,page in enumerate(pypdf.PdfReader(pdf).pages,1):
  t=page.extract_text()or''
  for j,c in enumerate(t):
   if(ord(c)<32 and c not in '\n\r\t')or unicodedata.category(c)=='Co'or c=='\ufffd':bad.append([i,j,hex(ord(c))])
  for ref in page['/Resources'].get('/Font',{}).values():
   d=ref.get_object();buf=io.BytesIO();d.write_to_stream(buf);ident=f'{ref.idnum}:{ref.generation}'if hasattr(ref,'idnum')else sha(buf.getvalue());to=d.get('/ToUnicode');desc=d.get('/DescendantFonts');dd=desc[0].get_object().get('/FontDescriptor')if desc else d.get('/FontDescriptor');dd=dd.get_object()if dd else {};embedded={}
   for typ in('/FontFile','/FontFile2','/FontFile3'):
    if typ in dd:embedded[typ]=sha(dd[typ].get_object().get_data())
   row=dict(dictionary_id=ident,dictionary_sha256=sha(buf.getvalue()),base_font=str(d.get('/BaseFont','')),subtype=str(d.get('/Subtype','')),encoding=str(d.get('/Encoding','')),to_unicode_sha256=sha(to.get_object().get_data())if to else None,embedded_streams=embedded,pages=[])
   need(to is not None and embedded,'own embedded Unicode font')
   if ident not in fonts:fonts[ident]=row
   need(all(fonts[ident][k]==row[k]for k in row if k!='pages'),'actual dictionary identity');fonts[ident]['pages'].append(i)
 for row in fonts.values():row['pages']=sorted(set(row['pages']))
 return list(fonts.values()),bad

def code_inclusion(rawrows,roots,spec,cache):
 result=[]
 for row in rawrows:
  if row['role']!='required_program_or_data':continue
  path,data=bound(row['file'],roots);key=row['printed_in'];texfile,_=bound(spec[key]['tex'],roots);tex=texfile.read_text();short=str(path.relative_to(texfile.parent))
  if short.startswith('required-code/'):
   blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',tex,re.S);need(sum(x==data.decode()for x in blocks)==1,'whole literal inline bytes '+short)
  else:
   ds=[x for x in re.findall(r'\\VerbatimInput(?:\[([^]]*)\])?\{([^}]+)\}',tex)if x[1]==short];need(len(ds)==1 and not re.search('firstline|lastline|firstnumber',ds[0][0]),'whole external input '+short)
  program=''.join(c for c in data.decode()if not c.isspace());printed=''.join(c for c in cache[key]['raw_selected']if not c.isspace()and c not in '↪⌋')
  need(program in printed,'complete printed file '+short)
  result.append(dict(file=row['file'],printed_in=key,whole_bytes_in_tex=True,whole_nonspace_characters_in_pdf=True,inclusion_only_normalization='Whitespace and exact wrapping marks ↪/⌋ ignored only for inclusion; measured text is never changed.'))
 need(len(result)==11,'all whole mathematical files');return result

def controls(policy,spec,rawrows,cache):
 passed=[]
 cases=[('omit source',lambda p,s,r:p['source_ids'].pop()),('omit application',lambda p,s,r:p['application_documents'].pop()),('omit whole common',lambda p,s,r:p.update(common_documents=[])),('omit data',lambda p,s,r:r.pop(1)),('driver made free',lambda p,s,r:r.pop(3)),('program role changed',lambda p,s,r:r[0].update(role='optional_validation')),('software factor claimed',lambda p,s,r:p.update(symmetric_software_factors=1.0)),('input factor claimed',lambda p,s,r:p.update(ratios={})),('unknown made zero',lambda p,s,r:p['unknown_costs'].update(full_graphical_structure=0)),('new source credit',lambda p,s,r:p['new_credit'].update(source=1)),('drop bibliography page',lambda p,s,r:s['A6'].update(pages=10)),('raw and printed additive',lambda p,s,r:p.update(programs_are_alternate_representations=False))]
 for name,change in cases:
  p,s,r=deepcopy(policy),deepcopy(spec),deepcopy(rawrows);change(p,s,r)
  try:validate_policy(p,s,r)
  except(ValueError,KeyError):passed.append(name)
  else:raise ValueError('control accepted '+name)
 for name,key,change in [('glyph erased','L032',lambda b:b['glyph_substitutions'][0].update(output='')),('wrong glyph font','L032',lambda b:b['glyph_substitutions'][0].update(input_font='/wrong')),('glyph shifted','L032',lambda b:b['glyph_substitutions'][0].update(offset=b['glyph_substitutions'][0]['offset']+1)),('own proof deleted as footer','U',lambda b:b['excluded_furniture'][0].update(start=0)),('new own rewrite','U',lambda b:b['glyph_substitutions'].append({}))]:
  r=deepcopy(spec[key]);change(r['boundary']);v=cache[key]
  try:validate_text(key,v['raw_untrimmed'],v['fonts'],v['pages'],r)
  except(ValueError,KeyError):passed.append(name)
  else:raise ValueError('control accepted '+name)
 need(metric('A\u030A ﬀ\t9','NFC')['characters_without_whitespace']==3 and metric('A\u030A ﬀ\t9','NFKC')['characters_without_whitespace']==4,'Unicode normalization fixture')
 return passed

def replay(a):
 roots=dict(study=a.study_root,public=a.public_root);p=load('policy.json');spec=load('input_spec.json');rawrows=load('raw_inventory.json');validate_policy(p,spec,rawrows)
 need(pypdf.__version__==p['pypdf_version']=='6.13.0','pinned pypdf')
 for row in load('precount_boundary_manifest.json')['exports']:
  b=(H/row['path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'precount policy remains fixed '+row['path'])
 if(H/'manifest.json').exists():
  for row in load('manifest.json')['exports']:
   b=(H/row['path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'frozen export '+row['path'])
 bindings=load('bindings.json')
 for row in bindings['references']+bindings['scientific_and_review_exports']:bound(row,roots)
 evidence=load('inherited_evidence.json')
 for row in evidence['public_records']:bound(row['binding'],roots)
 for row in evidence['own_visual_records']:bound(row,roots)
 for row in load('helper_provenance.json')['base_methods']:bound(row,roots)
 listing=load('written_listing_boundary.json');need(set(listing['documents'])==set(OWN[:9]) and len(listing['unique_files'])==38,'complete scientific TeX listing screen')
 for row in listing['unique_files']:
  _,b=bound(dict(root='study',**row),roots);need(not re.search(r'\\(?:VerbatimInput|begin\{(?:CompleteProgram|verbatim|Verbatim|lstlisting|minted)\})',b.decode()),'no unmatched executable listing in scientific TeX')
 docs={};cache={};baseline=load('baseline_documents.json');audits=load('own_font_audit.json');agreements=0
 for key,row in spec.items():
  pdf,_=bound(row['file'],roots);raw,fonts,pages=extract(pdf,key);edits=validate_text(key,raw,fonts,pages,row)
  texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,row['boundary'],style=row['calibration_style']),calibrated_selected=transform(raw,row['boundary'],edits,row['calibration_style']))
  m={v:{n:metric(t,n)for n in p['normalizations']}for v,t in texts.items()};docs[key]=dict(pdf_sha256=row['file']['sha256'],pages=row['pages'],glyph_substitutions=len(edits),metrics=m)
  cache[key]=texts|dict(fonts=fonts,pages=pages)
  if key in IDS:
   need(m==baseline[key]['metrics'],'all accepted source coordinates and text hashes unchanged '+key);agreements+=30
   # The full inherited spec itself is bound independently, not merely its numeric output.
   old=json.loads((a.public_root/row['legacy_spec']).read_text());old=old.get('sources',old)[key];need(row['boundary']==old,'exact inherited source selection/calibration '+key)
  else:
   fa,bad=font_audit(pdf);need(fa==audits[key]['dictionaries']and bad==audits[key]['unclassified_controls_private_use_replacement_characters']==[],'whole own font dictionary audit '+key)
  if key in OWN:bound(row['tex'],roots)
 rawcounts={}
 for row in rawrows:
  _,b=bound(row['file'],roots);rawcounts[row['id']]=dict(file=row['file'],role=row['role'],metrics={n:metric(b.decode(),n)for n in p['normalizations']})
 inclusion=code_inclusion(rawrows,roots,spec,cache);negative=controls(p,spec,rawrows,cache)
 report=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_documents=20,pdf_pages=217,pdf_metric_cells=600,raw_files=30,raw_metric_cells=300,unchanged_source_metric_cells=agreements,unchanged_source_collapsed_text_hashes=48,documents=docs,raw_files_measured=rawcounts,complete_program_inclusion=inclusion,controls_rejected=negative,unicode_fixture_passed=True,own_font_dictionaries=sum(len(x['dictionaries'])for x in audits.values()),retained_source_font_calibration_reused=True,new_primary_outline_audit_claimed=False,primary_text_exported=False,scientific_programs_executed=False,formal_compilation_performed=False,unknown_costs=p['unknown_costs'],ratios=None,new_credit=p['new_credit'])
 if(H/'author_counts.json').exists():need(report==load('author_counts.json'),'frozen author input replay')
 return report

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);r=replay(a);put(a.out/'counts.json',r);print('PASS600 PDF/300 raw cells;240 unchanged source cells;11 whole files;'+str(len(r['controls_rejected']))+' controls; no factors')
if __name__=='__main__':main()
