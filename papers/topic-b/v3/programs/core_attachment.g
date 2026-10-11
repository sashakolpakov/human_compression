# Exact finite hypotheses of the tree-attachment intersection theorem.
# The 156 identities validate explicit proofs on four or five letters.
SetAssertionLevel(1);
SubsetIndices:=Combinations([1,2]);;
Young:=function(blocks)
 local gens,b;
 gens:=[];
 for b in blocks do
  if Length(b)>1 then Append(gens,List([2..Length(b)],i->(b[1],b[i])));fi;
 od;
 if Length(gens)=0 then return Group(());fi;
 return Group(gens);
end;;
CheckCore:=function(name,marks,root)
 local H,parts,Y,S,T,hs,ht,merged,other,C,i,x,plus,n;
 H:=[];parts:=[];Y:=[];n:=0;
 for S in SubsetIndices do
  if Length(S)=0 then hs:=Group(());else hs:=Group(marks{S});fi;
  Add(H,hs);Add(parts,Orbits(hs,[1..4]));Add(Y,Young(parts[Length(parts)]));
 od;
 for i in [1..Length(H)]do
  C:=First(parts[i],b->root in b);other:=Filtered(parts[i],b->not root in b);plus:=Young(Concatenation([Concatenation(C,[5])],other));
  if Group(Concatenation(GeneratorsOfGroup(H[i]),[(root,5)]))<>plus then Error(name," failed saturation");fi;
  for x in [1..Length(H)]do
   S:=Position(SubsetIndices,Intersection(SubsetIndices[i],SubsetIndices[x]));
   if Intersection(H[i],H[x])<>H[S]then Error(name," failed core IP");fi;
   if Intersection(H[i],Y[x])<>H[S]then Error(name," failed mixed core intersection");fi;
   if Intersection(Y[i],Y[x])<>Y[S]then Error(name," failed partition meet");fi;
   n:=n+3;
  od;
  n:=n+1;
 od;
 Print(name,": PASS finite core checks=",n," root=",root," orders=",List(H,Size),"\n");
end;;
CheckCore("A",[(2,3),(1,2)(3,4)],4);
CheckCore("B",[(2,3),(1,2)(3,4)],3);
CheckCore("C",[(1,2)(3,4),(1,3)(2,4)],4);
QUIT;
