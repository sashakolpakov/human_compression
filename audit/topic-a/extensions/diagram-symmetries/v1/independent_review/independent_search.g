# Independent conjugacy-orbit enumeration: no import of the author's triple loop.
LoadPackage("smallgrp");;
IndependentReview:=function()
local rows,n,count,orbits,generated,allgen,k,pc,G,inv,cl,a,C,Bs,bo,b,D,Cs,co,c,o;
rows:=[];
for n in [40,48,56] do
  count:=0;orbits:=0;generated:=[];allgen:=0;
  for k in [1..NumberSmallGroups(n)] do
    pc:=SmallGroup(n,k);
    G:=Image(IsomorphismPermGroup(pc));
    inv:=Filtered(Elements(G),x->Order(x)=2);
    for cl in ConjugacyClasses(G) do
      a:=Representative(cl);
      if Order(a)<>2 then continue;fi;
      C:=Centralizer(G,a);
      Bs:=Filtered(inv,b->Order(a*b)=4);
      for bo in OrbitsDomain(C,Bs,OnPoints) do
        b:=bo[1];D:=Centralizer(C,b);
        Cs:=Filtered(inv,c->Order(a*c)=4 and Order(b*c)=4);
        for co in OrbitsDomain(D,Cs,OnPoints) do
          c:=co[1];o:=Size(Group(a,b,c));
          orbits:=orbits+1;
          count:=count+Size(cl)*Length(bo)*Length(co);
          AddSet(generated,o);
          if o=n then allgen:=allgen+1;fi;
        od;
      od;
    od;
  od;
  Add(rows,[n,NumberSmallGroups(n),orbits,count,generated,allgen]);
od;
Print("L128_INDEPENDENT_ORBITS ",rows,"\n");
if ForAny(rows,r->r[6]<>0) then Error("L128_REVIEW smaller generating triple");fi;
if List(rows,r->r[4])<>[0,528,0] then Error("L128_REVIEW orbit-size accounting");fi;
Print("L128_INDEPENDENT_ORBIT_SEARCH_PASS\n");
end;
IndependentReview();
QUIT;
