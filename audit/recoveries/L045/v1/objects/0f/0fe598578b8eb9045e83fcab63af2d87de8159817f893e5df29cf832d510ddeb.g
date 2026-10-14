# A bounded candidate search; only saved, subsequently verified pairs can
# contribute mathematical evidence. A failed or capped search proves nothing.
SizeScreen([240,40]);;
Reset(GlobalMersenneTwister,452026+CaseNumber);;
HC_G:=CallFuncList(SimpleGroup,Parameters);;
Print("CONSTRUCTED ",Parameters," order ",Size(HC_G)," degree ",LargestMovedPoint(HC_G),"\n");
HC_Found:=false;;
for HC_Trial in [1..300] do
    HC_Z:=Random(HC_G);;HC_ZOrder:=Order(HC_Z);;
    if IsOddInt(HC_ZOrder) then continue;fi;
    HC_T:=HC_Z^(HC_ZOrder/2);;HC_X:=Random(HC_G);;
    HC_W:=HC_X*HC_T*HC_X^2*HC_T*HC_X^3*HC_T;;
    HC_V:=HC_X^-1*HC_T*HC_X^-2*HC_T*HC_X^-3*HC_T;;
    HC_Orders:=[Order(HC_X),Order(HC_X^-1*HC_T),Order(HC_W),Order(HC_V)];;
    if HC_Orders[3]=HC_Orders[4] then continue;fi;
    HC_H:=Group(HC_X,HC_T);;
    if Size(HC_H)<>Size(HC_G) then continue;fi;
    if Order(HC_T)<>2 or Minimum(HC_Orders{[1,2]})<=2 then Error("invalid saved pair");fi;
    HC_Record:=rec(parameters:=Parameters,ambient_generators:=GeneratorsOfGroup(HC_G),
                   x:=HC_X,t:=HC_T,orders:=HC_Orders,group_order:=Size(HC_G),
                   degree:=LargestMovedPoint(HC_G),trial:=HC_Trial);;
    PrintTo(WitnessPath,"HC_SavedPair:=",HC_Record,";;\n");
    Print("FOUND ",Parameters," ",HC_Orders," trial ",HC_Trial,"\n");
    HC_Found:=true;;break;
od;
if HC_Found then Print("TERMINAL_CANDIDATE_FOUND\n");
else Print("TERMINAL_BOUNDED_SEARCH_NO_CANDIDATE\n");fi;
QUIT;
