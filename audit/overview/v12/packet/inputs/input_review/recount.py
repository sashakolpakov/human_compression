#!/usr/bin/env python3
"""Independent character-filter recount; imports no author measurement code."""
import argparse, copy, hashlib, json, unicodedata
from pathlib import Path
from pypdf import PdfReader

AUTHOR = 'b504e95a2b541f92e57644f93149eabc10a6072b75ffa2193e3467a6af40c462'
PRECOUNT = '6470b44e8f0f633b31341dab60c34e93f13c509e2418116ef8792f1fe953810c'
# Independently transcribed after reading the eight full source pages.
LINES = {
 'Chamber/L008': [(8,25,48),(9,2,7),(9,8,17),(9,18,47),(10,2,8)],
 'ChiralEnumeration/L028': [(9,61,64),(10,2,49),(11,2,3),(11,11,50),(12,2,10),(12,13,21)],
 'Operations/N006': [(20,14,27)]}
NAMES = {'Chamber/L008':['IntersectionProperty','CPlusGroupToCosetGeometry','IsChiralHypertope'],
 'ChiralEnumeration/L028':['ChiralPolytopes','OrderedSubsetsGroups','DiagramPlus'],
 'Operations/N006':['McL_involution_search']}
VARIANTS = [('raw_without_listings','raw_untrimmed'),('selected_without_listings','raw_selected'),('calibrated_selected_without_listings','calibrated_selected')]

def require(ok, msg):
 if not ok: raise ValueError(msg)
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def metric(s,n):
 s=unicodedata.normalize(n,s); collapsed=' '.join(s.split()); runs=0; prior=False
 for c in s:
  yes=c.isalnum()
  if yes and not prior: runs+=1
  prior=yes
 return {'whitespace_tokens':len(collapsed.split()),'alphanumeric_units':runs,
  'characters_without_whitespace':len([c for c in s if not c.isspace()]),
  'characters_with_collapsed_whitespace':len(collapsed),
  'utf8_bytes_with_collapsed_whitespace':len(collapsed.encode('utf-8')),
  'collapsed_text_sha256':digest(collapsed.encode('utf-8'))}
def filecheck(row,roots):
 p=roots[row['root']]/row['path']; b=p.read_bytes()
 require(len(b)==row['bytes'] and digest(b)==row['sha256'],'file '+str(p)); return p
def frozen(path,pin=None):
 if pin: require(digest((path/'manifest.json').read_bytes())==pin,'manifest pin')
 for row in load(path/'manifest.json')['exports']:
  b=(path/row['path']).read_bytes(); require(len(b)==row['bytes'] and digest(b)==row['sha256'],'export '+row['path'])
def masks(key,row,pages):
 require([b['name'] for b in row['executable_blocks']]==NAMES.get(key,[]),'named mask roster')
 chunks=[c for b in row['executable_blocks'] for c in b['chunks']]
 require([(c['page'],c['first_line'],c['last_line']) for c in chunks]==LINES.get(key,[]),'independently read line boundaries')
 offsets=[]; at=0
 for page in pages: offsets.append(at); at+=len(page)+1
 intervals=[]
 for c in chunks:
  page=pages[c['page']-1]; lines=page.splitlines(keepends=True)
  a=sum(len(x) for x in lines[:c['first_line']-1]); b=sum(len(x) for x in lines[:c['last_line']])
  while page[b-1:b] in ('\n','\r'): b-=1
  start=offsets[c['page']-1]+a; end=offsets[c['page']-1]+b
  require((c['start'],c['end'],c['page_start'],c['page_end'])==(start,end,a,b),'mask coordinate')
  require(digest(page[a:b].encode())==c['sha256'],'mask literal')
  require(not any(start<f['end'] and f['start']<end for f in row['accepted_spec']['excluded_furniture']),'mask avoids furniture')
  intervals.append((start,end))
 require(all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:])),'mask disjointness')
 return intervals
