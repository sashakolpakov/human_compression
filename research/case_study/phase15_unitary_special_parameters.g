# Small generic-b exceptions and two norm-curve exceptions; exact matrix powers only.
SizeScreen([4096,100000]);;
Projective15:=function(M)local o,r,I;o:=Order(M);I:=IdentityMat(Length(M),Field(Flat(M)));for r in DivisorsInt(o) do if M^r=(M^r)[1][1]*I then return r;fi;od;Error("unreachable");end;;
Run15:=function(q,ae,be,target)
 local E,g,i,a,b,c,t,x,y,o,z,R,S,Zz,r1,r2,T,ord,p,poly,basis,co,genorders,j;
 E:=GF(q*q);g:=Z(q*q);o:=One(E);z:=Zero(E);i:=g^((q*q-1)/4);a:=g^ae;b:=g^be;c:=-b^q;
 t:=a/i;x:=(b+b^q)/2;y:=(b-b^q)/(2*i);
 Assert(0,t^q=t and x^q=x and y^q=y and t^2+x^2+y^2=o and t*x*y<>z and t*t+2*y+2<>z);
 R:=[[z,i],[i,z]];S:=[[a,b],[c,-a]];Zz:=[[o,z],[z,-o]];
 genorders:=List([Zz*S,R*S,Zz*R*S],Projective15);Assert(0,Maximum(genorders)>5);
 r1:=[[o,z,z,z],[z,z,z,o],[z,z,-o,z],[z,o,z,z]];
 r2:=[[z,i,z,z],[i,z,z,z],[z,z,a,b],[z,z,c,-a]];T:=r1*r2;
 ord:=Projective15(T);Assert(0,ord=target and ord in [(q*q-1)/2,(q*q+1)/2]);
 Assert(0,T^(4*target)=IdentityMat(4,E));
 for p in Set(FactorsInt(target)) do Assert(0,T^(target/p)<>(T^(target/p))[1][1]*IdentityMat(4,E));od;
 basis:=Basis(E,[o,i]);co:=v->List(Coefficients(basis,v),IntFFE);
 Print("PARAMETER ",[q,IntFFE(t),IntFFE(x),IntFFE(y),target,genorders,co(a),co(b)],"\n");
 Print("PASS q=",q," h=",IntFFE(t*t+2*y+2),"\n");
end;;
Run15(19,150,5,181);
Run15(23,156,11,265);
Run15(43,594,1,924);
Print("ALL PASS: three special complete parameter choices.\n");
QUIT;
