"""Recheck the panel obstruction and retained complete residue receipt."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(p,s):
    if not p:raise ValueError(s)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    if (HERE/'manifest.json').exists():
        for row in json.loads((HERE/'manifest.json').read_text())['exports']:
            p=HERE/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'export binding '+row['path'])
    b=json.loads((HERE/'bindings.json').read_text())
    need(sha(HERE/'prior_representatives.g')==b['prior_representatives']['sha256'],'prior model')
    need(sha(HERE/'shadow_residues.g')==b['retained_engine']['sha256'],'unchanged engine')
    r=json.loads((HERE/'result.json').read_text())
    need(r['member']=='prior_m12.rk3' and r['construction_row']==18 and r['rank']==3,'exact missing input')
    need(r['parabolic_orders']==[24,660,660] and r['borel_order']==6,'parabolic orders')
    need(r['computed_all_ranks'] and r['IP'] and r['WIP'],'full residue property')
    need(r['filters']==dict(IP2=True,RWPRI=True,firm=True,flag_transitive=True,residually_connected=True,twoT1=False),'exact eligibility boundary')
    need(len(r['residues'])==7 and sorted(x['fixed_types'] for x in r['residues'])==[[],[1],[1,2],[1,3],[2],[2,3],[3]],'all base residues')
    e=json.loads((HERE/'execution.json').read_text());need(e['passed'],'complete actual execution')
    for name,item in e['inputs'].items():need((HERE/name).stat().st_size==item['bytes'] and sha(HERE/name)==item['sha256'],'executed input '+name)
    for name in ['prior_representatives.g','panels.g','identify_panel.g','omitted_mathieu_geometry.tex']:shutil.copyfile(HERE/name,a.out/name)
    for name,marker in [('panels.g','PASS_M12_MISSING_PANELS'),('identify_panel.g','PASS_EXACT_A5_DUAD_PANEL')]:
        z=subprocess.run(['/opt/homebrew/bin/gap','-q','-b','-T',name],cwd=a.out,capture_output=True,text=True,timeout=20)
        (a.out/(name+'.stdout')).write_text(z.stdout);(a.out/(name+'.stderr')).write_text(z.stderr)
        need(z.returncode==0 and not z.stderr.strip() and marker in z.stdout,'fresh '+name)
    for _ in range(2):
        z=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','omitted_mathieu_geometry.tex'],cwd=a.out,capture_output=True,text=True,timeout=30)
        need(z.returncode==0,'TeX compilation')
    log=(a.out/'omitted_mathieu_geometry.log').read_text()
    need('Overfull' not in log and 'undefined' not in log,'clean rendered text')
    from pypdf import PdfReader
    p=PdfReader(HERE/'omitted_mathieu_geometry.pdf').pages
    q=PdfReader(a.out/'omitted_mathieu_geometry.pdf').pages
    need(len(p)==len(q)==2,'two pages')
    need([x.extract_text() for x in p]==[x.extract_text() for x in q],'identical page text')
    report=dict(status='PASS_BOUNDED_M12_PANEL_ADDITION',fresh_panel_actions=True,fresh_A5_identification=True,retained_full_shadow_execution=True,full_shadow_execution_repeated=False,proof_pages=2,whole_L096_credit=0,historical_label_identified=False,new_Lean=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
