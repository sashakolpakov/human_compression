#!/usr/bin/env python3
"""Independent actual-dictionary/outline reconciliation and rejection controls."""
import unicodedata,copy,json
from fontTools import agl
from recount import need,ALIASES,sha
SPECIAL={'negationslash':'̸','unionsq':'⊔','square':'□','triangleleftequal':'⊴','prime':'′','lessnotequal':'⪇'}
def classify(audit):
    result=[]
    for r in audit['F010']['classes']:
        family=r['font'].split('+')[-1];name=r['glyph_name'];s=r['decoded_text'];alias=ALIASES.get((family,name))
        expected=SPECIAL.get(name,agl.toUnicode(name))
        need(alias is not None or s==expected or unicodedata.normalize('NFKC',s)==unicodedata.normalize('NFKC',expected),'unclassified actual glyph '+family+' '+name)
        result.append(dict(font_dictionary=r['font_dictionary'],encoded_byte=r['encoded_byte'],glyph_name=name,classification='visually classified alias' if alias else 'visually checked non-AGL glyph' if name in SPECIAL else 'AGL identity or normalized ligature',replacement=alias))
    need(len(result)==566,'all566 used classes');return result

def compare(ours,theirs):
    actual=ours['F010'];author=theirs['F010'];index={(tuple(r['font_dictionary']),r['encoded_byte'],r['decoded_text']):r for r in actual['classes']}
    rows=author['encoded_glyph_classes'];need(len(rows)==len(index),'all font class rows')
    dictionaries={tuple(r['font_dictionary']):r for r in actual['font_dictionaries']};need(len(dictionaries)==len(author['font_dictionaries'])==26,'all distinct font dictionaries')
    for r in rows:
        d=r['font_dictionary_object'];q=(tuple([d['idnum'],d['generation']]),r['encoded_byte'],r['decoded_text']);need(q in index,'actual font class identity');a=index[q]
        need(all(r[k]==a[k] for k in ['font','glyph_name','occurrences','font_stream_sha256','effective_encoding_sha256','outline_sha256']),'actual used glyph/outline/encoding')
        need(r['font_dictionary_sha256']==dictionaries[q[0]]['font_dictionary_sha256'],'font dictionary bytes')
        need(r['decoded_codepoints']==[f'U+{ord(c):04X}' for c in r['decoded_text']],'every decoded codepoint')
    for r in author['font_dictionaries']:
        d=r['font_dictionary_object'];a=dictionaries[d['idnum'],d['generation']]
        need(all(r[k]==a[k] for k in ['font','font_stream_sha256','effective_encoding_sha256','font_dictionary_sha256']),'full font dictionary identity')
        mapping={int(k):v for k,v in r['effective_encoding'].items()};need(sha(json.dumps(mapping,sort_keys=True).encode())==a['effective_encoding_sha256'],'full effective encoding map bound')
    need(sum(p['aligned_characters'] for p in author['pages'])==actual['aligned_characters']==25953,'complete character alignment')
    need(author['form_xobjects_visited']==actual['forms'],'complete Form traversal')
    need(len(author['actual_space_events'])==len(actual['actual_space_events']),'all actual spaces and visible whitespace')
    for a,b in zip(actual['actual_space_events'],author['actual_space_events']):need(all(b[k]==v for k,v in a.items()),'true encoded whitespace/visible outline preserved')
    need(sum(x['visible_outline'] for x in author['actual_space_events'])==3,'three actual visible tab braces')
    return True

def controls(ours,theirs):
    changes=[('substitute missing glyph',lambda x:x['F010']['encoded_glyph_classes'][0].update(glyph_name='.notdef')),('alter actual outline',lambda x:x['F010']['encoded_glyph_classes'][0].update(outline_sha256='0'*64)),('merge distinct dictionary',lambda x:x['F010']['encoded_glyph_classes'][0]['font_dictionary_object'].update(idnum=0)),('alter effective encoding',lambda x:x['F010']['encoded_glyph_classes'][0].update(effective_encoding_sha256='0'*64)),('omit used glyph class',lambda x:x['F010']['encoded_glyph_classes'].pop()),('discard true space',lambda x:x['F010']['actual_space_events'].pop(0)),('turn visible tab brace into space',lambda x:next(r for r in x['F010']['actual_space_events'] if r['visible_outline']).update(visible_outline=False)),('alter actual full encoding dictionary',lambda x:x['F010']['font_dictionaries'][0]['effective_encoding'].update({'0':'space'}))]
    out=[]
    for name,f in changes:
        b=copy.deepcopy(theirs);f(b)
        try:compare(ours,b)
        except (ValueError,KeyError):out.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted mutation '+name)
    return out
