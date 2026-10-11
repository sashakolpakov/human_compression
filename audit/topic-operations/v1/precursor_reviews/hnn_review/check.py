#!/usr/bin/env python3
"""Replay exact reviewed inputs, finite diagnostics and limited scope controls."""
from pathlib import Path
import argparse,hashlib,json,copy
from pypdf import PdfReader
from finite_checks import need,run
HERE=Path(__file__).resolve().parent

def validate(review,study):
    need(review['status']=='ACCEPTED_BOUNDED_MATHEMATICAL_REVIEW','accepted exact scope')
    need(review['new_recovered_originals']==review['new_question_credit']==review['formal_declarations']==0 and review['compression_factor'] is None,'no unsupported credit')
    need(not review['open_findings'] and not review['required_repairs'],'no unresolved finding')
    need([x['id'] for x in review['accepted']]==['H1','H2','H3','H4','G1'],'all five accepted results')
    need('explicit indexed compatibility' in review['source_routes'][0]['disposition'],'indexed source qualification')
    need('does not disprove existence' in review['source_routes'][1]['disposition'],'broad question remains separate')
    for r in review['bindings']:
        b=(study/r['path']).read_bytes()
        need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'bound exact input '+r['path'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output')
    r=json.loads((HERE/'review.json').read_text());validate(r,a.study_root)
    f=run();need(f==json.loads((HERE/'finite_result.json').read_text()),'fresh finite diagnostics')
    v=json.loads((HERE/'render_review.json').read_text());need(v['all_five_pages_visually_read'] and not v['visual_review_pending'],'recorded full visual reading')
    pages=0
    for row in v['records']:
        path=HERE/'render'/(row['name']+'.pdf');b=path.read_bytes()
        need(hashlib.sha256(b).hexdigest()==row['pdf_sha256'],'exact rendered PDF')
        texts=[p.extract_text()or'' for p in PdfReader(path).pages]
        need(len(texts)==row['pages'] and [hashlib.sha256(t.encode()).hexdigest() for t in texts]==row['page_text_sha256'],'reviewed page texts')
        need(not row['diagnostics'],'clean compile');pages+=len(texts)
    controls=[]
    for name,edit in [
        ('changed scientific binding',lambda d:d['bindings'][0].update(sha256='0'*64)),
        ('unsupported question credit',lambda d:d.update(new_question_credit=1)),
        ('drop indexed compatibility qualification',lambda d:d['source_routes'][0].update(disposition='all cases')),
        ('claim broad fundamental-geometry impossibility',lambda d:d['source_routes'][1].update(disposition='all cases impossible'))]:
        d=copy.deepcopy(r);edit(d)
        try:validate(d,a.study_root)
        except ValueError:controls.append(name)
        else:raise ValueError('control survived: '+name)
    if (HERE/'manifest.json').exists():
        for row in json.loads((HERE/'manifest.json').read_text())['exports']:
            b=(HERE/row['path']).read_bytes()
            need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'frozen review export '+row['path'])
    result=dict(status='PASS',reviewed_inputs=len(r['bindings']),accepted_results=len(r['accepted']),reviewed_pages=pages,finite_quotient_cases=f['finite_quotient_cases'],all_parabolic_generation_checks=f['all_parabolic_generation_checks'],nonstar_panel_checks=f['nonstar_panel_checks'],mathematical_weakening_controls=f['rejected_controls'],integrity_and_scope_controls=controls,uniform_written_proof_machine_verified=False,complete_N005_credit=False)
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
