# Source-bound raw presentations, all N009 finite table labels and universal orders.
# All orders below come from COMPLETE Todd--Coxeter coset tables, not NQ bounds.
SizeScreen([240,40]);;
report24:=[];;meet24:=0;;tc24:=0;;
Cox24:=function(f,typ)
 local n,rels,i,j;n:=Length(typ)+1;rels:=List(f{[1..n]},x->x^2);
 for i in [1..n] do for j in [i+1..n] do
  if j=i+1 then Add(rels,(f[i]*f[j])^typ[i]);else Add(rels,Comm(f[i],f[j]));fi;
 od;od;return rels;
end;;
TableWords24:=function(f)
 local a,b,c;a:=f[1];b:=f[2];c:=f[3];
 return [[(a*b*c*b)^4,(c*a*(b*c)^3*a*b)^2],
 [(c*a*b)^8,(a*(b*c)^3*b)^2],
 [(c*(a*b*c*b)^2)^2,(c*a*(b*c)^3*a*b)^2],
 [(a*(b*c)^3*b)^2,(c*a*b)^5*c*(b*a)^2*(c*b)^2*a*b]];
end;;
Build24:=function(name,F,rels,rank)
 local fg,table,n,gs,G,mark,sets,pars,i,j,typ;
 fg:=GeneratorsOfGroup(F);table:=CosetTableFromGensAndRels(fg,rels,[]);n:=Length(table[1]);
 gs:=List([1..Length(fg)],i->PermList(table[2*i-1]));G:=Group(gs);mark:=gs{[1..rank]};
 if Size(G)<>n or Subgroup(G,mark)<>G then Error("Complete regular coset action/order/generation",name);fi;
 if not ForAll(rels,w->MappedWord(w,fg,gs)=One(G)) then Error("Raw relators",name);fi;
 sets:=Combinations([1..rank]);pars:=List(sets,S->Subgroup(G,mark{S}));
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  if Intersection(pars[i],pars[j])<>pars[Position(sets,Intersection(sets[i],sets[j]))] then Error("Actual IP",name);fi;
  meet24:=meet24+1;
 od;od;
 typ:=List([1..rank-1],i->Order(mark[i]*mark[i+1]));
 Add(report24,[name,n,typ]);tc24:=tc24+1;
 Print("PRESENTATION ",name," order=",n," type=",typ," IP=PASS\n");
 return rec(name:=name,group:=G,mark:=mark,allgens:=gs,order:=n,F:=F,rels:=rels);
end;;
Same24:=function(A,B)
 local h;h:=GroupHomomorphismByImages(A.group,B.group,A.mark,B.mark);return h<>fail and IsBijective(h);
end;;

f:=[];;model:=fail;;pair78:=[];;
Read("phase78_n009_integration_data.g");;
for A in atlas78 do
 A.words:=List(A.words,w->List(w,c->Int([c])));
 F:=FreeGroup(Length(A.typ)+1);f:=GeneratorsOfGroup(F);
 rel:=List(A.words,w->Product(List(w,i->f[i])));
 model:=Build24(Concatenation("Atlas_",A.label),F,rel,Length(f));
 if model.order<>A.order or List([1..Length(A.typ)],i->Order(model.mark[i]*model.mark[i+1]))<>A.typ then Error("Complete Atlas order/type",A.label);fi;
 A.group:=model.group;A.gens:=model.mark;
od;
atlas22:=Filtered(atlas78,A->Length(A.typ)=2 and A.order<512);;
atlas4_22:=Filtered(atlas78,A->Length(A.typ)=3);;
atlas24:=Filtered(atlas78,A->Length(A.typ)=2 and A.order=512);;
if [Length(atlas22),Length(atlas4_22),Length(atlas24)]<>[56,11,5] then Error("Library partition");fi;
Identify78:=function(H,gs,library)
 local typ,matches,A,hom;
 typ:=List([1..Length(gs)-1],i->Order(gs[i]*gs[i+1]));matches:=[];
 for A in library do
  if A.order=Size(H) and A.typ=typ then
   hom:=GroupHomomorphismByImages(A.group,H,A.gens,gs);
   if hom<>fail and IsBijective(hom) then Add(matches,A.label);fi;
  fi;
 od;
 if Length(matches)<>1 then Error("Unique ordered marked label",matches,typ,Size(H));fi;
 return matches[1];
