hyperbolic_records:=[];;
# A bijective map taking the four ordered marks to the four ordered marks
# identifies the kernels of the same finitely presented Coxeter group.
SameOrderedMarking:=function(a,b)
  local s,t,H,K,f;
  if a.order<>b.order or Length(a.permutations)<>4 or
     Length(b.permutations)<>4 then return false;fi;
  s:=List(a.permutations,PermList);t:=List(b.permutations,PermList);
  H:=Group(s);K:=Group(t);
  if Size(H)<>a.order or Size(K)<>b.order then return false;fi;
  f:=GroupHomomorphismByImages(H,K,s,t);
  return f<>fail and IsBijective(f);
end;;
OrderedMarkingBijection:=function(a,b)
  local remaining,matches,i,j,hit;
  if Length(a)<>Length(b) then return fail;fi;
  remaining:=[1..Length(b)];matches:=[];
  for i in [1..Length(a)] do
    hit:=fail;
    for j in remaining do
      if SameOrderedMarking(a[i],b[j]) then hit:=j;break;fi;
    od;
    if hit=fail then return fail;fi;
    Add(matches,hit);RemoveSet(remaining,hit);
  od;
  if remaining<>[] then return fail;fi;
  return matches;
end;;
CompareMarkedFiles:=function(oldpath,newpath)
  local a,b,m,bad;
  Read(oldpath);a:=hyperbolic_records;
  Read(newpath);b:=hyperbolic_records;
  m:=OrderedMarkingBijection(a,b);
  if m=fail then Error("marked kernel inventories differ");fi;
  # Preserve multiplicity and ordered marks; an abstract group name or order
  # alone is insufficient. These probes exercise both failure paths.
  if OrderedMarkingBijection(a,Concatenation(b,[b[1]]))<>fail then
    Error("multiplicity damage accepted");fi;
  bad:=StructuralCopy(a[1]);bad.permutations[1]:=bad.permutations[2];
  if SameOrderedMarking(a[1],bad) then Error("damaged marking accepted");fi;
  Print("MARKED_BIJECTION ",m,"\nCOMPLETE_MARKED_COMPARISON ",Length(a)," 2 CONTROLS\n");
end;;
