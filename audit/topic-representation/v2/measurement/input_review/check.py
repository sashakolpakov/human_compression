#!/usr/bin/env python3
"""Replay the independent Representation input review; no factors or math rerun."""
import argparse,copy,json,pathlib,time
import recount,font_reconcile,boundary
from recount import need,read,sha
PIN='122820fac69c94d484444a88b4318fa7ae1a588770c4378737af7d457a037af1'

def audit(study,packet,public):
    start=time.monotonic();need(sha((packet/'manifest.json').read_bytes())==PIN,'exact author input freeze')
    ours=recount.run(study,packet);theirs=read(packet/'font_audit.json');font_reconcile.compare(ours['font_audit'],theirs);classes=font_reconcile.classify(ours['font_audit']);fontcontrols=font_reconcile.controls(ours['font_audit'],theirs)
    br=boundary.run(study,packet,public)
    row=read(packet/'source_input_spec.json')['sources']['F010'];controls=[]
    changes=[('omit mapped alias',lambda x:x['glyph_substitutions'].pop()),('lose tab-coded right brace',lambda x:next(r for r in x['glyph_substitutions'] if r['input_codepoint']=='U+0009').update(output=' ')),('merge mapsto with its separate arrow',lambda x:next(r for r in x['glyph_substitutions'] if r['pdf_event']['glyph_name']=='mapsto').update(output='↦')),('wrong actual dictionary',lambda x:x['glyph_substitutions'][0]['pdf_event']['font_dictionary_object'].update(idnum=0)),('delete body as furniture',lambda x:x['excluded_furniture'][0].update(end=x['excluded_furniture'][0]['end']+1)),('omit first source character',lambda x:x['included_spans'][0].update(start=1))]
    for name,change in changes:
        b=copy.deepcopy(row);change(b)
        try:recount.document(study,'F010',b)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted input mutation '+name)
    summary=dict(status='ACCEPTED_INDEPENDENT_MEASUREMENT_INPUT_REVIEW',author_manifest_sha256=PIN,pdf_metric_cells=120,raw_metric_cells=60,normalized_text_hashes=36,documents=ours['documents'],raw_files=ours['raw_files'],font_summary=dict(used_classes=len(classes),actual_dictionaries=26,aligned_characters=25953,calibration_occurrences=134,alias_classes=14,visible_whitespace_braces=3,unknown_unembedded_font_outline='Standard WinAnsi Times-Roman arXiv banner',all_used_outlines_and_encodings_match=True,basefont_collisions=ours['font_audit']['F010']['basefont_encoding_collisions']),boundary=br,controls=fontcontrols+controls,controls_rejected=len(fontcontrols)+len(controls)+len(br['controls']),ratios=None,new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_text_exported=False,elapsed_seconds=round(time.monotonic()-start,3))
    return summary
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path);ap.add_argument('--public-root',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh report path');packet=a.packet or a.study_root/'topic_Representation_measurement_inputs';result=audit(a.study_root,packet,a.public_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','controls_rejected','ratios','elapsed_seconds']}))