end;;
duals78:=List(Concatenation(atlas22,atlas4_22),A->[A.label,Identify78(A.group,Reversed(A.gens),Concatenation(atlas22,atlas4_22))]);;
Dual78:=function(label) return First(duals78,x->x[1]=label)[2];end;;
Canon78:=function(pair) return Minimum(pair,[Dual78(pair[2]),Dual78(pair[1])]);end;;
F:=FreeGroup(3);f:=GeneratorsOfGroup(F);words:=TableWords24(f);;
base24:=List([1..4],i->Build24(Concatenation("Table2_512",[CharInt(96+i)]),F,Concatenation(Cox24(f,[4,8]),words[i]),3));;
if not ForAll(base24,A->A.order=512) then Error("Table2 orders");fi;
for i in [1..4] do for j in [i+1..4] do if Same24(base24[i],base24[j]) then Error("Distinct Table2 markings");fi;od;od;
low24:=Build24("Example3.9_classI_base",F,Cox24(f,[2,8]),3);;
if low24.order<>32 then Error("ClassI boundary");fi;
q44:=Build24("Example3.9_classII_base",F,Concatenation(Cox24(f,[4,4]),[(f[1]*f[2]*f[3]*f[2])^8]),3);;
if q44.order<>512 then Error("ClassII base");fi;
F4:=FreeGroup(4);f4:=GeneratorsOfGroup(F4);t:=f4[4];a:=f4[1];b:=f4[2];c:=f4[3];;
central24:=Concatenation([t^2],List(f4{[1..3]},x->Comm(t,x)));;
classII24:=[];;
for eps in [0,1] do
 A:=Build24(Concatenation("Example3.9_classII_",String(eps)),F4,Concatenation(Cox24(f4,[4,8]),central24,[t^-1*(b*c)^4,(a*b*c*b)^8*t^-eps]),3);;
 if A.order<>1024 or Order(A.allgens[4])<>2 then Error("ClassII lift");fi;Add(classII24,A);
od;
words4:=TableWords24(f4);patterns24:=[[1,0],[0,1],[1,1]];lifts24:=[];;pi:=fail;;
for i in [1..4] do
 row:=[];
 for eps in patterns24 do
  A:=Build24(Concatenation("Table3_",String(i),"_",String(eps)),F4,Concatenation(Cox24(f4,[4,8]),central24,[words4[i][1]*t^-eps[1],words4[i][2]*t^-eps[2]]),3);;
  Add(row,A);
  N:=Subgroup(A.group,[A.allgens[4]]);pi:=NaturalHomomorphismByNormalSubgroup(A.group,N);Q:=Image(pi);;
  qm:=List(A.mark,x->Image(pi,x));h:=GroupHomomorphismByImages(base24[i].group,Q,base24[i].mark,qm);;
  if h=fail or not IsBijective(h) then Error("Lift quotient is exact Table2 marking");fi;
 od;Add(lifts24,row);
od;
# Names a,b from Example3.9 ClassII; c,d,e,f,g,h from the explicit Table3 assignments.
refs24:=[classII24[1],classII24[2],lifts24[1][1],lifts24[1][2],lifts24[1][3],lifts24[2][3],lifts24[3][2],lifts24[3][3]];;
if not ForAll(refs24,A->A.order=1024) then Error("Eight target orders");fi;
for i in [1..8] do for j in [i+1..8] do if Same24(refs24[i],refs24[j]) then Error("Eight targets not distinct",i,j);fi;od;od;
expected24:=[[3,4,5],[1,3,6],[3,7,8],[9,1,9]];;table3matches24:=[];;
for i in [1..4] do for j in [1..3] do
 k:=expected24[i][j];if k=9 then B:=base24[4];else B:=refs24[k];fi;
 if not Same24(lifts24[i][j],B) then Error("Exact Table3 assignment",i,j,k);fi;
 Add(table3matches24,[i,patterns24[j],k,lifts24[i][j].order,Order(lifts24[i][j].allgens[4])]);
