#!/usr/bin/env python3
"""Portable binding, finite-input, scoped-Lean and render replay for L040.

No primary PDFs or previous manuscripts are distributed. --study-root optionally
checks the exact external editions. This checker is author evidence, not an
independent mathematical acceptance of the new written arguments.
"""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','high-rank-symmetric-markings','program-appendix']
PROGRAMS=['primitive_bound.g','core_attachment.g','local_obstructions.py','boundary_example.g']
ROLES=['required_finite_primitive_inputs','finite_validation','finite_validation','required_only_for_auxiliary_n8_and_validation_of_branching']
PRINCIPAL=['L040.T1.1','L040.T1.2','L040.P3.1','L040.C6.5','L040.T6.6']
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(row,base=ROOT):
    n=Path(row['path']);need(not n.is_absolute() and '..' not in n.parts,'Safe relative binding')
    p=base/n;need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Changed binding '+str(n))
def validate(s):
    need(s['source_ids']==['L040'] and not s['new_title_intake'],'Exact source scope')
    need(s['principal_row_ids']==PRINCIPAL,'Complete five principal targets')
    need(len(s['contracts'])==35 and len({r['id'] for r in s['contracts']})==35,'Complete distinct source rows')
    need([r['id'] for r in s['contracts'] if r['principal']]==PRINCIPAL,'Principal row agreement')
    for b in s['documents']:binding(b)
    need(len(s['proof_spans'])==25,'Complete proof-context map')
    for name,row in s['proof_spans'].items():
        p=ROOT/row['path'];t=p.read_text();a=row['start_codepoint'];b=row['end_codepoint_exclusive']
        need(0<=a<b<=len(t),'Nonempty span '+name)
        need(hashlib.sha256(t[a:b].encode()).hexdigest()==row['sha256_utf8'],'Changed proof span '+name)
    for r in s['contracts']:
        need(r['current_spans'] and all(k in s['proof_spans'] for k in r['current_spans']),'Missing current source disposition')
        need(r['source_physical_pages'] and all(2<=x<=21 for x in r['source_physical_pages']),'Actual source locator')
    rows={r['id']:r for r in s['contracts']}
    for k in ['T1.1','T1.2','P3.1','T6.6']:need(rows['L040.'+k]['status']=='recovered_complete','Complete intended principal contract')
    need(rows['L040.C6.5']['status']=='corrected_complete_general_presentation','No literal false presentation admission')
    need(rows['L040.C6.5.2']['status']=='literal_statement_refuted','Preserve branching correction')
    need(rows['L040.Table1']['status']=='excluded_exact_census_not_claimed','Exact primitive census not recovered')
    need(rows['L040.leaf_count']['status']=='excluded_counting_convention_unfixed','Leaf counting scope')
    need([Path(r['path']).name for r in s['program_inventory']]==PROGRAMS,'Whole four programs')
    need([r['role'] for r in s['program_inventory']]==ROLES,'Distinct finite roles')
    for r in s['program_inventory']:binding(r);need(r['whole_file_printed'],'No pruned program')
    p=s['program_boundary'];need(p['principal_required_programs']==1 and p['complete_mathematical_programs']==4 and p['uniform_proof_validation_programs']==2 and p['auxiliary_source_example_programs']==1,'Exact required/validation boundary')
    need(p['no_finite_sample_promoted_to_uniform_proof'],'No family proof from samples')
    need(p['operational_drivers']==['check.py','formal/check.py'],'Both complete drivers visible')
    binding(s['formal_scope']);f=json.loads((ROOT/'formal/scope.json').read_text())
    need(s['formal_declarations']==8 and sum(len(r['declarations']) for r in f['modules'])==8,'Eight actual declarations')
    need(not s['source_specific_classification_formalized'] and not f['source_specific_claims'],'No full formalization claim')
    for row in f['modules']:binding({'path':'formal/'+row['file'],'bytes':row['bytes'],'sha256':row['sha256']})
    need(len(s['retained_inputs'])==3 and s['retained_inputs'][2]['path'] is None,'Original Whiston access limitation')
    c=s['cost_boundary'];need(c['whole_common_paper_charged_once'] and not c['cross_topic_discount'] and c['all_four_complete_programs_visible'],'Complete common/program boundary')
    for k in ['ratio','retained_classical_proof_cost','source_graphics_cost','required_catalogue_construction_cost']:need(c[k] is None,'No invented unknown cost')
    need(s['new_source_credit']==s['new_question_credit']==0,'No author admission/credit')
    return {'source_rows':35,'principal_targets':5,'proof_contexts':25,'complete_mathematical_programs':4,'Lean_declarations':8}
