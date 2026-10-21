"""Distinct whole-text recount; no author counting functions or factors."""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata
from pypdf import PdfReader

def need(ok,msg):
    if not ok: raise ValueError(msg)
def digest(b): return hashlib.sha256(b).hexdigest()
def measure(text,normalization):
    text=unicodedata.normalize(normalization,text)
    collapsed=' '.join(text.split())
    return dict(whitespace_tokens=len(text.split()),
        alphanumeric_units=len(re.findall(r'[^\W_]+',text)),
        characters_without_whitespace=len(''.join(text.split())),
        characters_with_collapsed_whitespace=len(collapsed),
        utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
        normalized_text_sha256=digest(text.encode()),
        collapsed_text_sha256=digest(collapsed.encode()))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--public',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();p=args.study/'topic_B_L047_measurement_inputs'
    need(not args.out.exists(),'fresh report')
    load=lambda n:json.loads((p/n).read_text())
    need(digest((p/'manifest.json').read_bytes())=='33de3038e6bca21ee35e79d819a0bd2bc5e8eb2c594ec16d65d671729f93fcef','author manifest')
    for row in load('manifest.json')['exports']:
        data=(p/row['path']).read_bytes()
        need(len(data)==row['bytes'] and digest(data)==row['sha256'],'author export '+row['path'])
    counts=load('author_counts.json');spec=load('input_spec.json');policy=load('policy.json')
    old=load('precount/baseline/author_counts.json')
    need(all(counts['documents'][k]==v for k,v in old['documents'].items()),'old PDF observations exact')
    need(counts['retained_source_coordinates']==load('precount/baseline/retained_source_counts.json'),'retained original observations exact')
    need(counts['raw_files']==old['raw_files'],'old raw observations exact')
    output={};num=0
    for key,row in spec.items():
        data=(args.study/row['path']).read_bytes()
        need(digest(data)==row['sha256'] and len(data)==row['bytes'],'new whole PDF binding')
        pages=[page.extract_text() or '' for page in PdfReader(args.study/row['path']).pages]
        raw='\n'.join(pages);need(len(pages)==row['pages'] and digest(raw.encode())==row['extraction_sha256'],'literal extraction')
        def edit(repairs):
            changes=[(f['start'],f['end'],'\n',f['literal']) for f in row['excluded_furniture']]
            if repairs:changes.extend((g['start'],g['end'],g['output'],g['input']) for g in row['glyph_substitutions'])
            previous=-1
            for a,b,value,literal in sorted(changes):
                need(0<=a<b<=len(raw) and a>=previous and raw[a:b]==literal,'nonoverlapping literal edits')
                previous=b
            result=raw
            for a,b,value,literal in sorted(changes,reverse=True):result=result[:a]+value+result[b:]
            return result
        variants={'raw_untrimmed':raw,'raw_selected':edit(False),'calibrated_selected':edit(True)}
        output[key]={v:{n:measure(text,n) for n in policy['normalizations']} for v,text in variants.items()}
        need(output[key]==counts['documents'][key]['metrics'],'distinct thirty-cell recount '+key);num+=30
    raw_num=0
    for row in load('precount/raw_inventory.json')['files']:
        source={'study':args.study,'public':args.public}[row['file']['root']]/row['file']['path']
        data=source.read_bytes();need(len(data)==row['file']['bytes'] and digest(data)==row['file']['sha256'],'whole raw binding')
        measured={n:measure(data.decode(),n) for n in policy['normalizations']}
        expected=counts['raw_files'][row['category']][row['old_path']]['metrics'] if row['inherited'] else counts['new_raw_files'][row['id']]['metrics']
        need(measured==expected,'distinct whole raw recount '+row['id']);raw_num+=10
    report=dict(status='PASS_DISTINCT_INPUT_RECOUNT',author_manifest_sha256=digest((p/'manifest.json').read_bytes()),
        new_document_cells=num,whole_raw_cells=raw_num,retained_document_cells=360,
        retained_article_sensitivity_cells=30,documents=output,source_intake_added=0,
        factors=None,new_formal_credit=0,new_question_credit=0,
        limits='PDF extractor version is retained; calibration event alignment replayed separately and outlines reviewed directly. No whole-source Lean claim.')
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS distinct120 new document cells and170 whole raw cells; retained inputs unchanged; no factors')
if __name__=='__main__':main()
