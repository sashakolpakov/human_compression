SizeScreen([1000000,1000000]);;
Need:=function(b,s) if not b then Error(s);fi;end;;
ActualControls:=function()
 local q,m,sg,G,iso,P,cc,t,I,B,C,omega,nu,found,E,F,k,z,basis,mat,c,v,p,nonalt,total,expected;
 total:=0;
 for p in [[2,3],[4,2]] do
  q:=p[1];m:=p[2];
  for sg in [-1,1] do
   G:=GO(sg,2*m,q);I:=IdentityMat(2*m,GF(q));
   B:=InvariantBilinearForm(G).matrix;
   iso:=IsomorphismPermGroup(G);P:=Image(iso);found:=0;
   for cc in ConjugacyClasses(P) do
    if Order(Representative(cc))=2 then
     t:=PreImagesRepresentative(iso,Representative(cc));
     nonalt:=ForAny([1..2*m],i->(B*TransposedMat(t))[i][i]<>Zero(GF(q)));
     if RankMat(t-I)=m and nonalt then
      C:=List(Elements(Centralizer(P,Representative(cc))),g->PreImagesRepresentative(iso,g));
      omega:=Filtered(C,g->RankMat(g-I) mod 2=0);
      nu:=Number(omega,g->g*g=I);found:=found+1;
      if m=3 then expected:=48;Need(nu=20,"actual rank-three involutions");
      else expected:=16;Need(nu=16,"actual rank-two involutions");fi;
      Need(Length(C)=2*expected and Length(omega)=expected,"actual orthogonal centralizer");
      Print("ACTUAL|",q,"|",m,"|",sg,"|",Length(C),"|",Length(omega),"|",nu,"\n");
     fi;
    fi;
   od;
   Need(found=1,"unique full-rank nonalternating class");total:=total+1;
  od;
 od;
 for p in [[2,1],[2,2],[2,3],[2,4],[4,1],[4,2],[4,3]] do
  q:=p[1];k:=p[2];E:=GF(q^(2*k));F:=GF(q);
  basis:=Basis(AsVectorSpace(F,E));z:=Z(q^(2*k))^(q^k-1);
  for c in List([0..q^k],i->z^i) do
   mat:=List(BasisVectors(basis),v->Coefficients(basis,c*v^(q^k)));
   Need(mat*mat=IdentityMat(2*k,F) and RankMat(mat-IdentityMat(2*k,F))=k,"trace inverter rank");
   nonalt:=false;
   for v in BasisVectors(basis) do
    Need(Trace(E,F,c^(q^k)*v^2)=Trace(GF(q^k),F,v*c^(q^k)*v+c*v^(2*q^k)),"literal polar trace identity");
    if Trace(E,F,c^(q^k)*v^2)<>Zero(F) then nonalt:=true;fi;
   od;
   Need(nonalt,"nonalternating full-rank inverter");
  od;
  Print("TRACE|",q,"|",k,"|",q^k+1,"\n");total:=total+1;
 od;
 Need(total=11,"complete controls");Print("COMPLETE_EVEN_FIXED_CONTROLS\n");
end;;
ActualControls();;
QUIT;
