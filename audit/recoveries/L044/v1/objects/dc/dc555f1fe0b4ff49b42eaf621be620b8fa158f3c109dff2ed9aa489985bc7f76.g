Read("model.g");;
CheckString:=function(t)
 local m;
 m:=Length(t);if m<=2 then return true;fi;
 return CheckString(t{[1..m-1]}) and CheckString(t{[2..m]}) and
 Intersection(Group(t{[1..m-1]}),Group(t{[2..m]}))=Group(t{[2..m-1]});
end;;
PartialC:=function(t,selected,H)
 local blocks,b,i;
 blocks:=[];b:=[];
 for i in selected do
  if Length(b)>0 and i<>b[Length(b)]+1 then Add(blocks,b);b:=[];fi;
  Add(b,i);
 od;
 if Length(b)>0 then Add(blocks,b);fi;
 for b in blocks do if not CheckString(t{b}) then return false;fi;od;
 return Product(blocks,b->Size(Group(t{b})))=Size(H);
end;;
allWElements:=Elements(W);;
referenceCalls:=0;;referencePairs:=0;;
ReferenceIP:=function(t)
 local m,sets,subsets,i,j,k;
 m:=Length(t);sets:=Combinations([1..m]);
 subsets:=List(sets,s->BlistList(allWElements,Elements(Group(Concatenation([()],t{s})))));
 referenceCalls:=referenceCalls+1;
 for i in [1..Length(sets)] do for j in [1..i] do
  k:=Position(sets,Intersection(sets[i],sets[j]));referencePairs:=referencePairs+1;
  if IntersectionBlist(subsets[i],subsets[j])<>subsets[k] then return false;fi;
 od;od;
 return true;
end;;
allInvolutions:=Filtered(Elements(W),x->Order(x)=2);;
nodes:=List([0..5],i->0);;leaves:=[];;allLeaves:=0;;
VisitFive:=function(labelOrder,t,selected,H,St)
 local m,j,pool,orbs,orb,x,u,ss,newH,fast,slow;
 m:=Length(selected);nodes[m+1]:=nodes[m+1]+1;
 if Sum(nodes)mod 1000=0 then Print("PROGRESS ",nodes," transitive ",Length(leaves),"\n");fi;
 if Sum(nodes)>100000 then Print("NODE_CAP_NOT_EXHAUSTION\n");QUIT_GAP(2);fi;
 if m=5 then
  allLeaves:=allLeaves+1;
  if IsTransitive(H,[1..16]) then Add(leaves,List(selected,i->t[i]));fi;
  return;
 fi;
 j:=labelOrder[m+1];
 pool:=Filtered(allInvolutions,x->not x in H and
  ForAll(selected,i->(AbsInt(i-j)>1 and t[i]*x=x*t[i]) or
   (AbsInt(i-j)=1 and t[i]*x<>x*t[i])));
 orbs:=OrbitsDomain(St,pool,OnPoints);
 if Sum(orbs,Length)<>Length(pool) or Set(Concatenation(orbs))<>Set(pool)
 then Error("direct orbit coverage");fi;
 for orb in orbs do
  x:=orb[1];u:=ShallowCopy(t);u[j]:=x;
  ss:=Set(Concatenation(selected,[j]));newH:=Group(u{ss});
  fast:=PartialC(u,ss,newH);slow:=ReferenceIP(u{ss});
  if fast<>slow then Error("partial criterion disagrees with full subset intersections");fi;
  if fast then VisitFive(labelOrder,u,ss,newH,Centralizer(St,x));fi;
 od;
end;;
