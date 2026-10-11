#!/usr/bin/env python3
"""Symmetric code-block exclusion, exact prior glyph policies; no factors or scientific replay."""
from pathlib import Path
import argparse,copy,hashlib,json,re,unicodedata
import pypdf
R=Path(__file__).resolve().parent
PRECOUNT='6470b44e8f0f633b31341dab60c34e93f13c509e2418116ef8792f1fe953810c'
TOPICS={'Chamber','ChiralEnumeration','Operations'}
NAMES={'L008':['IntersectionProperty','CPlusGroupToCosetGeometry','IsChiralHypertope'],'L028':['ChiralPolytopes','OrderedSubsetsGroups','DiagramPlus'],'N006':['McL_involution_search']}
VARIANTS={'raw_without_listings':'raw_untrimmed','selected_without_listings':'raw_selected','calibrated_selected_without_listings':'calibrated_selected'}
def need(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((R/n).read_text())
def metrics(t,form):
 t=unicodedata.normalize(form,t);c=' '.join(t.split())
 return {'whitespace_tokens':len(c.split()),'alphanumeric_units':len(re.findall(r'[^\W_]+',t)),'characters_without_whitespace':sum(not z.isspace()for z in t),'characters_with_collapsed_whitespace':len(c),'utf8_bytes_with_collapsed_whitespace':len(c.encode()),'collapsed_text_sha256':sha(c.encode())}
def selected(t,s):
 parts=[]
 for span in s['included_spans']:
  at=span['start']
  for f in s['excluded_furniture']:
   if span['start']<=f['start']<f['end']<=span['end']:parts.append(t[at:f['start']]);at=f['end']
  parts.append(t[at:span['end']])
 return '\n'.join(parts)
def fixed_glyphs(raw,s):
 chars=list(raw);seen=set()
 for g in s['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique glyph offset');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}'and len(g['output'])==1,'unchanged one-character glyph rule')
  need(sha(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'unchanged glyph context')
  pg=s['page_bindings'][g['page']-1];need(i==pg['start']+g['page_offset'],'unchanged glyph page')
  chars[i]=g['output']
 return ''.join(chars)
def masked(t,blocks):
 # Deletions represented internally by empty strings. This is applied ONLY after all original-offset selections.
 # The selector below instead uses a same-length sentinel, removed after furniture selection.
 need('\U0010FFFD'not in t,'Reserved sentinel not in measured input')
 chars=list(t)
 for b in blocks:
  for c in b['chunks']:
   for i in range(c['start'],c['end']):
    if not chars[i].isspace():chars[i]='\U0010FFFD'
 return ''.join(chars)
def clean(t):return t.replace('\U0010FFFD','')
def validate_masks(raw,row):
 s=row['accepted_spec'];bs=row['executable_blocks'];need([b['name']for b in bs]==NAMES.get(row['key'],[]),'exact seven named block interfaces')
 intervals=[]
 for b in bs:
  for c in b['chunks']:
   a,z=c['start'],c['end'];pg=s['page_bindings'][c['page']-1]
   need(pg['start']<=a<z<=pg['end']and(a-pg['start'],z-pg['start'])==(c['page_start'],c['page_end']),'within declared physical page')
   need(sha(raw[a:z].encode())==c['sha256'],'exact literal code chunk')
   need(not any(a<f['end']and f['start']<z for f in s['excluded_furniture']),'no page furniture in code mask')
   lines=raw[pg['start']:pg['end']].splitlines(keepends=True);aa=sum(map(len,lines[:c['first_line']-1]));zz=sum(map(len,lines[:c['last_line']]))
   while zz>aa and raw[pg['start']+zz-1]in'\r\n':zz-=1
   need((aa,zz)==(c['page_start'],c['page_end']),'exact complete code lines')
   need(sha(lines[c['first_line']-1].rstrip('\r\n').encode())==c['first_line_sha256']and sha(lines[c['last_line']-1].rstrip('\r\n').encode())==c['last_line_sha256'],'boundary-line hashes')
   intervals.append((a,z))
 intervals.sort();need(all(x[1]<=y[0]for x,y in zip(intervals,intervals[1:])),'no double deletion')
 if row['side']=='replacement':need(not bs,'all eleven replacement masks empty')
 return intervals
def validate_policy(p,spec):
 need(set(p['topics'])==TOPICS and len(spec)==17,'three topics and17 whole PDFs')
 need(sum(x['side']=='source'for x in spec.values())==6 and sum(x['side']=='replacement'for x in spec.values())==11,'six sources eleven replacements')
 need(sum(x['accepted_spec']['pages']for x in spec.values())==p['physical_pages']==215,'all215 pages')
 need(sum(len(x['executable_blocks'])for x in spec.values())==7 and sum(len(b['chunks'])for x in spec.values()for b in x['executable_blocks'])==12,'all7 blocks12 chunks')
 need(p['primary']=={'variant':'calibrated_selected_without_listings','normalization':'NFC','unit':'characters_without_whitespace','reason':'Preserves all three current primary extraction/calibration choices except the symmetric listing mask.'},'fixed primary')
 need(not p['factors_permitted']and p['ratio']is None,'inputs only')
 need(all(x is None for x in p['unknown_costs'].values()),'unknown costs null')
 need(all(p[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no credit')
def bound(b,public,study):
 need(b['root']in('public','study'),'known bound root');base=public if b['root']=='public'else study;p=base/b['path'];data=p.read_bytes();need(len(data)==b['bytes']and sha(data)==b['sha256'],'binding '+str(p));return p

def replay(public,study,controls=True):
 need(pypdf.__version__=='6.13.0','pinned pypdf6.13.0');need(sha((R/'precount_policy_manifest.json').read_bytes())==PRECOUNT,'precount mask policy pin')
 for b in read('precount_policy_manifest.json')['exports']:
  f=R/b['path'];need(f.stat().st_size==b['bytes']and sha(f.read_bytes())==b['sha256'],'precount export '+b['path'])
 if (R/'manifest.json').exists():
  for b in read('manifest.json')['exports']:
   f=R/b['path'];need(f.stat().st_size==b['bytes']and sha(f.read_bytes())==b['sha256'],'author frozen export '+b['path'])
 for b in read('baseline_bindings.json')['bindings']:bound(b,public,study)
 software=read('unchanged_software.json')['records'];need(len(software)==46,'all46 whole software/formal files')
 for row in software:bound(row['file'],public,study)
 p=read('policy.json');spec=read('input_spec.json');old=read('baseline_documents.json');validate_policy(p,spec);new={};cache={};cells=unchanged=0;oldcells=0;newtextonly={};oldtextcells=0
 for ident,row in spec.items():
  pdf=bound(row['file'],public,study);pages=[pg.extract_text()or''for pg in pypdf.PdfReader(pdf).pages];raw='\n'.join(pages);s=row['accepted_spec'];need(len(pages)==s['pages']and sha(raw.encode())==s['extraction_sha256'],'complete raw PDF '+ident)
  at=0
  for n,t in enumerate(pages,1):
   pg=s['page_bindings'][n-1];need((pg['page'],pg['start'],pg['end'],pg['sha256'])==(n,at,at+len(t),sha(t.encode())),'exact full physical page');at+=len(t)+1
  for f in s['excluded_furniture']:need(raw[f['start']:f['end']]==f['literal']and sha(f['literal'].encode())==f['sha256'],'exact old furniture')
  need(len(s['included_spans'])==1 and(s['included_spans'][0]['start'],s['included_spans'][0]['end'])==(0,len(raw)),'whole original selection')
  validate_masks(raw,row);cal=fixed_glyphs(raw,s);before={'raw_untrimmed':raw,'raw_selected':selected(raw,s),'calibrated_selected':selected(cal,s)}
  for v,t in before.items():
   for norm in p['normalizations']:need(metrics(t,norm)==old[ident]['metrics'][v][norm],'reproduce every accepted coordinate '+ident+'/'+v+'/'+norm);oldcells+=5
  rm=masked(raw,row['executable_blocks']);cm=masked(cal,row['executable_blocks']);texts={'raw_without_listings':clean(rm),'selected_without_listings':clean(selected(rm,s)),'calibrated_selected_without_listings':clean(selected(cm,s))}
  mm={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()}
  if not row['executable_blocks']:
   need(all(mm[v]==old[ident]['metrics'][prev]for v,prev in VARIANTS.items()),'exact unchanged document');unchanged+=30
  new[ident]={'pdf':row['file'],'pages':s['pages'],'executable_blocks':len(row['executable_blocks']),'page_chunks':sum(len(x['chunks'])for x in row['executable_blocks']),'metrics':mm,'whole_glyph_map_unchanged':True};cells+=30
  if row['topic']=='Operations':
   chars=list(cal);proxies=[g for g in s['glyph_substitutions']if g.get('kind')=='graphical_proxy']
   for g in proxies:chars[g['offset']]=' '
   beforetext=selected(''.join(chars),s);prior=old[ident]['text_only_sensitivity'];need(len(proxies)==prior['proxy_events_removed'],'unchanged diagram event roster')
   for n in p['normalizations']:need(metrics(beforetext,n)==prior['metrics'][n],'old text-only graphical coordinate');oldtextcells+=5
   aftertext=clean(selected(masked(''.join(chars),row['executable_blocks']),s));m={n:metrics(aftertext,n)for n in p['normalizations']};newtextonly[ident]={'proxy_events_removed':len(proxies),'metrics':m};cells+=10
   if not row['executable_blocks']:need(m==prior['metrics'],'unchanged text-only sensitivity');unchanged+=10
  cache[ident]=(raw,row,texts)
 need(cells==600 and oldcells==510 and oldtextcells==90 and unchanged==500,'complete coordinate totals')
 # Defend retained mathematical matter at the actual changed boundary.
 for ident,markers in {'ChiralEnumeration/L028':['Lemma 4.5.','4.3. Speed comparison'],'Chamber/L008':['5.Magma code','6.Acknowledgements'],'Operations/N006':['From the code above','5.3.Lamplighter Group']}.items():
  raw,row,tt=cache[ident]
  for q in markers:
   need(q in raw and q in tt['raw_without_listings'],'retain surrounding proof/prose '+q)
 rejected=[]
 if controls:
  def reject(name,f):
   try:f()
   except(ValueError,KeyError):rejected.append(name);return
   raise ValueError('accepted negative control '+name)
  def policy_change(k,v):
   q=copy.deepcopy(p);q[k]=v;validate_policy(q,spec)
  reject('permit factors',lambda:policy_change('factors_permitted',True));reject('zero unknown costs',lambda:policy_change('unknown_costs',{'historical_source_software':0}));reject('credit increase',lambda:policy_change('new_source_credit',1))
  raw,row,_=cache['Chamber/L008']
  def mask_change(fn):
   q=copy.deepcopy(row);fn(q);validate_masks(raw,q)
  reject('delete function block',lambda:mask_change(lambda q:q['executable_blocks'].pop()))
  reject('duplicate chunk',lambda:mask_change(lambda q:q['executable_blocks'][0]['chunks'].append(copy.deepcopy(q['executable_blocks'][0]['chunks'][0]))))
  reject('mask page header',lambda:mask_change(lambda q:q['executable_blocks'][0]['chunks'][1].update(start=q['accepted_spec']['page_bindings'][8]['start'])))
  reject('change exact chunk hash',lambda:mask_change(lambda q:q['executable_blocks'][0]['chunks'][0].update(sha256='0'*64)))
  reject('omit literal comment',lambda:mask_change(lambda q:q['executable_blocks'][0]['chunks'][0].update(first_line=29)))
  reject('invent glyph repair',lambda:fixed_glyphs(raw,{**row['accepted_spec'],'glyph_substitutions':[{**row['accepted_spec']['glyph_substitutions'][0],'input_codepoint':'U+0000'}]}))
  r2=copy.deepcopy(cache['Chamber/H1'][1]);r2['executable_blocks']=copy.deepcopy(row['executable_blocks']);reject('mask replacement proof',lambda:validate_masks(cache['Chamber/H1'][0],r2))
 result={'status':'AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW','precount_policy_manifest_sha256':PRECOUNT,'documents':new,'Operations_text_only_sensitivity':newtextonly,'PDF_documents':17,'PDF_pages':215,'unchanged_whole_software_formal_files':46,'PDF_metric_cells':510,'text_only_sensitivity_cells':90,'accepted_prior_cells_reproduced':600,'unchanged_cells':500,'changed_document_keys':['Chamber/L008','ChiralEnumeration/L028','Operations/N006'],'semantic_controls':rejected,'old_glyph_policies_reused':True,'font_parser_or_scientific_reexecuted':False,'primary_text_exported':False,'factors':None,'unknown_costs':p['unknown_costs']}
 if (R/'author_counts.json').exists():
  expected=read('author_counts.json')
  need(result==expected,'fresh complete result equals frozen author counts')
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',required=True,type=Path);ap.add_argument('--sources-root',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);d=replay(a.public_root,a.sources_root);(a.out/'counts.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in d.items()if k not in ['documents','Operations_text_only_sensitivity']}))
if __name__=='__main__':main()
