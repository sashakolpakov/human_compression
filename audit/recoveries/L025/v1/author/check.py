"""Portable author replay. Operational integrity is separate from mathematics."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_binding(root,row):
    p=root/row['path']
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'binding '+str(p))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--study-root',type=Path);parser.add_argument('--render',action='store_true')
    parser.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');args=parser.parse_args()
    need(not args.out.exists(),'fresh output directory');args.out.mkdir(parents=True)
    manifest=json.loads((HERE/'manifest.json').read_text())
    for row in manifest['exports']:check_binding(HERE,row)
    for folder in ['retained/common','retained/odd_cycle']:
        inner=json.loads((HERE/folder/'manifest.json').read_text())
        for row in inner['exports']:check_binding(HERE/folder,row)
    scope=json.loads((HERE/'scope.json').read_text());roles=json.loads((HERE/'program_roles.json').read_text())
    source_map=json.loads((HERE/'source_map.json').read_text());deps=json.loads((HERE/'dependencies.json').read_text())
    need(scope['new_original_credit']==scope['new_question_credit']==scope['new_Lean_declarations']==0,'no author credit')
    need(scope['numerical_factor'] is None and roles['software_inclusive_ratio'] is None,'unmeasured scope')
    need(not scope['whole_original_formalized'] and not roles['formal_rerun'],'partial retained formal scope')
    need(len(source_map['rows'])==41 and len({r['id'] for r in source_map['rows']})==41,'complete source map')
    need(not scope['principal_obligations_remaining'],'author principal completion')
    for id in ['T4.3_unrestricted_even','S2.3_identification','Appendix','C3.2','C4.5','C4.6']:
        need(sum(r['id']==id for r in source_map['rows'])==1,'critical source disposition '+id)
    source_bindings=0
    if args.study_root:
        for row in deps['private_primary_sources']:check_binding(args.study_root,row);source_bindings+=1
        # Source-row transcription check is available privately; the portable
        # packet exposes only mathematical adjacency, never the full source.
        txt=(args.study_root/'sources/catalogue_L025.txt').read_text()
        body=txt.split('gr:=Graph<32|',1)[1].split(']>;',1)[0]
        rows=re.findall(r'\{([^}]+)\}',body)
        literal=[sorted(int(v)-1 for v in re.findall(r'\d+',row)) for row in rows]
        need(literal==json.loads((HERE/'finite/inputs/source_G.json').read_text()),'literal source adjacency')
    run=subprocess.run([sys.executable,'-B','-O',str(HERE/'finite/verify.py'),'--out',str(args.out/'finite.json')],capture_output=True,text=True,check=True)
    need(json.loads((args.out/'finite.json').read_text())==json.loads((HERE/'reports/finite.json').read_text()),'fresh complete finite replay')
    renders=[]
    if args.render:
        from pypdf import PdfReader
        for relative,expected in [('cycles_in_incidence_graphs.tex',7),('retained/common/cages_and_planes.tex',5),('retained/odd_cycle/odd_cycle_bound.tex',3)]:
            original=HERE/relative;work=args.out/original.stem;work.mkdir();shutil.copy2(original,work/original.name)
            for i in range(2):
                r=subprocess.run([args.pdflatex,'-halt-on-error','-interaction=nonstopmode',original.name],cwd=work,capture_output=True,text=True)
                (work/f'build{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'native TeX '+relative)
            log=(work/(original.stem+'.log')).read_text()
            need(not any(x in log for x in ['Overfull','Undefined control sequence','LaTeX Warning:']),'clean TeX '+relative)
            a=PdfReader(original.with_suffix('.pdf'));b=PdfReader(work/(original.stem+'.pdf'))
            need(len(a.pages)==len(b.pages)==expected,'native page count '+relative)
            need(all(x.extract_text()==y.extract_text() for x,y in zip(a.pages,b.pages)),'exact native page text '+relative)
            renders.append(dict(path=relative,pages=expected))
    report=dict(status='PASS_COMPLETE_PRINCIPAL_AUTHOR_REPLAY',exports=len(manifest['exports']),source_dispositions=41,
                private_sources_checked=source_bindings,finite_graphs=6,uncached_full_automorphism_orders=6,
                native_renders=renders,external_censuses_rerun=False,Lean_rerun=False,distinct_scientific_review=False,
                original_credit=0,numerical_factor=None)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
