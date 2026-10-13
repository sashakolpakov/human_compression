rows:=[[[1, 2, 3, 4, 5, 6, 8, 7], [1, 2, 3, 4, 5, 7, 6, 8], [1, 2, 3, 4, 6, 5, 7, 8], [1, 2, 3, 5, 4, 6, 7, 8], [2, 1, 4, 3, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8]], [[1, 2, 3, 4, 5, 6, 8, 7], [1, 2, 3, 4, 7, 8, 5, 6], [1, 2, 3, 5, 4, 6, 7, 8], [1, 2, 4, 3, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [2, 1, 3, 4, 5, 6, 7, 8]]];;
S:=SymmetricGroup(8);;
c:=[(2,3),(1,2)(3,4),(4,5),(5,6),(6,7),(7,8)];;
for row in rows do
 t:=List(row,PermList);;
 if Length(t)<>6 or Group(t)<>S or not ForAll([1..6],i->Group(t{Difference([1..6],[i])})<>S) then Error("actual independent generating string");fi;
 if not ForAll(t,x->Order(x)=2) then Error("involutions");fi;
 for i in [1..6] do for j in [i+2..6] do if Comm(t[i],t[j])<>() then Error("string");fi;od;od;
 if RepresentativeAction(S,t,c,OnTuples)=fail and RepresentativeAction(S,t,Reversed(c),OnTuples)=fail then Error("core identification");fi;
od;
if RepresentativeAction(S,List(rows[1],PermList),List(rows[2],PermList),OnTuples)<>fail then Error("duplicate ordered classes");fi;
bad:=Concatenation(c,[c[1]]);;
if ForAll([1..7],i->Group(bad{Difference([1..7],[i])})<>Group(bad)) then Error("negative control");fi;
Print("TWO_COMPLETE_INDEPENDENT_ORDERED_CORE_CLASSES_PASS\n");QUIT;
