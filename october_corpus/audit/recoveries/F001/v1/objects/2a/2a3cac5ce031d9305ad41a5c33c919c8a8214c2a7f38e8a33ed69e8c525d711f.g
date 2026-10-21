Read("checks.g");;
F:=GF(7);;one:=One(F);;
marks:=[[[0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], [[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1]], [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0]], [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [6, 6, 6, 6, 6]], [[2, 1, 1, 1, 1], [1, 2, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 2, 1], [1, 1, 1, 1, 2]]]*one;;
B:=[[2, 1, 1, 1, 1], [1, 2, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 2, 1], [1, 1, 1, 1, 2]]*one;;
G:=Group(marks);;
if Size(G)<>5040 then Error("S7 order");fi;
for x in marks do
 if Order(x)<>2 or x*B*TransposedMat(x)<>B then Error("isometry");fi;
od;
for i in [1..6] do for j in [i+2..6] do if Comm(marks[i],marks[j])<>One(G) then Error("string");fi;od;od;
if not FullIP(marks) then Error("full IP");fi;
Print("PLAIN_GROUP_ORDER ",Size(G)," DETS ",List(marks,DeterminantMat)," FULL_IP true TYPE ",List([1..5],i->Order(marks[i]*marks[i+1])),"\n");
signed:=List(marks,x->-x);;H:=Group(signed);;
if Size(H)<>5040 or not FullIP(signed) then Error("signed marking");fi;
Print("SIGNED_GROUP_ORDER ",Size(H)," DETS ",List(signed,DeterminantMat)," FULL_IP true\n");
Print("GRAM_DETERMINANT ",DeterminantMat(B),"\n");
Print("COMPLETE_COUNTEREXAMPLE_CHECK\n");
QUIT;
