"""Supplied-word verification only; no tree search, class search or solver."""
def need(v,s):
    if not v:raise ValueError(s)
def equal(a,b,work):
    need(len(a)==len(b),'same original degree');work.charge(3*len(a),'whole_original_map_equality')
    return all(x==y for x,y in zip(a,b))
def inverse_word(word,work):
    work.charge(len(word),'whole_signed_word_inverse');return[-x for x in reversed(word)]
def word(K,maps,letters,n,work):
    need(type(letters)is list and len(letters)<=128 and all(type(j)is int and 1<=abs(j)<=36 for j in letters),'bounded typed CP36 word')
    out=K['identity'](n,work)
    for j in letters:
        need(abs(j)in maps,'actual accepted CP36 map for every letter')
        if j not in maps:maps[j]=K['inverse'](maps[-j],work)
        out=K['compose'](out,maps[j],work)
    return out
def verify(K,ctx,maps,g,cert,work):
    need(type(cert)is dict and set(cert)=={'schema','r_word','q_word','prefix_acceptance'}and cert['schema']=='L026_TWO_NORMALIZER_WORD_CANDIDATE_V1','entire supplied two-word candidate')
    n=ctx['n'];r=word(K,maps,cert['r_word'],n,work);q=word(K,maps,cert['q_word'],n,work)
    t=K['compose'](q,g,work);ri=K['inverse'](r,work);ti=K['inverse'](t,work)
    conjugate=lambda x,h,hi:K['compose'](K['compose'](hi,x,work),h,work)
    ac=K['compose'](ctx['a'],ctx['c'],work)
    need(equal(conjugate(ctx['a'],r,ri),ctx['a'],work)and equal(conjugate(ctx['c'],r,ri),ac,work),'whole a^r=a and c^r=ac')
    need(equal(conjugate(ctx['a'],t,ti),ctx['c'],work)and equal(conjugate(ctx['c'],t,ti),ctx['a'],work),'whole a^t=c and c^t=a')
    return dict(status='VERIFIED_TWO_ORIGINAL_NORMALIZER_WORD_EQUATIONS',degree=n,
        r_action=['a','ac'],t_action=['c','a'],r_word_alphabet='ACCEPTED_CP36',
        t_word_expression='CP36(q_word) * accepted_original_triangle_prefix(g)',
        original_Aut_and_tagged_word_membership_are_explicit_imports=True,
        induced_Klein_basis_actions_generate_S3=True,whole_bank_action_or_new_paid_rows=0,
        Root_model_and_component_adoption_owed=True)
