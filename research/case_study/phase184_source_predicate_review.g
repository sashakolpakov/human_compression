# Independent phase184 semantic checks after the hash-bound author program.
# The author constructs the group and object families; the predicates and
# counterexample extension calculation below are independently transcribed.
# This is not an independent construction of the 266-vertex graph.
Check184:=function(b,s) if not b then Error(Concatenation("phase184: ",s));fi;end;;

SourceRelation184:=function(mode,r,s,F,H)
 local K,T,A,B,e,W,O,v,V5,V6;
 if r=0 then
  K:=Pet[Position(Edges,F)];
  if s=1 then
   return ForAll(H[1],v->v in K) and F in H[4];
  elif s=2 then
   e:=H[3];
   if mode=1 then T:=Intersection(K,H[2]);else T:=Intersection(K,H[1]);fi;
   return ForAll(e,v->v in K) and Length(T)=2 and T[2] in Adj[T[1]]
    and ForAll(e,v->ForAll(T,u->Dist[v][u]=2));
  elif mode=1 then
   return H[1] in K and Number(K,v->v in H[3])=3;
  else
   return ForAll(F,v->Dist[v][H]=2)
    and ForAny(White,W->H in W and ForAll(F,v->v in W));
  fi;
 elif r=1 then
  if s=2 then
   if not ForAll(H[3],v->v in F[1]) then return false;fi;
   if mode=1 then
    return Number(F[1],v->v in H[2])=1 and Number(F[2],v->v in H[1])=1;
   else
    return Number(F[1],v->v in H[1])=1 and Number(F[2],v->v in H[2])=1;
   fi;
  elif mode=1 then
   return H[1] in F[1] and Number(F[1],v->v in H[3])=2
    and Number(F[2],v->v in H[2])=1;
  else return H in F[1];fi;
 else
  if mode=1 then return H[1] in F[3] and Number(F[3],v->v in H[3])=1;
  else return H in F[3];fi;
 fi;
end;;

# Every literal binary relation is compared on its complete base neighbourhood.
reviewed184:=0;; base184:=[];;
for mode in [1..2] do
 if mode=1 then sourceFaces184:=[Edges,Quads,Quads,Triples];
 else sourceFaces184:=[Edges,Quads,Quads,V];fi;
 for rs in Combinations([0..3],2) do
  base184:=BaseObjects[mode][rs[1]+1];
  own184:=Filtered(sourceFaces184[rs[2]+1],y->SourceRelation184(mode,rs[1],rs[2],base184,y));
  old184:=Filtered(sourceFaces184[rs[2]+1],y->Incident179(mode,rs[1]+1,rs[2]+1,base184,y));
  Check184(Set(own184)=Set(old184),"literal source predicate disagreement");
  reviewed184:=reviewed184+1;
  Print("REVIEWER_SOURCE_RELATION ",mode," ",rs," ",Length(own184)," PASS\n");
 od;
od;

# Inspect all twelve neighbours of the same source 2-face, not only the
# author's first extra neighbour. The rank-one predicates are literal.
q184:=BaseObjects[1][3];;
facets184:=Filtered(Triples,t->t[1] in q184[3]
 and Difference(q184[3],[t[1]])[1] in t[3]);;
Check184(Length(facets184)=12,"complete twelve-facet count");;
extensions184:=[];; repair184:=[];; induced184:=[];;
for t184 in facets184 do
 ext184:=Filtered(Quads,f->SourceRelation184(1,1,2,f,q184)
  and SourceRelation184(1,1,3,f,t184));
 Add(extensions184,Length(ext184));
 repaired184:=RepairedIncident179(1,3,4,q184,t184);
 Add(repair184,repaired184);
 # A different definition of the repair: the two pentagons must be the
 # orbits of the intersection of the block and pointwise-edge stabilizers.
 blockStabilizer184:=Stabilizer(G,t184,TripleAction);
 endpointStabilizer184:=Stabilizer(G,q184[3],OnTuples);
 D184:=Intersection(blockStabilizer184,endpointStabilizer184);
 orbits184:=Set(List(Orbits(D184,Union(q184[1],q184[2])),Set));
 algebraic184:=orbits184=Set([q184[1],q184[2]]);
 Add(induced184,algebraic184);
 Check184(Size(D184)=10 and algebraic184=repaired184,"algebraic induced-quadruple repair");
 if repaired184 then Check184(Length(ext184)>0,"repaired flag has no extension");
 else Check184(Length(ext184)=0,"extra literal flag unexpectedly extends");fi;
od;
Check184(reviewed184=12 and Number(repair184,x->x)=2,"review coverage");;
Print("REVIEWER_ALL_LITERAL_Q23_EXTENSION_COUNTS ",SortedList(extensions184),"\n");
Print("REVIEWER_ALGEBRAIC_REPAIR_MATCHES_ALL_TWELVE\n");
Print("PHASE184_SEMANTIC_SOURCE_REVIEW_PASS\n");
QUIT;
