# Exact deleted-pencil residue of the classical Hermitian unital U_H(4).
# No original source table is used as input.
need:=function(b,s) if not b then Error(s);fi;end;
q:=4;K:=GF(q^2);els:=Elements(K);z:=Zero(K);o:=One(K);
pv:=[];
for x in els do for y in els do Add(pv,[o,x,y]);od;od;
for x in els do Add(pv,[z,o,x]);od;Add(pv,[z,z,o]);
pts:=Filtered(pv,v->Sum(v,x->x^(q+1))=z);
blocks:=[];
for c in pv do
 B:=Filtered([1..Length(pts)],i->Sum([1..3],j->pts[i][j]*c[j])=z);
 if Length(B)=q+1 then AddSet(blocks,B);fi;
od;
need(Length(pts)=65 and Length(blocks)=208,"unital parameters");
need(ForAll(Combinations([1..65],2),P->Number(blocks,B->IsSubset(B,P))=1),"design pair uniqueness");
L:=blocks[1];p:=L[1];left:=Difference([1..65],L);right:=[];
for a in Difference(L,[p]) do for M in blocks do
 if a in M and M<>L then Add(right,[a,M]);fi;
od;od;
need(Length(left)=60 and Length(right)=60,"residue part sizes");
adj:=List([1..120],x->[]);
for i in [1..60] do for j in [1..60] do
 if left[i] in right[j][2] then Add(adj[i],j+60);Add(adj[j+60],i);fi;
od;od;
need(Set(List(adj,Length))=[4],"four-regular residue");
profiles:=[];girth:=120;
for root in [1..120] do
 dist:=List([1..120],x->-1);parent:=List([1..120],x->0);dist[root]:=0;queue:=[root];pos:=1;
 while pos<=Length(queue) do
  a:=queue[pos];pos:=pos+1;
  for b in adj[a] do
   if dist[b]=-1 then dist[b]:=dist[a]+1;parent[b]:=a;Add(queue,b);
   elif parent[a]<>b then girth:=Minimum(girth,dist[a]+dist[b]+1);fi;
  od;
 od;
 need(Length(queue)=120,"all-root connectivity");
 profile:=[];for d in [0..Maximum(dist)] do Add(profile,Number(dist,x->x=d));od;Add(profiles,profile);
od;
need(girth=8 and ForAll(profiles,P->Length(P)=7),"girth eight and diameter six");
Print("PHASE265_RESIDUE_PROFILES ",Set(profiles{[1..60]})," ",Set(profiles{[61..120]}),"\n");
need(Set(profiles{[1..60]})=[[1,4,12,36,44,20,3]],"point profile");
need(Set(profiles{[61..120]})=[[1,4,12,36,42,20,5]],"line profile");
# Any graph automorphism preserves distance profiles, so these distinct
# profiles exclude every part-interchanging automorphism.
Print("PHASE265_UH4_PASS points65 blocks208 residue120 edges240 degree4 girth8 diameter6 no_duality\n");
QUIT;
