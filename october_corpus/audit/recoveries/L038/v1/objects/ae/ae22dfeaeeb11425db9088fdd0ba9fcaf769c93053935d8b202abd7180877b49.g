Read("model.g");
CertifyBasics:=function(s,t,n)
 local i,j;
 if ForAny(s,x->Order(x)<>2 or SignPerm(x)<>1) then Error("involution/parity");fi;
 for i in [1..Length(s)] do for j in [i+1..Length(s)] do
  if j>i+1 and s[i]*s[j]<>s[j]*s[i] then Error("string relation");fi;
 od;od;
 if List([1..Length(s)-1],i->Order(s[i]*s[i+1]))<>t then Error("type");fi;
 if not IsTransitive(Group(s),[1..n]) then Error("connectivity");fi;
end;
CertifyBasics(LowSix(15),[5,6,3,5,3],15);
CertifyBasics(EvenFive2(10),[5,5,6,5],10);
CertifyBasics(EvenFive0(12),[3,4,6,5],12);
CertifyBasics(EvenFour0(16),[3,12,24],16);

CertifyLowSix:=function()
 local s,K,C,A,all,I,J,H,N,Q,B,j,o,Y,hom,row,pairs;
 s:=LowSix(15);K:=Group(s{[2..6]});C:=[4..15];
 if Size(K)<>Factorial(12) then Error("wrong finite end order");fi;
 A:=Stabilizer(Stabilizer(K,2),3);
 if A<>AlternatingGroup(C) then Error("supported alternating subgroup missing");fi;
 Print("K order ",Size(K)," supported alternating order ",Size(A),"\n");
 all:=List([0..31],m->Filtered([1..5],i->QuoInt(m,2^(i-1)) mod 2=1));pairs:=0;
 for I in all do for J in all do
  H:=Group(Concatenation([()],s{List(I,i->i+1)}));N:=Group(Concatenation([()],s{List(J,i->i+1)}));
  Q:=Group(Concatenation([()],s{List(Intersection(I,J),i->i+1)}));
  if Intersection(H,N)<>Q then Error("finite end IP failure");fi;pairs:=pairs+1;
 od;od;
 Print("finite end IP ordered pairs ",pairs,"\n");
 for j in [2..5] do
  H:=Group(s{[1..j]});N:=Group(s{[2..j+1]});Q:=Group(s{[2..j]});
  B:=N;
  for o in Orbits(H,[1..15]) do B:=Stabilizer(B,Set(o),OnSets);od;
  Print("step ",j," partition bound ",Size(B));
  
  if j=5 then
   Y:=[9,11,12,14,15];hom:=ActionHomomorphism(B,Y,OnPoints);
   B:=PreImage(hom,Intersection(Image(hom),AlternatingGroup(5)));
  fi;
  if B<>Q then Error("finite partition/parity bound is not exact");fi;
  Print(" final bound ",Size(B)," = middle subgroup\n");
 od;
 Print("LOW_SIX_FINITE_REDUCTION_PASS\n");
end;
CertifyLowSix();

CertifyEven:=function(tag,s,core)
 local n,r,K,A,I,J,L,M,Q,H,B,j,o,all,pairs,w,F,cl,N;
 n:=LargestMovedPoint(Group(s));r:=Length(s);K:=Group(s{[2..r]});
 all:=List([0..2^(r-1)-1],m->Filtered([1..r-1],i->QuoInt(m,2^(i-1)) mod 2=1));pairs:=0;
 for I in all do for J in all do
  L:=Group(Concatenation([()],s{List(I,i->i+1)}));M:=Group(Concatenation([()],s{List(J,i->i+1)}));Q:=Group(Concatenation([()],s{List(Intersection(I,J),i->i+1)}));
  if Intersection(L,M)<>Q then Error("finite end IP failure");fi;pairs:=pairs+1;
 od;od;
 Print(tag," Korder ",Size(K)," finite IP pairs ",pairs,"\n");
 if tag<>"four0" then
  A:=K;for j in Difference([1..n],core) do A:=Stabilizer(A,j);od;
  if A<>AlternatingGroup(core) then Error("supported alternating group missing");fi;
  Print("supported alternating order ",Size(A)," core ",core,"\n");
 fi;
 for j in [2..r-1] do
  H:=Group(s{[1..j]});L:=Group(s{[2..j+1]});Q:=Group(s{[2..j]});B:=L;
  for o in Orbits(H,[1..n]) do B:=Stabilizer(B,Set(o),OnSets);od;
  Print("step ",j," orbit bound ",Size(B));
  if tag="five0" and j=3 then B:=Centralizer(Centralizer(B,(1,3)*(2,4)),(1,5)*(2,6));fi;
  if tag="five0" and j=4 then B:=Centralizer(B,(1,4)*(2,3));fi;
  if B<>Q then Error("upper bound mismatch");fi;
  Print(" final ",Size(B),"\n");
 od;
 if tag="four0" then
  F:=Reversed(s);w:=(F[2]*F[3]*F[4]*F[3])^12;
  if w<>(4,9,12,14,11) then Error("wrong pure word");fi;
  cl:=Orbit(K,w,OnPoints);N:=Group(cl);
  if N<>AlternatingGroup(core) then Error("pure word conjugates fail");fi;
  Print("pure word ",w," conjugates ",Length(cl)," alternating core order ",Size(N),"\n");
 fi;
 Print(tag,"_FINITE_REDUCTION_PASS\n");
end;
CertifyEven("five2",Reversed(EvenFive2(10)),[1..7]);
CertifyEven("five0",Reversed(EvenFive0(12)),[1..9]);
CertifyEven("four0",Reversed(EvenFour0(16)),Concatenation([1..6],[9..14]));

Print("ALL_FOUR_FINITE_CERTIFICATES_PASS\n");
QUIT;
