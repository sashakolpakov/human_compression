# Fresh Compress_B replay. Exact census code retained and charged in manuscript Appendix A.
# Exhaustive marked {4,8}, order256 census using the GAP SmallGroups library.
# The three involutions must have independent images in G/Phi(G), so the
# abelianization is exactly C2^3. Conjugacy representatives for r=b*c and
# centralizer orbits for c lose no marked generating triples.
SetInfoLevel(InfoWarning,0);
Main:=function()
local started,ids,total,active,hits,counts,id,g,phi,rs,invs,hom,found,r,
 candidates,cr,c,b,plane,aas,right,a,d,z,matches;
started:=Runtime();;
ids:=IdsOfAllSmallGroups(256,AbelianInvariants,[[2,2,2]]);;
Print("GAP ",GAPInfo.Version," SmallGroups ",PackageInfo("smallgrp")[1].Version,
 " eligible_groups=",Length(ids),"\n");
total:=0;; active:=0;; hits:=[];; counts:=[0,0,0,0];;
for id in ids do
 g:=SmallGroup(id);;
 phi:=FrattiniSubgroup(g);;
 rs:=Filtered(List(ConjugacyClasses(g),Representative),x->Order(x)=8 and not x in phi);;
 if Length(rs)=0 then continue;fi;
 active:=active+1;
 invs:=Filtered(Elements(g),x->Order(x)=2);;
 hom:=NaturalHomomorphismByNormalSubgroup(g,phi);;
 found:=[];;
 for r in rs do
  candidates:=Set(Filtered(invs,c->r^c=r^-1 and not Image(hom,c) in Group(Image(hom,r))));;
  cr:=Elements(Centralizer(g,r));;
  while Length(candidates)>0 do
   c:=candidates[1];;
   candidates:=Difference(candidates,Set(cr,x->c^x));;
   b:=r*c;; plane:=Group(Image(hom,r),Image(hom,c));;
   aas:=Filtered(invs,a->not Image(hom,a) in plane and a*c=c*a and Order(a*b)=4);;
   right:=Group(b,c);;
   for a in aas do
    if Size(Intersection(Group(a,b),right))<>2 then continue;fi;
    total:=total+1;; d:=(a*b)^2;; z:=r^4;;
    matches:=[];;
    if Comm(a,r^2)^2=One(g) and Comm(a,r^4)=One(g) then Add(matches,1);fi;
    if Comm(a,r^2)^2=z and Comm(a,r^4)=One(g) then Add(matches,2);fi;
    if Comm(d,r^2)=z then Add(matches,3);fi;
    if Comm((r^2)^a,r)=z then Add(matches,4);fi;
    if Length(matches)<>1 then
     Print("UNEXPECTED ",id," matches=",matches," tuple=",[a,b,c],"\n");
     QUIT_GAP(1);
    fi;
    counts[matches[1]]:=counts[matches[1]]+1;;
    AddSet(found,matches[1]);;
   od;
  od;
 od;
 if Length(found)>0 then
  Add(hits,[id,found]);;
  Print("HIT ",id," patterns=",found," cumulative=",total," ms=",Runtime()-started,"\n");
 fi;
od;
Print("PASS groups=",Length(ids)," active=",active," triples=",total,
 " pattern_counts=",counts," hits=",hits," ms=",Runtime()-started,"\n");
end;
Main();
QUIT;
