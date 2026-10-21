"""Explicit erratum layer; retain the original transcription and literal failed join."""
from copy import deepcopy
from pathlib import Path
import json
from join import compare
H=Path(__file__).resolve().parent

def corrected(source,result):
    revised=deepcopy(source);changes=[]
    for n in [12,18,23,35]:
        row=revised['table3'][n-1]
        before=[row['point_diameter'],row['gonality'],row['line_diameter']]
        if before != ([3,2,4] if n in [12,18] else [3,3,4]):raise ValueError('Exact printed erratum input')
        row['point_diameter'],row['line_diameter']=row['line_diameter'],row['point_diameter']
        changes.append(dict(source_row=n,printed_triple=before,corrected_triple=[row['point_diameter'],row['gonality'],row['line_diameter']],rule='Keep printed G1/G2 columns; exchange the two type diameters.',reason='Section3 defines the point diameter at a G1 coset. The literal incidence graph gives the opposite orientation to the printed triple.'))
    joined=compare(revised,result)
    joined['explicit_source_corrections']=changes
    joined['source_transcription_modified']=False
    joined['correction_changes_only_two_type_diameters']=True
    return joined
if __name__=='__main__':
    source=json.loads((H/'printed.json').read_text());result=json.loads((H.parent/'m11_graph_execution01/stdout').read_text())
    out=H/'source_join_corrected.json'
    if out.exists():raise ValueError('Fresh corrected comparison required')
    joined=corrected(source,result);out.write_text(json.dumps(joined,indent=2)+'\n')
    print(json.dumps({k:joined[k] for k in ['status','actual_orbits','source_rows_with_no_candidate','explicit_source_corrections']}))
