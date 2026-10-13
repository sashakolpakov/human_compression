#!/usr/bin/env python3
"""Verify the exact mathematical review boundary without rerunning old searches."""
from pathlib import Path
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parent
PIN='632a6185c1caa1efff0bc430aae483781261ef7777764fe4e663bda0f8546deb'

def need(c,m):
    if not c:raise ValueError(m)

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())

def main():
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(h(a.author/'manifest.json')==PIN,'exact author pin')
    total=0
    for b in load(a.author/'manifest.json')['exports']:
        f=a.author/b['path'];need(f.stat().st_size==b['bytes'] and h(f)==b['sha256'],'complete author export');total+=1
    for b in load(ROOT/'manifest.json')['exports']:
        f=ROOT/b['path'];need(f.stat().st_size==b['bytes'] and h(f)==b['sha256'],'review export')
    review=load(ROOT/'review.json');need(review['status']=='ACCEPTED_BOUNDED_DN_THEOREMS','bounded review')
    need(review['mathematical_author']=='root' and review['reviewer']=='enumeration_volume','distinct mathematics roles')
    need(review['packager']=='enumeration_volume' and not review['claims_independent_packaging_review'],'packager disclosure')
    need(review['whole_original_credit']==0 and review['new_factor'] is None,'limits')
    for b in load(ROOT/'scientific_bindings.json'):
        f=a.author/b['path'];need(h(f)==b['sha256'] and f.stat().st_size==b['bytes'],'reviewed scientific bytes')
    replay=load(ROOT/'copied_author_replay.json');need(replay['exports']==246 and replay['complete_public_copies']==228,'full copy boundary')
    need(replay['old_finite_searches_repeated']==0 and replay['Lean_repeated']==0,'no repeated computations')
    need([x['pages'] for x in replay['native_documents']]==[2,3] and all(x['exact_page_text'] for x in replay['native_documents']),'complete native texts')
    report={'status':'PASS_DISTINCT_MATHEMATICAL_REVIEW_BINDING','author_exports':total,'bounded_source_routes':20,'pages_viewed':5,'fresh_science_computations':0,'whole_original_credit':0}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
