#!/usr/bin/env python3
"""Exercise independently checked boundary and glyph failures on real input."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--proposal',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    if a.out.exists():raise ValueError('fresh report required')
    spec=importlib.util.spec_from_file_location('independent',Path(__file__).with_name('recount.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    row=json.loads((a.proposal/'source_input_spec.json').read_text())['sources']['N003']
    pdf=a.study_root/row['path']
    raw='\n'.join(p.extract_text() for p in mod.pypdf.PdfReader(pdf).pages)
    cases=[]
    r=copy.deepcopy(row);r['glyph_substitutions'][0]['output']='';cases.append(('deleted_visible_glyph',r))
    r=copy.deepcopy(row);r['glyph_substitutions'][0]['input_font']='/wrong';cases.append(('wrong_font',r))
    r=copy.deepcopy(row);r['glyph_substitutions'][0]['offset']+=1;cases.append(('shifted_occurrence',r))
    r=copy.deepcopy(row);r['included_spans'][0]['end']-=1;cases.append(('trailing_text_omitted',r))
    r=copy.deepcopy(row);r['page_bindings'].pop();cases.append(('page_binding_omitted',r))
    r=copy.deepcopy(row);r['excluded_furniture'].append(copy.deepcopy(r['excluded_furniture'][0]));cases.append(('overlapping_furniture',r))
    r=copy.deepcopy(row);lo,hi=100,110;r['excluded_furniture']=[dict(page=1,start=lo,end=hi,literal=raw[lo:hi],sha256=hashlib.sha256(raw[lo:hi].encode()).hexdigest())];cases.append(('body_text_as_furniture',r))
    rejected=[]
    for name,bad in cases:
        try:mod.measure(pdf,bad)
        except ValueError as exc:rejected.append(dict(name=name,reason=str(exc)))
        else:raise RuntimeError('false boundary accepted: '+name)
    a.out.write_text(json.dumps(dict(status='PASS',scope='Independent boundary/font controls on actual N003 PDF; no author counter imported.',rejected=rejected),indent=2)+'\n')
    print('PASS:',len(rejected),'independent controls')
if __name__=='__main__':main()
