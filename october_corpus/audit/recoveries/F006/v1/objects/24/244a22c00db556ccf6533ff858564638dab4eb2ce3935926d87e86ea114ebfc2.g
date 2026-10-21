# Exploratory complete orbit-prefix enumeration. No source credit before review.
if not IsBound(modelFile) then modelFile:="F4_model.g";fi;
Read(modelFile);;
if Size(G)<>expectedOrder then Error("model order");fi;
Print("MODEL ",modelName," order ",Size(G),"\n");
involutionClasses:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
ivs:=Set(Concatenation(List(involutionClasses,AsList)));;
if Length(ivs)<>Sum(involutionClasses,Size) then Error("involution class coverage");fi;
Print("INVOLUTIONS ",Length(ivs),"\n");
aut:=AutomorphismGroup(G);;
act:=ActionHomomorphism(aut,ivs,OnPoints);;
A:=Image(act);;
if Size(A)<>Size(aut) then Error("unfaithful involution action");fi;
Print("AUT_ORDER ",Size(A),"\n");
Print("MODEL_GENERATORS ",GeneratorsOfGroup(G),"\n");
Print("INVOLUTIONS_LITERAL ",ivs,"\n");
Print("AUT_ACTION_GENERATORS ",GeneratorsOfGroup(A),"\n");

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
Visit:=function(ids,H,St)
 local t,m,candidates,orbs,orb,j,x,newt,newH,newids,newSt;
 m:=Length(ids);prefixes[m+1]:=prefixes[m+1]+1;
 if H=G then Add(leaves[m+1],ShallowCopy(ids));return;fi;
 if m=maxRank then return;fi;
 t:=List(ids,i->ivs[i]);
 candidates:=Filtered([1..Length(ivs)],i->not ivs[i] in H and
     ForAll([1..Maximum(0,m-1)],j->Comm(t[j],ivs[i])=One(G)));
 orbs:=Orbits(St,candidates,OnPoints);
 for orb in orbs do
  j:=Minimum(orb);x:=ivs[j];newt:=Concatenation(t,[x]);
  if CheckIP(newt) then
   newH:=Group(newt);newids:=Concatenation(ids,[j]);
   newSt:=Stabilizer(St,j,OnPoints);
   Visit(newids,newH,newSt);
  fi;
 od;
end;;
Visit([],TrivialSubgroup(G),A);;
Print("PREFIX_CLASSES ",prefixes,"\n");
for m in [1..maxRank] do
 ts:=leaves[m+1];;
 self:=Number(ts,t->RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail);;
 connected:=Filtered(ts,t->ForAll([1..m-1],j->Order(ivs[t[j]]*ivs[t[j+1]])>2));;
 selfConnected:=Number(connected,t->RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail);;
 Print("RANK ",m," ordered ",Length(ts)," self ",self," dual_classes ",(Length(ts)+self)/2,
       " connected_ordered ",Length(connected)," connected_self ",selfConnected,
       " connected_dual ",(Length(connected)+selfConnected)/2,"\n");
 Print("COMPLETE_MARKS_RANK_",m," ",ts,"\n");
od;
Print("COMPLETE_EXHAUSTION\n");
QUIT;
