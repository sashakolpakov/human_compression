"""Fresh actual prime19 word/fixed-vector check; no search or linear solver."""
import field as f
import common

def begin(g,raw,letters,b):
    v=f.vector(raw,7,b);b.scalar(7);f.need(any(v),'nonzero exact seed')
    mat=common.word(g,letters,b);f.need(mat!=f.I,'actual nonidentity word')
    power=f.I
    for _ in range(19):power=b.multiply(power,mat)
    f.need(power==f.I,'nineteen fresh complete word powers')
    f.need(b.image(v,mat)==bytes(v),'fresh selected v*M=v')
    return bytes(v)
