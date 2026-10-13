Read("model.g");;Read("inventory.g");;Read("checks.g");;
t:=List(ids,i->ivs[i]);;
if Length(t)<>7 or not ForAll(t,x->Order(x)=2) or Group(t)<>G or Size(G)<>2903040 then Error("generation");fi;
for i in [1..7] do for j in [i+2..7] do if Comm(t[i],t[j])<>() then Error("string");fi;od;od;
if not FullIP(t) then Error("full IP");fi;
Print("RANK_SEVEN_TUPLE ",t,"\n");
Print("ADJACENT_PRODUCT_ORDERS ",List([1..6],i->Order(t[i]*t[i+1])),"\n");
for i in [1..7] do
 if t[i] in Centre(G) then
  H:=Group(t{Difference([1..7],[i])});;
  if Size(H)<>1451520 or Intersection(H,Group(t[i]))<>TrivialSubgroup(G) then Error("direct product");fi;
  Print("CENTRAL_MARK ",i," COMPLEMENT_ORDER ",Size(H),"\n");
 fi;
od;
Print("COMPLETE_E7_RANK_SEVEN_FULL_SUBSET_IP_WITNESS\n");QUIT;
