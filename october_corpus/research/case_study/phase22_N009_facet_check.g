# Marked facet identification against primary Atlas permutation data.
# No SmallGroup calls and no source count/label filters in the original census.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([240,40]);;
Read("phase22_N009_atlas_library.g");;
Read("phase22_N009_facet_input.g");;
Identify22:=function(H,gs)
 local typ,matches,A,hom;
 typ:=List([1..Length(gs)-1],i->Order(gs[i]*gs[i+1]));matches:=[];
 for A in atlas22 do
  if A.order=Size(H) and A.typ=typ then
   hom:=GroupHomomorphismByImages(A.group,H,A.gens,gs);
   if hom<>fail and IsBijective(hom) then Add(matches,A.label);fi;
  fi;
 od;
 if Length(matches)<>1 then Error("Not a unique marked Atlas identification: ",matches," type ",typ," order ",Size(H));fi;
 return matches[1];
end;;
for A in atlas22 do
 A.group:=Group(A.gens);;
 if Size(A.group)<>A.order then Error("Atlas order");fi;
 if List([1,2],i->Order(A.gens[i]*A.gens[i+1]))<>A.typ then Error("Atlas type");fi;
 if not ForAll(A.words,w->Product(List(w,i->A.gens[i]))=One(A.group)) then Error("Atlas relator transcription");fi;
 ss:=Combinations([1..3]);pars:=List(ss,S->Subgroup(A.group,A.gens{S}));;
 for i in [1..8] do for j in [1..8] do
  if Intersection(pars[i],pars[j])<>pars[Position(ss,Intersection(ss[i],ss[j]))] then Error("Atlas actual IP");fi;
 od;od;
od;
duals22:=List(atlas22,A->[A.label,Identify22(A.group,Reversed(A.gens))]);;
Print("ATLAS_MARKINGS ",Length(atlas22)," actual_meets ",64*Length(atlas22),"\n");
Print("DUALS ",duals22,"\n");
F:=FreeGroup(4);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);;
for i in [1..4] do for j in [i+1..4] do if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;od;od;
Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,5);iso:=IsomorphismPcGroup(Image(epi));G:=Image(iso);;
r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(epi,x)));pc:=Pcgs(G);;
if not ForAll(RelativeOrders(pc),n->n=2) then Error("Binary coordinates");fi;
Decode22:=function(n) local exp,i;exp:=[];for i in [1..Length(pc)] do Add(exp,n mod 2);n:=QuoInt(n,2);od;if n<>0 then Error("Coordinate overflow");fi;return PcElementByExponents(pc,exp);end;;
facets22:=[];;at:=0;;pi:=fail;;s:=[];;
for rec22 in accepted22 do
 N:=Subgroup(G,List(rec22[1],Decode22));;
 if not IsNormal(G,N) or Index(G,N)<>1024 then Error("Census kernel reconstruction");fi;
 pi:=NaturalHomomorphismByNormalSubgroup(G,N);H:=Image(pi);s:=List(r,x->Image(pi,x));;
 left:=Identify22(Subgroup(H,s{[1..3]}),s{[1..3]});right:=Identify22(Subgroup(H,s{[2..4]}),s{[2..4]});
 Add(facets22,[rec22[1],rec22[2],left,right,rec22[5]]);at:=at+1;
od;
PrintTo("phase22_N009_facet_matches.json",facets22,"\n");
PrintTo("phase22_N009_atlas_duals.json",duals22,"\n");
Print("PASS all ",at," ordered rank-four markings: ",2*at," exact generator-preserving facet isomorphisms; every facet uniquely identified.\n");
QUIT;