od;od;
# Literal Table4, preserving each printed e (identity) even when Table3 disagrees.
literal24:=[];;
for i in [1..8] do
 if i<=2 then rel:=Concatenation(Cox24(f4,[4,8]),central24,[t^-1*(b*c)^4,(a*b*c*b)^8*t^-(i-1)]);
 elif i in [3,5] then rel:=Concatenation(Cox24(f4,[4,8]),central24,[words4[1][1]*t^-1,words4[1][2]]);
 elif i=4 then rel:=Concatenation(Cox24(f4,[4,8]),central24,[words4[1][1],words4[1][2]*t^-1]);
 elif i=6 then rel:=Concatenation(Cox24(f4,[4,8]),central24,[words4[2][1]*t^-1,words4[2][2]]);
 elif i=7 then rel:=Concatenation(Cox24(f4,[4,8]),central24,[words4[3][1],words4[3][2]*t^-1]);
 else rel:=Concatenation(Cox24(f4,[4,8]),central24,[words4[3][1]*t^-1,words4[3][2]]);fi;
 A:=Build24(Concatenation("Table4_literal_",String(i)),F4,rel,3);;
 matches:=Filtered([1..8],j->Same24(A,refs24[j]));if Length(matches)<>1 then Error("Literal Table4 identification");fi;
 Add(literal24,[i,matches[1]]);
od;
if literal24<>[[1,1],[2,2],[3,3],[4,4],[5,3],[6,1],[7,7],[8,3]] then Error("Unexpected literal Table4 mapping",literal24);fi;
Print("TABLE3_MATCHES ",table3matches24,"\n");Print("TABLE4_LITERAL_MATCHES ",literal24,"\n");
# Examples4.3--4.5, using exactly their printed raw relators.
a:=f4[1];b:=f4[2];c:=f4[3];d:=f4[4];;
ex43:=Build24("Example4.3",F4,Concatenation(Cox24(f4,[4,4,4]),[(a*b*c*b)^2,(b*c*d*c)^4]),4);;
ex44:=Build24("Example4.4",F4,Concatenation(Cox24(f4,[4,4,4]),[(a*b*c*b)^2,(d*b*c)^8]),4);;
ex45rel:=Concatenation(Cox24(f4,[4,4,8]),[(c*a*b)^4,d*b*c*d*(c*b)^2*(d*c)^2*b*c]);;
ex45:=Build24("Example4.5_universal",F4,ex45rel,4);;
if [ex43.order,ex44.order,ex45.order]<>[512,1024,2048] then Error("Example raw orders");fi;
tauwords24:=[b*c*d*c*b*a*b*(d*c)^2*d*b*a,(b*c*d*c*b*a)^2,(c*d)^4];;
tauimages24:=List(tauwords24,w->MappedWord(w,f4,ex45.mark));;
zinv24:=Filtered(Elements(Centre(ex45.group)),z->Order(z)=2);;
if Set(tauimages24)<>Set(zinv24) or Length(zinv24)<>3 then Error("Complete central involution list");fi;
ex45quot24:=[];;
for i in [1..3] do
 A:=Build24(Concatenation("Example4.5_quotient",String(i)),F4,Concatenation(ex45rel,[tauwords24[i]]),4);;
 if A.order<>1024 then Error("Quotient raw order");fi;Add(ex45quot24,A);
od;
if List(ex45quot24,A->List([1..3],i->Order(A.mark[i]*A.mark[i+1])))<>[[4,4,8],[4,4,8],[4,4,4]] then Error("Quotient smoothness");fi;
if Same24(ex45quot24[1],ex45quot24[2]) then Error("Distinct smooth quotients");fi;
# Primary Atlas identities for the five source order-512 names.

for i in [1..5] do
 A:=atlas24[i];B:=rec(group:=Group(A.gens),mark:=A.gens);
 if i=1 then target:=q44;else target:=base24[i-1];fi;
 if not Same24(target,B) then Error("Primary Atlas base label",A.label);fi;
 if not ForAll(A.words,w->Product(List(w,j->A.gens[j]))=One(B.group)) then Error("Primary Atlas defining word",A.label);fi;
od;
Print("PASS five exact primary Atlas order-512 marked labels\n");
# Exact facet identities for Examples4.3/4.4/4.5 and the two smooth quotients.

exampleFacets24:=[];;
for entry in [[ex43,["{4,4}*32","{4,4}*128"]],[ex44,["{4,4}*32","{4,4}*256"]],[ex45,["{4,4}*64","{4,8}*128a"]],[ex45quot24[1],["{4,4}*64","{4,8}*128a"]],[ex45quot24[2],["{4,4}*64","{4,8}*128a"]]] do
 A:=entry[1];
 for j in [1,2] do
  ar:=First(atlas22,x->x.label=entry[2][j]);B:=rec(group:=Group(ar.gens),mark:=ar.gens);
  mark:=A.mark{[j..j+2]};target:=rec(group:=Subgroup(A.group,mark),mark:=mark);
  if not Same24(target,B) then Error("Example facet label",A.name,entry[2][j]);fi;
 od;
 Add(exampleFacets24,[A.name,entry[2]]);
