LogTo("research/leemans/suzuki_coset_check.log");;
G:=SuzukiGroup(IsPermGroup,8);;
S:=SylowSubgroup(G,2);;
B:=Normalizer(G,S);;
T:=ComplementClassesRepresentatives(B,S)[1];;
H:=ClosureGroup(Center(S),T);;
K:=Normalizer(G,T);;
w:=First(Elements(K),x->Order(x)=2);;
Print("orders G,S,B,T,H,K=",List([G,S,B,T,H,K],Size),"\n");
cs:=RightCosets(G,H);;
act:=Action(G,cs,OnRight);;
base:=Position(cs,RightCoset(H,One(G)));;
mate:=Position(cs,RightCoset(H,w));;
arcs:=Orbit(act,[base,mate],OnTuples);;
adj:=List([1..Length(cs)],x->[]);;
for edge in arcs do AddSet(adj[edge[1]],edge[2]); od;
Print("vertices=",Length(cs)," degrees=",Set(List(adj,Length)),"\n");
v:=base;; u:=mate;;
c3:=Length(Intersection(adj[v],adj[u]));;
c4:=Sum(Difference(adj[v],[u]),x->Length(Intersection(Difference(adj[u],[v]),adj[x])));;
c5:=0;;
for a in Difference(adj[v],[u]) do
 for b in Difference(adj[u],[v]) do
  c5:=c5+Length(Difference(Intersection(adj[a],adj[b]),[v,u,a,b]));
 od;
od;
Print("edge cycles length3,4,5=",[c3,c4,c5],"\n");
if Length(cs)<>520 or Set(List(adj,Length))<>[8] or [c3,c4,c5]<>[0,0,7] then
 Error("Suzuki graph certificate failed");
fi;
Print("SUZUKI COSET GRAPH q=8 PASS\n");
LogTo();
QUIT;
