#!/usr/bin/env python3
"""Distinct structural and quotient-model review; imports no author code."""
import argparse, hashlib, json, pathlib, re, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
PIN = '7f2507f6f093aeb456396ba210407e14717d402b8d3e393a24957ebfcb093d65'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def need(t, s):
    if not t: raise RuntimeError('DIAGONAL_REVIEW_REJECT ' + s)
def main():
    ap=argparse.ArgumentParser()
    for n in ['author','gap','out']:ap.add_argument('--'+n,type=pathlib.Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
    m=a.author/'manifest.json';need(sha(m)==PIN,'exact author edition')
    exports=json.loads(m.read_text())['exports']
    for row in exports:
        p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
        q=a.author/p;need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'binding '+str(p))
    ledger=json.loads((a.author/'source_clause_map.json').read_text())
    need(len(ledger['rows'])==32 and len(ledger['proof_spans'])==13,'full clauses and spans')
    need(ledger['rows'][30]['status']=='open_general_question_not_claimed_solved','open question retained')
    for span in ledger['proof_spans'].values():
        b=b''.join((a.author/span['path']).read_bytes().splitlines(keepends=True)[span['start_line']-1:span['end_line']])
        need(len(b)==span['bytes'] and hashlib.sha256(b).hexdigest()==span['sha256'],'exact span')
    review=json.loads((ROOT/'review.json').read_text())
    need(review['author_manifest_sha256']==PIN and review['new_question_credit']==0 and
         review['N006_whole_original_credit']==0 and not review['whole_geometry_formalized'],'scope')
    r=subprocess.run([str(a.gap),'-q','-T',str(ROOT/'quotient_kernel.g')],text=True,capture_output=True,timeout=60)
    (a.out/'quotient.stdout').write_text(r.stdout);(a.out/'quotient.stderr').write_text(r.stderr)
    need(r.returncode==0 and 'UNFAITHFUL_QUOTIENT_CHECK PASS order96 kernel2 faithful48 chambers48' in r.stdout and
         not re.search('Error|warning',r.stdout+r.stderr,re.I),'quotient model')
    s=(ROOT/'quotient_kernel.g').read_text();need(s.count('chambers=48 and full=48')==1,'unique model control')
    bad=a.out/'wrong_chambers.g';bad.write_text(s.replace('chambers=48 and full=48','chambers=24 and full=24'))
    r=subprocess.run([str(a.gap),'-q','-T',str(bad)],text=True,capture_output=True,timeout=60)
    (a.out/'control.stdout').write_text(r.stdout);(a.out/'control.stderr').write_text(r.stderr)
    need('Error' in r.stdout+r.stderr and 'UNFAITHFUL_QUOTIENT_CHECK PASS' not in r.stdout,'negative control')
    result={'status':'PASS','author_exports':len(exports),'source_clauses':32,'proof_spans':13,
            'independent_quotient_model':{'raw_group':96,'kernel':2,'faithful_group':48,'chambers':48},
            'controls_rejected':['wrong_chamber_count'],'new_question_credit':0,
            'N006_whole_original_credit':0,'compression_factor':None}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
