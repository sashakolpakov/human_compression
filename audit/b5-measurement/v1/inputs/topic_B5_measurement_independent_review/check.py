#!/usr/bin/env python3
"""Independent bounded B5 input review; exact copied author replay is optional."""
from pathlib import Path
from collections import Counter
import argparse,copy,json,shutil,subprocess,sys,time
import pypdf
from recount import audit,need,read,sha,selection
import font_recheck

BASE='papers/topic-b/extensions/high-rank/v1/'
ADMISSION='audit/topic-b/extensions/high-rank/v1/admission.json'
def scope(p,b):
    need((p['source_id'],p['topic'],p['original_manuscripts_added'],p['old_original_manuscripts'],p['topic_originals_after_update'],p['new_topics'])==('L040','B',1,4,5,0),'one original in existing topic B')
    need((p['source_rows'],p['proof_spans'],p['principal_targets'])==(35,25,5),'fixed scientific contract')
    need((p['source']['pages'],p['source']['article_pages'],p['source']['cover_pages'])==(21,20,1) and p['source_cover_retained_in_primary'] is True,'complete accepted edition including cover')
    need([p['replacements'][k]['pages'] for k in ('U_ADD','A5','CODE')]==[10,11,7] and p['retained_old_common']['pages']==5,'all old and new common papers')
    for k in ('retain_all_four_old_applications','retain_complete_old_programs','new_common_whole_not_deduplicated','all_declared_code_prepurchased_for_conditional_results','raw_and_printed_code_are_alternatives'):need(p[k] is True,k)
    roles=[x['role'] for x in p['programs']]
    need(roles==['required_finite_primitive_inputs','finite_validation','finite_validation','required_only_for_auxiliary_n8_and_validation_of_branching'],'exact four complete program roles')
    need((p['new_code_whole_files'],p['principal_required_programs'],p['validation_programs'],p['auxiliary_example_programs'])==(4,1,2,1),'no program pruning or premise inflation')
    need(len(p['drivers'])==2 and len(p['formal'])==1 and p['partial_formal_declarations']==8 and p['whole_source_formalized'] is False,'separate drivers and scoped formal evidence')
    need(all(x is None for x in p['unknown_costs'].values()) and set(p['unknown_costs'])=={'full_graphics','historical_software','retained_external_proofs','primitive_catalogue_construction','full_formalization'},'unknown costs remain null')
    need(p['primary'].startswith('Whole literal rendered N001 text plus raw_untrimmed PDFs') and p['ratio'] is None and p['factors_permitted'] is False and p['new_scientific_credit']==0,'fixed old B primary and input-only scope')
    a=b[ADMISSION]
    need((a['source_rows'],a['proof_spans'],a['principal_targets'])==(35,25,5),'admitted contract preserved')
    need(a['literal_branching_clause_recovered'] is False and a['corrected_general_presentation'] is True and a['whole_source_formalized'] is False,'corrected source and formal boundary')
    need(a['charge_full_common_paper'] is True and a['cross_topic_overlap_discount'] is False,'complete common cost')
    need(a['complete_mathematical_programs']==4 and a['required_principal_programs']==1,'scientific program boundary')

