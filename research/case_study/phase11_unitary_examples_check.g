# Standalone bounded checks for the original sparse unitary template.
# GAP 4.15.1 core; no external group database or simple-group recognition.
CheckUnitaryTemplate:=function(q,aExponent,expectedMiddle,expectIP)
 local ff,ef,ee,zz,ii,delta,aa,kk,H,bar,r0,r1,r2,r3,rr,mg,plane,orbit,
 act,pp,pg,expected,subsets,groups,j,l,position,start,meetFailures,facetMeet;
 start:=Runtime();ff:=GF(q);ef:=GF(q^2);ee:=One(ef);zz:=Zero(ef);
 ii:=First(Elements(ff),x->x*x=-ee);
 delta:=Z(q^2)^((q+1)/2);aa:=Z(q)^aExponent;kk:=delta*aa;
 Assert(0,kk<>zz and kk^q=-kk and DegreeFFE(kk^2)=LogInt(q,Characteristic(ff)));
 H:=DiagonalMat([ee,-ee,ee,-ee]);
 bar:=m->List(m,row->List(row,x->x^q));
 r0:=DiagonalMat([ee,ee,-ee,-ee]);
 r1:=[[ee,zz,zz,zz],[zz,zz,zz,ee],[zz,zz,-ee,zz],[zz,ee,zz,zz]];
 r2:=[[zz,ii,zz,zz],[ii,zz,zz,zz],[zz,zz,kk,ii-kk],[zz,zz,ii+kk,-kk]];
 r3:=[[zz,zz,ee,zz],[zz,zz,zz,ee],[-ee,zz,zz,zz],[zz,-ee,zz,zz]];
 rr:=[r0,r1,r2,r3];
 Assert(0,ForAll(rr,m->m*H*TransposedMat(bar(m))=H and DeterminantMat(m)=ee));
 mg:=Group(rr);plane:=[[ee,ee,zz,zz],[zz,zz,ee,ee]];
 Assert(0,plane*H*TransposedMat(bar(plane))=NullMat(2,2,ef));
 orbit:=Orbit(mg,plane,OnSubspacesByCanonicalBasis);
 Assert(0,Length(orbit)=(q+1)*(q^3+1));
 act:=ActionHomomorphism(mg,orbit,OnSubspacesByCanonicalBasis);
 pp:=List(rr,m->Image(act,m));pg:=Group(pp);
 expected:=q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);
 Assert(0,Size(pg)=expected and ForAll(pp,x->Order(x)=2));
 Assert(0,List([1..3],j->Order(pp[j]*pp[j+1]))=[4,expectedMiddle,2*Characteristic(ff)]);
 for j in [1..4] do for l in [1..4] do
  if AbsInt(j-l)>1 then Assert(0,Comm(pp[j],pp[l])=());fi;
 od;od;
 subsets:=Combinations([1..4]);groups:=List(subsets,s->Subgroup(pg,pp{s}));meetFailures:=0;
 for j in [1..16] do for l in [1..16] do
  position:=Position(subsets,Intersection(subsets[j],subsets[l]));
  if Intersection(groups[j],groups[l])<>groups[position] then meetFailures:=meetFailures+1;fi;
 od;od;
 Assert(0,(meetFailures=0)=expectIP);
 facetMeet:=Size(Intersection(groups[Position(subsets,[1,2,3])],groups[Position(subsets,[2,3,4])]));
 Print("PASS q=",q," aExponent=",aExponent," middle=",expectedMiddle," order=",Size(pg),
       " orbit=",Length(orbit)," subset_groups=16 meets_tested=256 meet_failures=",meetFailures,
       " facet_meet=",facetMeet," expected_IP=",expectIP," runtime_ms=",Runtime()-start,"\n");
end;;
CheckUnitaryTemplate(5,0,26,true);
CheckUnitaryTemplate(9,2,80,true);
CheckUnitaryTemplate(13,4,170,true);
CheckUnitaryTemplate(9,0,40,false);
Print("PASS 3 C-group examples and1 failed-IP control;64 subset groups;1024 meets tested; no simple-group recognition\n");
QUIT;
