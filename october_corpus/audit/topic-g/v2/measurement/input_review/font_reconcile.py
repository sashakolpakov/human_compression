#!/usr/bin/env python3
"""Compare the independently decoded actual dictionaries and every used outline."""
import unicodedata,copy
from fontTools import agl
from recount import need,ALIASES
SPECIAL={'braceleftBigg':'{','bracketleftbig':'[','bracketrightbig':']','parenleftbig':'(','parenrightbig':')','summationdisplay':'∑','phi':'ϕ','star':'⋆','angbracketleft':'⟨','angbracketright':'⟩','mapsto':'↦','negationslash':'̸','unionsq':'⊔','prime':'′','greaterorequalslant':'⩾','lessorequalslant':'⩽','square':'□','triangleleftequal':'⊴','trianglerightequal':'⊵','multicloseright':'⋊','circlecopyrt':'⃝'}
def classify(audit):
    result=[]
    for key,a in audit.items():
        if key not in ('L009','L092'):continue
        for r in a['classes']:
            family=r['font'].split('+')[-1];name=r['glyph_name'];s=r['decoded_text'];alias=ALIASES.get((family,name))
            expected=SPECIAL.get(name,agl.toUnicode(name))
            need(alias is not None or s==expected or unicodedata.normalize('NFKC',s)==unicodedata.normalize('NFKC',expected),'unclassified actual glyph '+family+' '+name)
            result.append(dict(source=key,font_dictionary=r['font_dictionary'],encoded_byte=r['encoded_byte'],glyph_name=name,classification='visually classified alias' if alias else 'visually checked non-AGL/variant/composite glyph' if name in SPECIAL else 'AGL identity or normalized ligature',replacement=alias))
    return result

def compare(ours,theirs):
    for key in ['L009','L092']:
        actual=ours[key];author=theirs[key];index={(tuple(r['font_dictionary']),r['encoded_byte'],r['decoded_text']):r for r in actual['classes']}
        rows=author['encoded_glyph_classes'];need(len(rows)==len(index),'all font class rows')
        for r in rows:
            d=r['font_dictionary_object'];q=(tuple([d['idnum'],d['generation']]),r['encoded_byte'],r['decoded_text']);need(q in index,'actual font class identity');a=index[q]
            need(all(r[k]==a[k] for k in ['font','glyph_name','occurrences','font_stream_sha256','effective_encoding_sha256','outline_sha256']),'actual used glyph/outline/encoding')
            need(r['decoded_codepoints']==[f'U+{ord(c):04X}' for c in r['decoded_text']],'every decoded codepoint')
        dictionaries={tuple(r['font_dictionary']):r for r in actual['font_dictionaries']};need(len(dictionaries)==len(author['font_dictionaries']),'all distinct font dictionaries')
        for r in author['font_dictionaries']:
            d=r['font_dictionary_object'];a=dictionaries[d['idnum'],d['generation']]
            need(all(r[k]==a[k] for k in ['font','font_stream_sha256','effective_encoding_sha256','font_dictionary_sha256']),'full font dictionary identity')
        need(sum(p['aligned_characters'] for p in author['pages'])==actual['nonspace_characters'],'complete character alignment')
        need(author['form_xobjects_visited']==actual['forms'],'complete Form traversal')
        need(len(author['actual_space_events'])==len(actual['actual_space_events']),'all true spaces')
        for a,b in zip(actual['actual_space_events'],author['actual_space_events']):need(all(b[k]==v for k,v in a.items()),'true encoded space preserved')
    return True

def controls(ours,theirs):
    changes=[('restore name-only cache missing glyph',lambda x:x['L009']['encoded_glyph_classes'][0].update(glyph_name='.notdef')),('alter actual outline',lambda x:x['L009']['encoded_glyph_classes'][0].update(outline_sha256='0'*64)),('merge distinct dictionary',lambda x:x['L009']['encoded_glyph_classes'][0]['font_dictionary_object'].update(idnum=0)),('alter effective encoding',lambda x:x['L009']['encoded_glyph_classes'][0].update(effective_encoding_sha256='0'*64)),('omit used glyph class',lambda x:x['L092']['encoded_glyph_classes'].pop()),('discard true space',lambda x:x['L009']['actual_space_events'].pop())]
    out=[]
    for name,f in changes:
        b=copy.deepcopy(theirs);f(b)
        try:compare(ours,b)
        except (ValueError,KeyError):out.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted mutation '+name)
    return out
