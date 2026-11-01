"""Typed actual end marks and fixed-space equations; no search or elimination."""
import field as f

def marks(raw,b):
    f.need(type(raw)is list and len(raw)==3,'three ordered actual end involutions')
    out=[]
    for mat in raw:
        f.need(type(mat)is list and len(mat)==7,'whole seven matrix rows')
        out.append(bytes(x for row in mat for x in f.vector(row,7,b)))
    for mat in out:f.need(b.multiply(mat,mat)==f.I,'all three complete involution equations')
    return tuple(out)

def fixed_rows(mat,b):
    rows=[]
    for j in range(7):
        row=[]
        for i in range(7):
            b.scalar(1);row.append((mat[7*i+j]-int(i==j))%11)
        rows.append(tuple(row))
    return rows

def word(g,letters,b):
    f.need(type(letters)is list and 1<=len(letters)<=255 and
           all(type(i)is int and 0<=i<3 for i in letters),'bounded positive actual-generator word')
    b.scalar(len(letters));out=f.I
    for i in letters:out=b.multiply(out,g[i])
    return out

def end_id(job,b):
    name=job['end_id'];f.need(type(name)is str and 0<len(name)<=128 and name.isascii(),'bounded end identity')
    b.scalar(len(name));return name
