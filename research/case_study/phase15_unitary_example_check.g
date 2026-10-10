# Exact q=11 natural-matrix and full intersection certificate; finite scope only.
SizeScreen([1000,40]);;
Check15:=function(q,t0,x0,y0)
 local start,E,o,z,ii,a,b,c,t,x,y,R,S,zz,r0,r1,r2,r3,rr,H,bar,A,B,W,G,normminus,plane,orbit,act,pp,pg,expected,sets,groups,j,k,n,types,mid,m;
 start:=Runtime();E:=GF(q^2);o:=One(E);z:=Zero(E);ii:=Z(q^2)^((q^2-1)/4);a:=ii*t0;b:=x0*o+ii*y0;c:=-b^q;
 t:=a/ii;x:=(b+b^q)/2;y:=(b-b^q)/(2*ii);
 Assert(0,t^q=t and x^q=x and y^q=y and t*t+x*x+y*y=o);
 H:=IdentityMat(4,E);bar:=m->List(m,row->List(row,v->v^q));
 r0:=DiagonalMat([o,o,-o,-o]);r1:=[[o,z,z,z],[z,z,z,o],[z,z,-o,z],[z,o,z,z]];
 R:=[[z,ii],[ii,z]];S:=[[a,b],[c,-a]];zz:=[[o,z],[z,-o]];
 r2:=[[z,ii,z,z],[ii,z,z,z],[z,z,a,b],[z,z,c,-a]];
 r3:=[[z,z,o,z],[z,z,z,o],[-o,z,z,z],[z,-o,z,z]];rr:=[r0,r1,r2,r3];
 Assert(0,ForAll(rr,m->DeterminantMat(m)=o and m*TransposedMat(bar(m))=H));
 A:=[[z,ii*a,ii*b-o,-ii*a],[-ii*a,z,-ii*a,o-ii*c],[o-ii*b,ii*a,z,ii*a],[ii*a,ii*c-o,-ii*a,z]];
 B:=DiagonalMat([c,c,b,c]);
 Assert(0,A*bar(A)=-(t*t+2*y+2)*H and B*bar(B)=(o-t*t)*H);
 Print("START q=",q," parameter_txy=",[t0,x0,y0]," txy=",t*x*y," A_scalar=",-(t*t+2*y+2)," block_SU2_order=",Size(Group(ii*zz,R,S)),"\n");
 G:=Group(rr);normminus:=First(Elements(E),v->v*v^q=-o);
 plane:=[[o,normminus,z,z],[z,z,o,normminus]];orbit:=Orbit(G,plane,OnSubspacesByCanonicalBasis);
 expected:=q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 Assert(0,Length(orbit)=(q+1)*(q^3+1));act:=ActionHomomorphism(G,orbit,OnSubspacesByCanonicalBasis);
 pp:=List(rr,m->Image(act,m));pg:=Group(pp);Assert(0,Size(pg)=expected);
 types:=List([1..3],j->Order(pp[j]*pp[j+1]));Assert(0,ForAll(pp,m->Order(m)=2));
 for j in [1..4] do for k in [1..4] do if AbsInt(j-k)>1 then Assert(0,Comm(pp[j],pp[k])=());fi;od;od;
 sets:=Combinations([1..4]);groups:=List(sets,s->Subgroup(pg,pp{s}));n:=0;
 for j in [1..16] do for k in [1..16] do
  Assert(0,Intersection(groups[j],groups[k])=groups[Position(sets,Intersection(sets[j],sets[k]))]);n:=n+1;
 od;od;
 Print("PASS q=",q," type=",types," order=",Size(pg)," planes=",Length(orbit)," closures=16 meets=",n," subset_orders=",List(groups,Size)," runtime_ms=",Runtime()-start,"\n");
end;;
Check15(11,2,9,2);
QUIT;
