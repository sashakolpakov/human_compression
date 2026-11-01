"""Bounded distinct-element BFS supplier. No miss is an end exclusion."""
import field as f
import common
import solve

def fast19(mat,b):
    result=f.I;base=mat;exponent=19
    while exponent:
        if exponent&1:result=b.multiply(result,base)
        exponent//=2
        if exponent:base=b.multiply(base,base)
    return result

def path(parents,labels,index):
    out=[]
    while index:
        out.append(labels[index]);index=parents[index]
    return list(reversed(out))

def supply(g,cap,b,coverage):
    f.need(type(cap)is int and cap in(128,256),'explicit128or256 BFS storage/test cap')
    matrices=[f.I];index={f.I:0};parents=[-1];labels=[-1];head=0
    coverage.update(cap=cap,distinct_stored=1,nonidentity_words_tested=0,
                    generator_edges_evaluated=0,unrecorded_edge_images=0,
                    active_word_index=None,positive_word=None)
    while head<len(matrices):
        b.tick();mat=matrices[head]
        if head:
            coverage['active_word_index']=head;is19=fast19(mat,b)==f.I
            coverage['nonidentity_words_tested']+=1
            if is19:
                letters=path(parents,labels,head);kernel=solve.kernel(common.fixed_rows(mat,b),b)
                kernel.update(kind='FIXED_ORDER19',signs=[1])
                coverage['positive_word']=letters
                if not kernel['nullspace_basis']:
                    coverage['active_word_index']=None
                    coverage['stop']='NO_NONZERO_FIXED_VECTOR_CERTIFIED';return None,coverage
                seed=f.normalize(kernel['nullspace_basis'][0],b)
                coverage['active_word_index']=None;coverage['fixed_kernel_complete']=True
                return dict(word=letters,kernel=kernel,seed=seed),coverage
            coverage['active_word_index']=None
        for label,gen in enumerate(g):
            image=b.multiply(mat,gen);coverage['generator_edges_evaluated']+=1
            if image not in index:
                if len(matrices)==cap:
                    coverage['unrecorded_edge_images']+=1
                else:
                    index[image]=len(matrices);matrices.append(image);parents.append(head);labels.append(label)
                    coverage['distinct_stored']=len(matrices)
        head+=1
    coverage['stop']='FINITE_BFS_PREFIX_EXHAUSTED_WITHOUT_CARRIER'
    coverage['tested_all_stored_elements']=True
    return None,coverage
