import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,json
from pathlib import Path
import verify as v
P=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();v.need(not a.out.exists(),'fresh output')
    d=v.load();cert=v.read(P/'expected/certificate.json');gs=v.geometries(d);passed=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):passed.append(name);return
        raise ValueError('damage admitted: '+name)
    for k in range(3):
        for name,change in [('missing_image',lambda r:r['object_images'].pop()),('duplicate_image',lambda r:r['object_images'].__setitem__(0,r['object_images'][1])),('wrong_base',lambda r:r['base_indices'].__setitem__(0,(r['base_indices'][0]+1)%210)),('wrong_type',lambda r:r['catalogue_to_source_types'].__setitem__(0,r['catalogue_to_source_types'][1])),('wrong_scope',lambda r:r.__setitem__('catalogue_index',11)),('wrong_count',lambda r:r['checks'].__setitem__('coset_members',60479))]:
            r=copy.deepcopy(cert['maps'][k]);change(r);reject(str(k)+'_'+name,lambda r=r,k=k:v.validate_map(r,d,gs[k]))
        for name,change in [('omitted_neighbour',lambda w:w['line_pair_baer_neighbours'].pop()),('wrong_join',lambda w:w.__setitem__('joining_line',w['line_pair'][0])),('degrees_rebound',lambda w:w.__setitem__('printed_degree',6))]:
            w=copy.deepcopy(cert['source_witnesses'][k]);change(w);reject(str(k)+'_'+name,lambda w=w,k=k:v.validate_witness(w,d['orbits'][k],d['meta']['lines']))
    e=copy.deepcopy(d);e['orbits'][1][0]=e['orbits'][0][0];reject('duplicate_subplane',lambda:v.validate_orbits(e))
    e=copy.deepcopy(d);e['orbits'][0].pop();reject('missing_subplane',lambda:v.validate_orbits(e))
    g=v.c.Geometry(d['orbits'][0],d['meta']['lines'])
    reject('printed_relation_cannot_replace_repair',lambda:v.validate_map(cert['maps'][0],d,g))
    # Both distinct conventions are tested, not just the expected output degrees.
    for k,w in enumerate(cert['source_witnesses']):
        g=gs[k];i=g.lookups[1][tuple(w['line_pair'])];j=g.lookups[2][w['point_pair']]
        v.need(g.incident(1,tuple(w['line_pair']),2,w['point_pair']),'original predicate accepts witness')
        v.need(not (g.adj[1,2][i]>>j&1),'corrected adjacency rejects witness')
    a.out.mkdir(parents=True);r=dict(status='PASS_BAER_LITERAL_CONTROLS',damaged_controls=passed,source_convention_controls=3,target_runs=0,subset_enumerations=0)
    (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