def filters(raw,s,intervals,calibrated=False,text_only=False,selected=False):
 # Character membership, without deletion sentinels or author selector routines.
 replacement={g['offset']:g['output'] for g in s['glyph_substitutions']} if calibrated else {}
 if text_only:
  replacement.update({g['offset']:' ' for g in s['glyph_substitutions'] if g.get('kind')=='graphical_proxy'})
 spans=s['included_spans'] if selected else [{'start':0,'end':len(raw)}]
 out=[]
 for span in spans:
  fragments=[]; previous=False
  for i in range(span['start'],span['end']):
   furniture=selected and any(f['start']<=i<f['end'] for f in s['excluded_furniture'])
   if furniture:
    if not previous: fragments.append('\n')
    previous=True; continue
   previous=False
   c=replacement.get(i,raw[i])
   if not c.isspace() and any(a<=i<b for a,b in intervals): continue
   fragments.append(c)
  out.append(''.join(fragments))
 return '\n'.join(out)
def old_spec(key,public):
 topic,k=key.split('/')
 if topic=='Operations': return load(public/'audit/topic-operations/v1/measurement/inputs/input_spec.json')[k]
 folder='audit/topic-chamber/v2/measurement/inputs' if topic=='Chamber' else 'audit/additional-measurements/v1/inputs/additional_sources_measurement_inputs_v1'
 for name,field in [('source_input_spec.json','sources'),('replacement_input_spec.json','ours')]:
  d=load(public/folder/name)[field]
  if k in d:return d[k]
 raise ValueError('old spec key')
def old_metrics(key,public):
 topic,k=key.split('/')
 routes={'Chamber':'audit/topic-chamber/v2/measurement/inputs/input_counts.json',
 'ChiralEnumeration':'audit/additional-measurements/v1/inputs/additional_sources_measurement_inputs_v1/author_counts.json',
 'Operations':'audit/topic-operations/v1/measurement/inputs/author_counts.json'}
 d=load(public/routes[topic]); row=d['documents'][k]
 return row.get('metrics',row.get('variants')), d.get('text_only_sensitivity',{}).get(k)
