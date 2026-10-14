# Exhaustive partial C-markings in Alt(n), up to conjugation by Sym(n).
# This working program supplies no certificate until complete and reviewed.
if not IsBound(degree) then degree:=5;fi;
if not IsBound(rankLimit) then rankLimit:=5;fi;
if degree<5 then Error("connected target requires degree at least five");fi;
G:=SymmetricGroup(degree);;A:=SymmetricGroup(degree);;
classes:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
ivs:=Set(Concatenation(List(classes,AsList)));;
if Length(ivs)<>Sum(classes,Size) then Error("involution union");fi;
Print("DEGREE ",degree," RANK_LIMIT ",rankLimit," GROUP_ORDER ",Size(G),"\n");
Print("INVOLUTIONS ",Length(ivs),"\n");
Print("INVOLUTIONS_LITERAL ",ivs,"\n");
CheckIP:=function(t)
 local m,P,Q,M;
 m:=Length(t);if m<=2 then return true;fi;
 if not CheckIP(t{[2..m]}) then return false;fi;
 P:=Group(t{[1..m-1]});Q:=Group(t{[2..m]});M:=Group(t{[2..m-1]});
 return Intersection(P,Q)=M;
end;;
commutingSets:=[];;
GetCommuting:=function(i)
 if not IsBound(commutingSets[i]) then
  commutingSets[i]:=Filtered([1..Length(ivs)],j->Comm(ivs[i],ivs[j])=One(G));
 fi;
 return commutingSets[i];
end;;
prefixes:=List([0..rankLimit],x->0);;
leaves:=List([0..rankLimit],x->[]);;
pruned:=0;;visits:=0;;
Visit:=function(ids,H,St,pool)
 local m,t,possible,candidates,nextPool,orbs,orb,x,j,newt;
 m:=Length(ids);prefixes[m+1]:=prefixes[m+1]+1;visits:=visits+1;
 if visits mod 10000=0 then Print("PROGRESS ",visits," ",prefixes,"\n");fi;
 if m>=3 and IsTransitive(H,[1..degree]) then
  Add(leaves[m+1],ShallowCopy(ids));
 fi;
 if m=rankLimit or H=G then return;fi;
 if m>=2 then
  possible:=Group(Concatenation(GeneratorsOfGroup(H),List(pool,i->ivs[i])));
  if not IsTransitive(possible,[1..degree]) then pruned:=pruned+1;return;fi;
 fi;
 t:=List(ids,i->ivs[i]);
 candidates:=Filtered(pool,i->(m=0 or Comm(ivs[ids[m]],ivs[i])<>One(G)) and not ivs[i] in H);
 if m=0 then nextPool:=pool;else nextPool:=Filtered(pool,i->Comm(ivs[ids[m]],ivs[i])=One(G));fi;
 orbs:=OrbitsDomain(St,List(candidates,i->ivs[i]),OnPoints);
 for orb in orbs do
  x:=Minimum(orb);j:=PositionSorted(ivs,x);newt:=Concatenation(t,[x]);
  if CheckIP(newt) then
   Visit(Concatenation(ids,[j]),Group(newt),Centralizer(St,x),nextPool);
  fi;
 od;
end;;
if not IsBound(rootTranspositions) then Error("root branch required");fi;
x:=First(ivs,y->NrMovedPoints(y)=2*rootTranspositions);;
if x=fail then Error("no initial involution of this cycle type");fi;
j:=PositionSorted(ivs,x);;
Print("DIRECT_INITIAL_CHILD ",rootTranspositions," INDEX ",j," PERM ",x,"\n");
Visit([j],Group(x),Centralizer(A,x),[1..Length(ivs)]);;
Print("PREFIX_CLASSES ",prefixes,"\n");
Print("PRUNED_IMPOSSIBLE_TRANSITIVITY ",pruned,"\n");
t:=[];;H:=TrivialSubgroup(G);;
for m in [3..rankLimit] do
 ts:=leaves[m+1];;
 Print("RANK ",m," MARKS ",Length(ts),"\n");
 Print("COMPLETE_MARKS_RANK_",m," ",ts,"\n");
 for ids in ts do
  t:=List(ids,i->ivs[i]);H:=Group(t);
  Print("MARK ",ids," ORDER ",Size(H)," TYPE ",List([1..m-1],i->Order(t[i]*t[i+1])),
        " SELF_DUAL_PERMUTATION ",RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail,"\n");
 od;
od;
Print("COMPLETE_EXHAUSTION\n");
QUIT;
