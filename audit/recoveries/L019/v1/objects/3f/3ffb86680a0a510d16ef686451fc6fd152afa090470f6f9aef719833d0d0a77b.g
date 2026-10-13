rows:=[[[1, 2, 5, 6, 3, 4], [1, 3, 2, 5, 4, 6], [2, 1, 3, 6, 5, 4]], [[1, 2, 5, 6, 3, 4], [1, 3, 2, 5, 4, 6], [2, 1, 5, 4, 3, 6]], [[1, 2, 5, 6, 3, 4], [3, 4, 1, 2, 5, 6], [2, 1, 3, 6, 5, 4]], [[1, 2, 5, 6, 3, 4], [1, 3, 2, 5, 4, 6], [2, 1, 4, 3, 6, 5]], [[1, 2, 5, 6, 3, 4], [1, 3, 2, 5, 4, 6], [2, 1, 6, 5, 4, 3]], [[1, 2, 5, 6, 3, 4], [3, 6, 1, 5, 4, 2], [2, 1, 3, 6, 5, 4]], [[2, 1, 4, 3, 6, 5], [1, 3, 2, 5, 4, 6], [1, 2, 5, 6, 3, 4]], [[2, 1, 4, 3, 6, 5], [1, 3, 2, 5, 4, 6], [2, 1, 6, 5, 4, 3]], [[2, 1, 4, 3, 6, 5], [1, 4, 3, 2, 6, 5], [1, 2, 5, 6, 3, 4]], [[2, 1, 4, 3, 6, 5], [1, 4, 3, 2, 6, 5], [2, 1, 6, 5, 4, 3]], [[2, 1, 4, 3, 6, 5], [3, 5, 1, 6, 2, 4], [2, 1, 6, 5, 4, 3], [6, 5, 4, 3, 2, 1]], [[1, 2, 3, 7, 8, 9, 4, 5, 6, 10], [1, 6, 5, 4, 3, 2, 10, 8, 9, 7], [2, 1, 3, 5, 4, 6, 8, 7, 9, 10], [1, 3, 2, 4, 6, 5, 7, 9, 8, 10], [1, 2, 10, 8, 7, 6, 5, 4, 9, 3]]];;

ReplayPrimitiveBoundary:=function()
local k,row,marks,orientation,n,tail,points,a,G,C,images,hom,found;
C:=CyclicGroup(2);found:=[];
for k in [1..Length(rows)] do
 row:=rows[k];n:=Length(row[1]);marks:=List(row,PermList);
 for orientation in [0,1] do
  if orientation=1 then marks:=Reversed(marks);fi;
  G:=Group(marks);tail:=Group(marks{[2..Length(marks)]});
  images:=List(marks,x->One(C));images[1]:=GeneratorsOfGroup(C)[1];
  hom:=GroupHomomorphismByImages(G,C,marks,images);
  points:=Filtered([1..n],a->a^marks[1]<>a and ForAll(marks{[2..Length(marks)]},x->a^x=a));
  for a in points do
   if IsTransitive(tail,Difference([1..n],[a])) and hom<>fail then
    if [n,Length(marks),Size(G),Size(tail),a]<>[6,3,120,10,1] then Error("wrong primitive boundary");fi;
    Add(found,[k-1,orientation]);
   fi;
  od;
 od;
od;
if found<>[[3,1],[4,1],[6,0],[8,0]] then Error("wrong surviving list");fi;
Print("PASS_PRIMITIVE12_ORIENTATIONS24_SURVIVORS4_TYPES2\n");
end;
ReplayPrimitiveBoundary();QUIT_GAP(0);
