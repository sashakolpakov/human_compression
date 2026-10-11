"""Thirty-coordinate exclusive ownership using the accepted A/B atomic allocator."""
import bisect,collections,hashlib
from atomic_base import need,sha,atomic,total,METRICS,FORMS
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
def zero():return {v:{f:dict.fromkeys(METRICS,0) for f in FORMS} for v in VARIANTS}
def add(items):
 items=list(items)
 return {v:{f:{m:sum(x[v][f][m] for x in items) for m in METRICS} for f in FORMS} for v in VARIANTS}
def selected_positions(raw,row):
 parts=[]
 for r in row['included_spans']:
  start=r['start']
  for f in row['excluded_furniture']:
   if r['start']<=f['start']<f['end']<=r['end']:
    parts.append(list(range(start,f['start'])));start=f['end']
  parts.append(list(range(start,r['end'])))
 result=[]
 for i,part in enumerate(parts):
  if i:result.append(None)
  result.extend(part)
 return result

def rle(ownership,text,positions,page_bindings,owners):
 need(len(ownership)==len(text)==len(positions),'position/ownership alignment')
 starts=[x['start'] for x in page_bindings];out=[]
 for at,name in enumerate(ownership):
  if not out or out[-1]['owner']!=name:out.append({'start':at,'end':at+1,'owner':name})
  else:out[-1]['end']=at+1
 for row in out:
  a,b=row['start'],row['end'];raw=[x for x in positions[a:b] if x is not None]
  row.update(sha256=sha(text[a:b].encode()),category=owners[row['owner']]['category'],physical_pages=sorted({bisect.bisect_right(starts,x) for x in raw}),raw_start=min(raw) if raw else None,raw_end=max(raw)+1 if raw else None)
 return out

def partition_document(key,row,extraction,boundaries,owners):
 raw,before,after=extraction[:3];positions=selected_positions(raw,row)
 need(len(before)==len(after)==len(positions),'one-codepoint calibrated selection')
 lines=after.splitlines(keepends=True);offsets=[0]
 for line in lines:offsets.append(offsets[-1]+len(line))
 cuts=[]
 for location,name,category in boundaries:
  line,needle=(location,None) if isinstance(location,int) else location
  at=offsets[line-1]
  if needle is not None:
   need(lines[line-1].count(needle)==1,'unique intra-line semantic boundary')
   at+=lines[line-1].index(needle)
  need(not cuts or at>cuts[-1][0],'ordered semantic boundaries '+key)
  cuts.append((at,name,category))
  info={'id':name,'document':key,'category':category}
  need(name not in owners or owners[name]==info,'consistent noncontiguous owner')
  owners[name]=info
 need(cuts[0][0]==0,'front matter starts at zero')
 own=[None]*len(after)
 for i,(at,name,cat) in enumerate(cuts):
  end=cuts[i+1][0] if i+1<len(cuts) else len(after)
  own[at:end]=[name]*(end-at)
 rawown=[None]*len(raw)
 for at,pos in enumerate(positions):
  if pos is not None:rawown[pos]=own[at]
 if row['excluded_furniture']:
  name=key+'.furniture';owners[name]={'id':name,'document':key,'category':'excluded_furniture'}
  for f in row['excluded_furniture']:rawown[f['start']:f['end']]=[name]*(f['end']-f['start'])
 need(all(rawown),'every raw source character has one owner')
 variants={v:{'length':len(t),'sha256':sha(t.encode()),'spans':rle(os,t,ps,row['page_bindings'],owners)} for v,t,os,ps in [('raw_untrimmed',raw,rawown,list(range(len(raw)))),('raw_selected',before,own,positions),('calibrated_selected',after,own,positions)]}
 return {'pdf_sha256':row['pdf_sha256'],'pages':row['pages'],'variants':variants}

