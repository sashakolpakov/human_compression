Need:=function(ok) if not ok then Error("L059 subdivision certificate invalid"); fi; end;;
LoadPackage("grape");;

L059SubMax:=function(U,V)
  local degree,action;
  degree:=Index(U,V); Need(degree>1);
  action:=Action(U,RightCosets(U,V),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

L059SubdivisionRows:=function(F,edges,reps)
  local arcs,edge,u,v,rows,H,P,Q,B,row;
  arcs:=Concatenation(List(edges,e->[e,Reversed(e)]));
  edge:=edges[1];u:=edge[1];v:=edge[2];rows:=[];
  Need(IsTransitive(F,arcs,OnTuples));
  for H in reps do
    Need(IsSubgroup(F,H) and IsTransitive(H,arcs,OnTuples));
    P:=Stabilizer(H,u);Q:=Stabilizer(H,edge,OnSets);
    B:=Intersection(P,Q);
    Need(B=Stabilizer(P,v));
    Need(Size(Core(H,B))=1 and ClosureGroup(P,Q)=H);
    Need(Index(P,B)=3 and Index(Q,B)=2);
    row:=rec(H:=H,H0:=P,H1:=Q,B:=B,
      maxcode:=List([[P,B],[Q,B],[H,P],[H,Q]],p->L059SubMax(p[1],p[2])),
      normcode:=List([H,P,Q,B],K->IsNormal(F,K)),dualorder:=0,
      maxorder:=Maximum(List(ConjugacyClasses(H),c->Order(Representative(c)))),
      group_order:=Size(H),subgroup_orders:=List([P,Q,B],Size));
    Add(rows,row);
  od;
  return rows;
end;;

L059SubdivisionFromBipartite:=function(R)
  local F,A,reps,steps,old,K,N,T,x,H,j,tests,rows;
  F:=R.F;A:=R.A;Need(Index(F,A)=2 and IsNormal(F,A));
  reps:=[];steps:=[];
  for old in R.witnesses do
    K:=old.H;N:=Normalizer(F,K);T:=RightTransversal(N,K);tests:=[];
    Need(IsTransitive(K,R.edges,OnSets));
    for x in T do
      if x in A then
        Add(tests,rec(x:=x,reason:="preserves_parts"));
      elif not x^2 in K then
        Add(tests,rec(x:=x,reason:="square_outside_kernel"));
      else
        H:=ClosureGroup(K,x);
        Need(Size(H)=2*Size(K) and Intersection(H,A)=K);
        j:=PositionProperty(reps,L->Size(L)=Size(H) and IsConjugate(F,L,H));
        if j=fail then Add(reps,H);j:=Length(reps);fi;
        Add(tests,rec(x:=x,reason:="retained_class",target:=j));
      fi;
    od;
    Add(steps,rec(K:=K,N:=N,tests:=tests));
  od;
  rows:=L059SubdivisionRows(F,R.edges,reps);
  return rec(label:=R.label,n_original:=R.n,edges_original:=R.edges,
    A_subdivision:=F,witnesses:=rows,
    search:=rec(method:="index_two_normalizer_extension",steps:=steps));
end;;
