#!/usr/bin/env python3
"""Independent whole-document recount. No author module is imported.

Glyph choices are the visually reviewed, actual-font-bound declarations;
the author's separately replayed event walker checks their byte origins.
This checker independently extracts all page text and font labels, verifies
the complete boundaries, and recounts every declared cost coordinate.
"""
import argparse, copy, hashlib, json, pathlib, re, unicodedata
import pypdf

PIN='19e4dcc025a87b1b805c9e3674cbcc91bb53a639e145739528b5bd468156d604'
BANNER='arXiv:2608.23223v1  [math.CO]  24 Aug 2026'
def need(t,s):
    if not t: raise ValueError('INPUT_RECOUNT_REJECT '+s)
def sha(b): return hashlib.sha256(b).hexdigest()
def counts(s,norm):
    s=unicodedata.normalize(norm,s)
    words=s.split();flat=' '.join(words)
    runs=0;previous=False
    for c in s:
        current=c.isalnum()
        if current and not previous:runs+=1
        previous=current
    return {'whitespace_tokens':len(words),'alphanumeric_units':runs,
            'characters_without_whitespace':len(''.join(words)),
            'characters_with_collapsed_whitespace':len(flat),
            'utf8_bytes_with_collapsed_whitespace':sum(len(c.encode('utf-8')) for c in flat),
            'collapsed_text_sha256':sha(flat.encode())}

