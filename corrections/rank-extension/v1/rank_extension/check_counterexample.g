SizeScreen([240,60]);;
Require:=function(ok,msg)if not ok then Error(msg);fi;end;;
P:=function(xs,I)return Group(Concatenation([()],xs{I}));end;;
Failures:=function(xs)local sets,I,J,out;sets:=Combinations([1..Length(xs)]);out:=[];for I in sets do for J in sets do if Intersection(P(xs,I),P(xs,J))<>P(xs,Intersection(I,J)) then Add(out,[I,J]);fi;od;od;return out;end;;
Epsilon:=function(g)return (1-SignPerm(g))/2;end;;
ParityFibre:=function(points,sigma,tau)local out,g,u,v;out:=[];for g in Elements(SymmetricGroup(points)) do for u in [0,1] do for v in [0,1] do if (u+v) mod 2=Epsilon(g) then Add(out,g*sigma^u*tau^v);fi;od;od;od;return Set(out);end;;
OrbitSets:=function(G,points)return Set(List(Orbits(G,points),Set));end;;
CheckString:=function(xs)local i,j;Require(Length(Set(xs))=Length(xs) and ForAll(xs,x->Order(x)=2),"distinct nonidentity involutions");for i in [1..Length(xs)] do for j in [1..Length(xs)] do Require(AbsInt(i-j)<2 or xs[i]*xs[j]=xs[j]*xs[i],"distant commutations");od;od;end;;

sigma:=(6,7);tau:=(8,9);old:=[(1,2)*tau,(2,3)*sigma,(3,4)*sigma,(4,5)];
new:=[old[1],(2,10),(3,10)*sigma,old[3],old[4]];
G:=Group(old);H:=Group(new);CheckString(old);CheckString(new);
Require(Size(G)=480 and Size(H)=2880,"whole group orders");
Require(Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([1..5])),[sigma,tau]))=G,"full input direct product");
Require((old[1]*old[2])^3=sigma*tau and (old[3]*old[4])^3=sigma,"old central kernel words");
Require(Set(Elements(P(old,[1,2,3])))=ParityFibre([1..4],sigma,tau),"first rank-three formula");
Require(P(old,[2,3,4])=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([2..5])),[sigma])),"last rank-three formula");
Require(Set(Elements(P(old,[2,3])))=Set(List(Elements(SymmetricGroup([2..4])),g->g*sigma^Epsilon(g))),"middle parity graph");
Require(Set(Elements(P(old,[1,2])))=ParityFibre([1..3],sigma,tau),"first rank-two formula");
Require(P(old,[3,4])=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([3..5])),[sigma])),"last rank-two formula");
Require(Intersection(P(old,[1,2]),P(old,[2,3]))=P(old,[2]),"first rank-three end intersection");
Require(Intersection(P(old,[2,3]),P(old,[3,4]))=P(old,[3]),"last rank-three end intersection");
Require(Intersection(P(old,[1,2,3]),P(old,[2,3,4]))=P(old,[2,3]),"rank-four end intersection");
Require(Length(Failures(old))=0,"all256 original intersection identities");
Require(Length(Failures(new))=72,"all1024 new intersections with72 failures");
Require((new[2]*new[3])^3=sigma and (new[4]*new[5])^3=sigma and sigma<>(),"two disjoint-label word identities");
Require(Intersection(P(new,[2,3]),P(new,[4,5]))=Group(sigma),"literal disjoint intersection");
Require(Intersection([2,3],[4,5])=[],"disjoint label sets");

expected:=[[[1],[2,3,4,5],[6,7],[8],[9]],[[1,2],[3,4,5],[6,7],[8,9]],[[1,2,3],[4,5],[6,7],[8,9]],[[1,2,3,4],[5],[6,7],[8,9]]];
Require(OrbitSets(G,[1..9])=Set([[1..5],[6,7],[8,9]]),"full orbit partition");
for j in [1..4] do
 Q:=P(old,Difference([1..4],[j]));
 Require(OrbitSets(Q,[1..9])=Set(List(expected[j],Set)),"maximal parabolic orbit partition");
 Require(Length(OrbitSets(Q,[1..9]))>=Length(OrbitSets(G,[1..9]))+1,"source fracture orbit count");
 Require(j^old[j]=j+1 and not j+1 in Orbit(Q,j),"chosen fracture edge");
od;
A:=[1,2,8,9];B:=[3,4,5,6,7];splitgroup:=P(old,[1,3,4]);
Require(Union(A,B)=[1..9] and Intersection(A,B)=[],"partition convention");
Require(Length(OrbitSets(splitgroup,[1..9]))=Length(OrbitSets(G,[1..9]))+1,"exact split orbit count");
Require(Filtered(A,x->not x^old[2] in A)=[2] and 2^old[2]=3,"unique crossing edge");
Require(ForAll(B,x->x^old[1]=x) and ForAll(A,x->x^old[3]=x and x^old[4]=x),"perfect earlier/later supports");
Require(old[2]=(2,3)*sigma and ForAll(A,x->x^sigma=x),"alpha=1 and beta=sigma on B");
Require(2^old[1]<>2 and 3^old[3]<>3,"both endpoints moved by split parabolic");
Require(7 in Orbit(splitgroup,6),"remaining beta edge within one split-parabolic orbit");
Require(new=[old[1],(2,10),(3,10)*sigma,old[3],old[4]],"literal source extension");

# Controls distinguish the valid input and the essential repeated central factor.
untwisted:=[(1,2),old[2],old[3],old[4]];
Require(Length(Failures(untwisted))>0,"removing tau destroys the C input");
noSigma:=[old[1],(2,10),(3,10),(3,4),(4,5)];
Require(Length(Failures(noSigma))=0,"removing sigma eliminates the extension defect");
Require(not IsTransitive(G,[1..9]),"counterexample is not transitive");
Print("PASS all source hypotheses; old C256/256; new failures72/1024; explicit disjoint words; five subgroup formulas; three end intersections; orbit counts5/4/4/4;3 controls\n");
QUIT_GAP(0);
