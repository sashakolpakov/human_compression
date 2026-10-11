#!/usr/bin/env python3
"""Classify each actual primary font/byte glyph; no PDF text or font bytes exported."""
from pathlib import Path
import json,unicodedata
from collections import Counter
from fontTools.agl import toUnicode
from calibration import ALIASES
from extract_inputs import sha,need
HERE=Path(__file__).resolve().parent

def reconcile(audits):
    result={}
    preserved={'prime':'′','square':'□','triangleleftequal':'⊴','negationslash':'̸','angbracketleft':'⟨','angbracketright':'⟩','diamondmath':'⋄'}
    for key,audit in audits.items():
        rows=[]
        for row in audit['encoded_glyph_classes']:
            c=row['decoded_text'];alias=ALIASES.get((key,row['font'],row['encoded_byte'],c));u=toUnicode(row['glyph_name'])
            if alias:
                need(alias[1]==row['glyph_name'],'exact alias glyph identity');category='occurrence_bound_visible_glyph_repair';out=alias[0]
            elif u==c:category='decoded_text_agrees_with_glyph_name';out=c
            elif u and unicodedata.normalize('NFKC',u)==c:
                category='literal_parser_expansion_of_ligature_preserved';out=c
            else:
                need(row['glyph_name'] in preserved and preserved[row['glyph_name']]==c,'every non-AGL glyph explicitly identified')
                category='actual_outline_review_confirms_decoded_symbol';out=c
            need(row['glyph_evidence']['visible'] or c.isspace(),'every counted nonspace glyph visible')
            rows.append(dict(font_identity=row['font_identity'],font=row['font'],encoded_byte=row['encoded_byte'],glyph_name=row['glyph_name'],decoded_text=c,measured_text=out,occurrences=row['occurrences'],category=category,glyph_evidence=row['glyph_evidence']))
        counts=Counter(r['category'] for r in rows)
        result[key]=dict(actual_dictionary_count=len(audit['font_dictionaries']),encoded_class_count=len(rows),aligned_characters=sum(p['aligned_characters'] for p in audit['pages']),categories=dict(counts),substitutions=sum(r['occurrences'] for r in rows if r['category']=='occurrence_bound_visible_glyph_repair'),classes=rows)
    return dict(status='AUTHOR_FONT_RECONCILIATION_PENDING_INDEPENDENT_INPUT_REVIEW',font_audit_sha256=sha((HERE/'font_audit.json').read_bytes()),documents=result,source_graphics_cost=None,notes=['Names and outlines are identified at actual dictionary/effective encoding and byte, never cached by BaseFont alone.','Literal parser expansions of fi/fl/ff/ffi remain expanded; no discretionary re-ligaturing occurs.','Mathematical alphabet, parenthesis pieces, intersection signs, visible whitespace vertical extensions and bitmap bullets use exact occurrence-bound repairs.','All 18 repaired glyph classes and all 33 Adobe-glyph-list exception classes were rendered from the actual font programs and viewed. Some classes occur in both panels.','This records text-glyph identity; spatial formula/diagram construction cost remains unknown.'])

if __name__=='__main__':
    result=reconcile(json.loads((HERE/'font_audit.json').read_text()))
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ['actual_dictionary_count','encoded_class_count','aligned_characters','substitutions']} for k,v in result['documents'].items()}))
