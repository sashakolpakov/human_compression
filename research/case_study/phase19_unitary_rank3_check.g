# Exact finite diagnostics for the new rank-three template. No uniform inference.
SizeScreen([4096,100000]);;
Run19:=function(q,boundary)
 local F,o,z,zeta,s,H,A,B,C,v,bar,rr,M,plane,orb,hom,pp,G,expected,multiple,sets,subs,j,k,start;
 start:=Runtime();F:=GF(q^2);o:=One(F);z:=Zero(F);zeta:=Z(q^2)^((q+1)/2);
 if boundary then zeta:=Z(q^2)^((q^2-1)/4);fi;
 s:=-zeta*zeta;Assert(0,zeta^q=-zeta and Size(Field([s]))=q and s<>z and s<>-o);
 H:=DiagonalMat([o,-o,o,-o]);A:=DiagonalMat([o,o,-o,-o]);C:=[[z,z,o,z],[z,z,z,o],[o,z,z,z],[z,o,z,z]];
 v:=TransposedMat([[zeta,-o,s-zeta,s+o]]);bar:=m->List(m,row->List(row,x->x^q));B:=IdentityMat(4,F)+v*TransposedMat(bar(v))*H;rr:=[A,B,C];
 Assert(0,ForAll(rr,g->g*g=IdentityMat(4,F) and TransposedMat(bar(g))*H*g=H));
 M:=Group(rr);plane:=[[o,o,z,z],[z,z,o,o]];orb:=Orbit(M,plane,OnSubspacesByCanonicalBasis);Assert(0,Length(orb)=(q+1)*(q^3+1));
 hom:=ActionHomomorphism(M,orb,OnSubspacesByCanonicalBasis);pp:=List(rr,g->Image(hom,g));G:=Group(pp);
 multiple:=2;if q mod 8=7 then multiple:=1;fi;
 expected:=multiple*q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 Assert(0,Size(G)=expected and ForAll(pp,g->Order(g)=2) and Comm(pp[1],pp[3])=() and Order(pp[1]*pp[2])>2 and Order(pp[2]*pp[3])=2*Characteristic(F));
 sets:=Combinations([1..3]);subs:=List(sets,a->Subgroup(G,pp{a}));
 for j in [1..8] do for k in [1..8] do Assert(0,Intersection(subs[j],subs[k])=subs[Position(sets,Intersection(sets[j],sets[k]))]);od;od;
 Print("PASS q=",q," boundary=",boundary," z=",zeta," s=",s," order=",Size(G)," socle_index=",multiple," type=",[Order(pp[1]*pp[2]),Order(pp[2]*pp[3])]," planes=",Length(orb)," groups=8 meets=64 runtime_ms=",Runtime()-start,"\n");
end;;
for q in [5,7,9,11,13] do Run19(q,false);od;
Run19(7,true);
Print("ALL PASS:6markings,48subgroups,384exactmeets.\n");
QUIT;
