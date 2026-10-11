#!/usr/bin/env python3
"""Check canonical Topic F bindings; optionally replay validation, Lean and TeX.

This author checker is not an independent mathematical review. The three
complete mathematical programs validate bounded cases only. Historical source
PDFs and proof packets remain external optional byte-verification inputs.
"""
import argparse, copy, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','odd-kernel-polyhedra','program-appendix']
PROGRAMS=['phase236_models.py','phase236_finite_check.g','phase248_presentation_check.g']
DRIVERS=['phase236_check.py','phase248_check.py']
LEAN_DEFAULT='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'
PACKAGES_DEFAULT='/Users/sasha/bogachev/formal/.lake/packages'

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def local(name):
    p=(ROOT/name).resolve();need(p.is_relative_to(ROOT),'Local path escapes packet');return p
def binding(row,base=ROOT):
    path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'Safe binding path')
    p=base/path;need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Changed binding '+str(path))

def validate(s):
    need(s['source_ids']==['L014'] and s['intake_closed'],'Exact closed source')
    need(len(s['contracts'])==25 and [r['id'] for r in s['contracts']]==s['inherited_row_ids'],'Exact 25 inherited clauses')
    for row in s['documents']:binding(row)
    for name,row in s['proof_spans'].items():
        t=local(row['path']).read_text();a,b=row['start_codepoint'],row['end_codepoint_exclusive']
        need(0<=a<b<=len(t),'Nonempty proof span')
        need(hashlib.sha256(t[a:b].encode()).hexdigest()==row['sha256_utf8'],'Changed proof span '+name)
    for row in s['contracts']:
        need(row['inherited_record']['id']==row['id'],'Inherited source identity')
        need(row['current_spans'] and all(k in s['proof_spans'] for k in row['current_spans']),'Missing current scope/proof span')
    rows={r['id']:r for r in s['contracts']}
    need(rows['L014.T1.2.defect']['status']=='literal_preprint_marking_corrected','Lost marking correction')
    for n in ['excluded.census','excluded.classification']:
        need(rows[n]['status']=='excluded_not_recovered' and rows[n]['current_spans']==['F1.Scope'],'Lost exclusion')
    need(s['retained_remote_primary']['local_pdf'] is None and s['retained_remote_primary']['full_text_cost'] is None,'Invented CP PDF/cost')
    need(s['retained_remote_primary']['not_reproved'],'Retained CP theorem falsely discharged')
    need([r['original'] for r in s['program_inventory']]==PROGRAMS+DRIVERS,'Complete program/driver list')
    for row in s['program_inventory']:
        binding({'path':row['copy'],'bytes':row['bytes'],'sha256':row['sha256']})
        need(row['role']==('finite_validation' if row['original'] in PROGRAMS else 'historical_operational_driver'),'Wrong program role')
    need(s['validation_boundary']['full_mathematical_programs']==3 and s['validation_boundary']['complete_drivers']==2,'Complete validation boundary')
    need(s['validation_boundary']['uniform_written_proof_depends_on_finite_results'] is False,'Finite samples promoted to uniform proof')
    binding(s['formal_scope'])
    f=json.loads(local('formal/scope.json').read_text())
    need(len(f['modules'])==1 and len(f['modules'][0]['declarations'])==5 and f['new_declarations']==0,'Exact reused formal inventory')
    for row in f['modules']:binding({'path':'formal/'+row['file'],'bytes':row['bytes'],'sha256':row['sha256']})
    need(not f['source_specific_claims'] and len(f['not_formalized'])==6,'Source-specific formal overclaim')
    need(s['cost_boundary']['full_common_paper_charged_once'] and not s['cost_boundary']['cross_topic_discount'],'Whole common paper charged')
    for key in ['ratio','external_proof_cost','source_graphics_cost']:need(s['cost_boundary'][key] is None,'Invented cost')
    need(s['new_source_credit']==s['new_question_credit']==0,'No new credit')
    return {'source_rows':25,'proof_spans':len(s['proof_spans']),'mathematical_programs':3,'drivers':2,'scoped_Lean_declarations':5}

def code_inclusion():
    t=local('program-appendix.tex').read_text()
    names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',t)
    need(names==PROGRAMS,'Three entire printed programs in declared order')
    parts=[]
    for page in PdfReader(local('program-appendix.pdf')).pages:
        def visit(t,cm,tm,font,size):
            if font and 'Menlo' in str(font.get('/BaseFont','')):parts.append(t)
        page.extract_text(visitor_text=visit)
    norm=lambda s:''.join(c for c in s if not c.isspace())
    source=norm(''.join(local('programs/'+n).read_text() for n in names))
    need(source==norm(''.join(parts)),'Printed code omission or alteration')
    return {'complete_files':names,'nonspace_code_characters':len(source),'layout_whitespace_ignored_only_in_inclusion_test':True}

