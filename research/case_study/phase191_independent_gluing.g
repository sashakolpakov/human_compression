# Independent native-GAP reconstruction of the phase187 example.
# No author code or stored finite table is read. GAP permutations act on the
# right, hence products representing the manuscript compositions are reversed.

Require191 := function(ok, message)
  if not ok then
    Print("PHASE191_REJECT: ", message, "\n");
    QUIT_GAP(1);
  fi;
end;

points := [1..8];;
parts := [
  [[1,2],[3,4],[5,6],[7,8]],
  [[2,3],[4,5],[6,7],[1,8]],
  [[1,2,5,6],[3,4,7,8]],
  [[2,3,6,7],[1,4,5,8]]
];;
parts := List(parts, Set);;
blocks := Concatenation(parts);;
Require191(Length(Set(blocks))=12,"distinct shadows");
Require191(ForAll(parts, p -> SortedList(Concatenation(p))=points),
           "parallel classes partition the point set");

# Native set stabilizer computes the full point action. Shadow separation
# identifies this with the full type-preserving incidence automorphism group.
base := Stabilizer(SymmetricGroup(8),Set(blocks),OnSetsSets);;
Require191(Size(base)=16,"full base group order");
Require191(ForAll(Elements(base),g ->
  ForAll(parts,p -> OnSetsSets(p,g) in parts)),"full group preserves classes");
rho := ActionHomomorphism(base,parts,OnSetsSets);;
H := Image(rho);;
a := (1,2)(3,4);;
b := (1,3)(2,4);;
s := (2,3);;
t := (2,4);;
Require191(Set(Elements(H))=Set([(),a]),"direction image");
Require191(Size(Kernel(rho))=8,"direction kernel order");
alpha := [(),s,t];;
beta := [(),s,t*a];;
cosets := List([1..3],j -> Set(List(Elements(H),h -> alpha[j]^-1*h*beta[j])));;
Require191(cosets=[Set([(),a]),Set([(),b]),Set([a,b])],"literal common lift cosets");
Require191(ForAll(Combinations([1..3],2),ij ->
  Length(Intersection(cosets[ij[1]],cosets[ij[2]]))>0),"pairwise compatibility");
Require191(Length(Intersection(cosets))=0,"no common lift");
Pj := [];; Pk := [];;
for j in [1..3] do
  for k in Difference([1..3],[j]) do
    target := alpha[k]^-1*beta[k]*beta[j]^-1*alpha[j];
    Pj := List(Elements(H),h -> alpha[j]^-1*h*alpha[j]);
    Pk := List(Elements(H),h -> alpha[k]^-1*h*alpha[k]);
    productSet := Set(Concatenation(List(Pk,q -> List(Pj,p -> q*p))));
    Require191(target in productSet,"literal printed product formula");
  od;
od;

