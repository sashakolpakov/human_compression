# Exact standalone six-marking verification. Input is the original literal seed.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
Check24:=function(test,msg)
 if not test then Error(msg);fi;
end;;
seedRows24:=EvalString(StringFile("phase24_L088_seed.json"));;
s24:=List(seedRows24,PermList);;
G24:=Group(s24);;
Check24(Size(G24)=175560,"wrong ambient order");;
Check24(G24=UnderlyingGroup(TableOfMarks("J1")),"literal marking is not the retained TomLib J1");;
Check24(ForAll(s24,x->Order(x)=2),"seed generators");;
Check24(List(Combinations([1..4],2),ij->Order(s24[ij[1]]*s24[ij[2]]))=[5,2,2,3,2,5],"seed Coxeter relations");;
Check24((s24[1]*s24[2]*s24[3])^5=One(G24),"seed first extra relation");;
Check24(((s24[4]*s24[3]*s24[2])^5*s24[1])^3=One(G24),"seed second extra relation");;
w24:=(s24[2]*s24[3]*s24[4])^5;;
Check24(Order(w24)=2 and ForAll(s24{[2,3,4]},x->Comm(w24,x)=One(G24)),"central twist");;
marks24:=[s24,
 [s24[1],w24*s24[2],s24[3],s24[4]],
 [s24[1],s24[2],s24[3],s24[3]^s24[4]],
 [s24[2]^s24[1],s24[2],s24[3],s24[4]],
 [s24[2]^s24[1],s24[2],s24[3],s24[3]^s24[4]],
 [(w24*s24[2])^s24[1],w24*s24[2],s24[3],s24[4]]];;

Helly24:=function(K,pars)
 local I,i,j,J,rows,T,common,expected,out;
 I:=[1..Length(pars)];out:=[];
 for i in I do
  rows:=[];
  for j in Difference(I,[i]) do
   T:=Intersection(pars[i],pars[j]);
   rows[j]:=Set(List(RightTransversal(pars[j],T),x->RightCoset(pars[i],x)));
  od;
  for J in Combinations(Difference(I,[i])) do
   if Length(J)<2 then continue;fi;
   common:=Length(Intersection(List(J,j->rows[j])));
   T:=Intersection(pars{J});
   expected:=Index(T,Intersection(T,pars[i]));
   Add(out,[i,J,common,expected]);
  od;
 od;
 return out;
end;;

Verify24:=function(t)
 local ss,subs,meets,a,b,c,ipFailures,hellyRows,J,pars,panelOrders,rcRows,K,gens,rc;
 ss:=Combinations([1..4]);
 subs:=List(ss,J->Group(Concatenation([()],t{J})));
 ipFailures:=[];meets:=0;
 for a in [1..16] do
  for b in [1..16] do
   c:=Position(ss,Intersection(ss[a],ss[b]));
   if Intersection(subs[a],subs[b])<>subs[c] then
    Add(ipFailures,[ss[a],ss[b],Size(Intersection(subs[a],subs[b])),Size(subs[c])]);
   fi;
   meets:=meets+1;
  od;
 od;
 hellyRows:=[];
 for J in ss do
  if Length(J)<3 then continue;fi;
  K:=Group(t{J});
  pars:=List(J,i->Group(t{Difference(J,[i])}));
  Add(hellyRows,[J,Helly24(K,pars)]);
 od;
 pars:=List([1..4],i->Group(t{Difference([1..4],[i])}));
 panelOrders:=List([1..4],i->Size(Intersection(pars{Difference([1..4],[i])})));
 rcRows:=[];
 for J in ss do
  if Length(J)>2 then continue;fi;
  K:=Intersection(Concatenation([G24],pars{J}));
  gens:=Concatenation(List(Difference([1..4],J),i->GeneratorsOfGroup(Intersection(K,pars[i]))));
  rc:=Group(Concatenation([()],gens))=K;
  Add(rcRows,[J,Size(K),rc]);
 od;
 return rec(group_order:=Size(Group(t)),pair_orders:=List(Combinations([1..4],2),ij->Order(t[ij[1]]*t[ij[2]])),
 subset_orders:=List(subs,Size),parabolic_orders:=List(pars,Size),parabolic_types:=List(pars,StructureDescription),
 borel_order:=Size(Intersection(pars)),panel_orders:=panelOrders,
 meets_checked:=meets,ip_failures:=ipFailures,helly_rows:=hellyRows,residue_generation:=rcRows);
