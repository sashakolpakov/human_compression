# ExpectedParameters, ExpectedOrder, ExpectedOrders, ExpectedDegree, CaseNumber,
# PairPath, OutputPath and Control are set by the exact Python driver.
SizeScreen([1000000,40]);;
Need:=function(b,message)
  if not b then Print("REJECT ",message,"\n");FORCE_QUIT_GAP(1);fi;
end;;
Need(GAPInfo.Version="4.15.1","exact recorded GAP version");
Reset(GlobalMersenneTwister,452026+CaseNumber);;
Read(PairPath);;
if Control="parameters" then HC_SavedPair.parameters:=["L",4,2];fi;
Need(HC_SavedPair.parameters=ExpectedParameters,"exact source parameters");
G:=CallFuncList(SimpleGroup,ExpectedParameters);;
if Control="ambient" then HC_SavedPair.ambient_generators[1]:=();fi;
Need(GeneratorsOfGroup(G)=HC_SavedPair.ambient_generators,"literal named constructor generators");
H:=Group(HC_SavedPair.ambient_generators);;
Need(not HasSize(H),"fresh saved group has no supplied size");
Need(H=G,"actual saved and named group equality");
Need(Size(H)=ExpectedOrder and HC_SavedPair.group_order=ExpectedOrder,"actual ambient order");
Need(LargestMovedPoint(H)=ExpectedDegree and HC_SavedPair.degree=ExpectedDegree,"literal degree");
x:=HC_SavedPair.x;;t:=HC_SavedPair.t;;
if Control="identity" then t:=();fi;
if Control="outside" then x:=x*(ExpectedDegree+1,ExpectedDegree+2);fi;
if Control="generation" then x:=t;fi;
Need(Order(t)=2,"nonidentity involution");
Need(x in H and t in H,"actual pair membership");
K:=Group(x,t);;
Need(not HasSize(K),"fresh pair group has no supplied size");
Need(Size(K)=Size(H),"full pair generation");
Need(K=H,"actual generated subgroup equality");
u:=x*t*x^2*t*x^3*t;;v:=x^-1*t*x^-2*t*x^-3*t;;
orders:=[Order(x),Order(x^-1*t),Order(u),Order(v)];;
if Control="orders" then orders[1]:=orders[1]+1;fi;
if Control="equal_words" then orders[4]:=orders[3];fi;
Need(orders=ExpectedOrders and orders=HC_SavedPair.orders,"exact four orders");
Need(orders[1]>2 and orders[2]>2 and orders[3]<>orders[4],"word criterion");
PrintTo(OutputPath,"{\"parameters\":",ExpectedParameters,",\"degree\":",ExpectedDegree,
 ",\"group_order\":",Size(H),",\"orders\":",orders,
 ",\"literal_constructor_generators\":true,\"actual_membership\":true,\"full_generation\":true}\n");
Print("TERMINAL_PASS finite Lie certificate\n");
QUIT;
