# Source-bound raw finite presentations, N009 Tables 2--4 and Examples 3.9/4.3--4.5.
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
Read("phase24_N009_atlas_library.g");;
for i in [1..5] do
 A:=atlas24[i];B:=rec(group:=Group(A.gens),mark:=A.gens);
 if i=1 then target:=q44;else target:=base24[i-1];fi;
 if not Same24(target,B) then Error("Primary Atlas base label",A.label);fi;
 if not ForAll(A.words,w->Product(List(w,j->A.gens[j]))=One(B.group)) then Error("Primary Atlas defining word",A.label);fi;
od;
Print("PASS five exact primary Atlas order-512 marked labels\n");
# Exact facet identities for Examples4.3/4.4/4.5 and the two smooth quotients.
Read("phase22_N009_atlas_library.g");;
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
if LoadPackage("nq")=fail then Error("NQ required for frozen census adapter");fi;
Print("SOFTWARE GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
accepted24:=EvalString(StringFile("phase22_N009_rank3.accepted.json"));;
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
Print("PASS all eight type-{4,8} classes matched to frozen unfiltered census\n");
PrintTo("phase24_N009_example_facets.json",exampleFacets24,"\n");
PrintTo("phase24_N009_census_matches.json",censusMatches24,"\n");
PrintTo("phase24_N009_examples_results.json",report24,"\n");
PrintTo("phase24_N009_table3_matches.json",table3matches24,"\n");
PrintTo("phase24_N009_table4_literal_matches.json",literal24,"\n");
Print("PASS raw_presentations=",tc24," exact_IP_meets=",meet24,"; eight distinct Table3/Example3.9 target markings; all twelve Table3 assignments; Table4 literal e->c,f->a,h->c; three exhaustive Example4.5 central involutions.\n");
QUIT;