def controls(s):
    ans=[]
    def reject(n,fn):
        t=copy.deepcopy(s);fn(t)
        try:validate(t)
        except RuntimeError as e:ans.append({'name':n,'rejected':True,'reason':str(e)})
        else:raise RuntimeError('Bad control accepted '+n)
    reject('omit principal target',lambda t:t['principal_row_ids'].pop())
    reject('omit source clause',lambda t:t['contracts'].pop())
    reject('alter written proof',lambda t:t['proof_spans']['U.SimpleKernel'].__setitem__('sha256_utf8','0'*64))
    reject('admit literal branching clause',lambda t:next(r for r in t['contracts'] if r['id']=='L040.C6.5.2').__setitem__('status','recovered_complete'))
    reject('promote exact source census',lambda t:next(r for r in t['contracts'] if r['id']=='L040.Table1').__setitem__('status','recovered_complete'))
    reject('omit complete program',lambda t:t['program_inventory'].pop())
    reject('demote required finite input',lambda t:t['program_inventory'][0].__setitem__('role','finite_validation'))
    reject('promote samples to all n',lambda t:t['program_boundary'].__setitem__('no_finite_sample_promoted_to_uniform_proof',False))
    reject('claim full Lean classification',lambda t:t.__setitem__('source_specific_classification_formalized',True))
    reject('invent external proof cost',lambda t:t['cost_boundary'].__setitem__('retained_classical_proof_cost',0))
    reject('discount another topic umbrella',lambda t:t['cost_boundary'].__setitem__('cross_topic_discount',True))
    return ans
