"""Exact additive allocation of the adopted PDF text metrics.

No mathematical-edge validation, primary redistribution, or factor calculation.
"""
import bisect,hashlib,re,unicodedata
METRICS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace',
         'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
FORMS=('NFC','NFKC')
def need(value,message):
    if not value:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def total(text,form):
    t=unicodedata.normalize(form,text);c=' '.join(t.split())
    return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),
      characters_without_whitespace=sum(not x.isspace() for x in t),
      characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()))
def add_weights(items):
    return {f:{m:sum(x[f][m] for x in items) for m in METRICS} for f in FORMS}
def atomic(text,spans,form):
    """Assign whole-document tokens and whitespace runs to their starting owner."""
    chunks=[unicodedata.normalize(form,text[s['start']:s['end']]) for s in spans]
    norm=unicodedata.normalize(form,text)
    need(''.join(chunks)==norm,'normalization crosses an ownership boundary')
    ends=[];at=0
    for chunk in chunks:at+=len(chunk);ends.append(at)
    out=[dict.fromkeys(METRICS,0) for _ in spans]
    def add(pos,key,value=1):out[bisect.bisect_right(ends,pos)][key]+=value
    for x in re.finditer(r'\S+',norm):add(x.start(),'whitespace_tokens')
    for x in re.finditer(r'[^\W_]+',norm):add(x.start(),'alphanumeric_units')
    for i,c in enumerate(norm):
        if not c.isspace():
            add(i,'characters_without_whitespace');add(i,'characters_with_collapsed_whitespace')
            add(i,'utf8_bytes_with_collapsed_whitespace',len(c.encode()))
    for x in re.finditer(r'\s+',norm):
        if x.start()>0 and x.end()<len(norm):
            add(x.start(),'characters_with_collapsed_whitespace');add(x.start(),'utf8_bytes_with_collapsed_whitespace')
    need({m:sum(x[m] for x in out) for m in METRICS}==total(text,form),'atomic conservation')
    return out
def selected_raw_positions(raw,binding):
    # Calibration changes one codepoint to one codepoint. Only furniture is removed.
    positions=[]
    for sp in binding['included_spans']:
        start=sp['start']
        for f in binding['excluded_furniture']:
            if sp['start']<=f['start']<f['end']<=sp['end']:
                positions.extend(range(start,f['start']));positions.append(None);start=f['end']
        positions.extend(range(start,sp['end']));positions.append(None)
    return positions[:-1]
def page_locations(raw,binding,spans):
    positions=selected_raw_positions(raw,binding)
    pages=binding['page_bindings'];starts=[p['start'] for p in pages]
    for s in spans:
        points=[i for i in positions[s['start']:s['end']] if i is not None]
        s['raw_start']=min(points);s['raw_end']=max(points)+1
        s['physical_pages']=sorted({bisect.bisect_right(starts,i) for i in points})
    return positions
def validate_partition(text,spans):
    need(bool(spans),'no ownership spans');at=0
    for s in spans:
        need(s['start']==at and s['start']<s['end']<=len(text),'ownership gap, overlap, or empty span')
        need(sha(text[s['start']:s['end']].encode())==s['sha256'],'owned text hash')
        at=s['end']
    need(at==len(text),'unowned document suffix')
def build_weights(texts,documents,spans,owners):
    owner={n:{f:dict.fromkeys(METRICS,0) for f in FORMS} for n in owners}
    doc={}
    for k,text in texts.items():
        validate_partition(text,spans[k]);ss=spans[k]
        need(all(s['node'] in owner and owners[s['node']]['document']==k for s in ss),'owner/document mismatch')
        for form in FORMS:
            for s,w in zip(ss,atomic(text,ss,form)):
                for metric in METRICS:owner[s['node']][form][metric]+=w[metric]
        doc[k]={f:total(text,f) for f in FORMS}
        need(add_weights([v for n,v in owner.items() if owners[n]['document']==k])==doc[k],'whole-document conservation')
    return owner,doc
def validate_links(graph,owners,links):
    need(set(links)=={n['id'] for n in graph['nodes']},'one cost interface per logical node')
    for n in graph['nodes']:
        row=links[n['id']]
        need(len(row['owners'])==len(set(row['owners'])),'duplicate ownership in a rollup')
        need(set(row['owners'])<=set(owners),'unknown ownership leaf')
        need(row['charged_as_an_additional_item'] is False,'rollup double charge')
        if n['category']=='external':
            need(row['owners']==[] and row['weight'] is None and row['full_dependency_cost'] is None,'unknown external cost treated as zero')
    for n in ('code.census','code.finite','code.data','code.driver'):
        need(links[n]['owners']==['code.appendix'],'required code representation must remain one shared appendix')
