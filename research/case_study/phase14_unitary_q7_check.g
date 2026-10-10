# Original PSU4(7) witness. GAP core only; no recognition or group database.
SizeScreen([1000,40]);;
CheckUnitarySeven:=function()
 local start,q,F,o,z,ii,a,b,c,H,bar,r0,r1,r2,r3,rr,G,v,plane,orbit,
 action,pp,pg,expected,sets,groups,j,k,pos,tested,types,orders,pol,bas,
 coords,entry,rows;
 start:=Runtime();q:=7;F:=GF(49);o:=One(F);z:=Zero(F);
 # Z(49) has polynomial X^2-X+3; these equal 4+6Z(49),6+2Z(49),2.
 ii:=Z(49)^12;a:=Z(49)^4;b:=2*o;c:=-b^q;
 pol:=MinimalPolynomial(GF(7),Z(49));
 Assert(0,List(CoefficientsOfUnivariatePolynomial(pol),IntFFE)=[3,6,1]);
 Assert(0,ii=4*o+6*Z(49) and a=6*o+2*Z(49));
 Assert(0,ii^2=-o and ii^q=-ii and a^q=-a and a*a+b*c=-o);
 H:=IdentityMat(4,F);bar:=m->List(m,row->List(row,x->x^q));
 r0:=DiagonalMat([o,o,-o,-o]);
 r1:=[[o,z,z,z],[z,z,z,o],[z,z,-o,z],[z,o,z,z]];
 r2:=[[z,ii,z,z],[ii,z,z,z],[z,z,a,b],[z,z,c,-a]];
 r3:=[[z,z,o,z],[z,z,z,o],[-o,z,z,z],[z,-o,z,z]];
 rr:=[r0,r1,r2,r3];
 Assert(0,ForAll(rr,m->DeterminantMat(m)=o and m*TransposedMat(bar(m))=H));
 Assert(0,List(rr,m->m*m)=[H,H,-H,-H]);
 G:=Group(rr);v:=First(Elements(F),x->x*x^q=-o);
 plane:=[[o,v,z,z],[z,z,o,v]];
 Assert(0,plane*TransposedMat(bar(plane))=NullMat(2,2,F));
 orbit:=Orbit(G,plane,OnSubspacesByCanonicalBasis);
 Assert(0,Length(orbit)=(q+1)*(q^3+1));
 action:=ActionHomomorphism(G,orbit,OnSubspacesByCanonicalBasis);
 pp:=List(rr,m->Image(action,m));pg:=Group(pp);
 expected:=q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 Assert(0,Size(pg)=expected and expected=1165572172800);
 Assert(0,ForAll(pp,x->Order(x)=2));
 types:=List([1..3],j->Order(pp[j]*pp[j+1]));
 Assert(0,types=[4,24,4]);
 for j in [1..4] do for k in [1..4] do
  if AbsInt(j-k)>1 then Assert(0,Comm(pp[j],pp[k])=());fi;
 od;od;
 sets:=Combinations([1..4]);groups:=List(sets,s->Subgroup(pg,pp{s}));
 tested:=0;
 for j in [1..16] do for k in [1..16] do
  pos:=Position(sets,Intersection(sets[j],sets[k]));
  Assert(0,Intersection(groups[j],groups[k])=groups[pos]);tested:=tested+1;
 od;od;
 orders:=List(groups,Size);
 Assert(0,orders[Position(sets,[1,2,3])]=56448);
 Assert(0,orders[Position(sets,[2,3,4])]=138297600);
 bas:=Basis(F,[o,Z(49)]);coords:=x->List(Coefficients(bas,x),IntFFE);
 PrintTo("phase14_unitary_q7_check.json","{\n  \"status\": \"PASS\",\n",
  "  \"q\": 7,\n  \"characteristic\": 7,\n",
  "  \"defining_polynomial_low_to_high\": [3,6,1],\n",
  "  \"i\": ",coords(ii),",\n  \"a\": ",coords(a),",\n  \"b\": ",coords(b),",\n",
  "  \"projective_group_order\": ",Size(pg),",\n",
  "  \"isotropic_plane_orbit_size\": ",Length(orbit),",\n",
  "  \"schlafli_type\": ",types,",\n",
  "  \"subset_labels\": ",sets,",\n  \"subset_orders\": ",orders,",\n",
  "  \"exact_intersection_tests\": ",tested,",\n",
  "  \"runtime_ms\": ",Runtime()-start,",\n",
  "  \"gap_version\": \"",GAPInfo.Version,"\",\n",
  "  \"identification\": \"SU membership, unitary order formula and scalar-factor action order sandwich; no group recognition\"\n}\n");
 Print("PASS PSU4(7) order=",Size(pg)," type=",types,
       " planes=",Length(orbit)," closures=16 exact_meets=",tested,
       " runtime_ms=",Runtime()-start,"\n");
end;;
CheckUnitarySeven();
QUIT;
