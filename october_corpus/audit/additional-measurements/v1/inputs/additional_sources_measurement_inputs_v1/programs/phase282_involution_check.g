Need:=function(ok,msg) if not ok then Error("PHASE282_REJECT ",msg);fi;end;;
for family in ["PSL","PSU"] do
 for q in [2,3,4,5] do
  if family="PSL" then
   G:=PSL(3,q); ord:=q^3*(q^3-1)*(q^2-1)/Gcd(3,q-1);
   if IsOddInt(q) then inv:=q^2*(q^2+q+1);else inv:=(q^3-1)*(q+1);fi;
  else
   G:=PSU(3,q);ord:=q^3*(q^3+1)*(q^2-1)/Gcd(3,q+1);
   if IsOddInt(q) then inv:=q^2*(q^2-q+1);else inv:=(q^3+1)*(q-1);fi;
  fi;
  actual:=Sum(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Size);
  Need(Size(G)=ord,"classical group order");Need(actual=inv,"classical involution count");
  Print("PHASE282_CLASSICAL_PASS ",family," ",q," order ",ord," involutions ",actual,"\n");
 od;
od;
for n in [5..10] do
 for family in ["Alt","Sym"] do
  if family="Alt" then G:=AlternatingGroup(n);else G:=SymmetricGroup(n);fi;
  inv:=Sum(Filtered([1..QuoInt(n,2)],k->family="Sym" or IsEvenInt(k)),
     k->Factorial(n)/(2^k*Factorial(k)*Factorial(n-2*k)));
  actual:=Sum(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Size);
  Need(actual=inv,"permutation involution count");
  Print("PHASE282_PERMUTATION_PASS ",family," ",n," involutions ",actual,"\n");
 od;
od;
Print("PHASE282_ALL_TWENTY_COUNTS_PASS\n");
QUIT;
