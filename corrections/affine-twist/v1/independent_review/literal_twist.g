Require := function(ok,msg) if not ok then Error(msg); fi; end;
# Q/M has coordinates (v1+v4,v2+v4) mod2. The first four points
# encode these coordinates; the last four retain the full S4 linear part.
AffineMark := function(p,shift)
 local ims,a,b,v,w,i,j,aa,bb;
 ims:=[];
 for a in [0,1] do for b in [0,1] do
   v:=[b,a,0,(a+b) mod 2];w:=[0,0,0,0];
   for j in [1..4] do w[j^p]:=v[j];od;
   aa:=(w[1]+w[4]+shift[1]) mod 2;
   bb:=(w[2]+w[4]+shift[2]) mod 2;
   Add(ims,1+2*aa+bb);
 od;od;
 for i in [1..4] do Add(ims,4+i^p);od;
 return PermList(ims);
end;
marks:=[AffineMark((1,2),[0,0]),AffineMark((2,3),[0,0]),
        AffineMark((1,4),[0,1]),AffineMark((3,4),[0,0])];
A:=Group(marks);Require(Size(A)=96,"affine quotient size");
parabs:=List([1..4],i->Group(marks{Difference([1..4],[i])}));
Require(List(parabs,Size)=[24,24,24,24],"actual maximal parabolics");
ap:=GroupHomomorphismByImages(A,A,marks,marks{[2,1,4,3]});
aq:=GroupHomomorphismByImages(A,A,marks,marks{[1,3,2,4]});
Require(ap<>fail and aq<>fail and IsBijective(ap) and IsBijective(aq),"diagram automorphisms");
B:=Group(ap,aq);Require(Size(B)=8,"diagram action faithful");
G:=SemidirectProduct(B,A);eb:=Embedding(G,1);ea:=Embedding(G,2);
x:=Image(ea,marks[1]);p:=Image(eb,ap);q:=Image(eb,aq);
Require(Size(G)=768 and Order(x*p)=6 and Order(p*q)=4 and x*q=q*x,"whole group and orders");
Iall:=Intersection(parabs);
I234:=Intersection(parabs{[2,3,4]});I34:=Intersection(parabs{[3,4]});
Require(Iall=TrivialSubgroup(A) and I234=Group(marks[1]) and I34=Group(marks{[1,2]}),"literal intersection bridge");
literal:=[Group(Concatenation(List(GeneratorsOfGroup(Iall),a->Image(ea,a)),[p,q])),
 Group(Concatenation(List(GeneratorsOfGroup(I234),a->Image(ea,a)),[q])),
 Group(Concatenation(List(GeneratorsOfGroup(I34),a->Image(ea,a)),[p]))];
Require(literal=[Group(p,q),Group(x,q),Group(x,p)],"actual literal parabolics");
supports:=Combinations([1..3]);gen:=[x,p,q];
subs:=List(supports,s->Subgroup(G,gen{s}));
for i in [1..8] do for j in [1..8] do
 Require(Intersection(subs[i],subs[j])=subs[Position(supports,Intersection(supports[i],supports[j]))],"IP");
od;od;
prodset:=function(H,K) return Set(Concatenation(List(Elements(H),h->List(Elements(K),k->h*k))));end;
proper:=Filtered(subs,H->H<>G);nt:=0;
for H in proper do for K in proper do for L in proper do
 Require(Intersection(prodset(H,K),prodset(H,L))=prodset(H,Intersection(K,L)),"Helly product identity");nt:=nt+1;
od;od;od;
R:=Intersection(parabs[2],parabs[3]);R1:=Intersection(R,parabs[1]);R4:=Intersection(R,parabs[4]);
Require([Size(R),Size(R1),Size(R4),Size(ClosureGroup(R1,R4))]=[8,2,2,4],"input disconnected residue");
Print("PASS_DISTINCT_TWIST:base=",Size(A),";diagram=",Size(B),";whole=",Size(G),";literal=",List(literal,Size),";IP=64;products=",nt,";input-residue=8/4\n");
QUIT;
