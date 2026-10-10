# Search for one exact source marking in the retained J1 permutation group.
# No geometry from the prior RWPRI list is used as a thin seed.
Read("phase6_sporadic_J1_representatives.g");;
FindSeed24:=function(G)
 local a,b,c,d,ca,iv,ds,bs,tested;
 a:=GeneratorsOfGroup(G)[1];
 if Order(a)<>2 then Error("ambient first generator");fi;
 ca:=Centralizer(G,a);iv:=Filtered(Elements(ca),x->Order(x)=2);tested:=0;
 Print("GROUP_ORDER ",Size(G)," CENTRALIZER ",Size(ca)," INVOLUTIONS ",Length(iv),"\n");
 for d in iv do
  if d=a then continue;fi;
  bs:=Filtered(Elements(Centralizer(G,d)),x->Order(x)=2 and Order(a*x)=5);
  for c in iv do
   if Order(c*d)<>5 then continue;fi;
   for b in bs do
    tested:=tested+1;
    if Order(b*c)=3 and (a*b*c)^5=One(G) and ((d*c*b)^5*a)^3=One(G)
      and Size(Group(a,b,c,d))=Size(G) then
     Print("TESTED_CANDIDATES ",tested,"\n");return [a,b,c,d];
    fi;
   od;
  od;
 od;
 Error("No seed found");
end;;
s:=FindSeed24(G);;
PrintTo("phase24_L088_seed.json",List(s,g->ListPerm(g,266)),"\n");
Print("SEED_PARABOLICS ",List([1..4],i->Size(Group(s{Difference([1..4],[i])}))),"\n");
Print("EXTRA_RELATIONS_PASS\n");
QUIT;
