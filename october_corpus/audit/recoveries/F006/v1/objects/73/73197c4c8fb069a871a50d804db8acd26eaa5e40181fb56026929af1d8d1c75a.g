# Exact induced conjugation action on two copies of the original domain.
if not IsBound(modelFile) then modelFile:="E8_model.g";fi;
Read(modelFile);;
if Size(G)<>expectedOrder then Error("model order");fi;
oldG:=G;; N:=LargestMovedPoint(oldG);; cent:=Centre(oldG);;
if Size(cent)<>2 then Error("centre must have order two");fi;
z:=First(Elements(cent),x->x<>());;
if SignPerm(z)<>1 then Error("central element must be even");fi;
Twist:=function(g)if SignPerm(g)=-1 then return z*g;else return g;fi;end;;
Embed:=g->PermList(Concatenation(List([1..N],i->i^g),List([1..N],i->N+i^Twist(g))));;
G:=Group(List(GeneratorsOfGroup(oldG),Embed));;
swap:=PermList(Concatenation([N+1..2*N],[1..N]));;
A:=Group(Concatenation(GeneratorsOfGroup(G),[swap]));;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("embedding or normality");fi;
if not ForAll(GeneratorsOfGroup(oldG),g->Embed(g)^swap=Embed(Twist(g))) then Error("twist implementation");fi;
fullAutOrder:=Size(AutomorphismGroup(oldG));;
actionKernel:=Centralizer(A,G);;
if Size(A)/Size(actionKernel)<>fullAutOrder then Error("full automorphism action not covered");fi;
Print("MODEL ",modelName," order ",Size(G)," DEGREE ",2*N,"\n");
Print("AUT_ORDER ",fullAutOrder," CONJUGATING_ORDER ",Size(A)," KERNEL_ORDER ",Size(actionKernel),"\n");
involutionClasses:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
ivs:=Set(Concatenation(List(involutionClasses,AsList)));;
if Length(ivs)<>Sum(involutionClasses,Size) then Error("involution class coverage");fi;
Print("INVOLUTIONS ",Length(ivs),"\n");
Print("MODEL_GENERATORS ",GeneratorsOfGroup(G),"\n");
Print("INVOLUTIONS_LITERAL ",ivs,"\n");
Print("CONJUGATING_GENERATORS ",GeneratorsOfGroup(A),"\n");

# Every call has string commutations. Full end criterion recursively verifies IP.
CheckIP:=function(t)
 local m,P,Q,M;
 m:=Length(t);
 if m<=2 then return true;fi;
 if not CheckIP(t{[2..m]}) then return false;fi;
 P:=Group(t{[1..m-1]});Q:=Group(t{[2..m]});M:=Group(t{[2..m-1]});
 return Intersection(P,Q)=M;
end;;
maxRank:=0;;while 2^(maxRank+1)<=Size(G) do maxRank:=maxRank+1;od;
prefixes:=List([0..maxRank],x->0);;
leaves:=List([0..maxRank],x->[]);;
commutingSets:=[];;
GetCommuting:=function(i)
 if not IsBound(commutingSets[i]) then
  commutingSets[i]:=Filtered([1..Length(ivs)],j->Comm(ivs[i],ivs[j])=One(G));
 fi;
 return commutingSets[i];
end;;
pruned:=0;;visits:=0;;
Visit:=function(ids,H,St,pool)
 local t,m,candidates,orbs,orb,j,x,newt,newH,newids,newSt,nextPool,possible;
 m:=Length(ids);prefixes[m+1]:=prefixes[m+1]+1;visits:=visits+1;
 if visits mod 1000=0 then Print("PROGRESS ",visits," ",prefixes," LEAVES ",List(leaves,Length),"\n");fi;
 if H=G then Add(leaves[m+1],ShallowCopy(ids));return;fi;
 if m=maxRank then return;fi;
 if m>=2 then
  possible:=Group(Concatenation(GeneratorsOfGroup(H),List(pool,i->ivs[i])));
  if possible<>G then pruned:=pruned+1;return;fi;
 fi;
 t:=List(ids,i->ivs[i]);
 candidates:=Filtered(pool,i->not ivs[i] in H);
 if m=0 then nextPool:=pool;else nextPool:=Intersection(pool,GetCommuting(ids[m]));fi;
 orbs:=Orbits(St,List(candidates,i->ivs[i]),OnPoints);
 for orb in orbs do
  x:=Minimum(orb);j:=PositionSorted(ivs,x);newt:=Concatenation(t,[x]);
  if CheckIP(newt) then
   newH:=Group(newt);newids:=Concatenation(ids,[j]);
   newSt:=Centralizer(St,x);
   Visit(newids,newH,newSt,nextPool);
  fi;
 od;
end;;
Visit([],TrivialSubgroup(G),A,[1..Length(ivs)]);;
Print("PREFIX_CLASSES ",prefixes,"\n");
Print("PRUNED_IMPOSSIBLE_COMPLETIONS ",pruned,"\n");
for m in [1..maxRank] do
 ts:=leaves[m+1];;
 self:=Number(ts,t->RepresentativeAction(A,List(t,i->ivs[i]),List(Reversed(t),i->ivs[i]),OnTuples)<>fail);;
 connected:=Filtered(ts,t->ForAll([1..m-1],j->Order(ivs[t[j]]*ivs[t[j+1]])>2));;
 selfConnected:=Number(connected,t->RepresentativeAction(A,List(t,i->ivs[i]),List(Reversed(t),i->ivs[i]),OnTuples)<>fail);;
 Print("RANK ",m," ordered ",Length(ts)," self ",self," dual_classes ",(Length(ts)+self)/2,
       " connected_ordered ",Length(connected)," connected_self ",selfConnected,
       " connected_dual ",(Length(connected)+selfConnected)/2,"\n");
 Print("COMPLETE_MARKS_RANK_",m," ",ts,"\n");
od;
Print("COMPLETE_EXHAUSTION\n");
QUIT;
