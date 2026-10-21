#!/usr/bin/env python3
"""Exact replay of locally faithful abelian-cover criteria and Tomotope model."""
import argparse,hashlib,json,os,pathlib,re,subprocess,sys,time
from phase246_parallel_edges import analyze,need
from phase246_voltage import cover
from phase245_tomotope_integral import eliminate_units
ROOT=pathlib.Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def integer_small(data):
    E=data['complex']['endpoints'];rows=[{int(k):v for k,v in r.items()} for r in data['complex']['boundaries']]
    nv=data['graph_vertices'];parents=list(range(nv))
    def root(i):
        while parents[i]!=i:i=parents[i]
        return i
    tree=[]
    for e,(a,b) in enumerate(E):
        a,b=root(a),root(b)
        if a!=b:parents[a]=b;tree.append(e)
    need(len(tree)==nv-1,'small connected graph')
    cols=set(range(len(E)))-set(tree)
    vectors=[{e:a for e,a in {j:1,0:-1}.items() if e in cols} for j in data['defect_edges']]
    residual,active,vs,ops=eliminate_units([{e:a for e,a in r.items() if e in cols} for r in rows],cols,vectors)
    need(all(a%2==0 for r in residual for a in r.values()),'small integer lattice even')
    final,remaining,_,ops2=eliminate_units([{e:a//2 for e,a in r.items()} for r in residual],active,[])
    need(not final and not remaining and len(ops2)==len(active),'small residual lattice exactly twice the free lattice')
    images=[[v.get(c,0)%2 for c in active] for v in vs]
    need(all(any(v) for v in images),'small integral defects survive')
    return dict(integer_H1=[2]*len(active),unit_pivots=len(ops),defect_images=images,unit_operations=ops,halved_operations=ops2)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--gap',type=pathlib.Path,required=True);ap.add_argument('--lean',type=pathlib.Path,required=True);ap.add_argument('--packages',type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output path')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output path');out.mkdir(parents=True)
    start=time.monotonic()
    def run(label,args,env=None,timeout=180):
        t=time.monotonic();r=subprocess.run([str(x) for x in args],cwd=out,env=env,text=True,capture_output=True,timeout=timeout)
        for suffix,s in [('stdout',r.stdout),('stderr',r.stderr)]: (out/(label+'.'+suffix)).write_text(s)
        return r,dict(label=label,returncode=r.returncode,seconds=round(time.monotonic()-t,3))
    inputs={}
    def read(name):
        p=ROOT/name;inputs[name]=sha(p);return json.loads(p.read_text())
    specifications=[('diagnostic32',read('phase224_small_models.json')[0],32,1),('D256',read('phase109_cover_families_generalization_model.json'),256,2),('Tomotope',read('phase211_literal_Tomotope_model.json'),18432,2)]
    cells=[];small=[]
    for name,model,order,dim in specifications:
        data=analyze(model,primes=(2,3,5,7),complex_data=True)
        need(data['group_order']==order,'base order '+name)
        need([x['H1_dimension'] for x in data['fields']]==[dim,0,0,0],'field homology dimensions '+name)
        need(data['fields'][0]['C_group'] and all(not x['C_group'] for x in data['fields'][1:]),'defect field conditions '+name)
        (out/(name+'_complex.json')).write_text(json.dumps(data)+'\n')
        cells.append({k:v for k,v in data.items() if k!='complex'})
        if name!='Tomotope':small.append(dict(name=name,certificate=integer_small(data)))
        else:
            # Exact same literal rows as the separately frozen independent audit.
            frozen=read('phase245_tomotope_complex.json')
            need(json.loads(json.dumps(data['complex']))==frozen['complex'] and data['defect_edges']==frozen['defect_edges'],'independent integer input matches fresh geometry')
            tomotope=model;tomodata=data
    (out/'small_integral.json').write_text(json.dumps(small,indent=2)+'\n')
    rr,integral=run('integer',[sys.executable,'-B','-O',ROOT/'phase245_tomotope_integral.py','--input',out/'Tomotope_complex.json','--out',out/'Tomotope_integral.json'])
    need(rr.returncode==0 and '"status": "PASS"' in rr.stdout,'independent integral replay')
    bad=json.loads(json.dumps(tomodata));edge=bad['defect_edges'][0]
    bad['complex']['boundaries'].append({str(edge):1,'0':-1});bad['square_relator_rows']+=1
    (out/'bad_defect_complex.json').write_text(json.dumps(bad)+'\n')
    rr,c1=run('control_killed_defect',[sys.executable,'-B','-O',ROOT/'phase245_tomotope_integral.py','--input',out/'bad_defect_complex.json','--out',out/'bad_defect_report.json'])
    need(rr.returncode!=0 and 'unit invariant factors' in rr.stderr,'killed defect rejection')
    voltage=cover(tomotope);need(voltage['degree']==73728 and voltage['kernel_dimension']==2,'Tomotope voltage degree')
    (out/'Tomotope_voltage.json').write_text(json.dumps(voltage)+'\n')
    def marks(gs):return '['+','.join('PermList('+str(g)+')' for g in gs)+']'
    def program(model,expected):
        return 'HMarks:='+marks(model['generators'])+';;\nGMarks:='+marks(model['base_generators'])+';;\nExpectedKernelOrder:='+str(expected)+';;\n'+(ROOT/'phase246_voltage_check.g').read_text()
    fp=out/'finite.g';fp.write_text(program(voltage,4))
    rr,finite=run('finite',[a.gap,'-q','-T',fp],timeout=240)
    need(rr.returncode==0 and 'PHASE246_VOLTAGE_PASS' in rr.stdout and 'PHASE246_MINIMAL' in rr.stdout and not re.search(r'Error|warning',rr.stdout+rr.stderr),'actual finite group replay')
    need('normal_kernel_lines=1 good_lines=1' in rr.stdout and re.search(r'minimal_quotient_orders=\s*\[ 36864 \]',rr.stdout),'unique minimal abelian quotient')
    bv=dict(voltage);n=voltage['base_order'];bv['generators']=[[((x-1)%n)+(j//n)*n+1 for j,x in enumerate(s)] for s in voltage['generators']]
    bp=out/'bad_voltage.g';bp.write_text(program(bv,4))
    rr,c2=run('control_zero_voltage',[a.gap,'-q','-T',bp])
    need(rr.returncode!=0 and 'PHASE246_REJECT connected actual voltage action' in rr.stdout,'discarded voltage rejection')
    bp=out/'bad_kernel.g';bp.write_text(program(voltage,2))
    rr,c3=run('control_kernel_order',[a.gap,'-q','-T',bp])
    need(rr.returncode!=0 and 'PHASE246_REJECT actual elementary abelian kernel' in rr.stdout,'incorrect claimed kernel rejection')
    pins=read('formal/dependency_manifest.json');dependencies=[]
    for item in pins['packages']:
        pp=a.packages/item['name'];rev=subprocess.check_output(['git','-C',pp,'rev-parse','HEAD'],text=True).strip()
        need(rev==item['rev'] and subprocess.run(['git','-C',pp,'diff','--quiet','HEAD','--']).returncode==0,'pinned clean Lean dependency '+item['name'])
        dependencies.append(dict(name=item['name'],revision=rev))
    leanversion=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in leanversion,'Lean version')
    formal=ROOT/'phase246_formal/LocallyFaithfulIntersection.lean';source=formal.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',source,re.M),'no proof holes')
    cp=out/formal.name;cp.write_text(source)
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    rr,lean=run('formal',[a.lean,'-o',out/'LocallyFaithfulIntersection.olean',cp],env)
    need(rr.returncode==0 and not re.search(r'error:|warning:|sorryAx',rr.stdout+rr.stderr),'Lean compilation')
    axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",rr.stdout)
    need(len(axioms)==3 and all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in axioms),'three Lean standard-axiom declarations')
    # The injectivity hypothesis is essential: with f:C2→1 and q=id,
    # A=B=C2,C=1, the discrepancy condition is vacuous but intersection false.
    aa=bb={0,1};cc={0};ff=lambda x:0;qq=lambda x:x
    vacuous=all(ff(x)!=ff(y) or ff(x) in {ff(z) for z in cc} or qq((x-y)%2)!=0 for x in aa for y in bb)
    need(vacuous and ({qq(x) for x in aa}&{qq(x) for x in bb})!={qq(z) for z in cc},'actual C2 counterexample without end injectivity')
    for name in ['phase246_parallel_edges.py','phase246_voltage.py','phase246_voltage_check.g','phase246_check.py','phase246_formal/LocallyFaithfulIntersection.lean','phase245_tomotope_integral.py','phase245_integer_manifest.json']:inputs[name]=sha(ROOT/name)
    generated={p.name:dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.iterdir()) if p.is_file()}
    report=dict(generated_artifacts=generated,status='PASS',seconds=round(time.monotonic()-start,3),cells=cells,independent_integral=integral,finite=finite,negative_controls=[c1,c2,c3],formal=lean,axiom_reports=axioms,dependencies=dependencies,lean_version=leanversion,inputs=inputs,
        scope='Exact abelian locally faithful cover criterion; Tomotope abelian-kernel classification and all-odd-prime obstruction. No general finite multiplicity solution; written topology is not Lean-formalized.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',seconds=report['seconds'],models=3,finite_cover_order=73728,minimal_abelian_cover_order=36864,Lean_declarations=3)))
if __name__=='__main__':main()
