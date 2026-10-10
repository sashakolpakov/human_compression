# Independent literal source-presentation replay, without cyclotomic matrices.
Check248:=function(ok,s) if not ok then Error(Concatenation("P248_REJECT ",s));fi;end;;
IP248:=function(rr)
 local subsets,hs,i,j;
 subsets:=Combinations([1..3]);hs:=List(subsets,x->Group(rr{x},One(rr[1])));
 for i in [1..8] do for j in [1..8] do
  if Intersection(hs[i],hs[j])<>hs[Position(subsets,Intersection(subsets[i],subsets[j]))] then return false;fi;
 od;od;return true;
end;;
Run248:=function()
 local par,p,m,n,e,r,F,x,b,rels,i,j,U,iso,P,ss,beta,sigma,tau,K,G,a,z,rs,moduli;
 for par in [[3,3],[3,6],[5,3],[5,5],[11,3]] do
  p:=par[1];m:=par[2];n:=m-1;e:=QuoInt(n-1,p-1)+1;r:=((n-1) mod (p-1))+1;
  F:=FreeGroup(p);x:=GeneratorsOfGroup(F){[1..p-1]};b:=GeneratorsOfGroup(F)[p];
  moduli:=Concatenation(List([1..r],i->p^e),List([r+1..p-1],i->p^(e-1)));
  rels:=Concatenation(List([1..p-1],i->x[i]^moduli[i]),[b^p]);
  for i in [1..p-1] do for j in [i+1..p-1] do if j<=p-1 then Add(rels,Comm(x[i],x[j]));fi;od;od;
  for i in [1..p-2] do Add(rels,Comm(x[i],b)*x[i+1]^-1);od;
  Add(rels,Comm(x[p-1],b)*Product([1..p-1],i->x[i]^Binomial(p,i)));
  U:=F/rels;Check248(Size(U)=p^m,"exact presented order");
  iso:=IsomorphismPermGroup(U);Check248(iso<>fail,"permutation isomorphism");P:=Image(iso);
  ss:=List(GeneratorsOfGroup(U){[1..p-1]},x->Image(iso,x));beta:=Image(iso,GeneratorsOfGroup(U)[p]);
  Check248(List(ss,Order)=moduli,"individual source orders");
  sigma:=GroupHomomorphismByImages(P,P,[ss[1],beta],[ss[1],beta^-1]);
  tau:=GroupHomomorphismByImages(P,P,[ss[1],beta],[ss[1]^-1,beta]);
  Check248(sigma<>fail and tau<>fail and IsBijective(sigma) and IsBijective(tau),"literal maps extend to automorphisms");
  K:=Group(sigma,tau);Check248(Size(K)=4,"Klein complement");
  G:=SemidirectProduct(K,P);a:=Embedding(G,1);z:=Embedding(G,2);
  rs:=[Image(z,ss[1])*Image(a,tau)*Image(a,sigma),Image(z,beta)*Image(a,tau)*Image(a,sigma),Image(a,sigma)];
  Check248(Size(Group(rs))=4*p^m and ForAll(rs,x->Order(x)=2),"marked generation");
  Check248([Order(rs[1]*rs[2]),Order(rs[2]*rs[3])]=[p,2*p],"exact type");
  Check248(Comm(rs[1],rs[3])=One(G) and IP248(rs),"all marked intersections");
  Print("LITERAL_PRESENTATION ",p," ",m," ORDER ",Size(U)," MODULI ",moduli," IP64 PASS\n");
 od;
 # The prime-index hypothesis is necessary: a composite-index subgroup can
 # meet another subgroup nontrivially without being contained in it.
 G:=ElementaryAbelianGroup(8);x:=GeneratorsOfGroup(G);P:=Group(x{[1,2]});K:=Group(x{[1,3]});
 Check248(Index(P,TrivialSubgroup(P))=4 and not IsSubgroup(K,P) and Size(Intersection(P,K))=2,"composite-index false weakening");
 Print("COMPOSITE_INDEX_FALSE_WEAKENING_REJECTED\nPHASE248_PRESENTATION_PASS\n");
end;;
Run248();
QUIT_GAP(0);
