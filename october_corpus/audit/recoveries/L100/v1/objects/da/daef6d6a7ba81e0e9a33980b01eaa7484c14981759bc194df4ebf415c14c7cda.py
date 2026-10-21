import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,itertools,json
from pathlib import Path
import constructions as c

def partitions(n):
    a=[0]*n
    def go(i,maximum):
        if i==n:yield tuple(a);return
        for x in range(maximum+2):a[i]=x;yield from go(i+1,max(maximum,x))
    yield from go(1,0)

def partition_primitive(group):
    n=len(group[0])
    for p in partitions(n):
        if len(set(p)) in [1,n]:continue
        if all(all((p[a]==p[b])==(p[g[a]]==p[g[b]]) for a,b in itertools.combinations(range(n),2)) for g in group):return False
    return True

def report_check(report):
    c.need(report['status']=='PASS_LITERAL_L100_TWO_CONSTRUCTIONS_AND_TRUNCATIONS','result status')
    c.need(report['classification_claim'] is False and report['source_whole_credit']==0,'scope')
    c.need(report['truncation_checks']==8 and report['choice_isomorphisms']==24,'coverage counts')
    c.need([x['model'] for x in report['models']]==['5.1','5.2'],'two exact models')
    for r in report['models']:
        c.need(r['chambers']==20160 and len(r['flag_rows'])==32 and len(r['residue_rows'])==31,'flag coverage')
        c.need({tuple(x['types']) for x in r['flag_rows']}=={s for k in range(6) for s in itertools.combinations(range(5),k)},'all flag types')
        c.need(all(x['stabilizer_order']*x['count']==20160 for x in r['flag_rows']),'all stabilizer orders')
        panel=sorted((x['remaining_types'][0],x['two_transitive_actions'][0]) for x in r['residue_rows'] if len(x['remaining_types'])==1)
        c.need(panel==list(enumerate([False,True,True,True,True])),'exact local2T boundary')
        c.need(all(any(x['primitive_actions']) for x in r['residue_rows']),'RWPRI output')
        c.need(all(x['IP2_if_rank_two'] is True for x in r['residue_rows'] if len(x['remaining_types'])==2),'IP2 output')
        if r['model']=='5.1':c.need(r['rank_two_extension_table']==c.TABLE1,'source twenty entries')

def main():
    p=argparse.ArgumentParser();p.add_argument('--model-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    c.need(not a.out.exists(),'output exists');a.out.mkdir(parents=True)
    d=json.loads((a.model_dir/'model.json').read_text());r=json.loads((a.model_dir/'report.json').read_text());report_check(r)
    cases=[]
    for n in range(2,7):
        cycle=tuple((i+1)%n for i in range(n));flip=tuple((-i)%n for i in range(n));swap=tuple(1 if i==0 else 0 if i==1 else i for i in range(n))
        for extra in [(),(flip,),(swap,)]:
            g=c.closure([cycle,*extra],n);fast=c.primitive_action(g);slow=partition_primitive(g)
            c.need(fast==slow,'independent partition oracle');cases.append({'degree':n,'order':len(g),'primitive':fast})
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError):rejected.append(name)
        else:raise ValueError('damage accepted: '+name)
    damaged=copy.deepcopy(d['lines']);damaged[1]=damaged[0];reject('duplicate plane line',lambda:c.plane_tables(damaged))
    bad=tuple([1,0,*range(2,21)]);pts,_=c.coordinate_plane();reject('nonprojective input permutation',lambda:c.matrix_for(bad,pts))
    geom=c.Geometry(d,'5.1');target=c.Geometry(d,'5.1');target.adj[0,1][0]^=1
    reject('changed literal incidence',lambda:c.check_isomorphism(geom,target,tuple(range(21))))
    reject('repeated hyperoval orbit',lambda:c.Geometry(d,'5.1',(0,0)))
    target=c.Geometry(d,'5.1',(1,0));reject('wrong hyperoval image target',lambda:c.check_isomorphism(geom,target,tuple(range(21))))
    for name,edit in [
        ('wrong chamber number',lambda x:x['models'][0].update(chambers=20159)),
        ('missing flag type',lambda x:x['models'][0]['flag_rows'].pop()),
        ('wrong table entry',lambda x:x['models'][0]['rank_two_extension_table']['012'].update({'3':4})),
        ('blanket local2T assertion',lambda x:next(y for y in x['models'][0]['residue_rows'] if y['remaining_types']==[0]).update(two_transitive_actions=[True])),
        ('lost IP2 test',lambda x:next(y for y in x['models'][0]['residue_rows'] if len(y['remaining_types'])==2).update(IP2_if_rank_two=False)),
        ('whole classification overclaim',lambda x:x.update(classification_claim=True))]:
        v=copy.deepcopy(r);edit(v);reject(name,lambda v=v:report_check(v))
    report={'status':'PASS_L100_CONSTRUCTION_CONTROLS','partition_oracle_cases':cases,'damages_rejected':rejected,'target_censuses':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(cases),len(rejected))
if __name__=='__main__':main()
