"""Portable binding/render checker for a bounded distinct written review."""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess
HERE=Path(__file__).resolve().parent
PIN='66576b7c4cd353b33d19f48a1403d3cda93ea857f6dd51c15ea4657bbf07b571'

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(base,r):
    p=base/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'exact binding '+r['path'])
def scopecheck(s):
    need(s['author']=='root','author role')
    need(s['new_original_credit']==s['new_question_credit']==s['new_formal_declarations']==0,'bounded credits')
    need(len(s['claims'])==3,'all three scope claims')
    need(set(s['not_claimed'])=={'All forms/markings in dimensions3,4,5 classified','Larger-field construction recovered','Whole L031 accepted','Priority or new open-conjecture solution'},'complete boundaries')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true')
    ap.add_argument('--source',type=Path);a=ap.parse_args()
    need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    if (HERE/'manifest.json').exists():
        for r in read(HERE/'manifest.json')['exports']:bound(HERE,r)
    b=a.author_root;need(sha(b/'manifest.json')==PIN,'exact author freeze')
    m=read(b/'manifest.json')
    for r in m['exports']:bound(b,r)
    s=read(b/'scope.json');scopecheck(s)
    dep=read(b/'dependencies.json')
    need(dep['whole_companion_required'] is True,'whole positive companion paid')
    need(dep['bindings'][1]['sha256']=='c0f8f9c664a2024b31c9766804dc1c804323bfa30e4f9738293d6056ad5a2d0d','exact positive companion')
    need(dep['bindings'][4]['sha256']=='5841cf2277db9d3cf40399e1f70fb2fea0f45cd8f9141f6961c9cbaea69cfa91','exact distinct positive review')
    controls=[]
    for key,value in [('author','enumeration_volume'),('new_original_credit',1),('new_question_credit',1),('new_formal_declarations',1),('claims',[]),('not_claimed',[])]:
        bad=copy.deepcopy(s);bad[key]=value
        try:scopecheck(bad)
        except ValueError:controls.append(key)
        else:raise ValueError('scope control accepted '+key)
    source_checked=False
    if a.source:
        r=read(b/'dependencies.json')['bindings'][0]
        need(a.source.stat().st_size==r['bytes'] and sha(a.source)==r['sha256'],'fixed primary edition');source_checked=True
    native=read(b/'native.json');texts=None;diagnostics=[]
    if a.render:
        from pypdf import PdfReader
        t=a.out/'native';t.mkdir();shutil.copy2(b/'binary_exclusion.tex',t/'binary_exclusion.tex')
        for k in range(2):
            c=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','binary_exclusion.tex'],cwd=t,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (t/f'pass{k+1}.stdout').write_text(c.stdout);need(c.returncode==0,'native compiler')
        log=(t/'binary_exclusion.log').read_text(errors='replace')
        diagnostics=[x for x in log.splitlines() if re.search(r'Overfull|LaTeX Warning|undefined references|^!',x)]
        need(not diagnostics,'clean final render')
        texts=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(t/'binary_exclusion.pdf').pages]
        original=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(b/'binary_exclusion.pdf').pages]
        need(texts==original==native['page_text_sha256'] and len(texts)==2,'both complete page texts')
    result={'status':'PASS_DISTINCT_BOUNDED_REVIEW','author_manifest_sha256':PIN,
            'author_exports':len(m['exports']),'finite_mathematical_premise':False,'scope_controls':controls,
            'fresh_native_render':a.render,'page_text_sha256':texts,'diagnostics':diagnostics,
            'primary_edition_checked':source_checked,'whole_L031_accepted':False,
            'new_original_credit':0,'new_question_credit':0,'new_formal_credit':0,
            'author_bytes_modified':False}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
