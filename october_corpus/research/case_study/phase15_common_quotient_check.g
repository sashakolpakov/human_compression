# Exact diagnostics for the all-rank class<=4 canonical common-quotient proof.
# GAP/NQ only. No group catalogue, imported group or previous report is used.
if LoadPackage("nq")=fail then Error("NQ package required");fi;
SizeScreen([240,24]);;

UniversalPathFour:=function(d)
 local F,r,rels,i,j,G;
 F:=FreeGroup(d);r:=GeneratorsOfGroup(F);rels:=List(r,x->x^2);
 for i in [1..d] do
  for j in [i+1..d] do
   if j>i+1 then Add(rels,Comm(r[i],r[j]));fi;
  od;
 od;
 G:=NilpotentQuotient(F/rels,4);
 return rec(group:=G,r:=GeneratorsOfGroup(G){[1..d]});
end;

CheckAllIP:=function(G,r)
 local subsets,groups,i,j,k,valid;
 subsets:=Combinations([1..Length(r)]);
 groups:=List(subsets,I->Subgroup(G,r{I}));
 valid:=true;
 for i in [1..Length(groups)] do
  for j in [1..Length(groups)] do
   k:=Position(subsets,Intersection(subsets[i],subsets[j]));
   if Intersection(groups[i],groups[j])<>groups[k] then valid:=false;fi;
  od;
 od;
 return valid;
end;

CheckClassFourCollection:=function(d)
 local data,G,r,one,c,z,t,p,s,q,h,lc,L3,L4,D,At,ZTable,TTable,
       i,j,k,expected,countZ,countT,countDouble,countEdge,countPower,
       masks,I,g,selected,J,tests,pair,word,countCut;
 data:=UniversalPathFour(d);G:=data.group;r:=data.r;one:=One(G);
 c:=List([1..d-1],i->Comm(r[i],r[i+1]));z:=List(c,x->x^2);
 t:=List([1..d-2],i->Comm(c[i],r[i+2]));p:=List(c,x->x^4);
 s:=List(t,x->x^2);q:=List([1..d-2],i->Comm(c[i],c[i+1]));
 h:=List([1..d-3],i->Comm(t[i],r[i+3]));
 lc:=LowerCentralSeries(G);L3:=lc[3];L4:=lc[4];D:=lc[2];
 At:=function(list,index)
  if index<1 or index>Length(list) then return one;fi;
  return list[index];
 end;
 ZTable:=function(i,j)
  if j=i-1 then return At(s,i-1);fi;
  if j=i or j=i+1 then return At(p,i);fi;
  if j=i+2 then return At(s,i);fi;
  return one;
 end;
 TTable:=function(i,j)
  if i<1 or i>Length(t) then return one;fi;
  if j=i-1 then return At(h,i-1);fi;
  if j=i or j=i+2 then return At(s,i);fi;
  if j=i+1 then return At(q,i)*At(s,i);fi;
  if j=i+3 then return At(h,i);fi;
  return one;
 end;
 if NilpotencyClassOfGroup(G)<>4 then Error("Universal class");fi;
 if not IsElementaryAbelian(L4) or not IsAbelian(L3) or Exponent(L3)>4 then Error("Layer structure");fi;
 if NilpotencyClassOfGroup(D)>2 then Error("Derived class");fi;
 if Group(Concatenation(p,s,q,h))<>L4 then Error("Gamma4 generators");fi;
 if Group(Concatenation(z,t,p,s,q,h))<>L3 then Error("Gamma3 generators");fi;
 if not ForAll(Concatenation(p,s,q,h),x->Order(x)<=2 and ForAll(r,y->Comm(x,y)=one)) then Error("Central involutions");fi;
 countZ:=0;countT:=0;countDouble:=0;countEdge:=0;countPower:=0;countCut:=0;
 for i in [1..Length(z)] do
  for j in [1..d] do
   if Comm(z[i],r[j])<>ZTable(i,j) then Error("z table");fi;
   countZ:=countZ+1;
  od;
 od;
 for i in [1..Length(t)] do
  for j in [1..d] do
   if Comm(t[i],r[j])<>TTable(i,j) then Error("t table");fi;
   countT:=countT+1;
  od;
 od;
 for i in [1..Length(c)] do
  for j in [1..d] do
   for k in [1..d] do
    expected:=one;
    if j=i-1 then expected:=TTable(i-1,k);fi;
    if j=i or j=i+1 then expected:=ZTable(i,k);fi;
    if j=i+2 then expected:=TTable(i,k);fi;
    if Comm(Comm(c[i],r[j]),r[k])<>expected then Error("Double commutator table");fi;
    countDouble:=countDouble+1;
   od;
  od;
  for j in [i+1..Length(c)] do
   expected:=one;
   if j=i+1 then expected:=At(q,i);fi;
   if j=i+2 then expected:=At(h,i);fi;
   if Comm(c[i],c[j])<>expected then Error("Edge commutator");fi;
   countEdge:=countEdge+1;
  od;
 od;
 masks:=Combinations([1..Length(c)]);
 for I in masks do
  g:=Product(c{I},one);
  if g^4<>Product(p{I},one) then Error("Fourth-power formula");fi;
  countPower:=countPower+1;
  for j in [1..d] do
   for k in [1..d] do
    expected:=Product(List(I,i->Comm(Comm(c[i],r[j]),r[k])),one);
    if Comm(Comm(g,r[j]),r[k])<>expected then Error("Product double commutator");fi;
   od;
  od;
  # Equations (9)--(11), after precisely the selected p/s terms have
  # been killed. This checks the cut equations with their actual
  # boundary ranges, independently of requiring a relation in gamma3.
  selected:=i->i in I;
  J:=Subgroup(G,Concatenation(p{I},List(I,i->At(s,i-1)),List(I,i->At(s,i))));
  for i in I do
   tests:=[];
   if i>=2 and i<=d-2 then Add(tests,[i-1,i+2,At(h,i-1)]);fi;
   if i>=2 then
    word:=At(q,i-1);
    if selected(i-3) then word:=word*At(h,i-3);fi;
    Add(tests,[i-1,i,word]);
   fi;
   if i>=3 then
    word:=At(h,i-2);
    if selected(i-3) then word:=word*At(q,i-3);fi;
    Add(tests,[i-1,i-2,word]);
   fi;
   if i<=d-2 then
    word:=At(q,i);
    if selected(i+3) then word:=word*At(h,i+1);fi;
    Add(tests,[i+2,i+1,word]);
   fi;
   if i<=d-3 then
    word:=At(h,i);
    if selected(i+3) then word:=word*At(q,i+2);fi;
    Add(tests,[i+2,i+3,word]);
   fi;
   for pair in tests do
    if not Comm(Comm(g,r[pair[1]]),r[pair[2]])*pair[3] in J then Error("Cut correction equation");fi;
    countCut:=countCut+1;
   od;
  od;
 od;
 if Size(G)/Size(L3)<>2^(2*d-1) then Error("Universal class2 order");fi;
 Print("collection rank=",d," order=",Size(G)," gamma3=",Size(L3)," gamma4=",Size(L4),
       " z_t=",countZ+countT," double=",countDouble," edge=",countEdge,
       " masks=",countPower," product_double=",countPower*d*d," cut=",countCut," PASS\n");
 return [countZ+countT,countDouble,countEdge,countPower,countPower*d*d,countCut];
