#!/usr/bin/env python3
"""Portable binding, full bounded validation, formal and rendering checks.
This author replay is not an independent review or an all-groups finite proof.
"""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','finite-normal-pairs','program-appendix']
PROGRAMS=['phase177_hexagon_check.g','phase188_gadget_check.g']
DRIVERS=['phase188_verify.py','phase193_public_check.py']
BASELINE='a280f9903d130e36914923aeb0c2492103d876c2a6585ea1e48addfedb8aa8c1'
LEAN='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'
PACKAGES='/Users/sasha/bogachev/formal/.lake/packages'
def need(x,s):
    if not x:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def local(p):
    path=(ROOT/p).resolve();need(path.is_relative_to(ROOT),'safe local path');return path
def binding(row,base=ROOT):
    p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe binding path')
    p=base/p;need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'bound bytes '+str(p))
def validate(s):
    need(sha(local('baseline_contract.json'))==BASELINE,'unchanged accepted source contract')
    old=json.loads(local('baseline_contract.json').read_text())
    need(s['source_ids']==['F010'] and s['intake_closed'],'closed source')
    need(s['source']['authors']==['Antonio Díaz Ramos','Rémi Molinier','Antonio Viruel'],'original authors')
    need([r['inherited_record'] for r in s['contracts']]==old['principal_blocks'],'all six inherited source blocks')
    need(s['inherited_source_block_order']==[r['source'] for r in old['principal_blocks']],'source block ordering')
    for row in s['documents']:binding(row)
    for k,r in s['proof_spans'].items():
        t=local(r['path']).read_text();a,b=r['start_codepoint'],r['end_codepoint_exclusive']
        need(0<=a<b<=len(t) and hashlib.sha256(t[a:b].encode()).hexdigest()==r['sha256_utf8'],'complete proof context '+k)
    for row in s['contracts']:
        need(row['current_spans'] and all(k in s['proof_spans'] for k in row['current_spans']),'every inherited block has actual current proofs')
    by={r['id']:r for r in s['contracts']}
    need(by['F010.Example5.1']['status']=='corrected_example','hexagon correction')
    need(by['F010.Example5.2']['status']=='qualified_base_case','recursive base qualification')
    hyp=s['precise_hypotheses'];need(hyp['normal_subgroup_required'] and hyp['finite'] and not hyp['rank_two_universal_claim'],'finite normal pairs, not arbitrary rank-two pairs')
    need(hyp['main_nontrivial_rank']=='[G:H]+3' and hyp['trivial_rank']==1 and hyp['arbitrary_input_cleaning_need_not_be_connected'],'exact rank and component limits')
    need(len(s['source_qualifications'])==3 and len(s['exclusions'])==5 and s['no_whole_assertion_equivalence_claim'],'source qualifications and exclusions')
    need([r['original'] for r in s['program_inventory']]==PROGRAMS+DRIVERS,'whole program and driver list')
    for r in s['program_inventory']:
        binding(dict(path=r['copy'],bytes=r['bytes'],sha256=r['sha256']))
        need(r['role']==('bounded_validation' if r['original'] in PROGRAMS else 'historical_operational_driver') and not r['universal_proof_premise'],'bounded program role')
    v=s['validation_boundary'];need(v['full_mathematical_programs']==2 and v['complete_archival_drivers']==2 and v['uniform_written_proof_depends_on_finite_results'] is False,'complete bounded validation')
    binding(s['formal_scope']);f=json.loads(local('formal/scope.json').read_text())
    need(len(f['modules'])==2 and [len(r['declarations']) for r in f['modules']]==[8,4] and f['new_declarations']==8 and f['reused_declarations']==4,'eight generic plus four reused reports')
    for r in f['modules']:binding(dict(path='formal/'+r['file'],bytes=r['bytes'],sha256=r['sha256']))
    need(not f['source_specific_claims'] and len(f['not_formalized'])==6,'formal limitations')
    need([r['declaration'] for r in s['formal_statement_map']]==[d for m in f['modules'] for d in m['declarations']],'complete formal map')
    need(s['cost_boundary']['full_common_paper_charged_once'] and not s['cost_boundary']['cross_topic_discount'] and not s['cost_boundary']['prior_own_proof_bank_as_unpriced_logical_premise'],'full self-contained theory cost')
    for k in ['ratio','external_proof_cost','source_graphics_cost']:need(s['cost_boundary'][k] is None,'unknown cost')
    need(s['new_source_credit']==s['new_question_credit']==0,'no new intake or question claim')
    return dict(source_blocks=6,proof_spans=len(s['proof_spans']),programs=2,archival_drivers=2,formal_reports=12)