def document(path,key,spec,aliases):
    need(sha(path.read_bytes())==spec['sha256'],'PDF identity')
    text=[];fonts=[];bindings=[];offset=0;cuts=[]
    for number,page in enumerate(pypdf.PdfReader(path).pages,1):
        pieces=[];names=[]
        def visit(t,cm,tm,font,size):
            if key=='N007' and number==1 and font is None and t==BANNER and pieces and pieces[-1]==BANNER:return
            pieces.append(t);names.extend([str(font.get('/BaseFont',font.get('/Name',''))) if font else '']*len(t))
        raw=page.extract_text(visitor_text=visit) or ''
        need(raw==''.join(pieces) and raw,'whole nonempty page')
        bindings.append({'page':number,'start':offset,'end':offset+len(raw),
                         'sha256':sha(raw.encode()),'empty_extraction':False})
        start=end=None
        if key=='N007':
            if number==1:
                need(raw.count(BANNER)==1,'one original version stamp')
                start=raw.rfind('\n1\n'+BANNER)+1
                need(start>0,'page-one isolated folio before stamp');end=start+1
            else:
                header=(f'{number} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n'
                        if number%2==0 else f'THEj-DIAGONALS TWISTING {number}\n')
                need(raw.startswith(header),'running source header');start=0;end=len(header)
        else:
            match=re.search(r'(?:^|\n)'+str(number)+r'\s*$',raw)
            need(match is not None,'isolated folio')
            start=match.start()+int(raw[match.start()]=='\n');end=len(raw)
        if start is not None:
            literal=raw[start:end]
            cuts.append({'page':number,'start':offset+start,'end':offset+end,
                         'literal':literal,'sha256':sha(literal.encode())})
        offset+=len(raw)+1;text.append(raw);fonts.extend(names);fonts.append('')
    raw='\n'.join(text);fonts=fonts[:-1]
    need(spec['page_bindings']==bindings and spec['pages']==len(bindings),'all physical pages')
    need(spec['extraction_sha256']==sha(raw.encode()),'entire extracted text')
    need(len(spec['included_spans'])==1,'one full span')
    span=spec['included_spans'][0]
    need(span['start']==0 and span['end']==len(raw) and span['sha256']==sha(raw.encode()),'whole span')
    need([{k:c[k] for k in cuts[0]} for c in spec['excluded_furniture']]==cuts,'exact furniture only')
    calibrated=list(raw);used=set()
    for g in spec['glyph_substitutions']:
        i=g['offset'];need(i not in used,'unique glyph');used.add(i)
        need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and fonts[i]==g['input_font'],'actual input glyph/font')
        event=g['pdf_event']
        matches=[a for a in aliases if a['font_identity']==event['font_identity'] and
                 a['encoded_byte']==event['encoded_byte'] and a['glyph_name']==event['glyph_name'] and
                 a['input']==raw[i] and a['font']==fonts[i]]
        need(len(matches)==1 and matches[0]['output']==g['output'] and len(g['output'])==1,'reviewed visible glyph')
        need(sha(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'glyph context')
        need(not any(c['start']<=i<c['end'] for c in cuts),'glyph not in removed furniture')
        calibrated[i]=g['output']
    def select(s):
        chunks=[];at=0
        for c in cuts:chunks.append(s[at:c['start']]);at=c['end']
        chunks.append(s[at:]);return '\n'.join(chunks)
    variants={'raw_untrimmed':raw,'raw_selected':select(raw),'calibrated_selected':select(''.join(calibrated))}
    return {v:{n:counts(t,n) for n in ['NFC','NFKC']} for v,t in variants.items()}

def main():
    ap=argparse.ArgumentParser()
    for n in ['author','public-root','sources-root','out']:ap.add_argument('--'+n,type=pathlib.Path,required=True)
    a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    def load(name):return json.loads((a.author/name).read_text())
    need(sha((a.author/'manifest.json').read_bytes())==PIN,'frozen author manifest')
    for r in load('manifest.json')['exports']:
        data=(a.author/r['path']).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'exact export')
    policy=load('policy.json')
    def resolve(row):
        return {'public':a.public_root,'sources':a.sources_root}[row['root']]/row['path']
    specs=load('input_spec.json')
    aliases=load('glyph_aliases.json')['aliases'];expected=load('author_counts.json')
    need(set(specs)=={'N007','U','A1','CODE'},'all four complete PDFs')
    docs={}
    for key,spec in specs.items():
        docs[key]=document(resolve(spec),key,spec,aliases)
        need(docs[key]==expected['documents'][key]['metrics'],'all30 PDF coordinates '+key)
    raw={};raw_count=0
    for category in ['programs','drivers','formal']:
        for row in policy[category]:
            data=resolve(row).read_bytes()
            need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full raw-file identity')
            metrics={n:counts(data.decode(),n) for n in ['NFC','NFKC']}
            need(metrics==expected['raw_files'][category][row['path']]['metrics'],'all10 raw-file coordinates')
            raw[row['path']]=metrics;raw_count+=1
    need(raw_count==4,'all four complete raw files')
    controls=[]
    for name,fn in [
        ('drop physical page',lambda s:s['page_bindings'].pop()),
        ('select only a proof',lambda s:s['included_spans'][0].update(start=100)),
        ('remove body as furniture',lambda s:s['excluded_furniture'][0].update(start=0)),
        ('alter actual glyph font',lambda s:s['glyph_substitutions'][0].update(input_font='fake')),
        ('erase version stamp as furniture',lambda s:s['excluded_furniture'][0].update(end=s['excluded_furniture'][0]['end']+50)),
        ('change visible left angle',lambda s:next(x for x in s['glyph_substitutions'] if x['input_codepoint']=='U+000A').update(output=' '))]:
        changed=copy.deepcopy(specs['N007']);fn(changed)
        try:document(resolve(changed),'N007',changed,aliases)
        except ValueError:controls.append(name)
        else:raise ValueError('control accepted '+name)
    result={'status':'PASS_INDEPENDENT_RECOUNT','pdf_metric_cells':120,'raw_metric_cells':40,
            'documents':docs,'raw_files':raw,'negative_controls':controls,'glyph_choices_independently_viewed':34,
            'font_event_walker':'separate fresh author replay; not independently reimplemented here',
            'graphics_limit':'XYDASH aliases preserve stroke directions, not the full graph or precise angles.',
            'compression_factor':None,'new_original_credit':0,'new_question_credit':0}
    (a.out/'recount.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','negative_controls']}))
if __name__=='__main__':main()
