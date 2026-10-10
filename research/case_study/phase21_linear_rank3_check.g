# Exact diagnostics for the nonsquare-endpoint linear rank-three template.
SizeScreen([4096,100000]);;
Check21:=function(q)
 local F,z,o,nu,I,A,B,C,v,phi,rr,M,orb,hom,pp,G,expected,sets,subs,j,k,ok,U,V,P,blocks,D1,D2;
 F:=GF(q);o:=One(F);z:=Zero(F);nu:=Z(q);I:=IdentityMat(4,F);
 A:=[[z,z,o,z],[z,z,z,o],[nu,z,z,z],[z,nu,z,z]];
 C:=DiagonalMat([o,o,-o,-o]);v:=TransposedMat([[o,z,z,o]]);phi:=[[z,o,o,o]];B:=I-2*v*phi;rr:=[A,B,C];
 Assert(0,Order(nu)=q-1 and A*A=nu*I and B*B=I and C*C=I and A*C=-C*A);
 Assert(0,DeterminantMat(A)=nu^2 and DeterminantMat(B)=-o and DeterminantMat(C)=o);
 U:=(B*C)^2;V:=A*U*A^-1;P:=I{[1,3,2,4]};
 blocks:=List([U,V],g->P*g*P^-1);
 D1:=Group(List(blocks,g->g{[1,2]}{[1,2]}));D2:=Group(List(blocks,g->g{[3,4]}{[3,4]}));
 Assert(0,Size(D1)=q*(q^2-1) and Size(D2)=q*(q^2-1));
 Assert(0,(U-I)^2<>0*I and (U-I)^3=0*I);
 M:=Group(rr);orb:=Orbit(M,[o,z,z,z],OnLines);hom:=ActionHomomorphism(M,orb,OnLines);pp:=List(rr,g->Image(hom,g));G:=Group(pp);
 expected:=2*q^6*(q^2-1)*(q^3-1)*(q^4-1)/Gcd(4,q-1);
 sets:=Combinations([1..3]);subs:=List(sets,a->Subgroup(G,pp{a}));ok:=true;
 for j in [1..8] do for k in [1..8] do if Intersection(subs[j],subs[k])<>subs[Position(sets,Intersection(sets[j],sets[k]))] then ok:=false;fi;od;od;
 Assert(0,Size(G)=expected and Length(orb)=(q^4-1)/(q-1) and ok and ForAll(pp,g->Order(g)=2) and Order(pp[1]*pp[3])=2 and Order(pp[1]*pp[2])>2 and Order(pp[2]*pp[3])=2*Characteristic(F));
 Print("PASS q=",q," group_order=",Size(G)," expected=",expected," points=",Length(orb)," type=",[Order(pp[1]*pp[2]),Order(pp[2]*pp[3])]," rankone_orders=",[Size(D1),Size(D2)]," IP=",ok,"\n");
end;;
for q in [5,7,9,13,17,25] do Check21(q);od;
Print("ALL PASS: 6 fields, 48 marked subgroup closures, 384 exact meets.\n");
QUIT;
