# Exact budget-three transitions for the proved phase20 finite-state theorem.
# Requires DATA_FILE22 and OUTPUT_PREFIX22 to be bound before Read.
# The Python runner writes verified original mathematical kernel data only.
if LoadPackage("nq")=fail then Error("NQ required");fi;
if not IsBound(DATA_FILE22) or not IsBound(OUTPUT_PREFIX22) then
 Error("Set DATA_FILE22 and OUTPUT_PREFIX22");
fi;
SizeScreen([240,40]);;
data22:=fail;;Read(DATA_FILE22);;
if data22=fail then Error("Missing verified kernel data");fi;

Universal22:=function(d)
 local F,f,rel,i,j,Q,ep,iso,G,r,pc;
 F:=FreeGroup(d);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;
 od;od;
 Q:=F/rel;ep:=NqEpimorphismNilpotentQuotient(Q,5);
 iso:=IsomorphismPcGroup(Image(ep));G:=Image(iso);
 r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(ep,x)));pc:=Pcgs(G);
 if not ForAll(RelativeOrders(pc),x->x=2) then Error("Binary pc coordinates");fi;
 return rec(G:=G,r:=r,pc:=pc,K:=LowerCentralSeries(G)[3]);
end;;
Key22:=function(pc,H)
 local w;
 w:=List([1..Length(pc)],i->2^(i-1));
 return List(CanonicalPcgs(InducedPcgsByGenerators(pc,GeneratorsOfGroup(H))),
  x->ExponentsOfPcElement(pc,x)*w);
end;;
Decode22:=function(pc,key)
 if key<0 or key>=2^Length(pc) then Error("Out-of-range pc key");fi;
 return Product(List([1..Length(pc)],i->pc[i]^(QuoInt(key,2^(i-1)) mod 2)));
end;;
IP22:=function(G,r)
 local ss,pars,i,j,at;
 ss:=Combinations([1..Length(r)]);pars:=List(ss,S->Subgroup(G,r{S}));
 for i in [1..Length(ss)] do for j in [1..Length(ss)] do
  at:=Position(ss,Intersection(ss[i],ss[j]));
  if Intersection(pars[i],pars[j])<>pars[at] then return false;fi;
 od;od;
 return true;
end;;
BoundaryKey22:=function(U,B,r)
 local ep;
 ep:=GroupHomomorphismByImages(U.G,B,U.r,r);
 if ep=fail or not IsSurjective(ep) then Error("Universal boundary map");fi;
 return Key22(U.pc,Kernel(ep));
end;;