def controls(s):
    ans=[]
    def reject(name,change):
        x=copy.deepcopy(s);change(x)
        try:validate(x)
        except RuntimeError as exc:ans.append(dict(name=name,rejected=True,reason=str(exc)));return
        raise RuntimeError('Control accepted '+name)
    reject('omit inherited clause',lambda x:x['contracts'].pop())
    reject('alter source authors',lambda x:x['source']['authors'].pop())
    reject('change proof binding',lambda x:x['proof_spans']['UR.Restriction'].__setitem__('sha256_utf8','0'*64))
    reject('erase normality',lambda x:x['precise_hypotheses'].__setitem__('normal_subgroup_required',False))
    reject('claim universal rank two',lambda x:x['precise_hypotheses'].__setitem__('rank_two_universal_claim',True))
    reject('erase hexagon correction',lambda x:next(r for r in x['contracts'] if r['id']=='F010.Example5.1').__setitem__('status','proved_literal'))
    reject('erase degree-one base qualification',lambda x:next(r for r in x['contracts'] if r['id']=='F010.Example5.2').__setitem__('status','proved_literal'))
    reject('drop whole program',lambda x:x['program_inventory'].pop(0))
    reject('promote samples to uniform proof',lambda x:x['validation_boundary'].__setitem__('uniform_written_proof_depends_on_finite_results',True))
    reject('unpriced old own proof',lambda x:x['cost_boundary'].__setitem__('prior_own_proof_bank_as_unpriced_logical_premise',True))
    reject('new question claim',lambda x:x.__setitem__('new_question_credit',1))
    return ans
