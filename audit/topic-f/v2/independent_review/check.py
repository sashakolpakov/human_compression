#!/usr/bin/env python3
"""Verify this frozen review and its exact accepted author packet; no new theorem claim."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR='28a30b8eadef055a7cd00be44b7696b016538eae9931eaf8238de4b556bbc835'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(base,rows):
    for row in rows:
        path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'safe export path')
        p=base/path;need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'changed '+str(p))
def main():
    p=argparse.ArgumentParser();p.add_argument('--author-root',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.author_root/'manifest.json')==AUTHOR,'wrong author edition');author=json.loads((a.author_root/'manifest.json').read_text());verify(a.author_root,author['exports'])
    review=json.loads((ROOT/'manifest.json').read_text());verify(ROOT,review['exports'])
    scope=json.loads((a.author_root/'scope.json').read_text());rows=json.loads((ROOT/'source_rows.json').read_text())['rows']
    need([x['id'] for x in rows]==scope['inherited_row_ids'],'exact reviewed clauses')
    replay=json.loads((ROOT/'fresh_replay/report.json').read_text());lattice=json.loads((ROOT/'lattice_result.json').read_text())
    need(replay['status']=='PASS' and replay['source_rows']==25 and replay['formal']['distinct_declarations']==5,'replay scope')
    need(lattice['status']=='PASS' and lattice['count']==40,'independent bounded lattice scope')
    if a.study_root:
        s=scope['source']['primary'];source=a.study_root/s['path'];need(source.stat().st_size==s['bytes'] and sha(source)==s['sha256'],'primary edition')
    result={'status':'PASS','author_exports':len(author['exports']),'review_exports':len(review['exports']),'reviewed_source_rows':25,'independent_lattice_cases':40,'distinct_formal_declarations':5,'scope':'Frozen review/evidence binding only. Full computations and renders use the author portable replay; full quantified proofs were independently read.','new_source_credit':0,'new_question_credit':0,'ratio':None}
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
