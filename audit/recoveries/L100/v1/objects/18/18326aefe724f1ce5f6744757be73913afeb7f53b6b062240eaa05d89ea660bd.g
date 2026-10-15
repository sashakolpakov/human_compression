RunBorelFromLevel:=function(bid,resume)
 local B,N,panels,hom,A,orders,paircache,PairJoin,Equivalent,levels,rank,next,sigs,checked,ix,t,H,C,over,poss,orb,oo,x,u,K,sig,bucket,allFull,checkpoint,maxrank;
 B:=reps[bid];N:=Normalizer(G,B);if REQUIRE_2T then panels:=OvergroupsFromInclusions(B,local2T);
 else panels:=OvergroupsFromInclusions(B,maxinclusions);fi;
 if Set(panels)<>Set(resume.panels) then Error("saved panel inventory changed");fi;
 panels:=resume.panels;
 Print("BOREL_BEGIN id=",bid," order=",Size(B)," normalizer=",Size(N)," panels=",Length(panels),"\n");
 if Length(panels)=0 then
  PrintTo(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"),"borelResult:=rec(id:=",bid,",order:=",Size(B),",levels:=[],geometries:=[]);\n");
  Print("BOREL_COMPLETE id=",bid," rank_counts=[] full_group=[]\n");return;
 fi;
 hom:=ActionHomomorphism(N,panels,OnPoints);A:=Image(hom);orders:=List(panels,Size);paircache:=[];
 PairJoin:=function(i,j)
  local l,h,K;
  l:=Minimum(i,j);h:=Maximum(i,j);
  if not IsBound(paircache[l]) then paircache[l]:=[];fi;
  if not IsBound(paircache[l][h]) then paircache[l][h]:=RankTwoAdmissible(B,panels[l],panels[h]);fi;
  return paircache[l][h];
 end;
 Equivalent:=function(a,b)
  local p,ord,g,C,x,i;
  for p in SymmetricGroup(Length(a)) do
   ord:=Permuted(b,p);
   if orders{a}<>orders{ord} then continue;fi;
   if not ForAll(Combinations([1..Length(a)],2),ij->Size(PairJoin(a[ij[1]],a[ij[2]]))=Size(PairJoin(ord[ij[1]],ord[ij[2]]))) then continue;fi;
   g:=();C:=A;
   for i in [1..Length(a)] do
    x:=RepresentativeAction(C,a[i]^g,ord[i]);
    if x=fail then break;fi;
    g:=g*x;C:=Stabilizer(C,ord[i]);
   od;
   if x<>fail then return true;fi;
  od;
  return false;
 end;
 levels:=ShallowCopy(resume.levels);allFull:=ShallowCopy(resume.geometries);
 Print("BOREL_RESUME id=",bid," completed_levels=",List(levels,Length)," next_rank=",Length(levels)+1,"\n");
 maxrank:=Length(FactorsInt(Index(G,B)))+1;
 for rank in [Length(levels)+1..maxrank] do
  next:=[];sigs:=[];checked:=0;
  for ix in [1..Length(levels[rank-1])] do
   t:=levels[rank-1][ix];H:=JoinPanels(B,panels{t});C:=A;
   for x in t do C:=Stabilizer(C,x);od;
   over:=OvergroupsFromInclusions(H,maxinclusions);
   poss:=Filtered([1..Length(panels)],x->not IsSubgroup(H,panels[x]) and ForAny(over,K->IsSubgroup(K,panels[x])) and ForAll(t,y->PairJoin(x,y)<>fail));
   orb:=Orbits(C,poss);
   for oo in orb do
    x:=oo[1];u:=Concatenation(t,[x]);K:=First(over,K->IsSubgroup(K,panels[x]));checked:=checked+1;
    sig:=[Size(K),SortedList(orders{u}),SortedList(List(Combinations(u,2),ij->Size(PairJoin(ij[1],ij[2]))))];
    bucket:=Filtered([1..Length(next)],i->sigs[i]=sig);
    if ForAny(bucket,i->Equivalent(next[i],u)) then continue;fi;
    if not ValidPanels(B,panels{u}) then continue;fi;
    Add(next,u);Add(sigs,sig);
    if K=G then Add(allFull,panels{u});fi;
   od;
   if ix mod 10=0 or ix=Length(levels[rank-1]) then Print("BOREL_PROGRESS id=",bid," rank=",rank," anchor=",ix,"/",Length(levels[rank-1])," checked=",checked," accepted=",Length(next),"\n");fi;
  od;
  levels[rank]:=next;
  Print("BOREL_LEVEL id=",bid," rank=",rank," classes=",Length(next)," full_group=",Number(next,t->JoinPanels(B,panels{t})=G),"\n");
  checkpoint:=Concatenation(OUTPUT_DIR,"/b",String(bid),"_r",String(rank),".g");
  PrintTo(checkpoint,"borelCheckpoint:=rec(id:=",bid,",order:=",Size(B),",rank:=",rank,",panels:=",panels,",level:=",next,",geometries:=",allFull,");\n");
  if Length(next)=0 then break;fi;
 od;
 if Length(levels[Length(levels)])<>0 then Error("chain bound reached without an empty level");fi;
 PrintTo(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"),"borelResult:=rec(id:=",bid,",order:=",Size(B),",levels:=",List(levels,Length),",geometries:=",allFull,");\n");
 Print("BOREL_COMPLETE id=",bid," rank_counts=",List(levels,Length)," full_group_ranks=",List(allFull,Length),"\n");
end;
