#!/usr/bin/env python3
"""Portable bounded independent input review, no science or numerical ratios."""
import argparse,copy,json,pathlib,subprocess,sys
import boundary,recount,font_review
from boundary import need,read,sha,bound
H=pathlib.Path(__file__).resolve().parent
AUTHOR='4c61d955ddc8178c759e7943cde62deefb3c6696878a54d095146e207e5c8b29'
def summarize(r):
    return {**{k:v for k,v in r.items()if k!='evidence'},'evidence_summary':{k:dict(extraction_sha256=x['extraction_sha256'],pages=x['pages'],furniture=x['furniture'],calibration_occurrences=len(x['calibrations']),actual_font_dictionaries=x['font_audit'].get('distinct_font_dictionaries'),actual_glyph_classes=len(x['font_audit'].get('classes',[])),raster_images=x['images'],visitor=x['visitor'])for k,x in r['evidence'].items()}}
def same_counts(r,a):
    need(r['documents']==a['documents'],'all PDF counts and hashes');need(r['raw_files']==a['raw_files'],'all whole-file counts and hashes')
def reader_rows(packet,r):
    t=(packet/'input_reader.tex').read_text();rows=[]
    labels={'F010':'F010 original','L126':'L126 original','U_R':'Complete shared theory','R1':'Complete F010 application','R2':'Complete L126 application','CODE':'Separate full program appendix'}
    for k,label in labels.items():
        x=r['documents'][k];line=f"{label} & {x['pages']} & {x['variants']['raw_untrimmed']['NFC']['characters_without_whitespace']:,} & {x['variants']['calibrated_selected']['NFC']['characters_without_whitespace']:,}"
        need(line in t,'reader document integer row '+k);rows.append(line)
    roles={'required_finite_certificate':'Required finite certificate','required_graph_data':'Mandatory complete graph data','optional_validation':'Optional validation programs','current_orchestration_driver':'Operational helpers','partial_formal_evidence':'Partial Lean evidence'}
    for role,label in roles.items():
        xs=[x for x in r['raw_files'].values()if x['role']==role];line=f"{label} & {len(xs)} & {sum(x['bytes']for x in xs):,} & {sum(x['metrics']['NFC']['characters_without_whitespace']for x in xs):,}";need(line in t,'reader raw integer row '+role);rows.append(line)
    return rows

def run(a):
    need(not a.out.exists(),'fresh review output');a.out.mkdir(parents=True)
    need(sha((a.packet/'manifest.json').read_bytes())==AUTHOR,'exact author freeze')
    for x in read(a.packet/'manifest.json')['exports']:bound(a.packet,x)
    if (H/'manifest.json').exists():
        for x in read(H/'manifest.json')['exports']:bound(H,x)
    if (H/'bindings.json').exists():
        bindings=read(H/'bindings.json')
        for row in bindings['accepted_and_authored_packets']:bound(a.study_root,row)
        bound(a.study_root,bindings['font_helper_exact_reuse'])
    b=boundary.run(a.study_root,a.packet,a.public_root);r=recount.run(a.study_root,a.packet);f=font_review.run(a.study_root,a.packet,r);rows=reader_rows(a.packet,r)
    controls=[];author=read(a.packet/'author_counts.json')
    changes=[('wrong_PDF_count',lambda x:x['documents']['R1']['variants']['raw_untrimmed']['NFC'].update(characters_without_whitespace=0)),('wrong_normalization_hash',lambda x:x['documents']['L126']['variants']['calibrated_selected']['NFKC'].update(collapsed_text_sha256='0'*64)),('drop_complete_data',lambda x:x['raw_files'].pop('certificate/graph.json')),('wrong_raw_role',lambda x:x['raw_files']['certificate/check.py'].update(role='optional_validation'))]
    for name,change in changes:
        x=copy.deepcopy(author);change(x)
        try:same_counts(r,x)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('mutation accepted '+name)
    summary=summarize(r)
    for name,value in [('independent_counts.json',summary),('boundary_report.json',b),('font_report.json',f)]:
        if (H/name).exists():need(read(H/name)==value,'reproduces frozen '+name)
        (a.out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    report=dict(status='PASS_DISTINCT_INPUT_REVIEW',author_manifest_sha256=AUTHOR,author_exports=54,PDF_metric_cells=180,raw_metric_cells=170,normalized_text_hashes=70,actual_PDF_pages=71,reader_integer_rows=len(rows),independent_controls=b['controls']+f['controls']+controls,source_or_math_programs_rerun=False,factors=None)
    if a.author_replay:
        cmd=[sys.executable,'-B','-O',str(a.packet/'check.py'),'--study-root',str(a.study_root),'--public-root',str(a.public_root),'--out',str(a.out/'author_replay')]
        if a.render:cmd+=['--render','--xelatex',a.xelatex]
        proc=subprocess.run(cmd,capture_output=True,text=True);(a.out/'author.stdout').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'fresh author input replay');report['fresh_author_replay']=read(a.out/'author_replay/report.json')
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);p.add_argument('--public-root',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--author-replay',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.study_root=a.study_root.resolve();a.packet=a.packet.resolve();a.public_root=a.public_root.resolve();a.out=a.out.resolve();r=run(a);print(json.dumps({k:v for k,v in r.items()if k not in ['independent_controls','fresh_author_replay']},ensure_ascii=False))
