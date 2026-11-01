"""Independent full-word/power/fixed-kernel consumer; imports no supplier."""
import field as f
import common
import verify

def consume(g,certificate,b):
    f.need(type(certificate)is dict and set(certificate)=={'word','kernel','seed'},'complete fixed19 carrier')
    mat=common.word(g,certificate['word'],b)
    f.need(mat!=f.I,'actual word is nonidentity')
    power=f.I
    for _ in range(19):power=b.multiply(power,mat)
    f.need(power==f.I,'nineteen fresh naive whole-matrix products')
    kernel=certificate['kernel']
    f.need(type(kernel)is dict and kernel.get('kind')=='FIXED_ORDER19' and
           type(kernel.get('signs'))is list and len(kernel['signs'])==1 and
           type(kernel['signs'][0])is int and kernel['signs']==[1],'exact fixed1 kernel identity')
    rows=common.fixed_rows(mat,b);basis=verify.block(rows,kernel,b)
    f.need(len(basis)>0,'complete nonzero fixed space')
    for v in basis:f.need(b.image(v,mat)==bytes(v),'fresh actual word image for EVERY kernel basis vector')
    wanted=f.normalize(basis[0],b);chosen=f.vector(certificate['seed'],7,b)
    b.scalar(7);f.need(any(chosen)and list(chosen)==wanted,'exact first normalized nonzero fixed seed')
    f.need(b.image(chosen,mat)==bytes(chosen),'fresh selected v*M=v')
    return dict(status='VERIFIED_END_WORD_ORDER19_AND_FIXED_SEED_ONLY',word=certificate['word'],
                exact_prime_order=19,fixed_dimension=len(basis),selected_seed=wanted,
                original_end_order_or_generation_or_IP_authority=False,original_case_credit=0)
