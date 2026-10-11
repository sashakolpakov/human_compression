#!/usr/bin/env python3
"""Independent complete-text recount for the affine input proposal.

Reuses the reviewed root Topic D counting implementation, independently of the
affine input author. Font identities and furniture need their separate review."""
from pathlib import Path
import argparse,hashlib,json,unicodedata
import pypdf

def need(ok,message):
    if not ok: raise ValueError(message)

def digest(data):return hashlib.sha256(data).hexdigest()

def metrics(text,normalization):
    text=unicodedata.normalize(normalization,text)
    tokens=[];current=[];units=0;inside=False
    for c in text:
        if c.isspace():
            if current:tokens.append(''.join(current));current=[]
        else:current.append(c)
        if c.isalnum():
            if not inside:units+=1
            inside=True
        else:inside=False
    if current:tokens.append(''.join(current))
    collapsed=' '.join(tokens)
    return {'whitespace_tokens':len(tokens),'alphanumeric_units':units,
      'characters_without_whitespace':sum(map(len,tokens)),
      'characters_with_collapsed_whitespace':len(collapsed),
      'utf8_bytes_with_collapsed_whitespace':len(collapsed.encode()),
      'collapsed_text_sha256':digest(collapsed.encode())}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--proposal',type=Path,required=True)
    ap.add_argument('--study',type=Path,required=True);ap.add_argument('--public',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'Use a fresh output report')
    need(pypdf.__version__=='6.13.0','Pinned PDF extractor')
    load=lambda name:json.loads((a.proposal/name).read_text())
    manifest=load('manifest.json')
    for r in manifest['exports']:
        b=(a.proposal/r['path']).read_bytes();need(len(b)==r['bytes'] and digest(b)==r['sha256'],'Frozen export '+r['path'])
    original=load('source_input_spec.json')['sources'];ours=load('replacement_input_spec.json')['ours']
    expected=load('author_counts.json');publication=load('publication_binding.json');records={};total_pages=total_repaired=0
    for key,row in {**original,**ours}.items():
        path=(a.study/row['path']) if key in original else a.public/publication['documents'][key]['public_path']
        need(digest(path.read_bytes())==row['pdf_sha256'],'PDF binding '+key)
        texts=[];fonts=[];page_records=[];offset=0
        for number,page in enumerate(pypdf.PdfReader(path).pages,1):
            parts=[];fontmap=[]
            def visitor(text,cm,tm,font,size):
                parts.append(text);fontmap.extend([str(font.get('/BaseFont','')) if font else '']*len(text))
            text=page.extract_text(visitor_text=visitor) or ''
            need(text==''.join(parts) and len(text)==len(fontmap),'Visitor agreement')
            page_records.append({'page':number,'start':offset,'end':offset+len(text),
              'sha256':digest(text.encode()),'empty_extraction':not text})
            texts.append(text);fonts.extend(fontmap+['']);offset+=len(text)+1
        raw='\n'.join(texts);fonts=fonts[:-1]
        need(page_records==row['page_bindings'] and len(texts)==row['pages'],'All physical page bindings '+key)
        need(digest(raw.encode())==row['extraction_sha256'],'Full text '+key)
        need(len(row['included_spans'])==1 and row['included_spans'][0]['start']==0 and
             row['included_spans'][0]['end']==len(raw) and row['included_spans'][0]['sha256']==digest(raw.encode()),'Complete manuscript selection')
        furniture=row['excluded_furniture'];end=0
        for r in furniture:
            lo,hi=r['start'],r['end'];need(end<=lo<hi<=len(raw),'Ordered furniture')
            need(raw[lo:hi]==r['literal'] and digest(raw[lo:hi].encode())==r['sha256'],'Literal furniture');end=hi
        def select(text):
            out=[];cursor=0
            for r in furniture:out.append(text[cursor:r['start']]);cursor=r['end']
            out.append(text[cursor:]);return '\n'.join(out)
        calibrated=list(raw);seen=set()
        for r in row['glyph_substitutions']:
            at=r['offset'];need(at not in seen,'Duplicate calibration');seen.add(at)
            need(raw[at]==chr(int(r['input_codepoint'][2:],16)) and fonts[at]==r['input_font'],'Actual occurrence/font')
            need(len(r['output'])==1 and not r['output'].isspace(),'No deletion or spacing repair')
            page=page_records[r['page']-1]
            need(at==page['start']+r['page_offset'] and page['start']<=at<page['end'],'Physical-page occurrence')
            lo,hi=r['context_start'],r['context_end']
            need(lo<=at<hi and digest(raw[lo:hi].encode())==r['context_sha256'],'Occurrence context')
            calibrated[at]=r['output']
        variants={}
        for variant,text in [('raw_untrimmed',raw),('raw_selected',select(raw)),('calibrated_selected',select(''.join(calibrated)))]:
            variants[variant]={form:metrics(text,form) for form in ['NFC','NFKC']}
        need(variants==expected['documents'][key]['variants'],'Independent metric disagreement '+key)
        records[key]={'pdf_sha256':row['pdf_sha256'],'pages':len(texts),'calibrated_occurrences':len(seen),
          'furniture_occurrences':len(furniture),'variants':variants}
        total_pages+=len(texts);total_repaired+=len(seen)
    raw_records={}
    for kind,binding_key in [('complete_programs','complete_mathematical_programs'),
                             ('complete_auxiliary_scripts','complete_auxiliary_scripts'),
                             ('complete_formal_files','complete_formal_files')]:
        raw_records[kind]={}
        bindings={Path(r['public_path']).name:r for r in publication[binding_key]}
        need(set(bindings)==set(expected[kind]),'Complete file inventory '+kind)
        for name,row in expected[kind].items():
            binding=bindings[name];b=(a.public/binding['public_path']).read_bytes()
            need(len(b)==row['bytes']==binding['bytes'] and digest(b)==row['sha256']==binding['sha256'],'Whole file '+name)
            variants={form:metrics(b.decode(),form) for form in ['NFC','NFKC']}
            need(variants==row['metrics'],'Independent raw-file metrics '+name)
            raw_records[kind][name]={'sha256':digest(b),'bytes':len(b),'variants':variants}
    need(set(records)=={'L012','U_Affine','AF1','CODE'} and total_pages==41 and total_repaired==114,'Complete inventory')
    need([len(raw_records[k]) for k in ['complete_programs','complete_auxiliary_scripts','complete_formal_files']]==[6,3,3],'Complete file roles')
    result={'status':'PASS_INDEPENDENT_TEXT_RECOUNT_PENDING_FONT_AND_SELECTION_REVIEW',
      'proposal_manifest_sha256':digest((a.proposal/'manifest.json').read_bytes()),'checker_sha256':digest(Path(__file__).read_bytes()),
      'documents':records,'raw_records':raw_records,'pdf_metric_cells':120,'normalized_PDF_text_hashes':24,
      'raw_program_and_auxiliary_formal_metric_cells':120,'required_program_metric_cells':60,'auxiliary_metric_cells':30,'formal_metric_cells':30,'physical_pages':41,'calibrated_occurrences':114,
      'all_source_font_identities_independently_accepted':False,'all_furniture_visually_reviewed':False,
      'author_functions_imported':False,'shared_pypdf_dependency':pypdf.__version__,'ratio':None}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','normalized_PDF_text_hashes','raw_program_and_auxiliary_formal_metric_cells','physical_pages']}))
if __name__=='__main__':main()