def allocations(partition,texts):
 owners=partition['owners'];costs={n:zero() for n in owners};docs={}
 for key,record in partition['documents'].items():
  docs[key]=zero()
  for variant in VARIANTS:
   text=texts[key][variant];rec=record['variants'][variant];ss=rec['spans'];at=0
   need(rec['length']==len(text) and rec['sha256']==sha(text.encode()),'exact document text')
   for s in ss:
    need(s['start']==at and at<s['end']<=len(text),'exclusive continuous ownership')
    need(s['owner'] in owners and owners[s['owner']]['document']==key,'owner document')
    need(s['category']==owners[s['owner']]['category'],'owner category')
    need(s['sha256']==sha(text[s['start']:s['end']].encode()),'exact owned passage')
    at=s['end']
   need(at==len(text),'complete suffix ownership')
   for form in FORMS:
    aw=atomic(text,ss,form)
    for s,w in zip(ss,aw):
     for m in METRICS:costs[s['owner']][variant][form][m]+=w[m]
    docs[key][variant][form]=total(text,form)
  need(add(costs[n] for n in owners if owners[n]['document']==key)==docs[key],'complete document conservation')
 return costs,docs

def interfaces(graph,owners,costs,supplements):
 nodes={n['id']:n for n in graph['nodes']};children=collections.defaultdict(list)
 for n in nodes.values():
  if n.get('parent'):children[n['parent']].append(n['id'])
 links={}
 def link(name):
  if name in links:return links[name]
  n=nodes[name];unknown=n['side'] in ['external','verification']
  paid=set(supplements.get(name,[]))
  if not unknown:
   paid.update(o for o in owners if (o==name or o.startswith(name+'.')) and not any((o==other or o.startswith(other+'.')) and len(other)>len(name) for other in nodes))
   if n.get('parent') and n['parent']+'.statement' in owners:paid.add(n['parent']+'.statement')
   for child in children[name]:paid.update(link(child)['owners'])
  need(paid<=owners.keys(),'existing interface owners '+name)
  need(not unknown or not paid,'no cost invented for unknown input')
  need(unknown or paid,'unmapped mathematical node '+name)
  allowed={'CODE'} if name.startswith('program.') else {{'A_Affine':'AF1'}.get(n['document'],n['document'])}
  need(all(owners[x]['document'] in allowed for x in paid),'same-document ownership, except explicit CODE representation')
  links[name]={'owners':sorted(paid),'known_weight':None if unknown else add(costs[x] for x in sorted(paid)),
   'unknown_reason':('retained proof cost unknown' if n['side']=='external' else 'operational driver measured separately in raw form' if name.startswith('driver.') else 'diagnostic measured separately in raw form' if name.startswith('diagnostic.') else 'separate formal evidence, not a scientific PDF cost' if unknown else None),
   'charged_again':False,'expanded_dependency_cost':None}
  return links[name]
 for name in nodes:link(name)
 return links

def route(names,links,costs,owners,raw_programs):
 paid=sorted({x for n in names for x in links[n]['owners']});needed=[n for n in names if n in raw_programs]
 subtotal=add(costs[x] for x in paid)
 rawalt={v:{f:{m:sum(costs[x][v][f][m] for x in paid if owners[x]['document']!='CODE')+sum(raw_programs[n]['metrics'][f][m] for n in needed) for m in METRICS} for f in FORMS} for v in VARIANTS}
 return {'logical_nodes':sorted(names),'owners':paid,'known_extracted_subtotal':subtotal,
  'by_document':{d:add(costs[x] for x in paid if owners[x]['document']==d) for d in sorted({owners[x]['document'] for x in paid})},
  'raw_program_alternative_subtotal':rawalt,'unknown_inputs':sorted(n for n in names if links[n]['known_weight'] is None),
  'expanded_dependency_cost':None,'graphics_cost':None,
  'scope':'Selected prerequisite union; not a minimum proof or complete-paper denominator. Full paper context remains charged in every overall and application comparison.'}
