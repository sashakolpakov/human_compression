#!/usr/bin/env python3
"""Binding/scope replay; mathematical acceptance is the written independent review."""
import argparse, copy, hashlib, itertools, json, shutil, subprocess, tempfile
from pathlib import Path
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
def need(value, message):
    if not value:
        raise ValueError(message)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_text())
def bind(root, record):
    p = root / record['path']
    need(p.is_file(), 'missing binding: '+str(p))
    need(p.stat().st_size == record['bytes'], 'byte count: '+str(p))
    need(digest(p) == record['sha256'], 'hash: '+str(p))
def pages(p):
    return [page.extract_text() for page in PdfReader(p).pages]
def scope_checks(scope, deps, routes, tex):
    for k in ['main_theorem_refuted','whole_source_recovered']:
        need(scope[k] is False, 'unaccepted scope: '+k)
    for k in ['new_original_credit','new_question_credit','new_Lean']:
        need(scope[k] == 0, 'unaccepted credit: '+k)
    need(scope['measurement'] is None, 'unaccepted measurement')
    need(scope['pages']==3 and scope['author']=='root', 'scope pages/author')
    need(len(scope['pending'])==2 and 'Rank4' in scope['pending'][0], 'rank4 pending')
    need(len(deps['required_inputs'])==6, 'retained dependency classes')
    need(any('Noncommuting' in x['name'] for x in deps['required_inputs']), 'noncommuting retained input')
    need(deps['mathematical_software']==[] and deps['new_Lean']==0, 'author program/formal boundary')
    expected={'Theorem1', 'Figure1', 'Opening historical statements and cited chiral maps', 'Final statement that rank3 markings were not enumerated'} | {'Lemma'+str(i) for i in range(1,16)}
    need(len(routes['routes'])==19 and {r['source'] for r in routes['routes']}==expected,'complete unique source routes')
    by={r['source']:r['disposition'] for r in routes['routes']}
    need('rank4 pending' in by['Theorem1'] and 'not certified' in by['Figure1'], 'source rank4 scope')
    need('not the rank4 nonexistence theorem' in by['Lemma14'], 'conditional diagnostic scope')
    need('Let the finite set $\\Omega$' in tex, 'explicit finiteness')
    need('all the other listed maximal-subgroup types except the subfield' in tex, 'maximal-type precision')
    need('noncommuting case' in tex and 'not a new result' in tex, 'retained theorem and attribution')
def controls(s,d,r,t):
    cases=[]
    for key,value in [('main_theorem_refuted',True),('whole_source_recovered',True),('new_original_credit',1),('new_question_credit',1),('new_Lean',1),('measurement',0),('pending',[])]:
        q=copy.deepcopy(s);q[key]=value;cases.append((key,q,d,r,t))
    q=copy.deepcopy(d);q['required_inputs']=q['required_inputs'][:-1];cases.append(('lost dependency',s,q,r,t))
    q=copy.deepcopy(d);q['mathematical_software']=['claimed proof census'];cases.append(('invented computation',s,q,r,t))
    q=copy.deepcopy(r);q['routes'][1]['source']='Lemma2';cases.append(('duplicate source route',s,d,q,t))
    q=copy.deepcopy(r);q['routes'][0]['disposition']='Fully recovered';cases.append(('whole source overclaim',s,d,q,t))
    q=copy.deepcopy(r)
    next(x for x in q['routes'] if x['source']=='Lemma14')['disposition']='The principal theorem is false'
    cases.append(('diagnostic overclaim',s,d,q,t))
    cases.append(('missing finite hypothesis',s,d,r,t.replace('Let the finite set $\\Omega$','Let the set $\\Omega$')))
    rejected=[]
    for name,ss,dd,rr,tt in cases:
        try: scope_checks(ss,dd,rr,tt)
        except (ValueError,KeyError): rejected.append(name)
        else: raise ValueError('negative control accepted: '+name)
    return rejected
def a4_check():
    def mul(a,b): return tuple(a[b[i]] for i in range(4))
    def inverse(a): return tuple(a.index(i) for i in range(4))
    one=tuple(range(4))
    group=[p for p in itertools.permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
    x=(1,2,0,3); h=frozenset([one,x,mul(x,x)])
    conjugates={frozenset(mul(mul(inverse(g),v),g) for v in h) for g in group}
    need(len(group)==12 and len(conjugates)==4, 'A4 independent literal model')
    need(all(len(c)==3 for c in conjugates) and all(len(c&h)==1 for c in conjugates if c!=h), 'A4 C3 intersections')
    return {'ambient_order':12,'subgroup_order':3,'conjugate_subgroups':4,'normal':False,'role':'optional independent diagnostic, not a mathematical premise'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');args=ap.parse_args()
    b=load(HERE/'bindings.json');a=args.author.resolve()
    bind(a,b['author_manifest'])
    manifest=load(a/'manifest.json')
    need(manifest['exports']==b['author_exports'], 'author export set')
    for row in manifest['exports']: bind(a,row)
    if (HERE/'manifest.json').exists():
        for row in load(HERE/'manifest.json')['exports']: bind(HERE,row)
    s=load(a/'scope.json');d=load(a/'dependencies.json');r=load(a/'source_map.json');t=(a/'ree_involutions.tex').read_text()
    scope_checks(s,d,r,t)
    pt=pages(a/'ree_involutions.pdf');need(len(pt)==3,'PDF extent')
    need([hashlib.sha256(v.encode()).hexdigest() for v in pt]==b['page_text_sha256'],'page text bindings')
    sources_checked=False
    if args.study_root:
        for row in b['study_bindings']: bind(args.study_root,row)
        old=args.study_root/'corpus106_L039_recovery'
        expected=(old/'ree_involutions.tex').read_text().replace('Let $\\Omega$ carry a Steiner','Let the finite set $\\Omega$ carry a Steiner').replace('Hence the maximal subgroups of the first four listed types, apart\nfrom a normalizer of $C_\\beta$, cannot contain an element of order\n$\\beta$.','Hence all the other listed maximal-subgroup types except the subfield\ngroups cannot contain an element of order $\\beta$.')
        need(expected==t,'exact two-passage TeX delta')
        need((old/'dependencies.json').read_bytes()==(a/'dependencies.json').read_bytes(),'dependency conservation')
        need((old/'source_map.json').read_bytes()==(a/'source_map.json').read_bytes(),'source map conservation')
        sources_checked=True
    render=None
    if args.render:
        with tempfile.TemporaryDirectory(prefix='L039_distinct_render_') as temp:
            build=Path(temp);shutil.copy2(a/'ree_involutions.tex',build/'ree_involutions.tex')
            for _ in range(2):
                done=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','ree_involutions.tex'],cwd=build,capture_output=True,text=True)
                need(done.returncode==0,'TeX compilation: '+done.stdout[-1000:])
            log=(build/'ree_involutions.log').read_text()
            bad=[line for line in log.splitlines() if 'Overfull' in line or 'undefined' in line or 'Warning' in line]
            need(not bad,'TeX diagnostics: '+repr(bad))
            need(pages(build/'ree_involutions.pdf')==pt,'fresh three-page text equality')
            render={'pages':3,'two_passes':True,'page_texts_identical':True,'diagnostics':bad}
    report={'status':'PASS','author_manifest':b['author_manifest']['sha256'],'author_exports':6,'source_routes':19,'retained_input_classes':6,'source_and_predecessor_bindings_checked':sources_checked,'negative_controls':controls(s,d,r,t),'a4':a4_check(),'render':render,'scope':'bounded scientific review only; rank4 and whole original pending'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__': main()
