# Fresh witness validation. The producer is not loaded.
# Completeness still trusts GAP subgroup classes and GRAPE automorphism groups.
LoadPackage("grape");;
SetAssertionLevel(1);;
Read("phase177_graph_witnesses.g");;

P177CheckMax := function(L,K)
  local cosets, two;
  cosets := RightCosets(L,K);
  two := Length(Orbits(K,cosets,OnRight))=2;
  if two then return "2T"; fi;
  if ForAny(MaximalSubgroupClassReps(L),M->IsConjugate(L,M,K)) then return "M"; fi;
  return "X";
end;;

P177Validate := function(d)
  local graph, A, F, rows, r, H, P, Q, B, elements, conjugates,
        ca, cb, x, y, vx, vy, overlap, maxcode, normcode, duals,
        dualorder, cls, eligible, hits, i, j;
  graph := Graph(Group(()),[1..d.n],OnPoints,
    function(a,b) return Set([a,b]) in d.edges; end,true);
  A := AutGroupGraph(graph,[d.black,d.white]);
  F := AutGroupGraph(graph);
  Assert(1,A=d.A and F=d.F);
  Assert(1,Set(Concatenation(d.black,d.white))=[1..d.n]);
  Assert(1,IsEmpty(Intersection(d.black,d.white)));
  rows := d.witnesses;
  for r in rows do
    H:=r.H; elements:=Elements(H);
    Assert(1,IsSubgroup(A,H));
    Assert(1,Length(Orbit(H,d.base_edge,OnSets))=Length(d.edges));
    P:=Group(Filtered(elements,g->d.b^g=d.b));
    Q:=Group(Filtered(elements,g->d.w^g=d.w));
    B:=Intersection(P,Q);
    Assert(1,P=r.H0 and Q=r.H1 and B=r.B);
    conjugates:=List(elements,g->B^g);
    Assert(1,Size(Intersection(conjugates))=1);
    Assert(1,Size(ClosureGroup(P,Q))=Size(H));
    Assert(1,[Size(H),Size(P),Size(Q),Size(B)] =
      Concatenation([r.group_order],r.subgroup_orders));
    ca:=RightCosets(H,P); cb:=RightCosets(H,Q);
    Assert(1,Set(List(ca,c->d.b^Representative(c)))=d.black);
    Assert(1,Set(List(cb,c->d.w^Representative(c)))=d.white);
    for x in ca do
      for y in cb do
        vx:=d.b^Representative(x); vy:=d.w^Representative(y);
        overlap:=not IsEmpty(Intersection(AsList(x),AsList(y)));
        Assert(1,overlap=(Set([vx,vy]) in d.edges));
      od;
    od;
    maxcode:=List([[P,B],[Q,B],[H,P],[H,Q]],p->P177CheckMax(p[1],p[2]));
    normcode:=List([H,P,Q,B],K->ForAll(Elements(A),g->K^g=K));
    Assert(1,maxcode=r.maxcode and normcode=r.normcode);
    Assert(1,Maximum(List(elements,Order))=r.maxorder);
    duals:=Filtered(Elements(F),g->H^g=H and d.b^g=d.w and d.w^g=d.b);
    if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
    Assert(1,dualorder=r.dualorder);
  od;
  # Every eligible class occurs exactly once; no conjugate duplicates.
  eligible:=0;
  for cls in ConjugacyClassesSubgroups(A) do
    H:=Representative(cls);
    if Length(Orbit(H,d.base_edge,OnSets))=Length(d.edges) then
      eligible:=eligible+1;
      hits:=Number(rows,r->IsConjugate(A,H,r.H));
      Assert(1,hits=1);
    fi;
  od;
  Assert(1,eligible=Length(rows));
  for i in [1..Length(rows)] do
    for j in [i+1..Length(rows)] do
      Assert(1,not IsConjugate(A,rows[i].H,rows[j].H));
    od;
  od;
  Print("VALIDATED ",d.label," ",Length(rows)," markings; all coset incidences, columns, and subgroup-class coverage\n");
  return true;
end;;

Assert(1,List(P177Results,d->[d.label,d.n,Length(d.edges),Size(d.A),Size(d.F),Length(d.witnesses)])=
 [["K3_3",6,9,36,72,5],["K4_4",8,16,576,1152,58],
  ["cube",8,12,24,48,2],["Heawood",14,21,168,336,2],
  ["Petersen_subdivision",25,30,120,120,2]]);
List(P177Results,P177Validate);;
Print("PHASE177_WITNESSES_VALIDATED\n");
QUIT;
