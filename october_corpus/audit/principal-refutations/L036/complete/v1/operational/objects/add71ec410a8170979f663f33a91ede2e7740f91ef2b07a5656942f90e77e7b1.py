"""Compare actual finite invariants with source rows; retain ambiguity and failure."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
GROUPS={'GL2(3)':27,'S5':34,'L2(11)':37,'M9 : 2':35,'M10':38}
# These shapes are imported only after the actual ambient conjugator is checked.
INTERSECTIONS={'1':{1},'C2':{2},'C4':{5},'E4':{4},'S3':{7,8},
               'D8':{12},'D12':{17},'Q8 : 2':{18},'A5':{29,30},'M9':{31}}

def design_matches(d,source):
    if (d['v'],d['k'])!=(source['v'],source['k']):return False
    if d['complete_incidence']:
        return 1<=source['t']<=d['k'] and d['constant_lambda']==source['lambda_value']
    return any(r['t']==source['t'] and r['lambda_value']==source['lambda_value'] for r in d['uniform_counts'])


def compare(source,result):
    designs={i:[r for r in source['table4'] if r['row']==i] for i in range(1,38)}
    choices={}
    for s in source['table3']:
        values=[]
        for g in result['graphs']:
            cname=s['intersection'];actual=g['intersection_class_witness'][0]
            if cname.isdigit():
                if g['intersection_order']!=int(cname):continue
            elif actual not in INTERSECTIONS[cname]:continue
            orientations=[]
            for side in [0,1]:
                m=g['metrics']
                dd=[m['point_diameter'],m['line_diameter']]
                if [g['subgroup_classes'][side],g['subgroup_classes'][1-side]] != [GROUPS[s['G1']],GROUPS[s['G2']]]:continue
                if [dd[side],m['gonality'],dd[1-side]] != [s['point_diameter'],s['gonality'],s['line_diameter']]:continue
                orientations.append(side)
            if not orientations:continue
            design_sides=[]
            if designs[s['row']]:
                for side in [0,1]:
                    if all(design_matches(g['designs'][side if not d['dual'] else 1-side],d) for d in designs[s['row']]):design_sides.append(side)
                if not design_sides:continue
            elif not all(d['complete_incidence'] for d in g['designs']):continue
            values.append(dict(orbit=g['orbit'],geometry_point_sides=orientations,design_point_sides=design_sides))
        choices[s['row']]=values
    owner={};assignment={}
    def assign(row,seen):
        for candidate in choices[row]:
            orbit=candidate['orbit']
            if orbit in seen:continue
            seen.add(orbit)
            if orbit not in owner or assign(owner[orbit],seen):
                owner[orbit]=row;assignment[row]=candidate;return True
        return False
    matched=all(assign(row,set()) for row in range(1,38))
    return dict(status='ALL_PRINTED_ROWS_MATCH' if matched else 'PRINTED_ROW_DISCREPANCY',
        source_pdf_sha256=source['source_pdf_sha256'],source_rows=37,source_design_rows=70,
        actual_orbits=result['number_of_orbits'],candidate_joins={str(k):v for k,v in choices.items()},
        selected_bijection=[dict(source_row=row,**assignment[row]) for row in sorted(assignment)] if matched else None,
        source_rows_with_no_candidate=[i for i,v in choices.items() if not v],
        embedding_unique_from_printed_invariants=False,source_profile_ambiguities={str(k):v for k,v in choices.items() if len(v)>1},
        omitted_complete_incidence_rows=[31,32],numeric_values_automatically_repaired=False,
        design_orientation_is_recorded_separately=True)
