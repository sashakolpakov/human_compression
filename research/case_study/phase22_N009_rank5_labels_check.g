# Complete rank-five/order-1024 library and exact source facet labels.
# First-excess completeness follows independently from the reviewed phase17 theorem;
# this run enumerates all hyperplanes of the universal class-three gamma3.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([240,40]);;
Read("phase22_N009_atlas4_library.g");;
Identify5_22:=function(H,gs)
 local typ,matches,A,hom;
 typ:=List([1..3],i->Order(gs[i]*gs[i+1]));matches:=[];
 for A in atlas4_22 do
  if A.order=Size(H) and A.typ=typ then
   hom:=GroupHomomorphismByImages(A.group,H,A.gens,gs);
   if hom<>fail and IsBijective(hom) then Add(matches,A.label);fi;
  fi;
 od;
 if Length(matches)<>1 then Error("Unique rank-four Atlas identification",matches,typ,Size(H));fi;
 return matches[1];
end;;
f:=[];;
for A in atlas4_22 do
 A.group:=Group(A.gens);;
 if Size(A.group)<>A.order or List([1..3],i->Order(A.gens[i]*A.gens[i+1]))<>A.typ then Error("Atlas order/type");fi;
 if not ForAll(A.words,w->Product(List(w,i->A.gens[i]))=One(A.group)) then Error("Atlas relators");fi;
 ss:=Combinations([1..4]);pars:=List(ss,S->Subgroup(A.group,A.gens{S}));;
 for i in [1..16] do for j in [1..16] do
  if Intersection(pars[i],pars[j])<>pars[Position(ss,Intersection(ss[i],ss[j]))] then Error("Atlas IP");fi;
 od;od;
 F:=FreeGroup(4);f:=GeneratorsOfGroup(F);rel:=List(A.words,w->Product(List(w,i->f[i])));;
 tab:=CosetTableFromGensAndRels(f,rel,[]);;
 if Length(tab[1])<>A.order then Error("Complete Atlas rank-four presentation");fi;
od;
Print("ATLAS rank4_markings=",Length(atlas4_22)," actual_meets=",256*Length(atlas4_22)," complete_presentations=",Length(atlas4_22),"\n");
duals5_22:=List(atlas4_22,A->[A.label,Identify5_22(A.group,Reversed(A.gens))]);;
F:=FreeGroup(5);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);;
for i in [1..5] do for j in [i+1..5] do if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;od;od;
Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,3);iso:=IsomorphismPcGroup(Image(epi));G:=Image(iso);;
r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(epi,x)));K:=LowerCentralSeries(G)[3];pc:=Pcgs(G);;
if not IsElementaryAbelian(K) or not IsSubgroup(Centre(G),K) or Index(G,K)<>512 then Error("Universal first excess");fi;
rev:=GroupHomomorphismByImages(G,G,r,Reversed(r));;
if rev=fail or not IsBijective(rev) then Error("Reversal");fi;
H:=fail;;ss:=Combinations([1..5]);rows5_22:=[];checks22:=0;self22:=0;pi:=fail;s:=[];;
for N in MaximalSubgroups(K) do
 pi:=NaturalHomomorphismByNormalSubgroup(G,N);H:=Image(pi);s:=List(r,x->Image(pi,x));;
 if Size(H)<>1024 then Error("Target order");fi;
 pars:=List(ss,S->Subgroup(H,s{S}));good:=true;
 for i in [1..32] do for j in [1..32] do
  if Intersection(pars[i],pars[j])<>pars[Position(ss,Intersection(ss[i],ss[j]))] then good:=false;fi;
  checks22:=checks22+1;
 od;od;
 if good then
  left:=Identify5_22(Subgroup(H,s{[1..4]}),s{[1..4]});right:=Identify5_22(Subgroup(H,s{[2..5]}),s{[2..5]});
  sd:=Image(rev,N)=N;if sd then self22:=self22+1;fi;
  Add(rows5_22,[List(GeneratorsOfGroup(N),x->ExponentsOfPcElement(pc,x)),List([1..4],i->Order(s[i]*s[i+1])),left,right,sd]);
 fi;
od;
PrintTo("phase22_N009_rank5_facet_matches.json",rows5_22,"\n");
PrintTo("phase22_N009_rank4_atlas_duals.json",duals5_22,"\n");
Print("PASS rank5 candidates=",Length(MaximalSubgroups(K))," actual_meets=",checks22," ordered=",Length(rows5_22)," self_dual=",self22," reversal_classes=",(Length(rows5_22)+self22)/2," uniquely_identified_facets=",2*Length(rows5_22),"\n");
QUIT;