# Independent visual decisions: one glyph component, not reconstructed diagrams.
DASH={2:('╲',18),3:('╱',18),4:('─',33),5:('╲',5),6:('╱',3),7:('╲',3),8:('╱',5),9:('╲',3),10:('╲',3)}
SYMS={15:('⊢',1),68:('𝒟',4),70:('ℱ',26),71:('𝒢',44),80:('𝒫',2),84:('𝒯',5)}
def calibrated_scope(spec,font):
    seen=Counter();expected={( '/HDMLID+XYDASH-Medium',k,v[0]):v[1] for k,v in DASH.items()}
    expected.update({('/HDMKDA+CMSY10',k,v[0]):v[1] for k,v in SYMS.items()})
    for key,row in spec.items():
        for r in row['glyph_substitutions']:
            need(key=='L040','no speculative own calibration')
            e=r['pdf_events'][0];cl=[c for c in font[key]['encoded_glyph_classes'] if c['font_identity']==e['font_identity'] and c['encoded_byte']==e['encoded_byte'] and c['decoded_text']==r['input']]
            need(len(cl)==1,'exact actual dictionary/byte class')
            face=next(f for f in font[key]['font_dictionaries'] if f['font_identity']==e['font_identity'])
            for k in ('font_dictionary_object','font_dictionary_sha256','effective_encoding_sha256','font_stream_sha256'):need(e[k]==face[k],'actual event '+k)
            need(e['glyph_name']==cl[0]['glyph_name'] and e['font']==r['input_font'],'actual glyph identity')
            seen[e['font'],e['encoded_byte'],r['output']]+=1
    need(seen==Counter(expected),'all fifteen visual classes and 173 occurrences; no curved guesses')
    curves=[c for c in font['L040']['encoded_glyph_classes'] if 'XYCIRC' in c['font']]
    need(len(curves)==24 and all(c['decoded_text'].startswith('/c') for c in curves),'literal curved-component boundary')