start22:=Runtime();;
U22:=Universal22(5);;B22:=Universal22(4);;
Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
Print("UNIVERSAL rank5=",Size(U22.G)," rank4=",Size(B22.G),"\n");
ss22:=Combinations([1..5]);;
ks22:=List(ss22,S->Intersection(U22.K,Subgroup(U22.G,U22.r{S})));;
keys22:=[ [Key22(U22.pc,U22.K)],data22[1],data22[2],data22[3] ];;
pool22:=[];;counts22:=[0,0,0,0];;candidateCounts22:=[];;profileTests22:=0;;actualMeets22:=0;;
qp22:=fail;;q22:=fail;;old22:=fail;;dist22:=0;;
for e22 in [0..3] do
 Add(candidateCounts22,Length(keys22[e22+1]));
 for nkey22 in keys22[e22+1] do
  N22:=Subgroup(U22.G,List(nkey22,x->Decode22(U22.pc,x)));;
  if not IsNormal(U22.G,N22) or not IsSubgroup(U22.K,N22) or
   Index(U22.K,N22)<>2^e22 or Key22(U22.pc,N22)<>nkey22 then Error("Restored kernel");fi;
  qp22:=NaturalHomomorphismByNormalSubgroup(U22.K,N22);;
  kpars22:=List(ks22,H->Image(qp22,H));;good22:=true;;
  for i22 in [1..Length(ss22)] do
   for j22 in [i22+1..Length(ss22)] do
    at22:=Position(ss22,Intersection(ss22[i22],ss22[j22]));;
    profileTests22:=profileTests22+1;
    if Intersection(kpars22[i22],kpars22[j22])<>kpars22[at22] then good22:=false;break;fi;
   od;
   if not good22 then break;fi;
  od;
  if not good22 then
   if e22=3 then Error("Saved accepted kernel failed fresh profile");fi;
   continue;
  fi;
  q22:=NaturalHomomorphismByNormalSubgroup(U22.G,N22);;G22:=Image(q22);;
  r22:=List(U22.r,x->Image(q22,x));;
  if Size(G22)<>2^(9+e22) or Subgroup(G22,r22)<>G22 then Error("Window order/marking");fi;
  if not IP22(G22,r22) then Error("Fresh actual window IP");fi;
  actualMeets22:=actualMeets22+1024;
  h22:=rec(G:=G22,r:=r22,excess:=e22,sourceKey:=nkey22,pc:=Pcgs(G22));;
  if not ForAll(RelativeOrders(h22.pc),x->x=2) then Error("Window pc coordinates");fi;
  h22.first:=Subgroup(G22,r22{[1..4]});h22.last:=Subgroup(G22,r22{[2..5]});
  h22.firstKey:=BoundaryKey22(B22,h22.first,r22{[1..4]});
  h22.lastKey:=BoundaryKey22(B22,h22.last,r22{[2..5]});
  h22.N:=NormalClosure(G22,Subgroup(G22,[r22[5]]));
  h22.J:=Intersection(h22.N,h22.first);
  h22.lastKernel:=Intersection(Image(q22,U22.K),h22.last);
  h22.R:=Intersection(h22.last,NormalClosure(G22,Subgroup(G22,[r22[1]])));
  if not IsSubgroup(h22.lastKernel,h22.R) or Size(h22.lastKernel)>8 then Error("Initial defect bound");fi;
  Add(pool22,h22);counts22[e22+1]:=counts22[e22+1]+1;
  if Length(pool22) mod 50=0 then Print("WINDOW_PROGRESS accepted=",Length(pool22)," elapsed_ms=",Runtime()-start22,"\n");fi;
 od;
 Print("WINDOW_LEVEL excess=",e22," accepted=",counts22[e22+1]," elapsed_ms=",Runtime()-start22,"\n");
od;
if counts22<>[1,15,106,584] then Error("Window census disagrees with retained completed counts");fi;
Print("WINDOWS candidates=",candidateCounts22," accepted=",counts22," actual_meets=",actualMeets22," profile_meets=",profileTests22,"\n");

# Exact boundary kernels identify ordered marked boundary isomorphism types.
firstIndex22:=NewDictionary([],true);;
for hi22 in [1..Length(pool22)] do
 key22:=pool22[hi22].firstKey;;bucket22:=LookupDictionary(firstIndex22,key22);;
 if bucket22=fail then bucket22:=[];AddDictionary(firstIndex22,key22,bucket22);fi;
 Add(bucket22,hi22);
od;
overlaps22:=[];;overlapPairs22:=0;;centralReject22:=0;;
for oi22 in [1..Length(pool22)] do
 old22:=pool22[oi22];;bucket22:=LookupDictionary(firstIndex22,old22.lastKey);;
 if bucket22=fail then bucket22:=[];fi;
 entries22:=[];;
 for hi22 in bucket22 do
  h22:=pool22[hi22];;overlapPairs22:=overlapPairs22+1;
  theta22:=GroupHomomorphismByImages(old22.last,h22.first,old22.r{[2..5]},h22.r{[1..4]});;
  if theta22=fail or not IsBijective(theta22) then Error("Matching boundary keys failed actual marked isomorphism");fi;
  preJ22:=PreImage(theta22,h22.J);;
  if not ForAll(GeneratorsOfGroup(preJ22),x->Comm(x,old22.r[1])=One(old22.G)) then
   centralReject22:=centralReject22+1;continue;
  fi;
  w22:=LogInt(Index(h22.G,h22.first),2)-2;
  if w22<0 or w22>3 then Error("Window transition weight");fi;
  Add(entries22,rec(hi:=hi22,theta:=theta22,weight:=w22));
 od;
 Add(overlaps22,entries22);
 if oi22 mod 100=0 then Print("OVERLAP_PROGRESS old=",oi22," pairs=",overlapPairs22," elapsed_ms=",Runtime()-start22,"\n");fi;
