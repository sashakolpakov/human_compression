# Independent L092 Construction 2 review.
# Native GAP GF(9), determinant cross-ratios, all typed Cartesian products.
# No root checker, saved block list, or saved incidence list is read.
SizeScreen([100000,24]);;
Check183:=function(b,s) if not b then Error(s); fi; end;;
K:=GF(9);; one:=One(K);; zero:=Zero(K);;
F:=Elements(K);; Points:=[1..10];;
Coords:=Concatenation(List(F,x->[one,x]),[[zero,one]]);;
det183:=function(u,v) return u[1]*v[2]-u[2]*v[1]; end;;
cross183:=function(a,b,c,d)
 return det183(Coords[a],Coords[c])*det183(Coords[b],Coords[d])/
  (det183(Coords[a],Coords[d])*det183(Coords[b],Coords[c]));
end;;
SublineBlocks:=Filtered(Combinations(Points,4),t->cross183(t[1],t[2],t[3],t[4])=-one);;
Check183(Length(SublineBlocks)=30,"harmonic subline count");;
Check183(ForAll(Combinations(Points,3),t->Number(SublineBlocks,b->IsSubset(b,t))=1),
 "Steiner property from cross ratios");;
Families:=[List(Points,x->[x]),Concatenation(List(SublineBlocks,b->
 List(Combinations(b,2),t->[b,t]))),SublineBlocks,List(Points,x->[x])];;
Types:=Concatenation(List([1..4],i->List(Families[i],x->i)));;
Objects:=Concatenation(Families);;
Indices:=List([1..4],t->Filtered([1..Length(Objects)],i->Types[i]=t));;
Incident183:=function(i,j)
 local a,b,x,y;
 a:=Types[i]; b:=Types[j]; x:=Objects[i]; y:=Objects[j];
 if a>b then return Incident183(j,i); fi;
 if a=b then return i=j; fi;
 if [a,b]=[1,2] then return x[1] in y[2]; fi;
 if [a,b]=[1,3] then return x[1] in y; fi;
 if [a,b]=[1,4] then return x<>y; fi;
 if [a,b]=[2,3] then return IsSubset(y,x[2]); fi;
 if [a,b]=[2,4] then return y[1] in Difference(x[1],x[2]); fi;
 if [a,b]=[3,4] then return not y[1] in x; fi;
 Error("missing type pair");
end;;
IsFlag183:=f->ForAll(Combinations(f,2),p->Incident183(p[1],p[2]));;
TypeSets:=Combinations([1..4]);;
FlagsByType:=List(TypeSets,t->Filtered(Cartesian(Indices{t}),IsFlag183));;
Chambers183:=FlagsByType[Position(TypeSets,[1..4])];;
for pos in [1..Length(TypeSets)] do
 projected:=Set(List(Chambers183,c->c{TypeSets[pos]}));
 Check183(projected=Set(FlagsByType[pos]),"every typed flag extends");
od;
Residue183:=function(f)
 local remaining;
 remaining:=Difference([1..4],Types{f});
 return Filtered(Concatenation(Indices{remaining}),i->ForAll(f,j->Incident183(i,j)));
end;;
Choose183:=function(b,x,y) if b then return x;else return y;fi;end;;
Connected183:=function(f)
 local r,labels,p,i,j,k,classes;
 r:=Residue183(f); labels:=[1..Length(r)];
 for p in Combinations([1..Length(r)],2) do
  i:=p[1];j:=p[2];
  if labels[i]<>labels[j] and Incident183(r[i],r[j]) then
   k:=labels[j];labels:=List(labels,x->Choose183(x=k,labels[i],x));
  fi;
 od;
 return Length(Set(labels));
end;;
rankcounts:=List([0..4],n->Sum(Filtered([1..Length(TypeSets)],i->Length(TypeSets[i])=n),i->Length(FlagsByType[i])));;
paneldegrees:=[];; ResidueTable:=[];; IP2Checks:=0;; left:=[];;right:=[];;
for pos in [1..Length(TypeSets)] do
 ts:=TypeSets[pos]; flags:=FlagsByType[pos];
 if Length(ts)<=2 then
  sizes:=List(flags,f->Length(Residue183(f)));
  components:=List(flags,Connected183);
  Check183(Set(components)=[1],"all residues connected for this fixed type set");
  Add(ResidueTable,[ts,Length(flags),Collected(sizes),Collected(components)]);
  if Length(ts)=2 then
   remtypes:=Difference([1..4],ts);
   for f in flags do
    res:=Residue183(f);left:=Intersection(res,Indices[remtypes[1]]);
    right:=Intersection(res,Indices[remtypes[2]]);
    complete:=ForAll(left,i->ForAll(right,j->Incident183(i,j)));
    partial:=ForAll(Combinations(left,2),ij->Number(right,k->Incident183(ij[1],k)
     and Incident183(ij[2],k))<=1) and ForAll(Combinations(right,2),ij->
     Number(left,k->Incident183(ij[1],k) and Incident183(ij[2],k))<=1);
    Check183(complete or partial,"rank-two partial-linear or digon axiom");
    IP2Checks:=IP2Checks+1;
   od;
  fi;
 elif Length(ts)=3 then
  degrees:=List(flags,f->Length(Residue183(f)));
  Check183(Minimum(degrees)>=2,"firm panels");
  Append(paneldegrees,degrees);
 fi;
od;

# Every triple can be normalized by a unique fractional linear map.
# Count the remaining full design automorphisms by testing all 7! permutations
# fixing 0,1,infinity; this is a full-group upper bound, not a subgroup census.
z:=Position(F,zero);; u:=Position(F,one);; fixed:=[z,u,10];;
stabilizer:=Filtered(Elements(SymmetricGroup(Difference(Points,fixed))),g->
 ForAll(SublineBlocks,b->OnSets(b,g) in SublineBlocks));;
Check183(Length(stabilizer)=2,"complete normalized design automorphism census");;
FullDesignAutOrder:=10*9*8*Length(stabilizer);;
Check183(FullDesignAutOrder mod Length(Chambers183)<>0,"chamber transitivity excluded by full-group order");;
Print("BLOCKS ",SublineBlocks,"\n");
Print("OBJECT_COUNTS ",List(Families,Length),"\n");
Print("FLAG_COUNTS ",rankcounts,"\n");
Print("TYPED_FLAG_COUNTS ",List([1..Length(TypeSets)],i->[TypeSets[i],Length(FlagsByType[i])]),"\n");
Print("RESIDUE_TABLE ",ResidueTable,"\n");
Print("PANEL_DEGREES ",Collected(paneldegrees),"\n");
Print("IP2_RESIDUES_CHECKED ",IP2Checks,"\n");
Print("FULL_DESIGN_AUT_ORDER ",FullDesignAutOrder," CHAMBERS ",Length(Chambers183),"\n");
alpha:=First(F,x->x^2=-one);;
Map183:=Concatenation(List([0..8],n->Position(F,(n mod 3)*one+QuoInt(n,3)*alpha)),[10]);;
Print("ROOT_TO_NATIVE_POINT_MAP ",Map183,"\n");
Print("NATIVE_TYPES ",Types,"\n");
Print("NATIVE_OBJECTS ",Objects,"\n");
Print("NATIVE_NEIGHBOURS ",List([1..Length(Objects)],i->Filtered([1..Length(Objects)],j->
 Types[i]<>Types[j] and Incident183(i,j))),"\n");
Print("L092_LITERAL_Q3_E2_INDEPENDENT_PASS\n");
QUIT;
