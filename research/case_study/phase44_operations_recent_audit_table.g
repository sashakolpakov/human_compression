# Independent check of the subgroup-table indexing interface used by Appendix B.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
t44:=TableOfMarks("J1");; g44:=UnderlyingGroup(t44);;
s44:=SubsTom(t44);; o44:=OrdersTom(t44);; n44:=Length(s44);;
if n44<>40 or Length(o44)<>n44 then Error("table size");fi;
if not ForAll([1..n44],i->ForAll(s44[i],j->j<=i)) then
 Error("table is not lower triangular");fi;
if s44[n44]<>[1..n44] or o44[n44]<>Size(g44) then
 Error("ambient row");fi;
# This version examines every other proper row; it does not assume sorted order.
m44:=Filtered([1..n44-1],i->not ForAny([1..n44-1],
 j->j<>i and i in s44[j]));;
if m44<>SortedList(MaximalSubgroupsTom(t44)[1]) then
 Error("maximal classes");fi;
if not ForAll(m44,i->IsSubgroup(g44,RepresentativeTom(t44,i)) and
 Size(RepresentativeTom(t44,i))=o44[i]) then Error("representatives");fi;
Print("TABLE_CLASSES ",n44," LOWER_TRIANGULAR true AMBIENT_ORDER ",Size(g44),"\n");
Print("MAXIMAL_CLASSES ",m44," ORDERS ",List(m44,i->o44[i]),"\n");
Print("COMPRESS_C_INDEPENDENT_TABLE_INTERFACE_PASS\n");
QUIT;
