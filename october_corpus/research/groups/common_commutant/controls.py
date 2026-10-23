"""Byte-exact selected project definitions; see provenance/source_derivation.json.
No original host paths or project runtime are imported.
"""

NAMES=['nested21_and_original2_commutation','noninvertible_witness_accepted',
       'any_valid_escape_entry','false_commutation_rejected','false_escape_rejected',
       'Boolean_matrix_alias_rejected','Boolean_escape_alias_rejected',
       'wrong_621_domain_rejected','whole_fields_required','UNPAID_is_not_negative',
       'twenty_first_mark_checked','second_original_generator_checked']

def synthetic_codec():
    # TEST ONLY polynomial-basis GF(8), t^3=t+1.  Not the acquired GAP codec.
    add=[[x^y for y in range(8)]for x in range(8)];mul=[]
    for x in range(8):
        row=[]
        for y in range(8):
            r=0;a=x;b=y
            while b:
                if b&1:r^=a
                b>>=1;a<<=1
                if a&8:a^=11
            row.append(r)
        mul.append(row)
    return dict(schema='F004_GF8_EXPONENT_CODEC_V1',zero=0,one=1,addition=add,multiplication=mul)

def run(T,C,charge,V):
    import copy
    a=T['Arithmetic'](synthetic_codec(),charge);ident=a.identity
    x=list(ident);x[0]=0 # A singular projection, whose centralizer is proper.
    x=tuple(x);g=list(ident);g[1]=1;g=tuple(g)
    nested=[[list(ident[6*i:6*i+6])for i in range(6)]for _ in range(21)]
    marks=C['member_images'](a,nested);ambient=[ident,g]
    try:C['member_images'](a,[list(ident)]*21)
    except ValueError:pass
    else:raise ValueError('flat36 member images accepted instead of nested6x6')
    good=C['certificate'](x,C['escape'](a,x,ambient))
    def reject(cert,ms=marks,gs=ambient):
        try:C['verify'](a,ms,gs,cert)
        except ValueError:return
        raise ValueError('synthetic bad witness accepted')
    done=[]
    assert C['verify'](a,marks,ambient,good);done.append(NAMES[0])
    assert good['X'][0]==0 and C['verify'](a,marks,ambient,good);done.append(NAMES[1])
    swapped=copy.deepcopy(good);swapped['ambient_escape']=dict(generator=1,row=1,column=2,left=0,right=1)
    assert C['verify'](a,marks,[g,ident],swapped);done.append(NAMES[2])
    reject(good,[g]+marks[1:]);done.append(NAMES[3])
    bad=copy.deepcopy(good);bad['ambient_escape']['left']=1;reject(bad);done.append(NAMES[4])
    bad=copy.deepcopy(good);bad['X'][0]=False;reject(bad);done.append(NAMES[5])
    bad=copy.deepcopy(good);bad['ambient_escape']['row']=True;reject(bad);done.append(NAMES[6])
    bad=copy.deepcopy(good);bad['raw_621_domain']['original_job']=[630,5];reject(bad);done.append(NAMES[7])
    bad=copy.deepcopy(good);bad['extra']=0;reject(bad)
    assert not C['same_json'](V,dict(uniform_nongeneration=1),dict(uniform_nongeneration=True))
    assert not C['same_json'](V,dict(credit=False),dict(credit=0))
    assert not C['same_json'](V,dict(bytes=1.0),dict(bytes=1))
    done.append(NAMES[8])
    assert C['verify'](a,marks,ambient,C['certificate']())is False;done.append(NAMES[9])
    reject(good,marks[:20]+[g]);done.append(NAMES[10])
    reject(good,marks,[ident,ident]);done.append(NAMES[11])
    assert done==NAMES;charge(0)
    return dict(schema='TEST_ONLY_F004_Q8_621_COMMUTANT_CONTROLS_V1',controls=done,all_passed=True,TEST_ONLY=True,new_job_or_Original_or_Lean_credit=0)