def controls(s):
    ans=[]
    def reject(name,change):
        x=copy.deepcopy(s);change(x)
        try:validate(x)
        except RuntimeError as exc:ans.append({'name':name,'rejected':True,'reason':str(exc)})
        else:raise RuntimeError('Control accepted '+name)
    reject('omit inherited row',lambda x:x['contracts'].pop())
    reject('alter bound proof span',lambda x:x['proof_spans']['UF.Lattice'].__setitem__('sha256_utf8','0'*64))
    reject('erase literal correction',lambda x:next(r for r in x['contracts'] if r['id']=='L014.T1.2.defect').__setitem__('status','proved_literal'))
    reject('claim excluded census',lambda x:next(r for r in x['contracts'] if r['id']=='excluded.census').__setitem__('status','proved'))
    reject('invent retained PDF cost',lambda x:x['retained_remote_primary'].__setitem__('full_text_cost',0))
    reject('drop a validation program',lambda x:x['program_inventory'].pop(0))
    reject('promote examples to all parameters',lambda x:x['validation_boundary'].__setitem__('uniform_written_proof_depends_on_finite_results',True))
    reject('discount common theory',lambda x:x['cost_boundary'].__setitem__('cross_topic_discount',True))
    return ans

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path)
    ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--xelatex',default=shutil.which('xelatex'))
    ap.add_argument('--lean',default=LEAN_DEFAULT);ap.add_argument('--packages',default=PACKAGES_DEFAULT)
    a=ap.parse_args();need(not os.path.lexists(a.out),'Fresh output required');out=a.out.resolve();out.mkdir(parents=True)
    s=json.loads(local('scope.json').read_text());res=validate(s);res['integrity_controls']=controls(s);res['code_inclusion']=code_inclusion()
    if local('manifest.json').is_file():
        for row in json.loads(local('manifest.json').read_text())['exports']:binding(row)
        res['manifest_sha256']=sha(local('manifest.json'))
    external=[]
    for ns,base in [('study',a.study_root),('public',a.public_root)]:
        if base:
            for row in s['predecessors']:
                if row['namespace']==ns:binding(row,base);external.append(row['path'])
    if a.study_root:
        binding(s['source']['primary'],a.study_root)
        need(len(PdfReader(a.study_root/s['source']['primary']['path']).pages)==12,'Primary edition pages')
        prior=json.loads((a.study_root/'phase236_source_ledger.json').read_text())['rows']
        need(prior==[r['inherited_record'] for r in s['contracts']],'Exact inherited 25 records')
        external.append(s['source']['primary']['path'])
    res['external_bindings_checked']=external
    def run(name,cmd):
        p=subprocess.run(list(map(str,cmd)),cwd=out,text=True,capture_output=True,timeout=1800)
        (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr)
        need(p.returncode==0,'Replay failed '+name);return p
    if a.programs:
        need(a.gap,'GAP executable required')
        stage=out/'legacy_stage';stage.mkdir();(stage/'formal').mkdir();(stage/'phase236_formal').mkdir()
        for n in PROGRAMS[:2]:shutil.copyfile(local('programs/'+n),stage/n)
        shutil.copyfile(local('drivers/phase236_check.py'),stage/'phase236_check.py')
        shutil.copyfile(local('formal/OddKernelIntersection.lean'),stage/'phase236_formal/OddKernelIntersection.lean')
        shutil.copyfile(local('formal/dependency_manifest.json'),stage/'formal/dependency_manifest.json')
        run('validation236',[sys.executable,'-B','-O',stage/'phase236_check.py','--out',out/'validation236','--gap',a.gap,'--lean',a.lean,'--packages',a.packages])
        report=json.loads((out/'validation236/report.json').read_text())
        need(report['status']=='PASS' and len(report['cyclotomic_parameters'])==7 and len(report['abelian_parameters'])==4 and len(report['axiom_reports'])==5,'Legacy exact scope')
        p=run('presentation248',[a.gap,'-q','-T',local('programs/phase248_presentation_check.g')])
        need('PHASE248_PRESENTATION_PASS' in p.stdout and not re.search(r'Error|warning',p.stdout+p.stderr),'Literal presentation replay')
        params=[list(map(int,z)) for z in re.findall(r'^LITERAL_PRESENTATION (\d+) (\d+) ORDER (\d+)',p.stdout,re.M)]
        need(params==[[3,3,27],[3,6,729],[5,3,125],[5,5,3125],[11,3,1331]],'Five exact literal presentations')
        need(p.stdout.count('IP64 PASS')==5 and 'COMPOSITE_INDEX_FALSE_WEAKENING_REJECTED' in p.stdout,'Full finite IP and prime-index control')
        res['finite_validation']={'cyclotomic_models':7,'abelian_models':4,'source_presentations':params,'subset_intersections_per_model':64,'semantic_rejections':4,'uniform_proof':False}
        res['legacy_formal_replay_declarations']=5
    if a.formal:
        run('scoped_formal',[sys.executable,'-B','-O',local('formal/check.py'),'--out',out/'formal','--lean',a.lean,'--packages',a.packages])
        f=json.loads((out/'formal/report.json').read_text());need(sum(len(x['axioms']) for x in f['modules'])==5,'Five unchanged declarations')
        res['formal']={'distinct_declarations':5,'countermodels':2,'same_five_as_legacy_driver':True,'not_added_twice':True}
    if a.render:
        need(a.xelatex,'XeLaTeX required');render=out/'render';render.mkdir()
        for row in s['documents']:
            if row['path'].endswith('.tex'):
                p=render/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local(row['path']),p)
        shutil.copytree(local('programs'),render/'programs');rs=[]
        for n in DOCS:
            for i in range(2):
                p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',n+'.tex'],cwd=render,capture_output=True,text=True)
                need(p.returncode==0,'TeX failure '+n)
            log=(render/(n+'.log')).read_text();need(not any(x in log for x in ['Overfull','Missing character','LaTeX Warning','Package hyperref Warning']),'Render diagnostic '+n)
            old=PdfReader(local(n+'.pdf'));new=PdfReader(render/(n+'.pdf'))
            need(len(old.pages)==len(new.pages) and all(x.extract_text()==y.extract_text() for x,y in zip(old.pages,new.pages)),'Per-page render mismatch '+n)
            rs.append({'document':n,'pages':len(old.pages),'per_page_text_identical':True,'diagnostics':[]})
        res['render']=rs
    res.update(status='PASS',independent_mathematical_review=False,new_source_credit=0,new_question_credit=0,ratio=None)
    (out/'report.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({'status':'PASS','source_rows':25,'controls':len(res['integrity_controls']),'out':str(out)}))
if __name__=='__main__':main()
