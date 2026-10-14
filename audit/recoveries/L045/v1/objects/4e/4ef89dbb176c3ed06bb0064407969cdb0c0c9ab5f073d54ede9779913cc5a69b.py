"""Validate the private principal contract; does not rerun acquired censuses."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse
import copy
import hashlib
import json
from pathlib import Path

def need(x,message):
    if not x:raise ValueError(message)

def validate(claims,coverage,components,complete=False):
    need(claims['whole_original_credit']==claims['measurement_credit']==claims['new_question_credit']==0,'no premature credit')
    rows={r['id']:r for r in claims['claims']}
    need(len(rows)==len(claims['claims'])==36,'exact claim roster')
    need(rows['P1']['route']==['P1A','P1S','P1E','P1L','P1Sp','P1O','P1F'],'complete positive family routing')
    need(rows['P2']['route']==['P1','G1'],'exact geometric bridge')
    need(rows['N3']['status']=='SOURCE_ANNOUNCEMENT_NOT_A_PROVED_RESULT','announced negative is not proved here')
    need(rows['N1']['positive_proof_dependency']==rows['N2']['positive_proof_dependency']==False,'negative antecedents not positive proof premises')
    need(rows['G2']['kind']=='historical_antecedent','regular classification remains historical')
    need(rows['H_ON']['status']=='NOT_USED_OR_IMPORTED','O Nan historical total not imported')
    need(rows['Q7']['status']=='DEFERRED_ORIGINAL_QUESTION_NO_CREDIT','almost-simple question not claimed solved')
    for key in ['H_count_M11','H_count_M12','H_count_M22','H_count_J1','H_count_J2']:
        need(rows[key]['status']=='ATTRIBUTED_NOT_RECOUNTED','no new ancillary census')
    ordinary={'M11','M12','M22','M23','M24','J1','J2','J3','J4','Co1','Co2','Co3','Fi22','Fi23','Fi24prime','Monster','BabyMonster','Th','Ly','ON','HN','Ru','HS','He','Suz','McL'}
    one=coverage['sporadic_twelve'];two=coverage['sporadic_fourteen']
    need(len(one)==12 and len(two)==14 and not set(one)&set(two) and set(one+two)==ordinary,'exact disjoint 26 sporadics')
    initial=[(s,n,q) for s in ['L','U'] for n,q in [(4,2),(4,3),(4,4),(5,2),(6,2)]]
    initial += [('S',n,q) for n,q in [(4,3),(4,4),(6,2),(6,3),(8,2)]]
    initial += [('O',7,3),('O+',8,2),('O-',8,2),('O+',8,3),('O+',10,2),('O-',10,2)]
    second=[(s,n,q) for s in ['L','U'] for n,q in [(5,3),(6,3),(8,2)]]
    second += [('S',6,4),('S',8,3),('S',8,4),('O+',12,2),('O-',12,2)]
    exceptional=[('G',2,3),('G',2,4),('T',)]
    need((len(initial),len(second),len(exceptional))==(21,11,3),'independently expanded source parameter inventory')
    actual=[tuple(r['parameters']) for r in coverage['finite_parameter_routes']]
    need(len(actual)==len(set(actual))==35 and set(actual)==set(initial+second+exceptional),'all finite source parameters, no nonsimple insertion')
    need(coverage['excluded_nonsimple']['parameters']==['S',4,2],'nonsimple Sp4(2) qualification')
    cs=components['components'];need(len(cs)==13 and len({c['id'] for c in cs})==13,'full mathematical roots')
    pending=[c['id'] for c in cs if c['review_state']=='PENDING_DISTINCT_REVIEW']
    need(not pending,'principal freeze blocked by pending distinct review')
    orth=next(c for c in cs if c['id']=='orthogonal_counting')
    need(set(orth['manifests'])=={'author','distinct_review','root_adoption'},'complete counting acceptance')
    need(orth['discharged_cover_interface']['component']=='d4_cover','exact D4 cover join')
    need(orth['discharged_cover_interface']['historical_author_status_preserved'],'historical author scope retained')
    need(rows['P1']['status']==rows['P1O']['status']=='COMPLETE_POSITIVE_PRINCIPAL_ASSEMBLY' and rows['P1']['conditional_on']==[],'closed principal assembly')
    need('shared' in next(c for c in cs if c['id']=='d4_cover')['review_limit'],'shared multiplicity roles disclosed')
    return dict(source_claims=len(rows),finite_parameters=len(actual),sporadics=26,components=len(cs),pending=pending)

def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--require-complete',action='store_true');a=p.parse_args()
    P=Path(__file__).resolve().parent;S=a.study.resolve();O=a.out.resolve()
    need(not O.exists(),'fresh output')
    claims=json.loads((P/'claim_register.json').read_text());coverage=json.loads((P/'coverage.json').read_text());components=json.loads((P/'components.json').read_text())
    report=validate(claims,coverage,components,a.require_complete)
    bindings=json.loads((P/'direct_bindings.json').read_text())
    for row in bindings:
        data=(S/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'exact acquired bytes '+row['path'])
    negatives=[]
    for name in ['missing_family','false_announcement','regular_as_principal','new_count','missing_finite','nonsimple_finite','sporadic_overlap']:
        c=copy.deepcopy(claims);v=copy.deepcopy(coverage);m=copy.deepcopy(components)
        byid={r['id']:r for r in c['claims']}
        if name=='missing_family':byid['P1']['route'].remove('P1O')
        elif name=='false_announcement':byid['N3']['status']='ACCEPTED_PRINCIPAL_NEGATIVE'
        elif name=='regular_as_principal':byid['G2']['kind']='principal'
        elif name=='new_count':byid['H_count_M11']['status']='NEW_EXHAUSTIVE_COUNT'
        elif name=='missing_finite':v['finite_parameter_routes'].pop()
        elif name=='nonsimple_finite':v['finite_parameter_routes'][0]['parameters']=['S',4,2]
        else:v['sporadic_fourteen'][0]=v['sporadic_twelve'][0]
        try:validate(c,v,m)
        except ValueError:negatives.append(name)
        else:raise ValueError('damaged source contract accepted '+name)
    damaged=copy.deepcopy(components)
    next(c for c in damaged['components'] if c['id']=='orthogonal_counting')['review_state']='PENDING_DISTINCT_REVIEW'
    try:validate(claims,coverage,damaged,True)
    except ValueError:negatives.append('premature_complete_gate')
    else:raise ValueError('damaged pending assembly passed complete gate')
    O.mkdir(parents=True)
    report.update(status='PASS_COMPLETE_POSITIVE_PRINCIPAL_REGISTER',bindings=len(bindings),damaged_controls=negatives,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
