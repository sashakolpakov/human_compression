#!/usr/bin/env python3
"""Bounded independent input audit, with optional export-only author replay/render."""
from pathlib import Path
import argparse,copy,json,subprocess,sys,shutil,time
import pypdf
from recount import audit,need,read,sha,selection
import font_recheck

def scope(p,b):
    need(p['original_manuscripts_added']==2 and p['source_ids']==['L128','L068'] and p['new_topic_count']==0,'two originals in existing topics')
    need(p['source_originals_after_update']==dict(A=7,C=5),'whole topic source rosters')
    for topic,n in [('A',6),('C',4)]:
        r=p['whole_topic_rules'][topic]
        need(r['previous_originals']==n and r['retain_all_previous_applications'] is True and r['retain_full_previous_common'] is True and r['old_program_bundle_retained'] is True,'whole previous topic retained')
    a,c=p['whole_topic_rules']['A'],p['whole_topic_rules']['C']
    need(a['new_application']=='A7' and a['new_required_files']==1 and not a['additional_common'],'complete A addition')
    need(c['new_application']=='C5' and c['additional_common']==['U_C_INC'] and c['old_required_files']==2 and c['new_required_files']==1 and c['shared_existing_file_charged_once'] is True,'complete C addition and shared once')
    need(len(p['old_C_required_programs'])==2 and len(p['new_programs'])==2 and p['shared_program']['sha256']==p['old_C_required_programs'][0]['sha256'],'program closure')
    need(all(v is None for v in p['unknown_costs'].values()),'unknown is null')
    need(not p['full_formalization_claim'] and p['partial_formal_declarations']==9 and len(p['formal'])==2 and len(p['drivers'])==3,'partial formal evidence and separate drivers')
    need(not p['factors_permitted'] and p['ratio'] is None and p['no_new_mathematical_credit'],'inputs only')
    need(p['A_primary'].startswith('Unchanged accepted calibrated_selected NFC') and p['C_primary'].startswith('Unchanged accepted whole rendered L108 text + raw_untrimmed PDFs'),'different accepted primary policies preserved')
    ar=b['audit/topic-a/extensions/diagram-symmetries/v1/admission.json'];cr=b['audit/topic-c/extensions/livingstone/v1/admission.json']
    need((ar['source_rows'],ar['proof_spans'],cr['source_rows'],cr['proof_spans'])==(14,7,17,9),'exact current admitted scope')
    need(cr['literal_Q_recovered'] is False and cr['literal_P_recovered'] is True and cr['corrected_Q_recovered'] is True,'explicit corrected source contract')
    need(ar['whole_source_formalized'] is False and cr['whole_source_formalized'] is False,'no full Lean claim')
    for x in (ar,cr):need(x['charge_full_common_paper'] is True and x['cross_topic_overlap_discount'] is False,'scientific admission full common input')

