# Distinct review of the Fi24 marking. Only primary permutations and saved
# word data are read. Neither author program nor local_geometry.g is used.
# The anchored-coset method adapts the independently reviewed Fi22 checker.
Read("F24d2G1-p306936B0.g1");;
Read("F24d2G1-p306936B0.g2");;
Read("F24_compact.g");;
Require:=function(ok,msg) if not ok then Error(msg);fi;end;;
EvalWord:=function(gs,w)
 local result,letter;
 result:=();
 for letter in w do
  Require(letter<>0 and AbsInt(letter)<=Length(gs),"word index");
  result:=result*gs[AbsInt(letter)]^SignInt(letter);
 od;
 return result;
end;;
c:=b11;;d:=b21;;a:=EvalWord([c,d],F24aWord)^F24aPower;;
centralizers:=[];;
for seed in F24BraySeeds do
 h:=EvalWord([c,d],seed);x:=c*c^h;n:=Order(x);
 Require(n mod 2=1,"odd centralizer construction");
 z:=h*x^((n-1)/2);Require(c^z=c,"actual centralizer identity");
 Add(centralizers,z);
od;
b:=Product(List(F24bFactors,i->centralizers[i]))^F24bPower;;
r:=[c,a,b];;s:=[c,a,b^-1*a*b];;
Require(Order(EvalWord(r,F24Prime23[1])^F24Prime23[2])=23,"order23");;
Require(Order(EvalWord(r,F24Prime29[1])^F24Prime29[2])=29,"order29");;
Require(b=(s[2]*s[3])^17*s[2],"halved generation inverse");;
Require(List([[1,2],[1,3],[2,3]],p->Order(r[p[1]]*r[p[2]]))=[6,2,35],"string orders");;
Require(List([[1,2],[1,3],[2,3]],p->Order(s[p[1]]*s[p[2]]))=[6,6,35],"triangle orders");;
# Finite closure from the identity, without GAP Group/Intersection machinery.
Closure:=function(gs)
 local elements,pos,g,y;
 elements:=[()];pos:=1;
 while pos<=Length(elements) do
  for g in gs do
   y:=elements[pos]*g;
   if not y in elements then Add(elements,y);fi;
  od;
  pos:=pos+1;
  Require(Length(elements)<=100,"proper subgroup unexpectedly large");
 od;
 return Set(elements);
end;;
Analyze:=function(m)
 local ix,subs,A,B,i,j,k,ps,C,D,y,z,w,pairs,flags,counts;
 Require(Length(Set(m))=3 and ForAll(m,g->g^2=() and g<>()),"marks");
 ix:=Filtered(Combinations([1,2,3]),x->Length(x)<3);
 subs:=List(ix,x->Closure(m{x}));pairs:=0;
 for A in [1..7] do for B in [1..7] do
  Require(Intersection(subs[A],subs[B])=subs[Position(ix,Intersection(ix[A],ix[B]))],"literal intersection");
  pairs:=pairs+1;
 od;od;
 ps:=List([1..3],v->subs[Position(ix,Difference([1..3],[v]))]);
 counts:=[];
 for i in [1..3] do
  j:=Difference([1..3],[i])[1];k:=Difference([1..3],[i])[2];
  C:=Set(List(ps[i],g->Set(List(ps[j],h->g*h))));
  D:=Set(List(ps[i],g->Set(List(ps[k],h->g*h))));
  flags:=0;
  for y in C do for z in D do
   w:=Intersection(y,z);
   if Length(w)>0 then
    flags:=flags+1;
    Require(Length(Intersection(w,ps[i]))=1,"incident triple unique representative");
   fi;
  od;od;
  Require(flags=Length(ps[i]),"anchored chamber count");
  Add(counts,[Length(C),Length(D),flags]);
 od;
 return rec(properIP:=pairs,anchored:=counts);
end;;
u:=Analyze(r);;Print("STRING ",u,"\n");;
v:=Analyze(s);;Print("TRIANGLE ",v,"\n");;
Print("INDEPENDENT_FI24_LITERAL_COSETS PASS 98properIP 6all-flag-families 30full-subset-identities\n");;
QUIT;
