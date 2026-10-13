# Fixed-rank enumeration in the order 1,r,2,r-1,... .
# Every intermediate tuple is tested as the direct product of its contiguous
# components, each itself a string C-marking. Candidate orbits use exactly
# the acquired centralizer/double-coset lemma, with a different set of fixed marks.
Read(modelFile);;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>expectedAutOrder then Error("full action");fi;
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
 for b in blocks do
  if not CheckString(t{b}) then return false;fi;
 od;
 return Product(blocks,b->Size(Group(t{b})))=Size(H);
end;;
MakePool:=function(Q)
 local classes;
 classes:=Filtered(ConjugacyClasses(Q),c->Order(Representative(c))=2 and Representative(c) in G);
 return List(classes,Representative);
end;;
if IsBound(computeOddRankBound) and computeOddRankBound then
 syl:=SylowSubgroup(G,2);;pcs:=Image(IsomorphismPcGroup(syl));;
 cs:=ConjugacyClassesSubgroups(pcs);;
 maxElementary:=Maximum(List(Filtered(cs,c->Exponent(Representative(c))<=2),c->Size(Representative(c))));;
 twoRank:=LogInt(maxElementary,2);;
 Print("EXACT_SYLOW_BOUND order ",Size(syl)," subgroup_classes ",Length(cs)," max_elementary_order ",maxElementary," rank_bound ",2*twoRank,"\n");
 ranksToRun:=[4..2*twoRank];;
fi;
nodes:=[];;leaves:=[];;
VisitEnds:=function(rank,order,t,selected,H,St)
 local m,j,fixed,Q,pool,y,C,dc,d,x,u,ss,newH,i,self;
 m:=Length(selected);nodes[m+1]:=nodes[m+1]+1;
 if Sum(nodes) mod 1000=0 then Print("PROGRESS_RANK ",rank," ",nodes," LEAVES ",Length(leaves),"\n");fi;
 if H=G then
  if m=rank then Add(leaves,List([1..rank],i->t[i]));fi;
  return;
 fi;
 if m=rank then return;fi;
 j:=order[m+1];fixed:=Filtered(selected,i->AbsInt(i-j)>1);
 Q:=A;for i in fixed do Q:=Centralizer(Q,t[i]);od;
 if not IsSubgroup(Q,St) then Error("orbit stabilizer outside commuting pool");fi;
 pool:=MakePool(Q);
 for y in pool do
  C:=Centralizer(Q,y);dc:=DoubleCosetRepsAndSizes(Q,C,St);
  if Sum(dc,d->d[2])<>Size(Q) then Error("double coset coverage");fi;
  for d in dc do
   x:=y^d[1];
   if not x in H and ForAll(Filtered(selected,i->AbsInt(i-j)=1),i->Order(t[i]*x)>2) then
    u:=ShallowCopy(t);u[j]:=x;ss:=Set(Concatenation(selected,[j]));newH:=Group(u{ss});
    if PartialC(u,ss,newH) then
     VisitEnds(rank,order,u,ss,newH,Centralizer(St,x));
    fi;
   fi;
  od;
 od;
end;;
for rank in ranksToRun do
 labelOrder:=[];;lo:=1;;hi:=rank;;
 while lo<=hi do
  Add(labelOrder,lo);if lo<>hi then Add(labelOrder,hi);fi;lo:=lo+1;hi:=hi-1;
 od;
 nodes:=List([0..rank],x->0);;leaves:=[];;
 VisitEnds(rank,labelOrder,[],[],TrivialSubgroup(G),A);;
 self:=Number(leaves,t->RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail);;
 Print("RANK ",rank," ordered ",Length(leaves)," self ",self," dual_classes ",(Length(leaves)+self)/2,"\n");
 Print("NODE_COUNTS ",rank," ",nodes,"\n");
 Print("COMPLETE_TUPLES_RANK_",rank," ",leaves,"\n");
od;
Print("COMPLETE_ENDS_EXHAUSTION\n");
QUIT;
