# Distinct root cross-check. Shared trusted model and concrete class representatives.
Read("programs/ambient_marking.g");;
Read("computed_subgroups.g");;
Read("root_input.g");;
RootNeed:=function(b,m) if not b then Error(m);fi;end;;
rootGroups:=List(subgroupGenerators,gens->Group(gens,One(W)));;
rootGood:=List(rootRows,r->r[2]);;
rootSizes:=List(rootGood,i->Size(rootGroups[i]));;
RootIndex:=function(h)
 local j;
 j:=PositionProperty([1..Length(rootGood)],k->rootSizes[k]=Size(h) and IsConjugate(W,h,rootGroups[rootGood[k]]));
 RootNeed(j<>fail,"subgroup closure absent from complete survivor set");
 return rootGood[j];
end;;
rootAllPairs:=[];;rootFacetRows:=[];;rootNormalizers:=[];;
for row in rootRows do
 i:=row[2];; n:=rootGroups[i];;
 ids:=Set(List(ConjugacyClassesSubgroups(n),c->RootIndex(Representative(c))));;
 for k in ids do if k<>i then AddSet(rootAllPairs,[i,k]);fi;od;
 invols:=Filtered(Elements(n),x->Order(x)=2);;
 m:=Number(invols,x->IsConjugate(W,x,om));;
 hh:=2*Size(Centralizer(W,om))*m/(Size(H3)*Size(n));;
 dd:=(Size(W)/Size(H3)-hh*Size(n)/2)/Size(n);;
 RootNeed([Size(n),dd,hh]=row{[3,4,5]},"independent actual-involution facet counts");;
 Add(rootFacetRows,[row[1],Size(n),dd,hh,m]);;
 Add(rootNormalizers,[row[1],Size(Normalizer(W,n))/Size(n)]);;
od;
rootEdges:=Filtered(rootAllPairs,e->not ForAny(rootAllPairs,a->a[1]=e[1] and [a[2],e[2]] in rootAllPairs));;
RootNeed(rootEdges=rootExpectedEdges,"full subgroup relation has exactly the claimed Hasse edges");;
rootMaxima:=Difference(rootGood,Set(List(rootAllPairs,e->e[2])));;
RootNeed(Length(rootMaxima)=26,"all maximal ambient classes");;
PrintTo("root_distinct_result.json","{\"status\":\"PASS\",\"survivors\":137,\"strict_containment_pairs\":",Length(rootAllPairs),",\"cover_edges\":",Length(rootEdges),",\"maxima\":",Length(rootMaxima),",\"facet_rows\":",rootFacetRows,",\"normalizer_orders\":",rootNormalizers,"}\n");;
Print("ROOT_L084_DISTINCT_PASS\n");; QUIT;
