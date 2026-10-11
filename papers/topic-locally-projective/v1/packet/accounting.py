#!/usr/bin/env python3
"""Exact historical-table matching of a fresh complete GAP quotient census."""
import copy,json,re,math
import networkx as nx
DELETED={13,70,78,90,91,95,111,127}
ORDER=600415200

def need(ok,why):
    if not ok:raise ValueError(why)

def descriptor_order(s):
    s=s.split('(∼=')[0].strip()
    s=s.replace('PSL(2,19)','3420').replace('PSL(2,11)','660').replace('GL(2,4)','180').replace('L2(19)','3420').replace('L2(11)','660').replace('J1','175560')
    s=re.sub(r'(?<![A-Za-z0-9])(192|22|23|32)(?![0-9])',lambda m:str({22:4,23:8,32:9,192:361}[int(m[1])]),s)
    s=re.sub(r'([CASD])(\d+)',lambda m:str(math.factorial(int(m[2]))//(2 if m[1]=='A'else 1))if m[1]in'AS'else m[2],s)
    ns=[int(x)for x in re.findall(r'\d+',s)]
    # Literal PDF extraction of the four displayed powers of primes.
    return math.prod(ns)

def canonical_direct(s):
    """Elementary direct-product identities for the printed automorphism columns.
    No semidirect-product association is inferred beyond the literal two
    Frobenius factors 7:3 and 19:3 occurring in those columns.
    """
    s=s.replace('PSL(2,19)','L').replace('L2(19)','L').replace('GL(2,4)','C3 x A5')
    s=s.replace('×','x').replace(' ','')
    for a,b in [('(C7:C3)','F21'),('(7:3)','F21'),('C7:C3','F21'),('7:3','F21'),('C19:C3','F57'),('19:3','F57')]:s=s.replace(a,b)
    result=[]
    def cyclic(n):
        for p in [2,3,5,7,11,19]:
            q=1
            while n%p==0:q*=p;n//=p
            if q>1:result.append('C'+str(q))
        need(n==1,'explicit cyclic factorization')
    for t in s.split('x'):
        if t in ['J1','L','A5','S3','F21','F57','D10']:result.append(t)
        elif t=='D12':result.extend(['C2','S3'])
        elif t=='D20':result.extend(['C2','D10'])
        elif t in ['22','23','32']:
            result.extend(['C'+t[0]]*int(t[1]))
        elif t.startswith('C') and t[1:].isdigit():cyclic(int(t[1:]))
        elif t.isdigit():cyclic(int(t))
        else:raise ValueError('unrecognized automorphism factor '+t)
    return sorted(result)

def facets(row):
    text=row['facets_literal_extracted']
    if row['label']==1:return 0,int(text)
    if row['section_regular_table']:return int(text),0
    vals=list(map(int,re.findall(r'\d+',text)));need(len(vals)==2,'two facet counts');return tuple(vals)

def reconcile(census,rows):
    need(census['ambient_order']==ORDER and census['subgroup_classes']==1262,'complete ambient census')
    need(census['element_classes']==180 and len(census['bad_classes'])==47,'complete forbidden classes')
    ss=census['survivors'];good={r[0]for r in ss}
    need(len(ss)==len(good)==137,'distinct survivors')
    no={r[0]for r in census['rejected']};need(not good&no and good|no==set(range(1,1263)),'every class tested')
    need(all(r[1]in census['bad_classes']for r in census['rejected']),'every rejection has forbidden class')
    need(len(rows)==145 and {r['label']for r in rows}==set(range(1,146)),'complete historical tables')
    need([r[0]for r in census['deletion_witnesses']]==sorted(DELETED),'exact eight source deletions')
    need(all(r[1]in no and r[4]in census['bad_classes']for r in census['deletion_witnesses']),'deleted rows fail')
    anchors={i:(63 if lab==58 else lab)for lab,i,size in census['source_maximal_anchors']if i in good}
    need(len(anchors)==26 and set(anchors)==set(census['maximal_indices']),'all literal surviving maxima')
    S=nx.DiGraph();T=nx.DiGraph();source_by_id={r['label']:r for r in rows}
    for r in rows:
        lab=r['label']
        if lab in DELETED:continue
        d,h=facets(r);den=120*d+60*h;need(ORDER%den==0,'integral printed group order')
        size=ORDER//den
        if lab not in [21,27]:need(descriptor_order(r['group_literal_extracted'])==size,'printed subgroup order '+str(lab))
        else:need(size=={21:456,27:342}[lab],'explicit arxiv group-column correction')
        S.add_node(lab,color=(size,d,h,lab if lab in anchors.values()else 0))
    for r in rows:
        if r['label']not in DELETED:
            need(not DELETED.intersection(r['subgroups']),'no deleted child of a surviving parent')
            S.add_edges_from((r['label'],i)for i in r['subgroups'])
    for i,o,d,h in ss:
        need(type(d)is int and type(h)is int and min(d,h)>=0,'nonnegative integral facets')
        need(o*(120*d+60*h)==ORDER,'full facet partition')
        T.add_node(i,color=(o,d,h,anchors.get(i,0)))
    edges=set(map(tuple,census['maximal_edges']));need(len(edges)==349,'complete distinct containment edges')
    need(all(a in good and b in good for a,b in edges),'closure of all maximal subgroups')
    T.add_edges_from(edges)
    need(set(census['maximal_indices'])=={i for i in T if T.in_degree(i)==0},'all maximal classes')
    matcher=nx.algorithms.isomorphism.DiGraphMatcher(S,T,node_match=lambda x,y:x['color']==y['color'])
    need(matcher.is_isomorphic(),'complete historical and computed directed graphs')
    mapping=matcher.mapping
    need(len(mapping)==137 and set(mapping.values())==good,'full bijection of surviving labels')
    types={i:(g,q)for i,g,q in census['survivor_types']}
    need(set(types)==good,'every survivor has a subgroup and normalizer description')
    for lab,i in mapping.items():
        printed=source_by_id[lab]['automorphism_literal_extracted']
        need(canonical_direct(printed)==canonical_direct(types[i][1]),'actual normalizer quotient agrees with printed row '+str(lab))
    need(sum(r[3]==0 for r in ss)==65 and sum(r[2]==0 for r in ss)==1 and sum(r[2]>0 and r[3]>0 for r in ss)==71,'all corrected local types')
    result={'status':'PASS','source_rows':145,'surviving_rows':137,'maximal_rows':26,'section_regular':66,'same_local_type':65,'mixed':71,'directed_edges':349,'historical_to_computed':{str(k):v for k,v in sorted(mapping.items())},'deleted_labels':sorted(DELETED),'edition_crosswalk':{'arxiv_table1_label':58,'full_tables_label':63,'order':70,'journal_label_not_asserted':True,'group_column_corrections':{'21':'2^3 x (19:3), order456','27':'2 x (19:9), order342'}},'normalizer_quotients_matched':137}
    return result

def controls(census,rows):
    failures=[]
    def reject(name,c,r):
        try:reconcile(c,r)
        except (ValueError,KeyError,ZeroDivisionError):failures.append(name)
        else:raise ValueError('control passed '+name)
    c=copy.deepcopy(census);c['bad_classes'].pop();reject('omit_forbidden_element_class',c,rows)
    c=copy.deepcopy(census);c['survivors'].pop();reject('omit_one_subgroup',c,rows)
    c=copy.deepcopy(census);c['rejected'].pop();reject('skip_one_rejected_class',c,rows)
    c=copy.deepcopy(census);c['maximal_edges'].pop();reject('omit_containment_edge',c,rows)
    c=copy.deepcopy(census);c['maximal_indices'].pop();reject('wrong_maximal_count',c,rows)
    c=copy.deepcopy(census);c['deletion_witnesses'][0][0]=14;reject('alter_historical_deletion_label',c,rows)
    c=copy.deepcopy(census);c['survivors'][0][3]+=1;reject('change_local_facet_type',c,rows)
    c=copy.deepcopy(census);c['ambient_order']//=2;reject('omit_ambient_factor',c,rows)
    r=copy.deepcopy(rows);next(x for x in r if x['label']==1)['subgroups'].pop();reject('alter_printed_subgroup_link',census,r)
    r=copy.deepcopy(rows);next(x for x in r if x['label']==145)['facets_literal_extracted']='5003459';reject('alter_printed_facet_count',census,r)
    return failures
