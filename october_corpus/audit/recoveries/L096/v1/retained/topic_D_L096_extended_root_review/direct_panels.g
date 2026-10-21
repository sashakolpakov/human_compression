Read("data_m12/inputs.g");;
G:=fail;;
RootFailures:=[];;RootPanels:=0;;
for row in L096Inputs do
 G:=Group(Concatenation(row.parabolic_generators));;
 H:=List(row.parabolic_generators,x->Subgroup(G,x));;
 B:=Intersection(H);;n:=Length(H);;
 for i in [1..n] do
  R:=Intersection(H{Difference([1..n],[i])});;
  cosets:=RightCosets(R,B);;
  lengths:=SortedList(List(Orbits(B,cosets,OnRight),Length));;
  RootPanels:=RootPanels+1;
  if Length(cosets)<2 or Length(lengths)<>2 then
   Add(RootFailures,[row.member,row.active,row.construction,i,Length(cosets),lengths]);
  fi;
 od;
od;
Print("PANELS|",RootPanels,"\nFAILURES|",RootFailures,"\n");
if Set(List(RootFailures,r->[r[1],r[2]]))<>[["m12.rk3",15],["m12.rk3",17],["m12.rk3",20],["m12.rk4",4],["m12.rk4",7]] then Error("unexpected exact panel obstructions");fi;
Print("PASS_ROOT_DISTINCT_LITERAL_COSET_PANEL_CHECK\n");QUIT;
