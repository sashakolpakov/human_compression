AutoSub:=function(H,a) return Image(a,H);end;
Signature:=function(p)
 return [SortedList(List(p,Size)),SortedList(List(Combinations([1..Length(p)],2),ij->Size(Intersection(p[ij[1]],p[ij[2]])))),Size(Intersection(p))];
end;
EquivalentFamilies:=function(A,p,q)
 local perm,ord,cur,C,x,i;
 if Signature(p)<>Signature(q) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  ord:=Permuted(q,perm);
  if List(p,Size)<>List(ord,Size) then continue;fi;
  cur:=ShallowCopy(p);C:=A;x:=fail;
  for i in [1..Length(p)] do
   x:=RepresentativeAction(C,cur[i],ord[i],AutoSub);
   if x=fail then break;fi;
   cur:=List(cur,H->Image(x,H));C:=Stabilizer(C,ord[i],AutoSub);
  od;
  if x<>fail then return true;fi;
 od;
 return false;
end;
