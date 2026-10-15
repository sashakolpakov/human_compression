# Exact order-profile rejection plus reusable target stabilizer chains.
# Profiles are actual orders of all parabolic intersections, including Borel.
L096ProfileAction:=function(H,a)return Image(a,H);end;;
L096ProfileEquivalent:=function(ctx,p,pp,q,qp,cache)
 local perm,target,indices,alpha,cur,C,x,i,key,chain,T,j,places,k;
 if p=q then return true;fi;
 if SortedList(pp.orders)<>SortedList(qp.orders) or SortedList(List(p,Size))<>SortedList(List(q,Size)) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  target:=Permuted(q,perm);indices:=Permuted([1..Length(p)],perm);
  if List(p,Size)<>List(target,Size) then continue;fi;
  if not ForAll([1..Length(pp.keys)],j->pp.orders[j]=qp.orders[Position(qp.keys,Set(pp.keys[j],i->indices[i]))]) then continue;fi;
  if p=target then return true;fi;
  places:=SortedList([1..Length(p)],function(i,j)
   if Size(target[i])=Size(target[j]) then return i<j;fi;return Size(target[i])>Size(target[j]);end);
  key:=Concatenation("p",JoinStringsWithSeparator(List(indices,String),"_"));
  if not IsBound(cache.(key)) then cache.(key):=[ctx];fi;
  chain:=cache.(key);cur:=ShallowCopy(p);C:=ctx;x:=fail;
  for k in [1..Length(p)] do
   i:=places[k];
   x:=RepresentativeAction(C,cur[i],target[i],L096ProfileAction);
   if x=fail then break;fi;
   cur:=List(cur,H->Image(x,H));
   if k<Length(p) then
    if not IsBound(chain[k+1]) then chain[k+1]:=Stabilizer(C,target[i],L096ProfileAction);fi;
    C:=chain[k+1];
   fi;
  od;
  if x<>fail then return true;fi;
 od;
 return false;
end;;
