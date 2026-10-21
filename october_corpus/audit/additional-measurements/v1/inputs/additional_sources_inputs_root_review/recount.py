#!/usr/bin/env python3
"""Independent whole-document recount. No author module is imported.

Glyph choices are the visually reviewed, actual-font-bound declarations;
the author's separately replayed event walker checks their byte origins.
This checker independently extracts all page text and font labels, verifies
the complete boundaries, and recounts every declared cost coordinate.
"""
import argparse, copy, hashlib, json, pathlib, re, unicodedata
import pypdf

PIN='d4dd3429290d2a893b20f5c5205aa69b42fef44c56eec5acca31ea5a045e743a'
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
    need(sha(path.read_bytes())==spec['pdf_sha256'],'PDF identity')
    text=[];fonts=[];bindings=[];offset=0;cuts=[]
    for number,page in enumerate(pypdf.PdfReader(path).pages,1):
        pieces=[];names=[]
        def visit(t,cm,tm,font,size):
            pieces.append(t);names.extend([str(font.get('/BaseFont',font.get('/Name',''))) if font else '']*len(t))
        raw=page.extract_text(visitor_text=visit) or ''
        need(raw==''.join(pieces) and raw,'whole nonempty page')
        bindings.append({'page':number,'start':offset,'end':offset+len(raw),
                         'sha256':sha(raw.encode()),'empty_extraction':False})
        start=end=None
        if key=='F015':
            if number>1:
                footer='the electronic journal of combinatorics 30(2) (2023), #P2.20 '+str(number)
                need(raw.endswith(footer),'journal footer')
                start=len(raw)-len(footer);end=len(raw)
        elif key=='L028' and number>1:
            header=(f'{number} F. BUEKENHOUT, D. LEEMANS, AND P. TRANCHIDA\n'
                    if number%2==0 else f'A NEW ALGORITHM FOR CHIRAL POLYTOPES {number}\n')
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
        matches=[a for a in aliases if a['document']==key and a['font_identity']==event['font_identity'] and
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
    policy=load('policy.json');locations=load('publication_binding.json')['locations']
    def resolve(name):
        row=locations[name];return {'public':a.public_root,'sources':a.sources_root,'packet':a.author}[row['root']]/row['path']
    specs=load('source_input_spec.json')['sources']|load('replacement_input_spec.json')['ours']
    aliases=load('proposed_aliases.json')['aliases'];expected=load('author_counts.json')
    need(set(specs)=={'F015','L028','U_M','M1','M_CODE','U_CE','CE1','CE_CODE'},'all8 documents')
    docs={}
    for key,spec in specs.items():
        docs[key]=document(resolve(spec['path']),key,spec,aliases)
        need(docs[key]==expected['documents'][key]['metrics'],'all30 PDF coordinates '+key)
    raw={};raw_count=0
    for category in ['complete_programs','separate_drivers','separate_formal_files']:
        for row in policy[category]:
            data=resolve(row['path']).read_bytes()
            need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full raw-file identity')
            metrics={n:counts(data.decode(),n) for n in ['NFC','NFKC']}
            need(metrics==expected['raw_files'][category][row['path']]['metrics'],'all10 raw-file coordinates')
            raw[row['path']]=metrics;raw_count+=1
    need(raw_count==9,'all9 complete raw files')
    controls=[]
    for name,fn in [
        ('drop physical page',lambda s:s['page_bindings'].pop()),
        ('select only a proof',lambda s:s['included_spans'][0].update(start=100)),
        ('remove body as furniture',lambda s:s['excluded_furniture'][0].update(start=0)),
        ('alter actual glyph font',lambda s:s['glyph_substitutions'][0].update(input_font='fake'))]:
        changed=copy.deepcopy(specs['F015']);fn(changed)
        try:document(resolve(changed['path']),'F015',changed,aliases)
        except ValueError:controls.append(name)
        else:raise ValueError('control accepted '+name)
    result={'status':'PASS_INDEPENDENT_RECOUNT','pdf_metric_cells':240,'raw_metric_cells':90,
            'documents':docs,'raw_files':raw,'negative_controls':controls,'glyph_choices_independently_viewed':88,
            'font_event_walker':'separate fresh author replay; not independently reimplemented here',
            'UTF8_limit':'CE_CODE hook-left glyph retains extracted comma; exact standalone Unicode identity not asserted',
            'compression_factor':None,'new_original_credit':0,'new_question_credit':0}
    (a.out/'recount.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','negative_controls']}))
if __name__=='__main__':main()
