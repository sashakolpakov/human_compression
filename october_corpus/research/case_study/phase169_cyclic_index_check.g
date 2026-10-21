# Literal source presentations, independently of the coordinate implementation.
# These bounded checks do not replace the uniform collecting proof.
Require169 := function(test, message)
  if not test then Error(message); fi;
end;

Check169 := function(M, epsilon, expectedOrder, expectedCenter)
  local F,a,b,c,P,p,q,rho,Q,rels,G,K,g,k,forward,backward,x,z;
  F:=FreeGroup("a","b","c"); a:=F.1; b:=F.2; c:=F.3;
  rels:=[a^2,b^2,c^2,(a*c)^2,(a*b)^4,(b*c)^M,
         (a*b*c*b)^2*(c*b)^(epsilon*M/2)];
  G:=F/rels; g:=GeneratorsOfGroup(G);
  Require169(Size(G)=expectedOrder,"Wrong literal Coxeter presentation order");
  Require169(Exponent(G)=M,"Wrong literal exponent");
  Require169(Size(Center(G))=expectedCenter,"Wrong literal center");

  P:=FreeGroup("p","q","rho");p:=P.1;q:=P.2;rho:=P.3;
  Q:=[p^M,q^4,rho^2,
      (p^q)*(q^2*p^-1)^-1,
      (p^(q^2))*p^(-1-epsilon*M/2),
      (p^rho)*(q^2*p)^-1,
      (q^rho)*q];
  K:=P/Q;k:=GeneratorsOfGroup(K);
  Require169(Size(K)=expectedOrder,"Wrong literal original presentation order");
  forward:=GroupHomomorphismByImages(K,G,k,[g[2]*g[3],g[1]*g[2],g[1]]);
  backward:=GroupHomomorphismByImages(G,K,g,[k[3],k[2]^-1*k[3],k[1]^-1*k[2]^-1*k[3]]);
  Require169(forward<>fail and backward<>fail,"Presentation substitution not homomorphic");
  Require169(IsBijective(forward) and IsBijective(backward),"Presentation substitution not bijective");
  Require169(ForAll(g,t->Image(forward,Image(backward,t))=t),"Wrong generator inverse on G");
  Require169(ForAll(k,t->Image(backward,Image(forward,t))=t),"Wrong generator inverse on K");
  x:=(g[1]*g[2])^2;z:=(g[2]*g[3])^(M/2);
  Require169(Comm(x,g[3])=z^epsilon,"Marked commutator parameter mismatch");
  Print("CASE ",M," EPS ",epsilon," ORDER ",Size(G)," EXP ",Exponent(G),
        " CENTER ",Size(Center(G))," BOTH_PRESENTATIONS_AND_INVERSES PASS\n");
end;

for M in [4,8,16,32] do
  Check169(M,0,8*M,4);
  if M>=8 then Check169(M,1,8*M,2);fi;
od;

# The excluded M=4,epsilon=1 presentation really collapses; it cannot be
# admitted as the second order-32/type-{4,4} family.
F:=FreeGroup("a","b","c");a:=F.1;b:=F.2;c:=F.3;
Bad:=F/[a^2,b^2,c^2,(a*c)^2,(a*b)^4,(b*c)^4,(a*b*c*b)^2*(c*b)^2];
Require169(Size(Bad)=16,"Bad boundary did not collapse to order16");
bg:=GeneratorsOfGroup(Bad);
Require169(Order(bg[2]*bg[3])=2,"Bad boundary retained order4");
Print("NEGATIVE M 4 EPS 1 ORDER 16 RIGHT_ORDER 2 PASS\n");
Print("PHASE169_LITERAL_PRESENTATIONS_PASS\n");
QUIT;