od;
Print("PASS ten exact primary Atlas example facet labels\n");
# Match the eight printed/Table3 target names to the independent unfiltered census.
if LoadPackage("nq")=fail then Error("NQ required for unfiltered census adapter");fi;
Print("SOFTWARE GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
accepted24:=EvalString(StringFile("phase78_d3_k5.accepted.json"));;
F3:=FreeGroup(3);v:=GeneratorsOfGroup(F3);P:=F3/Concatenation(List(v,x->x^2),[Comm(v[1],v[3])]);;
ep:=NqEpimorphismNilpotentQuotient(P,7);is:=IsomorphismPcGroup(Image(ep));U:=Image(is);;
rr:=List(GeneratorsOfGroup(P),x->Image(is,Image(ep,x)));pc24:=Pcgs(U);;
if not ForAll(RelativeOrders(pc24),x->x=2) then Error("Frozen binary pc coordinates");fi;
Decode24:=function(n) local e,i;e:=[];for i in [1..Length(pc24)] do Add(e,n mod 2);n:=QuoInt(n,2);od;if n<>0 then Error("Coordinate overflow");fi;return PcElementByExponents(pc24,e);end;;
censusMatches24:=[];;
for entry in Filtered(accepted24,x->x[2]=[4,8]) do
 N:=Subgroup(U,List(entry[1],Decode24));
 if not IsNormal(U,N) or Index(U,N)<>1024 then Error("Frozen census reconstruction");fi;
 pi:=NaturalHomomorphismByNormalSubgroup(U,N);mark:=List(rr,x->Image(pi,x));target:=rec(group:=Image(pi),mark:=mark);
 matches:=Filtered([1..8],j->Same24(refs24[j],target));
 if Length(matches)<>1 then Error("Exact census match",matches);fi;
 Add(censusMatches24,[entry[1],matches[1]]);
od;
if Set(List(censusMatches24,x->x[2]))<>[1..8] or Length(censusMatches24)<>8 then Error("All eight census targets");fi;
Print("PASS all eight type-{4,8} classes matched to new unfiltered census\n");
PrintTo("phase78_n009_integration_example_facets.json",exampleFacets24,"\n");
PrintTo("phase78_n009_integration_census_matches.json",censusMatches24,"\n");
PrintTo("phase78_n009_integration_examples_results.json",report24,"\n");
PrintTo("phase78_n009_integration_table3_matches.json",table3matches24,"\n");
PrintTo("phase78_n009_integration_table4_literal_matches.json",literal24,"\n");

# Reconstruct both higher-rank catalogues from the new complete kernel census.
facetRows78:=[];;tableResults78:=[];;universal78:=[];;exceptionTargets78:=[];;
for d78 in [4,5] do
 excess78:=11-2*d78;
 accepted78:=EvalString(StringFile(Concatenation("phase78_d",String(d78),"_k",String(excess78),".accepted.json")));
 F:=FreeGroup(d78);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);
 for i in [1..d78] do for j in [i+1..d78] do if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;od;od;
 P:=F/rel;ep:=NqEpimorphismNilpotentQuotient(P,excess78+2);is:=IsomorphismPcGroup(Image(ep));U:=Image(is);
 rr:=List(GeneratorsOfGroup(P),x->Image(is,Image(ep,x)));pc24:=Pcgs(U);
 if not ForAll(RelativeOrders(pc24),x->x=2) then Error("Binary census coordinates");fi;
 if d78=4 then library78:=atlas22;else library78:=atlas4_22;fi;
 for entry in accepted78 do
  N:=Subgroup(U,List(entry[1],Decode24));
  if not IsNormal(U,N) or Index(U,N)<>1024 then Error("Census reconstruction");fi;
  pi:=NaturalHomomorphismByNormalSubgroup(U,N);H:=Image(pi);mark:=List(rr,x->Image(pi,x));
  labels78:=[Identify78(Subgroup(H,mark{[1..d78-1]}),mark{[1..d78-1]},library78),Identify78(Subgroup(H,mark{[2..d78]}),mark{[2..d78]},library78)];
  Add(facetRows78,[entry[1],entry[2],labels78,entry[5]]);
  if labels78=["{4,4}*128","{4,4}*64"] then Add(exceptionTargets78,rec(group:=H,mark:=mark));fi;
 od;
