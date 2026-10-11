# Independent exact projective-coordinate construction checks.
# Run: gap -q research/leemans/hermitian_unital_check.g
LogTo("research/leemans/hermitian_unital_check.log");

ConnectedBipartite := function(left,right,inc)
 local nl,nr,adj,i,j,seen,queue,pos,v,w;
 nl:=Length(left); nr:=Length(right);
 adj:=List([1..nl+nr],x->[]);
 for i in [1..nl] do for j in [1..nr] do
  if inc(left[i],right[j]) then
   Add(adj[i],nl+j); Add(adj[nl+j],i);
  fi;
 od; od;
 seen:=List([1..nl+nr],x->false); seen[1]:=true;
 queue:=[1]; pos:=1;
 while pos<=Length(queue) do
  v:=queue[pos];pos:=pos+1;
  for w in adj[v] do if not seen[w] then
   seen[w]:=true;Add(queue,w);
  fi;od;
 od;
 return rec(connected:=ForAll(seen,x->x),vertices:=nl+nr,
            edges:=Sum(adj,Length)/2,
            degrees:=Set(List(adj,Length)));
end;

CheckUnital := function(q)
 local K,elts,z,o,pv,x,y,pts,blocks,c,B,n,Q,L,p,M,flag,
       outside,flags,R,pr,lr,fr,global,delta,ts,gens,H,X,g,v,
       shellnorm,rootmoves,orbit;
 K:=GF(q^2);elts:=Elements(K);z:=Zero(K);o:=One(K);
 pv:=[];
 for x in elts do for y in elts do Add(pv,[o,x,y]);od;od;
 for x in elts do Add(pv,[z,o,x]);od;
 Add(pv,[z,z,o]);
 pts:=Filtered(pv,v->Sum(v,x->x^(q+1))=z);
 blocks:=[];
 for c in pv do
  B:=Filtered([1..Length(pts)],i->Sum([1..3],j->pts[i][j]*c[j])=z);
  if Length(B)=q+1 then Add(blocks,B);fi;
 od;
 n:=Length(pts);
 if n<>q^3+1 or Length(blocks)<>q^2*(q^2-q+1) then Error("Design sizes");fi;
 if not ForAll([1..n],i->Number(blocks,B->i in B)=q^2) then Error("Point degrees");fi;
 for x in [1..n] do for y in [x+1..n] do
  if Number(blocks,B->x in B and y in B)<>1 then Error("Pair uniqueness");fi;
 od;od;
 Q:=1;L:=blocks[1];
 # Residue of a point: distinct flag vertices identify with all p<>Q.
 pr:=ConnectedBipartite(Difference([1..n],[Q]),Filtered(blocks,B->not Q in B),
                       function(p,B) return p in B; end);
 # Residue of a block: flags (p,M) with p in L and M<>L.
 flags:=[];
 for p in L do for M in blocks do
  if p in M and M<>L then Add(flags,[p,M]);fi;
 od;od;
 outside:=Difference([1..n],L);
 lr:=ConnectedBipartite(outside,flags,
             function(Q,f) return Q in f[2] and Q<>f[1];end);
 # Residue of an original flag (p,M).
 p:=L[1]; M:=L;
 fr:=ConnectedBipartite(Difference(M,[p]),
       Filtered(blocks,B->p in B and B<>M),
       function(Q,B) return not Q in B;end);
 global:=ConnectedBipartite([1..n],blocks,function(Q,B)return not Q in B;end);
 if not pr.connected or not lr.connected or not fr.connected or not global.connected
 then Error("Disconnected geometry/residue");fi;
 # Independent root-group orbit check, in hyperbolic Hermitian coordinates.
 delta:=First(elts,t->t<>z and t+t^q=z);
 ts:=Filtered(elts,t->t+t^q=z);
 gens:=Concatenation(List(ts,t->[[o,t],[z,o]]),List(ts,t->[[o,z],[t,o]]));
 H:=Group(gens);
 shellnorm:=v->v[1]*v[2]^q+v[1]^q*v[2];
 X:=[];
 for x in elts do for y in elts do
  if shellnorm([x,y])=-o then Add(X,[x,y]);fi;
 od;od;
 if Size(H)<>q*(q^2-1) or Length(X)<>Size(H) then Error("SU2/shell size");fi;
 orbit:=Orbit(H,X[1],OnRight);
 if Set(orbit)<>Set(X) then Error("Root group not transitive on shell");fi;
 rootmoves:=ForAll(gens,g->ForAll(X,v->shellnorm(v*g-v)=z));
 if not rootmoves then Error("Root move non-isotropic");fi;
 Print("q=",q," points=",n," blocks=",Length(blocks),"\n");
 Print("point_residue=",pr,"\nblock_residue=",lr,
       "\nflag_residue=",fr,"\nantiincidence=",global,"\n");
 Print("SU2_size=",Size(H)," norm_shell=",Length(X),
       " root_group_orbit=",Length(orbit)," isotropic_moves=",rootmoves," PASS\n");
end;

for q in [2,3,4,5] do CheckUnital(q);od;
LogTo();
QUIT;
