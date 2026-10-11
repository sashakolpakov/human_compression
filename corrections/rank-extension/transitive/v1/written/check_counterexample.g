# Literal diagnostic for the transitive degree-eleven example.
# Native permutation subgroup algorithms; never list S11 or S12 elements.
SizeScreen([240,60]);;
Require:=function(ok,msg)if not ok then Error(msg);fi;end;;
Parabolic:=function(xs,I)return Group(Concatenation([()],xs{I}));end;;
Failures:=function(xs)local sets,groups,i,j,out;
 sets:=Combinations([1..Length(xs)]);groups:=List(sets,I->Parabolic(xs,I));out:=[];
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  if Intersection(groups[i],groups[j])<>Parabolic(xs,Intersection(sets[i],sets[j])) then Add(out,[sets[i],sets[j]]);fi;
 od;od;return out;end;;
Epsilon:=g->(1-SignPerm(g))/2;;
OrbitSets:=function(G,points)return Set(List(Orbits(G,points),Set));end;;
CheckString:=function(xs)local i,j;
 Require(Length(Set(xs))=Length(xs) and ForAll(xs,g->Order(g)=2),"distinct involutions");
 for i in [1..Length(xs)] do for j in [1..Length(xs)] do
  Require(AbsInt(i-j)<2 or xs[i]*xs[j]=xs[j]*xs[i],"string commutations");
 od;od;end;;

x:=(8,9)(10,11);y:=(1,8)(9,10);q:=(1,2)(3,4);
r:=(2,6)(3,5)(4,7);s:=(3,4)(6,7);
t:=(3,4);u:=(3,5)(4,7);tau:=(9,10);
old:=[x,y,q,r,s];new:=[x,y,(1,12),(2,12)*t,r,s];
G:=Group(old);H:=Group(new);CheckString(old);CheckString(new);
Require(G=SymmetricGroup(11) and H=SymmetricGroup(12),"whole symmetric groups");
D:=Group(t,u);rot:=Group(t*u);Chi:=function(d)if d in rot then return 0;else return 1;fi;end;;
Require(Size(D)=8 and Size(rot)=4 and Chi(t)=1 and Chi(u)=1,"dihedral character");
Require(ForAll(Elements(D),d->ForAll(Elements(D),e->Chi(d*e)=(Chi(d)+Chi(e)) mod 2)),"character homomorphism");
w:=q*r*(q*s*r)^4*s;
Require(w=(4,5),"short transposition word");
Require(List([(),q,r,r*s,r*s*r,r*s*r*q],z->w^z)=[(4,5),(3,5),(3,7),(4,6),(2,7),(1,7)],"six conjugates");
Require(Group((4,5),(3,5),(3,7),(4,6),(2,7),(1,7))=SymmetricGroup([1..7]),"spanning-tree transpositions");
Require(r*s=(2,7,3,5,4,6) and x*y=(1,8,10,11,9),"cycle coordinates");
Require((y*q)^3=t*tau and (y*(1,2))^3=tau,"separation words");
Require((q*r)^4=(1,6,2),"pure alternating generator");
T:=Group(q,r);R:=Group(r,s);Q:=Group(q,r,s);
A:=Group(x,y,q,r);N:=Group(x,y,q);M:=Group(y,q,r);P:=Group(y,q);B:=Group(y,q,r,s);
Fiber:=function(points,tag)
 local out,g,d;out:=[];
 for g in Elements(SymmetricGroup(points)) do for d in Elements(tag) do
  if Epsilon(g)=Chi(d) then Add(out,g*d);fi;
 od;od;return Set(out);end;;
Require(Set(Elements(T))=Fiber([1,2,6],D),"T formula");
Require(Size(R)=12 and Stabilizer(R,[2,6],OnSets)=Group(r),"R edge stabilizer");
Require(Q=SymmetricGroup([1..7]),"Q formula");
Require(Set(Elements(N))=Set(List(Elements(SymmetricGroup([1,2,8,9,10,11])),g->g*t^Epsilon(g))),"N formula");
expectedP:=[];;
for g in Elements(SymmetricGroup([1,2,8])) do for e in [0,1] do
 Add(expectedP,g*t^e*tau^((Epsilon(g)+e) mod 2));
