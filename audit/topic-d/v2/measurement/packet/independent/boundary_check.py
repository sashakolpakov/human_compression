#!/usr/bin/env python3
"""Check immutable editions, complete program roles, and corrected glyph evidence."""
from pathlib import Path
import argparse, hashlib, json, re

def need(ok, message):
    if not ok: raise ValueError(message)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--public',type=Path,required=True);ap.add_argument('--font-report',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'Fresh output required')
    old=a.study/'topic_D_measurement';new=a.study/'topic_D_measurement_v2'
    manifests=[]
    for directory,count in [(old,15),(new,16)]:
        manifest=read(directory/'manifest.json');need(len(manifest['exports'])==count,'Complete frozen export inventory')
        for row in manifest['exports']:
            p=directory/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Frozen export '+row['path'])
        manifests.append(dict(path=directory.name+'/manifest.json',sha256=sha(directory/'manifest.json'),exports=count))
    unchanged=['policy.json','publication_binding.json','replacement_input_spec.json','source_contract_boundary.json']
    for name in unchanged:need((old/name).read_bytes()==(new/name).read_bytes(),'Unchanged '+name)
    binding=read(new/'publication_binding.json')
    need(sha(a.public/binding['admission']['path'])==binding['admission']['sha256'],'Accepted public mathematical edition')
    for row in binding['scientific_documents'].values():
        need(sha(a.public/row['public_path'])==row['pdf_sha256'],'Published PDF identity')
    programs=binding['complete_mathematical_programs'];drivers=binding['complete_drivers']
    need(len(programs)==8 and len(drivers)==2,'Complete program and driver inventory')
    for row in programs+drivers:
        p=a.public/row['public_path'];need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Complete raw program binding')
    need(sum(r['classification']=='required' for r in programs)==5 and
         sum(r['classification']=='diagnostic' for r in programs)==3,'Five required and three diagnostics')
    appendix=(a.public/'papers/topic-d/v2/program-appendix.tex').read_text()
    included=re.findall(r'\\VerbatimInput\[[^\]]*\]\{(programs/[^}]+)\}',appendix)
    need(len(included)==8 and set(included)=={'programs/'+Path(r['path']).name for r in programs},'Each complete mathematical program printed once')
    need(not re.search(r'(firstline|lastline)\s*=',appendix),'No code-line pruning')
    boundary=read(new/'source_contract_boundary.json');scope=read(a.public/'papers/topic-d/v2/scope.json')
    need(boundary['contract_count']==len(boundary['rows'])==len(scope['contracts'])==37,'All detailed source clauses')
    for row,original in zip(boundary['rows'],scope['contracts']):
        need(all(original[k]==v for k,v in row.items()),'Preserved detailed source clause')
    source_before=read(old/'source_input_spec.json')['sources'];source_after=read(new/'source_input_spec.json')['sources']
    edits=[]
    for key,row in source_after.items():
        before=source_before[key]
        for field in ['pdf_sha256','pages','page_bindings','extraction_sha256','included_spans','excluded_furniture']:
            need(row[field]==before[field],'Unchanged complete source selection')
        need(len(row['glyph_substitutions'])==len(before['glyph_substitutions']),'No removed calibration')
        for x,y in zip(before['glyph_substitutions'],row['glyph_substitutions']):
            for field in ['offset','page','page_offset','input_codepoint','input_font','context_start','context_end','context_sha256']:
                need(x[field]==y[field],'Same original calibration occurrence')
            if x['output']!=y['output']:edits.append(dict(document=key,offset=y['offset'],before=x['output'],after=y['output']))
    need(len(edits)==14 and all(r['document']=='L066' and r['after'] in '[]' for r in edits),'Exactly fourteen bracket repairs')
    before=read(old/'author_counts.json');after=read(new/'author_counts.json');delta=[]
    for key,row in before['documents'].items():
        for variant,normalizations in row['variants'].items():
            for form,units in normalizations.items():
                for unit,value in units.items():
                    new_value=after['documents'][key]['variants'][variant][form][unit]
                    if new_value!=value:delta.append(dict(document=key,variant=variant,normalization=form,unit=unit,
                        before=value,after=new_value))
    need(len(delta)==4 and all(r['document']=='L066' and r['variant']=='calibrated_selected' and
         r['unit'] in ['utf8_bytes_with_collapsed_whitespace','collapsed_text_sha256'] for r in delta),'Exactly declared count/hash changes')
    need(all(r['after']-r['before']==-28 for r in delta if r['unit']!='collapsed_text_sha256'),'Exactly minus28 UTF8 bytes')
    for k in ['raw_program_alternative','full_drivers_separate']:
        need(before[k]==after[k],'Whole raw program and driver counts unchanged')
    font=read(a.font_report);need(font['status']=='PASS_INDEPENDENT_GLYPH_IDENTITIES','Independent event/font review accepted')
    need(font['proposal_manifest_sha256']==sha(new/'manifest.json'),'Independent report binds corrected edition')
    groups=read(new/'glyph_evidence.json')['groups'];need(len(groups)==21,'All encoded glyph identities retained')
    seen=set()
    for group in groups:
        key=group['document'];identity=group['glyph_identity'];name=group['font'];byte=group['encoded_byte']
        uses=[r for r in font['documents'][key]['calibrated_occurrences'] if r['font']==name and r['encoded_byte']==byte]
        need(len(uses)==group['count'] and uses,'All encoded glyph occurrences')
        for actual in uses:
            need(actual['expected_output']==group['visible_output'] and actual['glyph_name']==identity['glyph_name']
                 and actual['outline_sha256']==identity['outline_sha256']
                 and actual['font_stream_sha256']==group['font_identity']['font_stream_sha256'],'Embedded outline evidence')
            need((key,actual['offset']) not in seen,'No duplicate group ownership');seen.add((key,actual['offset']))
        need({x['offset'] for x in uses}=={x['offset'] for x in group['occurrences']},'Exact encoded occurrence set')
    need(len(seen)==148,'Complete reviewed calibration set')
    policy=read(new/'policy.json');need(policy['comparison_policy']['cross_topic_deduplication'] is False,'Whole topic common theory')
    for k in ['retained_external_cost','diagram_and_layout_cost','ratio']:need(policy[k] is None,'Unknown costs/factors remain null')
    result=dict(status='PASS_INDEPENDENT_D_INPUT_BOUNDARY',checker_sha256=sha(Path(__file__)),manifests=manifests,
        immutable_metadata=unchanged,public_proof_admission_sha256=binding['admission']['sha256'],
        detailed_source_rows=37,complete_mathematical_programs=8,required_programs=5,diagnostics=3,separate_full_drivers=2,
        source_selection_unchanged=True,calibrated_occurrences=148,encoded_font_glyph_classes=21,
        corrected_occurrences=edits,metric_delta=delta,independent_font_report_sha256=sha(a.font_report),
        new_source_credit=0,new_question_credit=0,ratio=None)
    a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','detailed_source_rows','calibrated_occurrences','encoded_font_glyph_classes']}))

if __name__=='__main__':main()
