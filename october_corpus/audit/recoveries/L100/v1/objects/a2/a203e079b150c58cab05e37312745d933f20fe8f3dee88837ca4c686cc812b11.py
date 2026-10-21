import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def read(p):return json.loads(p.read_text())
def need(v,s):
    if not v:raise ValueError(s)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
SPEC=[
('2.1','Gamma','AutG',7),('2.2','Sigma','Sigma',7),('2.3','V','V',7),('2.4','G:2','V',7),('2.5','Sigma','Sigma',8),('2.6','AutG','C2xAutG',8),('2.7','AutG','AutG',8),
('3.1','Sigma','Sigma',8),('3.2','V','C2xV',8),('3.3','Sigma','V',8),('3.4','Sigma','V',9),('3.5','Sigma','V',9),('3.6','G','Sigma',9),('3.7','Gamma','AutG',9),
('4.1','G','Sigma',9),('4.2','Sigma','V',10),('4.3','Sigma','V',10),('4.4','Sigma','Sigma',10),('4.5','Sigma','Sigma',10),('4.6','Sigma','Sigma',11),('4.7','Sigma','V',11),('4.8','G','C2xSigma',11),('4.9','G','Sigma',11),('4.10','G','G',12),('4.11','G','Sigma',12),
('5.1','G','G',12),('5.2','G','Sigma',13),('5.3','G','C2xSigma',13),('5.4','G','C2xG',13)]
def subgroup(table,generators):
    result=[0]
    for x in result:
        for y in generators:
            z=table[x][y]
            if z not in result:result.append(z)
    return set(result)
def join(results):
    coord=read(results[0]/'coordinate_group.json');names=coord['names'];table=coord['table']
    need(len(table)==12 and all(len(r)==12 for r in table),'exact coordinate table')
    index={name:i for i,name in enumerate(names)}
    f=index['diagonal0_field1'];d=index['diagonal1_field0'];t=index['duality'];u=index['diagonal0_field1_duality']
    representatives={'G':{0},'Sigma':subgroup(table,[f]),'Graph':subgroup(table,[t]),'Unitary':subgroup(table,[u]),'Gamma':subgroup(table,[d,f]),'V':subgroup(table,[f,t]),'AutG':set(range(12))}
    inverses=[next(j for j in range(12) if table[i][j]==table[j][i]==0)for i in range(12)]
    def identify(T):
        matches=[]
        for name,U in representatives.items():
            for h in range(12):
                if {table[table[inverses[h]][x]][h]for x in T}==U:matches.append((name,h))
        need(matches and len({x[0]for x in matches})==1,'unique precise outer conjugacy class')
        return matches[0]
    comparison=read(G/'source_join_component_v2/diagram_comparison01.json')['rows']
    labelmap={r['label']:r['candidates'][0]['catalogue_index']for r in comparison}
    inputs=[pin(G/'source_join_component_v2/diagram_comparison01.json')]+[pin(p/'coordinate_group.json')for p in results]
    rows=[]
    for label,typed,corr,page in SPEC:
        i=labelmap[label];paths=[p/f'model{i}.json'for p in results if(p/f'model{i}.json').exists()]
        need(len(paths)==1,'exact one acquired result per model');r=read(paths[0]);inputs.append(pin(paths[0]));out={}
        for profile,printed in [('typed',typed),('correlations',corr)]:
            p=r['profiles'][profile];name,h=identify(set(p['outer_indices']));actual=('C2x'if p['kernel_order']==2 else'')+name
            matches=actual==printed or printed=='G:2'and p['kernel_order']==1 and len(p['outer_indices'])==2
            out[profile]=dict(printed=printed,actual=actual,outer_conjugator=h,kernel_order=p['kernel_order'],order=p['acquired_order'],matches_under_explicit_notation=matches)
        rows.append(dict(source_label=label,physical_page=page,catalogue_index=i,profiles=out))
    differences=[(r['source_label'],k)for r in rows for k,v in r['profiles'].items()if not v['matches_under_explicit_notation']]
    need(differences==[('3.5','typed'),('4.11','correlations')],'exact two structural-name differences; no numerical inference')
    return dict(status='LITERAL_AUT_COR_SOURCE_JOIN',rows=rows,inputs=inputs,differences=differences,
        notation={'G':'PSL3(4)','Sigma':'G extended by coordinate field involution','Graph':'G extended by inverse-transpose graph involution','Unitary':'G extended by commuting field times graph involution','Gamma':'G extended by diagonal and field maps','V':'G extended by field and graph maps','AutG':'complete Aut(G)','C2x':'certified split central direct factor'},
        source_qualification='The same printed P-Sigma name occurs for three mutually nonisomorphic groups. The two corrections use the explicit field-extension convention; no universal interpretation of unspecified :2 is imposed.',source_credit=0)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,nargs='+',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.write_text(json.dumps(join(a.results),indent=2)+'\n')
if __name__=='__main__':main()