end;;

results24:=[];;
expectedPars24:=[[120,20,20,60],[120,20,20,660],[120,20,60,60],
 [120,120,20,60],[120,120,60,60],[120,120,20,660]];;
for i24 in [1..6] do
 Check24(ForAll(marks24[i24],x->Order(x)=2),"transformed generators");;
 r24:=Verify24(marks24[i24]);;
 Check24(r24.group_order=175560 and Length(r24.ip_failures)=0,"generation or IP failure");;
 Check24(r24.borel_order=1 and r24.panel_orders=[2,2,2,2],"thinness");;
 Check24(r24.parabolic_orders=expectedPars24[i24],"source-defined parabolic orders");;
 Check24(ForAll(r24.helly_rows,r->ForAll(r[2],x->x[3]=x[4])),"Helly failure");;
 Check24(ForAll(r24.residue_generation,r->r[3]),"residual connectivity");;
 Add(results24,r24);;
 Print("GEOMETRY ",i24," PAIRS ",r24.pair_orders," PARABOLICS ",r24.parabolic_orders," TYPES ",r24.parabolic_types," IP ",r24.meets_checked," HELLY ",Sum(r24.helly_rows,r->Length(r[2]))," PASS\n");
od;
Check24(Length(Set(List(results24,r->SortedList(r.parabolic_orders))))=6,"geometries must be pairwise distinct");;
left24:=Intersection(Group(s24{[2,3,4]}),Group(s24{[2,3,4]})^s24[1]);;
right24:=Intersection(Group(s24{[1,2,3]}),Group(s24{[1,2,3]})^s24[4]);;
Check24(left24=Group(s24{[3,4]}) and right24=Group(s24{[1,2]}),"doubling criterion");;
bad24:=[Verify24([s24[1],w24*s24[2],s24[3],s24[3]^s24[4]]),
        Verify24([s24[1],s24[2],s24[3],w24*s24[4]])];;
for i24 in [1..2] do
 Check24(bad24[i24].group_order=175560 and bad24[i24].borel_order=1 and Length(bad24[i24].ip_failures)=8,"negative example IP scope");;
 Check24(ForAll(bad24[i24].helly_rows,r->ForAll(r[2],x->x[3]=x[4])),"negative examples retain Helly");;
 Check24(bad24[i24].panel_orders=[[2,4,2,2],[2,2,2,4]][i24],"negative example panel witness");;
 Print("NEGATIVE ",i24," ORDER ",bad24[i24].group_order," PAIRS ",bad24[i24].pair_orders," IP_FAILURES ",Length(bad24[i24].ip_failures)," HELLY_FAILURES ",Sum(bad24[i24].helly_rows,r->Number(r[2],x->x[3]<>x[4]))," PANEL_ORDERS ",bad24[i24].panel_orders,"\n");
od;
PrintTo("phase24_L088_results.g","L088Results:=",results24,";\nL088Negative:=",bad24,";\n");;
jsonRow24:=function(r)
 return [r.group_order,r.pair_orders,r.subset_orders,r.parabolic_orders,r.parabolic_types,
 r.borel_order,r.panel_orders,r.meets_checked,r.ip_failures,r.helly_rows,r.residue_generation];
end;;
PrintTo("phase24_L088_results.json",[List(results24,jsonRow24),List(bad24,jsonRow24),[Size(left24),Size(right24)]],"\n");;
Print("L088_ALL_SIX_PASS\n");
QUIT;
