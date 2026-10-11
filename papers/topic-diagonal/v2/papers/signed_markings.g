# Finite validation of the written all-rank module and cocycle proofs.
SizeScreen([180,1000]);;
Check:=function(ok,msg) if not ok then Error(msg);fi;end;;
IP:=function(gens)
 local sets,groups,i,j,k;
 sets:=Combinations([1..Length(gens)]);;
 groups:=List(sets,s->Group(Concatenation([()],gens{s})));;
 for i in [1..Length(sets)] do
  for j in [1..Length(sets)] do
   k:=Position(sets,Intersection(sets[i],sets[j]));
   Check(Intersection(groups[i],groups[j])=groups[k],"all-subset IP");
  od;
 od;
 return Length(sets)^2;
end;;
for r in [3..8] do
 e:=List([1..r],j->(2*j-1,2*j));;lambda:=Product(e);;
 s:=List([1..r-1],i->(2*i-1,2*i+1)(2*i,2*i+2));;
 q:=List([1..r-1],i->lambda*e[i]*e[i+1]*s[i]);;
 for seed in [lambda,e[1],lambda*e[1]] do
  plain:=Concatenation([seed],s);;changed:=Concatenation([seed],q);;
  G:=Group(plain);;H:=Group(changed);;
  f:=GroupHomomorphismByImages(G,H,plain,changed);;
  Check(f<>fail and IsBijective(f),"exact marked isomorphism");;
  if seed=lambda then expected:=2*Factorial(r);
  elif seed=e[1] or r mod 2=0 then expected:=2^r*Factorial(r);
  else expected:=2^(r-1)*Factorial(r);fi;
  Check(Size(G)=expected and Size(H)=expected,"exact expected orders");;
  for i in [1..r] do for j in [1..r] do
   if AbsInt(i-j)>1 then Check(Order(plain[i]*plain[j])=2 and Order(changed[i]*changed[j])=2,"string commutations");fi;
  od;od;
  if r<=6 then n:=IP(plain)+IP(changed);else n:=0;fi;
  Print("SIGNED_MARKINGS r=",r," seed=",Position([lambda,e[1],lambda*e[1]],seed)," order=",expected," exact_iso=1 IP_checks=",n," PASS\n");
 od;
od;
Print("SIGNED_MARKINGS_ALL_VALIDATION_PASS\n");
QUIT;
