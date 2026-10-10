# Independent check of the binary canonical-pcgs key assumption used by
# phase21_kernel_census.g and the exploratory ladder. No group catalogue.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([240,40]);;
CheckCoordinates21:=function(d)
 local F,f,rel,i,j,Q,ep,iso,G,pc,orders,r;
 F:=FreeGroup(d);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;
 od;od;
 Q:=F/rel;ep:=NqEpimorphismNilpotentQuotient(Q,5);
 iso:=IsomorphismPcGroup(Image(ep));G:=Image(iso);pc:=Pcgs(G);
 r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(ep,x)));
 orders:=RelativeOrders(pc);
 if not ForAll(orders,n->n=2) then Error("Binary pcgs key is not injective");fi;
 if Size(G)<>2^Length(pc) or Subgroup(G,r)<>G then Error("Coordinate size/marking");fi;
 Print("BINARY_COORDINATES rank=",d," order=",Size(G)," pcgs_length=",Length(pc),
  " relative_orders=",orders," marking_vectors=",List(r,x->ExponentsOfPcElement(pc,x)),"\n");
end;;
Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
for d21 in [3..5] do CheckCoordinates21(d21);od;
Print("PASS: the binary integer encoding is injective on every element of each actual universal pc group.\n");
QUIT;
