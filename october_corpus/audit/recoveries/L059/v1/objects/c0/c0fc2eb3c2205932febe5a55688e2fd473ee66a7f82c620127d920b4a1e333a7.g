Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;
Read("maximal_descent.g");;

# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Need(degree>1);
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
  Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := L059Descent(A,data.edges);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Need(Size(ClosureGroup(H0,H1))=Size(H));
      Need(Size(Core(H,B))=1);
      Need(Index(H,B)=Length(data.edges));
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
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,retained_edge_transitive_classes:=Length(classes),search:=L059Search,witnesses:=witnesses);
end;;


t:=Runtime();;
D:=P177Graph("120_039",120,[1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 66, 67, 68, 69, 70, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 91, 92, 93, 94, 95, 101, 102, 103, 104, 105, 116, 117, 118, 119, 120],[[1, 11], [1, 13], [1, 21], [1, 41], [2, 39], [2, 41], [2, 63], [2, 65], [3, 21], [3, 59], [3, 71], [3, 73], [4, 39], [4, 100], [4, 109], [4, 110], [5, 59], [5, 89], [5, 90], [5, 100], [6, 18], [6, 31], [6, 32], [6, 83], [7, 18], [7, 51], [7, 52], [7, 103], [8, 26], [8, 27], [8, 67], [8, 83], [9, 46], [9, 47], [9, 78], [9, 103], [10, 67], [10, 78], [10, 94], [10, 95], [11, 26], [11, 31], [11, 33], [12, 26], [12, 69], [12, 83], [12, 85], [13, 46], [13, 51], [13, 53], [14, 69], [14, 80], [14, 118], [14, 120], [15, 46], [15, 80], [15, 103], [15, 105], [16, 38], [16, 61], [16, 62], [16, 107], [17, 38], [17, 42], [17, 44], [17, 112], [18, 87], [18, 107], [19, 22], [19, 24], [19, 58], [19, 112], [20, 58], [20, 74], [20, 75], [20, 87], [21, 48], [21, 53], [22, 33], [22, 35], [22, 53], [23, 48], [23, 79], [23, 91], [23, 93], [24, 84], [24, 85], [24, 120], [25, 69], [25, 70], [25, 79], [25, 120], [26, 63], [27, 71], [27, 72], [27, 90], [28, 37], [28, 41], [28, 43], [28, 63], [29, 59], [29, 60], [29, 90], [29, 98], [30, 37], [30, 98], [30, 114], [30, 115], [31, 61], [31, 63], [32, 89], [32, 107], [32, 109], [33, 41], [33, 42], [34, 60], [34, 89], [34, 98], [34, 100], [35, 60], [35, 112], [35, 114], [36, 68], [36, 81], [36, 82], [36, 116], [37, 68], [37, 92], [38, 104], [38, 116], [39, 49], [39, 92], [40, 49], [40, 54], [40, 55], [40, 104], [42, 53], [42, 55], [43, 70], [43, 91], [43, 92], [44, 104], [44, 105], [44, 118], [45, 70], [45, 79], [45, 80], [45, 118], [46, 73], [47, 64], [47, 65], [47, 110], [48, 57], [48, 73], [49, 99], [49, 110], [50, 57], [50, 99], [50, 111], [50, 113], [51, 73], [51, 75], [52, 87], [52, 89], [52, 109], [54, 99], [54, 100], [54, 109], [55, 111], [55, 112], [56, 77], [56, 101], [56, 102], [56, 119], [57, 77], [57, 93], [58, 84], [58, 119], [59, 93], [60, 84], [61, 81], [61, 83], [62, 105], [62, 116], [62, 118], [64, 78], [64, 80], [64, 105], [65, 92], [65, 94], [66, 88], [66, 96], [66, 106], [66, 108], [67, 72], [67, 88], [68, 96], [68, 115], [69, 72], [70, 115], [71, 93], [71, 95], [72, 85], [74, 85], [74, 119], [74, 120], [75, 101], [75, 103], [76, 86], [76, 88], [76, 97], [76, 108], [77, 97], [77, 113], [78, 108], [79, 113], [81, 106], [81, 107], [82, 96], [82, 98], [82, 114], [84, 114], [86, 101], [86, 117], [86, 119], [87, 101], [88, 95], [90, 95], [91, 113], [91, 115], [94, 108], [94, 110], [96, 117], [97, 102], [97, 117], [99, 102], [102, 111], [104, 111], [106, 116], [106, 117]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_039.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_039 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
