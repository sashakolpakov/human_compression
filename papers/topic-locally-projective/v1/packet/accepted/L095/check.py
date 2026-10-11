#!/usr/bin/env python3
"""Bounded fresh L095 presentation/geometry replay; exact accepted census reuse."""
import argparse,copy,hashlib,importlib.util,json,math,os,re,shutil,signal,subprocess,time,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parent
def need(b,s):
    if not b:raise ValueError(s)
def binding(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def bound(base,row):
    rel=Path(row['path']);need(not rel.is_absolute() and '..'not in rel.parts,'relative bound path')
    p=base/rel;need(p.is_file() and binding(p)=={k:row[k] for k in ['bytes','sha256']},'binding '+str(p));return p
def manifest(base):
    m=load(base/'manifest.json')
    for r in m['exports']:bound(base,r)
    need(len({x['path']for x in m['exports']})==len(m['exports']),'unique exports')
    return len(m['exports'])
def execute(cmd,cwd,stem,timeout=45,input=None):
    t=time.monotonic();p=subprocess.Popen(cmd,cwd=cwd,stdin=subprocess.PIPE if input else None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
    try:stdout,stderr=p.communicate(input,timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid,signal.SIGTERM)
        try:stdout,stderr=p.communicate(timeout=5)
        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);stdout,stderr=p.communicate()
        (cwd/(stem+'.stdout')).write_text(stdout);(cwd/(stem+'.stderr')).write_text(stderr)
        raise ValueError('bounded timeout '+stem)
    (cwd/(stem+'.stdout')).write_text(stdout);(cwd/(stem+'.stderr')).write_text(stderr)
    need(p.returncode==0 and not any(s in stdout+stderr for s in ['Error,','Syntax error','Syntax warning','Missing character:','Emergency stop','Fatal error']),'command failure '+stem)
    return stdout,time.monotonic()-t
def validate(p,m,s,g):
    need(p==[20,175560,171,600415200,290],'exact presentation upper bound')
    need(len(m)==290 and all(len(r)==1 and type(r[0])is int for r in m),'complete one-column relation matrix')
    need(math.gcd(*(r[0]for r in m))==171 and [-171]in m,'actual cyclic gcd')
    need(s[0]==[[2,2,2],[1,2,1,-2,1,2,-1,2,1]],'actual complete final relators')
    need(s[1][:3]==[[-1,-2,1],[-2,-1,2],[-2,-1,2,2,1]],'source generator images')
    need(g==[256,256,256,[[2,1],[3,1],[5,1],[7,1],[11,1],[19,1]],[[2,1],[3,1],[5,1],[19,1]],1463,2926,57,6],'all finite geometry interfaces')
    return True
def controls(p,m,s,g):
    result=[]
    def reject(name,q,n,t,h):
        try:validate(q,n,t,h)
        except (ValueError,IndexError,TypeError):result.append(name)
        else:raise ValueError('missed control '+name)
    for i in range(5):
        q=copy.deepcopy(p);q[i]+=1;reject('alter_presentation_coordinate_'+str(i),q,m,s,g)
    reject('replace_cyclic_relations_by_even_multiples',p,[[2*r[0]]for r in m],s,g)
    reject('omit_relation_matrix_row',p,m[:-1],s,g)
    t=copy.deepcopy(s);t[0].pop();reject('omit_two_generator_relator',p,m,t,g)
    t=copy.deepcopy(s);t[1][1][0]*=-1;reject('wrong_source_word_image',p,m,t,g)
    for i in range(9):
        h=copy.deepcopy(g)
        if isinstance(h[i],list):h[i].pop()
        else:h[i]+=1
        reject('alter_geometry_interface_'+str(i),p,m,s,h)
    return result
def inherited():
    d=load(R/'dependencies.json')
    for k in ['census_manifest','census_review_manifest']:bound(R,d[k])
    need(d['census_manifest']['sha256']=='e9fbe22f018d64b994c67ef0f190c685873285db0b62c7c059e4caac37ef0cfb','accepted census pin')
    need(d['census_review_manifest']['sha256']=='24994f8e6a30131dde603cd4c78b2ad96b369742b795216d932e595a76c066ac','distinct review pin')
    n=manifest(R/'census');nr=manifest(R/'census_review')
    for a,b in d['reused_file_aliases']:need((R/a).read_bytes()==(R/b).read_bytes(),'exact reused marking')
    review=load(R/'census_review/review.json');need(review['status']=='PASS_DISTINCT_ROOT_REVIEW_COMPLETE_L084_CONTRACT' and review['original_rows_checked']==145,'accepted full census scope')
    spec=importlib.util.spec_from_file_location('l095_inherited_accounting',R/'census/accounting.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    c=load(R/'census/evidence/census.json');rows=load(R/'census/source_tables.json')
    rec=module.reconcile(c,rows)
    return {'exports':n,'review_exports':nr,'reconciliation':rec,'census_reexecuted':False,'trust':'The exact exhaustive census and distinct fresh root replay are reused; all complete tables/evidence are bound and reconciled again.'}
def runtime(gap,out):
    script='SizeScreen([100000,24]);; LoadPackage("ace");; LoadPackage("tomlib");; Print("GAP|",GAPInfo.Version,"\\nACE|",PackageInfo("ace")[1].Version,"\\nTomLib|",PackageInfo("tomlib")[1].Version,"\\n");; for p in GAPInfo.RootPaths do Print("gap_root|",p,"\\n"); od; Print("ace_root|",Filename(DirectoriesPackageLibrary("ace","")[1],""),"\\n");; Print("tomlib_root|",Filename(DirectoriesPackageLibrary("tomlib","")[1],""),"\\n");; QUIT;\n'
    text,_=execute([gap,'-q','-b','-A','-r'],out,'runtime',input=script);spec=load(R/'computational_inputs.json');vals={};roots={}
    for line in text.splitlines():
        if '|'not in line:continue
        k,v=line.split('|',1)
        if k.endswith('_root'):roots.setdefault(k,[]).append(Path(v))
        else:vals[k]=v
    for k in ['GAP','ACE','TomLib']:need(vals.get(k)==spec[k],'runtime version '+k)
    for r in spec['file_pins']+load(R/'census/computational_inputs.json')['file_pins']:need(any((p/r['path']).is_file() and binding(p/r['path'])=={k:r[k]for k in ['bytes','sha256']} for p in roots[r['root']]),'algorithm pin '+r['path'])
    return {'versions':vals,'file_pins':spec['file_pins'],'limits':spec['limits'],'trust':spec['scope']}
def texts(path):
    from pypdf import PdfReader
    return [p.extract_text()or''for p in PdfReader(path).pages]
def code_inclusion(pdf):
    compact=lambda s:''.join(c for c in unicodedata.normalize('NFKC',s)if not c.isspace())
    pages=[re.sub(r'\n'+str(i)+r'\s*$','',t)for i,t in enumerate(texts(pdf),1)]
    full=compact('\n'.join(pages));out=[]
    for f in ['programs/presentation.g','programs/ambient_marking.g','programs/local_geometry.g']:
        need(compact((R/f).read_text())in full,'entire printed file '+f);out.append({'path':f,**binding(R/f)})
    return out
def render(out,xe):
    q=out/'render';q.mkdir();shutil.copytree(R/'programs',q/'programs');report=[]
    for n in ['universal-locally-projective','required-programs']:
        shutil.copy2(R/(n+'.tex'),q/(n+'.tex'))
        for i in [1,2]:execute([xe,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',n+'.tex'],q,n+'-'+str(i),120)
        logs=(q/(n+'.log')).read_text();diagnostics=[l for l in logs.splitlines() if any(w in l for w in ['Overfull','Missing character','Warning:'])];need(not diagnostics,'render diagnostics '+str(diagnostics))
        ts=texts(q/(n+'.pdf'));need(ts==texts(R/(n+'.pdf')),'exact fresh page text '+n)
        need(all(not any(ord(c)<32 and c not in '\n\r\t'for c in t) and '\ufffd'not in t for t in ts),'glyph extraction '+n)
        report.append({'name':n,'pages':len(ts),'text_hashes':[hashlib.sha256(t.encode()).hexdigest()for t in ts],'diagnostics':diagnostics})
    code_inclusion(q/'required-programs.pdf');return report
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path);ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default=shutil.which('xelatex'));a=ap.parse_args()
    need(a.gap is not None,'GAP required');need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);start=time.monotonic()
    count=manifest(R)if (R/'manifest.json').exists() else None
    scope=load(R/'scope.json');need(scope['principal_original']=='L095' and scope['complete_corrected_principal_contract'] is True and scope['formal_declarations']==0 and scope['historical_g_txt_used'] is False,'exact source/formal boundary')
    need(scope['full_subgroup_type_identification_from_abbreviations_claimed'] is False and scope['unseen_journal_identity_claimed'] is False,'edition qualifications')
    need(len(load(R/'source_ledger.json')['rows'])==scope['source_rows']==34,'full source ledger')
    for x in load(R/'proof_map.json')['spans']:
        t='\n'.join((R/x['path']).read_text().splitlines()[x['start_line']-1:x['end_line']])+'\n';need(hashlib.sha256(t.encode()).hexdigest()==x['sha256'],'exact proof span '+x['id'])
    primary=[]
    if a.study_root:
        for k,row in load(R/'source_bindings.json').items():bound(a.study_root,row);primary.append(k)
    old=inherited();rt=runtime(a.gap,a.out);shutil.copytree(R/'programs',a.out/'programs');runs=[]
    for name,sentinel in [('presentation','L095_PRESENTATION_PASS'),('local_geometry','L095_GEOMETRY_PASS')]:
        txt,sec=execute([a.gap,'-q','-b','-A','-K','512m','-r','programs/'+name+'.g'],a.out,name)
        need(sentinel in txt,'complete program sentinel '+name);runs.append({'program':name,'seconds':sec})
    p,m,s,g=[load(a.out/n)for n in ['presentation_summary.json','cyclic_relations.json','schreier_final.json','geometry_summary.json']]
    validate(p,m,s,g);negative=controls(p,m,s,g)
    for n in ['index20.json','schreier_initial.json','schreier_final.json','cyclic_relations.json','presentation_summary.json','geometry_summary.json']:
        need(load(a.out/n)==load(R/'evidence'/n),'full fresh evidence '+n)
    pdf=render(a.out,a.xelatex)if a.render else []
    report={'status':'PASS','source':'L095','exports':count,'source_rows':34,'proof_contexts':5,'source_bindings_checked':primary,'presentation':p,'full_IP_identities':768,'new_finite_program_runs':runs,'semantic_controls':negative,'accepted_census_reuse':old,'runtime':rt,'complete_code_inclusion':code_inclusion(R/'required-programs.pdf'),'renders':pdf,'formal_declarations':0,'new_question_credit':0,'seconds':time.monotonic()-start,'result_scope':'Complete corrected principal author candidate; distinct mathematical review remains required. GAP/ACE algorithms and declared geometric/classical inputs retained.'}
    write(a.out/'report.json',report);print(json.dumps({'status':'PASS','source_rows':34,'controls':len(negative),'seconds':report['seconds']}))
if __name__=='__main__':main()