od;
Print("OVERLAPS exact_pairs=",overlapPairs22," centralization_rejected=",centralReject22,"\n");

# Dijkstra on nonnegative excess weights retains every path of total cost<=3.
states22:=[];;byWindow22:=List(pool22,h->[]);;
FindState22:=function(hi,R,cost)
 local i;
 if cost<pool22[hi].excess then Error("Global excess smaller than window excess");fi;
 for i in byWindow22[hi] do
  if states22[i].R=R then
   if cost<states22[i].cost then
    if states22[i].done then Error("Dijkstra finalized too early");fi;
    states22[i].cost:=cost;
   fi;
   return i;
  fi;
 od;
 Add(states22,rec(hi:=hi,R:=R,cost:=cost,done:=false));
 i:=Length(states22);Add(byWindow22[hi],i);return i;
end;;
initial22:=[];;
for hi22 in [1..Length(pool22)] do
 h22:=pool22[hi22];;Add(initial22,[FindState22(hi22,h22.R,h22.excess),h22.excess]);
od;
edges22:=[];;actionReject22:=0;;budgetReject22:=0;;attempts22:=0;;processed22:=0;;
while true do
 pending22:=Filtered([1..Length(states22)],i->not states22[i].done);;
 if Length(pending22)=0 then break;fi;
 dist22:=Minimum(List(pending22,i->states22[i].cost));;
 si22:=First(pending22,i->states22[i].cost=dist22);;st22:=states22[si22];;
 old22:=pool22[st22.hi];;st22.done:=true;
 for ed22 in overlaps22[st22.hi] do
  if dist22+ed22.weight>3 then budgetReject22:=budgetReject22+1;continue;fi;
  attempts22:=attempts22+1;h22:=pool22[ed22.hi];;
  imR22:=Image(ed22.theta,st22.R);;
  if Size(CommutatorSubgroup(imR22,h22.N))<>1 then actionReject22:=actionReject22+1;continue;fi;
  Rnew22:=Intersection(h22.last,NormalClosure(h22.G,ClosureGroup(imR22,h22.r[1])));;
  if not IsSubgroup(h22.lastKernel,Rnew22) then Error("Updated defect escapes gamma3 boundary");fi;
  ni22:=FindState22(ed22.hi,Rnew22,dist22+ed22.weight);;
  Add(edges22,[si22,ni22,ed22.weight]);
 od;
 processed22:=processed22+1;
 if processed22 mod 100=0 then Print("STATE_PROGRESS processed=",processed22," states=",Length(states22)," edges=",Length(edges22)," elapsed_ms=",Runtime()-start22,"\n");fi;
od;
if Length(Set(edges22))<>Length(edges22) then Error("Duplicate transition");fi;
Print("GRAPH states=",Length(states22)," transitions=",Length(edges22)," attempts=",attempts22," action_rejected=",actionReject22," budget_rejected=",budgetReject22,"\n");

