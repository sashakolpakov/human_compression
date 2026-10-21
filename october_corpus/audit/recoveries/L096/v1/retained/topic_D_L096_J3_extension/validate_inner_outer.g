Read("inner_outer_direct.g");;Read("reference_aut_match.g");;
G:=AlternatingGroup(5);;ctx:=L096IOSetup(G);;
K:=List(ConjugacyClassesSubgroups(G),Representative);;
Profile:=function(p)
 local keys;keys:=Combinations([1..Length(p)]);
 return rec(keys:=keys,orders:=List(keys,J->(function()if Length(J)=0 then return Size(G);fi;return Size(Intersection(List(J,i->p[i])));end)()));
end;;
families:=List([1..6],i->[K[i],K[(i+2) mod Length(K)+1],K[(i+4) mod Length(K)+1]]);;
Append(families,List(ShallowCopy(families),p->Permuted(List(p,H->Image(ctx.outer[2],H)),(1,2,3))));;
profiles:=List(families,Profile);;caches:=List(families,p->rec());;yes:=0;;no:=0;;
for i in [1..Length(families)] do
 for j in [1..Length(families)] do
  a:=L096IOEquivalent(ctx,families[i],profiles[i],families[j],profiles[j]);
  b:=L096ProfileEquivalent(ctx.aut,families[i],profiles[i],families[j],profiles[j],caches[j]);
  if a<>b then Error("inner/outer/full-Aut mismatch");fi;
  if a then yes:=yes+1;else no:=no+1;fi;
 od;
od;
Print("VALIDATION|",Length(families)^2,"|",yes,"|",no,"\nPASS_INNER_OUTER_VALIDATION\n");QUIT;
