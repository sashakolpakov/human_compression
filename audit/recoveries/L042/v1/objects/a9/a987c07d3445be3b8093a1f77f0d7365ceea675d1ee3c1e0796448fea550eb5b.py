"""Extract the eighteen xymatrices of the original Figure 1.

Documentary source adapter. Public replay uses the derived numeric records;
the primary article itself is retained privately and identified by hash.
"""
import hashlib,json,re,sys
from pathlib import Path
from diagrams import need, FAMILIES, graph, isomorphism
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')

ARROW=re.compile(r'\\ar@\{([^}]+)\}\[([rd]+)\]((?:[_^](?:\{[^}]+\}|[0-9]))*)')
LABEL=re.compile(r'[_^](?:\{([^}]+)\}|([0-9]))')

def integer(expression,n):
    expression=expression.strip()
    if expression.isdigit():return int(expression)
    m=re.fullmatch(r'n\s*-\s*(\d+)',expression)
    need(m is not None,'unsupported source label')
    return n-int(m.group(1))

def extract(source):
    figure=source.split('\\begin{figure}[h]',1)[1].split('\\end{figure}',1)[0]
    out=[];position=0
    while True:
        i=figure.find('\\xymatrix@-1pc{',position)
        if i<0:break
        start=i+len('\\xymatrix@-1pc{');depth=1;j=start
        while depth:
            need(j<len(figure),'unfinished source matrix')
            depth+=(figure[j]=='{')-(figure[j]=='}');j+=1
        out.append(figure[start:j-1]);position=j
    need(len(out)==18,'not eighteen source matrices')
    return out

def literal(matrix,n):
    rows=re.split(r'\\\\\s*',matrix)
    cells={(r,c):cell for r,row in enumerate(rows) for c,cell in enumerate(row.split('&'))}
    vertices={rc for rc,cell in cells.items() if '*+[o][F]{}' in cell}
    arrows=[]
    for rc in sorted(vertices):
        cell=cells[rc]
        found=list(ARROW.finditer(cell))
        need(cell.count('\\ar')==len(found),'unparsed arrow')
        for m in found:
            style,direction,labels=m.groups();need(direction in ('r','d'),'nonunit arrow')
            dest=(rc[0]+(direction=='d'),rc[1]+(direction=='r'))
            need(dest in vertices,'arrow missing vertex')
            values=tuple(integer(a or b,n) for a,b in LABEL.findall(labels))
            need(style in ('-','=','.', '..'),'unknown edge style')
            need((style=='-' and len(values)==1) or (style=='=' and len(values)==2) or (style in ('.','..') and not values),'edge label count')
            arrows.append((rc,dest,style,values))
    ids={v:i for i,v in enumerate(sorted(vertices))};edges=[];next_id=len(ids)
    for a,b,style,values in arrows:
        if style not in ('.','..'):
            edges.extend((ids[a],ids[b],v) for v in values);continue
        need(a[0]==b[0],'nonhorizontal ellipsis')
        before=[vs[0] for x,y,s,vs in arrows if y==a and x[0]==a[0] and s=='-']
        after=[vs[0] for x,y,s,vs in arrows if x==b and y[0]==b[0] and s=='-']
        need(len(before)==len(after)==1,'ambiguous ellipsis')
        labels=list(range(before[0]+1,after[0]));need(bool(labels),'degree too small for literal displayed ellipsis')
        path=[ids[a]]+list(range(next_id,next_id+len(labels)-1))+[ids[b]]
        next_id+=len(labels)-1
        edges.extend((x,y,l) for x,y,l in zip(path,path[1:],labels))
    need(next_id==n,'expanded source degree')
    r=max(l for _,_,l in edges)+1;marks=[list(range(n)) for _ in range(r)]
    for a,b,l in edges:
        need(marks[l][a]==a and marks[l][b]==b,'source not a matching')
        marks[l][a],marks[l][b]=b,a
    return tuple(tuple(g) for g in marks),edges

if __name__=='__main__':
    need(len(sys.argv)==3,'usage: read_figure.py SOURCE_TEX OUT_JSON')
    p=Path(sys.argv[1]);raw=p.read_bytes();matrices=extract(raw.decode());records=[]
    for (k,name,j),matrix in zip(FAMILIES,matrices):
        marks,edges=literal(matrix,31);model,_=graph(k,name,31)
        iso=isomorphism(marks,model);need(iso is not None and not iso['reverse_target'],'source/model mismatch')
        records.append({'k':k,'family':name,'n':31,'source_matrix_sha256':hashlib.sha256(matrix.encode()).hexdigest(),'marks':marks,'edges':edges,'to_model':iso})
    out={'status':'PASS_ALL_18_SOURCE_MATRICES','primary_tex_sha256':hashlib.sha256(raw).hexdigest(),'interpretation':'Dotted paths contain precisely all consecutive labels strictly between the adjacent displayed labels. All arrows and label multiplicities parsed. Numeric records derived from source Figure 1.','records':records}
    Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
