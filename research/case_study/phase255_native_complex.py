#!/usr/bin/env python3
"""Build the Tomotope end-coset complex independently in native GAP.

No phase246 cell or voltage implementation is imported. The retained literal
flag model supplies only the four input permutations.
"""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--gap', default='/opt/homebrew/bin/gap')
    args = p.parse_args()
    if args.out.exists():
        raise ValueError('fresh output required')
    args.out.mkdir(parents=True)
    model = json.loads((args.root/'phase211_literal_Tomotope_model.json').read_text())
    marks = '['+','.join('PermList('+str(x)+')' for x in model['generators'])+']'
    program = 'marks:='+marks+';;\n'+r'''
G:=Group(marks);;
A:=Subgroup(G,marks{[1,2,3]});;B:=Subgroup(G,marks{[2,3,4]});;
C:=Subgroup(G,marks{[2,3]});;D:=Intersection(A,B);;
ac:=RightCosets(G,A);;bc:=RightCosets(G,B);;cc:=RightCosets(G,C);;
alpha:=ActionHomomorphism(G,cc,OnRight);;
ends:=List(cc,c->[Position(ac,RightCoset(A,Representative(c)))-1,
                 Length(ac)+Position(bc,RightCoset(B,Representative(c)))-1]);;
e0:=Position(cc,RightCoset(C,One(G)));;
seed:=List([One(G),marks[1],marks[1]*marks[4],marks[4]],g->Position(cc,RightCoset(C,g)));;
cells:=Orbit(Image(alpha),seed,OnTuples);;
defects:=Difference(Orbit(Image(alpha,D),e0),[e0]);;
Print("{\"group_order\":",Size(G),",\"orders\":[",Size(A),",",Size(B),",",Size(C),",",Size(D),"],");
Print("\"vertices\":",Length(ac)+Length(bc),",\"edges\":",Length(cc),",\"base_edge\":",e0-1,",");
Print("\"endpoints\":",ends,",\"cells\":",List(cells,c->List(c,x->x-1)),",");
Print("\"defects\":",List(defects,x->x-1),"}\n");
QUIT_GAP(0);
'''
    script = args.out/'native.g'
    script.write_text(program)
    run = subprocess.run([args.gap,'-q','-T',str(script)],text=True,capture_output=True,timeout=120)
    (args.out/'native.stdout').write_text(run.stdout)
    (args.out/'native.stderr').write_text(run.stderr)
    if run.returncode or run.stderr or 'Error' in run.stdout:
        raise ValueError('native GAP construction failed: '+run.stderr+run.stdout[-1000:])
    data = json.loads(run.stdout)
    boundaries = []
    for cell in data['cells']:
        row = {}
        for edge,sign in zip(cell,[1,-1,1,-1]):
            row[edge] = row.get(edge,0)+sign
        row = {e:v for e,v in row.items() if v}
        boundary = [0]*data['vertices']
        for edge,coeff in row.items():
            a,b = data['endpoints'][edge]
            boundary[a] -= coeff
            boundary[b] += coeff
        if any(boundary):
            raise ValueError('native translated square is not a cycle')
        boundaries.append(row)
    if data['base_edge'] != 0:
        raise ValueError('integer checker requires base edge zero; explicitly reindex')
    if any(data['endpoints'][e]!=data['endpoints'][0] for e in data['defects']):
        raise ValueError('native defects are not parallel edges')
    report = {
        'name':'Tomotope independently reconstructed in GAP',
        'group_order':data['group_order'],
        'A_order':data['orders'][0], 'B_order':data['orders'][1],
        'C_order':data['orders'][2], 'D_order':data['orders'][3],
        'graph_vertices':data['vertices'], 'graph_edges':data['edges'],
        'square_relator_rows':len(boundaries), 'defect_edges':data['defects'],
        'complex':{'endpoints':data['endpoints'],'boundaries':boundaries},
        'method':'Native GAP right cosets and complete orbit of the square under the induced right action; no phase246 geometry code imported.',
    }
    (args.out/'complex.json').write_text(json.dumps(report)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='complex'},indent=2))


if __name__=='__main__':
    main()
