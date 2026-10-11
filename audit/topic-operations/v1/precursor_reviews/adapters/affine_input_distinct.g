Require := function(ok,msg) if not ok then Error(msg); fi; end;
CanonicalVector := function(v,s)
 local a,b;
 a:=List(v,x->x mod (2*s)); b:=List(a,x->(x+s) mod (2*s));
 return Minimum(a,b);
end;
ProductSet := function(H,K)
 return Set(Concatenation(List(Elements(H),h->List(Elements(K),k->h*k))));
end;
CheckParameter := function(s)
 local vectors,n,marks,permutations,shifts,m,p,shift,images,v,w,j,pos,G,i,e,
       supports,subgroups,orders,products,k,l;
 vectors:=Set(Concatenation(List([0..2*s-1],i->Concatenation(
  List([0..2*s-1],j->List([0..2*s-1],k->CanonicalVector([i,j,k,-i-j-k],s)))))));
 n:=Length(vectors);Require(n=4*s^3,"root lattice quotient order");
 marks:=[];
 permutations:=[(1,2),(2,3),(1,4),(3,4)];
 shifts:=[[0,0,0,0],[0,0,0,0],[1,0,0,-1],[0,0,0,0]];
 for m in [1..4] do
  p:=permutations[m];shift:=shifts[m];images:=[];
  for v in vectors do
   w:=ShallowCopy(shift);
   for j in [1..4] do w[j^p]:=w[j^p]+v[j];od;
   w:=CanonicalVector(w,s);pos:=Position(vectors,w);
   Require(pos<>fail,"affine action preserves root quotient");Add(images,pos);
  od;
  for j in [1..4] do Add(images,n+j^p);od;
  Add(marks,PermList(images));
 od;
 G:=Group(marks);Require(Size(G)=96*s^3,"faithful affine quotient order");
 Require(ForAll(marks,a->Order(a)=2),"literal reflection orders");
 for i in [1..4] do for j in [i+1..4] do
  if [i,j] in [[1,4],[2,3]] then e:=2;else e:=3;fi;
  Require(Order(marks[i]*marks[j])=e,"literal Coxeter orders");
 od;od;
 Require(Order(marks[3]*marks[4]*marks[1]*marks[2])=2*s,"literal quotient word");
 supports:=List([0..14],mask->Filtered([1..4],i->QuoInt(mask,2^(i-1)) mod 2=1));
 subgroups:=List(supports,I->Subgroup(G,marks{I}));
 orders:=List(subgroups,Size);
 Require(orders=[1,2,2,6,2,6,4,24,2,4,6,24,6,24,24],"all proper parabolic orders");
 products:=List(subgroups,H->List(subgroups,K->ProductSet(H,K)));
 for i in [1..15] do for j in [1..15] do
  k:=Position(supports,Intersection(supports[i],supports[j]));
  Require(Intersection(subgroups[i],subgroups[j])=subgroups[k],"parabolic IP");
 od;od;
 for i in [1..15] do for j in [1..15] do for k in [1..15] do
  l:=Position(supports,Intersection(supports[j],supports[k]));
  Require(Intersection(products[i][j],products[i][k])=products[i][l],"coset Helly product identity");
 od;od;od;
 Print("PASS_DISTINCT_AFFINE_INPUT:s=",s,";order=",Size(G),";degree=",n+4,";proper=15;IP=225;products=3375\n");
end;
for s in [2,3,4] do CheckParameter(s);od;
QUIT;