Gluing191 := function(match)
  local lines, dirs, x, idx, d, sizes, adj, u, v, j, k, line, f,
        flags, layer, extensions, candidate, residual, seen, frontier,
        next, w, panelCounts, nr, connectedCounts, q;
  # Build all 12^3 tuples first, then apply exactly the source equations.
  # This is distinct from the author program's direction-first construction.
  lines := []; dirs := [];
  for x in Tuples(blocks,3) do
    idx := List([1..3],j -> PositionProperty(parts,p -> x[j] in p));
    d := idx[1]^match[1];
    if ForAll([2,3],j -> idx[j]^match[j]=d) then
      Add(lines,x); Add(dirs,d);
    fi;
  od;
  Require191(Length(Set(lines))=Length(lines),"distinct tuple lines");
  sizes := [8,8,8,Length(lines)];
  adj := List([1..24+Length(lines)],u -> []);
  for j in [1..3] do
    for k in [j+1..3] do
      for u in [1..8] do
        for v in [1..8] do
          Add(adj[8*(j-1)+u],8*(k-1)+v);
          Add(adj[8*(k-1)+v],8*(j-1)+u);
        od;
      od;
    od;
  od;
  for q in [1..Length(lines)] do
    for j in [1..3] do
      for u in lines[q][j] do
        Add(adj[8*(j-1)+u],24+q);
        Add(adj[24+q],8*(j-1)+u);
      od;
    od;
  od;
  adj := List(adj,Set);
  # All cliques are generated recursively, without a prespecified type tuple.
  # A same-type edge cannot occur in this source incidence graph.
  flags := [[[]]];
  for nr in [1..4] do
    layer := [];
    for f in flags[nr] do
      if Length(f)=0 then
        extensions := [1..Length(adj)];
      else
        extensions := Intersection(List(f,u -> adj[u]));
        extensions := Filtered(extensions,u -> u>Maximum(f));
      fi;
      for candidate in extensions do
        Add(layer,Concatenation(f,[candidate]));
      od;
    od;
    Add(flags,layer);
  od;
  panelCounts := [];
  connectedCounts := [0,0,0];
  for nr in [0..3] do
    for f in flags[nr+1] do
      if nr=0 then residual := [1..Length(adj)];
      else residual := Intersection(List(f,u -> adj[u])); fi;
      Require191(Length(residual)>0,"every proper flag extends");
      if nr=3 then
        Add(panelCounts,Length(residual));
        Require191(Length(residual)>=2,"firm panels");
      else
        seen := [residual[1]]; frontier := seen;
        while Length(frontier)>0 do
          next := Difference(Intersection(residual,
                    Union(List(frontier,w -> adj[w]))),seen);
          seen := Union(seen,next); frontier := next;
        od;
        Require191(seen=residual,"residual connectivity");
        connectedCounts[nr+1] := connectedCounts[nr+1]+1;
      fi;
    od;
  od;
  Require191(ForAll(flags[5],f -> Length(Intersection(List(f,u -> adj[u])))=0),
    "rank four and no larger flags");
  return rec(objects:=sizes, lineCounts:=List([1..4],d -> Number(dirs,x -> x=d)),
    flags:=List(flags,Length), connectedByFlagSize:=connectedCounts,
    panels:=Collected(panelCounts));
end;

ga := Gluing191(alpha);;
gb := Gluing191(beta);;
Require191(ga.objects=[8,8,8,112] and gb.objects=[8,8,8,104],"literal object totals");
Require191(ga.lineCounts=[64,16,16,16] and gb.lineCounts=[32,32,32,8],
           "direction line multiplicities");
Print("BASE_ORDER=",Size(base)," DIRECTION_ORDER=",Size(H),
      " KERNEL_ORDER=",Size(Kernel(rho)),"\n");
Print("ALPHA=",ga,"\nBETA=",gb,"\n");

# Bounded independent diagnostic of Proposition3.1: compare orbit-stabilizer
# cardinality with every factorization, for all ordered subgroup triples of S3.
small := SymmetricGroup(3);;
subs := AllSubgroups(small);;
checks := 0;; transitiveCount := 0;;
for ps in Tuples(subs,3) do
  orbitSize := Index(small,Intersection(ps));
  totalSize := Product(ps,p -> Index(small,p));
  factors := ForAll([1..3],k ->
    Size(Intersection(ps{Difference([1..3],[k])}))*Size(ps[k]) /
    Size(Intersection(ps)) = Size(small));
  Require191((orbitSize=totalSize)=factors,"uniqueness criterion diagnostic");
  checks := checks+1;
  if factors then transitiveCount := transitiveCount+1; fi;
od;
Print("UNIQUENESS_SUBGROUP_TRIPLES=",checks," TRANSITIVE=",transitiveCount,"\n");
Print("PHASE191_JSON_BEGIN\n{\"base_order\":",Size(base),
      ",\"direction_order\":",Size(H),",\"kernel_order\":",Size(Kernel(rho)),
      ",\"alpha\":{\"object_counts\":",ga.objects,
      ",\"line_counts\":",ga.lineCounts,",\"flag_counts\":",ga.flags,
      ",\"connected_by_flag_size\":",ga.connectedByFlagSize,
      ",\"panel_counts\":",ga.panels,"},\"beta\":{\"object_counts\":",gb.objects,
      ",\"line_counts\":",gb.lineCounts,",\"flag_counts\":",gb.flags,
      ",\"connected_by_flag_size\":",gb.connectedByFlagSize,
      ",\"panel_counts\":",gb.panels,"},\"uniqueness_subgroup_triples\":",checks,
      ",\"transitive_triples\":",transitiveCount,"}\nPHASE191_JSON_END\n");
Print("PHASE191_NATIVE_GAP_PASS\n");
QUIT_GAP(0);
