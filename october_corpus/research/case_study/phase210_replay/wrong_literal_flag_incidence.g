# Phase210 independent literal construction, unitary action and transport audit.
SizeScreen([4096,4096]);;
P210Need:=function(ok,msg)
  if not ok then Print("PHASE210_FAIL ",msg,"\n"); FORCE_QUIT_GAP(1); fi;
end;;
P210Normalize:=v->v/First(v,x->not IsZero(x));;
P210Connected:=function(left,right,inc)
 local adj,i,j,queue,k,a,b,seen;
 adj:=List([1..Length(left)+Length(right)],x->[]);
 for i in [1..Length(left)] do for j in [1..Length(right)] do
  if inc(left[i],right[j]) then Add(adj[i],Length(left)+j);Add(adj[Length(left)+j],i);fi;
 od;od;
 seen:=[];queue:=[1];AddSet(seen,1);k:=1;
 while k<=Length(queue) do
  a:=queue[k];k:=k+1;
  for b in adj[a] do if not b in seen then AddSet(seen,b);Add(queue,b);fi;od;
 od;
 P210Need(Length(seen)=Length(adj),"literal graph connected");
 return [Length(adj),Sum(adj,Length)/2];
end;;
P210Check:=function(q)
 local F,el,z,o,J,J2,vecs,points,blocks,v,w,B,p,Q,L,M,flags,outside,
       shell,norm2,projection,pointres,blockres,flagres,global,
       gens,a,b,A,G,H,pair,alternatives,base,perms,rootgens,S,
       x,y,u,r,k,T,transportChecks,isotropic,common,idx,expected,
       bar,gram,wrong;
 F:=GF(q^2);el:=AsList(F);z:=Zero(F);o:=One(F);
 J:=[[z,z,o],[z,o,z],[o,z,z]];J2:=[[z,o],[o,z]];
 bar:=A->List(A,row->List(row,t->t^q));
 vecs:=Concatenation(List(Tuples(el,2),v->[o,v[1],v[2]]),List(el,x->[z,o,x]),[[z,z,o]]);
 points:=Filtered(vecs,v->v[1]*v[3]^q+v[1]^q*v[3]+v[2]^(q+1)=z);
 blocks:=Set(Filtered(List(vecs,c->Filtered([1..Length(points)],i->points[i]*c=z)),B->Length(B)=q+1));
 P210Need(Length(points)=q^3+1 and Length(blocks)=q^2*(q^2-q+1),"design counts");
 P210Need(ForAll(Combinations([1..Length(points)],2),pair->Number(blocks,B->IsSubset(B,pair))=1),"pair uniqueness");
 p:=Position(points,[o,z,z]);Q:=Position(points,[z,z,o]);
 L:=Filtered([1..Length(points)],i->points[i][2]=z);
 P210Need(L in blocks and p in L and Q in L,"literal hyperbolic secant");
 flags:=Concatenation(List(L,p->List(Filtered(blocks,M->p in M and M<>L),M->[p,M])));
 outside:=Difference([1..Length(points)],L);
 norm2:=v->v[1]*v[2]^q+v[1]^q*v[2];
 shell:=Filtered(Tuples(el,2),v->norm2(v)=-o);
 projection:=List(outside,i->[points[i][1],points[i][3]]/points[i][2]);
 P210Need(Set(projection)=Set(shell) and Length(projection)=Length(shell),"literal outside-to-shell bijection");
 for pair in Combinations([1..Length(outside)],2) do
  isotropic:=norm2(projection[pair[1]]-projection[pair[2]])=z;
  common:=ForAny(flags,f->outside[pair[1]] in f[2] and outside[pair[2]] in f[2]);
  P210Need(isotropic=common,"literal common flag iff isotropic difference");
 od;
 blockres:=P210Connected(outside,flags,function(i,f)return i=f[1];end);
 pointres:=P210Connected(Difference([1..Length(points)],[p]),Filtered(blocks,B->not p in B),function(i,B)return i in B;end);
 flagres:=P210Connected(Difference(L,[p]),Filtered(blocks,B->p in B and B<>L),function(i,B)return not i in B;end);
 global:=P210Connected([1..Length(points)],blocks,function(i,B)return not i in B;end);
 # Explicit unitary matrices in the same hyperbolic coordinates as the proof.
 gens:=[];
 for a in el do for b in el do
  if b+b^q+a^(q+1)=z then
   Add(gens,TransposedMat([[o,-a^q,b],[z,o,a],[z,z,o]]));
  fi;
 od;od;
 Add(gens,[[z,z,o],[z,o,z],[o,z,z]]);
 a:=Z(q^2);Add(gens,DiagonalMat([a,o,a^(-q)]));
 P210Need(ForAll(gens,A->A*J*TransposedMat(bar(A))=J),"each explicit generator unitary");
 perms:=List(gens,A->PermList(List(points,v->Position(points,P210Normalize(v*A)))));
 G:=Group(perms);expected:=q^3*(q^3+1)*(q^2-1);
 P210Need(Size(G)=expected,"explicit unitary subgroup order");
 P210Need(Length(Orbit(G,p))=Length(points),"point transitivity");
 P210Need(Length(Orbit(Stabilizer(G,p),Q))=Length(points)-1,"ordered-pair transitivity");
 H:=Stabilizer(G,[p,Q],OnTuples);
 alternatives:=Filtered(blocks,B->p in B and B<>L);base:=alternatives[1];
 P210Need(Size(H)=q^2-1 and Set(Orbit(H,base,OnSets))=Set(alternatives),"ordered-pair fiber transitivity");
 P210Need(Size(Stabilizer(H,base,OnSets))=1,"literal chamber stabilizer trivial");
 # SU2 roots are enumerated from the actual trace-zero field elements.
 rootgens:=Concatenation(List(Filtered(el,t->t+t^q=z),t->[[o,t],[z,o]]),
                         List(Filtered(el,t->t+t^q=z),t->[[o,z],[t,o]]));
 S:=Group(rootgens);
 P210Need(Size(S)=q*(q^2-1) and Set(Orbit(S,shell[1],OnRight))=Set(shell),"root-generated shell orbit");
 P210Need(ForAll(rootgens,A->ForAll(shell,v->norm2(v*A-v)=z)),"isotropic root moves");
 transportChecks:=0;
 for v in shell do for w in shell do
  x:=v[1];y:=v[2];u:=w[1];r:=w[2];k:=norm2(v);
  T:=[[u*y^q+u^q*y,u*x^q-u^q*x],[r*y^q-r^q*y,r*x^q+r^q*x]]/k;
  P210Need(DeterminantMat(T)=o and T*v=w and TransposedMat(T)*J2*bar(T)=J2,
           "uniform transport specializes to actual unitary matrix");
  transportChecks:=transportChecks+1;
 od;od;
 Print("{\"q\":",q,",\"points\":",Length(points),",\"blocks\":",Length(blocks),
       ",\"block_residue\":",blockres,",\"point_residue\":",pointres,
       ",\"flag_residue\":",flagres,",\"antiincidence\":",global,
       ",\"unitary_action_order\":",Size(G),",\"chamber_stabilizer\":1",
       ",\"ordered_pair_stabilizer\":",Size(H),",\"norm_shell\":",Length(shell),
       ",\"root_orbit\":",Length(Orbit(S,shell[1],OnRight)),
       ",\"transport_pairs\":",transportChecks,"}\n");
end;;
for q in [2,3,4,5] do P210Check(q);od;
Print("PHASE210_LITERAL_AND_UNITARY_PASS\n");
QUIT;
