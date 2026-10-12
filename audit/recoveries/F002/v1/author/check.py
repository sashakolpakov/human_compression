"""Complete rerun; saved records alone are not a coverage certificate."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,time
from pypdf import PdfReader
P=Path(__file__).resolve().parent

def need(v,m):
    if not v: raise ValueError(m)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def verify(rows,base):
    for r in rows:
        p=base/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'binding '+r['path'])
    return len(rows)

def bracket(log,label):
    need(log.count(label)==1,'unique log label '+label)
    begin=log.index('[',log.index(label)+len(label));depth=0
    for i in range(begin,len(log)):
        depth+=(log[i]=='[')-(log[i]==']')
        if depth==0:return log[begin:i+1]
    raise ValueError('unterminated array '+label)

def records(log):
    s='recordedInvolutions:='+bracket(log,'INVOLUTIONS_LITERAL')+';;\nrecordedMarks:=[];;\n'
    for r in [3,4,5]:s+='recordedMarks[%d]:='%r+bracket(log,'COMPLETE_MARKS_RANK_%d'%r)+';;\n'
    return s

def execute(command,cwd,out,name,seconds):
    begin=time.monotonic()
    with (out/(name+'.stdout')).open('wb') as a,(out/(name+'.stderr')).open('wb') as b:
        p=subprocess.Popen(command,cwd=cwd,stdout=a,stderr=b)
        try:rc=p.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            p.kill();p.wait();raise ValueError(name+' timeout: no certificate')
    need(rc==0 and (out/(name+'.stderr')).stat().st_size==0,name+' execution diagnostics')
    log=(out/(name+'.stdout')).read_text();need('Error' not in log,name+' GAP error')
    return log,round(time.monotonic()-begin,6)

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--study-root',type=Path)
    a.add_argument('--gap',default=shutil.which('gap') or '/opt/homebrew/bin/gap');a.add_argument('--render',action='store_true')
    a.add_argument('--pdflatex',default=shutil.which('pdflatex') or '/opt/homebrew/bin/pdflatex');args=a.parse_args()
    need(not args.out.exists(),'fresh output required');args.out.mkdir(parents=True)
    exports=verify(json.loads((P/'manifest.json').read_text())['exports'],P) if (P/'manifest.json').exists() else None
    retained=verify(json.loads((P/'retained_projective.json').read_text())['whole_files'],P)
    external=verify(json.loads((P/'provenance.json').read_text())['local_bindings'],args.study_root) if args.study_root else None
    job=args.out/'job';job.mkdir()
    for name in ['enumerate_even.g','checks.g','source_markings.g','compare.g']:shutil.copy2(P/name,job/name)
    log,elapsed=execute([args.gap,'-q','-b','-c','degree:=11;rankLimit:=5;Read("enumerate_even.g");'],job,args.out,'enumeration',300)
    need(log.rstrip().endswith('COMPLETE_EXHAUSTION'),'complete census required')
    need(re.search(r'INVOLUTIONS 18315\b',log),'full even involution pool')
    need(json.loads(bracket(log,'PREFIX_CLASSES'))==[1,2,78,2634,147,20],'prefix census')
    need('PRUNED_IMPOSSIBLE_TRANSITIVITY 2497' in log,'pruning count')
    generated=records(log);(job/'generated_markings.g').write_text(generated)
    # Whitespace is incidental GAP line wrapping; every literal permutation/id is compared.
    normalize=lambda s:re.sub(r'\s+','',s)
    need(normalize(generated)==normalize((P/'generated_markings.g').read_text()),'complete literal record equality')
    compared,seconds=execute([args.gap,'-q','-b','compare.g'],job,args.out,'comparison',300)
    need(compared.rstrip().endswith('COMPLETE_COMPARISON_PASS'),'complete comparison')
    expected=[([1,5,5],[1,5,5]),([2,3,6],[1,5,5]),([2,3,6],[1,5,5]),([2,3,6],[2,3,6]),([1,10],[5,6])]
    for i,(x,y) in enumerate(expected,1):
        for label,value in [('SOURCE_SUFFIX_ORBITS',x),('SOURCE_DUAL_SUFFIX_ORBITS',y)]:
            need(json.loads(bracket(compared,label+' '+str(i)+' '))==value,'source orbit cell')
        wanted='true' if i in [1,4,5] else 'false'
        need('SOURCE_ORBIT %d RECORDS 2 SELF_DUAL_ABSTRACT %s SELF_DUAL_PERMUTATION false'%(i,wanted) in compared,'duality comparison')
    rendered=[]
    if args.render:
        native=args.out/'native';native.mkdir()
        for name in ['marked_search','degree_eleven']:
            shutil.copy2(P/(name+'.tex'),native)
            for n in range(2):
                q=subprocess.run([args.pdflatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=native,capture_output=True)
                (native/(name+'.pass%d.stdout'%n)).write_bytes(q.stdout);need(q.returncode==0,'native render')
            warnings=[x for x in (native/(name+'.log')).read_text().splitlines() if any(y in x for y in ['Overfull','undefined','LaTeX Warning'])]
            need(not warnings,'native diagnostics '+str(warnings))
            texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
            pages=texts(native/(name+'.pdf'));need(pages==texts(P/(name+'.pdf')),'exact native page texts')
            rendered.append({'document':name,'pages':len(pages),'all_page_texts_equal':True})
    report={'status':'PASS','exports':exports,'retained_whole_files':retained,'source_bindings':external,'complete_enumeration_seconds':elapsed,'comparison_seconds':seconds,'even_involutions':18315,'prefix_classes':[1,2,78,2634,147,20],'transitive_markings_by_rank':{'3':130,'4':2,'5':0},'full_subset_IP_checks':132,'source_markings':5,'source_orbit_cells':10,'render':rendered,'whole_original_credit':0,'new_conjecture_credit':0,'new_Lean_credit':0}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
