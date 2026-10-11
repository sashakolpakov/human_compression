#!/usr/bin/env python3
"""Independent G input review: requires the separately retained primary PDFs."""
import argparse,copy,json,pathlib
from recount import run as recount,read,sha,need
from boundary import run as boundary
from font_reconcile import compare,classify,controls
PIN='c46e1742d44138d9a63af86ae2ee9dd9d1498d0b4ca0d75cf1fd19a022af978d'
OLD='79ee51fdfcd4eb9526015863af2abc588fd257d6eed8dcecc4b96a79ebc8173b'
def packet_check(p,pin):
    need(sha((p/'manifest.json').read_bytes())==pin,'manifest pin')
    m=read(p/'manifest.json')
    for r in m['exports']:
        q=pathlib.PurePosixPath(r['path']);need(not q.is_absolute() and '..' not in q.parts,'relative export')
        b=(p/q).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen export '+r['path'])
    return len(m['exports'])
def run(study,packet,old,public):
    n=packet_check(packet,PIN);no=packet_check(old,OLD)
    b=boundary(study,packet,public);r=recount(study,packet);fa=read(packet/'font_audit.json')
    compare(r['font_audit'],fa);classification=classify(r['font_audit']);fc=controls(r['font_audit'],fa)
    correction=read(packet/'font_identity_correction.json');need(r['font_audit']['L009']['cache_repair_occurrences']==correction['corrected_occurrences'],'all701 actual correction events')
    before=read(old/'author_counts.json');after=read(packet/'author_counts.json')
    sections=['documents','identification_cover_sensitivity','complete_programs','complete_operational_drivers','complete_formal_files','appendix']
    need(all(before[k]==after[k] for k in sections),'all counts/text hashes/cover/code unchanged')
    s1=read(old/'source_input_spec.json');s2=read(packet/'source_input_spec.json')
    for k in ['L009','L092']:
        a=copy.deepcopy(s1['sources'][k]);v=copy.deepcopy(s2['sources'][k])
        for row in a['glyph_substitutions']:row.pop('pdf_event')
        for row in v['glyph_substitutions']:row.pop('pdf_event')
        need(a==v,'only event metadata changed in selected source inputs')
    need(len(classification)==1209 and len(correction['corrected_occurrences'])==701,'full glyph/repair census')
    raw=(study/'sources/older_L092_gwdg.pdf').read_bytes()
    need(b'/F18 9 0 R /F18 9 0 R' in raw and b'/F27 27 0 R /F25 30 0 R /F27 27 0 R' in raw,'literal benign duplicate keys')
    need(r['font_audit']['L009']['nonspace_characters']+r['font_audit']['L092']['nonspace_characters']==75909,'all source nonspace chars')
    need(len(fc)==6 and len(b['controls'])==15,'independent controls')
    r.update(status='PASS_INDEPENDENT_TOPIC_G_INPUT_REVIEW',author_exports=n,preserved_original_exports=no,boundary=b,font_classifications=classification,independent_controls=b['controls']+fc,font_correction=dict(used_classes=1209,changed_old_classes=9,changed_events=701,calibrations_unchanged=509,all_counts_and_normalized_hashes_unchanged=True),font_parser_trust='Pinned pypdf/fontTools; independent event traversal and dictionary-keyed mapping, not an independent font interpreter. Full outlines and source pages inspected separately.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,factors=None)
    return r
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--study-root',type=pathlib.Path,required=True);a.add_argument('--packet',type=pathlib.Path);a.add_argument('--original',type=pathlib.Path);a.add_argument('--public-root',type=pathlib.Path,required=True);a.add_argument('--out',type=pathlib.Path,required=True);v=a.parse_args();need(not v.out.exists() and not v.out.is_symlink(),'fresh output path');p=v.packet or v.study_root/'topic_G_measurement_inputs_v2';old=v.original or v.study_root/'topic_G_measurement_inputs';r=run(v.study_root,p,old,v.public_root);v.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:r[k] for k in ['status','author_exports','preserved_original_exports','pdf_metric_cells','raw_metric_cells','font_correction','factors']}))