end;

CheckRankThreeClassFourQuotients:=function()
 local data,iso,G,r,D,L3,normals,N,hom,H,s,type,counts,bad,valid;
 data:=UniversalPathFour(3);iso:=IsomorphismPermGroup(data.group);G:=Image(iso);
 r:=List(data.r,x->Image(iso,x));D:=DerivedSubgroup(G);L3:=CommutatorSubgroup(D,G);
 normals:=NormalSubgroups(G);counts:=[0,0,0,0,0];
 for N in normals do
  if not IsSubgroup(D,N) then continue;fi;
  counts[1]:=counts[1]+1;
  hom:=NaturalHomomorphismByNormalSubgroup(G,N);H:=Image(hom);
  s:=List(r,x->Image(hom,x));type:=List([1..2],i->Order(s[i]*s[i+1]));
  if Minimum(type)<4 then continue;fi;
  counts[2]:=counts[2]+1;
  bad:=not IsSubgroup(L3,N);
  if bad then counts[3]:=counts[3]+1;fi;
  valid:=CheckAllIP(H,s);
  if valid then
   counts[4]:=counts[4]+1;
   if bad then counts[5]:=counts[5]+1;fi;
   if Size(H)/Size(CommutatorSubgroup(DerivedSubgroup(H),H))<>32 then Error("Class4 IP counterexample");fi;
  fi;
 od;
 if Length(normals)<>207 or counts<>[174,167,9,114,0] then Error("Class4 diagnostic counts changed");fi;
 Print("quotient census universal_order=",Size(G)," all_normals=",Length(normals),
       " derived_kernels=",counts[1]," nondegenerate=",counts[2],
       " smaller_class2=",counts[3]," IP_valid=",counts[4],
       " smaller_class2_and_IP=",counts[5]," all_subset_comparisons=",64*counts[2]," PASS\n");
 return counts;
end;

Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
total:=Sum(List([2..6],CheckClassFourCollection));;
counts:=CheckRankThreeClassFourQuotients();;
Print("totals z_t,double,edge,masks,product_double,cut=",total,"\n");
Print("PASS: universal class4 collection and full rank3/class<=4 quotient diagnostics; uniform proof is separate.\n");
QUIT;