od;
if Length(facetRows78)<>214 or Length(exceptionTargets78)<>2 then Error("Facet/exceptions cardinality");fi;
if Length(Set(List(rows78,r->Canon78(r[1]))))<>107 then Error("Distinct Table6 pairs");fi;
for row78 in rows78 do
 pair78:=Canon78(row78[1]);hits78:=Filtered(facetRows78,r->Canon78(r[3])=pair78);
 fixed78:=Number(hits78,r->r[4]);actual78:=(Length(hits78)+fixed78)/2;
 if actual78<>row78[3] then Error("Exact Table6 count",row78,actual78);fi;
 if not ForAll(hits78,r->Minimum(r[2],Reversed(r[2]))=Minimum(row78[4],Reversed(row78[4]))) then Error("Table6 type");fi;
 Add(tableResults78,[row78[1],Length(hits78),fixed78,actual78]);
 if row78[2]<>0 then
  A:=First(atlas78,x->x.label=row78[1][1]);B:=First(atlas78,x->x.label=row78[1][2]);
  F:=FreeGroup(Length(A.typ)+2);f:=GeneratorsOfGroup(F);
  rel:=Concatenation(List(A.words,w->Product(List(w,i->f[i]))),List(B.words,w->Product(List(w,i->f[i+1]))),[Comm(f[1],f[Length(f)])]);
  model:=Build24(Concatenation("Universal_",A.label,"_",B.label),F,rel,Length(f));
  if model.order<>row78[2] then Error("Complete universal order",row78);fi;
  if [Identify78(Subgroup(model.group,model.mark{[1..Length(f)-1]}),model.mark{[1..Length(f)-1]},atlas78),Identify78(Subgroup(model.group,model.mark{[2..Length(f)]}),model.mark{[2..Length(f)]},atlas78)]<>row78[1] then Error("Universal exact facet identities");fi;
  Add(universal78,[row78[1],model.order]);
 fi;
od;
# Exact source Theorem5.5 raw presentations; match both independently found markings.
F:=FreeGroup(4);f:=GeneratorsOfGroup(F);a:=f[1];b:=f[2];c:=f[3];d:=f[4];
common78:=Concatenation(Cox24(f,[4,4,4]),[(a*b*c*b)^4,(b*c*d)^4]);;
extras78:=[[(d*c*b*a*b*d*c)^2],[(b*d*c*d*b*a)^2*(c*b*a*b)^2,(a*b*c*b)^2*(b*a*b*d*c*d)^2]];;
exceptionMatches78:=[];;
for i in [1,2] do
 model:=Build24(Concatenation("Theorem5.5_",String(i)),F,Concatenation(common78,extras78[i]),4);
 if model.order<>1024 then Error("Exceptional raw order");fi;
 matches78:=Filtered([1,2],j->Same24(model,exceptionTargets78[j]));
 if Length(matches78)<>1 then Error("Exceptional marked isomorphism");fi;
 Add(exceptionMatches78,matches78[1]);
od;
if Set(exceptionMatches78)<>[1,2] then Error("Exceptional completeness");fi;
if Length(universal78)<>106 or Collected(List(universal78,x->x[2]))<>[[1024,101],[2048,5]] then Error("All finite universals");fi;
# Table5 counts, from the full rank3 census, only after generation is complete.
expected578:=[[[4,4],1],[[4,8],8],[[4,16],14],[[4,32],4],[[4,64],2],[[4,128],2],[[8,8],22],[[8,16],40],[[8,32],8],[[8,64],4],[[16,16],10],[[16,32],10]];;
for row78 in expected578 do
 hits78:=Filtered(accepted24,r->Minimum(r[2],Reversed(r[2]))=row78[1]);
 if (Length(hits78)+Number(hits78,r->r[5]))/2<>row78[2] then Error("Table5 count");fi;
od;
PrintTo("phase78_n009_integration_facet_matches.json",facetRows78,"\n");
PrintTo("phase78_n009_integration_duals.json",duals78,"\n");
PrintTo("phase78_n009_integration_table6_results.json",tableResults78,"\n");
PrintTo("phase78_n009_integration_universal_orders.json",universal78,"\n");
PrintTo("phase78_n009_integration_all_presentations.json",report24,"\n");
Print("PASS complete_presentations=",tc24," actual_IP_meets=",meet24," atlas=72 raw_examples=34 exceptional=2 finite_universals=106 exact_census_facets=428 table6_rows=107 table5_rows=12\n");
QUIT;
