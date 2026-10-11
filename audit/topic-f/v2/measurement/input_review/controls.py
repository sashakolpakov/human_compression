#!/usr/bin/env python3
"""Semantic corruptions exercise the independent checker below immutable hash gates."""
import argparse, copy, json, pathlib
import recount as R

def main(study, packet):
    src=R.read(packet/'source_input_spec.json')['sources']['L014'];rep=R.read(packet/'replacement_input_spec.json');fa=R.read(packet/'font_audit.json');gi=R.read(packet/'graphic_inventory.json')
    cases=[]
    def reject(name, fn):
        try:fn()
        except (ValueError,KeyError,IndexError) as e:cases.append(dict(name=name,rejected=True,reason=str(e)));return
        raise ValueError('Control accepted: '+name)
    def pdfchange(name,fn):
        x=copy.deepcopy(src);fn(x);reject(name,lambda:R.document(study,'L014',x,fa,gi))
    pdfchange('drop a visible calibrated glyph',lambda x:x['glyph_substitutions'].pop())
    pdfchange('replace one blackboard glyph by ordinary letter',lambda x:x['glyph_substitutions'][0].update(output='Z'))
    pdfchange('wrong actual font',lambda x:x['glyph_substitutions'][0].update(input_font='/Times-Roman'))
    pdfchange('wrong encoded text byte',lambda x:x['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=88))
    pdfchange('omit first page from selected text',lambda x:x['included_spans'][0].update(start=x['page_bindings'][1]['start']))
    def bodycut(x):
        first=R.pypdf.PdfReader(study/x['path']).pages[0].extract_text()[0]
        c=x['excluded_furniture'][0];c.update(start=0,end=1,literal=first,sha256=R.digest(first.encode()))
    pdfchange('replace first footer by a body cut',bodycut)
    def reverse(x):
        next(r for r in x['glyph_substitutions'] if r['output']=='⊲')['output']='⊳'
    pdfchange('reverse normality glyph',reverse)
    for key in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']:
        x=copy.deepcopy(rep);x[key].pop();reject('omit a complete '+key,lambda x=x:R.boundary(x))
    x=copy.deepcopy(rep);x['complete_validation_programs'][0]['uniform_written_proof_premise']=True;reject('relabel validation as a proof premise',lambda:R.boundary(x))
    x=copy.deepcopy(rep);x['retained_external_cost']=0;reject('price unknown external theorem at zero',lambda:R.boundary(x))
    # A numeric error is rejected after an otherwise valid independent extraction.
    d,_,_=R.document(study,'L014',src,fa,gi);bad=copy.deepcopy(d);bad['variants']['calibrated_selected']['NFC']['characters_without_whitespace']+=1
    reject('one wrong input metric',lambda:R.require(d==bad,'independent document differs'))
    return dict(status='PASS',independent_controls=len(cases),controls=cases,scope='Semantic gates, with immutable author data unchanged; no factors.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();R.require(not a.out.exists(),'fresh output');r=main(a.study_root,a.packet or a.study_root/'topic_F_measurement_inputs');a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['independent_controls'])
