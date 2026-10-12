# Exact index-two reduction of Aut(G), avoiding its large subgroup action.
L096IOSetup:=function(G)
 local A,a,T;
 A:=AutomorphismGroup(G);Print("AUT|",Size(A),"\n");
 if Size(Centre(G))<>1 or Size(A)<>2*Size(G) then Error("index-two inner hypothesis failed");fi;
 a:=First(GeneratorsOfGroup(A),x->not IsInnerAutomorphism(x));
 if a=fail then Error("no outer generator");fi;
 return rec(group:=G,aut:=A,outer:=[IdentityMapping(G),a]);
end;;
L096IOEquivalent:=function(ctx,p,pp,q,qp)
 local perm,target,indices,places,alpha,cur,C,x,k,i;
 if p=q then return true;fi;
 if SortedList(pp.orders)<>SortedList(qp.orders) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  target:=Permuted(q,perm);indices:=Permuted([1..Length(p)],perm);
  if not ForAll([1..Length(pp.keys)],j->pp.orders[j]=qp.orders[Position(qp.keys,Set(pp.keys[j],i->indices[i]))]) then continue;fi;
  if p=target then return true;fi;
  places:=SortedList([1..Length(p)],function(i,j)if Size(target[i])=Size(target[j]) then return i<j;fi;return Size(target[i])>Size(target[j]);end);
  for alpha in ctx.outer do
   cur:=List(p,H->Image(alpha,H));C:=ctx.group;x:=fail;
   for k in [1..Length(p)] do
    i:=places[k];x:=RepresentativeAction(C,cur[i],target[i]);
    if x=fail then break;fi;
    cur:=List(cur,H->H^x);
    if k<Length(p) then C:=Normalizer(C,target[i]);fi;
   od;
   if x<>fail then return true;fi;
  od;
 od;
 return false;
end;;