def controls(packet,public,sources):
    p=read(packet/'policy.json');b=read(packet/'source_boundary.json');spec=read(packet/'input_spec.json');font=read(packet/'font_audit.json');scope(p,b);calibrated_scope(spec,font);tests=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,StopIteration):tests.append(dict(name=name,rejected=True));return
        raise ValueError('Control survived: '+name)
    def mutate(fn):q=copy.deepcopy(p);fn(q);scope(q,b)
    for name,fn in [
      ('clauses counted as originals',lambda q:q.update(original_manuscripts_added=35)),
      ('new topic invented',lambda q:q.update(new_topics=1)),
      ('old applications omitted',lambda q:q.update(retain_all_four_old_applications=False)),
      ('old program bundle omitted',lambda q:q.update(retain_complete_old_programs=False)),
      ('overlap discount for new common',lambda q:q.update(new_common_whole_not_deduplicated=False)),
      ('source cover omitted from primary',lambda q:q.update(source_cover_retained_in_primary=False)),
      ('whole validation program pruned',lambda q:q['programs'].pop(1)),
      ('auxiliary example promoted to uniform premise',lambda q:q['programs'][3].update(role='required_finite_primitive_inputs')),
      ('conditional prepays only required program',lambda q:q.update(all_declared_code_prepurchased_for_conditional_results=False)),
      ('raw and printed program charged together',lambda q:q.update(raw_and_printed_code_are_alternatives=False)),
      ('graphics assigned zero',lambda q:q['unknown_costs'].update(full_graphics=0)),
      ('external proof assigned zero',lambda q:q['unknown_costs'].update(retained_external_proofs=0)),
      ('whole source formalization claimed',lambda q:q.update(whole_source_formalized=True)),
      ('old B primary silently replaced',lambda q:q.update(primary='calibrated_selected')),
      ('premature factor allowed',lambda q:q.update(factors_permitted=True))]:reject(name,lambda fn=fn:mutate(fn))
    roots=dict(packet=packet,public=public,sources=sources);r=spec['L040'];pages=[x.extract_text() or '' for x in pypdf.PdfReader(roots[r['root']]/r['path']).pages]
    def cut(fn):s=copy.deepcopy(r);fn(s);selection('L040',pages,s)
    reject('last authored page omitted',lambda:selection('L040',pages[:-1],r))
    reject('authored text removed as furniture',lambda:cut(lambda s:s['excluded_furniture'].append(dict(page=1,start=0,end=100))))
    reject('visible control glyph deleted',lambda:cut(lambda s:next(x for x in s['glyph_substitutions'] if x['input']=='\x00').update(output='')))
    reject('article span starts on wrong page',lambda:cut(lambda s:s['article_only_span'].update(start=0)))
    def glyph(fn):s=copy.deepcopy(spec);fn(s['L040']['glyph_substitutions']);calibrated_scope(s,font)
    reject('sloping stroke reversed',lambda:glyph(lambda g:next(x for x in g if x['output']=='╱').update(output='╲')))
    reject('mapsto component promoted to full arrow',lambda:glyph(lambda g:next(x for x in g if x['output']=='⊢').update(output='↦')))
    reject('actual encoding replaced by font-name assumption',lambda:glyph(lambda g:g[0]['pdf_events'][0].update(effective_encoding_sha256='0'*64)))
    reject('actual dictionary replaced',lambda:glyph(lambda g:g[0]['pdf_events'][0].update(font_dictionary_object=dict(idnum=1,generation=0))))
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--author-replay',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
    home=Path(__file__).resolve().parent
    if (home/'manifest.json').exists():
        for r in read(home/'manifest.json')['exports']:
            path=Path(r['path']);need(not path.is_absolute() and '..' not in path.parts,'safe review export');data=(home/path).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'unchanged review export')
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);a.packet=a.packet.resolve();a.public_root=a.public_root.resolve();a.sources_root=a.sources_root.resolve();start=time.monotonic()
    counts=audit(a.packet,a.public_root,a.sources_root);fonts=font_recheck.audit(a.packet,a.public_root,a.sources_root);tests=controls(a.packet,a.public_root,a.sources_root)
    # The packet's snapshots must match actual scientific JSON bytes, not just labels.
    for path,data in read(a.packet/'source_boundary.json').items():need(data==read(a.public_root/path),'exact scientific boundary '+path)
    copied=None;author=None;render=None
    def run(cmd,name):
        p=subprocess.run(cmd,capture_output=True,text=True);(a.out/(name+'.stdout')).write_text(p.stdout);(a.out/(name+'.stderr')).write_text(p.stderr);need(p.returncode==0,'fresh '+name)
    if a.author_replay or a.render:
        copied=a.out/'author_packet';copied.mkdir();m=read(a.packet/'manifest.json')
        for r in m['exports']:
            rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe author export');dest=copied/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.packet/rel,dest)
        shutil.copy2(a.packet/'manifest.json',copied/'manifest.json');need(len([f for f in copied.rglob('*') if f.is_file()])==25,'24 exact exports plus manifest only')
    if a.author_replay:
        run([sys.executable,'-B','-O',str(copied/'check.py'),'--public-root',str(a.public_root),'--sources-root',str(a.sources_root),'--out',str(a.out/'author_replay')],'author')
        author=read(a.out/'author_replay/report.json');need((author['semantic_controls'],author['pdf_metric_cells'],author['article_only_cells'],author['raw_metric_cells'])==(34,120,30,70),'author complete replay scope')
    if a.render:
        run([sys.executable,'-B','-O',str(copied/'build_reader.py'),'--out',str(a.out/'reader_render'),'--xelatex',a.xelatex],'reader')
        render=read(a.out/'reader_render/render_report.json');old=[p.extract_text() or '' for p in pypdf.PdfReader(a.packet/'input_reader.pdf').pages];new=[p.extract_text() or '' for p in pypdf.PdfReader(a.out/'reader_render/input_reader.pdf').pages]
        need(old==new and len(new)==2 and render['diagnostics']==[],'all reader page text and clean build');render['complete_page_text_identical']=True
    report=dict(status='PASS',author_manifest_sha256=counts['author_manifest_sha256'],pdf_cells=120,article_only_cells=30,raw_cells=70,text_hashes=44,source_replacement_code_pages=49,font_dictionaries=27,actual_encoded_classes=667,independent_controls=tests,author_replay=author,reader_rebuild=render,export_only_copy=copied is not None,scientific_programs_executed=False,new_credit=0,ratio=None,elapsed_seconds=time.monotonic()-start)
    for name,data in [('recount.json',counts),('font_recheck.json',fonts),('report.json',report)]: (a.out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('PASS 220 coordinates, 44 hashes, 27 dictionaries, 667 classes,',len(tests),'independent controls')
if __name__=='__main__':main()
