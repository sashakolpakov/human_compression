# Enumeration through classes in centralizers; no scientific credit until reviewed.
Read(modelFile);;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model or normality");fi;
fullAutOrder:=Size(AutomorphismGroup(G));;
if Size(A)/Size(Centralizer(A,G))<>fullAutOrder then Error("incomplete automorphism action");fi;
forbiddenMarks:=Intersection(Centre(G),DerivedSubgroup(G));;
Print("FORBIDDEN_CENTRAL_DERIVED_ORDER ",Size(forbiddenMarks),"\n");
Print("MODEL ",modelName," ORDER ",Size(G)," AUT_ORDER ",fullAutOrder,"\n");
Print("MODEL_GENERATORS ",GeneratorsOfGroup(G),"\n");
Print("CONJUGATING_GENERATORS ",GeneratorsOfGroup(A),"\n");
CheckIP:=function(t)
 local m,P,Q,M;
 m:=Length(t);if m<=2 then return true;fi;
 if not CheckIP(t{[2..m]}) then return false;fi;
 P:=Group(t{[1..m-1]});Q:=Group(t{[2..m]});M:=Group(t{[2..m-1]});
 return Intersection(P,Q)=M;
end;;
MakePool:=function(Q)
 local classes,reps,K;
 classes:=Filtered(ConjugacyClasses(Q),c->Order(Representative(c))=2 and Representative(c) in G and not Representative(c) in forbiddenMarks);
 reps:=List(classes,Representative);
 K:=NormalClosure(Q,Group(Concatenation([One(G)],reps)));
 if not IsSubgroup(G,K) then Error("pool left G");fi;
 return rec(group:=Q,reps:=reps,closure:=K);
end;;
maxRank:=0;;while 2^(maxRank+1)<=Size(G) do maxRank:=maxRank+1;od;
prefixes:=List([0..maxRank],x->0);;
leaves:=List([0..maxRank],x->[]);;
visits:=0;;pruned:=0;;
Visit:=function(t,H,St,pool)
 local m,nextPool,y,C,dc,d,x,u,newH;
 m:=Length(t);prefixes[m+1]:=prefixes[m+1]+1;visits:=visits+1;
 if visits mod 1000=0 then Print("PROGRESS ",visits," ",prefixes," LEAVES ",List(leaves,Length),"\n");fi;
 if H=G then Add(leaves[m+1],ShallowCopy(t));return;fi;
 if m=maxRank then return;fi;
 if m>=2 and Group(Concatenation(GeneratorsOfGroup(H),GeneratorsOfGroup(pool.closure)))<>G then
  pruned:=pruned+1;return;
 fi;
 if not IsSubgroup(pool.group,St) then Error("stabilizer outside pool group");fi;
 nextPool:=fail;
 for y in pool.reps do
  C:=Centralizer(pool.group,y);
  dc:=DoubleCosetRepsAndSizes(pool.group,C,St);
  if Sum(dc,d->d[2])<>Size(pool.group) then Error("double-coset coverage sizes");fi;
  for d in dc do
   x:=y^d[1];
   if not x in H then
    u:=Concatenation(t,[x]);
    if CheckIP(u) then
     if nextPool=fail then
      if St=pool.group then nextPool:=pool;else nextPool:=MakePool(St);fi;
     fi;
     newH:=Group(u);
     Visit(u,newH,Centralizer(St,x),nextPool);
    fi;
   fi;
  od;
 od;
end;;
Visit([],TrivialSubgroup(G),A,MakePool(A));;
Print("PREFIX_CLASSES ",prefixes,"\n");
Print("PRUNED_IMPOSSIBLE_COMPLETIONS ",pruned,"\n");
for m in [1..maxRank] do
 ts:=leaves[m+1];;
 self:=Number(ts,t->RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail);;
 connected:=Filtered(ts,t->ForAll([1..m-1],j->Order(t[j]*t[j+1])>2));;
 selfConnected:=Number(connected,t->RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail);;
 Print("RANK ",m," ordered ",Length(ts)," self ",self," dual_classes ",(Length(ts)+self)/2,
       " connected_ordered ",Length(connected)," connected_self ",selfConnected,
       " connected_dual ",(Length(connected)+selfConnected)/2,"\n");
 Print("COMPLETE_TUPLES_RANK_",m," ",ts,"\n");
od;
Print("COMPLETE_EXHAUSTION\n");QUIT;

