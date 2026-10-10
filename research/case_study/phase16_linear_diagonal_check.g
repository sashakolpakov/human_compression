# Exact finite diagnostics for the uniform linear diagonal construction.
# No sampling, group recognition, or claimed all-field proof from finite cases.
SizeScreen([4096,100000]);;
Run16:=function(q)
 local start,p,F,o,z,h,rr,r0,r1,r2,r3,M,B,lines,hom,pp,G,expected,sets,subs,j,k,types;
 start:=Runtime();p:=Set(FactorsInt(q))[1];F:=GF(q);o:=One(F);z:=Zero(F);
 if q=3 then h:=o;else h:=First(List([1..q-2],j->Z(q)^j),v->Order(v)=q-1 and o+4*v<>z);fi;
 Assert(0,h<>fail and h<>z and o+4*h<>z and Size(Field([h]))=q);
 r0:=[[z,o,o,z],[z,z,z,o],[-h,z,z,-o],[z,-h,z,z]];
 r1:=DiagonalMat([o,o,-o,o]);r2:=[[-1,0,0,0],[1,1,0,0],[-1,-2,-1,0],[0,1,1,1]]*o;r3:=DiagonalMat([-o,o,o,-o]);rr:=[r0,r1,r2,r3];
 Assert(0,r0^2=-h*IdentityMat(4,F) and ForAll(rr{[2..4]},r->r*r=IdentityMat(4,F)));
 B:=[[-4*o,2*o,z,-o],[2*o,-o,z,-2*h],[z,z,o+4*h,z],[-o,-2*h,z,h]];
 Assert(0,DeterminantMat(B)=(o+4*h)^3 and r0*B*TransposedMat(r0)=-h*B);
 Assert(0,ForAll(rr{[2..3]},r->r*B*TransposedMat(r)=B));
 M:=Group(rr);lines:=Set(NormedRowVectors(F^4),v->ImmutableVector(F,v));hom:=ActionHomomorphism(M,lines,OnLines);pp:=List(rr,r->Image(hom,r));G:=Group(pp);
 expected:=2*q^6*(q^2-1)*(q^3-1)*(q^4-1)/Gcd(4,q-1);
 Assert(0,Size(G)=expected);types:=List([1..3],j->Order(pp[j]*pp[j+1]));Assert(0,types=[4,2*p,2*p]);
 Assert(0,ForAll(pp,r->Order(r)=2));
 for j in [1..4] do for k in [1..4] do if AbsInt(j-k)>1 then Assert(0,Comm(pp[j],pp[k])=());fi;od;od;
 sets:=Combinations([1..4]);subs:=List(sets,s->Subgroup(G,pp{s}));
 for j in [1..16] do for k in [1..16] do Assert(0,Intersection(subs[j],subs[k])=subs[Position(sets,Intersection(sets[j],sets[k]))]);od;od;
 Assert(0,Size(Group(pp{[2..4]}))=8*p^6);
 Print("PASS q=",q," h=",h," order=",Size(G)," type=",types," vertex=",8*p^6," facet=",Size(Group(pp{[1..3]}))," lines=",Length(lines)," groups=16 meets=256 runtime_ms=",Runtime()-start,"\n");
end;;
for q in [3,5,7,9] do Run16(q);od;
Print("ALL PASS:4fields,64subgroups,1024exactintersections.\n");
QUIT;
