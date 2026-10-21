# Enumerate edge-transitive subgroups through maximal overgroups.
# Completeness follows from a maximal chain from each desired subgroup to A.
L059Search:=fail;;
L059Descent := function(A,E)
  local reps, nodes, i, H, maximal, children, K, j, ok, reason;
  Need(IsTransitive(A,E,OnSets));
  reps:=[A];nodes:=[];i:=1;
  while i<=Length(reps) do
    H:=reps[i];
    maximal:=MaximalSubgroupClassReps(H);
    children:=[];
    for K in maximal do
      Need(IsSubgroup(H,K) and Size(K)<Size(H));
      if Size(K) mod Length(E)<>0 then
        Add(children,rec(K:=K,reason:="order"));
      elif not IsTransitive(K,E,OnSets) then
        Add(children,rec(K:=K,reason:="edge_orbits"));
      else
        j:=PositionProperty(reps,L->Size(L)=Size(K) and IsConjugate(A,L,K));
        if j=fail then Add(reps,K);j:=Length(reps);fi;
        Add(children,rec(K:=K,reason:="retained_class",target:=j));
      fi;
    od;
    Add(nodes,rec(H:=H,children:=children));
    i:=i+1;
  od;
  L059Search:=rec(nodes:=nodes,method:="maximal_subgroup_descent");
  return List(reps,H->ConjugacyClassSubgroups(A,H));
end;;
