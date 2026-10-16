# Independent finite-field specialization of both Bruhat extraction maps.
# No author symbolic program or earlier Suzuki census is imported.
CheckBruhat := function(n)
 local F,z,o,zz,q,theta,inv,U,h,w,i,a,b,c,f,t,g,got,closed,opened,
       fieldTests,d,K,kl,tuple,original,j,allSmall,matrixSmall;
 F:=GF(2^n); z:=PrimitiveElement(F); o:=One(F); zz:=Zero(F); q:=Size(F);
 theta:=2^((n+1)/2); inv:=Gcdex(theta+1,q-1).coeff1 mod(q-1);
 if ((theta+1)*inv) mod(q-1)<>1 then Error("Power inverse"); fi;
 U:=function(a,b)
  return [[o,zz,zz,zz],[a,o,zz,zz],[a^(theta+1)+b,a^theta,o,zz],
   [a^(theta+2)+a*b+b^theta,b,a,o]];
 end;
 h:=t->DiagonalMat([t^(theta+1),t,t^-1,t^(-theta-1)]);
 w:=NullMat(4,4,F);
 for i in [1..4] do w[i,5-i]:=o; od;
 closed:=0; opened:=0; fieldTests:=0;
 for i in [0..63] do
  a:=z^i; b:=z^(2*i+1); c:=z^(3*i+2); f:=z^(5*i+3); t:=z^(7*i+4);
  if i mod 3=0 then a:=zz; fi;
  if i mod 5=0 then b:=zz; fi;
  if i mod 7=0 then c:=zz; fi;
  if i mod 11=0 then f:=zz; fi;
  g:=U(a,b)*h(t);
  got:=[g[2][1]/g[1][1],g[4][2]/g[2][2],g[2][2]];
  if g[1][4]<>zz or got<>[a,b,t] then Error("Closed Bruhat extraction"); fi;
  closed:=closed+1;
  g:=g*w*U(c,f);
  got:=[g[2][4]/g[1][4],g[3][4]/g[1][4]+(g[2][4]/g[1][4])^(theta+1),
        g[1][4]^inv,g[1][3]/g[1][4],g[1][2]/g[1][4]];
  if g[1][4]=zz or got<>[a,b,t,c,f] then Error("Open Bruhat extraction"); fi;
  opened:=opened+1;
 od;
 for d in DivisorsInt(n) do
  K:=GF(2^d); kl:=AsList(K);
  for i in [1..16] do
   original:=[kl[(i mod Length(kl))+1],kl[((2*i) mod Length(kl))+1],
       PrimitiveElement(K),kl[((3*i) mod Length(kl))+1],kl[((5*i) mod Length(kl))+1]];
   for j in [0..5] do
    tuple:=ShallowCopy(original);
    if j>0 then tuple[j]:=z; fi;
    a:=tuple[1]; b:=tuple[2]; t:=tuple[3]; c:=tuple[4]; f:=tuple[5];
    allSmall:=ForAll(tuple,x->x^(2^d)=x);
    g:=U(a,b)*h(t)*w*U(c,f);
    matrixSmall:=ForAll(g,row->ForAll(row,x->x^(2^d)=x));
    if allSmall<>matrixSmall then Error("Actual subfield membership equivalence"); fi;
    fieldTests:=fieldTests+1;
   od;
  od;
 od;
 Print("BRUHAT_FIELD ",n," closed=",closed," open=",opened," field_tests=",fieldTests,"\n");
end;
for n in [3,5,9,15] do CheckBruhat(n); od;
Print("PASS_INDEPENDENT_L110_BRUHAT\n");
QUIT_GAP(0);