def code_inclusion():
    t=local('program-appendix.tex').read_text();names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',t)
    need(names==PROGRAMS,'whole two-program appendix')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber',t),'no excerpted code')
    pieces=[]
    for page in PdfReader(local('program-appendix.pdf')).pages:
        def visit(t,cm,tm,font,size):
            if font and 'Menlo' in str(font.get('/BaseFont','')):pieces.append(t)
        page.extract_text(visitor_text=visit)
    norm=lambda t:''.join(c for c in t if not c.isspace())
    src=norm(''.join(local('programs/'+n).read_text() for n in names))
    need(src==norm(''.join(pieces)),'full unchanged printed code')
    return dict(files=names,nonspace_code_characters=len(src),layout_whitespace_ignored_only_for_inclusion=True)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path)
    ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--xelatex',default=shutil.which('xelatex'))
    ap.add_argument('--lean',default=LEAN);ap.add_argument('--packages',default=PACKAGES)
    a=ap.parse_args();need(not os.path.lexists(a.out),'fresh output required');out=a.out.resolve();out.mkdir(parents=True)
    s=json.loads(local('scope.json').read_text());res=validate(s);res['controls']=controls(s);res['code_inclusion']=code_inclusion()
    if local('manifest.json').is_file():
        for r in json.loads(local('manifest.json').read_text())['exports']:binding(r)
        res['manifest_sha256']=sha(local('manifest.json'))
    external=[]
    for ns,base in [('study',a.study_root),('public',a.public_root)]:
        if base:
            for r in s['predecessors']:
                if r['namespace']==ns:binding(r,base);external.append(r['path'])
    if a.study_root:
        binding(s['source']['primary'],a.study_root)
        need(len(PdfReader(a.study_root/s['source']['primary']['path']).pages)==13,'exact primary edition')
        external.append(s['source']['primary']['path'])
    res['external_bindings_checked']=external
    def run(name,cmd):
        p=subprocess.run(list(map(str,cmd)),cwd=out,text=True,capture_output=True,timeout=1800)
        (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr)
        need(p.returncode==0,'Replay failed '+name);return p
    if a.programs:
        need(a.gap,'GAP required');env=run('gap_version',[a.gap,'-q','-T','-c','LoadPackage("grape");;Print(GAPInfo.Version,"\\n",PackageInfo("grape")[1].Version,"\\n");QUIT;'])
        versions=env.stdout.strip().splitlines();need(versions==['4.15.1','4.9.3'] and not env.stderr.strip(),'pinned GAP and GRAPE')
        markers=['PHASE177_HEXAGON_CHECK_COMPLETE','PHASE188_BOUNDED_GADGET_REVIEW_PASS'];runs=[]
        for n,m in zip(PROGRAMS,markers):
            p=run(Path(n).stem,[a.gap,'-q','-T',local('programs/'+n)])
            need(m in p.stdout and not re.search(r'Error,|error:|warning:',p.stdout+p.stderr),'finite positive marker '+n)
            runs.append(dict(file=n,sha256=sha(local('programs/'+n)),marker=m,pass_result=True))
        mutations=[('tail_chord',PROGRAMS[1],'Add(edges,[base+2*M+3,base+2*M]);','','restriction pair mismatch'),
          ('arrow_labels',PROGRAMS[1],'k:=Position(els,els[y]/els[x]);','k:=2;','uncolored arrow rigidity'),
          ('wrong_hexagon_kernel',PROGRAMS[0],'P177Hexagon([0..5],[12,6]);;','P177Hexagon([0..5],[12,3]);;','Assertion failure')]
        negatives=[]
        for name,src,old,new,error in mutations:
            t=local('programs/'+src).read_text();need(t.count(old)==1,'exact mutation anchor');t=t.replace(old,new)
            if name=='arrow_labels':t=t.replace('result.n=(q^3+9*q^2-8*q)/2','true')
            f=out/(name+'.g');f.write_text(t);p=subprocess.run([a.gap,'-q','-T',str(f)],cwd=out,text=True,capture_output=True,timeout=300)
            log=p.stdout+p.stderr;(out/(name+'.log')).write_text(log)
            need(error in log and markers[PROGRAMS.index(src)] not in log,'semantic rejection '+name)
            negatives.append(dict(name=name,rejected=True,expected=error))
        res['bounded_validation']=dict(versions=versions,runs=runs,controls=negatives,small_colored_graphs=25,normal_pairs=7,completed_pairs=4,family_n=[2,3,4,5],universal_proof=False)
    if a.formal:
        run('formal',[sys.executable,'-B','-O',local('formal/check.py'),'--out',out/'formal','--lean',a.lean,'--packages',a.packages])
        f=json.loads((out/'formal/report.json').read_text());need(sum(len(m['axioms']) for m in f['modules'])==12 and len(f['countermodels'])==4,'exact formal coverage')
        res['formal']=dict(reports=12,generic_new=8,local_reused=4,countermodels=4,end_to_end_source=False)
    if a.render:
        need(a.xelatex,'XeLaTeX required');r=out/'render';r.mkdir()
        for row in s['documents']:
            if row['path'].endswith('.tex'):
                p=r/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local(row['path']),p)
        shutil.copytree(local('programs'),r/'programs');rs=[]
        for n in DOCS:
            for i in range(2):
                p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',n+'.tex'],cwd=r,text=True,capture_output=True)
                need(p.returncode==0,'TeX build '+n)
            log=(r/(n+'.log')).read_text();diag=[x for x in log.splitlines() if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning',x)]
            need(not diag,'render diagnostics '+n)
            old,new=PdfReader(local(n+'.pdf')),PdfReader(r/(n+'.pdf'))
            need(len(old.pages)==len(new.pages) and all(x.extract_text()==y.extract_text() for x,y in zip(old.pages,new.pages)),'exact rendered page text '+n)
            rs.append(dict(document=n,pages=len(new.pages),diagnostics=[],per_page_text_identical=True))
        res['render']=rs
    res.update(status='PASS',independent_mathematical_review=False,new_source_credit=0,new_question_credit=0,ratio=None)
    (out/'report.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(dict(status='PASS',source_blocks=6,controls=len(res['controls']),out=str(out))))
if __name__=='__main__':main()
