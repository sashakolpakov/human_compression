#!/usr/bin/env python3
"""Independent full-document recount using a character mask, not measure.py.

Source PDFs are supplied separately. No source text is emitted. This checks
lengths, not mathematical validity or the costs of missing historical code.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
import pypdf


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(data):
    return sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument('--sources-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'Use a fresh output file.')
    protocol = args.repo/'audit/topic-e/v2/protocol.json'
    data = protocol.read_bytes()
    need(digest(data)=='1e3a2c97bc32d1edf5d1844fe871384ea71588a3dab64cb799c347ba16eea982',
         'Changed measurement boundary.')
    p = json.loads(data)
    need(pypdf.__version__==p['pypdf_version'], 'Different PDF extractor.')
    costs = {}
    for key,row in (p['sources']|p['old']|p['new']).items():
        path = (args.sources_root/row['path'] if key in p['sources'] else
                args.repo/p['public_locations'][row['path']])
        need(digest(path.read_bytes())==row['pdf_sha256'], key+' PDF')
        pages = [page.extract_text() or '' for page in pypdf.PdfReader(path).pages]
        need(len(pages)==row['pages'], key+' pages')
        raw = '\n'.join(pages)
        need(digest(raw.encode())==row['extraction_sha256'], key+' extraction')
        changes = {r['offset']:r for r in row['glyph_substitutions']}
        need(len(changes)==len(row['glyph_substitutions']), 'Repeated glyph offset.')
        controls = set()
        for i,c in enumerate(raw):
            if ord(c)<32 and c not in '\r\n\t':
                controls.add(i)
                r = changes.get(i)
                need(key=='L021' and r is not None and
                     (c,r['output']) in [('\x12','('),('\x13',')')] and
                     c==chr(int(r['input_codepoint'][2:],16)), key+' glyph')
            need(c!='\ufffd' and unicodedata.category(c)!='Co', key+' invalid glyph')
        need(controls==set(changes), key+' glyph coverage')
        need(len(row['included_spans'])==1, key+' whole manuscript')
        span = row['included_spans'][0]
        need(span['start']==0 and span['end']==len(raw) and
             span['sha256']==digest(raw.encode()), key+' complete boundary')
        keep = [True]*len(raw)
        for span in row['excluded_furniture']:
            a,b = span['start'],span['end']
            need(0<=a<b<=len(raw) and digest(raw[a:b].encode())==span['sha256'],
                 key+' furniture')
            for i in range(a,b):
                need(keep[i], key+' overlapping exclusion')
                keep[i] = False
        output = []
        last_removed = False
        for i,c in enumerate(raw):
            if keep[i]:
                output.append(changes[i]['output'] if i in changes else c)
            elif not last_removed:
                output.append('\n')
            last_removed = not keep[i]
        text = ''.join(output)
        costs[key] = {}
        for form in p['normalizations']:
            t = unicodedata.normalize(form,text)
            s = ' '.join(t.split())
            costs[key][form] = {
                'whitespace_tokens':len(s.split()),
                'alphanumeric_units':len(re.findall(r'[^\W_]+',t)),
                'characters_without_whitespace':sum(not c.isspace() for c in t),
                'characters_with_collapsed_whitespace':len(s),
                'utf8_bytes_with_collapsed_whitespace':len(s.encode())}
    result = {'status':'PASS_INDEPENDENT_RECOUNT', 'protocol_sha256':digest(data),
              'checker_sha256':digest(Path(__file__).read_bytes()),
              'scope':'Independent character-mask extraction and metric implementation; all 15 full documents and 10 coordinates.',
              'costs':costs}
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: independently counted 150 document/metric cells.')


if __name__=='__main__':
    main()
