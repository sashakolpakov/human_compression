# Actual marked finite models and all intersection identities.
Read("programs/ambient_marking.g");;
Need:=CheckL084;;
IP:=function(r)
 local sets,pars,i,j;
 sets:=Combinations([1..Length(r)]);pars:=List(sets,s->Group(Concatenation([One(r[1])],r{s})));
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  Need(Intersection(pars[i],pars[j])=pars[Position(sets,Intersection(sets[i],sets[j]))],"full intersection property");
 od;od;
 return Length(sets)^2;
end;;
jIP:=IP(jmarks);;pIP:=IP(pmarks);;wIP:=IP(marks);;
for r in [jmarks,pmarks,marks] do
 Need(ForAll(r,x->Order(x)=2) and List([1..3],i->Order(r[i]*r[i+1]))=[5,3,5],"exact marker and adjacent orders in each quotient");
 Need(ForAll([[1,3],[1,4],[2,4]],ij->Comm(r[ij[1]],r[ij[2]])=One(r[1])),"all string commutators in each quotient");
 Need((r[2]*r[3]*r[4])^5=One(r[1]),"hemi relation in each quotient");
od;
Need(IsSimpleGroup(G) and IsSimpleGroup(P),"two actual simple factors");
iso:=IsomorphismGroups(P,PSL(2,19));;Need(iso<>fail,"named PSL identification");
jo:=(jmarks[1]*jmarks[2]*jmarks[3])^5;;jn:=jo*jmarks[4];;
po:=(pmarks[1]*pmarks[2]*pmarks[3])^5;;pn:=po*pmarks[4];;
Need(Order(jo)=2 and Order(jn)=3 and Order(po)=1 and Order(pn)=2,"exact quotient normal words");
Need(NormalClosure(G,Group(jo))=G and NormalClosure(P,Group(pn^3))=P,"full normal closures in factors");
Need(List([jmarks,pmarks],r->List([[1,2,3],[2,3,4]],s->Size(Group(r{s}))))=[[120,60],[60,60]],"local orders");
jd:=Group(jmarks{[1,2,3]});;ji:=Group(jmarks{[2,3,4]});;
Need(IsomorphismGroups(jd,DirectProduct(CyclicGroup(2),AlternatingGroup(5)))<>fail and IsomorphismGroups(ji,AlternatingGroup(5))<>fail,"named endpoint groups");
# Exact source prime-order words, each tested in the endpoint product.
jwords:=[jmarks[2]*jmarks[3],jmarks[1]*jmarks[2],
 jmarks[4]*jmarks[2]*jmarks[3]*jmarks[2]*jmarks[1],
 jmarks[4]*jmarks[3]*jmarks[2]*jmarks[1]*jmarks[2]*jmarks[1],
 jmarks[2]*jmarks[4]*jmarks[3]*jmarks[2]*jmarks[4]*jmarks[1]*jmarks[2]*jmarks[1]*jmarks[3]*jmarks[2]*jmarks[1]];;
jproduct:=Set(Concatenation(List(Elements(ji),a->List(Elements(jd),b->a*b))));;
Need(List(jwords,Order)=[3,5,19,11,7] and ForAll(jwords,x->x in jproduct),"all five literal prime witnesses");
Need(Length(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2))=1,"unique Janko involution class");
Need(ForAll([3,5,7,11,19],p->Size(SylowSubgroup(G,p))=p),"odd Sylow groups have prime order");
# A second direct finite check: every nonidentity subgroup has an order-p
# subgroup conjugate to one meeting the forbidden endpoint product.
PrimeObstruction:=function(k,r,allowed)
 local product,primes,p,cl,subs,rep,z,hit,out;
 product:=Set(Concatenation(List(Elements(Group(r{[2,3,4]})),a->List(Elements(Group(r{[1,2,3]})),b->a*b))));
 primes:=Set(FactorsInt(Size(k)));out:=[];
 for p in primes do
  subs:=[];
  for cl in ConjugacyClasses(k) do
   z:=Representative(cl);if Order(z)<>p then continue;fi;
   rep:=Group(z);
   if ForAny(subs,h->IsConjugate(k,h,rep)) then continue;fi;
   Add(subs,rep);
   hit:=First(Difference(product,allowed),b->Order(b)=p and IsConjugate(k,rep,Group(b)));
   Need(hit<>fail,"prime subgroup misses forbidden endpoint product");
  od;
  Add(out,[p,Length(subs)]);
 od;
 return out;
end;;
jobs:=PrimeObstruction(G,jmarks,[One(G),jo]);;
pobs:=PrimeObstruction(P,pmarks,[One(P)]);;
# Reversal of the four exact PSL markers extends to the duality automorphism.
dual:=GroupHomomorphismByImages(P,P,pmarks,Reversed(pmarks));;
Need(dual<>fail and IsBijective(dual),"marked self-duality of the 57-cell");
Need(Size(G)/120=1463 and Size(G)/60=2926 and Size(P)/60=57,"exact source face counts");
Need(Order(om*marks[4])=6,"exact nu order six");
reps:=[[],[1],[2],[4],[1,2],[1,3],[1,4],[2,4],[4,3],[1,2,1],
 [1,2,3],[1,2,4],[1,3,2],[1,3,4],[1,4,3],[2,4,3],[4,3,2],
 [4,3,4],[1,2,1,3],[1,4,3,4]];;
Need(List(reps,w->1^Product(Concatenation([One(P)],pmarks{w})))=[1..20],"all twenty literal coset representatives");
us:=[marks[3]*marks[2],(marks[1]*marks[2])^2*marks[3]*marks[4]*marks[1],
 marks[1]*marks[2]*marks[1]*marks[4]*marks[3]*marks[4]*marks[2]];;
Need(Size(Group(us))=30020760 and Order(us[2]^-1*us[3]*us[1])=171,"actual index-twenty subgroup and cyclic image");
PrintTo("geometry_summary.json",[jIP,pIP,wIP,jobs,pobs,1463,2926,57,6],"\n");
Print("L095_GEOMETRY_PASS 768 IP identities; two prime obstructions; marked duality\n");
QUIT;
