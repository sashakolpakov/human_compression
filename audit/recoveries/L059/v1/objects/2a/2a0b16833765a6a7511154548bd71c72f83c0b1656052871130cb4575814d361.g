L059Need := function(ok) if not ok then Error("L059 exact check failed"); fi; end;;
# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  L059Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  L059Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  L059Need(degree>1);
  action := Action(upper,RightCosets(upper,lower),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

P177Census := function(data)
  local A, F, classes, edge, b, w, witnesses, H, H0, H1, B, D, duals,
        row, cls, maxcode, normcode, maxorder, dualorder, suborders;
  A := AutGroupGraph(data.graph,[data.black,data.white]);
  F := AutGroupGraph(data.graph);
  L059Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := ConjugacyClassesSubgroups(A);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      L059Need(Size(ClosureGroup(H0,H1))=Size(H));
      L059Need(Size(Core(H,B))=1);
      L059Need(Index(H,B)=Length(data.edges));
      maxcode := List([[H0,B],[H1,B],[H,H0],[H,H1]],p->P177Max(p[1],p[2]));
      normcode := List([H,H0,H1,B],K->IsNormal(A,K));
      D := Stabilizer(Normalizer(F,H),edge,OnSets);
      duals := Filtered(Elements(D),g->b^g=w);
      if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
      maxorder := Maximum(List(ConjugacyClasses(H),c->Order(Representative(c))));
      row := rec(H:=H,H0:=H0,H1:=H1,B:=B,maxcode:=maxcode,normcode:=normcode,
                 dualorder:=dualorder,maxorder:=maxorder,
                 group_order:=Size(H),subgroup_orders:=List([H0,H1,B],Size),
                 structure:=List([H,H0,H1,B],StructureDescription));
      Add(witnesses,row);
    fi;
  od;
  Print(data.label," vertices=",data.n," edges=",Length(data.edges)," Aut+=",Size(A),
        " Aut=",Size(F)," subgroup_classes=",Length(classes)," geometries=",Length(witnesses),"\n");
  Print("MAX ",Collected(List(witnesses,r->r.maxcode)),"\n");
  Print("NORM ",Collected(List(witnesses,r->r.normcode)),"\n");
  return rec(label:=data.label,n:=data.n,black:=data.black,white:=data.white,edges:=data.edges,
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,subgroup_classes:=Length(classes),witnesses:=witnesses);
end;;


D:=P177Graph("C4_current_110_7",110,[1..55],[[50, 58], [54, 62], [49, 58], [53, 62], [43, 56], [46, 61], [42, 63], [44, 57], [32, 56], [34, 57], [37, 57], [35, 61], [34, 61], [38, 57], [30, 62], [31, 58], [25, 63], [25, 62], [31, 56], [21, 63], [16, 61], [19, 60], [23, 56], [12, 60], [13, 60], [8, 59], [9, 60], [14, 59], [6, 58], [7, 59], [2, 63], [4, 59], [24, 88], [26, 90], [31, 95], [41, 105], [33, 96], [1, 67], [20, 86], [2, 64], [34, 96], [4, 71], [47, 108], [27, 88], [8, 75], [6, 69], [33, 98], [8, 76], [28, 88], [22, 82], [35, 103], [3, 70], [19, 86], [11, 78], [9, 76], [40, 109], [5, 67], [27, 93], [39, 97], [26, 93], [38, 97], [17, 89], [29, 85], [43, 99], [26, 83], [31, 86], [12, 70], [47, 101], [39, 109], [3, 72], [45, 102], [24, 84], [29, 81], [28, 80], [27, 87], [32, 108], [9, 68], [28, 81], [25, 84], [11, 70], [10, 68], [40, 102], [10, 69], [44, 99], [18, 93], [37, 106], [11, 91], [29, 77], [30, 78], [17, 64], [53, 100], [23, 70], [21, 68], [1, 83], [6, 84], [12, 95], [29, 78], [5, 81], [14, 90], [8, 92], [7, 82], [23, 66], [22, 67], [15, 90], [25, 79], [1, 86], [28, 75], [54, 110], [17, 75], [24, 66], [23, 77], [19, 73], [12, 87], [48, 107], [22, 77], [20, 79], [18, 73], [16, 75], [19, 77], [52, 106], [51, 109], [27, 69], [48, 80], [6, 100], [7, 101], [4, 103], [15, 108], [7, 100], [3, 103], [45, 73], [36, 64], [40, 76], [5, 96], [50, 87], [47, 74], [13, 107], [55, 81], [46, 72], [44, 74], [14, 104], [37, 67], [39, 65], [9, 110], [47, 72], [11, 108], [41, 78], [14, 102], [52, 92], [40, 64], [2, 107], [51, 90], [1, 107], [51, 89], [46, 68], [10, 96], [43, 65], [10, 97], [53, 94], [52, 95], [13, 102], [42, 65], [2, 110], [55, 91], [15, 99], [5, 105], [3, 110], [54, 91], [4, 105], [15, 97], [55, 89], [38, 72], [13, 98], [51, 92], [35, 76], [42, 69], [24, 104], [50, 66], [49, 65], [36, 84], [39, 85], [53, 71], [52, 71], [22, 98], [33, 85], [36, 80], [42, 94], [32, 85], [55, 66], [37, 80], [18, 100], [49, 71], [20, 99], [21, 98], [41, 94], [43, 92], [21, 109], [16, 105], [46, 87], [17, 104], [30, 103], [32, 89], [16, 106], [48, 74], [18, 104], [34, 88], [30, 101], [50, 73], [38, 93], [41, 82], [35, 95], [54, 74], [20, 106], [49, 79], [45, 83], [26, 101], [48, 79], [45, 82], [44, 83], [33, 94], [36, 91]]);;
R:=P177Census(D);;
PrintTo("exception_witnesses.g","L059Exception := ",R,";\n");
Print("L059_EXCEPTION_COMPLETE\n");
QUIT;
