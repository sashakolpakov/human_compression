# Exact full-Aut family comparison through inner/outer representatives.
L096InnerOuterSetup:=function(G)
 local A,I,T;
 A:=AutomorphismGroup(G);I:=InnerAutomorphismsAutomorphismGroup(A);
 if not IsNormal(A,I) then Error("inner automorphisms not normal");fi;
 T:=RightTransversal(A,I);
 return rec(group:=G,automorphisms:=A,inner:=I,outer_representatives:=T);
end;;
L096InnerOuterEquivalent:=function(ctx,p,q)
 local perm,target,alpha,cur,C,x,i;
 if SortedList(List(p,Size))<>SortedList(List(q,Size)) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  target:=Permuted(q,perm);if List(p,Size)<>List(target,Size) then continue;fi;
  for alpha in ctx.outer_representatives do
   cur:=List(p,H->Image(alpha,H));C:=ctx.group;x:=fail;
   for i in [1..Length(p)] do
    x:=RepresentativeAction(C,cur[i],target[i]);
    if x=fail then break;fi;
    cur:=List(cur,H->H^x);C:=Normalizer(C,target[i]);
   od;
   if x<>fail then return true;fi;
  od;
 od;
 return false;
end;;
