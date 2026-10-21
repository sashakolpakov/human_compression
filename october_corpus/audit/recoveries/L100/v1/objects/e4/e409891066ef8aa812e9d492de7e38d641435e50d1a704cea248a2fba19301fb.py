import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,json
from pathlib import Path
import replay as r
def rejected(fn,label,out):
    try:fn()
    except (ValueError,KeyError,IndexError,TypeError)as e:out.append(dict(control=label,error=str(e)));return
    raise ValueError('damaged certificate accepted: '+label)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r.o.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);C=r.Context();out=[]
    maps=r.expected('recipes.json')['maps']+r.expected('ovals.json')['maps']
    for i,w in enumerate(maps):
        # A duplicate in one actual type must reject before any group reasoning.
        q=copy.deepcopy(w);index=q['catalogue_index'];m=r.read(r.G/f'palette_serialization_v1/derived/model{index}.json');t=m['types'][0];same=[a for a,u in enumerate(m['types'])if u==t]
        q['object_images'][same[1]]=q['object_images'][same[0]];rejected(lambda:C.validate(q),f'duplicate-object-map-{i}',out)
        q=copy.deepcopy(w);q['base_indices'][0]=-1;rejected(lambda:C.validate(q),f'negative-base-{i}',out)
    w=maps[0]
    for key,value in [('catalogue_index',25),('hyperoval_class',9),('source_pair_checks',0),('source_type_sizes',[1,1,1,1]),('automorphism','invented'),('target_to_derived_types',[1,1,2,3])]:
        q=copy.deepcopy(w);q[key]=value;rejected(lambda:C.validate(q),'wrong-'+key,out)
    for key in ['oval_hyperoval_class','dual_oval_hyperoval_class']:
        q=copy.deepcopy(maps[-1]);q[key]=9;rejected(lambda:C.validate(q),'wrong-'+key,out)
    q=copy.deepcopy(w);q['automorphism_generator_images'][0][0]=q['automorphism_generator_images'][0][1];rejected(lambda:C.validate(q),'wrong-actual-generator-image',out)
    # A bijective but altered map tests the all-coset-member identity, rather
    # than only its type/cardinality check.
    q=copy.deepcopy(w);m=r.read(r.G/f"palette_serialization_v1/derived/model{q['catalogue_index']}.json");ix=[a for a,t in enumerate(m['types'])if t==m['types'][0]][:2]
    q['object_images'][ix[0]],q['object_images'][ix[1]]=q['object_images'][ix[1]],q['object_images'][ix[0]];rejected(lambda:C.validate(q),'wrong-bijective-object-map',out)
    for field in ['point_mask','central_line_mask']:
        q=copy.deepcopy(r.expected('ambiguity.json'));q['witnesses'][0][field]^=2;rejected(lambda:r.ambiguity_checks(C,q),'bad-displayed-witness-'+field,out)
    q=copy.deepcopy(r.expected('ambiguity.json'));q['witnesses'][1]=copy.deepcopy(q['witnesses'][0]);rejected(lambda:r.ambiguity_checks(C,q),'same-completion-twice',out)
    q=copy.deepcopy(r.expected('ambiguity.json'));q['witnesses'][0]['literal_group_maps_from_first'][0][0]=q['witnesses'][0]['literal_group_maps_from_first'][0][1];rejected(lambda:r.ambiguity_checks(C,q),'nonpermutation-orbit-witness',out)
    # Actual group: an involution cannot replace the certified order-four
    # generator without destroying sixteen distinct normal forms.
    s=C.objects['stabilizers'][0]['structure'];aa=tuple(s['a']);bb=tuple(s['b']);zz=tuple(s['z']);e=tuple(range(21))
    r.o.need(r.o.mul(aa,aa)!=e and r.o.mul(bb,bb)==e,'genuine order4 versus order2 control')
    bad=[r.o.mul(r.o.mul(bb if i%2 else e,bb if j else e),zz if k else e)for i in range(4)for j in range(2)for k in range(2)]
    rejected(lambda:r.o.need(len(set(bad))==16,'sixteen distinct normal forms'),'collapsed-stabilizer-normal-forms',out)
    report=dict(status='PASS_L100_BUTTERFLY_OVAL_DAMAGED_CONTROLS',damages=len(out),controls=out,targets=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
