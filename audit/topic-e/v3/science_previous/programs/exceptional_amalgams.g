# Exact finite premises for the exceptional rotation-end classification.
# Uses GAP's finite-presentation and subgroup algorithms. No random search.
Need:=function(b,m) if not b then Error(m);fi;end;
Base:=function(typ)
 local F,x,rel;
 F:=FreeGroup("a","b","c");x:=GeneratorsOfGroup(F);
 rel:=[x[1]^typ[1],x[2]^typ[2],x[3]^typ[3],(x[1]*x[2])^2,(x[2]*x[3])^2,Product(x)^2];
 return [F,x,rel];
end;
Run:=function()
 local G,ps,a,b,c,au,rem,orb,types,pair,typ,base,F,x,rel,t1,t2,t3,t4,k,j,i,l,ord,orders,expected,rels,U,iso,P,cf,n,ss,hs,As,chosen,rt,lt;
 for G in [AlternatingGroup(4),SymmetricGroup(4),AlternatingGroup(5)] do
  ps:=[];
  for a in Elements(G) do for b in Elements(G) do
   if Order(a)>2 and Order(b)>2 and Order(a*b)=2 and Group(a,b)=G and Size(Intersection(Group(a),Group(b)))=1 then Add(ps,[a,b]);fi;
  od;od;
  au:=AutomorphismGroup(G);rem:=ShallowCopy(ps);types:=[];
  while Length(rem)>0 do
   pair:=rem[1];orb:=Orbit(au,pair,OnTuples);Add(types,List(pair,Order));rem:=Filtered(rem,z->not z in orb);
  od;
  if Size(G)=12 then expected:=[[3,3]];n:=24;elif Size(G)=24 then expected:=[[3,4],[4,3]];n:=48;else expected:=[[3,5],[5,3],[5,5]];n:=360;fi;
  Need(Set(types)=Set(expected) and Length(ps)=n,"complete local pair census");
  if Size(G)=60 then
   for pair in ps do
    a:=pair[1];b:=pair[2];
    if List(pair,Order)=[5,5] then Need(a*b^2*a^3*b^2*a^2=One(G),"complete five-five local relator");fi;
    if Order(b) in [3,5] and Order(a)<>Order(b) then
     t1:=a*b^2*a^2*b^2*a^2;
     Need(Order(t1)=2 and b^t1=b^-1,"literal dihedral normalizer word");
     Need(Normalizer(G,Group(b))=Group(b,t1),"complete cyclic normalizer");
    fi;
    if List(pair,Order)=[5,3] then
     t1:=a^2*b^-1*a;t2:=a*b^-1*a^2;
     Need(Order(t1*b)=2 and Order(t2*b)=2,"A4 word involutions");
     As:=Filtered(AllSubgroups(G),H->Size(H)=12 and IsSubgroup(H,Group(b)));
     Need(Length(As)=2 and Set([Group(t1,b),Group(t2,b)])=Set(As),"both A4 overgroups");
     for chosen in [t1,t2] do Need(Set(List([0..2],k->(chosen*b)^(b^k)))=Set(Filtered(Elements(Group(chosen,b)),z->Order(z)=2)),"three A4 involutions by beta");od;
    fi;
   od;
  fi;
  Print("LOCAL_PAIRS ",Size(G)," ",Length(ps)," ",types," PASS\n");
 od;
 for pair in [[[3,3,3],60],[[3,3,4],192],[[3,4,3],576],[[3,3,5],7200]] do
  base:=Base(pair[1]);U:=base[1]/base[3];Need(Size(U)=pair[2],"spherical rotation order");
  iso:=IsomorphismPermGroup(U);P:=Image(iso);cf:=List(CompositionSeries(P),Size);
  Need(ForAll([1..Length(cf)-1],k->cf[k]/cf[k+1] in [2,3,60]),"spherical simple factors");
  Print("SPHERICAL ",pair[1]," ORDER ",Size(P)," SERIES ",cf,"\n");
 od;
 # Source exclusion of the remaining five-five types. Full presentation, not quotient sampling.
 for typ in [[5,5,3],[5,5,5]] do
  base:=Base(typ);F:=base[1];x:=base[2];rel:=ShallowCopy(base[3]);a:=x[1];b:=x[2];c:=x[3];
  Add(rel,a*b^2*a^3*b^2*a^2);
  if typ[3]=5 then Add(rel,b*c^2*b^3*c^2*b^2);fi;
  U:=F/rel;Need(Size(U)=7200,"five-five universal order");iso:=IsomorphismPermGroup(U);P:=Image(iso);
  cf:=List(CompositionSeries(P),Size);Need(Set(Factors(Size(P)))=[2,3,5],"five-five order primes");
  Need(ForAll([1..Length(cf)-1],k->cf[k]/cf[k+1] in [2,60]),"five-five simple factors C2,A5");
  Print("FIVE_FIVE ",typ," ORDER ",Size(P)," SERIES ",cf,"\n");
 od;
 for typ in [[5,3,4],[5,3,5],[3,5,3]] do
  base:=Base(typ);F:=base[1];x:=base[2];a:=x[1];b:=x[2];c:=x[3];
  t1:=a*b^2*a^2*b^2*a^2;
  if typ[3]=4 then t2:=c*b^2*c^2;expected:=[60,1,1];
  elif typ[2]=3 then t2:=c*b^2*c^2*b^2*c^2;expected:=[3420,60,60];
  else t2:=c*b^2*c^2*b^2*c^2;expected:=[660,1,360,360,1];fi;
  orders:=[];
  for k in [1..typ[2]] do
   rel:=Concatenation(base[3],[t2/(t1*b^k)]);U:=F/rel;ord:=Size(U);Add(orders,ord);Need(ord=expected[k],"dihedral collision universal order");
   if ord>2 then
    iso:=IsomorphismPermGroup(U);P:=Image(iso);
    if ord=60 then G:=AlternatingGroup(5);elif ord=360 then G:=PSL(2,9);elif ord=660 then G:=PSL(2,11);else G:=PSL(2,19);fi;
    Need(IsomorphismGroups(P,G)<>fail,"dihedral collision group identification");
   fi;
  od;
  Print("DIHEDRAL_COLLISION ",typ," ORDERS ",orders,"\n");
  if typ[2]=3 then
   t1:=a^2*b^-1*a;t2:=a*b^-1*a^2;
   if typ[3]=4 then rt:=[b^2*c^2];expected:=[2,2,2,2,2,2];else rt:=[c^2*b^-1*c,c*b^-1*c^2];expected:=[1,1,1,1,60,60,60,1,60,1,1,1];fi;
   orders:=[];
   for lt in [t1,t2] do for t3 in rt do for j in [0..2] do
    rel:=Concatenation(base[3],[lt^(b^j)/t3]);U:=F/rel;ord:=Size(U);Add(orders,ord);Need(ord=expected[Length(orders)],"A4 collision universal order");
    if ord=60 then iso:=IsomorphismPermGroup(U);Need(IsomorphismGroups(Image(iso),AlternatingGroup(5))<>fail,"A4 collision quotient A5");fi;
   od;od;od;
   Need(orders=expected,"complete A4 collision table");Print("A4_COLLISION ",typ," ORDERS ",orders,"\n");
  fi;
 od;
 G:=AlternatingGroup(5);a:=(1,2,3,4,5);b:=(2,5,3);
 Need(Order(a*b)=2,"fixed A5 seed");
 hs:=Filtered(AllSubgroups(G),H->IsSubgroup(H,Group(b)));
 Need(Set(List(hs,Size))=[3,6,12,60],"all A5 C3 overgroup sizes");
 ps:=Filtered(Elements(G),c->Order(c)=5 and Order(b*c)=2 and Order(a*b*c)=2);
 Need(Length(ps)=2 and ForAll(ps,c->not IsConjugate(G,a,c)),"mixed-class extensions lie in A5");
 a:=(3,4,5);b:=(1,3,5,2,4);
 hs:=Filtered(AllSubgroups(G),H->IsSubgroup(H,Group(b)));
 Need(Set(List(hs,Size))=[5,10,60],"all A5 C5 overgroup sizes");
 Need(IsEmpty(Filtered(Elements(G),c->Order(c)=3 and Order(b*c)=2 and Order(a*b*c)=2)),"no 353 extension inside A5");
 G:=SymmetricGroup(4);b:=(2,3,4);c:=(1,2,4,3);
 Need(Order(b*c)=2 and Group(b,c)=G,"fixed S4 seed");
 t2:=c*b^2*c^2;t3:=b^2*c^2;
 Need(Order(t2)=2 and b^t2=b^-1 and Normalizer(G,Group(b))=Group(b,t2),"S4 normalizer word");
 Need(Order(t3*b)=2 and Group(b,t3)=AlternatingGroup(4),"S4 A4 word");
 Print("EXCEPTIONAL_AMALGAMS_PASS\n");
end;
Run();QUIT;
