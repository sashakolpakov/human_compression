# Exact natural-action certificate for the unitary diagonal template.
SizeScreen([4096,100000]);;
Test17:=function(q)
 local F,o,z,ii,k,r0,r1,r2,r3,rr,H,bar,M,v,plane,orb,hom,pp,G,expected,fac,vert,mid,lambda,sets,subs,j,l;
 F:=GF(q^2);o:=One(F);z:=Zero(F);ii:=Z(q)^((q-1)/4);lambda:=Z(q^2)^(q-1);k:=lambda-lambda^-1;Assert(0,Order(lambda)=q+1 and k^q=-k and Size(Field([k*k]))=q);
 r0:=DiagonalMat([o,o,-o,-o]);r1:=[[o,z,z,z],[z,z,z,o],[z,z,o,z],[z,o,z,z]];
 r2:=[[z,ii,z,z],[ii,z,z,z],[z,z,k,ii-k],[z,z,ii+k,-k]];
 r3:=[[z,z,o,z],[z,z,z,o],[o,z,z,z],[z,o,z,z]];rr:=[r0,r1,r2,r3];H:=DiagonalMat([o,-o,o,-o]);
 bar:=m->List(m,row->List(row,t->t^q));Assert(0,ForAll(rr,r->r*H*TransposedMat(bar(r))=H));
 M:=Group(rr);plane:=[[o,o,z,z],[z,z,o,o]];orb:=Orbit(M,plane,OnSubspacesByCanonicalBasis);
 Assert(0,Length(orb)=(q+1)*(q^3+1));hom:=ActionHomomorphism(M,orb,OnSubspacesByCanonicalBasis);pp:=List(rr,r->Image(hom,r));G:=Group(pp);
 expected:=2*q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 Assert(0,ForAll(pp,g->Order(g)=2));
 for j in [1..4] do for l in [1..4] do if AbsInt(j-l)>1 then Assert(0,Comm(pp[j],pp[l])=());fi;od;od;
 fac:=Group(pp{[1..3]});vert:=Group(pp{[2..4]});mid:=Group(pp{[2,3]});
 Assert(0,Size(G)=expected and List([1..3],j->Order(pp[j]*pp[j+1]))=[4,2*(q+1),2*Characteristic(F)]);
 sets:=Combinations([1..4]);subs:=List(sets,s->Subgroup(G,pp{s}));
 for j in [1..16] do for l in [1..16] do Assert(0,Intersection(subs[j],subs[l])=subs[Position(sets,Intersection(sets[j],sets[l]))]);od;od;
 Print("PASS q=",q," actual=",Size(G)," expected=",expected," types=",List([1..3],j->Order(pp[j]*pp[j+1]))," facets=",Size(fac)," vertex=",Size(vert)," actualmeet=",Size(Intersection(fac,vert))," targetmeet=",Size(mid)," full_groups=16 full_meets=256\n");
end;;
for q in [5,9,13,17] do Test17(q);od;
Print("ALL PASS:4fields,64subgroups,1024exactintersections.\n");
QUIT;
