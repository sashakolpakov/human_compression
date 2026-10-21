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
D:=P177Graph("120_034",120,[1, 3, 7, 9, 10, 15, 16, 17, 18, 19, 21, 22, 23, 25, 28, 29, 30, 31, 36, 38, 40, 41, 42, 43, 44, 45, 46, 48, 51, 52, 57, 58, 64, 68, 72, 73, 74, 82, 86, 87, 88, 89, 90, 98, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],[[1, 2], [1, 6], [1, 47], [1, 95], [2, 7], [2, 19], [2, 107], [3, 8], [3, 20], [3, 78], [3, 93], [4, 9], [4, 21], [4, 68], [4, 115], [5, 10], [5, 22], [5, 36], [5, 43], [6, 23], [6, 29], [6, 116], [7, 24], [7, 54], [7, 99], [8, 25], [8, 31], [8, 103], [9, 20], [9, 26], [9, 55], [10, 27], [10, 56], [10, 60], [11, 28], [11, 46], [11, 101], [11, 111], [12, 29], [12, 57], [12, 105], [12, 110], [13, 15], [13, 30], [13, 46], [13, 58], [14, 28], [14, 31], [14, 72], [14, 108], [15, 35], [15, 59], [15, 91], [16, 32], [16, 60], [16, 100], [16, 120], [17, 33], [17, 61], [17, 67], [17, 92], [18, 34], [18, 55], [18, 62], [18, 70], [19, 39], [19, 63], [19, 67], [20, 64], [20, 102], [21, 35], [21, 65], [21, 76], [22, 55], [22, 66], [22, 77], [23, 26], [23, 53], [23, 54], [24, 31], [24, 41], [24, 98], [25, 67], [25, 96], [25, 119], [26, 52], [26, 88], [27, 68], [27, 98], [27, 101], [28, 69], [28, 79], [29, 70], [29, 80], [30, 63], [30, 71], [30, 81], [31, 60], [32, 42], [32, 57], [32, 86], [33, 58], [33, 72], [33, 102], [34, 73], [34, 89], [34, 103], [35, 101], [35, 113], [36, 65], [36, 85], [36, 118], [37, 43], [37, 74], [37, 82], [37, 109], [38, 49], [38, 75], [38, 95], [38, 96], [39, 74], [39, 104], [39, 112], [40, 53], [40, 63], [40, 76], [40, 117], [41, 77], [41, 79], [41, 97], [42, 65], [42, 78], [42, 83], [43, 79], [43, 120], [44, 69], [44, 80], [44, 91], [44, 99], [45, 59], [45, 70], [45, 75], [45, 81], [46, 92], [46, 117], [47, 86], [47, 90], [47, 104], [48, 49], [48, 55], [48, 118], [48, 119], [49, 74], [49, 89], [50, 82], [50, 87], [50, 88], [50, 105], [51, 60], [51, 67], [51, 71], [51, 83], [52, 66], [52, 80], [52, 84], [53, 102], [53, 112], [54, 87], [54, 106], [56, 88], [56, 107], [56, 110], [57, 59], [57, 85], [58, 62], [58, 80], [59, 90], [61, 86], [61, 108], [61, 113], [62, 109], [62, 112], [63, 98], [64, 70], [64, 96], [64, 100], [65, 88], [66, 72], [66, 101], [68, 81], [68, 119], [69, 87], [69, 114], [71, 109], [71, 110], [72, 100], [73, 85], [73, 91], [73, 97], [74, 92], [75, 111], [75, 115], [76, 90], [76, 106], [77, 112], [77, 116], [78, 106], [78, 108], [79, 89], [81, 103], [82, 83], [82, 117], [83, 102], [84, 107], [84, 113], [84, 114], [85, 109], [86, 96], [87, 93], [89, 93], [90, 94], [91, 108], [92, 114], [93, 115], [94, 98], [94, 111], [94, 116], [95, 105], [95, 114], [97, 104], [97, 106], [99, 103], [99, 110], [100, 116], [104, 118], [105, 120], [107, 119], [111, 120], [113, 118], [115, 117]]);;
R:=P177Census(D);;Need(Size(R.F)=2880);;
PrintTo("current_c4_descent/120_034.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_034 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