def controls(packet,public,sources):
    p=read(packet/'policy.json');b=read(packet/'source_boundary.json');scope(p,b);tests=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):tests.append(dict(name=name,rejected=True));return
        raise ValueError('Control survived: '+name)
    def mutate(fn):
        q=copy.deepcopy(p);fn(q);scope(q,b)
    for name,fn in [
        ('clauses counted as original manuscripts',lambda q:q.update(original_manuscripts_added=31)),
        ('new topics invented',lambda q:q.update(new_topic_count=2)),
        ('free old A common paper',lambda q:q['whole_topic_rules']['A'].update(retain_full_previous_common=False)),
        ('drop earlier C applications',lambda q:q['whole_topic_rules']['C'].update(retain_all_previous_applications=False)),
        ('drop whole additional incidence note',lambda q:q['whole_topic_rules']['C'].update(additional_common=[])),
        ('double shared construction',lambda q:q['whole_topic_rules']['C'].update(shared_existing_file_charged_once=False)),
        ('erase old exhaustive census',lambda q:q['old_C_required_programs'].pop()),
        ('erase whole new finite program',lambda q:q['new_programs'].pop()),
        ('silently zero graphics',lambda q:q['unknown_costs'].update(full_graphics=0)),
        ('claim full formal proof',lambda q:q.update(full_formalization_claim=True)),
        ('change C primary coordinate',lambda q:q.update(C_primary='calibrated_selected')),
        ('factor before acceptance',lambda q:q.update(factors_permitted=True))]:reject(name,lambda fn=fn:mutate(fn))
    spec=read(packet/'input_spec.json');roots=dict(packet=packet,public=public,sources=sources)
    cached={k:[pg.extract_text() or '' for pg in pypdf.PdfReader(roots[r['root']]/r['path']).pages] for k,r in spec.items() if k in ('L128','L068')}
    def change(key,fn):r=copy.deepcopy(spec[key]);fn(r);selection(key,cached[key],r)
    reject('drop final source page',lambda:selection('L068',cached['L068'][:-1],spec['L068']))
    reject('erase authored front matter as furniture',lambda:change('L068',lambda r:r['excluded_furniture'].append(dict(page=1,start=0,end=100))))
    reject('envelope reconstructed as seven glyphs',lambda:change('L068',lambda r:next(g for g in r['glyph_substitutions'] if g['input']=='/letter').update(output='✉'*7)))
    reject('visible formfeed erased',lambda:change('L128',lambda r:next(g for g in r['glyph_substitutions'] if g['input']=='\f').update(output='')))
    reject('one envelope truncated to one decoded character',lambda:change('L068',lambda r:next(g for g in r['glyph_substitutions'] if g['input']=='/letter').update(end=next(g for g in r['glyph_substitutions'] if g['input']=='/letter')['start']+1)))
    reject('one encoded envelope mislabeled as separate byte events',lambda:change('L068',lambda r:next(g for g in r['glyph_substitutions'] if g['input']=='/letter')['pdf_events'][1].update(byte_index=999)))
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--author-replay',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
    home=Path(__file__).resolve().parent
    if (home/'manifest.json').exists():
        for row in read(home/'manifest.json')['exports']:
            rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe review export')
            data=(home/rel).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged review export '+str(rel))
    need(not a.out.exists(),'fresh output path');a.out.mkdir(parents=True);a.packet=a.packet.resolve();start=time.monotonic()
    counts=audit(a.packet,a.public_root,a.sources_root);fonts=font_recheck.audit(a.packet,a.public_root,a.sources_root);tests=controls(a.packet,a.public_root,a.sources_root)
    author=None;render=None;copied=None
    if a.author_replay or a.render:
        copied=a.out/'author_packet';copied.mkdir();m=read(a.packet/'manifest.json')
        for r in m['exports']:
            d=copied/r['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.packet/r['path'],d)
        shutil.copy2(a.packet/'manifest.json',copied/'manifest.json')
        need(len([f for f in copied.rglob('*') if f.is_file()])==28,'exact exports plus manifest only')
    def run(cmd,name,cwd=None):
        r=subprocess.run(cmd,capture_output=True,text=True,cwd=cwd);(a.out/(name+'.stdout')).write_text(r.stdout);(a.out/(name+'.stderr')).write_text(r.stderr);need(r.returncode==0,'fresh '+name)
    if a.author_replay:
        run([sys.executable,'-B','-O',str(copied/'check.py'),'--public-root',str(a.public_root),'--sources-root',str(a.sources_root),'--out',str(a.out/'author_replay')],'author')
        author=read(a.out/'author_replay/report.json');need(author['controls_rejected']==36 and author['pdf_metric_cells']==210 and author['raw_metric_cells']==80,'fresh author scope')
    if a.render:
        run([sys.executable,'-B',str(copied/'build_reader.py'),'--out',str(a.out/'reader_render'),'--xelatex',a.xelatex],'reader')
        render=read(a.out/'reader_render/render_report.json')
        old=[pg.extract_text() or '' for pg in pypdf.PdfReader(a.packet/'input_reader.pdf').pages];new=[pg.extract_text() or '' for pg in pypdf.PdfReader(a.out/'reader_render/input_reader.pdf').pages]
        need(old==new and render['diagnostics']==[],'exact reader page text and clean build')
        render['complete_page_text_identical']=True
        ar=a.out/'appendix_render';(ar/'programs').mkdir(parents=True)
        shutil.copy2(copied/'livingstone_additional_program.tex',ar/'livingstone_additional_program.tex')
        shutil.copy2(copied/'programs/phase179_livingstone_check.g',ar/'programs/phase179_livingstone_check.g')
        for n in (1,2):run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','livingstone_additional_program.tex'],'appendix'+str(n),cwd=ar)
        ap=[pg.extract_text() or '' for pg in pypdf.PdfReader(ar/'livingstone_additional_program.pdf').pages]
        op=[pg.extract_text() or '' for pg in pypdf.PdfReader(copied/'livingstone_additional_program.pdf').pages]
        need(ap==op and len(ap)==5,'complete additional program appendix page text')
        log=(ar/'livingstone_additional_program.log').read_text();need(not any(x in log for x in ('Overfull','Missing character','LaTeX Warning:','Package fontspec Warning')),'clean appendix build')
        render['additional_program_appendix']=dict(pages=5,complete_page_text_identical=True,diagnostics=[],page_text_sha256=[sha(t.encode()) for t in ap])
    report=dict(status='PASS',author_manifest_sha256=counts['author_manifest_sha256'],pdf_cells=210,raw_cells=80,text_hashes=58,source_replacement_code_pages=48,font_dictionaries=36,actual_encoded_classes=805,independent_controls=tests,author_replay=author,reader_rebuild=render,export_only_copy=copied is not None,scientific_programs_executed=False,new_credit=0,ratio=None,elapsed_seconds=time.monotonic()-start)
    for name,data in [('recount.json',counts),('font_recheck.json',fonts),('report.json',report)]: (a.out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('PASS 290 coordinates, 58 hashes, 36 dictionaries, 805 classes,',len(tests),'independent controls')
if __name__=='__main__':main()
