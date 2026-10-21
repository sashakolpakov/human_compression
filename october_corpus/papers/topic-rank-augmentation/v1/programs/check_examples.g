# Complete three source examples, with actual parabolic and orbit computations.
SizeScreen([240,60]);;
Need:=function(x,m)if not x then Error(m);fi;end;;
Par:=function(xs,I)return Group(Concatenation([()],xs{I}));end;;
AllIP:=function(xs)local ss,i,j,n;ss:=Combinations([1..Length(xs)]);n:=0;
 for i in ss do for j in ss do
  Need(Intersection(Par(xs,i),Par(xs,j))=Par(xs,Intersection(i,j)),"old intersection property");n:=n+1;
 od;od;return n;end;;
cases:=[
 rec(n:=9,a:=(2,3)(6,9)(7,8),q:=(1,2)(3,4)(5,6),c:=(4,5)(6,7)(8,9),t:=(1,2),big:=[2..9],primitive:=true),
 rec(n:=10,a:=(1,2)(3,4)(9,10),q:=(2,3)(4,5)(6,7)(8,9),c:=(5,6)(7,8),t:=(2,3),big:=[3..10],primitive:=false),
 rec(n:=13,a:=(1,2)(3,4)(7,9)(8,10),q:=(2,3)(4,5)(6,7)(10,11)(12,13),c:=(5,6)(7,8)(9,10)(11,12),t:=(2,3),big:=[3..13],primitive:=true)
];;
rows:=[];;
for e in cases do
 old:=[e.a,e.q,e.c];;b:=e.t*e.q;;new:=[e.t,e.a,b,e.c];;
 Need(Size(Group(old))=Factorial(e.n),"original symmetric group");
 Need(ForAll(old,g->Order(g)=2) and e.a*e.c=e.c*e.a,"original string");
 count:=AllIP(old);;B:=Group([e.a,b]);;H:=Group([e.t,e.a,b]);;K:=Group([e.a,b,e.c]);;
 Need(ForAll(Orbits(B,[1..e.n]),o->Length(o)<=3),"middle orbit bound");
 Need(IsPrimitive(Action(K,e.big))=e.primitive,"specified primitive action");
 if e.n<>10 then Need(Size(Action(K,e.big))=Factorial(Length(e.big)),"full symmetric projection");fi;
 Need(Intersection(H,K)<>B,"new intersection failure");
 if e.n=9 then Need((2,3,4) in Intersection(H,K) and not (2,3,4) in B,"source first independent triple witness");fi;
 if e.n=10 then
  Need(Set(Orbit(K,[3,10],OnSets))=Set([[3,10],[4,9],[5,8],[6,7]]),"literal source block system");
  Need((1,2) in Intersection(H,K) and not (1,2) in B,"source pair-flip witness");
 fi;
 if e.n=13 then
  Need(ForAll([e.a,b,e.c],g->SignPerm(g)=1),"all three even marks");
  Need((3,4,5) in Intersection(H,K) and not (3,4,5) in B,"source third independent triple witness");
 fi;
 Add(rows,[e.n,Size(B),Size(H),Size(K),Size(Intersection(H,K)),List([e.a,b,e.c],SignPerm),count]);
od;
Need(rows=[[9,12,288,40320,72,[-1,1,-1],64],[10,12,1440,768,24,[-1,-1,1],64],[13,12,1440,39916800,72,[1,1,1],64]],"complete fixed source-example table");
Print("SOURCE_EXAMPLES ",rows,"\n");
Print("PASS three source examples; old_IP_pairs=192; all output defects witnessed\n");
QUIT_GAP(0);
