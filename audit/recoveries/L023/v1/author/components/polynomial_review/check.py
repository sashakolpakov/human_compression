"""Independent bounded review checker; never imports author implementation."""
from pathlib import Path
import argparse,copy,hashlib,json,re
from oracle import examine
HERE=Path(__file__).resolve().parent
PIN='c3b74315f9acf6d8c20a7045d5a795770b865bc835411cc3f14dcf771d9039e6'
QS=[3,4,5,7,8,9,11,13,16,17,19,23]
COUNTS=[[0,24],[24,24],[48,36],[96,96],[216,144],[192,192],
        [324,216],[432,576],[960,1920],[1440,624],[1020,1440],[2952,2160]]
PRINTED=[[0,24],[12,12],[48,36],[96,96],[162,108],[192,192],
         [324,216],[432,576],[840,1680],[1440,624],[1020,1440],[2952,2160]]
def need(x,m):
    if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(root,r):
    p=root/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'binding '+r['path'])
def validate(rows,scope):
    need([r['q'] for r in rows]==QS,'all twelve exact field sizes')
    for r,q,c,p in zip(rows,QS,COUNTS,PRINTED):
        total=(q+1 if q in [4,8,16] else q)*(q*q-1)
        need(r['nonscalar_total']==total,'complete proved solution count')
        need(r['primitive_counts']==c,'exact finite primitive columns')
        need(r['bc_zero_counts']==[x-y for x,y in zip(c,p)],'all even corrections are bc=0')
        need(len(r['seed_log_encoding'])==2 and all(len(x)==2 for x in r['seed_log_encoding']),'complete matrix seed')
    need(sum(r['nonscalar_total'] for r in rows)==33561,'whole finite census')
    need(scope['required_mathematical_programs']==['polynomial_table.g'],'whole required GAP')
    need(scope['new_original_credit']==scope['new_question_credit']==scope['new_Lean_declarations']==0,'bounded role')
    need(scope['new_factors'] is None,'no factor')
    need(len(scope['excluded'])==5 and 'WholeL023 recovery' in scope['excluded'],'no full-original acceptance')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output')
    if (HERE/'manifest.json').exists():
        for r in read(HERE/'manifest.json')['exports']:bound(HERE,r)
    b=a.author_root;need(sha(b/'manifest.json')==PIN,'exact reviewed author freeze')
    m=read(b/'manifest.json')
    for r in m['exports']:bound(b,r)
    rows=read(b/'polynomial_table_rows.json');scope=read(b/'scope.json');validate(rows,scope)
    tex=(b/'polynomial_solutions.tex').read_text()
    actual=[]
    for line in tex.splitlines():
        if re.fullmatch(r'\d+&\d+&\d+&\d+&\d+&\d+\\\\',line):
            actual.append([int(x) for x in line[:-2].split('&')])
    expected=[[q,r['nonscalar_total'],*c,*p] for q,r,c,p in zip(QS,rows,COUNTS,PRINTED)]
    need(actual==expected,'all twelve complete printed rows')
    own={'role':'distinct reviewer independent coordinate arithmetic','author_or_GAP_imports':False,
         'cases':[examine(*c) for c in [(2,2,[1,1,0]),(3,3,[1,2,0]),(4,2,[1,1,0,0,0,0]),(5,5,[1,1,0])]]}
    need(own==read(HERE/'oracle_results.json'),'fresh independent exhaustive fields')
    for c in own['cases']:
        if c['q'] in QS:
            r=rows[QS.index(c['q'])]
            need(all(c[k]==r[k] for k in ['nonscalar_total','primitive_counts','bc_zero_counts']),'independent finite table intersection')
    controls=[]
    def reject(name,rr,ss):
        try:validate(rr,ss)
        except (ValueError,KeyError,IndexError):controls.append(name);return
        raise ValueError('control passed '+name)
    for name,fn in [('drop row',lambda r:r.pop()),('duplicate field',lambda r:r[1].__setitem__('q',3)),
                    ('prune bc=0',lambda r:r[1].__setitem__('primitive_counts',[12,12])),
                    ('include scalar in total',lambda r:r[1].__setitem__('nonscalar_total',76)),
                    ('conceal boundary discrepancy',lambda r:r[1].__setitem__('bc_zero_counts',[0,0]))]:
        r=copy.deepcopy(rows);fn(r);reject(name,r,scope)
    for name,fn in [('omit required code',lambda s:s.__setitem__('required_mathematical_programs',[])),
                    ('grant source credit',lambda s:s.__setitem__('new_original_credit',1)),
                    ('grant formal credit',lambda s:s.__setitem__('new_Lean_declarations',1)),
                    ('invent factor',lambda s:s.__setitem__('new_factors',1)),
                    ('remove whole-original boundary',lambda s:s.__setitem__('excluded',[]))]:
        s=copy.deepcopy(scope);fn(s);reject(name,rows,s)
    report={'status':'PASS_DISTINCT_BOUNDED_REVIEW','author_manifest':PIN,'author_exports':len(m['exports']),
            'finite_rows':12,'complete_nonscalar_matrices':33561,'printed_rows':12,'own_complete_fields':[2,3,4,5],
            'own_projective_generation_orders':[504,9828],'negative_controls':controls,
            'no_author_code_import':True,'whole_L023_recovery':False}
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
