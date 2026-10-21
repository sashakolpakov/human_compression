LoadPackage("grape");;
SizeScreen([4096, 4096]);;
P197Need := function(ok, msg)
  if not ok then Print("P197_REJECT ", msg, "\n"); FORCE_QUIT_GAP(1); fi;
end;;
P197Need(IsBound(P197Data), "data path");;
Read(P197Data);;
P197Rows := [];;
P197Adj := [];;
for P197C in P197Cases do
  P197N := P197C.n;;
  P197R := Maximum(P197C.types);;
  P197Adj := List([1..P197N + P197R], x -> []);;
  for P197E in P197C.edges do
    AddSet(P197Adj[P197E[1]], P197E[2]);
    AddSet(P197Adj[P197E[2]], P197E[1]);
  od;
  for P197I in [1..P197N] do
    P197J := P197N + P197C.types[P197I];;
    AddSet(P197Adj[P197I], P197J);
    AddSet(P197Adj[P197J], P197I);
  od;
  P197Graph := Graph(Group(()), [1..P197N + P197R], OnPoints,
    function(x, y) return y in P197Adj[x]; end, true);;
  P197Old := [1..P197N];;
  P197Palette := [P197N + 1..P197N + P197R];;
  P197Corr := AutGroupGraph(P197Graph, [P197Old, P197Palette]);;
  P197Typed := AutGroupGraph(P197Graph,
    Concatenation([P197Old], List(P197Palette, x -> [x])));;
  P197Need([Size(P197Typed), Size(P197Corr)] = P197C.expected,
    Concatenation("group orders ", P197C.name));
  P197Image := Action(P197Corr, P197Palette);;
  P197Need(Size(P197Corr) = Size(P197Typed) * Size(P197Image), "type quotient");
  for P197G in GeneratorsOfGroup(P197Corr) do
    for P197I in P197Old do
      P197Need(P197C.types[P197I ^ P197G] + P197N =
        (P197C.types[P197I] + P197N) ^ P197G, "exact palette action");
    od;
  od;
  Add(P197Rows, Concatenation("{\"name\":\"", P197C.name,
    "\",\"typed\":", String(Size(P197Typed)),
    ",\"correlations\":", String(Size(P197Corr)),
    ",\"type_image\":", String(Size(P197Image)), "}"));
od;
Print("{\"status\":\"PASS_NATIVE_GAP_FULL_GROUPS\",\"rows\":[",
  JoinStringsWithSeparator(P197Rows, ","), "]}\n");;
QUIT;
