"""Replay exact maximal-subgroup bounds; compare the source only after derivation."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not an accepted execution mode')
from pathlib import Path
import argparse,json,hashlib,subprocess,re
from bounds import read_vectors,derive,need

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    here=Path(__file__).resolve().parent
    for r in json.loads((here/'manifest.json').read_text())['exports']:
        b=(here/r['path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'changed export')
    for r in json.loads((here/'dependencies.json').read_text())['bindings']:
        b=Path(r['absolute_path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'changed dependency')
    need(a.out.resolve()!=here and here not in a.out.resolve().parents,'external replay output required');a.out.mkdir(exist_ok=False,parents=True)
    for script,marker in [('maximal_vectors.g','COMPLETE EXACT ORDER VECTORS'),('maximal_controls.g','COMPLETE MAXIMAL UNION CONTROLS')]:
        p=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',str(here/script)],capture_output=True,timeout=60)
        (a.out/(script+'.stdout')).write_bytes(p.stdout);(a.out/(script+'.stderr')).write_bytes(p.stderr)
        need(p.returncode==0 and not p.stderr and p.stdout.decode().count(marker)==1,'GAP execution failed')
        need(p.stdout==(here/(script+'.stdout')).read_bytes(),'fresh character/control output differs')
    result=derive(*read_vectors((a.out/'maximal_vectors.g.stdout').read_text()))
    need(result==json.loads((here/'bounds.json').read_text()),'exact bounds changed')
    source=json.loads((here/'source_table1.json').read_text())['rows']
    need(len(source)==136 and len({(r['p'],r['q'])for r in source})==136,'source row partition')
    source={(r['p'],r['q']):r['source_count'] for r in source}
    need(sum(source.values())==796772,'source total mismatch')
    rows=result['rows'];need(set(source)=={(r['p'],r['q'])for r in rows},'different source types')
    violations=[dict(p=r['p'],q=r['q'],source=source[(r['p'],r['q'])],lower=r['lower'],upper=r['upper']) for r in rows if not r['lower']<=source[(r['p'],r['q'])]<=r['upper']]
    need(violations==[dict(p=20,q=31,source=7246,lower=9118,upper=9118)],'source discrepancy differs')
    need({(r['p'],r['q'])for r in rows if r['lower']>0}=={pq for pq,n in source.items() if n>0},'positive types differ')
    control=(a.out/'maximal_controls.g.stdout').read_text()
    need(re.findall(r'CONTROL (\d+) MAXCLASSES (\d+) TYPES (\d+) PASS',control)==[('6','2','3'),('8','3','3'),('12','2','3'),('24','3','6'),('60','3','6')],'control coverage')
    (a.out/'bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    pages=None
    if a.render:
        from pypdf import PdfReader
        native=a.out/'native';native.mkdir()
        for i in [1,2]:
            r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native.resolve()),'maximal_bounds.tex'],cwd=here,capture_output=True,timeout=60)
            (native/f'build{i}.stdout').write_bytes(r.stdout);(native/f'build{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'native build failed')
        old=PdfReader(here/'maximal_bounds.pdf');new=PdfReader(native/'maximal_bounds.pdf');pages=len(new.pages)
        need(pages==len(old.pages)==4 and [p.extract_text()for p in new.pages]==[p.extract_text()for p in old.pages],'native text differs')
        need('Overfull' not in(native/'maximal_bounds.log').read_text(),'native overflow')
    report=dict(status='PASS_MAXIMAL_UNION_BOUND_AND_SOURCE_CONTRADICTION',rows=136,lower_total=result['lower_total'],source_total=796772,
                exact_rows=20,positive_types=129,source_discrepancies=violations,native_pages=pages,
                original_other_principal_claims_remaining=True,new_question_credit=0,new_Lean_declarations=0,new_measurements=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
