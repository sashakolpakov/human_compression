#!/usr/bin/env python3
"""Independent selected-PDF-text audit; does not import the author counter."""
import argparse, hashlib, json, unicodedata
from pathlib import Path
import pypdf


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def count(raw, form):
    text=unicodedata.normalize(form,raw)
    tokens=alphanumeric=nonspace=0
    in_token=in_alpha=False
    compact=[]
    for c in text:
        white=c.isspace()
        alpha=c.isalnum()
        if not white:
            nonspace+=1
            if not in_token:
                tokens+=1
                if compact:compact.append(' ')
            compact.append(c)
        if alpha and not in_alpha:alphanumeric+=1
        in_alpha=alpha
        in_token=not white
    selected=''.join(compact)
    return dict(whitespace_tokens=tokens,alphanumeric_units=alphanumeric,
                characters_without_whitespace=nonspace,
                characters_with_collapsed_whitespace=len(selected),
                utf8_bytes_with_collapsed_whitespace=sum(len(c.encode()) for c in selected),
                collapsed_text_sha256=digest(selected.encode()))


def measure(pdf,row):
    require(digest(pdf.read_bytes())==row['pdf_sha256'],'source PDF hash')
    reader=pypdf.PdfReader(pdf)
    require(len(reader.pages)==row['pages'],'all physical pages')
    texts=[];fonts=[];actual_pages=[];offset=0
    for number,page in enumerate(reader.pages,1):
        fragments=[]
        def visit(text,cm,tm,font,size):
            fragments.append((text,str(font.get('/BaseFont','')) if font else ''))
        body=page.extract_text(visitor_text=visit) or ''
        require(body==''.join(t for t,_ in fragments),'font visitor/extracted text agreement')
        local=[font for text,font in fragments for _ in text]
        require(len(local)==len(body),'font attribution coverage')
        actual_pages.append(dict(page=number,start=offset,end=offset+len(body),
            sha256=digest(body.encode()),empty_extraction=not body))
        texts.append(body);fonts.extend(local);fonts.append('');offset+=len(body)+1
    raw='\n'.join(texts);fonts=fonts[:-1]
    require(actual_pages==row['page_bindings'],'page order, extents and extracted hashes')
    require(digest(raw.encode())==row['extraction_sha256'],'complete extracted text hash')
    require(len(row['included_spans'])==1 and row['included_spans'][0]['start']==0 and
            row['included_spans'][0]['end']==len(raw),'complete document boundary')
    keep=bytearray([1])*len(raw);deletions={}
    for furniture in row['excluded_furniture']:
        lo,hi=furniture['start'],furniture['end'];page=actual_pages[furniture['page']-1]
        require(page['start']<=lo<hi<=page['end'],'furniture contained in recorded page')
        require(raw[lo:hi]==furniture['literal'] and digest(raw[lo:hi].encode())==furniture['sha256'],
                'exact furniture occurrence')
        prefix=raw[page['start']:lo];suffix=raw[hi:page['end']]
        require(not prefix.strip() or not suffix.strip(),'furniture must be a page prefix or suffix')
        require(all(keep[lo:hi]),'overlapping furniture')
        keep[lo:hi]=bytes(hi-lo);deletions[lo]=hi
    substitute={}
    hooks={0xf8eb:'⎛',0xf8ed:'⎝',0xf8f6:'⎞',0xf8f8:'⎠'}
    for g in row['glyph_substitutions']:
        i=g['offset'];c=raw[i];f=fonts[i]
        require(i not in substitute and keep[i],'unique retained glyph')
        require(ord(c)==int(g['input_codepoint'][2:],16) and f==g['input_font'],'actual font and glyph')
        expected=hooks.get(ord(c)) if 'CMEX' in f else ('○' if 'LCIRCLE' in f and c=='i' else None)
        require(expected is not None and g['output']==expected,'visually authorized substitution')
        page=actual_pages[g['page']-1]
        require(page['start']+g['page_offset']==i and page['start']<=i<page['end'],'glyph page locator')
        require(g['context_start']<=i<g['context_end'] and
                digest(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'glyph context')
        substitute[i]=g['output']
    suspects={i for i,c in enumerate(raw) if
        (ord(c)<32 and not c.isspace()) or unicodedata.category(c)=='Co' or c=='\ufffd' or
        ('LCIRCLE' in fonts[i] and not c.isspace())}
    require(suspects==set(substitute),'all and only classified suspect glyphs')
    selected=[];calibrated=[];i=0
    while i<len(raw):
        if i in deletions:
            selected.append('\n');calibrated.append('\n');i=deletions[i]
        else:
            selected.append(raw[i]);calibrated.append(substitute.get(i,raw[i]));i+=1
    variants=dict(raw_untrimmed=raw,raw_selected=''.join(selected),calibrated_selected=''.join(calibrated))
    return {name:{form:count(text,form) for form in ('NFC','NFKC')} for name,text in variants.items()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--proposal',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    require(not a.out.exists(),'fresh report path')
    require(pypdf.__version__=='6.13.0','pinned pypdf')
    def load(name):return json.loads((a.proposal/name).read_text())
    manifest=load('manifest.json')
    for r in manifest['exports']:
        b=(a.proposal/r['path']).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'author export binding')
    source=load('source_input_spec.json');replacement=load('replacement_input_spec.json')
    publication=load('publication_binding.json');author=load('author_counts.json')
    expected=source['sources']|replacement['ours']
    require(set(expected)=={'N003','N008','L030','U_B','B1','B2','B3','B4'},'full existing document roster')
    results={};cells=hashes=0
    for key,row in expected.items():
        pdf=a.study_root/row['path'] if key in source['sources'] else a.public_root/publication['scientific_documents'][key]['public_path']
        result=measure(pdf,row);require(result==author['documents'][key]['variants'],'independent numerical disagreement: '+key)
        results[key]=result
        cells+=sum(len(v)-1 for forms in result.values() for v in forms.values())
        hashes+=sum(len(forms) for forms in result.values())
    require(cells==240 and hashes==48,'all metric and hash coordinates')
    require(source['missing_source_pdf']['N001']['pdf_cost'] is None and author['four_source_pdf_total'] is None,'missing source remains unknown')
    output=dict(status='PASS_INDEPENDENT_RECOUNT',method='Independent character-state counters, page-prefix/suffix furniture checks and font-glyph audit; same pinned PDF parser, no author functions imported.',
        proposal_manifest_sha256=digest((a.proposal/'manifest.json').read_bytes()),checker_sha256=digest(Path(__file__).read_bytes()),
        pypdf_version=pypdf.__version__,metric_cells=cells,text_hashes=hashes,documents=results,
        complete_application_roster=list(replacement['ours']),N001_pdf_cost=None,whole_topic_factor=None,
        new_source_credit=0,new_question_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=output['status'],metric_cells=cells,text_hashes=hashes)))

if __name__=='__main__':main()