od;od;
Require(Set(Elements(P))=Set(expectedP),"P formula");
expectedM:=[];;
for g in Elements(SymmetricGroup([1,2,6,8])) do for d in Elements(D) do
 Add(expectedM,g*d*tau^((Epsilon(g)+Chi(d)) mod 2));
od;od;
Require(Set(Elements(M))=Set(expectedM),"M formula");
Require(Set(Elements(A))=Fiber([1,2,6,8,9,10,11],D),"A formula");
Require(B=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([1..8])),[tau])),"B formula");
Require(Intersection(T,R)=Group(r),"Q end intersection");
Require(Intersection(Group(x,y),P)=Group(y),"N end intersection");
Require(Intersection(P,T)=Group(q),"M end intersection");
Require(Intersection(N,M)=P,"A end intersection");
Require(Intersection(M,Q)=T,"B end intersection");
Require(Intersection(A,B)=M,"whole end intersection");
Require(Length(Failures(old))=0,"all1024 old intersections");
Require(Length(Failures(new))=96,"all4096 new intersections");
Require((new[3]*new[4])^3=t and t in Parabolic(new,[4,5,6]),"explicit repeated beta");
Require(not t in Parabolic(new,[4]),"beta not in common-label subgroup");
Require(Intersection(Parabolic(new,[3,4]),Parabolic(new,[4,5,6]))=Group((2,12),t),"witness intersection is V4");

expected:=[[[1..8],[9,10],[11]],[[1..7],[8,9],[10,11]],[[1,8,9,10,11],[2,3,4,5,6,7]],[[1,2,8,9,10,11],[3,4],[5],[6,7]],[[1,2,6,8,9,10,11],[3,4,5,7]]];
edges:=[[8,9],[1,8],[1,2],[2,6],[6,7]];
for j in [1..5] do
 J:=Parabolic(old,Difference([1..5],[j]));
 Require(OrbitSets(J,[1..11])=Set(List(expected[j],Set)),"deleted orbit partition");
 Require(Length(OrbitSets(J,[1..11]))>1,"fracture availability");
 Require(edges[j][1]^old[j]=edges[j][2] and not edges[j][2] in Orbit(J,edges[j][1]),"chosen fracture edge");
od;
Require(Set(Concatenation(edges))=[1,2,6,7,8,9],"fracture path support");
left:=[1,8,9,10,11];right:=[2,3,4,5,6,7];
Require(Union(left,right)=[1..11] and Intersection(left,right)=[],"split partition");
Require(Filtered(left,a->not a^q in left)=[1] and 1^q=2,"unique crossing edge");
Require(ForAll(right,a->a^x=a and a^y=a) and ForAll(left,a->a^r=a and a^s=a),"perfect split supports");
Require(q=(1,2)*t and ForAll(left,a->a^t=a),"alpha trivial; beta internal");
Require(1^y<>1 and 2^r<>2,"both endpoints moved");
Require(IsTransitive(G,[1..11]),"transitive input");
Require(5< (11+3)/2,"outside main stability range");

# Structural controls, each testing an essential distinction.
Require(not t in Group(new[4]),"a nonidentity witness is essential");
Require(Length(Failures([x,y,(1,2),r,s]))=0,"pure crossing has a C input");
Require(Length(Failures([x,y,(1,12),(2,12),r,s]))=0,"pure crossing extension has no defect");
Require(not (3 in left),"the internal beta factor is on the correct side");
Print("PASS transitive S11 input;1024 old identities;96 failures/4096 new pairs;7 subgroup formulas;6 end intersections;5 fracture edges;perfect split;explicit beta witness;4 controls\n");
QUIT_GAP(0);
