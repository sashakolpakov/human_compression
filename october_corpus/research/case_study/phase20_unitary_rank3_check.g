# Exact finite certificates for the anti-isometric-endpoint template.
# The q=3 case is the separate finite base; larger fields corroborate the proof.
SizeScreen([4096,100000]);;
Check20:=function(q)
 local E,o,z,J,H,A,C,v,B,eta,t,bar,rr,M,plane,orb,hom,pp,G,expected,sets,subs,j,k,ok;
 E:=GF(q^2);o:=One(E);z:=Zero(E);eta:=Z(q^2)^((q-1)/2);t:=Z(q^2);bar:=m->List(m,row->List(row,x->x^q));
 Assert(0,Order(t)=q^2-1 and Size(Field([t^2]))=q^2 and eta^(q+1)=-o and Order(eta^2)=q+1);
 H:=[[z,o,z,z],[o,z,z,z],[z,z,z,-o],[z,z,-o,z]];
 A:=eta*[[z,z,o,z],[z,z,z,o],[o,z,z,z],[z,o,z,z]];C:=DiagonalMat([o,o,-o,-o]);
 v:=TransposedMat([[o,z,2/t,t^q/2]]);B:=IdentityMat(4,E)+v*TransposedMat(bar(v))*H;rr:=[A,B,C];
 Assert(0,ForAll(rr,g->TransposedMat(bar(g))*H*g=H));
 Assert(0,A*A=eta^2*IdentityMat(4,E) and B*B=IdentityMat(4,E) and C*C=IdentityMat(4,E) and A*C=-C*A);
 Assert(0,DeterminantMat(A)=eta^4 and DeterminantMat(B)=-o and DeterminantMat(C)=o);
 if q=3 then
  Assert(0,t^2=t+o and t^4=-o and t^3=o-t);
  Assert(0,B=[[o,o,t,-t],[z,o,z,z],[z,o-t,z,o],[z,t-o,o,z]]);
 fi;
 M:=Group(rr);plane:=[[o,z,z,z],[z,z,o,z]];orb:=Orbit(M,plane,OnSubspacesByCanonicalBasis);hom:=ActionHomomorphism(M,orb,OnSubspacesByCanonicalBasis);pp:=List(rr,g->Image(hom,g));G:=Group(pp);
 expected:=2*q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 sets:=Combinations([1..3]);subs:=List(sets,a->Subgroup(G,pp{a}));ok:=true;for j in [1..8] do for k in [1..8] do if Intersection(subs[j],subs[k])<>subs[Position(sets,Intersection(sets[j],sets[k]))] then ok:=false;fi;od;od;
 Assert(0,Size(G)=expected and Length(orb)=(q+1)*(q^3+1) and ok and ForAll(pp,g->Order(g)=2) and Order(pp[1]*pp[3])=2 and Order(pp[1]*pp[2])>2 and Order(pp[2]*pp[3])=2*Characteristic(E));
 Print("PASS q=",q," image_order=",Size(G)," expected=",expected," full=",Size(G)=expected," planes=",Length(orb)," type=",[Order(pp[1]*pp[2]),Order(pp[2]*pp[3])]," IP=",ok," involutions=",List(pp,Order)," endpoints=",Order(pp[1]*pp[3]),"\n");
end;;
for q in [3,5,7,9,11,13] do Check20(q);od;
Print("ALL PASS: 6 fields, 48 marked subgroup closures, 384 exact meets.\n");
QUIT;
