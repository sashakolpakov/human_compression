"""Untrusted bounded word/start hints."""
def need(v,s):
    if not v:raise ValueError(s)
def search(K,ctx,triangle,settings,probe,work):
    words,starts=settings['words'],settings['starts']
    need(type(words)is list and 1<=len(words)<=64 and all(type(w)is list and 1<=len(w)<=64 and all(type(j)is int and j in(-2,-1,1,2)for j in w)for w in words),'at most64 finite signed-word hints')
    need(type(starts)is list and 1<=len(starts)<=4 and all(type(x)is int and 0<=x<ctx['n']for x in starts)and len(set(starts))==len(starts),'four distinct actual point starts')
    b=K.prepare_triangle(ctx,triangle,work);out={}
    for prime,name in((11,'prime11'),(13,'prime13')):
        found=None
        for word in words:
            if found is not None:break
            for start in starts:
                work.charge(16,'bounded hint candidate framing')
                cost=prime*len(word)
                if probe['attempts']>=512 or probe['point_letters']+cost>32768:continue
                probe['attempts']+=1;probe['point_letters']+=cost;cycle=[];seen=set();point=start
                for _ in range(prime):
                    if point in seen:break
                    seen.add(point);cycle.append(point);point=K.rotation_word(ctx,b,word,point,work)
                if len(cycle)==prime and point==start:found=dict(word=list(word),cycle=cycle);break
        out[name]=found
    return out if all(x is not None for x in out.values())else None
