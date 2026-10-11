# Optional validation of written intersection and voltage arguments.
Read("base_certificate.g");
sets:=Combinations([1..4]);subs:=List(sets,s->Subgroup(G,rr{s}));
for a in [1..16] do for b in [1..16] do
 Need(Intersection(subs[a],subs[b])=subs[Position(sets,Intersection(sets[a],sets[b]))],"base all-subset IP");
od;od;
V:=Group(r0,r0^r1,r3,r3^r2);Need(Size(V)=16 and IsElementaryAbelian(V)and IsNormal(G,V),"actual translation kernel");
Need(Size(Group(r1,r2))=6 and Size(Intersection(V,Group(r1,r2)))=1,"split S3 quotient");
Edge:=Group(r0,r2,r3);VE:=Group(Concatenation(GeneratorsOfGroup(V),GeneratorsOfGroup(Edge)));
Need(Size(Edge)=16 and Size(VE)=32 and Size(Intersection(Edge,V))=8,"opposite edge union");
Need(Group(r0,r3,r0^r1,r2)=VE,"source sign rules connect all32 flags");
H0:=Group(r1,r2,r3);vertices:=RightCosets(G,H0);
edge1:=Set(Edge);edge2:=Difference(Set(VE),edge1);
a:=Filtered([1..4],i->not IsEmpty(Intersection(Set(vertices[i]),edge1)));
b:=Filtered([1..4],i->not IsEmpty(Intersection(Set(vertices[i]),edge2)));
Need(Length(a)=2 and Length(b)=2 and IsEmpty(Intersection(a,b)),"opposite source edges");
z:=function(g,i)
 if i<>2 then return 0;elif g in V then return 1;
 elif g*r2 in V then return -1;else return 0;fi;
end;
for g in Elements(G) do
 for i in [0..3] do for j in [0..3] do if j>i+1 then
  a:=g;v:=0;for k in [i,j,i,j]do v:=v+z(a,k);a:=a*rr[k+1];od;
  Need(a=g and v=0,"distant square integer voltage");
 fi;od;od;
 # Every middle section projects bijectively to the alternating quotient cycle.
 a:=g;v:=0;for k in [1,2,1,2,1,2]do v:=v+z(a,k);a:=a*rr[k+1];od;
 Need(a=g and AbsInt(v)=1,"primitive section voltage");
od;
hshift:=function(g)if g in V or g*r1 in V then return 0;else return 1;fi;end;
for g in Elements(G) do for i in [0..3]do
 Need(z(r1*g,i)=-z(g,i)+hshift(g*rr[i+1])-hshift(g),"literal rho1 lift");
 Need(z(r0*g,i)=z(g,i)and z(r3*g,i)=z(g,i),"outer voltage lifts");
 Need(z(r2*g,i)=-z(g,i),"rho2 voltage inversion");
od;od;
Print("BASE_DIAGNOSTICS_ALL256_IP_INTEGER_VOLTAGES_PASS\n");