def controls(spec,pages,raw):
 rejected=[]
 def reject(name,f):
  try:f()
  except (ValueError,KeyError):rejected.append(name); return
  raise ValueError('mutation accepted: '+name)
 def mutate(key,fn):
  d=copy.deepcopy(spec[key]); fn(d); masks(key,d,pages[key])
 k='Chamber/L008'
 reject('omit function',lambda:mutate(k,lambda d:d['executable_blocks'].pop()))
 reject('omit literal comment',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'][0].update(first_line=29)))
 reject('add proof to mask',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'][0].update(first_line=24)))
 reject('mask running header',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'][1].update(first_line=1)))
 reject('mask L028 lemma',lambda:mutate('ChiralEnumeration/L028',lambda d:d['executable_blocks'][0]['chunks'][0].update(first_line=20)))
 reject('mask McL conclusion',lambda:mutate('Operations/N006',lambda d:d['executable_blocks'][0]['chunks'][0].update(last_line=35)))
 reject('duplicate chunk',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'].append(copy.deepcopy(d['executable_blocks'][0]['chunks'][0]))))
 reject('change literal hash',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'][0].update(sha256='0'*64)))
 reject('change absolute offset',lambda:mutate(k,lambda d:d['executable_blocks'][0]['chunks'][0].update(start=0)))
 reject('invent replacement mask',lambda:mutate('Chamber/H1',lambda d:d.update(executable_blocks=copy.deepcopy(spec[k]['executable_blocks']))))
 # Actual raw NULs must remain unless an accepted event calibration or exact mask touches them.
 require(any('\x00' in x for x in raw.values()),'real NUL fixture present')
 for name,form in [('NFC','NFC'),('NFKC','NFKC')]:
  require(metric('a_b  \x00 c\n',form)['alphanumeric_units']==3,'independent metric fixture')
  require(metric('a_b  \x00 c\n',form)['characters_without_whitespace']==5,'NUL not globally omitted')
 rejected.extend(['global NUL deletion detected by independent fixture','underscore counted as alphanumeric detected by fixture'])
 return rejected
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 require(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 frozen(a.author,AUTHOR);require(digest((a.author/'precount_policy_manifest.json').read_bytes())==PRECOUNT,'precount pin')
 for r in load(a.author/'precount_policy_manifest.json')['exports']:
  b=(a.author/r['path']).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'precount exact binding')
 roots={'public':a.public_root,'study':a.sources_root}
 for b in load(a.author/'baseline_bindings.json')['bindings']:filecheck(b,roots)
 software=load(a.author/'unchanged_software.json');require(len(software['records'])==46,'whole software roster')
 for r in software['records']:filecheck(r['file'],roots)
 spec=load(a.author/'input_spec.json');baseline=load(a.author/'baseline_documents.json');expected=load(a.author/'author_counts.json')
 require(len(spec)==17 and sum(x['accepted_spec']['pages'] for x in spec.values())==215,'complete 17 PDF boundary')
 result={};textonly={};pages_by_key={};raw_by_key={};cells=unchanged=hashes=0
 for key,row in spec.items():
  s=row['accepted_spec'];require(s==old_spec(key,a.public_root),'unchanged original full spec '+key)
  prior_metrics,prior_textonly=old_metrics(key,a.public_root)
  require(baseline[key]['metrics']==prior_metrics,'baseline metrics copied exactly from prior frozen packet')
  if prior_textonly is not None:require(baseline[key]['text_only_sensitivity']==prior_textonly,'prior text-only sensitivity copied exactly')
  p=filecheck(row['file'],roots); pages=[x.extract_text() or '' for x in PdfReader(p).pages];raw='\n'.join(pages);pages_by_key[key]=pages;raw_by_key[key]=raw
  require(len(pages)==s['pages'] and digest(raw.encode())==s['extraction_sha256'],'full extraction '+key)
  at=0
  for n,txt in enumerate(pages,1):
   pb=s['page_bindings'][n-1];require((pb['page'],pb['start'],pb['end'],pb['sha256'])==(n,at,at+len(txt),digest(txt.encode())),'page binding');at+=len(txt)+1
  require(len(s['included_spans'])==1 and (s['included_spans'][0]['start'],s['included_spans'][0]['end'])==(0,len(raw)),'whole document selected')
  for f in s['excluded_furniture']:require(raw[f['start']:f['end']]==f['literal'],'furniture literal')
  for g in s['glyph_substitutions']:
   require(g['input_codepoint']==f'U+{ord(raw[g["offset"]]):04X}' and len(g['output'])==1,'unchanged glyph input')
   require(digest(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'glyph context')
  intervals=masks(key,row,pages);d={}
  for index,(new,old) in enumerate(VARIANTS):
   kwargs={'calibrated':index==2,'selected':index>0}; before=filters(raw,s,[],**kwargs);after=filters(raw,s,intervals,**kwargs)
   d[new]={}
   for norm in ('NFC','NFKC'):
    mb=metric(before,norm);ma=metric(after,norm)
    require(mb==baseline[key]['metrics'][old][norm],'old metric/hash '+key)
    require(ma==expected['documents'][key]['metrics'][new][norm],'new metric/hash '+key)
    d[new][norm]=ma;cells+=5;hashes+=1
    if not intervals:require(ma==mb,'unchanged document');unchanged+=5
  result[key]=d
  if row['topic']=='Operations':
   before=filters(raw,s,[],True,True,True);after=filters(raw,s,intervals,True,True,True);d={}
   for norm in ('NFC','NFKC'):
    mb=metric(before,norm);ma=metric(after,norm);require(mb==baseline[key]['text_only_sensitivity']['metrics'][norm],'old text-only')
    require(ma==expected['Operations_text_only_sensitivity'][key]['metrics'][norm],'new text-only');d[norm]=ma;cells+=5;hashes+=1
    if not intervals:require(ma==mb,'unchanged text-only');unchanged+=5
   textonly[key]=d
 require(cells==600 and unchanged==500 and hashes==120,'complete count totals')
 negative=controls(spec,pages_by_key,raw_by_key)
 out={'status':'PASS','author_manifest_sha256':AUTHOR,'precount_manifest_sha256':PRECOUNT,'PDF_documents':17,'PDF_pages':215,'independent_metric_cells':cells,'independent_text_hashes':hashes,'unchanged_cells':unchanged,'whole_software_files':46,'source_masks':7,'page_chunks':12,'documents':result,'Operations_text_only':textonly,'controls':negative,'no_author_code_imports':True,'reused_exact_font_audits':True,'scientific_replays':False,'ratios':None}
 write(a.out/'recount.json',out); print(json.dumps({k:v for k,v in out.items() if k not in ('documents','Operations_text_only')}))
if __name__=='__main__':main()
