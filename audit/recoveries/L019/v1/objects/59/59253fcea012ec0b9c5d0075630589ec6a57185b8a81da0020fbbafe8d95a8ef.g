RunL019Check := function()
local rows,row,s,u,v,ii,m,sets,groups,a,b,c,ip;
rows := [
rec(tag:="1", marks:=[(2,3)(4,7)(5,8)(6,9),(1,2)(3,4),(2,3)(4,5)(7,8),(5,6)(8,9)]),
rec(tag:="2", marks:=[(1,2)(3,7)(4,8)(5,9),(2,3)(6,7),(1,2)(3,4)(7,8),(4,5)(8,9)]),
rec(tag:="3", marks:=[(1,2),(2,3)(4,5),(3,4)(5,6),(6,7)]),
rec(tag:="4", marks:=[(4,7)(5,8)(6,9),(1,2)(3,4),(2,3)(4,5)(7,8),(5,6)(8,9)]),
rec(tag:="5a", marks:=[(1,2)(6,7),(2,3)(4,8)(5,9),(3,4)(1,6)(2,7),(4,5)(8,9)]),
rec(tag:="5b", marks:=[(1,2)(7,8),(2,3)(4,9)(5,10)(6,11),(3,4)(1,7)(2,8),(4,5)(9,10)]),
rec(tag:="6a", marks:=[(1,2),(2,3)(4,7)(5,8),(3,4)(6,7),(4,5)(7,8)]),
rec(tag:="6b", marks:=[(1,2),(2,3)(4,8)(5,9)(6,10),(3,4)(7,8),(4,5)(8,9)]),
rec(tag:="7", marks:=[(1,2),(2,3)(4,6)(5,7),(3,4)(7,8),(4,5)(6,7)]),
rec(tag:="8", marks:=[(1,2),(2,3)(4,7)(5,8),(3,4)(5,6),(4,5)(7,8)]),
rec(tag:="9", marks:=[(1,2),(2,3)(4,5),(3,4)(5,6),(4,5)(6,7)])
 ];
for row in rows do
 s:=row.marks; u:=Group(s{[2..4]});v:=Group(s{[1..3]});ii:=Intersection(u,v);m:=Group(s{[2,3]});
 if not ForAll([[1,3],[1,4],[2,4]],p->s[p[1]]*s[p[2]]=s[p[2]]*s[p[1]]) then Error("string");fi;
 Print("ROW ",row.tag," ",Size(u)," ",Size(v)," ",Size(ii)," ",Size(m)," ",Index(ii,m),"\n");
 if row.tag="9" then
 sets:=Combinations([1..4]);groups:=List(sets,i->Group(s{i},()));ip:=true;
 for a in [1..16] do for b in [1..16] do c:=Position(sets,Intersection(sets[a],sets[b])); if Intersection(groups[a],groups[b])<>groups[c] then ip:=false;fi;od;od;
 if not ip or Size(Group(s))<>5040 or List([1..3],i->Order(s[i]*s[i+1]))<>[6,5,5] then Error("graph9");fi;
 Print("GRAPH9_ALL_256_SUBSET_PAIRS_PASS\n");
 fi;
od;
Print("PASS_L019_LITERAL_DIAGRAMS_GAP\n");
end;
RunL019Check();
QUIT_GAP(0);
