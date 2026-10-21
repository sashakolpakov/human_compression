# Probe the stronger candidate |a||b| exp(P/Z(P)) <= |P| for core-free
# cyclic generators a,b of a finite 2-group. This is NOT assumed in a proof.
LogTo("research/leemans/phase3_corefree_bound_probe.log");;
Main:=function()
local lg,n,abtypes,i,j,ids,id,g,phi,hom,im,z,e,cat,x,o,k,m,idx,found;
for lg in [3..8] do
 n:=2^lg;abtypes:=[];
 for i in [1..lg] do for j in [i..lg] do
  if i+j<lg then Add(abtypes,[2^i,2^j]);fi;
 od;od;
 ids:=IdsOfAllSmallGroups(n,AbelianInvariants,abtypes);found:=0;
 for id in ids do
  g:=SmallGroup(id);z:=Centre(g);phi:=FrattiniSubgroup(g);
  hom:=NaturalHomomorphismByNormalSubgroup(g,phi);
  im:=Filtered(Elements(Image(hom)),x->not IsOne(x));
  cat:=[1,1,1];
  for x in Elements(g) do
   if x in phi then continue;fi;
   o:=Order(x);if x^(o/2) in z then continue;fi;
   k:=Position(im,Image(hom,x));cat[k]:=Maximum(cat[k],o);
  od;
  Sort(cat);if cat[2]=1 then continue;fi;
  e:=Exponent(g/z);
  if cat[2]*cat[3]*e>n then
   Print("FALSE candidate at ",id," class=",NilpotencyClassOfGroup(g),
     " center-free_max_orders=",cat," exponent_quotient=",e,"\n");
   found:=found+1;
  fi;
 od;
 Print("ORDER ",n," groups=",Length(ids)," false_examples=",found,"\n");
 if found>0 then return;fi;
od;
end;
Main();
LogTo();
QUIT;