# Exercise every additional deletion state by an actual one-step gluing,
# when (as in this bounded run) it has an incoming initial-state edge.
GlueCheck22:=function(old,h,targetR)
 local P,N,ng,maps,i,actor,aut,action,SD,ep,en,theta,jgens,D,qu,G,r,
  Himage,Pimage,hm,pm,realR;
 P:=old.G;N:=h.N;ng:=GeneratorsOfGroup(N);
 maps:=List([1..5],i->IdentityMapping(N));
 for i in [2..5] do
  actor:=h.r[i-1];
  maps[i]:=GroupHomomorphismByImages(N,N,ng,List(ng,x->x^actor));
 od;
 aut:=Group(maps);
 if not IsGroupOfAutomorphisms(aut) then Error("Gluing action maps");fi;
 action:=GroupHomomorphismByImages(P,aut,old.r,maps);
 if action=fail then Error("Actual prefix action fails");fi;
 SD:=SemidirectProduct(P,action,N);ep:=Embedding(SD,1);en:=Embedding(SD,2);
 theta:=GroupHomomorphismByImages(old.last,h.first,old.r{[2..5]},h.r{[1..4]});
 jgens:=GeneratorsOfGroup(h.J);
 D:=Subgroup(SD,List(jgens,j->Image(ep,PreImagesRepresentative(theta,j))*Image(en,j^-1)));
 if not IsNormal(SD,D) or Size(D)<>Size(h.J) then Error("Actual diagonal subgroup");fi;
 qu:=NaturalHomomorphismByNormalSubgroup(SD,D);G:=Image(qu);
 r:=Concatenation(List(old.r,x->Image(qu,Image(ep,x))),[Image(qu,Image(en,h.r[5]))]);
 if Subgroup(G,r)<>G or Size(G)<>Size(P)*Index(h.G,h.first) then Error("Glued order/marking");fi;
 if Length(LowerCentralSeries(G))-1>5 or not IP22(G,r) then Error("Glued class or actual IP");fi;
 Himage:=Subgroup(G,r{[2..6]});Pimage:=Subgroup(G,r{[1..5]});
 hm:=GroupHomomorphismByImages(h.G,Himage,h.r,r{[2..6]});
 pm:=GroupHomomorphismByImages(P,Pimage,old.r,r{[1..5]});
 if hm=fail or pm=fail or not IsBijective(hm) or not IsBijective(pm) then Error("Actual factor embeddings");fi;
 realR:=Intersection(Subgroup(G,r{[3..6]}),NormalClosure(G,Subgroup(G,r{[1,2]})));
 if realR<>Image(hm,targetR) then Error("Actual deletion kernel mismatch");fi;
 return [Size(G),Size(h.J),Size(realR),4096];
end;;
initialStates22:=Set(List(initial22,x->x[1]));;glueRows22:=[];;si22:=0;;
for si22 in Difference([1..Length(states22)],initialStates22) do
 incoming22:=Filtered(edges22,e->e[2]=si22 and e[1] in initialStates22);;
 if Length(incoming22)=0 then Error("Additional-state diagnostic needs longer witness walk");fi;
 ed22:=incoming22[1];;
 gr22:=GlueCheck22(pool22[states22[ed22[1]].hi],pool22[states22[si22].hi],states22[si22].R);;
 Add(glueRows22,Concatenation([ed22[1],si22],gr22));
od;
Print("EXTRA_STATE_GLUINGS ",glueRows22,"\n");

dp22:=List(states22,s->[0,0,0,0]);;
for init22 in initial22 do dp22[init22[1]][init22[2]+1]:=dp22[init22[1]][init22[2]+1]+1;od;
values22:=[];;
for d22 in [5..24] do
 coeff22:=List([1..4],k->Sum(dp22,v->v[k]));;Add(values22,Concatenation([d22],coeff22));;
 if coeff22{[1..3]}<>[1,5*d22-10,(25*d22^2-107*d22+122)/2] then Error("Known lower-excess transfer disagreement");fi;
 Print("COUNT rank=",d22," coefficients=",coeff22,"\n");
 next22:=List(states22,s->[0,0,0,0]);;
 for ed22 in edges22 do
  for k22 in [0..3-ed22[3]] do
   next22[ed22[2]][k22+ed22[3]+1]:=next22[ed22[2]][k22+ed22[3]+1]+dp22[ed22[1]][k22+1];
  od;
 od;
 dp22:=next22;
od;
stateRows22:=List(states22,s->[s.hi,Key22(pool22[s.hi].pc,s.R),s.cost,Size(s.R)]);;
windowRows22:=List(pool22,h->[h.sourceKey,h.excess,h.firstKey,h.lastKey]);;
PrintTo(Concatenation(OUTPUT_PREFIX22,".graph.json"),[initial22,stateRows22,edges22,values22],"\n");
PrintTo(Concatenation(OUTPUT_PREFIX22,".windows.json"),windowRows22,"\n");
PrintTo(Concatenation(OUTPUT_PREFIX22,".gluings.json"),glueRows22,"\n");
Print("PASS exact budget-three window reconstruction, actual-IP verification, both transition tests, and weighted transfer; elapsed_ms=",Runtime()-start22,"\n");
QUIT;
