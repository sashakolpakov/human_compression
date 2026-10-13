t:=[];;matrix:=[];;
Read("/Users/sasha/medusa/research/leemans/corpus106_F006_exceptional_work/F4_model.g");;
t:=List(modelPerms,PermList);;
matrix:=[[1, 3, 2, 2], [3, 1, 4, 2], [2, 4, 1, 3], [2, 2, 3, 1]];;
if Length(t)<>4 or Size(G)<>1152 then Error("order or degree");fi;
if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;
for i in [1..Length(t)] do for j in [1..Length(t)] do
 if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;
od;od;
Print("VERIFIED_COXETER_MODEL F4 ORDER ",Size(G),"\n");
Read("/Users/sasha/medusa/research/leemans/corpus106_F006_exceptional_work/H4_model.g");;
t:=List(modelPerms,PermList);;
matrix:=[[1, 5, 2, 2], [5, 1, 3, 2], [2, 3, 1, 3], [2, 2, 3, 1]];;
if Length(t)<>4 or Size(G)<>14400 then Error("order or degree");fi;
if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;
for i in [1..Length(t)] do for j in [1..Length(t)] do
 if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;
od;od;
Print("VERIFIED_COXETER_MODEL H4 ORDER ",Size(G),"\n");
Read("/Users/sasha/medusa/research/leemans/corpus106_F006_exceptional_work/E6_model.g");;
t:=List(modelPerms,PermList);;
matrix:=[[1, 3, 2, 2, 2, 2], [3, 1, 3, 2, 2, 2], [2, 3, 1, 3, 2, 3], [2, 2, 3, 1, 3, 2], [2, 2, 2, 3, 1, 2], [2, 2, 3, 2, 2, 1]];;
if Length(t)<>6 or Size(G)<>51840 then Error("order or degree");fi;
if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;
for i in [1..Length(t)] do for j in [1..Length(t)] do
 if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;
od;od;
Print("VERIFIED_COXETER_MODEL E6 ORDER ",Size(G),"\n");
Read("/Users/sasha/medusa/research/leemans/corpus106_F006_exceptional_work/E7_model.g");;
t:=List(modelPerms,PermList);;
matrix:=[[1, 3, 2, 2, 2, 2, 2], [3, 1, 3, 2, 2, 2, 2], [2, 3, 1, 3, 2, 2, 3], [2, 2, 3, 1, 3, 2, 2], [2, 2, 2, 3, 1, 3, 2], [2, 2, 2, 2, 3, 1, 2], [2, 2, 3, 2, 2, 2, 1]];;
if Length(t)<>7 or Size(G)<>2903040 then Error("order or degree");fi;
if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;
for i in [1..Length(t)] do for j in [1..Length(t)] do
 if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;
od;od;
Print("VERIFIED_COXETER_MODEL E7 ORDER ",Size(G),"\n");
Read("/Users/sasha/medusa/research/leemans/corpus106_F006_exceptional_work/E8_model.g");;
t:=List(modelPerms,PermList);;
matrix:=[[1, 3, 2, 2, 2, 2, 2, 2], [3, 1, 3, 2, 2, 2, 2, 2], [2, 3, 1, 3, 2, 2, 2, 3], [2, 2, 3, 1, 3, 2, 2, 2], [2, 2, 2, 3, 1, 3, 2, 2], [2, 2, 2, 2, 3, 1, 3, 2], [2, 2, 2, 2, 2, 3, 1, 2], [2, 2, 3, 2, 2, 2, 2, 1]];;
if Length(t)<>8 or Size(G)<>696729600 then Error("order or degree");fi;
if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;
for i in [1..Length(t)] do for j in [1..Length(t)] do
 if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;
od;od;
Print("VERIFIED_COXETER_MODEL E8 ORDER ",Size(G),"\n");
Print("COMPLETE_FIVE_MODEL_IDENTIFICATIONS\n");QUIT;
