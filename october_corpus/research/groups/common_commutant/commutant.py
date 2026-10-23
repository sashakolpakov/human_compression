"""Byte-exact selected project definitions; see provenance/source_derivation.json.
No original host paths or project runtime are imported.
"""

SCHEMA='F004_Q8_621_COMMON_COMMUTANT_CERTIFICATE_V1'

def need(ok,why):
    if not ok:raise ValueError(why)

def commute(a,x,y):
    return a.product(x,y)==a.product(y,x)

def escape(a,x,ambient):
    need(len(ambient)==2,'exact two original ambient generator images')
    for g,m in enumerate(ambient,1):
        left=a.product(x,m);right=a.product(m,x)
        for i,(u,v)in enumerate(zip(left,right)):
            if u!=v:return dict(generator=g,row=i//6+1,column=i%6+1,left=u,right=v)
    return None

def verify(a,marks,ambient,certificate):
    need(type(marks)is list and len(marks)==21 and type(ambient)is list and len(ambient)==2,'fixed3/K9/H9 and original2 order')
    need(type(certificate)is dict and set(certificate)=={'schema','status','X','ambient_escape','all21_commutations','raw_621_domain','new_job_or_Original_or_Lean_credit'},'whole witness fields')
    need(certificate['schema']==SCHEMA and certificate['raw_621_domain']==dict(original_job=[621,5],namespace='NEW_UNQUOTIENTED_KH_INVOLUTION_CARTESIAN_V1',K_involutions=511,H_involutions=119,raw_pair_slots=60809)
         and type(certificate['new_job_or_Original_or_Lean_credit'])is int and certificate['new_job_or_Original_or_Lean_credit']==0,'exact domain and zero administrative credit')
    if certificate['status']=='UNPAID_NO_WITNESS':
        need(certificate['X']is certificate['ambient_escape']is None and certificate['all21_commutations']is False,'miss is inconclusive')
        a.charge(0);return False
    need(certificate['status']=='CERTIFIED_UNIFORM_NONGENERATION'and certificate['all21_commutations']is True,'positive exact witness status')
    x=a.literal(certificate['X'])
    for m in marks:need(commute(a,x,m),'actual commutation with EVERY fixed/basis image')
    e=certificate['ambient_escape']
    need(type(e)is dict and set(e)=={'generator','row','column','left','right'}and all(type(e[k])is int for k in e),'typed escape, never Boolean alias')
    need(1<=e['generator']<=2 and 1<=e['row']<=6 and 1<=e['column']<=6,'actual original generator and entry')
    m=ambient[e['generator']-1];left=a.product(x,m);right=a.product(m,x);i=6*(e['row']-1)+e['column']-1
    need(e['left']==left[i]and e['right']==right[i]and left[i]!=right[i],'actual nonzero ordinary commutator entry')
    a.charge(0);return True

def certificate(x=None,e=None):
    return dict(schema=SCHEMA,status='UNPAID_NO_WITNESS'if x is None else'CERTIFIED_UNIFORM_NONGENERATION',
        X=None if x is None else list(x),ambient_escape=e,all21_commutations=x is not None,
        raw_621_domain=dict(original_job=[621,5],namespace='NEW_UNQUOTIENTED_KH_INVOLUTION_CARTESIAN_V1',K_involutions=511,H_involutions=119,raw_pair_slots=60809),
        new_job_or_Original_or_Lean_credit=0)

def member_images(a,matrices):
    need(type(matrices)is list and len(matrices)==21,'all original nested21 images')
    return [a.flat(m)for m in matrices]

def same_json(V,left,right):
    return V['canonical'](left)==V['canonical'](right)
