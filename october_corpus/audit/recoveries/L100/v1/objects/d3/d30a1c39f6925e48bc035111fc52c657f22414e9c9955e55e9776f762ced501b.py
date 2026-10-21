import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,json
from pathlib import Path
import replay as r
import fusion_join as f
P=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r.c.need(not a.out.exists(),'fresh output');C=r.Context();dp,tp,fp=r.paths();double,trunc,fusion=map(r.read,[dp,tp,fp]);maps=double['routes']+trunc['acquired_prefix_maps']+trunc['routes'];damages=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):damages.append(name);return
        raise ValueError('damage admitted '+name)
    for k,q in enumerate(maps):
        v=copy.deepcopy(q);v['object_images'].pop();reject(f'missing_object_{k}',lambda v=v:C.map(v))
        v=copy.deepcopy(q);v['automorphism_generator_images'][0][0]^=1;reject(f'wrong_generator_image_{k}',lambda v=v:C.map(v))
    v=copy.deepcopy(maps[0]);v['source_index']=1;reject('wrong_source_model',lambda:C.map(v))
    v=copy.deepcopy(maps[0]);v['point_type']=v['pair_type'];reject('same_point_pair_type',lambda:C.map(v))
    v=copy.deepcopy(maps[4]);v['source_types'][0]=v['source_types'][1];reject('duplicate_retained_type',lambda:C.map(v))
    text=(r.G/'incremental_target02/result.g').read_text();rows=f.extract(text)
    reject('fusion_missing_record',lambda:f.extract(text.replace('  members := [ rec(','  members := [ Rubbish(',1)))
    reject('fusion_unknown_expression',lambda:f.extract(text.replace('  members := [ rec(','  members := [ Evil(); rec(',1)))
    reject('fusion_duplicate_field',lambda:f.extract(text+'\n  members := []'))
    inv=r.read(r.G/'source_join_component_v2/diagram_inventory02.json')['rows'];comp=r.read(r.G/'source_join_component_v2/diagram_comparison01.json')['rows'];models={i:r.read(r.D/f'model{i}.json')for i in range(1,30)}
    bad=copy.deepcopy(inv);bad[0]['printed_G_conjugacy_fusion_multiplicity']+=1;reject('wrong_printed_multiplicity',lambda:f.join(rows,bad,comp,models))
    badrows=copy.deepcopy(rows);badrows[0]['representative']=[999,1];reject('unknown_fusion_class',lambda:f.join(badrows,inv,comp,models))
    a.out.mkdir(parents=True);result=dict(status='PASS_DOUBLING_JOIN_DAMAGED_CONTROLS',damaged_controls=damages,target_runs=0,new_censuses=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
