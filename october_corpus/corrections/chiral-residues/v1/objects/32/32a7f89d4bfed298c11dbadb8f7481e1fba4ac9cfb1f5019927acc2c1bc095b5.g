Read("/dev/null");;
Need := function(ok, why)
  if not ok then Print("FAIL: ",why,"\n"); QUIT_GAP(1); fi;
end;;
f := GF(13);; one := One(f);;
ks := Set(List([1,3,4,9,10,12], n -> n*one));;
Decoration := v -> Set(List(ks, k -> k*v));;
points := Set(Concatenation(List(Elements(f), a ->
  List(Filtered(Elements(f), b -> a<>Zero(f) or b<>Zero(f)),
       b -> Decoration([a,b])))));;
Need(Length(points)=28,"28 scalar classes");;
mats := List([[[1,0],[0,1]],[[4,0],[7,10]],[[4,6],[0,10]],[[3,0],[0,9]]],
  m -> List(m, row -> List(row, n -> n*one)));;
# Inverse transpose gives a right action with the source's product convention.
marks := List(mats, m -> Permutation(TransposedMat(m)^-1,points,OnSets));;
grp := Group(marks);;
Need(Size(grp)=1092,"PSL2(13)");;
subsets := Combinations([1..4]);;
parts := List(subsets, s -> Group(Concatenation([ [()]],
   List(s, i -> List(s,j -> marks[i]^-1*marks[j])))));;
for i in [1..16] do
 for j in [1..16] do
  Need(Intersection(parts[i],parts[j])=parts[Position(subsets,Intersection(subsets[i],subsets[j]))],"IC-plus");
 od;
od;
base := List([[4,1],[1,0],[0,1],[1,1]], v -> Position(points,Decoration(v*one)));;
parabolics := List([1..4],i -> parts[Position(subsets,Difference([1..4],[i]))]);;
Need(List(parabolics,Size)=[39,39,39,39],"parabolic orders");;
for i in [1..4] do
 Need(parabolics[i]=Stabilizer(grp,base[i]),"actual point stabilizer");
od;
cosets := List(parabolics,h -> RightCosets(grp,h));;
pointlabels := List([1..4],i -> List(cosets[i],c -> base[i]^Representative(c)));;
for row in pointlabels do Need(Set(row)=[1..28],"coset-point bijection"); od;
sets := List(cosets,row -> List(row,AsSSortedList));;
Adjacent := function(i,j)
 local v,w;
 v:=points[i][1];w:=points[j][1];
 return v[1]*w[2]-v[2]*w[1] in ks;
end;;
checked:=0;;
for ij in Combinations([1..4],2) do
 for a in [1..28] do
  for b in [1..28] do
   Need((Length(Intersection(sets[ij[1]][a],sets[ij[2]][b]))>0)=
     Adjacent(pointlabels[ij[1]][a],pointlabels[ij[2]][b]),"literal right-coset incidence");
   checked:=checked+1;
  od;
 od;
od;
# Build the rank-two residue from coset intersections themselves.
fixed := List([2,3],i -> Position(cosets[i],parabolics[i]));;
Need(not fail in fixed,"base cosets");;
resobjects:=[];;
for i in [1,4] do
 for a in [1..28] do
  if ForAll([1,2],j -> Length(Intersection(sets[i][a],sets[j+1][fixed[j]]))>0) then
   Add(resobjects,[i,a]);
  fi;
 od;
od;
radj:=List(resobjects,x -> Filtered([1..Length(resobjects)],j ->
  resobjects[j][1]<>x[1] and Length(Intersection(sets[x[1]][x[2]],sets[resobjects[j][1]][resobjects[j][2]]))>0));;
Need(Length(resobjects)=12 and ForAll(radj,x -> Length(x)=2),"rank-two coset residue");;
remaining:=[1..12];; sizes:=[];;
while Length(remaining)>0 do
 reached:=[remaining[1]]; at:=1;
 while at<=Length(reached) do
  UniteSet(reached,radj[reached[at]]);
  at:=at+1;
 od;
 # A stable closure avoids dependence on insertion order in the sorted set.
 repeat
  old:=ShallowCopy(reached);
  for v in old do UniteSet(reached,radj[v]); od;
 until old=reached;
 Add(sizes,Length(reached));SubtractSet(remaining,reached);
od;
Need(SortedList(sizes)=[6,6],"two disconnected six-cycles");;
Print("PASS independent GAP: order ",Size(grp),", all256 intersections, ",checked,
 " literal coset incidences, residue components ",SortedList(sizes),"\n");
QUIT_GAP(0);
