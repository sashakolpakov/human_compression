"""Fresh complete S10 enumeration plus actual IP and independent fusion."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import argparse, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    a=argparse.ArgumentParser();a.add_argument('--study',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');args=a.parse_args()
    P=Path(__file__).resolve().parent;S=args.study.resolve();O=args.out.resolve()
    need(not O.exists(),'fresh output required');bindings=json.loads((P/'dependencies.json').read_text())
    for row in bindings:
        b=(S/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'exact acquired input '+row['path'])
    exports=[]
    if (P/'manifest.json').exists():
        exports=json.loads((P/'manifest.json').read_text())['exports']
        for row in exports:
            b=(P/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'frozen export '+row['path'])
    method=S/'corpus106_L120_finite_method_v1';plan=json.loads((P/'plan.json').read_text())
    need(len(plan['runs'])==5,'five initial branches')
    for i,row in enumerate(plan['runs'],1):
        need(row['name']==f'symmetric10_part{i}' and row['spec']==dict(kind='symmetric',degree=10,rank_limit=9,branch=i,engine_entry='pool') and row['cap_seconds']==120,'fixed complete S10 plan')
    O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    def run(name,cmd,cap,cwd=None):
        cp=subprocess.run(cmd,env=env,capture_output=True,timeout=cap,cwd=cwd)
        (O/(name+'.stdout')).write_bytes(cp.stdout);(O/(name+'.stderr')).write_bytes(cp.stderr)
        need(cp.returncode==0 and not cp.stderr,'clean complete '+name);return cp.stdout.decode()
    run('enumeration',[sys.executable,str(method/'run_pool.py'),'--plan',str(P/'plan.json'),'--out',str(O/'branches')],650)
    ids=[];literal=None;counts={str(r):dict(ordered=0,self_dual=0) for r in range(3,10)}
    for i in range(1,6):
        D=O/'branches'/f'symmetric10_part{i}';receipt=json.loads((D/'report.json').read_text());need(receipt['status']=='COMPLETE_FIXED_BRANCH','complete initial branch')
        result=json.loads((D/'result.json').read_text());need(result==json.loads((P/'completed_branches'/f'symmetric10_part{i}'/'result.json').read_text()),'exact complete branch output')
        text=(D/'stdout.log').read_text();m=re.search(r'INVOLUTIONS_LITERAL\s+(\[.*?\])\s+DIRECT_INITIAL_CHILD',text,re.S);need(m is not None,'literal involutions')
        if literal is None:literal=m.group(1)
        else:need(literal==m.group(1),'identical involution list')
        ids.extend(row['ids'] for row in result['marks'] if row['order']==3628800)
        for r,c in counts.items():
            for k in c:c[k]+=result['counts'][r][k]
    need(len(ids)==len(set(map(tuple,ids))),'distinct literal tuples')
    (O/'input.g').write_text('ivs:='+literal+';;\nids:='+json.dumps(ids)+';;\n')
    (O/'driver.g').write_text('inputFile:='+json.dumps(str(O/'input.g'))+';;\nRead('+json.dumps(str(P/'validate.g'))+');\n')
    run('validation',['/opt/homebrew/bin/gap','-q','-T',str(O/'driver.g')],600)
    run('canonical',[sys.executable,str(P/'canonical.py'),'--input',str(O/'validation.stdout'),'--out',str(O/'canonical_report.json')],15)
    actual=json.loads((O/'canonical_report.json').read_text());need(actual==json.loads((P/'expected.json').read_text()),'all literal classes and reversal maps')
    for row in actual['rows']:
        c=counts[str(row['rank'])];need(c['ordered']==row['ordered'] and c['self_dual']==row['self_dual'],'independent agreement with enumeration')
    damaged=0
    for name,text in [('truncated',(O/'validation.stdout').read_text().replace('COMPLETE_S10_VALIDATION','')),('duplicate',(O/'validation.stdout').read_text().replace('COMPLETE_S10_VALIDATION',next(x for x in (O/'validation.stdout').read_text().splitlines() if x.startswith('SOLUTION|'))+'\nCOMPLETE_S10_VALIDATION'))]:
        src=O/(name+'.txt');src.write_text(text);dest=O/(name+'.json')
        cp=subprocess.run([sys.executable,str(P/'canonical.py'),'--input',str(src),'--out',str(dest)],env=env,capture_output=True,timeout=15)
        (O/(name+'.stderr')).write_bytes(cp.stderr);need(cp.returncode!=0 and not dest.exists(),'damaged certificate rejection');damaged+=1
    guards=0
    for script in ['check.py','canonical.py']:
        for mode in ['argument','environment']:
            e=env.copy();cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:e['PYTHONOPTIMIZE']='1'
            target=O/(script+'_'+mode+'_forbidden')
            cp=subprocess.run(cmd+[str(P/script),'--out',str(target)],env=e,capture_output=True,timeout=10)
            (O/(script+'_'+mode+'.stderr')).write_bytes(cp.stderr)
            need(cp.returncode!=0 and b'unoptimized execution required' in cp.stderr and not target.exists(),'optimization rejected before output');guards+=1
    pages=None
    if args.render:
        N=O/'native';N.mkdir();shutil.copy2(P/'ten.tex',N/'ten.tex')
        for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','ten.tex'],45,N)
        from pypdf import PdfReader
        reader=PdfReader(N/'ten.pdf');pages=len(reader.pages);text='\n'.join(p.extract_text() or '' for p in reader.pages);(N/'text.txt').write_text(text)
        need('Overfull' not in (N/'ten.log').read_text() and 'LaTeX Warning' not in (N/'ten.log').read_text(),'native overflow/reference guard')
        if (P/'native_expected.txt').exists():need(text==(P/'native_expected.txt').read_text(),'exact native text')
        run('raster',['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','ten.pdf'],45,N)
    report=dict(status='PASS_COMPLETE_S10',exports=len(exports),dependencies=len(bindings),complete_branches=5,tuples=len(ids),subset_pairs=actual['subset_pairs'],counts=actual['rows'],damaged_controls=damaged,optimization_guards=guards,native_pages=pages,new_numeric_cells=4,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