def code_inclusion():
    t=(ROOT/'program-appendix.tex').read_text();names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',t)
    need(names==PROGRAMS,'Every complete program printed once')
    pieces=[]
    for page in PdfReader(ROOT/'program-appendix.pdf').pages:
        def visit(t,cm,tm,font,size):
            if font and 'Menlo' in str(font.get('/BaseFont','')):pieces.append(t)
        page.extract_text(visitor_text=visit)
    norm=lambda t:''.join(c for c in t if not c.isspace())
    expected=norm(''.join((ROOT/'programs'/n).read_text() for n in names))
    need(norm(''.join(pieces))==expected,'Printed program truncation/change')
    return {'files':names,'nonspace_codepoints':len(expected),'only_layout_whitespace_ignored':True}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path)
    ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--xelatex',default=shutil.which('xelatex'))
    ap.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean');ap.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages')
    a=ap.parse_args();need(not os.path.lexists(a.out),'Fresh output path required');out=a.out.resolve();out.mkdir(parents=True)
    s=json.loads((ROOT/'scope.json').read_text());result=validate(s);result['integrity_controls']=controls(s);result['complete_code']=code_inclusion()
    if (ROOT/'manifest.json').is_file():
        for r in json.loads((ROOT/'manifest.json').read_text())['exports']:binding(r)
        result['manifest_sha256']=sha(ROOT/'manifest.json')
    ext=[]
    if a.study_root:
        for r in [s['primary'],s['comparison_edition']]+s['retained_inputs']:
            if r['path'] is not None:binding(r,a.study_root);ext.append(r['path'])
        need(len(PdfReader(a.study_root/s['primary']['path']).pages)==21,'Accepted source edition pages')
    result['external_bindings_checked']=ext
    def run(name,cmd):
        start=time.monotonic();p=subprocess.run(list(map(str,cmd)),cwd=out,capture_output=True,text=True,timeout=1800)
        (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr)
        need(p.returncode==0,'Failed process '+name)
        return p,round(time.monotonic()-start,3)
    if a.programs:
        need(a.gap,'GAP executable required');runs=[]
        for n,markers in [
          ('primitive_bound.g',['PRIMITIVE_CATALOGUE 154','AFFINE16_BOUND 7','M11_MAXIMAL_ORDERS','MAROTI_INTEGER_ENVELOPE 26..63 PASS','PASS primitive block-stabilizer identifications and independent bounds']),
          ('core_attachment.g',['A: PASS finite core checks=52','B: PASS finite core checks=52','C: PASS finite core checks=52']),
          ('boundary_example.g',['BOUNDARY_N8 group40320 IP4096 flag_products156 transitive_parabolic1344 PASS','BRANCHING_LITERAL_CORRECTION two_bridge_neighbours_order3 PASS'])]:
            p,sec=run(n,[a.gap,'-q','-T',ROOT/'programs'/n]);need(not re.search(r'Error|warning',p.stdout+p.stderr,re.I),'GAP diagnostic '+n)
            need(all(m in p.stdout for m in markers),'Incomplete finite output '+n);runs.append({'file':n,'seconds':sec,'sha256':sha(ROOT/'programs'/n),'markers':markers})
        p,sec=run('local_obstructions',[sys.executable,'-B','-O',ROOT/'programs/local_obstructions.py','--out',out/'local_obstructions'])
        q=json.loads((out/'local_obstructions/report.json').read_text());need(q['status']=='PASS' and q['cases']==18 and len(q['controls'])==5,'Complete local diagnostics')
        runs.append({'file':'local_obstructions.py','seconds':sec,'cases':18,'semantic_controls':5,'sha256':sha(ROOT/'programs/local_obstructions.py')})
        result['programs']=runs
    if a.formal:
        run('formal',[sys.executable,'-B','-O',ROOT/'formal/check.py','--out',out/'formal','--lean',a.lean,'--packages',a.packages])
        f=json.loads((out/'formal/report.json').read_text());need(f['status']=='PASS' and sum(len(x['axioms']) for x in f['modules'])==8 and len(f['countermodels'])==6,'Exact formal result')
        result['formal']={'declarations':8,'hypothesis_countermodels':6,'scope':'generic normalization only','report_sha256':sha(out/'formal/report.json')}
    if a.render:
        need(a.xelatex,'XeLaTeX required');stage=out/'render';stage.mkdir()
        for r in s['documents']:
            if r['path'].endswith('.tex'):
                p=stage/r['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/r['path'],p)
        shutil.copytree(ROOT/'programs',stage/'programs');rs=[]
        for n in DOCS:
            for _ in range(2):
                p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',n+'.tex'],cwd=stage,capture_output=True,text=True)
                need(p.returncode==0,'Render failed '+n)
            log=(stage/(n+'.log')).read_text();need(not any(k in log for k in ['LaTeX Warning','Package hyperref Warning','Missing character','Overfull']),'Render diagnostics '+n)
            old=PdfReader(ROOT/(n+'.pdf'));new=PdfReader(stage/(n+'.pdf'));need(len(old.pages)==len(new.pages),'Render page count '+n)
            need(all(x.extract_text()==y.extract_text() for x,y in zip(old.pages,new.pages)),'Per-page extracted text mismatch '+n)
            rs.append({'document':n,'pages':len(old.pages),'per_page_text_identical':True,'diagnostics':[]})
        result['render']=rs
    result.update(status='PASS',independent_mathematical_review=False,new_source_credit=0,new_question_credit=0,ratio=None)
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','rows':35,'controls':len(result['integrity_controls']),'out':str(out)}))
if __name__=='__main__':main()
